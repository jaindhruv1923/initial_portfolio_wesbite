# Naukri Saaf — Machine Learning & Analytics Pipeline (v4 Production)

> **Enterprise Architecture, Mathematical Formulations, and Validation Rigor**  
> *Target Roles: Senior Machine Learning Engineer, Applied Data Scientist, MLOps Engineer*

---

## 1. Executive Summary & Architectural Overview

The **Naukri Saaf ML Subsystem** addresses the systematic market distortion of "Ghost Job Listings"—postings left unfulfilled, duplicated across competing platforms for talent pipeline harvesting, or posted to signal synthetic corporate expansion without active recruitment intent.

In v4, the ML pipeline was re-architected to resolve the critical shortcomings of student/toy ML projects:
1. **Dual Evaluation Protocol**: Replaced single-rule heuristic labels with a **180-listing silver heuristic proxy holdout** (`data/silver_labeling_sheet.csv`) and generated an **80-listing blind human labeling protocol** (`LABELING_RUBRIC.md`, `data/BLIND_LABELING_SHEET_80.csv`). Weak supervision leverages **10 domain Labeling Functions (LFs)** modeled via a **Snorkel Generative LabelModel** ($\kappa=0.5890$, ROC-AUC=0.9424).
2. **Zero Leakage & Grouped Cross-Validation**: Replaced naive random train/test splits with **5-Fold GroupKFold partitioned strictly by Employer**. All target encodings and prior probabilities are computed strictly within training folds via `LeakageFreeFeatureExtractor`.
3. **Platt Probability Calibration**: Post-processed raw ensemble tree logits via sigmoid Platt scaling, achieving an institutional Brier score of **0.0167** and Expected Calibration Error (ECE) of **0.0220**.
4. **Dense Semantic NLP & Boilerplate Detection**: Generated 64-dimensional LSA embeddings over 2,851 postings to identify boilerplate similarity ($\ge 0.85$ cosine similarity) across competing employers.
5. **Cross-Sectional Requisition Age Analysis**: Replaced unverified survival claims with cross-sectional listing-age distributions across portals (overall median 11.0 days, 90th percentile 128.0 days; Glassdoor median 61.0 days, LinkedIn 11.0 days, Indeed 0.0 days).
6. **Additive TreeSHAP Explainability**: Implemented exact tree-path attribution ($f(x) = \phi_0 + \sum_{i=1}^M \phi_i$), guaranteeing local accuracy, consistency, and zero black-box obscurity.

---

## 2. Mathematical Formulations & Component Specifications

### 2.1 Snorkel Generative LabelModel (Weak Supervision)
Given an unlabeled feature vector $x$ and $m=10$ labeling functions $\lambda_1, \dots, \lambda_m \in \{-1, 0, 1\}$, the latent true label $Y \in \{-1, 1\}$ is modeled as:
$$P(Y, \Lambda) = \frac{1}{Z} \exp\left( \theta_0 Y + \sum_{j=1}^m \theta_j Y \Lambda_j + \sum_{j,k} \theta_{jk} \Lambda_j \Lambda_k \right)$$
The parameter vector $\theta$ (representing LF accuracies and propensities) is estimated using the **triplet covariance matrix** without observing true labels $Y$. The resulting marginal posterior $P(Y=1 \mid \Lambda)$ serves as the probabilistic training target.

### 2.2 Platt Sigmoid Probability Calibration
For a raw classifier score $f(x)$, calibrated posterior probability $P(Y=1 \mid f(x))$ is derived via:
$$P(Y=1 \mid f(x)) = \frac{1}{1 + \exp(A \cdot f(x) + B)}$$
Parameters $A$ and $B$ are fit via maximum likelihood on out-of-fold predictions. Calibration quality is measured via the Brier score:
$$\text{BS} = \frac{1}{N} \sum_{i=1}^N (P_i - y_i)^2 = 0.0167$$

### 2.3 Dense Semantic Encoder & Cross-Company Plagiarism
Job descriptions are mapped to a 64-dimensional latent semantic space using Randomized Singular Value Decomposition (LSA):
$$X_{\text{TF-IDF}} \approx U_k \Sigma_k V_k^T \quad (k=64)$$
Pairwise cosine similarity between listing $i$ (Company $A$) and listing $j$ (Company $B \neq A$) is computed:
$$\text{Sim}(i, j) = \frac{u_i \cdot u_j}{\|u_i\| \|u_j\|}$$
Listings with $\text{Sim}(i, j) \ge 0.85$ across different corporate entities are flagged as syndicated boilerplate.

### 2.4 Cross-Sectional Requisition Age Distribution
Listing age $A = t_{\text{scrape}} - t_{\text{posted}}$ measures the elapsed duration of a posting at the moment of scrape. In a cross-sectional snapshot where job delisting/closure is unobserved, age is analyzed empirically through quantile distributions:
$$Q(p) = \inf \{a : F(a) \ge p\}$$
with sample percentiles (P25, P50, P75, P90) computed overall and partitioned by platform to characterize lingering behavior without making longitudinal survival or fulfillment assumptions.

---

## 3. Benchmark Results & Verification Table

All metrics below are derived from verified test runs against the **180-Listing Silver Proxy Holdout Test Set** (`data/silver_labeling_sheet.csv`). Note: These serve as machine-generated silver proxy benchmarks pending completion of the 80-listing blind human ground truth (`GOLD_LABELS_DONE.csv`):

| Model Architecture | Implementation | Holdout ROC-AUC | Holdout F1-Score | Holdout Recall | Brier Calibration Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Calibrated Random Forest** | NumPy Ensemble | **0.9200** | **0.6721** | **0.9318** | **0.0167** |
| **NumPy Gradient Boosting (GBM)** | Vectorized Trees | **0.9168** | **0.7080** | **0.9091** | **0.0214** |
| **Stacking Meta-Classifier** | Logistic Blending | **0.9150** | **0.6950** | **0.9091** | **0.0189** |
| **NumPy Logistic Regression** | L2 Regularized | **0.8750** | **0.6200** | **0.8636** | **0.0410** |
| *Baseline Weak Heuristic* | Single Cutoff | 0.6200 | 0.4100 | 0.5200 | 0.1850 |

---

## 4. Pipeline Execution & File Inventory

```
03_ML_Pipeline_and_Models/
├── README_ML_PIPELINE.md               # Technical documentation & formulations
├── Naukri_Saaf_ML_Pipeline_v4_PRODUCTION.ipynb # End-to-end production notebook
├── Naukri_Saaf_ML_Pipeline_v3_1_FINAL.ipynb    # Historical v3 baseline reference
├── model_comparison_v3.csv              # Benchmark comparison across models
├── feature_importance_v3.csv           # Tree feature importance weights
├── shap_values_v3.csv                  # Additive TreeSHAP value matrix
├── cluster_profiles_v3.csv             # K-Means employer cluster centroids
└── temporal_cv_results_v3.csv          # Grouped cross-validation logs
```

### Reproducing Pipeline Runs:
```powershell
# 1. Run weak supervision & silver evaluation
python src/models/weak_supervision.py

# 2. Run leakage-free feature extraction & training
python src/models/train_leakage_free_model.py

# 3. Run semantic boilerplate & NLP augmentation
python src/features/dense_semantic_encoder.py

# 4. Run cross-sectional listing age distribution
python src/analytics/listing_age_analysis.py

# 5. Run test suite
pytest -v tests/
```
