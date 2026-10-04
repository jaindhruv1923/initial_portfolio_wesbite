# 🌐 Dhruv Jain — Executive Data Analyst & AI Engineer Portfolio
### Production Build (`final_work`) · Audit-Grade Traceability · 100% Standalone

[![Status](https://img.shields.io/badge/Status-Production_Ready-10B981?style=for-the-badge)](https://jaindhruv1923.github.io/initial_portfolio_wesbite/)
[![Resume](https://img.shields.io/badge/Resume-1--Page_Verified_ATS-C9A227?style=for-the-badge)](assets/DhruvJain_Resume.pdf)
[![PowerBI](https://img.shields.io/badge/Power_BI-2_Interactive_PBIX-F59E0B?style=for-the-badge&logo=powerbi)](dashboards/)
[![SQL](https://img.shields.io/badge/Engine-DuckDB_OLAP-38BDF8?style=for-the-badge)](index.html#sql-lab)

---

## 🌟 Executive Overview

This directory (`final_work`) contains the complete, self-contained, publication-grade portfolio build for **Dhruv Jain** (Final-Year B.Tech Computer Science & Engineering, Specialization: AI & Data Science, BML Munjal University, 2023–2027).

Every metric, figure, visualization, and finding across this build is **100% reproducible and audit-traceable** from underlying raw datasets, Python notebooks, SQL queries, and Power BI data models.

---

## 🏗️ Architecture & File Structure

```
final_work/
├── index.html                   # Master flagship portfolio website (SQL Lab, Matrix, Projects, Artifacts Hub)
├── profitara.html               # Retail BI & ML Pipeline case study (16 high-res screenshots, DAX, DuckDB)
├── naukri-saaf.html             # Recruitment Intelligence & Ghost Job ML case study (8 screenshots, Snorkel, SHAP)
├── kavach.html                  # Autonomous Architecture & Dependency Sentinel case study (13 screenshots, 164 tests)
├── archon.html                  # Enterprise AI IDE & Empirical LLM Benchmarking study (Lab 4, 78 eval pairs)
├── grilli.html                  # Full-Stack Restaurant Table Reservation System case study (Node/Express/MongoDB)
├── kidlearn.html                # Gamified EdTech habit loop case study with interactive app launcher
├── style.css                    # Obsidian/Gold/Emerald design system, micro-animations, glassmorphism, responsive CSS
├── script.js                    # Interactive DuckDB SQL runner, live counters, filter tabs, modal lightbox, IST clock
├── chatbot.js                   # Google Gemini-Grade AI Assistant (Universal World Knowledge + Verified Portfolio Ledger)
├── DhruvJain_Resume.pdf        # Verified strict 1-page ATS resume PDF (Tectonic engine compiled)
├── dhruv-photo.jpg              # High-resolution professional portrait
├── .nojekyll                    # GitHub Pages routing & static asset compatibility flag
│
├── assets/
│   ├── DhruvJain_Resume.pdf    # Master 1-page ATS resume copy
│   └── dhruv-photo.jpg          # Portrait copy
│
├── certs/                       # 10 verified industry credentials (PNG lightbox assets)
│   ├── powerbi_harnessing-1.png
│   ├── powerbi_etl-1.png
│   ├── powerbi_data_modeling-1.png
│   ├── powerbi_creative_design-1.png
│   ├── excel_data_prep-1.png
│   ├── iot_security-1.png
│   ├── digital_products_canva-1.png
│   ├── figma_components-1.png
│   ├── customer_personas_canva-1.png
│   └── storyboard_canva-1.png
│
├── dashboards/                  # Production Power BI models (.pbix)
│   ├── Profitara_BIDashBoard.pbix      # 4.8MB Retail BI Star Schema (22 DAX measures, churn simulation)
│   └── Naukrisaaf_FinalDashboard.pbix  # 3.2MB Recruitment Intelligence (8 interactive pages, wage gap analysis)
│
├── projects/                    # Raw datasets, analytical SQL scripts, and BA documentation packages
│   ├── profitara/
│   │   ├── 01_Dataset/          # Profitara_India_Dataset.csv (10,000 real-parameter transactions)
│   │   ├── 02_Excel_Workbook/   # Profitara_Business_Analytics_Model.xlsx
│   │   ├── 03_SQL/              # Profitara_Complete.sql (42 analytical SQL queries, CTEs, Window Functions)
│   │   ├── 04_ML_Pipeline/      # Jupyter predictive model notebooks
│   │   ├── 05_Streamlit_Dashboard/
│   │   └── 07_BA_Documentation/ # BRD, Executive Summary, Process Flow
│   ├── naukri_saaf/
│   │   ├── 01_Datasets_Raw_Scrapes/ # 2,851 multi-portal scraped job listings
│   │   ├── 02_SQL/              # MySQL analytical workbench scripts
│   │   ├── 06_Chrome_Extension/ # Manifest V3 extension bundle
│   │   └── 07_BA_Documentation/ # Full BA suite (BRD, Data Dictionary, Risk Register, UAT Script)
│   ├── kavach/                  # Security gate reports & final architecture blueprint
│   ├── archon/                  # evaluation_report.json (78-pair benchmark) & LAB4_REPORT.md
│   └── KidLearn/                # Complete runnable interactive gamified educational app
│
└── screenshots/                 # High-resolution dashboard, UI, and architecture captures
    ├── profitara/               # 16 visual verification figures
    ├── naukri-saaf/             # 8 visual verification figures
    ├── kavach/                  # 13 visual verification figures
    └── grilli/                  # Full-stack reservation system captures
```

---

## 📊 Summary of Flagship Platforms

| System | Domain | Scale / Primary Data | Core Algorithms / Models | Key Metric | Deliverables |
|---|---|---|---|---|---|
| **Profitara** | Retail BI & Predictive Analytics | 10,000 Indian Q-commerce orders (₹66.95L) + 541k UCI | Random Forest CLV Regressor, Logistic Regression Churn, Apriori Rules | **R² = 0.930** (CLV), **AUC = 0.91** (Churn) | `.pbix` dashboard, DuckDB SQL lab, 13-page Streamlit, 10k CSV, BRD |
| **Naukri Saaf** | Recruitment Intelligence & Ghost Jobs | 2,851 scraped postings (LinkedIn, Indeed, Glassdoor) | Snorkel Weak Supervision ($\kappa=0.589$), LightGBM, TreeSHAP | **ROC-AUC = 0.920** (Calibrated) | `.pbix` dashboard, MV3 Chrome extension, sub-15ms FastAPI, BA suite |
| **KAVACH** | Security Sentinel & Code Intelligence | 4 enterprise repository modules, 42-run security corpus | Deterministic Regex/Checksum Parser, Python AST Call-Graph | **F1 = 1.00** (PII Scanner), **Avg F1 = 0.72** (AST) | 164/164 Pytest passing tests, CI gate, JSON telemetry report |
| **Archon Copilot** | Enterprise AI IDE & LLM Evaluation | 21 OpenAPI / Markdown files (103 chunks), 26 tasks | Hybrid RAG (BM25 + BGE Dense + Cross-Encoder), Local CoT Judge | **71.15% Correctness** (Gemma 3), **100% Code Pass** (CodeLlama) | 78-pair eval JSON, 27KB Lab 4 report, Next.js 14 Web IDE |
| **Grilli** | Full-Stack Reservation Platform | Multi-table restaurant dining floor | Node.js, Express, MongoDB, Anti-collision slot locking | **100% Real-Time Validation** | 5 REST endpoints, responsive UI, 6 critical bug fixes |
| **KidLearn** | Gamified EdTech Habit Dashboard | 6 academic subjects, multi-child profiles | Vanilla JavaScript (ES6+), Canvas API, LocalStorage | **21 Achievement Badges** | 8-page client-side app, Pomodoro timer, parent report card |

---

## 💼 Professional Experience & Credentials

- **Udaghosh Social Welfare Society** (*Data Analyst Intern*, Remote, July 2026 – Oct 2026):
  - Authored complex SQL pipelines (multi-table JOINs, CTEs, Window Functions) consolidating organizational records.
  - Designed interactive Power BI executive dashboards tracking operational KPIs, performance benchmarks, and seasonal volunteer trends.
  - Built automated Excel reporting models with dynamic lookups and Pivot Tables, cutting report turnaround time.
- **Contentora Media** (*MIS Analyst Intern*, Remote, July 2026 – Oct 2026):
  - Engineered and maintained structured Excel MIS trackers for leadership research and commercial metrics.
  - Standardized, normalized, and deduplicated multi-source market intelligence feeds.
- **10 Industry Certifications**:
  - Microsoft Power BI Data Modeling & DAX Foundations
  - Microsoft Power BI ETL & Power Query Transformations
  - Microsoft Power BI Creative Designing & Dashboard UX
  - Microsoft Harnessing the Power of Data with Power BI
  - Microsoft Preparing Data for Analysis with Microsoft Excel
  - CertNexus IoT Security, Data Privacy & Governance
  - Coursera Digital Products Architecture in Canva
  - Coursera Figma Component Systems & Auto-Layout
  - Coursera Customer Personas & User Analytics in Canva
  - Coursera Storyboard & Product Narratives in Canva

---

## 🚀 How to Run & Deploy Locally

### Option 1: Double-Click or Open Directly in Browser
Since all asset paths in `final_work` are relative, you can simply double-click [index.html](index.html) or open it in Google Chrome, Microsoft Edge, Firefox, or Safari!

### Option 2: Run a Local Static HTTP Server
```bash
# Using Python built-in HTTP server:
python -m http.server 8080 --directory final_work

# Open in browser:
http://localhost:8080
```

### Option 3: Deploy to GitHub Pages
1. Push the contents of `final_work` to the `gh-pages` or `main` branch of your repository.
2. The `.nojekyll` file is already included to ensure all folders (including those with underscores or special characters) are served correctly.
3. Access your live portfolio at `https://<username>.github.io/<repo-name>/`.

---

## 📬 Contact & Inquiries
- **Dhruv Jain**
- **Email**: [jaindhruv1923@gmail.com](mailto:jaindhruv1923@gmail.com)
- **Phone**: [+91 99118 50506](tel:+919911850506)
- **LinkedIn**: [linkedin.com/in/jaindhruv1923](https://www.linkedin.com/in/jaindhruv1923)
- **GitHub**: [github.com/jaindhruv1923](https://github.com/jaindhruv1923)
