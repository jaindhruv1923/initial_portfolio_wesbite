"""
Token & Cost Financial Circuit Breaker Engine for KAVACH Enterprise v3.0.
Prevents runaway multi-agent loops, unbounded token spend, and latency starvation
by enforcing hard budget ceilings across each workflow execution stage.
"""

from typing import Dict, Any, Optional
import time


class BudgetGuardrailEngine:
    """Enforces financial and resource rate-limiting ceilings."""

    DEFAULT_MAX_TOKENS = 4000
    DEFAULT_MAX_STAGE_MS = 15000  # 15s
    DEFAULT_MAX_COST_USD = 0.05   # $0.05 per individual developer request

    def __init__(
        self,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        max_cost_usd: float = DEFAULT_MAX_COST_USD,
        max_stage_ms: float = DEFAULT_MAX_STAGE_MS
    ):
        self.max_tokens = max_tokens
        self.max_cost_usd = max_cost_usd
        self.max_stage_ms = max_stage_ms
        self.pricing_per_1k_tokens = 0.00025  # Blended tier estimate

    def evaluate_budget(
        self,
        tokens_consumed: int,
        duration_ms: float,
        stage_name: str = "orchestration"
    ) -> Dict[str, Any]:
        """
        Evaluate if current stage resource consumption is within safe operational bounds.
        """
        cost_usd = round((tokens_consumed / 1000.0) * self.pricing_per_1k_tokens, 6)

        token_breached = tokens_consumed > self.max_tokens
        latency_breached = duration_ms > self.max_stage_ms
        cost_breached = cost_usd > self.max_cost_usd

        is_circuit_open = token_breached or latency_breached or cost_breached

        reasons = []
        if token_breached:
            reasons.append(f"Token ceiling exceeded: {tokens_consumed} > {self.max_tokens}")
        if latency_breached:
            reasons.append(f"Latency timeout breached: {duration_ms}ms > {self.max_stage_ms}ms")
        if cost_breached:
            reasons.append(f"Financial threshold exceeded: ${cost_usd} > ${self.max_cost_usd}")

        return {
            "stage": stage_name,
            "tokens_consumed": tokens_consumed,
            "max_tokens_allowed": self.max_tokens,
            "duration_ms": duration_ms,
            "cost_usd": cost_usd,
            "max_cost_allowed": self.max_cost_usd,
            "circuit_breaker_tripped": is_circuit_open,
            "status": "CIRCUIT_BREAKER_TRIPPED" if is_circuit_open else "WITHIN_BUDGET",
            "reasons": reasons,
            "enforcement_action": "HALT_EXECUTION" if is_circuit_open else "ALLOW"
        }


global_budget_engine = BudgetGuardrailEngine()
