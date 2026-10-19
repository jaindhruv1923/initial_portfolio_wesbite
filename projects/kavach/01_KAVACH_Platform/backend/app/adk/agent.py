"""
Google ADK LlmAgent Base Architecture for KAVACH.
Complies with Google Agent Development Kit core specifications:
- Agent (LlmAgent) class
- Agent lifecycle states & transitions (INITIALIZED, PLANNING, EXECUTING_TOOL, REFLECTING, COMPLETED, FAILED)
- 8-Hook-Point Callbacks integration:
    * before_agent_callback / after_agent_callback
    * before_model_callback / after_model_callback / on_model_error_callback
    * before_tool_callback / after_tool_callback / on_tool_error_callback
- Tool context, built-in tools, and custom tool registration
- Function calling with pre/post safety hooks and session state
"""

from enum import Enum
from typing import Dict, Any, List, Callable, Optional
import time
import inspect
from .memory import AgentMemory
from .callbacks import (
    AgentCallbacks,
    ToolCallback,
    ModelCallback,
    CallbackContext,
    ToolContext,
    LlmRequest,
    LlmResponse,
)


class AgentLifecycleState(str, Enum):
    INITIALIZED = "INITIALIZED"
    PLANNING = "PLANNING"
    EXECUTING_TOOL = "EXECUTING_TOOL"
    REFLECTING = "REFLECTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class LlmAgent:
    """
    Standard Google ADK LlmAgent class.
    Encapsulates lifecycle, function calling, memory, and 8-hook security callbacks.
    """
    def __init__(
        self,
        name: str,
        system_instruction: str,
        capabilities: Optional[List[str]] = None,
        memory: Optional[AgentMemory] = None,
        callbacks: Optional[AgentCallbacks] = None,
        output_key: Optional[str] = None,
    ):
        self.name = name
        self.system_instruction = system_instruction
        self.capabilities = capabilities or ["reasoning", "tool_use"]
        self.memory = memory or AgentMemory(session_id=f"session_{name.lower()}")
        self.callbacks = callbacks or AgentCallbacks()
        self.output_key = output_key
        self.lifecycle_state = AgentLifecycleState.INITIALIZED
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def register_tool(
        self,
        name: str,
        func: Callable,
        description: str,
        parameters_schema: Optional[Dict[str, Any]] = None,
    ):
        """Register a custom or built-in tool with schema and context."""
        self.tools[name] = {
            "name": name,
            "func": func,
            "description": description,
            "parameters": parameters_schema or {},
            "doc": inspect.getdoc(func) or description,
        }

    def invoke_tool(
        self,
        tool_name: str,
        context: Optional[CallbackContext] = None,
        **kwargs
    ) -> Any:
        """
        Execute a tool passing through the ADK tool callback lifecycle:
        before_tool_callback -> tool_execution -> after_tool_callback (or on_tool_error_callback).
        """
        if tool_name not in self.tools:
            err = ValueError(f"Tool '{tool_name}' is not registered on agent '{self.name}'")
            if context:
                self.callbacks.trigger_on_tool_error(tool_name, kwargs, context, err)
            else:
                self.callbacks.trigger_tool_error(tool_name, err)
            raise err

        tool_meta = self.tools[tool_name]
        func = tool_meta["func"]

        ctx = context or CallbackContext(agent_name=self.name)
        tool_obj = type("ToolObj", (), {"name": tool_name, "description": tool_meta["description"]})()

        self.lifecycle_state = AgentLifecycleState.EXECUTING_TOOL

        # Hook 6: before_tool_callback (Can return early for Caching / Skipping)
        early_result = self.callbacks.trigger_before_tool(tool_obj, kwargs, ctx)
        if early_result is not None:
            self.memory.transient.record_tool_output(tool_name, early_result)
            return early_result

        start_time = time.time()
        try:
            # Filter kwargs to match func's signature if func does not accept var keyword
            sig = inspect.signature(func)
            has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
            call_kwargs = dict(kwargs)
            if "context" in sig.parameters:
                call_kwargs["context"] = ctx
            elif "ctx" in sig.parameters:
                call_kwargs["ctx"] = ctx

            if not has_var_keyword:
                call_kwargs = {k: v for k, v in call_kwargs.items() if k in sig.parameters}

            result = func(**call_kwargs)

            duration_ms = round((time.time() - start_time) * 1000, 2)

            # Hook 7: after_tool_callback (Can rewrite result, record state delta, save artifacts)
            rewritten_result = self.callbacks.trigger_after_tool(tool_obj, kwargs, ctx, result)
            final_result = rewritten_result if rewritten_result is not None else result

            self.memory.transient.record_tool_output(tool_name, final_result)
            return final_result
        except Exception as e:
            # Hook 8: on_tool_error_callback
            handled = self.callbacks.trigger_on_tool_error(tool_obj, kwargs, ctx, e)
            if handled is not None:
                return handled
            raise

    def execute(
        self,
        task: str,
        context: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Execute task across the formal ADK agent lifecycle:
        1. before_agent_callback (Hook 1 - can skip agent)
        2. Planning phase
        3. before_model_callback (Hook 3 - can intercept/guardrail/cache)
        4. Tool execution (Hooks 6, 7, 8)
        5. after_model_callback (Hook 4 - response rewriting)
        6. Reflection & state delta tracking
        7. after_agent_callback (Hook 2 - final rewrite & state persistence)
        """
        start_time = time.time()

        # Build or wrap context into CallbackContext
        if isinstance(context, CallbackContext):
            ctx = context
            if ctx.agent_name in ("ADK_Agent", ""):
                ctx.agent_name = self.name
        elif isinstance(context, dict):
            ctx = CallbackContext(agent_name=self.name, state=context)
        else:
            ctx = CallbackContext(agent_name=self.name)

        # Hook 1: before_agent_callback (Pattern 06: Conditional Skipping)
        early_agent_skip = self.callbacks.trigger_before_agent(ctx, task)
        if early_agent_skip is not None:
            self.lifecycle_state = AgentLifecycleState.COMPLETED
            return {
                "agent": self.name,
                "state": self.lifecycle_state.value,
                "skipped": True,
                "result": early_agent_skip,
                "session_state": dict(ctx.state),
                "state_delta": ctx.actions.state_delta,
            }

        self.lifecycle_state = AgentLifecycleState.PLANNING
        self.memory.persistent.append_message("user", task, dict(ctx.state))

        plan = [
            f"Understand task: {task[:60]}...",
            f"Query available tools ({', '.join(self.tools.keys()) or 'none'})",
            "Synthesize output with security validation"
        ]
        self.memory.transient.add_thought(f"Planning complete: {len(plan)} steps.")

        # Hook 3: before_model_callback (Pattern 01 Guardrails, Pattern 05 Modification)
        llm_request = LlmRequest(contents=task, system_instruction=self.system_instruction)
        early_model_response = self.callbacks.trigger_before_model(ctx, llm_request)

        model_response_text = ""
        is_refusal = False

        if early_model_response is not None:
            # Model call was intercepted (e.g. guardrail refusal or cached response)
            model_response_text = early_model_response.text
            is_refusal = early_model_response.is_refusal
        else:
            # Normal model / tool simulation
            tool_results = {}
            for tool_name, tool_data in self.tools.items():
                if any(k in task.lower() for k in [tool_name.lower(), "audit", "scan", "check", "search", "tavily", "details"]):
                    try:
                        res = self.invoke_tool(tool_name, context=ctx, text=task, query=task)
                        tool_results[tool_name] = res
                    except TypeError:
                        pass
                    except Exception as e:
                        tool_results[tool_name] = {"error": str(e)}

            model_response_text = f"Agent '{self.name}' completed task based on {len(tool_results)} tool activations."

            # Hook 4: after_model_callback (Pattern 05: Response Modification)
            llm_resp = LlmResponse(text=model_response_text, is_refusal=False)
            rewritten_model_resp = self.callbacks.trigger_after_model(ctx, llm_resp)
            if rewritten_model_resp:
                model_response_text = rewritten_model_resp.text

        self.lifecycle_state = AgentLifecycleState.REFLECTING
        reflection = f"Agent '{self.name}' analyzed task. Refusal: {is_refusal}."
        self.memory.transient.add_thought(reflection)

        self.lifecycle_state = AgentLifecycleState.COMPLETED
        duration_ms = round((time.time() - start_time) * 1000, 2)

        output: Dict[str, Any] = {
            "agent": self.name,
            "state": self.lifecycle_state.value,
            "task": task,
            "plan": plan,
            "response": model_response_text,
            "is_refusal": is_refusal,
            "tool_results": locals().get("tool_results", {}),
            "reflection": reflection,
            "duration_ms": duration_ms,
            "memory": self.memory.persistent.to_dict(),
            "session_state": dict(ctx.state),
            "state_delta": ctx.actions.state_delta,
        }

        # If agent specifies an output_key, write output to state
        if self.output_key:
            ctx.state[self.output_key] = model_response_text
            output["session_state"][self.output_key] = model_response_text

        # Hook 2: after_agent_callback (Pattern 02: Dynamic State Management, Hook 2 inspection)
        rewritten_agent_output = self.callbacks.trigger_after_agent(ctx, output)
        if rewritten_agent_output is not None:
            output = rewritten_agent_output

        self.execution_history.append(output)
        self.memory.persistent.append_message("assistant", reflection, output)
        return output

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "state": self.lifecycle_state.value,
            "capabilities": self.capabilities,
            "registered_tools": list(self.tools.keys()),
            "execution_count": len(self.execution_history),
        }
