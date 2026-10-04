"""
Recruiter Domain, Phishing & Typosquatting Security Auditor
===========================================================
Audits job description text and contact channels for recruitment
fraud, domain spoofing, PII harvesting, and upfront fee scams.

Assigns an institutional Recruiter Security Grade (A, B, C, F)
with specific threat alerts and candidate safety advisories.
"""

import re
from typing import Dict, Any, List

class RecruiterSecurityAuditor:
    FREE_EMAIL_DOMAINS = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "rediffmail.com", "protonmail.com", "yopmail.com", "mail.com"
    }

    KNOWN_BRANDS = [
        "google", "amazon", "microsoft", "meta", "apple", "netflix",
        "uber", "airbnb", "stripe", "flipkart", "swiggy", "zomato",
        "infosys", "tcs", "wipro", "hcl", "cognizant", "accenture"
    ]

    UPFRONT_FEE_TRIGGERS = [
        "registration fee", "security deposit", "training fee", "processing fee",
        "laptop deposit", "documentation charge", "refundable deposit",
        "pay after placement", "enrollment fee"
    ]

    PII_HARVEST_TRIGGERS = [
        "aadhaar", "pan card", "bank details", "bank account", "passport copy",
        "credit card", "security pin", "date of birth with certificate"
    ]

    def audit_contact_security(
        self,
        company_name: str,
        text_content: str,
        contact_email: str = ""
    ) -> Dict[str, Any]:
        """
        Conducts deep forensic audit on recruiter email, domain authenticity,
        and description copy.
        """
        flags = []
        risk_score = 0  # 0 to 100
        text_lower = text_content.lower() if text_content else ""
        comp_lower = company_name.lower().strip() if company_name else ""

        # 1. Email Extraction & Domain Check
        found_emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text_content or "")
        if contact_email:
            found_emails.append(contact_email.lower().strip())

        has_free_email = False
        is_typosquatted = False
        inspected_domain = None

        for em in found_emails:
            domain = em.split("@")[-1].lower()
            inspected_domain = domain
            if domain in self.FREE_EMAIL_DOMAINS:
                has_free_email = True
                flags.append(f"Recruiter utilizes free public email domain (@{domain}) instead of authenticated corporate email.")
                risk_score += 35

            # Check domain typosquatting against major brands
            for brand in self.KNOWN_BRANDS:
                if brand in domain and domain != f"{brand}.com" and not domain.endswith(f".{brand}.com"):
                    is_typosquatted = True
                    flags.append(f"Potential typosquatting / domain impersonation detected: '@{domain}' attempts to mimic legitimate brand '{brand}'.")
                    risk_score += 45

        # 2. Instant Messaging Contact Bypass Check
        whatsapp_match = re.search(r"\b(whatsapp|wa\.me|\+?91[\s-]?\d{10})\b", text_lower)
        telegram_match = re.search(r"\b(telegram|t\.me)\b", text_lower)
        if whatsapp_match or telegram_match:
            flags.append("Listing directs applicants to bypass official ATS via WhatsApp or Telegram.")
            risk_score += 25

        # 3. Upfront Fee / Financial Extortion Check
        for fee_term in self.UPFRONT_FEE_TRIGGERS:
            if fee_term in text_lower:
                flags.append(f"EXTREME FRAUD ALERT: Upfront payment request detected ('{fee_term}'). Legitimate employers NEVER charge applicants.")
                risk_score += 60

        # 4. Premature PII Harvesting Check
        for pii_term in self.PII_HARVEST_TRIGGERS:
            if pii_term in text_lower:
                flags.append(f"Premature sensitive PII request detected ('{pii_term}'). Highly indicative of identity theft or data harvesting.")
                risk_score += 35

        # 5. Determine Security Grade
        risk_score = min(100, risk_score)
        if risk_score >= 60:
            grade = "Grade F (High Fraud / Phishing Threat)"
            verdict = "DANGEROUS"
            action = "DO NOT APPLY. Immediately report this listing. Never send money, OTPs, or government IDs."
        elif risk_score >= 35:
            grade = "Grade C (Suspicious / Opaque Recruiter)"
            verdict = "SUSPICIOUS"
            action = "Exercise caution. Do not communicate outside official platform messaging or verified corporate email."
        elif risk_score >= 15:
            grade = "Grade B (Standard Third-Party / Agency)"
            verdict = "MODERATE"
            action = "Standard recruiting agency. Verify client company identity before submitting private information."
        else:
            grade = "Grade A (Enterprise Authenticated)"
            verdict = "SAFE"
            action = "Clean contact channels. Authentic corporate hiring communication standards observed."

        return {
            "security_grade": grade,
            "verdict": verdict,
            "threat_risk_score": risk_score,
            "detected_email": found_emails[0] if found_emails else None,
            "inspected_domain": inspected_domain,
            "has_free_email": has_free_email,
            "is_typosquatted": is_typosquatted,
            "security_flags": flags,
            "safety_action": action
        }

# Singleton instance
recruiter_auditor = RecruiterSecurityAuditor()
