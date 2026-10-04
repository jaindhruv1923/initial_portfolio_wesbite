# 📁 Portfolio Master Workspace Architecture & Directory Guide
**Owner:** Dhruv Jain (Final-Year B.Tech CSE, AI & Data Science · BML Munjal University)  
**Status:** Audit-Grade Verified · 100% Functionality Tested · All Subsystems Operational

---

## 🏛️ Executive Directory Architecture

The workspace has been organized into a two-tier hierarchy: **`important/`** (production codebases, running projects, flagship website, certifications, and resume) and **`unimportant/`** (project documentation packages, defense slide decks, BRDs, evaluation benchmarks, and legacy archives in `EXTRA_STUFF`).

```
c:\Users\jaind\Desktop\portfolio\
├── important/                                      # 🚀 Active Production Projects & Verified Artifacts
│   ├── Master_Portfolio_Website/                  # Flagship 7-page interactive portfolio website (100% standalone)
│   ├── Project_Kavach_Agentic_Security/           # KAVACH: Autonomous multi-agent AI DevSecOps governance platform
│   ├── Project_Naukri_Saaf_Job_Intelligence/      # Naukri Saaf: Recruitment intelligence, ghost job detection & NLP pipeline
│   ├── Project_Profitara_Retail_BI_Pipeline/      # Profitara: 10,000-txn retail BI pipeline, DuckDB OLAP, ML churn & PBI
│   ├── Project_Archon_apiCopilot/                 # Archon: Enterprise AI pair programming IDE & hybrid RAG orchestrator
│   ├── Project_Grilli_Restaurant_Reservation/     # Grilli: Full-stack restaurant table reservation system
│   ├── Certifications/                            # 10 verified industry credential badges (Power BI, Excel, IoT, Canva)
│   └── DhruvJain_Resume.pdf                       # Strict 1-page ATS-verified resume PDF
│
├── unimportant/                                    # 📚 Comprehensive Documentation Packages & Extra Archives
│   ├── project_documentations/                    # High-value business analysis, blueprints, slides, and reports
│   │   ├── kavach_agentic_security_docs/          # 15-Slide Master PPTX, Python generator, blueprints, flowcharts
│   │   ├── naukri_saaf_docs/                      # Complete BA documentation package (BRD, data dict, user stories, UAT)
│   │   ├── profitara_bi_docs/                     # Profitara BA documentation, analytical reports, business models
│   │   ├── archon_apicopilot_docs/                # Lab 4 empirical evaluation report, ablation studies, JSON benchmarks
│   │   └── README.md                              # Documentation directory index
│   │
│   └── EXTRA_STUFF/                               # 📦 Archival, Legacy, Rough Work & Redundant Backups
│       ├── kavach_rough_and_archives/             # Mid-sem rough drafts, legacy iterations, scratch scripts
│       ├── profitara_legacy_and_scratch/          # Legacy notebooks, deprecated files
│       ├── website_old_backups/                   # Deprecated initial website zip clones & Next.js prototypes
│       ├── raw_screenshots_archive/              # 92 raw unorganized loose screenshots
│       └── github_profile_repo/                   # Personal GitHub profile README repository
│
└── PORTFOLIO_DIRECTORY_GUIDE.md                   # Master index (this file)
```

---

## ⚡ Quick Launch Guide for All Projects

| Subsystem | Folder | Key Execution Command | Health Check |
|---|---|---|---|
| **Flagship Website** | `important/Master_Portfolio_Website` | Double-click `index.html` or run `npx serve .` | 104/104 links 100% operational |
| **Kavach Security** | `important/Project_Kavach_Agentic_Security` | `run_kavach.bat` or `python -m uvicorn app.main:app` | 13/13 frontend, 18/18 CSS, 12/12 exports pass |
| **Naukri Saaf** | `important/Project_Naukri_Saaf_Job_Intelligence` | `run_project.bat` or `pytest tests/` | 21/21 pytest unit tests pass |
| **Profitara BI** | `important/Project_Profitara_Retail_BI_Pipeline` | `run.bat` or `pytest tests/` | 10/10 pytest unit tests pass |
| **Archon Copilot** | `important/Project_Archon_apiCopilot` | `run_archon.bat` or `python test/verify_dataset_chunks.py` | 100% chunks & endpoints pass |
| **Grilli System** | `important/Project_Grilli_Restaurant_Reservation` | `cd backend && npm start` | Node/Express backend & static client |
| **Presentation Deck** | `unimportant/project_documentations/kavach_agentic_security_docs/pptmaker_docs` | `python build_master_presentation.py` | Generates 15-slide defense deck |

---

## 🔒 Verification & Website Safety Guarantee

1. **Master Website Integrity:** All 104 internal links (HTML pages, CSS stylesheets, DuckDB engine, AI chatbot, resume downloads, Power BI models, and screenshots) resolve locally inside `important/Master_Portfolio_Website`.
2. **Zero Missing Dependencies:** No code depends on files moved to `unimportant/`. All test suites pass directly.
3. **Audit-Grade Traceability:** All business documentation packages (BRDs, data dictionaries, UML flowcharts, and evaluation metrics) remain accessible under `unimportant/project_documentations/`.
