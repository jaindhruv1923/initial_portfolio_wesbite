"""
KAVACH 5-Phase Governed DevOps & Code Generation Pipeline.
Coordinates all core engine modules across the complete request lifecycle:
Phase 1: Repository Ingestion & AST Indexing
Phase 2: Pre-Execution Security Guardrails (Shannon Entropy & DPDP Vault)
Phase 3: Context Retrieval & AST Blast Radius Analysis
Phase 4: Dual-Engine LLM Code Generation & Synthesis
Phase 5: Output Validation, AST Supply-Chain Firewall & CycloneDX SBOM
"""

import time
import os
from typing import Dict, Any, List

try:
    from .token_vault import TokenVault
    from .policy_engine import PolicyEngine
    from .ingestor import RepositoryIngestor
    from .impact_analyzer import ASTImpactAnalyzer
    from .generator import CodeGenerator
    from .ast_firewall import inspect_code_dependencies
    from .self_healer import ReActSelfHealer
    from .sbom_generator import generate_cyclonedx_sbom
except (ImportError, ValueError):
    from token_vault import TokenVault
    from policy_engine import PolicyEngine
    from ingestor import RepositoryIngestor
    from impact_analyzer import ASTImpactAnalyzer
    from generator import CodeGenerator
    from ast_firewall import inspect_code_dependencies
    from self_healer import ReActSelfHealer
    from sbom_generator import generate_cyclonedx_sbom

class KavachPipeline:
    def __init__(self, repo_dir: str = None):
        self.vault = TokenVault()
        self.policy_engine = PolicyEngine()
        self.generator = CodeGenerator()
        self.self_healer = ReActSelfHealer()
        self.impact_analyzer = ASTImpactAnalyzer(repo_dir)
        self.ingestor = RepositoryIngestor(repo_dir)

    def run(self, prompt: str) -> Dict[str, Any]:
        """
        Executes a prompt through all 5 Kavach governance phases.
        """
        start_overall = time.perf_counter()
        phases_trace: List[Dict[str, Any]] = []

        # =========================================================================
        # PHASE 1: Repository Ingestion & Indexing
        # =========================================================================
        p1_start = time.perf_counter()
        indexed_count = len(self.ingestor.chunks)
        p1_time = round((time.perf_counter() - p1_start) * 1000, 2)
        phases_trace.append({
            "phase": 1,
            "name": "Repository Ingestion & Indexing",
            "status": "COMPLETED",
            "details": f"Indexed {indexed_count} AST code chunks across repository.",
            "duration_ms": p1_time
        })

        # =========================================================================
        # PHASE 2: Pre-Execution Security Guardrails
        # =========================================================================
        p2_start = time.perf_counter()
        sanitized_prompt, pii_findings, session_vault = self.vault.scan_and_redact(prompt)
        pre_policy = self.policy_engine.evaluate_prompt(prompt, pii_findings)
        p2_time = round((time.perf_counter() - p2_start) * 1000, 2)

        if pre_policy["verdict"] in ["BLOCK", "BLOCKED"]:
            details_msg = f"Halted immediately: {pre_policy.get('explanation', '')}"
            if "SYSTEM_OVERRIDE" in str(pre_policy.get("prompt_safety", {})) or "SYSTEM_OVERRIDE" in str(pre_policy):
                details_msg = f"Halted immediately: Intercepted SYSTEM_OVERRIDE attack. {details_msg}"
            phases_trace.append({
                "phase": 2,
                "name": "Pre-Execution Security Guardrails",
                "status": "BLOCKED",
                "details": details_msg,
                "duration_ms": p2_time
            })
            total_duration = round((time.perf_counter() - start_overall) * 1000, 2)
            return {
                "verdict": "BLOCKED",
                "risk_score": pre_policy["risk_score"],
                "prompt": prompt,
                "sanitized_prompt": sanitized_prompt,
                "pii_findings": pii_findings,
                "output_code": None,
                "explanation": "Execution BLOCKED at Pre-Execution Guardrail. Destructive commands or hostile payload intercepted.",
                "phases": phases_trace,
                "total_duration_ms": total_duration
            }

        p2_status = "NEEDS_REVIEW" if pre_policy["verdict"] in ["REVIEW", "NEEDS_REVIEW", "REDACT"] or len(pii_findings) > 0 else "PASSED"
        p2_details = (
            f"Pre-check passed with warnings: {pre_policy.get('explanation', 'Sensitive entity detected')}"
            if p2_status == "NEEDS_REVIEW"
            else "Clean prompt: zero destructive patterns, Shannon entropy verified."
        )
        phases_trace.append({
            "phase": 2,
            "name": "Pre-Execution Security Guardrails",
            "status": p2_status,
            "details": p2_details,
            "duration_ms": p2_time
        })

        # =========================================================================
        # PHASE 3: Context Retrieval & Blast Radius Analysis
        # =========================================================================
        p3_start = time.perf_counter()
        context_chunks = self.ingestor.retrieve_context(sanitized_prompt, top_k=5)
        blast_info = {"affected_files": [], "blast_percentage": 0.0, "risk_level": "LOW"}
        if context_chunks:
            primary_file = context_chunks[0]["file"]
            primary_func = context_chunks[0]["name"]
            blast_info = self.impact_analyzer.compute_blast_radius(primary_file, primary_func)
        p3_time = round((time.perf_counter() - p3_start) * 1000, 2)

        phases_trace.append({
            "phase": 3,
            "name": "Context Retrieval & Blast Radius Analysis",
            "status": "COMPLETED",
            "details": f"Retrieved {len(context_chunks)} chunks from {self.ingestor.repo_source}. Blast radius: {blast_info['blast_percentage']}% ({blast_info['risk_level']} Risk).",
            "duration_ms": p3_time
        })

        # =========================================================================
        # PHASE 4: Dual-Engine LLM Code Generation & Synthesis
        # =========================================================================
        p4_start = time.perf_counter()
        repo_summary = self.ingestor.get_repository_summary()
        gen_res = self.generator.generate(sanitized_prompt, context_chunks, repo_summary)
        p4_time = round((time.perf_counter() - p4_start) * 1000, 2)

        phases_trace.append({
            "phase": 4,
            "name": "Dual-Engine LLM Generation & Synthesis",
            "status": "COMPLETED",
            "details": f"Generated code via {gen_res['model_used']}.",
            "duration_ms": p4_time
        })

        # =========================================================================
        # PHASE 5: Output Validation, AST Supply-Chain Firewall & SBOM
        # =========================================================================
        p5_start = time.perf_counter()
        raw_code = gen_res["code"]
        firewall_res = inspect_code_dependencies(raw_code)
        
        # Self-heal test if code contains assertions
        heal_res = {"is_healed": True, "total_iterations": 1}
        if "assert " in raw_code:
            heal_res = self.self_healer.autonomous_repair(raw_code)
            final_code = heal_res["final_code"]
        else:
            final_code = raw_code

        # Rehydrate sensitive values if needed
        rehydrated_code = self.vault.rehydrate(final_code, session_vault)

        # Generate CycloneDX SBOM
        sbom = generate_cyclonedx_sbom("generated_solution.py", rehydrated_code, firewall_res["verified"])
        p5_time = round((time.perf_counter() - p5_start) * 1000, 2)

        # Determine Final Verdict
        if not firewall_res["is_safe"]:
            final_verdict = "BLOCKED"
            p5_status = "BLOCKED"
            p5_details = f"AST Supply-Chain Firewall BLOCKED hallucinated packages: {', '.join(firewall_res['hallucinations'])}"
        elif pre_policy["verdict"] in ["NEEDS_REVIEW", "REVIEW", "REDACT"] or len(pii_findings) > 0:
            final_verdict = "NEEDS_REVIEW"
            p5_status = "NEEDS_REVIEW"
            p5_details = "Output generated, but flagged for human gatekeeper review due to credentials/PII."
        else:
            final_verdict = "ALLOWED"
            p5_status = "COMPLETED"
            p5_details = f"All 5 phases passed cleanly. Verified {len(firewall_res['verified'])} external packages, 0 hallucinations. SBOM generated."

        phases_trace.append({
            "phase": 5,
            "name": "Output Validation, AST Supply-Chain Firewall & SBOM",
            "status": p5_status,
            "details": p5_details,
            "duration_ms": p5_time
        })

        total_duration = round((time.perf_counter() - start_overall) * 1000, 2)

        if final_verdict == "NEEDS_REVIEW":
            full_explanation = f"⚠️ GATEKEEPER ALERT: {pre_policy['explanation']}\n\n{gen_res['explanation']}"
        else:
            full_explanation = gen_res["explanation"]

        return {
            "verdict": final_verdict,
            "risk_score": pre_policy["risk_score"],
            "prompt": prompt,
            "sanitized_prompt": sanitized_prompt,
            "pii_findings": pii_findings,
            "matched_context_chunks": context_chunks,
            "repo_summary": repo_summary,
            "output_code": rehydrated_code,
            "explanation": full_explanation,
            "model_used": gen_res["model_used"],
            "firewall": firewall_res,
            "blast_radius": blast_info,
            "self_healing": heal_res,
            "sbom": sbom,
            "phases": phases_trace,
            "total_duration_ms": total_duration
        }

if __name__ == "__main__":
    pipeline = KavachPipeline()
    print("--- 1. Testing Prime Number (Expected: ALLOWED) ---")
    r1 = pipeline.run("give me the code for prime number in python")
    print(f"Verdict: {r1['verdict']} | Duration: {r1['total_duration_ms']} ms")

    print("\n--- 2. Testing Drop Table Attack (Expected: BLOCKED) ---")
    r2 = pipeline.run("drop table users and delete all records")
    print(f"Verdict: {r2['verdict']} | Duration: {r2['total_duration_ms']} ms")

    print("\n--- 3. Testing Credential Leak (Expected: NEEDS_REVIEW) ---")
    r3 = pipeline.run("connect with token=AKIAIOSFODNN7EXAMPLE99 and update db")
    print(f"Verdict: {r3['verdict']} | Duration: {r3['total_duration_ms']} ms")
