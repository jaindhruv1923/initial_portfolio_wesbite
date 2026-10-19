"""
Google ADK (Agent Development Kit) Callbacks Architecture for KAVACH.
Complies with Google ADK Callbacks Design Patterns (adk.dev/callbacks) & CSE3101 Agentic AI:
- Three Phases: Agent Lifecycle, LLM Interaction, Tool Execution
- Eight Hook Points:
    1. before_agent_callback
    2. after_agent_callback
    3. before_model_callback
    4. after_model_callback
    5. on_model_error_callback
    6. before_tool_callback
    7. after_tool_callback
    8. on_tool_error_callback
- Eight Canonical Design Patterns:
    01 Guardrails & Policy Enforcement (before_model, before_tool)
    02 Dynamic State Management (after_tool, context.state, state_delta)
    03 Logging & Monitoring (structured logging across invocation IDs)
    04 Caching (cache key in state, early return cache hit)
    05 Request / Response Modification (system prompt rewrite, response scrubbing)
    06 Conditional Skipping of Steps (early returns to skip agent/model/tool)
    07 Tool-Specific Actions (request_credential, skip_summarization)
    08 Artifact Handling (save_artifact, load_artifact, artifact_delta)
"""

from typing import Callable, Any, Dict, List, Optional
import time
import uuid
import copy


class CallbackActions:
    """Tracks dynamic actions requested by callbacks during execution."""
    def __init__(self):
        self.skip_summarization: bool = False
        self.state_delta: Dict[str, Any] = {}
        self.artifact_delta: List[Dict[str, Any]] = []
        self.credential_requests: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skip_summarization": self.skip_summarization,
            "state_delta": self.state_delta,
            "artifact_delta": self.artifact_delta,
            "credential_requests": self.credential_requests,
        }


class StateProxy(dict):
    """
    Session state wrapper that automatically records mutations into actions.state_delta,
    satisfying Pattern 02 (Dynamic State Management).
    """
    def __init__(self, initial: Optional[Dict[str, Any]] = None, actions: Optional[CallbackActions] = None):
        super().__init__(initial or {})
        self._actions = actions or CallbackActions()

    def __setitem__(self, key: str, value: Any):
        super().__setitem__(key, value)
        if self._actions is not None:
            self._actions.state_delta[key] = value

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for k, v in dict(*args, **kwargs).items():
            if self._actions is not None:
                self._actions.state_delta[k] = v


class CallbackContext:
    """
    Unified Google ADK Callback Context passed to lifecycle hooks.
    Exposes shared state, execution actions, and artifact management.
    """
    def __init__(
        self,
        invocation_id: Optional[str] = None,
        agent_name: str = "ADK_Agent",
        state: Optional[Dict[str, Any]] = None,
    ):
        self.invocation_id = invocation_id or f"inv-{uuid.uuid4().hex[:8]}"
        self.agent_name = agent_name
        self.actions = CallbackActions()
        self.state = StateProxy(state or {}, self.actions)
        self.artifacts_store: Dict[str, Any] = {}

    def request_credential(self, auth_config: Dict[str, Any]):
        """Pattern 07: Handle authentication flows from before_tool_callback."""
        self.actions.credential_requests.append({
            "auth_config": auth_config,
            "timestamp": time.time(),
        })

    def save_artifact(self, name: str, data: Any) -> str:
        """Pattern 08: Save session-related files and data blobs outside state object."""
        self.artifacts_store[name] = data
        delta_entry = {
            "artifact_name": name,
            "size_bytes": len(str(data)),
            "timestamp": time.time(),
        }
        self.actions.artifact_delta.append(delta_entry)
        return name

    def load_artifact(self, name: str) -> Optional[Any]:
        """Pattern 08: Retrieve session-related file or blob."""
        return self.artifacts_store.get(name)


class ToolContext(CallbackContext):
    """Specialized context provided to tool-level callbacks."""
    pass


class LlmRequest:
    """Encapsulates LLM input payload and configuration for model callbacks."""
    def __init__(self, contents: str, system_instruction: str = "", model_name: str = "gemini-2.5"):
        self.contents = contents
        self.config = type("Config", (), {"system_instruction": system_instruction})()
        self.model_name = model_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contents": self.contents,
            "system_instruction": getattr(self.config, "system_instruction", ""),
            "model_name": self.model_name,
        }


class LlmResponse:
    """Encapsulates LLM output or pre-model interception refusal response."""
    def __init__(self, text: str, is_refusal: bool = False, metadata: Optional[Dict[str, Any]] = None):
        self.text = text
        self.is_refusal = is_refusal
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "is_refusal": self.is_refusal,
            "metadata": self.metadata,
        }


# --- Legacy compatibility wrappers ---

class ToolCallback:
    """Legacy tool invocation lifecycle callback."""
    def __init__(
        self,
        on_tool_start: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_tool_end: Optional[Callable[[str, Any, float], None]] = None,
        on_tool_error: Optional[Callable[[str, Exception], None]] = None,
    ):
        self.on_tool_start = on_tool_start
        self.on_tool_end = on_tool_end
        self.on_tool_error = on_tool_error


class ModelCallback:
    """Legacy LLM inference lifecycle callback."""
    def __init__(
        self,
        on_model_start: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_model_end: Optional[Callable[[str, Any, float], None]] = None,
        on_model_error: Optional[Callable[[str, Exception], None]] = None,
    ):
        self.on_model_start = on_model_start
        self.on_model_end = on_model_end
        self.on_model_error = on_model_error


class AgentCallbacks:
    """
    Comprehensive Google ADK 8-Hook-Point Agent Lifecycle Callbacks Manager.
    Exposes hooks for:
      Phase 1 - Agent: before_agent, after_agent
      Phase 2 - Model: before_model, after_model, on_model_error
      Phase 3 - Tool:  before_tool, after_tool, on_tool_error
    """
    def __init__(self):
        # 8 Hook Point Callback lists
        self.before_agent_hooks: List[Callable[[CallbackContext, Any], Optional[Any]]] = []
        self.after_agent_hooks: List[Callable[[CallbackContext, Any], Optional[Any]]] = []

        self.before_model_hooks: List[Callable[[CallbackContext, LlmRequest], Optional[LlmResponse]]] = []
        self.after_model_hooks: List[Callable[[CallbackContext, LlmResponse], Optional[LlmResponse]]] = []
        self.on_model_error_hooks: List[Callable[[CallbackContext, Exception], Optional[Any]]] = []

        self.before_tool_hooks: List[Callable[[Any, Dict[str, Any], CallbackContext], Optional[Dict[str, Any]]]] = []
        self.after_tool_hooks: List[Callable[[Any, Dict[str, Any], CallbackContext, Any], Optional[Any]]] = []
        self.on_tool_error_hooks: List[Callable[[Any, Dict[str, Any], CallbackContext, Exception], Optional[Any]]] = []

        # Legacy callback objects
        self.tool_callbacks: List[ToolCallback] = []
        self.model_callbacks: List[ModelCallback] = []

        # Audit event logs
        self.event_log: List[Dict[str, Any]] = []

    # --- Hook Registration Methods ---

    def register_before_agent(self, fn: Callable[[CallbackContext, Any], Optional[Any]]):
        self.before_agent_hooks.append(fn)

    def register_after_agent(self, fn: Callable[[CallbackContext, Any], Optional[Any]]):
        self.after_agent_hooks.append(fn)

    def register_before_model(self, fn: Callable[[CallbackContext, LlmRequest], Optional[LlmResponse]]):
        self.before_model_hooks.append(fn)

    def register_after_model(self, fn: Callable[[CallbackContext, LlmResponse], Optional[LlmResponse]]):
        self.after_model_hooks.append(fn)

    def register_on_model_error(self, fn: Callable[[CallbackContext, Exception], Optional[Any]]):
        self.on_model_error_hooks.append(fn)

    def register_before_tool(self, fn: Callable[[Any, Dict[str, Any], CallbackContext], Optional[Dict[str, Any]]]):
        self.before_tool_hooks.append(fn)

    def register_after_tool(self, fn: Callable[[Any, Dict[str, Any], CallbackContext, Any], Optional[Any]]):
        self.after_tool_hooks.append(fn)

    def register_on_tool_error(self, fn: Callable[[Any, Dict[str, Any], CallbackContext, Exception], Optional[Any]]):
        self.on_tool_error_hooks.append(fn)

    def register(self, hook_name: str, fn: Callable):
        """Dynamic string-based hook registration for 8 hook points."""
        mapping = {
            "before_agent": self.register_before_agent,
            "after_agent": self.register_after_agent,
            "before_model": self.register_before_model,
            "after_model": self.register_after_model,
            "on_model_error": self.register_on_model_error,
            "before_tool": self.register_before_tool,
            "after_tool": self.register_after_tool,
            "on_tool_error": self.register_on_tool_error,
        }
        clean_name = hook_name.lower().replace("-", "_")
        if clean_name in mapping:
            mapping[clean_name](fn)
        else:
            raise ValueError(f"Unknown hook name '{hook_name}'. Valid: {list(mapping.keys())}")

    # Legacy registration
    def register_tool_callback(self, cb: ToolCallback):
        self.tool_callbacks.append(cb)

    def register_model_callback(self, cb: ModelCallback):
        self.model_callbacks.append(cb)

    # --- Hook Execution Trigger Methods ---

    def trigger_before_agent(self, ctx: CallbackContext, agent_input: Any) -> Optional[Any]:
        """Hook 1: Intercept agent start. Return non-None value to conditionally skip agent (Pattern 06)."""
        self.event_log.append({
            "phase": "agent",
            "hook": "before_agent",
            "invocation_id": ctx.invocation_id,
            "agent": ctx.agent_name,
            "input": str(agent_input)[:100],
            "timestamp": time.time(),
        })
        for hook in self.before_agent_hooks:
            try:
                res = hook(ctx, agent_input)
                if res is not None:
                    return res
            except Exception as e:
                self.event_log.append({"error": f"before_agent exception: {e}"})
        return None

    def trigger_after_agent(self, ctx: CallbackContext, agent_output: Any) -> Any:
        """Hook 2: Inspect or rewrite agent output, update state."""
        current_output = agent_output
        self.event_log.append({
            "phase": "agent",
            "hook": "after_agent",
            "invocation_id": ctx.invocation_id,
            "agent": ctx.agent_name,
            "output_summary": str(current_output)[:100],
            "timestamp": time.time(),
        })
        for hook in self.after_agent_hooks:
            try:
                rewritten = hook(ctx, current_output)
                if rewritten is not None:
                    current_output = rewritten
            except Exception as e:
                self.event_log.append({"error": f"after_agent exception: {e}"})
        return current_output

    def trigger_before_model(self, ctx: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
        """Hook 3: Intercept LLM request. Return LlmResponse to skip model call (Pattern 01 Guardrail / Pattern 04 Caching)."""
        self.event_log.append({
            "phase": "model",
            "hook": "before_model",
            "invocation_id": ctx.invocation_id,
            "model": llm_request.model_name,
            "contents": llm_request.contents[:100],
            "timestamp": time.time(),
        })
        # Legacy trigger
        self.trigger_model_start(llm_request.model_name, {"contents": llm_request.contents})

        for hook in self.before_model_hooks:
            try:
                res = hook(ctx, llm_request)
                if res is not None:
                    return res
            except Exception as e:
                self.event_log.append({"error": f"before_model exception: {e}"})
        return None

    def trigger_after_model(self, ctx: CallbackContext, llm_response: LlmResponse) -> LlmResponse:
        """Hook 4: Inspect or rewrite LLM response (Pattern 05)."""
        current_res = llm_response
        self.event_log.append({
            "phase": "model",
            "hook": "after_model",
            "invocation_id": ctx.invocation_id,
            "response_text": current_res.text[:100],
            "is_refusal": current_res.is_refusal,
            "timestamp": time.time(),
        })
        # Legacy trigger
        self.trigger_model_end("llm_model", current_res.text, 0.0)

        for hook in self.after_model_hooks:
            try:
                rewritten = hook(ctx, current_res)
                if rewritten is not None:
                    current_res = rewritten
            except Exception as e:
                self.event_log.append({"error": f"after_model exception: {e}"})
        return current_res

    def trigger_on_model_error(self, ctx: CallbackContext, error: Exception) -> Optional[Any]:
        """Hook 5: Handle LLM inference failures."""
        self.event_log.append({
            "phase": "model",
            "hook": "on_model_error",
            "invocation_id": ctx.invocation_id,
            "error": str(error),
            "timestamp": time.time(),
        })
        for hook in self.on_model_error_hooks:
            try:
                res = hook(ctx, error)
                if res is not None:
                    return res
            except Exception:
                pass
        return None

    def trigger_before_tool(self, tool: Any, args: Dict[str, Any], ctx: CallbackContext) -> Optional[Dict[str, Any]]:
        """Hook 6: Intercept tool call. Return dict to skip real tool execution (Pattern 04 Caching, Pattern 06 Quota Skip)."""
        tool_name = getattr(tool, "name", str(tool))
        self.event_log.append({
            "phase": "tool",
            "hook": "before_tool",
            "invocation_id": ctx.invocation_id,
            "tool": tool_name,
            "args": copy.deepcopy(args),
            "timestamp": time.time(),
        })
        # Legacy trigger
        self.trigger_tool_start(tool_name, args)

        for hook in self.before_tool_hooks:
            try:
                res = hook(tool, args, ctx)
                if res is not None:
                    return res
            except Exception as e:
                self.event_log.append({"error": f"before_tool exception: {e}"})
        return None

    def trigger_after_tool(self, tool: Any, args: Dict[str, Any], ctx: CallbackContext, tool_response: Any) -> Any:
        """Hook 7: Dynamic state updates (state_delta), artifact savings, rewriting."""
        tool_name = getattr(tool, "name", str(tool))
        current_res = tool_response
        self.event_log.append({
            "phase": "tool",
            "hook": "after_tool",
            "invocation_id": ctx.invocation_id,
            "tool": tool_name,
            "result_summary": str(current_res)[:100],
            "timestamp": time.time(),
        })
        # Legacy trigger
        self.trigger_tool_end(tool_name, tool_response, 0.0)

        for hook in self.after_tool_hooks:
            try:
                rewritten = hook(tool, args, ctx, current_res)
                if rewritten is not None:
                    current_res = rewritten
            except Exception as e:
                self.event_log.append({"error": f"after_tool exception: {e}"})
        return current_res

    def trigger_on_tool_error(self, tool: Any, args: Dict[str, Any], ctx: CallbackContext, error: Exception) -> Optional[Any]:
        """Hook 8: Handle tool execution failure."""
        tool_name = getattr(tool, "name", str(tool))
        self.event_log.append({
            "phase": "tool",
            "hook": "on_tool_error",
            "invocation_id": ctx.invocation_id,
            "tool": tool_name,
            "error": str(error),
            "timestamp": time.time(),
        })
        # Legacy trigger
        self.trigger_tool_error(tool_name, error)

        for hook in self.on_tool_error_hooks:
            try:
                res = hook(tool, args, ctx, error)
                if res is not None:
                    return res
            except Exception:
                pass
        return None

    # --- Legacy Trigger Methods (Maintained for backward compatibility) ---

    def trigger_tool_start(self, tool_name: str, args: Dict[str, Any]):
        for cb in self.tool_callbacks:
            if cb.on_tool_start:
                try:
                    cb.on_tool_start(tool_name, args)
                except Exception:
                    pass

    def trigger_tool_end(self, tool_name: str, result: Any, duration_ms: float):
        for cb in self.tool_callbacks:
            if cb.on_tool_end:
                try:
                    cb.on_tool_end(tool_name, result, duration_ms)
                except Exception:
                    pass

    def trigger_tool_error(self, tool_name: str, error: Exception):
        for cb in self.tool_callbacks:
            if cb.on_tool_error:
                try:
                    cb.on_tool_error(tool_name, error)
                except Exception:
                    pass

    def trigger_model_start(self, model_name: str, prompt_meta: Dict[str, Any]):
        for cb in self.model_callbacks:
            if cb.on_model_start:
                try:
                    cb.on_model_start(model_name, prompt_meta)
                except Exception:
                    pass

    def trigger_model_end(self, model_name: str, response: Any, duration_ms: float):
        for cb in self.model_callbacks:
            if cb.on_model_end:
                try:
                    cb.on_model_end(model_name, response, duration_ms)
                except Exception:
                    pass
