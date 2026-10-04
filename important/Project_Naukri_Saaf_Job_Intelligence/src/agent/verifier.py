"""
Autonomous Listing Verification Agent (Multi-Tool Analytical Reasoning)
========================================================================
Orchestrates 4 deterministic analytical tools to conduct end-to-end
forensic investigations of job postings.

Outputs cited verdicts with evidence bullets and actionable applicant advice.
Runs 100% locally and free with zero external paid API dependencies.
"""

from typing import Dict, Any, List
from src.agent.tools import (
    ml_scorer_tool,
    semantic_duplicate_tool,
    company_history_tool,
    salary_benchmark_tool
)

class ListingVerificationAgent:
    def __init__(self, agent_name: str = "Naukri Saaf Forensic Agent v4"):
        self.agent_name = agent_name

    def investigate(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes multi-tool investigation and synthesizes evidence into a verdict.
        """
        title = listing.get("job_title", listing.get("title", "Unknown Role"))
        company = listing.get("company_name", "Unknown Employer")
        desc = listing.get("description_text", "")
        days_live = float(listing.get("days_live", 14.0))
        sal_min = listing.get("salary_min")
        sal_max = listing.get("salary_max")
        city = listing.get("location_city", "Bangalore")
        
        # Tool Execution Trace
        tool_trace = []
        
        # 1. Machine Learning Probability Scorer
        ml_res = ml_scorer_tool(listing)
        tool_trace.append({
            "tool": "ml_scorer_tool",
            "finding": f"Calibrated Ghost Probability: {ml_res['calibrated_ghost_prob']*100:.1f}%, Primary SHAP Driver: {ml_res['top_shap_driver']}"
        })
        
        # 2. Semantic Cross-Company Duplicate Detector
        dup_res = semantic_duplicate_tool(desc, company)
        tool_trace.append({
            "tool": "semantic_duplicate_tool",
            "finding": f"Max Cross-Company Similarity: {dup_res['max_cross_company_similarity']:.2f}, Syndicated: {dup_res['is_syndicated']}"
        })
        
        # 3. Employer Historical Repost Analyzer
        hist_res = company_history_tool(company)
        tool_trace.append({
            "tool": "company_history_tool",
            "finding": f"Employer History: {hist_res['total_postings_found']} postings found, Historical Ghost Rate: {hist_res['historical_ghost_rate']*100:.1f}%"
        })
        
        # 4. Salary Transparency & Market Benchmark
        sal_res = salary_benchmark_tool(title, sal_min, sal_max, city)
        tool_trace.append({
            "tool": "salary_benchmark_tool",
            "finding": sal_res["assessment"]
        })
        
        # Multi-factor Evidence Synthesis
        evidence_points = []
        ghost_signals_count = 0
        
        # Evaluate ML score
        if ml_res["calibrated_ghost_prob"] >= 0.70:
            evidence_points.append(f"ML Classifier flags high phantom risk ({ml_res['calibrated_ghost_prob']*100:.1f}%) driven by {ml_res['top_shap_driver']}.")
            ghost_signals_count += 2
        elif ml_res["calibrated_ghost_prob"] >= 0.50:
            evidence_points.append(f"ML Classifier indicates moderate risk ({ml_res['calibrated_ghost_prob']*100:.1f}%).")
            ghost_signals_count += 1
            
        # Evaluate Days Live
        if days_live >= 60:
            evidence_points.append(f"Requisition is severely aged ({days_live:.0f} days live) with no closing or refresh.")
            ghost_signals_count += 2
            
        # Evaluate Syndication
        if dup_res["is_syndicated"]:
            evidence_points.append(f"Job description appears syndicated with other recruitment agencies (similarity: {dup_res['max_cross_company_similarity']:.2f}).")
            ghost_signals_count += 2
            
        # Evaluate Repost Velocity
        if hist_res["total_postings_found"] >= 5 and hist_res["historical_ghost_rate"] >= 0.4:
            evidence_points.append(f"Employer shows high repost velocity ({hist_res['total_postings_found']} postings) with {hist_res['historical_ghost_rate']*100:.1f}% historical ghost rate.")
            ghost_signals_count += 1
            
        # Evaluate Salary
        if not sal_res["salary_disclosed"]:
            evidence_points.append("Compensation is completely undisclosed.")
            ghost_signals_count += 1
        elif not sal_res["salary_range_valid"]:
            evidence_points.append(f"Salary spread is unrealistically wide ({sal_res['salary_spread_ratio']}x ratio).")
            ghost_signals_count += 1
            
        # Synthesize Final Verdict
        if ghost_signals_count >= 3 or ml_res["calibrated_ghost_prob"] >= 0.75:
            final_status = "Ghost"
            confidence = "High" if ghost_signals_count >= 4 else "Moderate"
            advice = "High likelihood of an unmonitored or phantom posting. Do not prioritize applying; verify if the role is still active on the employer's official career portal."
        elif ghost_signals_count >= 1 or ml_res["calibrated_ghost_prob"] >= 0.50:
            final_status = "Suspect"
            confidence = "Moderate"
            advice = "Exercise caution. Check whether the employer is actively hiring and compare requested qualifications against standard industry expectations."
        else:
            final_status = "Genuine"
            confidence = "High"
            advice = "Legitimate active requisition with normal lifespan, specific requirements, and positive transparency signals."
            evidence_points.append("Listing shows healthy hiring activity and authentic corporate copy.")
            
        return {
            "listing_id": listing.get("listing_id", "live_check"),
            "company_name": company,
            "job_title": title,
            "agent_verdict": final_status,
            "agent_is_ghost": (final_status == "Ghost"),
            "confidence": confidence,
            "calibrated_ml_prob": ml_res["calibrated_ghost_prob"],
            "evidence_bullets": evidence_points,
            "actionable_advice": advice,
            "investigation_trace": tool_trace
        }
