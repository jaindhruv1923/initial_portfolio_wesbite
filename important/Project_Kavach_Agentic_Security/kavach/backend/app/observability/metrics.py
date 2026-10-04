"""
Kavach Observability & Token Cost Telemetry Engine.

Tracks real-time platform metrics:
1. Request throughput & policy verdicts (ALLOWED, BLOCKED, REVIEW).
2. Input/Output token usage & real-time cost estimation ($ USD).
3. Latency instrumentation (security screening, AST parsing, RAG retrieval).
4. Prometheus OpenMetrics format export.
"""

import json
import os
import time
from typing import Dict, Any


class ObservabilityCollector:
    def __init__(self, seed_from_disk: bool = False):
        self.start_time = time.time()
        self.total_requests = 0
        self.allowed_requests = 0
        self.blocked_requests = 0
        self.needs_review_requests = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_latency_seconds = 0.0
        self.threats_blocked_by_type: Dict[str, int] = {
            "PII": 0,
            "INJECTION": 0,
            "HALLUCINATED_PACKAGE": 0,
            "SECRET_LEAK": 0
        }
        self.healed_code_runs = 0
        if seed_from_disk:
            self._seed_from_disk()

    def _seed_from_disk(self):
        try:
            runs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "workflow_runs.json"))
            if os.path.exists(runs_path):
                with open(runs_path, "r", encoding="utf-8") as f:
                    runs = json.load(f)
                if isinstance(runs, list):
                    for r in runs:
                        self.total_requests += 1
                        duration_s = (r.get("duration_ms") or 500.0) / 1000.0
                        self.total_latency_seconds += duration_s
                        v = (r.get("verdict") or "ALLOWED").upper()
                        if "BLOCK" in v:
                            self.blocked_requests += 1
                        elif "REVIEW" in v:
                            self.needs_review_requests += 1
                        else:
                            self.allowed_requests += 1

                        category = (r.get("run_type") or "").lower()
                        if "pii" in category:
                            self.threats_blocked_by_type["PII"] += 1
                        elif "secret" in category:
                            self.threats_blocked_by_type["SECRET_LEAK"] += 1
                        elif "hallucinat" in category:
                            self.threats_blocked_by_type["HALLUCINATED_PACKAGE"] += 1
                        elif "inject" in category:
                            self.threats_blocked_by_type["INJECTION"] += 1
                        elif "heal" in category:
                            self.healed_code_runs += 1

                        p_text = r.get("request_text", "")
                        g_res = r.get("generation_result", {})
                        g_text = g_res.get("code", "") if isinstance(g_res, dict) else ""
                        self.input_tokens += max(1, len(p_text) // 4)
                        self.output_tokens += max(1, len(g_text) // 4) if g_text else 10
        except Exception as e:
            print(f"ObservabilityCollector seed error: {e}")

    def record_request(
        self,
        decision: str,
        latency_sec: float,
        prompt_text: str = "",
        generated_text: str = "",
        threat_type: str = None
    ):
        self.total_requests += 1
        self.total_latency_seconds += latency_sec

        decision_upper = (decision or "ALLOWED").upper()
        if "BLOCK" in decision_upper:
            self.blocked_requests += 1
        elif "REVIEW" in decision_upper:
            self.needs_review_requests += 1
        else:
            self.allowed_requests += 1

        if threat_type and threat_type in self.threats_blocked_by_type:
            self.threats_blocked_by_type[threat_type] += 1

        # Heuristic token counting: ~4 chars per token
        if prompt_text:
            self.input_tokens += max(1, len(prompt_text) // 4)
        if generated_text:
            self.output_tokens += max(1, len(generated_text) // 4)

    def record_self_healing(self):
        self.healed_code_runs += 1

    def get_summary(self) -> Dict[str, Any]:
        avg_latency_ms = (
            round((self.total_latency_seconds / self.total_requests) * 1000, 2)
            if self.total_requests > 0
            else 0.0
        )
        # Gemini 2.5/Flash-Lite pricing: $0.075 / 1M input tokens, $0.30 / 1M output tokens
        cost_usd = (self.input_tokens * 0.000000075) + (self.output_tokens * 0.00000030)

        uptime_seconds = int(time.time() - self.start_time)

        return {
            "uptime_seconds": uptime_seconds,
            "total_requests": self.total_requests,
            "verdicts": {
                "allowed": self.allowed_requests,
                "blocked": self.blocked_requests,
                "needs_review": self.needs_review_requests
            },
            "threats_neutralized": self.threats_blocked_by_type,
            "self_healed_runs": self.healed_code_runs,
            "tokens": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "total_tokens": self.input_tokens + self.output_tokens,
                "estimated_cost_usd": round(cost_usd, 6),
                "estimated_cost_cents": round(cost_usd * 100, 4)
            },
            "performance": {
                "avg_latency_ms": avg_latency_ms,
                "total_latency_sec": round(self.total_latency_seconds, 3)
            }
        }

    def export_prometheus(self) -> str:
        s = self.get_summary()
        lines = [
            "# HELP kavach_requests_total Total requests processed by Kavach",
            "# TYPE kavach_requests_total counter",
            f"kavach_requests_total {s['total_requests']}",
            f"kavach_requests_allowed_total {s['verdicts']['allowed']}",
            f"kavach_requests_blocked_total {s['verdicts']['blocked']}",
            "",
            "# HELP kavach_tokens_total Total tokens processed",
            "# TYPE kavach_tokens_total counter",
            f"kavach_tokens_input_total {s['tokens']['input_tokens']}",
            f"kavach_tokens_output_total {s['tokens']['output_tokens']}",
            f"kavach_estimated_cost_usd {s['tokens']['estimated_cost_usd']}",
            "",
            "# HELP kavach_self_healed_total Code units autonomously healed",
            "# TYPE kavach_self_healed_total counter",
            f"kavach_self_healed_total {s['self_healed_runs']}",
        ]
        return "\n".join(lines) + "\n"


global_metrics = ObservabilityCollector(seed_from_disk=True)
