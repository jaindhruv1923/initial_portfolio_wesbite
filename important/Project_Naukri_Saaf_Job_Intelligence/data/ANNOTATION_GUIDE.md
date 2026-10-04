# Human Annotation Guide: Ground Truth Gold Standard Set

**File to Label:** `data/gold_labeling_sheet.csv`  
**Total Listings:** 180 (Stratified 60 Glassdoor, 60 Indeed, 60 LinkedIn)  
**Estimated Time to Complete:** 30–45 minutes  
**Goal:** Establish an honest, gold-standard human evaluation set to test both the weak supervision label model and the machine learning classifiers.

---

## 1. The Core Question to Ask
> *"If an qualified job seeker spends 45 minutes tailoring their resume and cover letter and applies to this role today, is there a realistic, active hiring process behind it, or is this posting dead, resume-farming, or fake?"*

---

## 2. Annotation Codes (`gold_label` Column)

| Value | Meaning | Description | Typical Examples |
|:---:|:---:|---|---|
| **`1`** | **Ghost / Low-Quality Fake** | High confidence that this posting is NOT actively hiring for a real open seat. | Reposted 5+ times over months; vague buzzword salad; direct WhatsApp/personal Gmail contact; zero salary + generic JD from unknown agency. |
| **`0`** | **Genuine Active Role** | High confidence that this is a real, active job posting with real hiring intent. | Specific tech stack, concrete project scope, transparent salary or recognizable verified company, fresh posting (< 30 days). |
| **`-1`** | **Ambiguous / Unsure** | Genuinely impossible to tell from the available text. | Standard boilerplate template from a known company, but no salary and posted 40 days ago. |

---

## 3. Decision Matrix & Specific Forensic Signals

### Strong Evidence of a GHOST / FAKE Listing (`gold_label = 1`)
1. **The "Forever Opening" (Extreme Staleness):**
   - Listed as live for `days_live > 90` without being refreshed, or reposted `repost_count >= 4` times without closing.
2. **Contact Bypass / Phishing Signature:**
   - Mentions a personal contact in the description: *"Send CV to hr.consulting2024@gmail.com"* or *"WhatsApp your resume to +91 98765..."*. Real corporate hiring uses portal ATS or official `@company.com` domains.
3. **Empty "Vibe" Description:**
   - 2–3 sentences with no actual responsibilities or requirements: *"Looking for passionate, hard-working candidates. Great learning environment. Apply immediately."*
4. **The Impossible Entry-Level Paradox:**
   - Title says *"Junior Data Analyst / Freshers Welcome"*, but description asks for 5–7 years of enterprise Snowflake, Kafka, and Kubernetes with no salary disclosed.
5. **Generic Recruiter "Talent Pool" Farming:**
   - *"We are building a pipeline for future opportunities across multiple unnamed Fortune 500 clients."*

### Strong Evidence of a GENUINE Listing (`gold_label = 0`)
1. **Concrete Responsibilities & Stack Specifics:**
   - Mentions specific tools, databases, internal workflows, or domain context (e.g., *"Working with our payments team to migrate PostgreSQL tables to BigQuery using dbt"*).
2. **Compensation Transparency:**
   - Real, plausible salary band disclosed (e.g., ₹6,00,000 – ₹10,00,000 INR).
3. **Fresh Listing & Active Velocity:**
   - Posted within the last 15 days (`days_live <= 15`) with clear submission instructions.
4. **Verifiable Corporate Employer:**
   - Well-known tech firm, established startup, or enterprise with clear team structure.

---

## 4. How to Complete the Sheet in Excel or VS Code

1. Open `data/gold_labeling_sheet.csv` in Excel, Google Sheets, or VS Code.
2. For each row (1 to 180):
   - Look at `job_title`, `company_name`, `days_live`, `salary_range`, and `description_snippet`.
   - Read `full_description` if the snippet is not enough.
   - Enter `1`, `0`, or `-1` into the **`gold_label`** column.
   - *(Optional)* In `primary_red_flags`, note keywords like `stale`, `no_salary`, `contact_bypass`, `vague`, or `reposted`.
3. Save the file as `data/gold_labeling_sheet.csv`.

---

## 5. What Happens After You Save
Once saved, our automated evaluation script (`python src/labeling/evaluate_labels.py`):
1. Calculates **inter-annotator agreement** and **Cohen's Kappa** between your gold labels and the programmatic Snorkel weak supervision model.
2. Evaluates the legacy heuristic rule vs. the gold set (exposing the true baseline accuracy).
3. Locks this gold set as the pristine, untouchable holdout set that all downstream models (GBM, RF, Agent) will be benchmarked against.
