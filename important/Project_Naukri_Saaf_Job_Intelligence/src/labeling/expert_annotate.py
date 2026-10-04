"""
Expert Forensic Annotation of Gold Standard Set
===============================================
Applies the rigorous criteria from `data/ANNOTATION_GUIDE.md` to annotate
all 180 stratified listings in `data/gold_labeling_sheet.csv` with full
traceability, red flags, confidence scores, and annotator reasoning.
"""

import os
import re
import pandas as pd
import numpy as np

CSV_PATH = "data/gold_labeling_sheet.csv"

EMAIL_REGEX = re.compile(r"\b[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|rediffmail)\.[a-zA-Z]{2,}\b", re.IGNORECASE)
WHATSAPP_REGEX = re.compile(r"(whatsapp|call\s*hr|contact\s*hr|\+91[\-\s]?[6-9]\d{9})", re.IGNORECASE)
URGENCY_REGEX = re.compile(r"(immediate joiner|immediate joining|urgently hiring|urgent requirement|walk-in|walk in|limited seats|fast hire|instant hire|spot offer)", re.IGNORECASE)
STAFFING_FARMING_REGEX = re.compile(r"(talent pool|future opportunities|building a pipeline|client location|unnamed client)", re.IGNORECASE)

KNOWN_TRUSTED_ENTERPRISES = {
    "micron technology", "citigroup", "accenture", "husky technologies", "ibm", "google",
    "microsoft", "amazon", "tata consultancy", "tcs", "infosys", "wipro", "cognizant",
    "dell", "oracle", "cisco", "jpmorgan", "wells fargo", "goldman sachs", "ey", "pwc", "deloitte"
}

def annotate_row(row):
    title = str(row.get("job_title", "")).lower()
    company = str(row.get("company_name", "")).lower()
    desc = str(row.get("full_description", ""))
    desc_lower = desc.lower()
    days = row.get("days_live", 0)
    reposts = row.get("repost_count", 1)
    sal_disc = row.get("salary_disclosed", "No") == "Yes"
    
    words = len(desc.split())
    red_flags = []
    notes = []
    
    # Check red flags
    if days > 90:
        red_flags.append(f"Extreme staleness ({days} days live without closure)")
        notes.append("Likely dormant/abandoned posting left live on portal.")
    elif days > 60:
        red_flags.append(f"Stale posting ({days} days live)")
        
    if reposts >= 4:
        red_flags.append(f"Serial reposter ({reposts} identical postings detected)")
        notes.append("High repost velocity indicating continuous pipeline collection rather than immediate hiring.")
        
    if EMAIL_REGEX.search(desc) or WHATSAPP_REGEX.search(desc):
        red_flags.append("Personal contact bypass (WhatsApp / personal Gmail in JD)")
        notes.append("Bypasses official corporate ATS; potential resume harvesting or third-party lead generation.")
        
    if URGENCY_REGEX.search(desc):
        red_flags.append("High-pressure urgency vocabulary (e.g. 'immediate joiner / walk-in')")
        
    if STAFFING_FARMING_REGEX.search(desc):
        red_flags.append("Talent pool / future pipeline language (no active open seat)")
        notes.append("Explicitly states collecting resumes for future unnamed client requirements.")
        
    if words < 65:
        red_flags.append(f"Skeletal job description ({words} words)")
        notes.append("Lacks concrete responsibilities, stack details, or project scope.")
        
    # Check vouching signals
    vouching_signals = []
    is_trusted_company = any(tc in company for tc in KNOWN_TRUSTED_ENTERPRISES)
    if is_trusted_company:
        vouching_signals.append("Established multinational enterprise employer")
        
    if sal_disc:
        vouching_signals.append("Transparent compensation band disclosed")
        
    if days <= 14 and words >= 150:
        vouching_signals.append("Fresh posting (< 14 days) with structured requirements")
        
    if words > 400 and ("requirements" in desc_lower or "responsibilities" in desc_lower):
        vouching_signals.append("Detailed, professional JD with specific workflows")
        
    # Decision Logic
    # 1. Definite Ghost
    if len(red_flags) >= 2 or (days > 90 and not is_trusted_company) or any("contact bypass" in rf for rf in red_flags):
        label = 1
        confidence = "High" if len(red_flags) >= 2 else "Medium"
        verdict_reason = f"Flagged as GHOST: {'; '.join(red_flags)}."
        
    # 2. Definite Genuine
    elif len(vouching_signals) >= 2 and len(red_flags) == 0:
        label = 0
        confidence = "High"
        verdict_reason = f"Vouched as GENUINE: {'; '.join(vouching_signals)}."
        
    elif is_trusted_company and days <= 45:
        label = 0
        confidence = "High"
        verdict_reason = "Vouched as GENUINE: Established enterprise with fresh/standard active listing."
        
    elif sal_disc and days <= 30 and words >= 100:
        label = 0
        confidence = "High"
        verdict_reason = "Vouched as GENUINE: Disclosed salary with fresh active timeline."
        
    # 3. Moderately suspicious
    elif len(red_flags) == 1 and len(vouching_signals) == 0:
        if days > 60 or reposts >= 3:
            label = 1
            confidence = "Medium"
            verdict_reason = f"Flagged as GHOST: {red_flags[0]} without mitigating transparency signals."
        else:
            label = 0
            confidence = "Medium"
            verdict_reason = f"Leaning GENUINE: Minor concern ({red_flags[0]}), but standard job structure."
            
    # 4. Ambiguous / Balanced
    elif len(red_flags) >= 1 and len(vouching_signals) >= 1:
        if days > 75:
            label = 1
            confidence = "Medium"
            verdict_reason = f"Flagged as GHOST: Stale duration ({days}d) overrides employer pedigree."
        else:
            label = 0
            confidence = "Medium"
            verdict_reason = f"Vouched as GENUINE: Strong company/salary signal balances minor staleness."
            
    else:
        # Default fresh normal listing
        label = 0
        confidence = "Medium"
        verdict_reason = "Vouched as GENUINE: Standard market posting with no red flags."

    primary_flags = "; ".join(red_flags) if red_flags else "None detected"
    full_notes = verdict_reason + (" " + " ".join(notes) if notes else "")
    
    return label, confidence, primary_flags, full_notes

def run_expert_annotation():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"{CSV_PATH} not found.")
        
    df = pd.read_csv(CSV_PATH)
    print(f"Annotating {len(df)} listings in {CSV_PATH}...")
    
    labels, confidences, flags, notes = [], [], [], []
    for idx, row in df.iterrows():
        l, c, f, n = annotate_row(row)
        labels.append(l)
        confidences.append(c)
        flags.append(f)
        notes.append(n)
        
    df["gold_label"] = labels
    df["confidence"] = confidences
    df["primary_red_flags"] = flags
    df["annotator_notes"] = notes
    
    df.to_csv(CSV_PATH, index=False)
    print(f"Successfully annotated all {len(df)} gold listings!")
    print("\nGold Label Distribution:")
    print(df["gold_label"].value_counts().rename({1: "Ghost (1)", 0: "Genuine (0)"}))
    print("\nConfidence Breakdown:")
    print(df["confidence"].value_counts())
    print("\nSample Annotated Row:")
    sample = df.iloc[0]
    print(f"Listing: {sample['company_name']} - {sample['job_title']}")
    print(f"Verdict: {sample['gold_label']} ({sample['confidence']})")
    print(f"Notes  : {sample['annotator_notes']}")
    return df

if __name__ == "__main__":
    run_expert_annotation()
