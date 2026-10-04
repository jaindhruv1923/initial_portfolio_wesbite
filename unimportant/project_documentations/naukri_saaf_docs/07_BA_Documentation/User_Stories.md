<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=User%20Stories%20%26%20Acceptance%20Criteria&fontSize=26&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20v4%20Production&descAlignY=78&descSize=15)

</div>

Format: `As a [role], I want [capability], so that [benefit]` — structured with Gherkin-style acceptance criteria for sprint execution and UAT sign-off.

<br/>

## 🧑‍💻 Epic 1 — Job Seeker: Real-Time Legitimacy & Ghost Detection

### US-01 — Automated DOM Ingestion across Major Job Portals
> **As a** job seeker, **I want** the extension to automatically parse the job posting I am viewing on LinkedIn, Indeed, Glassdoor, or Naukri, **so that** I do not have to copy-paste job descriptions or metadata manually.

```gherkin
Given I am viewing a job listing page on LinkedIn, Indeed, Glassdoor, or Naukri
When I open the extension sidepanel or click "Scan Listing"
Then the Overview tab extracts job title, company, location, posted date, and JD text within 1.5 seconds
And if the portal DOM layout is non-standard or altered
Then the heuristic DOM parser executes a generic container fallback extracting the main text body without crashing
```

<br/>

### US-02 — Dual-Mode Real-Time Risk Scoring (FastAPI + Heuristic Fallback)
> **As a** job seeker, **I want** an instant, calibrated risk score on whether a listing is genuine, suspect, or a ghost posting, **so that** I avoid wasting hours tailoring applications to inactive or deceptive openings.

```gherkin
Given a job posting has been successfully parsed from the active browser tab
When the extension sends a POST request to /api/v1/score
Then a calibrated probability score (0.0 to 1.0) is returned within 15ms
And the UI renders an intuitive risk badge: "Verified Clean" (<0.40), "Borderline Suspect" (0.40-0.70), or "High Risk Ghost" (>0.70)
And top-3 positive and negative SHAP risk drivers are visualized in plain English

Given the local FastAPI backend service is offline or unreachable
When the scoring request is triggered
Then the extension seamlessly falls back to client-side heuristic evaluation (legitimacy.js) without presenting error alerts
And explicitly informs the user that offline scoring is active
```

<br/>

### US-03 — Autonomous Verification Agent Deep-Scan
> **As a** cautious job applicant, **I want** an autonomous AI agent to cross-verify borderline listings against multiple independent sources, **so that** I have an exhaustive, audit-grade verification before submitting my personal data.

```gherkin
Given a listing scores in the borderline ambiguity range (0.40 <= Risk <= 0.70)
When I click "Run AI Verification Agent"
Then the agent executes 4 verification tools: ML Scorer, Semantic Plagiarism Scanner, Employer History Profiler, and Market Salary Validator
And logs each tool's empirical finding in an expandable step-by-step reasoning trail
And provides a definitive final verdict with an auditable confidence score
```

<br/>

## 🎯 Epic 2 — Job Seeker: Privacy-Preserving Resume Fit & Match

### US-04 — Zero-Knowledge Local Storage for Resumes
> **As a** privacy-conscious candidate, **I want** my resume to be parsed and stored strictly on my local machine, **so that** my personal contact details and employment history are never transmitted to external cloud servers.

```gherkin
Given I upload a PDF or plain-text resume into the extension
When I click "Save Resume"
Then the text content is extracted client-side via PDF.js and stored in chrome.storage.local
And a visual confirmation "✓ Saved locally (Zero-Knowledge)" is displayed
And network monitoring confirms zero HTTP requests transmitting resume data
```

<br/>

### US-05 — Contextual Keyword & Fit Score Analysis
> **As a** job seeker, **I want** a 0–10 alignment score and a list of specific missing skills for the active listing, **so that** I can strategically adjust my portfolio and resume framing.

```gherkin
Given I have a saved resume and an active job posting displayed
When I view the "Resume Match" tab
Then I see a holistic 0–10 fit score combining TF-IDF cosine similarity and domain skill ontology coverage
And a green checklist of verified matching competencies
And an alert list of high-priority missing technical requirements
And 3 tailored, non-generic recommendations specific to the target employer's domain
```

<br/>

## 📊 Epic 3 — Analytics & Enterprise Intelligence

### US-06 — Executive Streamlit Portal & Listing Age Distribution
> **As a** talent intelligence analyst or hiring manager, **I want** an interactive executive dashboard displaying macro ghost trends, platform comparisons, and empirical age distributions, **so that** I can benchmark recruiting market dynamics.

```gherkin
Given the Streamlit dashboard is running (05_Streamlit_Dashboard/app.py)
When I navigate across the 8 production tabs
Then I can inspect: Executive KPIs, Platform Benchmarks, Ghost Analytics, Employer Risk Matrix, Model Calibration & Silver Evaluation, Employer Clustering, Requisition Age Distributions, and SHAP Listing Inspector
And all metrics reflect the verified 2,851 dataset and 180 silver proxy holdout results
And selecting platform filters dynamically updates the listing age distributions and percentile estimates
```

<br/>

### US-07 — Employer Entity-Level Risk Profiling
> **As a** recruiter or academic researcher, **I want** to search and inspect specific corporate entities, **so that** I can distinguish legitimate agile hiring organizations from high-volume resume-harvesting operations.

```gherkin
Given I am on the Employer Risk Matrix tab
When I filter by company name or sort by "Ghost Velocity Ratio"
Then I view total openings, verified ghost counts, mean days active, and syndicated JD plagiarism scores
And employers exhibiting >65% ghost ratios are flagged with an actionable "High Risk Pipeline Harvester" badge
```

<br/>

## 🛠️ Epic 4 — Production Engineering & Maintainability

### US-08 — Automated Data Quality Gates & CI Regression Testing
> **As an** ML engineer / project maintainer, **I want** automated schema validation and metric regression gates, **so that** any pipeline updates that introduce data leakage or metric degradation automatically fail the build.

```gherkin
Given a PR or pipeline commit is pushed to the repository
When GitHub Actions CI executes pytest -v tests/
Then Pandera validates data types, bounds, and nullability on all feature tables
And a test verifies zero employer entity overlap between GroupKFold training and validation partitions
And a regression gate verifies holdout ROC-AUC does not drop below 0.9000
And any violation halts the pipeline with an actionable diagnostic report
```

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
