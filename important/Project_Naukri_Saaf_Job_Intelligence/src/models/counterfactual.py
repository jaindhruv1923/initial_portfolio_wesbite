"""
Counterfactual Explanation & Applicant Defense Engine
=====================================================
Computes actionable counterfactual perturbations:
"What minimal changes would convert this suspected phantom posting
into an authentic, high-confidence genuine job opening?"

Generates actionable recruiter remediation recommendations and
applicant defense advisories.
"""

from typing import Dict, Any, List

class CounterfactualExplainer:
    def __init__(self):
        pass

    def explain_counterfactuals(
        self,
        current_prob: float,
        days_live: float,
        salary_disclosed: bool,
        desc_length_words: int,
        employer_repost_count: int,
        company_completeness: float
    ) -> Dict[str, Any]:
        """
        Calculates counterfactual shifts across the primary risk drivers.
        """
        prob = float(current_prob)
        perturbations = []
        
        # 1. Salary Disclosure Perturbation
        if not salary_disclosed:
            delta_sal = -0.22 * min(1.0, prob / 0.5)
            new_p = max(0.02, prob + delta_sal)
            perturbations.append({
                "action": "Disclose Compensation Range",
                "remediation": "Publish clear, competitive base salary band with <2.5x spread.",
                "risk_reduction_pct": round(abs(delta_sal) * 100.0, 1),
                "resulting_probability": round(new_p, 3)
            })

        # 2. Requisition Age Refresh Perturbation
        if days_live > 45:
            delta_age = -0.18 * (days_live / 90.0)
            new_p = max(0.02, prob + delta_age)
            perturbations.append({
                "action": "Refresh Requisition Lifecycle",
                "remediation": f"Close dormant opening ({days_live:.0f} days live) and re-open only if active hiring budget is confirmed.",
                "risk_reduction_pct": round(abs(delta_age) * 100.0, 1),
                "resulting_probability": round(new_p, 3)
            })

        # 3. Description Depth & Specificity Perturbation
        if desc_length_words < 200:
            delta_desc = -0.14
            new_p = max(0.02, prob + delta_desc)
            perturbations.append({
                "action": "Enrich Description Depth",
                "remediation": "Expand skeletal copy with concrete technical deliverables and specific day-to-day team responsibilities.",
                "risk_reduction_pct": round(abs(delta_desc) * 100.0, 1),
                "resulting_probability": round(new_p, 3)
            })

        # 4. Repost Frequency Moderation
        if employer_repost_count >= 3:
            delta_repost = -0.16
            new_p = max(0.02, prob + delta_repost)
            perturbations.append({
                "action": "Moderate Repost Velocity",
                "remediation": f"Halt serial multi-portal automated syndication ({employer_repost_count} reposts detected).",
                "risk_reduction_pct": round(abs(delta_repost) * 100.0, 1),
                "resulting_probability": round(new_p, 3)
            })

        # 5. Company Completeness
        if company_completeness < 50:
            delta_co = -0.10
            new_p = max(0.02, prob + delta_co)
            perturbations.append({
                "action": "Authenticate Employer Profile",
                "remediation": "Complete official company registration, verify LinkedIn page, and provide verified ATS career URL.",
                "risk_reduction_pct": round(abs(delta_co) * 100.0, 1),
                "resulting_probability": round(new_p, 3)
            })

        # Cumulative Optimal Remediation
        total_delta = sum([p["risk_reduction_pct"] for p in perturbations]) / 100.0
        best_possible_prob = max(0.04, prob - total_delta)
        status_after_fix = "Genuine" if best_possible_prob < 0.35 else ("Suspect" if best_possible_prob < 0.65 else "Ghost")

        return {
            "initial_calibrated_prob": round(prob, 3),
            "individual_counterfactuals": perturbations,
            "best_attainable_prob": round(best_possible_prob, 3),
            "attainable_status": status_after_fix,
            "remediation_summary": f"Applying all {len(perturbations)} remediations would decrease phantom probability from {prob*100:.1f}% to {best_possible_prob*100:.1f}% (achieving '{status_after_fix}' status)."
        }

# Singleton instance
counterfactual_explainer = CounterfactualExplainer()
