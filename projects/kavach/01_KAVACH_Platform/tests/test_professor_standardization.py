"""
KAVACH Test Suite: Professor Pranshu Tiwari's 11 Project Review Minimum Requirements.
Strictly verifies that all 11 standardization criteria are implemented with 100% compliance:

 1. Context Sharing & State Updates: Intermediate outputs feed into downstream agents,
    shared state context, comparison of 4 messaging architectures, and Hover Blackboard Architecture.
 2. Tool Integration using MCP: At least 2 external tools (web search, database lookup, file parser, calculator).
 3. Structured Output using Pydantic: Final output rendered in Markdown, Table, and JSON formats.
 4. Agentic Design Patterns: Comparative evaluation matrix across 5 agentic design patterns.
 5. Task Monitoring & Logging using Callbacks: ADK 8-hook callbacks tracking flow, state delta, and errors.
 6. Agent-to-Agent (A2A) Protocol Interoperability: Direct communication between Google ADK and CrewAI.
 7. Strict Framework Restriction: Exclusively Google ADK and CrewAI agentic frameworks.
 8. System Security, Guardrails & Prompt Variances: Tool return type validation, toxic/abusive parsing,
    prompt injection defense, and 6-way prompt variance evaluation (ReAct vs Few-Shot across 3 personas).
 9. Observability & Cryptographic Provenance Tracing: NIST FIPS 202 SHA3-512 Merkle leaf audit trails.
 10. End-to-End Multi-Run Performance Evaluation: Latency, token metrics, cost in USD/INR across runs.
 11. Cloud Platform Deployment Readiness: Multi-service containerization and health probe verification.
"""

import os
import sys
import pytest
import time
import json
from pydantic import BaseModel

# Ensure Kavach backend is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.agent.blackboard import HoverBlackboard, BlackboardPartition, compare_messaging_architectures
from app.mcp.server import handle_mcp_request, MCP_TOOLS
from app.agent.structured_output import AgentStructuredReport, AgentStepOutput, GuardrailVerdict, ExecutionMetrics, OutputFormat
from app.a2a.interop_bridge import AdkCrewInteropBridge
from app.a2a.protocol import A2AMessage, A2AMessageType, global_a2a_bus
from app.adk.agent import LlmAgent, AgentLifecycleState
from app.adk.callbacks import AgentCallbacks, CallbackContext
from app.crew.agents import CrewAgent
from app.security.prompt_variance_engine import (
    PromptVarianceGenerator,
    PromptArchitecture,
    PersonaType,
    validate_tool_return_type,
    parse_toxic_and_abusive_language
)
from app.security.injection_shield import inspect_prompt_safety
from app.observability.e2e_performance_benchmarker import E2EPerformanceBenchmarker


# ==============================================================================
# REQUIREMENT 1: CONTEXT SHARING, STATE UPDATES & HOVER BLACKBOARD ARCHITECTURE
# ==============================================================================

def test_req1_hover_blackboard_context_sharing():
    """Point 1: Intermediate outputs must feed from one agent to another via Hover Blackboard."""
    blackboard = HoverBlackboard()
    
    # Agent 1 (ADK Triage) posts intermediate triage finding
    entry1 = blackboard.post(
        partition=BlackboardPartition.INTERMEDIATE_OUTPUTS,
        author_agent="ADK_Triage_Agent",
        title="Sanitization Verdict",
        payload={"sanitized_sql": "SELECT * FROM accounts WHERE id = 101;", "entropy": 3.42},
        target_agent="CrewAI_Auditor",
        hover_summary="[ADK Triage] Sanitized input string, calculated Shannon entropy 3.42."
    )
    assert entry1.entry_id is not None
    assert len(entry1.state_hash) == 16
    
    # Agent 2 reads intermediate output fed by Agent 1
    feed = blackboard.get_latest_output_for("CrewAI_Auditor")
    assert feed is not None
    assert feed.author_agent == "ADK_Triage_Agent"
    assert feed.payload["sanitized_sql"] == "SELECT * FROM accounts WHERE id = 101;"
    
    # Export Hover UI state and verify partitions
    hover_view = blackboard.export_hover_view()
    assert hover_view["total_entries"] >= 1
    assert any(p["partition_name"] == BlackboardPartition.INTERMEDIATE_OUTPUTS for p in hover_view["partitions"])


def test_req1_messaging_architectures_benchmark():
    """Point 1: Different Messaging Architectures must be tried and compared."""
    benchmark = compare_messaging_architectures()
    assert "architectures" in benchmark
    assert benchmark["evaluated_architectures_count"] == 4
    
    # Verify Blackboard Architecture is benchmarked
    arch_names = list(benchmark["architectures"].keys())
    assert any("Blackboard" in name for name in arch_names)
    assert any("A2A" in name for name in arch_names)
    assert any("Pub/Sub" in name for name in arch_names)
    assert any("SAGA" in name for name in arch_names)
    assert "verdict" in benchmark


# ==============================================================================
# REQUIREMENT 2: TOOL INTEGRATION USING MCP (MINIMUM 2 EXTERNAL TOOLS)
# ==============================================================================

def test_req2_mcp_tool_web_search():
    """Point 2: MCP Tool 1 - Web search API / PyPI live knowledge lookup."""
    req = {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/call",
        "params": {
            "name": "mcp_web_search",
            "arguments": {"query": "fastapi"}
        }
    }
    resp = handle_mcp_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert "result" in resp
    assert "results" in resp["result"]
    assert len(resp["result"]["results"]) >= 1


def test_req2_mcp_tool_database_lookup():
    """Point 2: MCP Tool 2 - Database / vector store audit ledger lookup."""
    req = {
        "jsonrpc": "2.0",
        "id": 102,
        "method": "tools/call",
        "params": {
            "name": "mcp_database_lookup",
            "arguments": {"query": "KYC_VERIFICATION", "limit": 3}
        }
    }
    resp = handle_mcp_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert "result" in resp
    assert "records" in resp["result"]
    assert len(resp["result"]["records"]) >= 1


def test_req2_mcp_tool_file_parser():
    """Point 2: MCP Tool 3 - Static AST file parser and dependency extractor."""
    sample_code = "import hashlib\n\ndef calculate_hash(data: str) -> str:\n    return hashlib.sha256(data.encode()).hexdigest()\n"
    req = {
        "jsonrpc": "2.0",
        "id": 103,
        "method": "tools/call",
        "params": {
            "name": "mcp_file_parser",
            "arguments": {"filename": "crypto_util.py", "source_code": sample_code}
        }
    }
    resp = handle_mcp_request(req)
    ast_info = resp["result"]["ast_details"]
    assert ast_info["syntax_valid"] is True
    assert "calculate_hash" in ast_info["functions"]
    assert "hashlib" in ast_info["imports"]


def test_req2_mcp_tool_calculator():
    """Point 2: MCP Tool 4 - Calculator (CVSS, Shannon Entropy, Basel III ratios)."""
    # Test CVSS calculation
    cvss_req = {
        "jsonrpc": "2.0",
        "id": 104,
        "method": "tools/call",
        "params": {
            "name": "mcp_calculator",
            "arguments": {"operation": "cvss", "params": {"impact": 5.9, "exploitability": 3.9}}
        }
    }
    cvss_resp = handle_mcp_request(cvss_req)
    assert cvss_resp["result"]["calculation"]["cvss_base_score"] == 9.8
    assert cvss_resp["result"]["calculation"]["severity"] == "CRITICAL"

    # Test Shannon Entropy calculation
    ent_req = {
        "jsonrpc": "2.0",
        "id": 105,
        "method": "tools/call",
        "params": {
            "name": "mcp_calculator",
            "arguments": {"operation": "entropy", "params": {"text": "AKIAIOSFODNN7EXAMPLESECRETKEY12345"}}
        }
    }
    ent_resp = handle_mcp_request(ent_req)
    assert ent_resp["result"]["calculation"]["entropy_value"] > 3.0


# ==============================================================================
# REQUIREMENT 3: STRUCTURED OUTPUT USING PYDANTIC (MARKDOWN, TABLE, JSON)
# ==============================================================================

def test_req3_structured_output_formats():
    """Point 3: Final output must be generated in structured Markdown, Table, and JSON formats."""
    step1 = AgentStepOutput(
        step_number=1,
        agent_name="ADK_Gatekeeper",
        framework="Google ADK",
        action_type="INPUT_PARSING",
        output_summary="Parsed request and validated parameters",
        duration_ms=12.4
    )
    step2 = AgentStepOutput(
        step_number=2,
        agent_name="CrewAI_Auditor",
        framework="CrewAI",
        action_type="SECURITY_AUDIT",
        output_summary="Verified cryptographic tokens and zero-trust policy",
        duration_ms=25.8
    )
    report = AgentStructuredReport(
        report_id="P3-TEST-REPORT-001",
        task_goal="Verify user credentials and execute settlement",
        execution_status="SUCCESS",
        summary="Task executed cleanly across ADK and CrewAI.",
        primary_agent="ADK_Gatekeeper (Google ADK)",
        collaborating_agents=["CrewAI_Auditor (CrewAI)"],
        steps=[step1, step2],
        security=GuardrailVerdict(is_safe=True, risk_score=0.01, cryptographic_seal="SEAL-TEST-999"),
        metrics=ExecutionMetrics(
            total_duration_ms=38.2,
            tokens_consumed=184,
            estimated_cost_usd=0.000027,
            estimated_cost_inr=0.0023,
            merkle_leaf_hash="a1b2c3d4e5f67890"
        )
    )

    # 1. Format: Markdown
    md_output = report.to_markdown()
    assert md_output.startswith("# KAVACH Multi-Agent Governance Report")
    assert "| Step | Agent | Framework |" in md_output
    assert "ADK_Gatekeeper" in md_output

    # 2. Format: Table
    tbl_output = report.to_table()
    assert isinstance(tbl_output, list)
    assert len(tbl_output) == 2
    assert tbl_output[0]["Step"] == 1
    assert tbl_output[0]["Framework"] == "Google ADK"
    assert tbl_output[1]["Framework"] == "CrewAI"

    # 3. Format: JSON
    json_output = report.to_json_dict()
    assert isinstance(json_output, dict)
    assert json_output["report_id"] == "P3-TEST-REPORT-001"
    assert json_output["security"]["cryptographic_seal"] == "SEAL-TEST-999"


# ==============================================================================
# REQUIREMENT 4: AGENTIC DESIGN PATTERNS COMPARATIVE EVALUATION
# ==============================================================================

def test_req4_agentic_design_patterns_evaluation():
    """Point 4: Implement suitable agentic design patterns and evaluate against alternatives."""
    matrix = E2EPerformanceBenchmarker.compare_agentic_design_patterns()
    assert matrix["evaluated_patterns_count"] == 5
    
    patterns = matrix["patterns"]
    assert "ReAct (Reasoning + Acting)" in patterns
    assert "Plan-and-Solve / Graph-of-Thought (GoT)" in patterns
    assert "Hover Blackboard Architecture" in patterns
    assert "Hierarchical Multi-Agent Crew" in patterns
    assert "Human-in-the-Loop (HITL) Gate" in patterns
    
    # Check that each pattern has empirical metrics
    for name, p_data in patterns.items():
        assert "mean_latency_ms" in p_data
        assert "token_overhead" in p_data
        assert "error_resilience" in p_data
        assert "primary_use_case" in p_data


# ==============================================================================
# REQUIREMENT 5: TASK MONITORING & LOGGING USING CALLBACK FUNCTIONS
# ==============================================================================

def test_req5_task_monitoring_callbacks():
    """Point 5: Agents must include a monitoring mechanism tracking intermediate outputs, flows, errors."""
    callbacks = AgentCallbacks()
    events_logged = []

    # Custom monitoring hooks
    def monitor_before_agent(ctx, task):
        events_logged.append({"event": "BEFORE_AGENT", "task": task[:30]})
        return None

    def monitor_after_agent(ctx, output):
        events_logged.append({"event": "AFTER_AGENT", "state_keys": list(ctx.actions.state_delta.keys())})
        return output

    callbacks.register("before_agent", monitor_before_agent)
    callbacks.register("after_agent", monitor_after_agent)

    agent = LlmAgent(
        name="Monitored_Sentinel",
        system_instruction="Monitor all intermediate task flows and execute state updates.",
        callbacks=callbacks
    )

    ctx = CallbackContext(agent_name="Monitored_Sentinel")
    ctx.state["pre_auth"] = True
    result = agent.execute("Execute payment audit", context=ctx)

    assert result["agent"] == "Monitored_Sentinel"
    assert len(events_logged) == 2
    assert events_logged[0]["event"] == "BEFORE_AGENT"
    assert events_logged[1]["event"] == "AFTER_AGENT"


# ==============================================================================
# REQUIREMENTS 6 & 7: A2A PROTOCOL INTEROP & STRICT FRAMEWORK RESTRICTION
# ==============================================================================

def test_req6_and_7_a2a_interoperability_adk_and_crewai():
    """Points 6 & 7: Interoperability between Google ADK and CrewAI using A2A Protocol."""
    bridge = AdkCrewInteropBridge()
    
    # Execute workflow across both frameworks
    report = bridge.execute_interop_workflow(
        task_instruction="Enforce DPDP Act data minimization on customer records",
        code_snippet="def process_customer(c): return {'aadhaar': c.get('aadhaar'), 'name': c.get('name')}"
    )

    assert report.execution_status == "SUCCESS"
    assert len(report.steps) == 2
    
    # Step 1 must be Google ADK
    assert report.steps[0].framework == "Google ADK"
    assert "ADK" in report.steps[0].agent_name
    
    # Step 2 must be CrewAI
    assert report.steps[1].framework == "CrewAI"
    assert "CrewAI" in report.steps[1].agent_name
    
    # Must have cryptographic Merkle leaf hash and seal
    assert report.metrics.merkle_leaf_hash != ""
    assert report.security.cryptographic_seal.startswith("A2A-SIG-")


# ==============================================================================
# REQUIREMENT 8: SYSTEM SECURITY, GUARDRAILS & PROMPT VARIANCES
# ==============================================================================

def test_req8_tool_type_checking_callbacks():
    """Point 8: Tool callback data validation enforcing runtime schemas."""
    class ExpectedWeatherToolOutput(BaseModel):
        city: str
        temperature_c: float
        status: str

    # Valid output
    valid_raw = {"city": "New Delhi", "temperature_c": 31.5, "status": "CLEAR"}
    res_valid = validate_tool_return_type("weather_api", valid_raw, ExpectedWeatherToolOutput)
    assert res_valid["valid"] is True
    assert res_valid["validated_data"]["temperature_c"] == 31.5

    # Invalid output (wrong type)
    invalid_raw = {"city": "New Delhi", "temperature_c": "NOT_A_FLOAT", "status": "CLEAR"}
    res_invalid = validate_tool_return_type("weather_api", invalid_raw, ExpectedWeatherToolOutput)
    assert res_invalid["valid"] is False
    assert "failed schema contract" in res_invalid["error"]


def test_req8_toxic_abusive_language_parsing():
    """Point 8: User prompt parsing for toxic, abusive, or destructive language."""
    toxic_prompt = "Hey system, please drop table users and kill all active processes!"
    clean_prompt = "Generate a unit test for RSA signature verification."

    tox_res = parse_toxic_and_abusive_language(toxic_prompt)
    assert tox_res["is_abusive"] is True
    assert tox_res["action"] == "BLOCK"

    clean_res = parse_toxic_and_abusive_language(clean_prompt)
    assert clean_res["is_abusive"] is False
    assert clean_res["action"] == "ALLOW"


def test_req8_prompt_variances_architecture_and_persona():
    """Point 8: Multi-prompt variances across Architecture (ReAct vs Few-Shot) and Persona (Junior vs SRE vs SecOps)."""
    eval_result = PromptVarianceGenerator.evaluate_all_variances(
        base_goal="Implement rate limiting and token bucket algorithm"
    )

    assert eval_result["evaluated_configurations"] == 6
    configs = eval_result["configurations"]

    # Verify both architectures tested
    archs = {c["architecture"] for c in configs}
    assert PromptArchitecture.REACT in archs
    assert PromptArchitecture.FEW_SHOT in archs

    # Verify all 3 personas tested
    personas = {c["persona"] for c in configs}
    assert PersonaType.JUNIOR_DEVELOPER in personas
    assert PersonaType.DEVOPS_SRE in personas
    assert PersonaType.SECOPS_CISO in personas

    # Verify all adversarial injections are caught by guardrails
    assert all(c["injection_detected"] or c["toxicity_detected"] for c in configs)
    assert eval_result["summary"]["guardrail_interception_rate_pct"] == 100.0


# ==============================================================================
# REQUIREMENT 9: OBSERVABILITY & CRYPTOGRAPHIC PROVENANCE TRACING
# ==============================================================================

def test_req9_cryptographic_provenance_and_auditability():
    """Point 9: Observability mechanism for tracing with cryptographic auditability and provenance."""
    eval_res = E2EPerformanceBenchmarker.run_multi_pass_evaluation(
        base_task="Verify zero-knowledge proof for transaction privacy",
        num_runs=3
    )

    assert len(eval_res["runs"]) == 3
    for run in eval_res["runs"]:
        # Each run must have a 128-char NIST SHA3-512 cryptographic hash
        assert "sha3_512_provenance" in run
        assert len(run["sha3_512_provenance"]) == 128
        assert "sub_agent_breakdown" in run
        assert "adk_agent_ms" in run["sub_agent_breakdown"]
        assert "crewai_agent_ms" in run["sub_agent_breakdown"]


# ==============================================================================
# REQUIREMENT 10: END-TO-END PERFORMANCE EVALUATION, COST & RUNTIME ESTIMATES
# ==============================================================================

def test_req10_e2e_performance_and_cost_estimates():
    """Point 10: End-to-end performance evaluation, cost and running time estimates for multiple runs."""
    eval_res = E2EPerformanceBenchmarker.run_multi_pass_evaluation(
        base_task="Execute Basel III Liquidity Coverage Ratio check",
        num_runs=4
    )

    assert eval_res["total_runs"] == 4
    metrics = eval_res["aggregate_metrics"]
    
    # Running time estimate
    assert metrics["mean_running_time_ms"] > 0
    # Token count
    assert metrics["total_tokens_consumed"] > 0
    # Cost in USD
    assert metrics["total_cost_usd"] > 0
    # Cost in INR
    assert metrics["total_cost_inr"] > 0
    # Verified conversion rate
    assert metrics["total_cost_inr"] == round(metrics["total_cost_usd"] * 86.50, 4)
    assert metrics["overall_success_rate_pct"] == 100.0


# ==============================================================================
# REQUIREMENT 11: CLOUD PLATFORM DEPLOYMENT READINESS
# ==============================================================================

def test_req11_cloud_deployment_configuration():
    """Point 11: Docker Compose and cloud configuration files exist with multi-service architecture."""
    workspace_dir = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
    if not os.path.isfile(os.path.join(workspace_dir, "docker-compose.yml")):
        workspace_dir = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
    docker_compose_path = os.path.join(workspace_dir, "docker-compose.yml")
    
    assert os.path.isfile(docker_compose_path), "docker-compose.yml must exist at project root"
    
    with open(docker_compose_path, "r", encoding="utf-8") as f:
        compose_content = f.read()

    # Must define all 3 platform services
    assert "kavach-platform" in compose_content
    assert "bharat-core-banking" in compose_content
    assert "results-cockpit" in compose_content
    
    # Must specify port mappings
    assert "8000:8000" in compose_content
    assert "8050:8050" in compose_content
    assert "8090:8090" in compose_content


def test_req11_enterprise_multi_target_deployments():
    """Verify that all 5 advanced enterprise deployment targets are configured and valid."""
    workspace_dir = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
    if not os.path.isdir(os.path.join(workspace_dir, "k8s")):
        workspace_dir = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))

    # 1. Kubernetes manifests
    k8s_dir = os.path.join(workspace_dir, "k8s")
    assert os.path.isdir(k8s_dir), "k8s directory must exist"
    for k8s_file in ["namespace.yaml", "configmap.yaml", "kavach-deployment.yaml", "ingress.yaml", "kustomization.yaml"]:
        assert os.path.isfile(os.path.join(k8s_dir, k8s_file)), f"{k8s_file} must exist in k8s/"

    # 2. Terraform IaC manifests
    tf_dir = os.path.join(workspace_dir, "terraform")
    assert os.path.isdir(tf_dir), "terraform directory must exist"
    for tf_file in ["main.tf", "alb.tf", "ecs.tf", "variables.tf", "outputs.tf"]:
        assert os.path.isfile(os.path.join(tf_dir, tf_file)), f"{tf_file} must exist in terraform/"

    # 3. Google Cloud Run manifests
    gcp_dir = os.path.join(workspace_dir, "deploy", "gcp")
    assert os.path.isdir(gcp_dir), "deploy/gcp directory must exist"
    assert os.path.isfile(os.path.join(gcp_dir, "cloudbuild.yaml")), "cloudbuild.yaml must exist in deploy/gcp/"
    assert os.path.isfile(os.path.join(gcp_dir, "deploy_cloud_run.ps1")), "deploy_cloud_run.ps1 must exist in deploy/gcp/"

    # 4. Hugging Face Spaces manifests
    hf_dir = os.path.join(workspace_dir, "deploy", "huggingface")
    assert os.path.isdir(hf_dir), "deploy/huggingface directory must exist"
    hf_readme = os.path.join(hf_dir, "README.md")
    assert os.path.isfile(hf_readme), "README.md must exist in deploy/huggingface/"
    with open(hf_readme, "r", encoding="utf-8") as f:
        hf_content = f.read()
    assert "sdk: docker" in hf_content
    assert "app_port: 8000" in hf_content

    # 5. Live Edge Tunnel scripts
    assert os.path.isfile(os.path.join(workspace_dir, "run_live_cloud_tunnel.ps1")), "run_live_cloud_tunnel.ps1 must exist"
    assert os.path.isfile(os.path.join(workspace_dir, "run_live_cloud_tunnel.bat")), "run_live_cloud_tunnel.bat must exist"

