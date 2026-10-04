"""
Transparent Fair Pay & Market Compensation Estimator
====================================================
Estimates realistic market compensation bands (P25, P50 Median, P75)
for roles lacking salary disclosure, and audits listed ranges for
clickbait spreads and lowball exploitation.
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class SalaryFairPayEstimator:
    # Role base compensation medians (INR per annum for mid-level 3-5 yrs)
    ROLE_BASELINES = {
        "machine learning": 1800000.0,
        "data scientist": 1600000.0,
        "data analyst": 950000.0,
        "data engineer": 1500000.0,
        "software engineer": 1400000.0,
        "backend": 1500000.0,
        "frontend": 1200000.0,
        "full stack": 1400000.0,
        "devops": 1600000.0,
        "cloud": 1500000.0,
        "product manager": 2200000.0,
        "qa engineer": 850000.0,
        "business analyst": 1050000.0,
        "security": 1700000.0
    }

    CITY_TIER_MULTIPLIERS = {
        "bangalore": 1.20,
        "bengaluru": 1.20,
        "hyderabad": 1.05,
        "pune": 1.00,
        "mumbai": 1.15,
        "delhi": 1.10,
        "gurgaon": 1.12,
        "noida": 1.05,
        "chennai": 0.95,
        "remote": 1.10
    }

    def estimate_fair_compensation(
        self,
        job_title: str,
        city: str = "Bangalore",
        years_exp: float = 3.5,
        listed_min: Optional[float] = None,
        listed_max: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Estimates expected compensation bands and evaluates listed salary realism.
        """
        title_lower = job_title.lower() if job_title else ""
        city_lower = city.lower() if city else "bangalore"

        # Determine base median from matching role keywords
        base_sal = 1100000.0  # default tech baseline
        matched_role = "General Technology"
        for role_kw, sal in self.ROLE_BASELINES.items():
            if role_kw in title_lower:
                base_sal = sal
                matched_role = role_kw.title()
                break

        # Adjust for city tier
        city_mult = 1.0
        for c_kw, mult in self.CITY_TIER_MULTIPLIERS.items():
            if c_kw in city_lower:
                city_mult = mult
                break

        # Adjust for years of experience (approx. +12% per year over baseline 3 yrs)
        exp_factor = max(0.6, 1.0 + (years_exp - 3.0) * 0.12)

        median_annual = base_sal * city_mult * exp_factor
        p25_annual = median_annual * 0.80
        p75_annual = median_annual * 1.30

        # Evaluate listed salary if provided
        audit_verdict = "Salary Undisclosed (Estimated via Market Forensics)"
        is_realistic = True
        spread_ratio = 1.0

        if listed_min and listed_max and listed_max > 0:
            spread_ratio = round(listed_max / max(1.0, listed_min), 2)
            if spread_ratio > 3.5:
                audit_verdict = f"⚠️ Suspiciously Wide Clickbait Spread ({spread_ratio}x spread between min and max)"
                is_realistic = False
            elif listed_max < p25_annual * 0.60:
                audit_verdict = "⚠️ Severe Lowball / Sub-market Exploitative Range"
                is_realistic = False
            elif listed_min > p75_annual * 2.5:
                audit_verdict = "⚠️ Unrealistically High Compensation (Potential Clickbait / Phishing Lure)"
                is_realistic = False
            else:
                audit_verdict = "✅ Realistic Market Range Consistent with Industry Standards"
                is_realistic = True
        elif listed_max and listed_max > 0:
            audit_verdict = "Single Max Salary Disclosed (Partial Transparency)"

        return {
            "matched_role_archetype": matched_role,
            "estimated_p25_lpa": round(p25_annual / 100000.0, 2),
            "estimated_median_lpa": round(median_annual / 100000.0, 2),
            "estimated_p75_lpa": round(p75_annual / 100000.0, 2),
            "estimated_annual_median_inr": round(median_annual, 0),
            "salary_spread_ratio": spread_ratio,
            "is_realistic_range": is_realistic,
            "audit_verdict": audit_verdict
        }

# Singleton instance
salary_estimator = SalaryFairPayEstimator()
