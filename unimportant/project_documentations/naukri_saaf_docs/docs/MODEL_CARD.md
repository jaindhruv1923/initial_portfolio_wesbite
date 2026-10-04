# Model Card: Naukri Saaf Ghost Job Detection (v4 Production)

## 1. Model Details
- **Model Name**: Naukri Saaf Ghost Job Detector v4
- **Model Type**: Ensemble of Supervised Tree-based & Linear Classifiers (Gradient Boosting, Random Forest, Logistic Regression, Stacking)
- **Primary Architecture**: Platt-Calibrated `NumPyRandomForest` / `NumPyGradientBoosting` with exact `AuthenticTreeSHAP` explanation paths.
- **Framework**: High-performance vectorized Python / NumPy 2.5.3, designed for zero external binary DLL dependency and full deterministic reproducibility.
- **Serialization**: Saved in `outputs/models/best_model_v4.pkl`, with `calibrator_v4.pkl` and `feature_extractor_v4.pkl`.
- **Date**: October 2026
- **Status**: Production-Ready / Interview-Grade

---

## 2. Intended Use
- **Primary Use Case**: Classifying whether a job posting on major job portals (LinkedIn, Indeed, Glassdoor) is a "Ghost Job" (perpetually open, unmonitored, reposted for brand vanity or data harvesting, or lacking an active hiring requisition).
- **Users**: Job seekers, university career cells, data analysts, automated job aggregator platforms.
- **Out of Scope**: Automated rejection of genuine applicants or defamatory public blacklisting without multi-factor verification.

---

## 3. Training & Validation Setup

### 3.1 Data Splits & Partitioning
To guarantee zero contamination, the dataset was strictly split:
- **Total Clean Listings**: 2,851 listings scraped across LinkedIn, Indeed, and Glassdoor.
- **Holdout Gold Standard Test Set**: **180 listings** (60 Glassdoor, 60 Indeed, 60 LinkedIn) hand-annotated with domain forensic rules (`data/gold_labeling_sheet.csv`). Untouched during feature engineering and model training.
- **Training Set**: **2,671 listings** across 1,231 unique companies, pseudo-labeled using the Snorkel Generative Label Model.

### 3.2 Leakage Prevention Strategy
In previous student iterations, target-correlated aggregate features (`employer_repost_count`, `title_median_salary`) were computed globally on all rows before splitting, creating fatal lookahead leakage.
In v4, `LeakageFreeFeatureExtractor` strictly enforces:
1. Feature statistics (e.g., historical repost frequency, multi-portal presence, salary medians) are computed **strictly inside training folds**.
2. Any unseen company or job title in a validation/test fold receives a non-leaking global prior (defaulting to single-post baseline).
3. 5-Fold GroupKFold Cross-Validation is strictly grouped by `company_name`. **No company appearing in a validation fold exists in the training fold.**

---

## 4. Cross-Validation Performance (Unseen Employers)

5-Fold GroupKFold evaluated on 2,671 training listings (out-of-fold predictions):

| Rank | Model Architecture | Out-of-Fold ROC-AUC | F1 Score | Precision | Recall | Accuracy |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| **1** | **Random Forest (Tuned)** | **0.9961** | **0.9638** | 0.9421 | **0.9864** | **0.9775** |
| 2 | Stacking Ensemble | 0.9954 | 0.9630 | 0.9452 | 0.9815 | 0.9772 |
| 3 | Gradient Boosting (GBM) | 0.9949 | 0.9747 | 0.9741 | 0.9753 | 0.9846 |
| 4 | Logistic Regression (L2) | 0.9839 | 0.9254 | 0.8814 | 0.9740 | 0.9525 |

*Note*: These exceptionally high OOF metrics reflect learning the consensus patterns of the 10 domain labeling functions without memorizing specific employer IDs.

---

## 5. Probability Calibration (Platt Scaling)

Raw tree ensemble probabilities often exhibit overconfidence near 0 and 1. To provide trustworthy risk probabilities for end users, Platt Scaling (logistic sigmoid mapping on out-of-fold logits) was fitted on the best model:

| Metric | Raw Uncalibrated | Platt Calibrated | Relative Improvement |
|---|:---:|:---:|:---:|
| **Brier Score** (Mean Squared Prob Error) | 0.0188 | **0.0167** | **+11.18%** |
| **Expected Calibration Error (ECE)** | 0.0366 | **0.0220** | **+39.89%** |

The calibrated output enables safe risk bucketing:
- **Genuine** (0.00 – 0.49): Normal job listings with active hiring signals.
- **Suspect** (0.50 – 0.74): Elevated risk; caution advised (verify on employer careers page).
- **Ghost** (0.75 – 1.00): High likelihood of perpetual repost or unmonitored listing.

---

## 6. Holdout Gold Standard Benchmark (180 Hand-Verified Listings)

Evaluating the trained models on the pristine, untouched 180 Gold Standard listings provides the true test of real-world generalization:

| Model | ROC-AUC | F1 Score | Precision | Recall | Accuracy |
|---|:---:|:---:|:---:|:---:|:---:|
| **Gradient Boosting (GBM)** | 0.8665 | **0.7080** | 0.5797 | 0.9091 | **0.8167** |
| **Logistic Regression** | **0.9320** | 0.6992 | 0.5443 | **0.9773** | 0.7944 |
| **Random Forest (Calibrated)** | 0.9200 | 0.6949 | 0.5541 | 0.9318 | 0.8000 |
| Random Forest (Raw) | 0.9200 | 0.6777 | 0.5325 | 0.9318 | 0.7833 |
| *Baseline: Original Rule Heuristic* | *—* | *0.4536* | *0.4151* | *0.5000* | *0.7056* |

### Key Observations:
1. **Dramatic Generalization Boost**: All v4 models achieve an F1 of **0.69 – 0.71** and ROC-AUC of **0.87 – 0.93** on hand-verified listings, compared to the baseline rule's F1 of **0.4536** (+56% gain).
2. **High Ghost Recall**: The calibrated Random Forest captures **93.2%** of true ghost listings (41 / 44), while Logistic Regression captures **97.7%** (43 / 44).
3. **Platt Calibration Efficacy**: Probability calibration improved the Random Forest's Gold F1 from 0.6777 to 0.6949 by eliminating threshold overconfidence.

---

## 7. Explainability via Authentic TreeSHAP

Rather than relying on ungrounded heuristic weights, v4 implements an exact TreeSHAP decision path traversal algorithm. Global feature importance (mean absolute SHAP value across the entire corpus) demonstrates what truly drives ghost classification:

| Feature Name | Mean \|SHAP\| | % Global Importance | Directional Impact |
|---|:---:|:---:|---|
| `description_length_words` | 0.1621 | **31.39%** | Short/skeletal descriptions (<150 words) strongly push risk positive. |
| `description_lexical_diversity` | 0.1480 | **28.65%** | Low lexical diversity (repetitive boilerplate/buzzwords) increases ghost probability. |
| `listing_age_bucket` | 0.0550 | **10.66%** | Listings in >90d or >60d age brackets sharply elevate ghost risk. |
| `company_data_completeness_score` | 0.0545 | **10.55%** | Missing company metadata (no industry, no rating, no logo) signals low-intent posting. |
| `desc_per_day` | 0.0299 | **5.80%** | Ratio of description length to days live reveals stale copy decay. |
| `days_live` | 0.0150 | **2.91%** | Raw lifespan confirms persistence. |
| `portal_ghost_baseline` | 0.0140 | **2.71%** | Glassdoor baseline carries slightly higher empirical risk than LinkedIn. |
| `salary_range_ratio` | 0.0114 | **2.21%** | Extremely wide or absurd salary ranges indicate placeholder or phishing listings. |
| `salary_disclosed_num` | 0.0094 | **1.81%** | Absence of compensation disclosure correlates with low commitment. |
| `posting_velocity_per_week` | 0.0066 | **1.27%** | Extreme posting volume by single employer triggers repost flags. |

---

## 8. Dataset Predictions Summary
Across the full dataset of 2,851 postings evaluated with calibrated probabilities:
- **Genuine**: 1,711 listings (**60.0%**)
- **Suspect**: 712 listings (**25.0%**)
- **Ghost**: 428 listings (**15.0%**)

Exported to `data/predictions_v4.csv` with per-listing calibrated probabilities, status tiers, and top TreeSHAP driver.
