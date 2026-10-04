# 🛡️ Naukri Saaf — Streamlit Command Center (15 Workbenches Guide)

> **Enterprise Forensic Intelligence & Candidate Defense Dashboard**  
> *Architected by Dhruv Jain · Production Zero-Leakage Architecture*

---

## 🧭 Executive Walkthrough of All 15 Dashboard Workbenches

Below is a complete, tab-by-tab guide explaining:
1. **What it does**: Its core capability and user-facing feature.
2. **How it achieves results**: The underlying mathematical, statistical, or engineering methodology.
3. **How it helps you**: The practical, real-world value for job seekers, recruiters, and technical interviewers in plain English.

---

### Tab 1: 🏠 Executive Overview & Macro Telemetry
- **What it does**: Provides a birds-eye view of labor market integrity across all 2,851 audited job listings from LinkedIn, Indeed, and Glassdoor, showing exact proportions of Genuine vs. Suspect vs. Ghost jobs, multi-portal risk shares, and weekly posting volume trends.
- **How it achieves results**: Ingests `data/predictions_v4.csv` and renders Plotly interactive donut charts, platform-comparative horizontal stacked bars, and longitudinal publication date area charts.
- **How it helps**: Gives leadership and recruiters an instant 30-second pulse check on market deception without getting lost in thousands of individual rows.

---

### Tab 2: 🔬 Live Forensic Lab & Dynamic Risk Gauge
- **What it does**: An interactive audit station where an applicant pastes any job title, company name, platform, listing lifespan, compensation, and description text to receive an immediate forensic risk assessment.
- **How it achieves results**: Feeds inputs into `VaguenessScorer`, `ats_prober`, and the Platt-calibrated Random Forest model to output an interactive speedometer gauge (0–100%), TreeSHAP feature drivers, 3 verified genuine alternative openings, 5 recruiter screening questions, and a hiring manager outreach template.
- **How it helps**: Before spending hours tailoring a resume and cover letter, a job seeker can paste the posting to know in 5 seconds whether the job is real, why it was flagged, and exactly what to ask the recruiter on the first screening call.

---

### Tab 3: 💡 Ghost-Safe Alternative Job Recommender
- **What it does**: Surfaces verified genuine, active alternative job requisitions matching the user's target job title and preferred tech hub (Bangalore, Pune, Hyderabad, Mumbai, Delhi-NCR).
- **How it achieves results**: Queries `data/predictions_v4.csv` using title tokenization and filters for low calibrated ghost risk (<25%), verified corporate backing, recent posting activity (<30 days), and transparent compensation bands.
- **How it helps**: Eliminates applicant frustration by immediately redirecting wasted energy away from phantom openings toward verified employers actively hiring right now.

---

### Tab 4: 🛡️ Recruiter Fraud & Phishing Threat Auditor
- **What it does**: Scans recruiter outreach messages, emails, WhatsApp messages, or job descriptions for cybersecurity threats, scam domains, upfront registration fees, and sensitive identity harvesting.
- **How it achieves results**: Runs regex domain analyzers, free-email detectors (e.g. `@gmail.com` or `@uber-jobs.in`), WhatsApp redirect flaggers, and PII extortion detectors (Aadhaar/PAN cards) to output an institutional security grade from A (safe) to F (critical threat).
- **How it helps**: Protects college freshers and job seekers from losing money to fraudulent placement agencies (e.g., "deposit ₹3,500 registration fee") and prevents identity theft.

---

### Tab 5: 🏢 Automated ATS Verification Prober
- **What it does**: Autonomously verifies whether an employer actually has active job requisitions indexed on official corporate Applicant Tracking Systems (ATS) like Greenhouse, Lever, Ashby, Workday, and SmartRecruiters.
- **How it achieves results**: Parses organization slugs and queries canonical ATS career portal endpoints, calculating an independent grounding confidence score and displaying an employer verification table.
- **How it helps**: Breaks the fundamental "chicken-and-egg" label circularity problem in job board data—third-party portals often leave expired jobs online, but a company's official ATS never lies about open headcount.

---

### Tab 6: 🕸️ Recruitment Syndication & Graph Network Visualizer
- **What it does**: Uncovers cross-company description syndication rings where different recruitment agencies or shell entities post identical job descriptions verbatim across portals.
- **How it achieves results**: Builds a bipartite NetworkX graph connecting employers to shared description clusters, applying Greedy Modularity community detection and PageRank centrality to highlight the most influential ringleader agencies.
- **How it helps**: Exposes resume-harvesting networks that spam job boards with duplicate roles to artificially inflate candidate databases.

---

### Tab 7: 🎛️ What-If Counterfactual Simulator
- **What it does**: An interactive simulator where users adjust core risk parameters (days live, disclosing salary, expanding word count, lowering repost velocity) and watch the calibrated risk score dynamically drop in real time.
- **How it achieves results**: Uses an inverse optimization counterfactual explainer that computes the minimal feature changes needed to convert a "Ghost" or "Suspect" posting into a "Genuine" rating.
- **How it helps**: Helps legitimate employers and HR teams understand why their job posts might look suspicious and gives them a step-by-step checklist to optimize their listings and attract higher-quality applicants.

---

### Tab 8: ⏳ Requisition Lifecycle & Survival Decay Simulator
- **What it does**: Displays empirical Kaplan-Meier survival trajectories and requisition half-life benchmarks, contrasting how rapidly genuine postings get filled versus phantom postings that linger indefinitely.
- **How it achieves results**: Generates non-parametric survival probability coordinates $S(t)$ over a 150-day timeline and computes empirical half-life statistics across platforms (e.g., Glassdoor median half-life: 41 days vs. Indeed: 0.3 days).
- **How it helps**: Informs candidates when a job has entered the "zombie" or "phantom" stage, preventing them from wasting hours applying to postings that have been abandoned by recruiters.

---

### Tab 9: 💰 Candidate Economic Waste & Opportunity Cost Calculator
- **What it does**: Quantifies the macroeconomic financial and time damage caused by phantom job openings on applicants across Indian tech hubs.
- **How it achieves results**: Multiplies wasted applicant counts by customizable candidate hourly rates (₹/hr) and preparation times (e.g., 45 minutes per application), aggregating total economic loss in Lakhs/Crores and US Dollars.
- **How it helps**: Translates abstract ML risk percentages into tangible human impact (e.g., ₹1.47+ Crores and 30,000+ candidate hours wasted), creating an unforgettable story during interviews.

---

### Tab 10: 📡 Employer Risk Radar & Serial Reposter Leaderboard
- **What it does**: Benchmarks 1,200+ employers on an interactive scatter plot, contrasting their repost frequency against their average calibrated ghost risk, and ranks the Top 10 serial ghost reposters vs. Top 10 high-transparency employers.
- **How it achieves results**: Aggregates company-level metrics across all scraped listings, filtering for multi-post organizations and tracking maximum repost counts.
- **How it helps**: Functions as a "Glassdoor for Job Posting Integrity," allowing candidates to check an employer's hiring reputation before submitting an application.

---

### Tab 11: 📝 NLP Vagueness & Buzzword Forensic Matrix
- **What it does**: Analyzes the linguistic DNA of job descriptions, contrasting concrete technical entity density (Python, SQL, AWS, Docker) against empty corporate fluff ("rockstar", "wear many hats", "fast-paced environment").
- **How it achieves results**: Scans text with regular expressions and a 4,000-term technical vocabulary, calculating entity frequency per 100 words, action-to-vague verb ratios, and a composite vagueness index.
- **How it helps**: Empirically proves that ghost jobs hide behind buzzwords, teaching job seekers to spot low-effort, copy-pasted job posts at a glance.

---

### Tab 12: 🌐 Cross-Portal Vulnerability & Salary Opacity Matrix
- **What it does**: Compares LinkedIn, Indeed, and Glassdoor head-to-head on ghost job rates, salary transparency rates, and average posting lifespans.
- **How it achieves results**: Groups all 2,851 harmonized postings by source portal, computing weighted means for salary disclosure and staleness.
- **How it helps**: Shows job seekers which hiring platforms have the highest data integrity and which ones are plagued by stale listings (e.g., Glassdoor listings averaging 63.8 days live vs Indeed's fresh listings).

---

### Tab 13: 📄 Executive Forensic Dossier & Audit Exporter
- **What it does**: Allows the user to select any audited job listing and generate an institutional-grade, formal markdown investigation report with complete risk breakdowns, forensic evidence bullets, and recommended actions.
- **How it achieves results**: Compiles listing metadata, Platt probability, top TreeSHAP driver, and ATS grounding flags into a formatted dossier downloadable as a `.md` file.
- **How it helps**: Gives candidates and talent acquisition auditors a tangible, professional proof-of-work artifact they can save, share, or bring into discussions.

---

### Tab 14: 🤖 MLOps Telemetry & 5-Fold GroupKFold Leaderboard
- **What it does**: Displays the machine learning benchmark leaderboard evaluated strictly on 180 unseen holdout gold standard listings, probability calibration curves (Brier score & ECE), and real-time Population Stability Index (PSI) drift reports.
- **How it achieves results**: Reads `data/model_benchmark_gold_test.csv`, `data/calibration_metrics_v4.csv`, and `data/drift_monitoring_report.json` with styled data tables.
- **How it helps**: Proves to senior technical interviewers and engineering managers that the system is built with zero data leakage, calibrated probabilities, and production-grade monitoring.

---

### Tab 15: 🔍 Searchable Enterprise Data Explorer
- **What it does**: An interactive, searchable data table that allows full-text searching across all 2,851 harmonized listings by title, company, location, or keyword, with instant CSV filtering and exporting.
- **How it achieves results**: Applies dynamic multi-column pandas text filtering and renders interactive dataframes with custom column projection and a one-click CSV download button.
- **How it helps**: Allows recruiters, candidates, and analysts to slice and dice the dataset however they want without needing to write code or SQL queries.
