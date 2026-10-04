# Security, Ethics & Responsible AI Policy: Naukri Saaf

## 1. Ethical Problem Framing & Intent
Online job seekers invest significant time, emotional energy, and personal data applying to job postings. A growing proportion of these openings are **Ghost Jobs**—requisitions that are:
- Perpetually reposted to project artificial company growth to investors.
- Left active after a role is filled due to HR disorganization or automated subscription renewals.
- Published by low-intent agencies to harvest applicant resumes for third-party talent pools.

**Naukri Saaf** exists to restore hiring market transparency by equipping job seekers and analysts with objective, verifiable risk diagnostics.

---

## 2. Protection Against False Positives & Wrongful Blacklisting

A key ethical failure in student or amateur fraud detection systems is issuing binary, defamatory classifications ("This company is a scam"). 

To eliminate wrongful harm to legitimate employers:
1. **Calibrated Tri-Tier Status**: The system strictly avoids binary labels. Postings are segmented into:
   - **Genuine** (0.00 – 0.49): Verified hiring requisitions.
   - **Suspect** (0.50 – 0.74): Informational warning advising applicants to cross-verify on official portals.
   - **Ghost** (0.75 – 1.00): High likelihood of phantom posting, supported by explicit TreeSHAP evidence.
2. **Deterministic Citations**: The system never reports a score without providing the underlying observable indicators (e.g. `days_live > 90`, `undisclosed salary`, `syndicated description`).
3. **No Defamatory Claims**: The platform evaluates *individual requisitions*, not corporate reputations. Legitimate enterprises can have an abandoned posting without being labeled a fraudulent company.

---

## 3. Data Privacy & Ethical Web Scraping

1. **Public Domain Data Only**: Datasets were collected strictly from publicly accessible web pages without bypassing authentication paywalls or CAPTCHAs.
2. **PII Sanitization**: Any personal phone numbers or direct contact emails identified in job descriptions (often indicators of contact bypass scams) are sanitized and hashed in analytics logs.
3. **Respect for Platform Infrastructure**: Scrapes were collected using polite rate-limiting with exponential backoff via Apify scrapers to prevent server degradation.
4. **Local Browser Isolation**: The Chrome extension processes resume matching 100% locally in the browser memory using PDF.js and client-side tokenizers. **No user resume data is ever transmitted to an external server or third-party cloud API.**

---

## 4. Bias, Fairness & Slice Analysis

Models trained on job portal data risk reinforcing geographic or industrial disparities. We conducted bias evaluations across:
- **Geographic Tech Tiers**: Tier-2 and Tier-3 cities exhibit higher rates of undisclosed salaries. To avoid penalizing Tier-2 employers, salary opacity is treated as an informative signal rather than a dispositive disqualifier.
- **Enterprise vs. Small Business**: Small businesses naturally have lower metadata completeness (no Glassdoor rating or Fortune 500 status). The `LeakageFreeFeatureExtractor` combines metadata completeness with description richness so authentic startups are not misclassified as ghosts.

---

## 5. System Security & Threat Modeling

1. **Input Validation**: All API inputs are strictly enforced with Pydantic V2 schemas and validated against Pandera constraints to prevent malformed data injection.
2. **Prompt Injection Hardening**: In the Listing Verification Agent, all data retrieval is performed via deterministic Python functions rather than untrusted LLM prompt chaining. The agent never executes arbitrary code passed in scraped job text.
3. **Dependency Hardening**: The core pipeline relies on pure-vectorized NumPy implementations with zero external untrusted binary DLLs, eliminating C-extension vulnerability vectors.
