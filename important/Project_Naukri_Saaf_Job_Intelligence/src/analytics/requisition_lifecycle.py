"""
Requisition Lifecycle Telemetry & Candidate Opportunity Cost Engine
===================================================================
Models the 4-stage requisition state machine:
  State 0: Fresh / Active (0 - 21 days)
  State 1: Stagnant / Passive (22 - 60 days)
  State 2: Zombie / Pipeline (61 - 120 days)
  State 3: Phantom / Ghost (>120 days or syndicated ring)

Computes Candidate Opportunity Cost:
  - Estimated applicant hours wasted
  - Economic monetary loss (INR/USD)
  - Application Friction Index
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

class RequisitionLifecycleEngine:
    def __init__(self, avg_app_time_hours: float = 0.75, avg_hourly_wage_inr: float = 650.0):
        self.avg_app_time_hours = avg_app_time_hours
        self.avg_hourly_wage_inr = avg_hourly_wage_inr

    def classify_lifecycle_stage(self, days_live: float, repost_count: int = 1, is_syndicated: bool = False) -> str:
        """Determines the discrete requisition lifecycle state."""
        days = float(days_live) if pd.notna(days_live) else 14.0
        reposts = int(repost_count) if pd.notna(repost_count) else 1
        
        if is_syndicated or days > 120 or (days > 60 and reposts >= 4):
            return "Phantom / Ghost"
        elif days > 60 or reposts >= 3:
            return "Zombie / Pipeline"
        elif days > 21 or reposts >= 2:
            return "Stagnant / Passive"
        else:
            return "Fresh / Active"

    def compute_opportunity_cost(self, applications_count: float, days_live: float, ghost_prob: float) -> Dict[str, Any]:
        """
        Computes wasted candidate hours and economic loss for a single listing.
        """
        apps = float(applications_count) if pd.notna(applications_count) and applications_count > 0 else 45.0
        prob = float(ghost_prob) if pd.notna(ghost_prob) else 0.25
        days = float(days_live) if pd.notna(days_live) else 14.0
        
        # Wasted probability weight
        wasted_apps = apps * prob
        hours_wasted = round(wasted_apps * self.avg_app_time_hours, 1)
        economic_loss_inr = round(hours_wasted * self.avg_hourly_wage_inr, 0)
        economic_loss_usd = round(economic_loss_inr / 85.0, 1)
        
        # Friction index (0 to 100) based on days live and applicant volume
        friction_index = min(100.0, (days / 120.0) * 50.0 + (min(apps, 300) / 300.0) * 50.0)
        
        return {
            "estimated_applicants": int(apps),
            "wasted_applicants": int(wasted_apps),
            "hours_wasted": hours_wasted,
            "economic_loss_inr": economic_loss_inr,
            "economic_loss_usd": economic_loss_usd,
            "friction_index": round(friction_index, 1)
        }

    def aggregate_market_waste(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Computes macroeconomic aggregate waste across the entire dataset.
        """
        total_listings = len(df)
        if total_listings == 0:
            return {}
            
        prob_col = "predicted_ghost_prob" if "predicted_ghost_prob" in df.columns else (
            "calibrated_ghost_prob" if "calibrated_ghost_prob" in df.columns else "ghost_label"
        )
        probs = df[prob_col].fillna(0.25).values
        
        app_col = "applications_count" if "applications_count" in df.columns else None
        if app_col and df[app_col].notna().sum() > 50:
            apps = df[app_col].fillna(df[app_col].median()).values
        else:
            apps = np.full(total_listings, 52.0)
            
        wasted_apps_total = np.sum(apps * probs)
        total_hours = wasted_apps_total * self.avg_app_time_hours
        total_inr = total_hours * self.avg_hourly_wage_inr
        total_usd = total_inr / 85.0
        
        # Breakdown by state
        stages = []
        for _, row in df.iterrows():
            d = row.get("days_live", 14.0)
            r = row.get("employer_repost_count", 1)
            s = bool(row.get("is_syndicated_description", 0) == 1)
            stages.append(self.classify_lifecycle_stage(d, r, s))
            
        stage_counts = pd.Series(stages).value_counts().to_dict()
        
        return {
            "total_listings_audited": total_listings,
            "total_candidate_hours_wasted": round(total_hours, 0),
            "total_economic_waste_inr": round(total_inr, 0),
            "total_economic_waste_usd": round(total_usd, 0),
            "wasted_applications_count": int(wasted_apps_total),
            "lifecycle_breakdown": stage_counts,
            "zombie_and_ghost_share_pct": round(((stage_counts.get("Zombie / Pipeline", 0) + stage_counts.get("Phantom / Ghost", 0)) / max(1, total_listings)) * 100.0, 1)
        }

# Singleton instance
lifecycle_engine = RequisitionLifecycleEngine()
