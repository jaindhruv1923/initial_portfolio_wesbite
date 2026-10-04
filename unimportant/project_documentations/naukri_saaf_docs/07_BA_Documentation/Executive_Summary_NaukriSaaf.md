<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Executive%20Summary&fontSize=34&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Naukri%20Saaf%20%C2%B7%20Recruitment%20Quality%20Analytics&descAlignY=68&descSize=14)

</div>

## 🔮 Headline Finding

**Employer posting behavior, listing age at scrape time, and salary disclosure provide measurable signals for identifying ghost job postings.** Across 2,851 deduplicated job listings from LinkedIn, Indeed, and Glassdoor, the overall mean listing age at scrape date was **32.7 days** (median **11.0 days**), with older listings heavily concentrated on Glassdoor (mean **63.8 days**, median **41.0 days**). Postings with hidden compensation exhibited significantly higher risk scores and longer lingering times than transparent roles.

<br/>

<div align="center">

| 2,851 | 180 | 80 | 0.0167 |
|:---:|:---:|:---:|:---:|
| Cleaned Listings Analyzed | Silver Proxy Listings | Blind Human Verification Sample | Platt-Calibrated Brier Score |

</div>

<br/>

---

## 1️⃣ Breaking the Circular Labeling Trap (Snorkel Weak Supervision)

Traditional heuristic labeling uses a single arbitrary if-else rule (e.g., `if days_live > 60: ghost = 1`), causing supervised models to simply reverse-engineer programmer assumptions.
- **Approach**: Implemented 10 orthogonal domain Labeling Functions (LFs) capturing extreme age (>90 days), high repost velocity, personal contact bypass patterns (WhatsApp/Gmail), skeletal descriptions (<65 words), and salary disclosure.
- **Snorkel Generative Model**: Estimated LF accuracies using class-conditional likelihood ratio EM without ground truth.
- **Silver Proxy Benchmark**: Evaluated LF consensus against a 180-listing silver proxy set (`data/silver_labeling_sheet.csv`) generated via heuristic rules, boosting agreement (Cohen's Kappa) from 0.2545 to **0.5890** and F1 score from 0.4536 to **0.7130**.
- **Human Ground Truth**: Generated an independent blind evaluation sheet of 80 listings (`data/BLIND_LABELING_SHEET_80.csv`) with a standardized verification rubric (`LABELING_RUBRIC.md`) for verified human ground truth (`data/GOLD_LABELS_DONE.csv`).

<br/>

## 2️⃣ Leakage-Free Machine Learning & Platt Probability Calibration

- **Eliminating Entity Leakage**: Our `LeakageFreeFeatureExtractor` computes company repost dictionaries and target statistics strictly inside training folds. Unseen employers in test sets default to a single-post prior (1.0).
- **GroupKFold by Employer**: 5-Fold cross-validation grouped strictly by `company_name` across 1,231 unique employers achieved **0.9961 Out-of-Fold ROC-AUC** against weak supervision targets.
- **Platt Scaling Probability Calibration**: Reduced Brier Score from 0.0188 to **0.0167** and Expected Calibration Error (ECE) from 0.0366 to **0.0220** (-40% miscalibration), enabling consistent risk bucketing (**Genuine 60.0%**, **Suspect 25.0%**, **Ghost 15.0%**).

<br/>

## 3️⃣ Text Analysis & Semantic Similarity

- **Dense Semantic Encoder**: 64-dimensional latent semantic vector space via sublinear TF-IDF and Randomized SVD (LSA), executing in 1.4s across all listings.
- **Text Similarity**: Evaluated cosine similarity across job descriptions from distinct companies. In low-dimensional projection (64-d), standard tech boilerplate language ("agile environment", "unit testing", "collaborative teams") naturally clusters together, showing elevated similarity across listings.
- **Syntactic Vagueness**: Engineered a composite vagueness index (mean: 0.504) measuring concrete technical skill density (mean: 1.99 entities / 100 words) vs. buzzword density.

<br/>

## 4️⃣ Multi-Tool Listing Verification Agent

- Rather than relying solely on a probability score, we built an automated inspection agent equipped with 4 deterministic analytical tools (`ml_scorer_tool`, `semantic_duplicate_tool`, `company_history_tool`, `salary_benchmark_tool`).
- The agent gathers multi-source evidence and outputs a structured JSON report with specific bullet points (e.g. compensation disclosure status, posting age category, and company posting history), giving candidates clear context.

<br/>

---

## 🏁 Business Value & Candidate Impact

Naukri Saaf provides practical transparency for job seekers:
1. **Time Saved**: Candidates can triage listings in seconds rather than spending 45 minutes applying to abandoned postings.
2. **Transparent Evidence**: Every score is accompanied by local TreeSHAP drivers and multi-tool audit notes.
3. **Data Privacy**: Resume parsing and keyword matching execute **100% locally in browser memory** via PDF.js with zero network transmission.
