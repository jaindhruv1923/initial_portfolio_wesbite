// ==============================================================================
// Google Gemini-Grade AI Assistant & Universal World Knowledge Engine
// Integrated for Dhruv Jain's Flagship Data Analyst & AI Portfolio
// ==============================================================================

(function () {
  "use strict";

  // ----------------------------------------------------------------------------
  // 1. VERIFIED PORTFOLIO LEDGER (Ground Truth Facts)
  // ----------------------------------------------------------------------------
  const PORTFOLIO_KB = [
    {
      kw: ["who is dhruv", "about dhruv", "introduce", "biography", "background", "profile", "who are you", "what is your name"],
      title: "Dhruv Jain — Profile & Executive Summary",
      ans: `**Dhruv Jain** is a final-year B.Tech CSE (AI & Data Science) student at **BML Munjal University, Gurugram** (Hero Group, 2023–2027).

He specializes in **Audit-Grade Retail BI Pipelines**, **Recruitment Intelligence ML**, and **Security-Governed Agentic AI Systems**. Dhruv is actively seeking full-time **Data Analyst, BI Analyst, and Analytics Engineering** roles.

- 🎓 **Education**: B.Tech CSE (AI & Data Science), BML Munjal University (2023–2027, Final Year).
- 💼 **Internships**: Data Analyst Intern at **Udaghosh Social Welfare Society** & MIS Analyst Intern at **Contentora Media**.
- 🚀 **Flagship Systems**: Profitara (₹66.95L Retail BI), Naukri Saaf (2,851 Ghost Jobs ML), KAVACH (1.00 PII F1 Sentinel), Archon Copilot (78 LLM Eval Pairs).
- 📜 **Certifications**: 10 verified industry credentials (5 Power BI/Excel, 1 CertNexus IoT Security, 4 Canva/Figma).
- 📍 **Location**: Gurugram / Delhi NCR, India (Open to On-site, Hybrid & Remote).`
    },
    {
      kw: ["education", "college", "university", "degree", "bml", "munjal", "cgpa", "school", "btech", "coursework"],
      title: "Academic Background & Coursework",
      ans: `**Bachelor of Technology (B.Tech) in Computer Science & Engineering**
*Specialization in Artificial Intelligence & Data Science*
**BML Munjal University, Gurugram** (Hero Group, 2023–2027 · Final Year).

**Core Quantitative Coursework:**
- Linear Algebra, Probability & Mathematical Statistics
- Database Management Systems (PostgreSQL, MySQL, DuckDB)
- Machine Learning & Predictive Modeling
- Big Data Analytics & Distributed Computing
- Data Structures & Algorithms (Python, C++)`
    },
    {
      kw: ["internship", "experience", "work experience", "udaghosh", "contentora", "mis analyst", "data analyst intern"],
      title: "Professional Work Experience",
      ans: `Dhruv has completed two concurrent professional data analytics internships:

1. **Data Analyst Intern · Udaghosh Social Welfare Society** *(July 2026 – Oct 2026)*
   - Authored complex SQL queries (Window Functions, recursive CTEs, multi-table aggregations) to audit operational databases.
   - Built interactive Microsoft Power BI executive dashboards tracking donor retention, fund disbursement velocity, and campaign ROI.
   - Automated weekly operational MIS reports in Excel, reducing manual turnaround time by 65%.

2. **MIS Analyst Intern · Contentora Media** *(July 2026 – Oct 2026)*
   - Designed enterprise MIS reporting trackers in Excel with automated data consolidation and lookup frameworks.
   - Conducted market intelligence and competitive data benchmarking across digital media campaigns.
   - Applied strict data hygiene and standardization procedures across multi-source client datasets.`
    },
    {
      kw: ["skills", "tech stack", "tools", "technologies", "languages", "programming", "python", "sql", "power bi", "dax", "excel"],
      title: "Technical Stack & Tooling Mastery",
      ans: `**Dhruv Jain's Verified Technical Stack:**

- 🐍 **Core Programming**: Python (Pandas, NumPy, Scikit-learn, LightGBM, Statsmodels, mlxtend), JavaScript (ES6+), C++, HTML5/CSS3.
- 🗄️ **Databases & Query Engines**: PostgreSQL, MySQL, DuckDB (OLAP in-memory), MongoDB, SQLite.
- 📊 **BI & Analytics**: Microsoft Power BI (DAX, Star Schema, Power Query M), Advanced Excel (Pivot Tables, XLOOKUP, Solver, Power Query), Streamlit, Plotly.
- 🤖 **Machine Learning & AI**: Snorkel (Weak Supervision), TreeSHAP (Explainability), Okapi BM25, ChromaDB, Qdrant Vector DB, Cross-Encoders, Ollama, Google Gemini API.
- ⚙️ **Engineering & CI/CD**: Git/GitHub, Docker, FastAPI, pytest (164 automated tests), Node.js, Next.js.`
    },
    {
      kw: ["profitara", "retail", "clv", "churn", "quick commerce", "66.95", "4918", "apriori", "basket", "ba", "business analyst", "leakage", "discount"],
      title: "Project 1: Profitara — Retail BI, BA & Decision Platform",
      ans: `**Profitara** is an enterprise-grade retail business intelligence and decision analytics platform pairing rigorous data engineering with full Business Analyst deliverables.

- 📈 **Data Foundation**: Audited 10,000 quick-commerce transactions (**₹66.95 Lakhs revenue, 4,918 orders, 1,448 customers**) and 541,909 real UCI retail transactions with Pandera schema verification.
- 📋 **Business Analyst Deliverables**: Comprehensive Business Requirements Document (BRD) across 11 formal requirements (\`BR-01\` to \`BR-11\`), stakeholder KPI dictionary, and line-item profitability audit.
- 💸 **Margin Leakage Audit**: Uncovered that 4,743 items (47.4% of catalog) operated at negative profit (-₹2.06L operational loss). Proved discounts &ge;30% collapse net margins to -13.3%; modeled sub-category discount caps recovering ₹38k on Fresh Fruits.
- 🎯 **Prescriptive Win-Back Policy**: Decision-theoretic Expected Value layer achieving **+£720.03 simulated net profit** under £1,500 budget (23× gain over naive recency's £31.60).
- 🛡️ **Zero-Leakage ML Core**: Out-of-time Platt-scaled Churn classifier (**AUC = 0.764**, Brier 0.1928), BG/NBD lifetime value baseline (MAE £755.28), and 248 Apriori rules with up to **27.86× lift**.
- 💻 **Interfaces & Serving**: 13-page interactive Streamlit web application, live in-browser DuckDB SQL lab, and 4.8MB Power BI star schema (\`Profitara_BIDashBoard.pbix\`) with 22 DAX measures.`
    },
    {
      kw: ["naukri saaf", "naukrisaaf", "ghost job", "recruitment", "fake job", "snorkel", "lightgbm", "2851", "chrome extension", "economic waste", "labor market", "counterfactual"],
      title: "Project 2: Naukri Saaf — Labor Market Intelligence & Ghost Job Detection",
      ans: `**Naukri Saaf** is an end-to-end labor market forensic intelligence platform and business analysis deliverable.

- 🔍 **Audited Corpus**: 2,851 real job listings scraped across LinkedIn, Indeed, and Glassdoor with Pandera schema verification.
- 💸 **Macroeconomic Labor Waste**: Audited 428 phantom listings (15.0% ghost rate) resulting in **179,261 wasted applications**, 134,446 lost preparation hours, and **₹8.74 Crores (₹873.9 Lakhs)** in candidate deadweight loss.
- ⚖️ **Asymmetric Cost Policy ($C_{FP} = 5 \times C_{FN}$)**: Falsely rejecting a real job costs 5× more to candidate careers than applying to a ghost job; tuned optimal decision cutoff to $\\tau^* = 0.65$, slashing false alarms by 78%.
- 🏢 **Cross-Portal Vulnerability**: Uncovered that Glassdoor hosts **42.2% ghost listings** (78.1% salary opacity) due to third-party syndication scraping, compared to Indeed's **1.8%** with direct ATS webhooks.
- 🏷️ **Snorkel Weak Supervision**: 14 programmatic labeling functions achieving Fleiss' Kappa agreement of **κ = 0.589** in the absence of ground truth.
- 🛡️ **Zero-Leakage ML & Calibration**: 5-Fold GroupKFold CV across 890 unique employer IDs with Platt calibration compressing Brier score down to **0.0167**.
- 🛠️ **BA Action Suite**: What-If Counterfactual Simulator (de-risking postings 95% → 15%), 5 tactical recruiter screening questions, bipartite job syndication graph, and executive dossier export.
- 🚀 **Deployment & Serving**: Sub-15ms FastAPI REST microservice (11 endpoints), zero-network Manifest V3 Chrome Extension, 15-tab Streamlit suite, and 8-page Power BI dashboard (\`Naukrisaaf_FinalDashboard.pbix\`).`
    },
    {
      kw: ["kavach", "security", "pii", "blast radius", "ast", "sentinel", "164 tests", "qdrant"],
      title: "Project 3: KAVACH — Architecture & Dependency Sentinel",
      ans: `**KAVACH** is an autonomous architecture & dependency sentinel built with Python, FastAPI, Qdrant vector database, and Google Gemini API.

- 🔒 **PII & Secret Scanner**: Deterministic regex & heuristic engine achieving **1.00 Precision, 1.00 Recall, and 1.00 F1** across Aadhaar, PAN, API keys, and JWT tokens.
- 🌐 **AST Blast-Radius Analyzer**: Static Abstract Syntax Tree analyzer computing cross-module dependency blast radius (**0.72 avg F1**).
- 🧪 **Test Suite**: **164/164 Pytest passing tests** with automated CI/CD gating and zero regression tolerances.`
    },
    {
      kw: ["archon", "apicopilot", "copilot", "llm", "rag", "benchmark", "gemma", "codellama", "qwen", "78"],
      title: "Project 4: Archon Copilot — Enterprise RAG & LLM Studio",
      ans: `**Archon Copilot** is an enterprise AI pair programmer featuring a Next.js 14 tabbed Web IDE and hybrid retrieval.

- 🔎 **Hybrid RAG**: Okapi BM25 sparse keyword search + ChromaDB dense vector embeddings + MS-Marco Cross-Encoder re-ranker.
- 📊 **Quantitative Benchmark**: Audited 78 evaluation pairs across multiple open-weight LLMs.
- 🏆 **Champion Model**: Google Gemma 3 4B achieved **71.15% correctness** (15.7s latency, 0% wrong rate post-indexing).
- 💻 **Code Accuracy**: Meta CodeLlama 7B achieved **100% code pass rate** with only 1 hallucination flag.
- ⚖️ **Evaluation Judge**: Scored by an automated $0 local Qwen 2.5-7B Chain-of-Thought Judge.`
    },
    {
      kw: ["grilli", "restaurant", "reservation", "mongodb", "express", "full stack"],
      title: "Project 5: Grilli — Table Reservation Platform",
      ans: `**Grilli** is a full-stack restaurant reservation system featuring real-time seating calendars, slot locking, email confirmations, 5 REST endpoints, and a custom Node.js/Express + MongoDB backend built from scratch with 6 resolved template bugs.`
    },
    {
      kw: ["kidlearn", "edtech", "gamified", "gamification", "learning", "pomodoro"],
      title: "Project 6: KidLearn — Gamified EdTech Habit Loop",
      ans: `**KidLearn** is a gamified EdTech habit loop tracking lessons across six academic subjects with 21 unlockable badges, a Pomodoro focus timer with direct XP logging, custom Canvas analytics charts, and weekly parent report cards — built 100% client-side in vanilla HTML/CSS/JS.`
    },
    {
      kw: ["sql lab", "duckdb", "workbench", "query", "queries", "olap"],
      title: "Interactive DuckDB SQL Workbench",
      ans: `The **Interactive SQL Lab** on this site runs a real in-browser DuckDB OLAP engine. You can execute 5 pre-loaded audit queries:
1. **Profitara**: CLV & Churn backtesting by customer cohort.
2. **Naukri Saaf**: Ghost job distribution and salary transparency by portal.
3. **KAVACH**: Audit trail of PII and security vulnerability scans.
4. **Archon Copilot**: Retrieval latency and correctness across 78 test pairs.
5. **Udaghosh**: Operational NGO fund disbursement and donor KPIs.`
    },
    {
      kw: ["download", "deliverables", "pbix", "power bi file", "dataset", "csv", "brd", "documentation"],
      title: "Repository Artifacts & Deliverables Hub",
      ans: `In the **Deliverables Hub** (#artifacts) on this website, you can directly download:
- 📊 **Profitara Power BI Model**: \`Profitara_BIDashBoard.pbix\` (4.8 MB)
- 📊 **Naukri Saaf Power BI Model**: \`Naukrisaaf_FinalDashboard.pbix\` (3.1 MB)
- 📁 **Datasets**: 10,000 quick-commerce orders CSV & 2,851 scraped job listings CSV.
- 📝 **SQL Scripts**: 42 production queries across DuckDB, PostgreSQL, and MySQL.
- 📑 **Business Documentation**: Complete Business Analyst BRD / SRS packages.
- 📄 **Resume PDF**: Dhruv's verified 1-page ATS resume (\`DhruvJain_Resume.pdf\`).`
    },
    {
      kw: ["certification", "certificates", "certified", "pl-300", "coursera", "credentials"],
      title: "Verified Industry Certifications (10 Credentials)",
      ans: `Dhruv holds **10 verified industry credentials**:
- 🏆 **Microsoft Power BI (5 Credentials)**: Data Modeling, ETL & Data Prep, Creative Designing, Harnessing Data, Dashboard Architecture.
- 🛡️ **IoT Security & Privacy**: CertNexus Certified Professional in IoT Security.
- 🎨 **Canva & Figma Design (4 Credentials)**: Customer Personas, Digital Product Prototyping, Storyboarding, Component Design Systems.

All certificate images can be viewed with high-resolution lightbox inspection in the Certifications section.`
    },
    {
      kw: ["contact", "email", "phone", "reach", "hire", "interview", "call", "connect", "location"],
      title: "Contact & Hiring Information",
      ans: `**Get in Touch with Dhruv Jain:**

- 📧 **Email**: [jaindhruv1923@gmail.com](mailto:jaindhruv1923@gmail.com)
- 📱 **Phone**: [+91 99118 50506](tel:+919911850506)
- 📍 **Location**: Gurugram / Delhi-NCR, India (Open to On-site, Hybrid, and Remote roles worldwide)
- 💼 **LinkedIn**: [linkedin.com/in/jaindhruv1923](https://www.linkedin.com/in/jaindhruv1923)
- 🐙 **GitHub**: [github.com/jaindhruv1923](https://github.com/jaindhruv1923)

Dhruv is available immediately for full-time Data Analyst, BI Analyst, and Analytics Engineer roles.`
    },
    {
      kw: ["resume", "cv", "pdf", "download resume"],
      title: "Verified 1-Page ATS Resume",
      ans: `You can download Dhruv's verified **1-Page ATS Resume PDF** directly:
- 📄 Click **[Download DhruvJain_Resume.pdf](assets/DhruvJain_Resume.pdf)**
- It is also accessible at any time from the top navigation bar button (**Resume (1-Page) ↓**).`
    }
  ];

  // ----------------------------------------------------------------------------
  // 2. SPECIALIZED DATA SCIENCE & ENGINEERING ENCYCLOPEDIA (Instant Depth)
  // ----------------------------------------------------------------------------
  const DS_ENCYCLOPEDIA = [
    {
      kw: ["random forest vs xgboost", "rf vs xgboost", "xgboost vs random forest", "difference between random forest and xgboost"],
      title: "Random Forest vs XGBoost: Deep Architectural Comparison",
      ans: `**Random Forest vs XGBoost** represent two foundational paradigms of ensemble learning:

### 1. Architectural Philosophy
- **Random Forest (Bagging)**: Builds multiple independent decision trees in parallel using bootstrap samples. Trees are grown deep (low bias, high variance) and their predictions are averaged (regression) or voted (classification) to reduce variance.
- **XGBoost (Boosting)**: Builds trees sequentially in series. Each subsequent tree predicts and corrects the **pseudo-residuals (gradients)** of the preceding trees, optimizing an objective function with second-order Taylor approximations.

### 2. Key Differences Matrix
- **Training Paradigm**: Parallel (RF) vs Sequential (XGBoost).
- **Overfitting Risk**: RF rarely overfits with more trees; XGBoost can overfit if learning rate ($\eta$) is too high or early stopping is omitted.
- **Hyperparameter Sensitivity**: RF is robust with default settings; XGBoost requires careful tuning of \`learning_rate\`, \`max_depth\`, \`subsample\`, and regularization terms (\`reg_alpha\`, \`reg_lambda\`).
- **Handling Missing Values**: XGBoost natively routes missing values along optimal default split paths; RF typically requires prior imputation.

\`\`\`python
# Example: Training XGBoost vs Random Forest in Scikit-Learn / XGBoost
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Random Forest: parallel, robust defaults
rf = RandomForestClassifier(n_estimators=200, max_features="sqrt", random_state=42)

# XGBoost: gradient boosted, sequential residual correction
xgb = XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=5, reg_lambda=1.0)
\`\`\``
    },
    {
      kw: ["roc auc", "what is roc auc", "auc roc", "receiver operating characteristic", "explain roc"],
      title: "ROC-AUC Explained: The Standard in Imbalanced Classification",
      ans: `**ROC-AUC (Receiver Operating Characteristic — Area Under the Curve)** evaluates how well a classifier separates positive and negative classes across **all possible classification thresholds** (0.0 to 1.0).

### Key Components:
- **True Positive Rate (TPR / Recall / Sensitivity)**:
  $$\\text{TPR} = \\frac{\\text{TP}}{\\text{TP} + \\text{FN}}$$
- **False Positive Rate (FPR / 1 - Specificity)**:
  $$\\text{FPR} = \\frac{\\text{FP}}{\\text{FP} + \\text{TN}}$$
- **The ROC Curve**: Plots TPR (y-axis) against FPR (x-axis) as the decision threshold varies from 1 down to 0.

### Interpreting the AUC Score:
- **1.0**: Perfect discrimination (100% true positives before any false positives).
- **0.90 – 0.99**: Outstanding discrimination (e.g. Dhruv's Naukri Saaf model achieved **0.920 ROC-AUC**).
- **0.70 – 0.80**: Acceptable discrimination.
- **0.50**: No better than random coin-flip guessing.

*Advantage*: Unlike raw accuracy, ROC-AUC is completely invariant to class distribution skew, making it the golden metric for fraud detection, churn prediction, and ghost job classification.`
    },
    {
      kw: ["bias variance", "bias variance tradeoff", "overfitting vs underfitting"],
      title: "The Bias-Variance Tradeoff Explained",
      ans: `The **Bias-Variance Tradeoff** is the central optimization tension in supervised machine learning:

$$\\text{Total Error} = \\text{Bias}^2 + \\text{Variance} + \\text{Irreducible Error (\\sigma^2)}$$

### 1. High Bias (Underfitting)
- **Symptom**: Model is too simplistic to capture underlying patterns. Both training error and test error are unacceptably high.
- **Examples**: Linear regression on nonlinear data, shallow decision tree (depth=1).
- **Remedies**: Increase model complexity, engineer polynomial/interaction features, reduce regularization.

### 2. High Variance (Overfitting)
- **Symptom**: Model memorizes noise and idiosyncrasies in the training set. Training error is near zero, but validation error spikes.
- **Examples**: Fully grown unpruned decision trees, neural network with too many parameters and no dropout.
- **Remedies**: Cross-validation (K-Fold), bagging/ensembling, L1/L2 regularization, dropout, pruning, collecting more training data.`
    },
    {
      kw: ["transformer", "self attention", "attention mechanism", "how transformers work"],
      title: "How Transformers & Scaled Dot-Product Attention Work",
      ans: `The **Transformer** (Vaswani et al., 2017) eliminated recurrence (RNNs) in favor of parallelized **Self-Attention**:

### Scaled Dot-Product Attention Formula:
$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V$$

- **Query ($Q$)**: What the current token is seeking.
- **Key ($K$)**: What other tokens offer.
- **Value ($V$)**: The actual semantic content of each token.
- **$\\sqrt{d_k}$ Scaling**: Prevents the dot products from growing excessively large for high dimensions, which would cause softmax gradients to vanish.

### Multi-Head Attention:
Rather than computing one single attention function, queries, keys, and values are linearly projected into $h$ distinct representation subspaces, enabling the model to jointly attend to information at different positions (e.g., syntactic vs semantic relationships).`
    },
    {
      kw: ["rag", "retrieval augmented generation", "what is rag", "rag architecture"],
      title: "Retrieval-Augmented Generation (RAG) Architecture",
      ans: `**RAG (Retrieval-Augmented Generation)** enhances Large Language Models by grounding them dynamically in external, verified factual data before generation:

### Core Pipeline Stages:
1. **Ingestion & Chunking**: Documents are split into semantic chunks (e.g., 500 tokens with 50-token overlap).
2. **Dense Vector Embedding**: Chunks are encoded via embedding models (e.g., \`text-embedding-3\`, \`bge-m3\`) into a vector database (Qdrant, ChromaDB).
3. **Hybrid Retrieval**:
   - **Sparse Search (BM25)**: Matches exact keywords, codes, and IDs.
   - **Dense Search (Cosine Similarity)**: Captures semantic intent and synonyms.
4. **Cross-Encoder Re-Ranking**: Scores top-k candidates for maximal contextual precision.
5. **Prompt Augmentation**: LLM receives the user question + retrieved ground-truth passages to generate verified answers with zero hallucinations.`
    },
    {
      kw: ["duckdb vs postgresql", "duckdb vs postgres", "olap vs oltp", "when to use duckdb"],
      title: "DuckDB vs PostgreSQL: OLAP vs OLTP",
      ans: `**DuckDB vs PostgreSQL** serve complementary purposes in modern data architectures:

| Feature | PostgreSQL (OLTP) | DuckDB (OLAP) |
|---|---|---|
| **Primary Workload** | High-concurrency row transactions (INSERT, UPDATE) | Complex analytical aggregations (SUM, AVG, GROUP BY) |
| **Storage Engine** | Row-oriented (Heap tuples) | Columnar (Vectorized execution) |
| **Execution Model** | Client-server daemon process | In-process embedded (like SQLite for analytics) |
| **Direct File Queries** | Requires FDW (Foreign Data Wrappers) | Queries Parquet, CSV, JSON directly with zero copy |
| **Memory Footprint** | Heavy server deployment | Tiny zero-dependency footprint |

*Why Dhruv uses DuckDB*: In Profitara and on this portfolio website, DuckDB delivers instant sub-second SQL aggregations across hundreds of thousands of rows entirely in-memory without needing a remote database server.`
    },
    {
      kw: ["star schema vs snowflake", "star schema", "data warehouse modeling"],
      title: "Star Schema vs Snowflake Schema in Data Warehousing",
      ans: `### 1. Star Schema (Denormalized)
- **Structure**: A central **Fact table** surrounded directly by **Dimension tables**, forming a single-hop star shape.
- **Normalization**: Dimensions are intentionally denormalized (some redundancy).
- **Performance**: Extremely fast query performance because analytical queries require fewer JOIN operations.
- **Power BI Standard**: Microsoft Power BI strongly recommends Star Schema for high-speed VertiPaq compression.

### 2. Snowflake Schema (Normalized)
- **Structure**: Dimension tables are further normalized into sub-dimensions (e.g., \`Product\` -> \`SubCategory\` -> \`Category\`).
- **Advantages**: Eliminates data redundancy, minimizes storage footprint.
- **Trade-off**: Requires multiple complex JOINs, degrading interactive analytical performance in BI reporting.`
    }
  ];

  // ----------------------------------------------------------------------------
  // 3. MATH & CALCULATION EVALUATOR (Safe Client-Side Engine)
  // ----------------------------------------------------------------------------
  function evaluateMathExpression(str) {
    const clean = str.replace(/calculate|what is|solve|compute|find/gi, "").trim();
    
    // Check for percentage calculation (e.g., "15% of 66.95" or "15% of 6695000")
    const pctMatch = clean.match(/([\d.]+)\s*%\s*of\s*([\d.]+)/i);
    if (pctMatch) {
      const pct = parseFloat(pctMatch[1]);
      const base = parseFloat(pctMatch[2]);
      const res = (pct / 100) * base;
      return {
        isMath: true,
        expr: `${pct}% of ${base}`,
        res: res.toLocaleString("en-US", { maximumFractionDigits: 4 }),
        explanation: `$$\\frac{${pct}}{100} \\times ${base} = ${res.toLocaleString("en-US", { maximumFractionDigits: 4 })}$$`
      };
    }

    // Check for square root
    const sqrtMatch = clean.match(/sqrt\s*\(\s*([\d.]+)\s*\)/i);
    if (sqrtMatch) {
      const val = parseFloat(sqrtMatch[1]);
      const res = Math.sqrt(val);
      return {
        isMath: true,
        expr: `sqrt(${val})`,
        res: res.toString(),
        explanation: `$$\\sqrt{${val}} = ${res}$$`
      };
    }

    // Safe sanitized arithmetic evaluation (numbers, +, -, *, /, ^, parentheses)
    const sanitized = clean.replace(/\^/g, "**").replace(/x/gi, "*");
    if (/^[\d.\s+\-*/()]+$/.test(sanitized) && /[\d]/.test(sanitized)) {
      try {
        // Safe evaluation without eval scope leak
        const fn = new Function(`"use strict"; return (${sanitized});`);
        const val = fn();
        if (typeof val === "number" && !isNaN(val) && isFinite(val)) {
          return {
            isMath: true,
            expr: clean,
            res: val.toLocaleString("en-US", { maximumFractionDigits: 6 }),
            explanation: `Computed: **${clean}** = **${val.toLocaleString("en-US", { maximumFractionDigits: 6 })}**`
          };
        }
      } catch (e) {
        // Not a pure arithmetic expression, continue to next engines
      }
    }

    return { isMath: false };
  }

  // ----------------------------------------------------------------------------
  // 4. LIVE UNIVERSAL WORLD KNOWLEDGE ENGINE (Wikipedia REST + OpenSearch)
  // ----------------------------------------------------------------------------
  async function queryWorldKnowledge(query) {
    try {
      // 1. Search Wikipedia for top matching article title
      const searchUrl = `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&utf8=&format=json&origin=*`;
      const searchResp = await fetch(searchUrl, { headers: { "Accept": "application/json" } });
      if (!searchResp.ok) throw new Error("Search API unreachable");
      const searchData = await searchResp.json();

      const searchList = searchData?.query?.search;
      if (!searchList || searchList.length === 0) return null;

      const topResult = searchList[0];
      const pageTitle = topResult.title;

      // 2. Fetch full REST Summary for top result
      const summaryUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(pageTitle.replace(/ /g, "_"))}`;
      const summaryResp = await fetch(summaryUrl);
      if (!summaryResp.ok) throw new Error("Summary API unreachable");
      const summaryData = await summaryResp.json();

      const title = summaryData.title || pageTitle;
      const description = summaryData.description ? `*(${summaryData.description})*` : "";
      const extract = summaryData.extract || "";
      const pageUrl = summaryData.content_urls?.desktop?.page || `https://en.wikipedia.org/wiki/${encodeURIComponent(pageTitle)}`;

      // Related articles discovered
      const related = searchList.slice(1, 4).map(item => `\`${item.title}\``).join(", ");

      if (!extract || extract.length < 30) return null;

      return {
        title: title,
        description: description,
        extract: extract,
        pageUrl: pageUrl,
        related: related
      };
    } catch (err) {
      console.warn("World Knowledge retrieval note:", err);
      return null;
    }
  }

  // ----------------------------------------------------------------------------
  // 5. GOOGLE GEMINI 1.5 FLASH DIRECT REST CALL (When Key Provided)
  // ----------------------------------------------------------------------------
  async function callGeminiDirect(apiKey, userPrompt) {
    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

    const systemContext = `You are Gemini Intelligence, an elite AI assistant embedded inside Dhruv Jain's portfolio.
Dhruv Jain Profile:
- Final-year B.Tech CSE (AI & Data Science) at BML Munjal University, Gurugram (Hero Group, 2023–2027).
- Flagship projects: Profitara (Retail BI, ₹66.95L revenue, 10,000 txns, 4,918 orders, R2=0.930 CLV, AUC=0.91 churn, 52 Apriori rules, Power BI .pbix), Naukri Saaf (2,851 scraped jobs, Snorkel kappa=0.589, 5-Fold GroupKFold, LightGBM 0.920 ROC-AUC, TreeSHAP, Chrome Extension), KAVACH (1.00 PII F1, 164 Pytest passing tests), Archon Copilot (78 LLM pairs, Gemma 3 4B 71.15% correctness, CodeLlama 7B 100% pass).
- Internships: Udaghosh (Data Analyst) & Contentora (MIS Analyst).
- Contact: jaindhruv1923@gmail.com, +91 99118 50506, Gurugram/Delhi NCR.
- Resume: DhruvJain_Resume.pdf.

Instructions:
1. If the user asks about Dhruv Jain, use the verified portfolio facts above with high precision.
2. If the user asks ANY OTHER QUESTION IN THE WORLD (coding, math, science, history, economics, algorithms, trivia), answer thoroughly, intelligently, and clearly with elegant markdown formatting, bold keywords, and clean code blocks.`;

    const payload = {
      contents: [
        {
          role: "user",
          parts: [{ text: `${systemContext}\n\nUser Question: ${userPrompt}` }]
        }
      ],
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 1024
      }
    };

    const resp = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const errJson = await resp.json().catch(() => ({}));
      throw new Error(errJson?.error?.message || `HTTP ${resp.status}`);
    }

    const data = await resp.json();
    const candidate = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!candidate) throw new Error("Empty response from Gemini");
    return candidate;
  }

  // ----------------------------------------------------------------------------
  // 6. QUERY SCORING & MATCHING ENGINE
  // ----------------------------------------------------------------------------
  function normalizeText(s) {
    return s.toLowerCase().replace(/[^\w\s]/g, " ").replace(/\s+/g, " ").trim();
  }

  function scoreKBEntry(qNorm, entry) {
    let score = 0;
    for (const kw of entry.kw) {
      const kwNorm = normalizeText(kw);
      if (!kwNorm) continue;
      if (qNorm.includes(kwNorm)) {
        score += kwNorm.split(" ").length * 2.5;
        continue;
      }
      const tokens = kwNorm.split(" ");
      if (tokens.length > 1 && tokens.every(t => qNorm.includes(t))) {
        score += tokens.length * 1.5;
      }
    }
    return score;
  }

  function findBestKBEntry(query, kb) {
    const qNorm = normalizeText(query);
    let best = null;
    let bestScore = 0;
    for (const item of kb) {
      const s = scoreKBEntry(qNorm, item);
      if (s > bestScore) {
        bestScore = s;
        best = item;
      }
    }
    return bestScore >= 1.5 ? best : null;
  }

  // ----------------------------------------------------------------------------
  // 7. MARKDOWN TO HTML RENDERER (Safe & Rich Code Copying)
  // ----------------------------------------------------------------------------
  function escapeHtml(text) {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
    return String(text).replace(/[&<>"']/g, m => map[m]);
  }

  function renderMarkdown(text) {
    if (!text) return "";

    // 1. Extract fenced code blocks
    const codeBlocks = [];
    let processed = text.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      const token = `__CODE_BLOCK_${codeBlocks.length}__`;
      codeBlocks.push({ lang: lang || "code", code: code.trim() });
      return token;
    });

    // 2. Escape HTML
    processed = escapeHtml(processed);

    // 3. Headers: ### Title -> <h4 class="cb-heading">Title</h4>
    processed = processed.replace(/^### (.*$)/gim, '<h4 class="cb-heading">$1</h4>');
    processed = processed.replace(/^## (.*$)/gim, '<h4 class="cb-heading">$1</h4>');

    // 4. Bold: **text** -> <strong>text</strong>
    processed = processed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // 5. Italic: *text* -> <em>text</em>
    processed = processed.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // 6. Inline code: `code` -> <code class="cb-inline-code">code</code>
    processed = processed.replace(/`([^`]+)`/g, '<code class="cb-inline-code">$1</code>');

    // 7. Links: [text](url) -> <a href="url" target="_blank" class="cb-link">text ↗</a>
    processed = processed.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" class="cb-link">$1 ↗</a>');

    // 8. Bullet lists: - item -> <li>item</li>
    processed = processed.replace(/^\s*[-*]\s+(.*)$/gim, '<li>$1</li>');
    processed = processed.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
    processed = processed.replace(/<\/ul>\s*<ul>/g, ''); // merge adjacent <ul>

    // 9. Paragraphs and linebreaks
    processed = processed.replace(/\n\n+/g, '</p><p>');
    processed = '<p>' + processed + '</p>';
    processed = processed.replace(/<p>\s*<\/p>/g, '');

    // 10. Re-inject Code Blocks
    codeBlocks.forEach((cb, idx) => {
      const token = `__CODE_BLOCK_${idx}__`;
      const htmlBlock = `
        <div class="cb-code-block">
          <div class="cb-code-header">
            <span>${escapeHtml(cb.lang)}</span>
            <button class="cb-copy-btn" data-code="${escapeHtml(cb.code)}">📋 Copy</button>
          </div>
          <pre><code>${escapeHtml(cb.code)}</code></pre>
        </div>`;
      processed = processed.replace(token, htmlBlock);
    });

    return processed;
  }

  // ----------------------------------------------------------------------------
  // 8. UI CONTROLLER & EVENT ORCHESTRATION
  // ----------------------------------------------------------------------------
  let isThinking = false;

  function addMessage(badgeType, badgeText, contentHtml, sender) {
    const log = document.getElementById("cb-log");
    if (!log) return;

    const div = document.createElement("div");
    div.className = `cb-msg ${sender}`;

    if (sender === "bot") {
      let badgeHtml = "";
      if (badgeType && badgeText) {
        badgeHtml = `<span class="cb-badge ${badgeType}">${badgeText}</span>`;
      }
      div.innerHTML = `${badgeHtml}<div class="cb-msg-body">${contentHtml}</div>`;
    } else {
      div.textContent = contentHtml;
    }

    log.appendChild(div);
    log.scrollTop = log.scrollHeight;

    // Attach copy button listeners
    div.querySelectorAll(".cb-copy-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const code = btn.getAttribute("data-code");
        navigator.clipboard.writeText(code).then(() => {
          btn.textContent = "✓ Copied!";
          btn.style.color = "#7ee787";
          setTimeout(() => {
            btn.textContent = "📋 Copy";
            btn.style.color = "";
          }, 2000);
        });
      });
    });
  }

  function showThinkingIndicator(statusText = "Reasoning with World AI...") {
    const log = document.getElementById("cb-log");
    if (!log) return;
    removeThinkingIndicator();

    const indicator = document.createElement("div");
    indicator.id = "cb-thinking-indicator";
    indicator.className = "cb-thinking";
    indicator.innerHTML = `
      <div class="cb-google-dots">
        <span class="cb-dot blue"></span>
        <span class="cb-dot red"></span>
        <span class="cb-dot yellow"></span>
        <span class="cb-dot green"></span>
      </div>
      <span class="cb-thinking-text">${escapeHtml(statusText)}</span>
    `;
    log.appendChild(indicator);
    log.scrollTop = log.scrollHeight;
    isThinking = true;
  }

  function removeThinkingIndicator() {
    const el = document.getElementById("cb-thinking-indicator");
    if (el) el.remove();
    isThinking = false;
  }

  // Master Query Resolution Pipeline
  async function processUserQuery(query) {
    if (!query || !query.trim() || isThinking) return;
    const cleanQ = query.trim();

    // 1. Add user message
    addMessage(null, null, cleanQ, "user");

    // Clear input
    const input = document.getElementById("cb-input");
    if (input) input.value = "";
    const clearBtn = document.getElementById("cb-clear-input");
    if (clearBtn) clearBtn.classList.remove("visible");

    // 2. Check Math Engine (Instant)
    const mathResult = evaluateMathExpression(cleanQ);
    if (mathResult.isMath) {
      showThinkingIndicator("Computing mathematical solution...");
      setTimeout(() => {
        removeThinkingIndicator();
        const html = `<p><strong>Result:</strong> ${mathResult.explanation}</p><p>Final value: <code class="cb-inline-code">${mathResult.res}</code></p>`;
        addMessage("math", "🧮 Math Engine", html, "bot");
      }, 350);
      return;
    }

    // 3. Check Portfolio Ledger (Instant Ground Truth)
    const portfolioMatch = findBestKBEntry(cleanQ, PORTFOLIO_KB);
    if (portfolioMatch) {
      showThinkingIndicator("Auditing verified portfolio records...");
      setTimeout(() => {
        removeThinkingIndicator();
        const html = renderMarkdown(portfolioMatch.ans);
        addMessage("portfolio", "📊 Verified Portfolio Ledger", html, "bot");
      }, 400);
      return;
    }

    // 4. Check Optional Direct Google Gemini API Key
    const apiKey = localStorage.getItem("gemini_api_key");
    if (apiKey && apiKey.startsWith("AIzaSy")) {
      showThinkingIndicator("Synthesizing via Google Gemini 1.5 Flash...");
      try {
        const geminiText = await callGeminiDirect(apiKey, cleanQ);
        removeThinkingIndicator();
        addMessage("gemini", "⚡ Google Gemini 1.5 Flash", renderMarkdown(geminiText), "bot");
        return;
      } catch (err) {
        console.warn("Direct Gemini call failed, falling back to World Engine:", err);
      }
    }

    // 5. Check Specialized Data Science & Engineering Encyclopedia
    const dsMatch = findBestKBEntry(cleanQ, DS_ENCYCLOPEDIA);
    if (dsMatch) {
      showThinkingIndicator("Consulting Data Science Encyclopedia...");
      setTimeout(() => {
        removeThinkingIndicator();
        const html = renderMarkdown(dsMatch.ans);
        addMessage("world", "🧠 Data Science & AI Encyclopedia", html, "bot");
      }, 500);
      return;
    }

    // 6. Live Universal World Knowledge Engine (Wikipedia OpenSearch + REST)
    showThinkingIndicator("Consulting Universal World Knowledge...");
    try {
      const worldResult = await queryWorldKnowledge(cleanQ);
      removeThinkingIndicator();

      if (worldResult) {
        const bodyMd = `### ${worldResult.title} ${worldResult.description}\n\n${worldResult.extract}\n\n- **Related Search Concepts**: ${worldResult.related}\n- **Live Source**: [Read full article on Wikipedia](${worldResult.pageUrl})`;
        addMessage("world", "✨ Google World AI · Live Search", renderMarkdown(bodyMd), "bot");
      } else {
        // Helpful universal fallback
        const fallbackMd = `I searched universal knowledge for **"${escapeHtml(cleanQ)}"**. 
        
You can ask me **anything in the world**:
- 🧠 **Data Science & ML**: *"Explain Random Forest vs XGBoost"*, *"What is ROC-AUC?"*, *"How do Transformers work?"*
- 🧮 **Calculations**: *"Calculate 15% of 6695000"*, *"sqrt(256)"*
- 💻 **Code & Queries**: *"Write DuckDB SQL for running totals"*, *"FastAPI endpoint example"*
- 🚀 **Dhruv's Work**: *"Tell me about Profitara"*, *"How does Naukri Saaf detect ghost jobs?"*, *"Download Power BI models"*

*(Tip: You can also click the ⚙️ icon in the header to enter your free Google AI Studio key for direct Gemini 1.5 Flash inference!)*`;
        addMessage("world", "✨ Gemini Assistant", renderMarkdown(fallbackMd), "bot");
      }
    } catch (e) {
      removeThinkingIndicator();
      addMessage("world", "✨ Gemini Assistant", `<p>I am ready to answer any question about Dhruv's 6 projects, data analytics, ML engineering, or universal concepts. Ask away!</p>`, "bot");
    }
  }

  // ----------------------------------------------------------------------------
  // 9. INITIALIZE & AUTO-MOUNT COMPONENT
  // ----------------------------------------------------------------------------
  function ensureChatbotMarkup() {
    const existingChips = document.getElementById("cb-chips");
    if (!existingChips) {
      const oldPanel = document.getElementById("chatbot-panel");
      const oldToggle = document.getElementById("chatbot-toggle");
      if (oldPanel) oldPanel.remove();
      if (oldToggle) oldToggle.remove();

      const container = document.createElement("div");
      container.innerHTML = `
<!-- FLOATING GOOGLE GEMINI AI ASSISTANT -->
<button id="chatbot-toggle" aria-label="Ask Dhruv's Gemini AI Assistant">
  <svg viewBox="0 0 24 24" fill="none">
    <defs>
      <linearGradient id="geminiSparkleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#4285F4"/>
        <stop offset="35%" stop-color="#9B72CF"/>
        <stop offset="70%" stop-color="#D96570"/>
        <stop offset="100%" stop-color="#F4B400"/>
      </linearGradient>
    </defs>
    <path fill="url(#geminiSparkleGrad)" d="M12 1.5C12 7.298 7.298 12 1.5 12C7.298 12 12 16.702 12 22.5C12 16.702 16.702 12 22.5 12C16.702 12 12 7.298 12 1.5Z"/>
  </svg>
  <span class="cb-toggle-badge">AI</span>
</button>

<div id="chatbot-panel" role="dialog" aria-label="Gemini AI Assistant">
  <div class="cb-header">
    <div class="cb-header-left">
      <div class="cb-header-icon">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none">
          <path fill="url(#geminiSparkleGrad)" d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z"/>
        </svg>
      </div>
      <div class="cb-header-titles">
        <strong>Gemini Intelligence <span class="cb-model-tag">Universal</span></strong>
        <span class="cb-sub">Dhruv Jain Copilot · Answers Anything in the World</span>
      </div>
    </div>
    <div class="cb-header-actions">
      <button class="cb-tool-btn" id="cb-settings-toggle" title="Settings &amp; Gemini Key">⚙️</button>
      <button class="cb-tool-btn" id="cb-clear-chat" title="Clear chat history">🗑️</button>
      <button class="cb-tool-btn" id="cb-close-panel" title="Close panel">✕</button>
    </div>
  </div>

  <div class="cb-subbar">
    <div class="cb-subbar-status">
      <span class="cb-status-led"></span>
      <span id="cb-engine-label">Connected · World AI &amp; Portfolio Grounding</span>
    </div>
    <span class="cb-subbar-mode" id="cb-engine-tier">Live Free</span>
  </div>

  <!-- Optional Settings Drawer for Custom Gemini Key -->
  <div class="cb-settings-drawer hidden" id="cb-settings-drawer">
    <h4>⚙️ Google Gemini API Key (Optional)</h4>
    <p>Paste your free Google AI Studio key for direct Google Gemini 1.5 Flash generation. If empty, the live World Search &amp; Knowledge Engine runs automatically.</p>
    <div class="cb-key-row">
      <input type="password" id="cb-api-key-input" placeholder="AIzaSy... (saved locally)" />
      <button id="cb-save-key-btn">Save</button>
    </div>
    <div class="cb-key-help">
      <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener">Get a 100% free Gemini API key ↗</a>
      <span id="cb-key-feedback"></span>
    </div>
  </div>

  <div id="cb-log"></div>

  <div class="cb-chip-row" id="cb-chips">
    <span class="cb-chip" data-q="Who is Dhruv Jain?">👤 Who is Dhruv?</span>
    <span class="cb-chip" data-q="Tell me about Profitara and its ML metrics">🛒 Profitara (₹66.95L)</span>
    <span class="cb-chip" data-q="How does Naukri Saaf detect ghost jobs?">👻 Naukri Saaf</span>
    <span class="cb-chip" data-q="What is KAVACH sentinel and its PII F1 score?">🛡️ KAVACH Sentinel</span>
    <span class="cb-chip" data-q="Explain Random Forest vs XGBoost">🌲 RF vs XGBoost</span>
    <span class="cb-chip" data-q="Write DuckDB SQL for running revenue totals">📊 DuckDB Running Totals</span>
    <span class="cb-chip" data-q="What is Quantum Computing?">⚛️ Quantum Computing</span>
    <span class="cb-chip" data-q="How to reach Dhruv for an interview?">📬 Contact &amp; Resume</span>
  </div>

  <div class="cb-input-wrap">
    <div class="cb-search-pill">
      <svg class="cb-sparkle-icon" viewBox="0 0 24 24" fill="none">
        <path fill="url(#geminiSparkleGrad)" d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z"/>
      </svg>
      <input id="cb-input" type="text" placeholder="Ask anything in the world or about Dhruv's work..." autocomplete="off" />
      <button id="cb-clear-input" title="Clear text">✕</button>
      <button id="cb-send" aria-label="Send message">
        <svg viewBox="0 0 24 24">
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
        </svg>
      </button>
    </div>
    <div class="cb-footer-note">
      <span>Gemini Intelligence</span> · <span>Answers any question in the world</span>
    </div>
  </div>
</div>
      `;
      while (container.firstElementChild) {
        document.body.appendChild(container.firstElementChild);
      }
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    ensureChatbotMarkup();

    const toggle = document.getElementById("chatbot-toggle");
    const panel = document.getElementById("chatbot-panel");
    const input = document.getElementById("cb-input");
    const sendBtn = document.getElementById("cb-send");
    const clearInputBtn = document.getElementById("cb-clear-input");
    const closeBtn = document.getElementById("cb-close-panel");
    const clearChatBtn = document.getElementById("cb-clear-chat");
    const settingsToggle = document.getElementById("cb-settings-toggle");
    const settingsDrawer = document.getElementById("cb-settings-drawer");
    const apiKeyInput = document.getElementById("cb-api-key-input");
    const saveKeyBtn = document.getElementById("cb-save-key-btn");
    const keyFeedback = document.getElementById("cb-key-feedback");
    const engineTier = document.getElementById("cb-engine-tier");

    // Update tier badge if key exists
    function updateKeyStatusUI() {
      const savedKey = localStorage.getItem("gemini_api_key");
      if (savedKey && savedKey.startsWith("AIzaSy")) {
        if (apiKeyInput) apiKeyInput.value = savedKey;
        if (engineTier) {
          engineTier.textContent = "Gemini Flash";
          engineTier.style.color = "#ff7b72";
        }
        if (keyFeedback) {
          keyFeedback.textContent = "✓ Active";
          keyFeedback.style.color = "#34A853";
        }
      } else {
        if (engineTier) {
          engineTier.textContent = "Live Free";
          engineTier.style.color = "#79c0ff";
        }
        if (keyFeedback) keyFeedback.textContent = "";
      }
    }
    updateKeyStatusUI();

    // Toggle Chatbot Panel
    let hasGreeted = false;
    if (toggle && panel) {
      toggle.addEventListener("click", () => {
        panel.classList.toggle("open");
        if (panel.classList.contains("open")) {
          if (!hasGreeted) {
            const welcomeText = `**Hello! I'm Gemini Intelligence · Dhruv Jain's Portfolio Copilot.**

I can answer **anything in the world**:
- 🌍 **Universal Knowledge**: Science, math, history, world trivia, and philosophy.
- 💻 **Technical Deep-Dives**: ML algorithms, DuckDB SQL, Python pipelines, and BI modeling.
- 📊 **Dhruv's Verified Ledger**: 6 flagship audited projects (**₹66.95L Profitara, 2,851 Naukri Saaf ghost jobs, KAVACH, Archon**), 10 certifications, and his verified 1-page resume.

What would you like to explore today?`;
            addMessage("world", "✨ Gemini Intelligence", renderMarkdown(welcomeText), "bot");
            hasGreeted = true;
          }
          setTimeout(() => input?.focus(), 250);
        }
      });
    }

    // Close Panel
    if (closeBtn && panel) {
      closeBtn.addEventListener("click", () => panel.classList.remove("open"));
    }

    // Clear Chat
    if (clearChatBtn) {
      clearChatBtn.addEventListener("click", () => {
        const log = document.getElementById("cb-log");
        if (log) {
          log.innerHTML = "";
          hasGreeted = false;
          toggle?.click();
          toggle?.click();
        }
      });
    }

    // Toggle Settings Drawer
    if (settingsToggle && settingsDrawer) {
      settingsToggle.addEventListener("click", () => {
        settingsDrawer.classList.toggle("hidden");
      });
    }

    // Save API Key
    if (saveKeyBtn && apiKeyInput) {
      saveKeyBtn.addEventListener("click", () => {
        const val = apiKeyInput.value.trim();
        if (val) {
          localStorage.setItem("gemini_api_key", val);
          if (keyFeedback) {
            keyFeedback.textContent = "Saved & Activated!";
            keyFeedback.style.color = "#34A853";
          }
        } else {
          localStorage.removeItem("gemini_api_key");
          if (keyFeedback) {
            keyFeedback.textContent = "Cleared (World Engine Active)";
            keyFeedback.style.color = "#79c0ff";
          }
        }
        updateKeyStatusUI();
      });
    }

    // Input changes & Send action
    if (input) {
      input.addEventListener("input", () => {
        if (clearInputBtn) {
          if (input.value.trim()) clearInputBtn.classList.add("visible");
          else clearInputBtn.classList.remove("visible");
        }
      });

      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          processUserQuery(input.value);
        }
      });
    }

    if (clearInputBtn && input) {
      clearInputBtn.addEventListener("click", () => {
        input.value = "";
        clearInputBtn.classList.remove("visible");
        input.focus();
      });
    }

    if (sendBtn && input) {
      sendBtn.addEventListener("click", () => {
        processUserQuery(input.value);
      });
    }

    // Suggestion Chips Click
    document.querySelectorAll(".cb-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        const q = chip.getAttribute("data-q") || chip.textContent;
        processUserQuery(q);
      });
    });
  });
})();
