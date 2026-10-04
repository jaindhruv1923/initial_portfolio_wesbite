"""
Programmatic Labeling Functions (LFs) for Weak Supervision
==========================================================
Implements 10 orthogonal domain-heuristic labeling functions following the Snorkel paradigm.
Each LF outputs:
   1 : Vote Ghost / Non-Hiring
   0 : Vote Genuine Active Listing
  -1 : Abstain (no strong signal)
"""

import re
import pandas as pd
import numpy as np

# Label Constants
ABSTAIN = -1
GENUINE = 0
GHOST = 1

EMAIL_REGEX = re.compile(r"\b[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|rediffmail)\.[a-zA-Z]{2,}\b", re.IGNORECASE)
WHATSAPP_REGEX = re.compile(r"(whatsapp|call\s*hr|contact\s*hr|\+91[\-\s]?[6-9]\d{9})", re.IGNORECASE)

URGENCY_TERMS = [
    "immediate joiner", "immediate joining", "urgently hiring", "urgent requirement",
    "walk-in", "walk in", "limited seats", "fast hire", "instant hire", "spot offer"
]

def lf_extreme_staleness(row) -> int:
    """Flag listings that have sat live for over 90 days without closure."""
    days = row.get("days_live", 0)
    if pd.notna(days) and days > 90:
        return GHOST
    return ABSTAIN

def lf_fresh_active_posting(row) -> int:
    """Vouch for fresh postings (< 14 days old) with reasonable detail."""
    days = row.get("days_live", 0)
    words = row.get("description_length_words", 0)
    if pd.notna(days) and pd.notna(words):
        if days <= 14 and words >= 150:
            return GENUINE
    return ABSTAIN

def lf_contact_bypass(row) -> int:
    """Flag direct personal email or WhatsApp phone dump bypassing official ATS."""
    desc = str(row.get("description_text", ""))
    if EMAIL_REGEX.search(desc) or WHATSAPP_REGEX.search(desc):
        return GHOST
    return ABSTAIN

def lf_transparent_compensation(row) -> int:
    """Vouch for listings that disclose realistic salary bands."""
    sal_num = row.get("salary_disclosed_num", 0)
    sal_ratio = row.get("salary_range_ratio", 3.0)
    if sal_num == 1:
        if pd.notna(sal_ratio) and sal_ratio <= 2.2:
            return GENUINE
    return ABSTAIN

def lf_suspicious_salary_spread(row) -> int:
    """Flag extreme salary spread ratios (e.g. 3 LPA - 25 LPA placeholder)."""
    sal_num = row.get("salary_disclosed_num", 0)
    sal_ratio = row.get("salary_range_ratio", 0.0)
    if sal_num == 1 and pd.notna(sal_ratio) and sal_ratio > 3.0:
        return GHOST
    return ABSTAIN

def lf_serial_reposter_opaque(row) -> int:
    """Flag high-volume repeat postings from employers who hide salary info."""
    reposts = row.get("employer_repost_count", 1)
    sal_num = row.get("salary_disclosed_num", 0)
    if pd.notna(reposts) and reposts >= 4 and sal_num == 0:
        return GHOST
    return ABSTAIN

def lf_skeletal_description(row) -> int:
    """Flag skeletal, lazy job descriptions (< 60 words)."""
    words = row.get("description_length_words", 0)
    if pd.notna(words) and words < 60:
        return GHOST
    return ABSTAIN

def lf_detailed_verified_enterprise(row) -> int:
    """Vouch for well-documented positions from established, highly rated employers."""
    words = row.get("description_length_words", 0)
    rating = row.get("glassdoor_rating", 0)
    comp = row.get("company_data_completeness_score", 0)
    
    if pd.notna(words) and words > 350:
        if (pd.notna(rating) and rating >= 3.8) or (pd.notna(comp) and comp >= 65):
            return GENUINE
    return ABSTAIN

def lf_high_urgency_pressure(row) -> int:
    """Flag high-pressure scam/urgent hiring vocabulary."""
    desc = str(row.get("description_text", "")).lower()
    matches = sum(1 for term in URGENCY_TERMS if term in desc)
    if matches >= 2:
        return GHOST
    return ABSTAIN

def lf_high_applicant_momentum(row) -> int:
    """Vouch for listings receiving active applicant volume on LinkedIn."""
    source = row.get("source", "")
    apd = row.get("applications_per_day", 0)
    days = row.get("days_live", 0)
    if source == "LinkedIn" and pd.notna(apd) and apd >= 2.5 and pd.notna(days) and days <= 30:
        return GENUINE
    return ABSTAIN


LABELING_FUNCTIONS = [
    lf_extreme_staleness,
    lf_fresh_active_posting,
    lf_contact_bypass,
    lf_transparent_compensation,
    lf_suspicious_salary_spread,
    lf_serial_reposter_opaque,
    lf_skeletal_description,
    lf_detailed_verified_enterprise,
    lf_high_urgency_pressure,
    lf_high_applicant_momentum,
]

LF_NAMES = [
    "LF_ExtremeStaleness",
    "LF_FreshActivePosting",
    "LF_ContactBypass",
    "LF_TransparentComp",
    "LF_SuspiciousSalarySpread",
    "LF_SerialReposterOpaque",
    "LF_SkeletalDescription",
    "LF_DetailedVerifiedEnterprise",
    "LF_HighUrgencyPressure",
    "LF_HighApplicantMomentum",
]

def apply_lfs(df: pd.DataFrame) -> np.ndarray:
    """Applies all LFs to a dataframe and returns an (N, K) voting matrix."""
    n_rows = len(df)
    n_lfs = len(LABELING_FUNCTIONS)
    matrix = np.full((n_rows, n_lfs), ABSTAIN, dtype=int)
    
    for j, lf in enumerate(LABELING_FUNCTIONS):
        matrix[:, j] = df.apply(lf, axis=1).values
        
    return matrix
