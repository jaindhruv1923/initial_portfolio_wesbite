<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Risk%20Register&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf%20v4%20Production&descAlignY=78&descSize=15)

</div>

Risk score = Likelihood (1–5) × Impact (1–5). Scored with audit rigor, documenting active mitigations and architectural controls implemented in v4.

<br/>

| ID | Risk | Likelihood | Impact | Score | Mitigation Architecture (v4) | Status |
|---|---|:---:|:---:|:---:|---|---|
| `R-01` | Weak-supervision circular bias (model learns LF heuristics rather than true market signals) | 2 | 4 | 8 | Established a **180-sample silver heuristic proxy holdout** and generated an independent **80-sample blind human audit sheet** (`LABELING_RUBRIC.md`). Replaced naive single-rule labels with a **Snorkel Generative LabelModel** learning unsupervised label accuracies ($\kappa=0.5890$). Holdout metrics are benchmarked against the silver proxy pending complete human annotation. | 🟢 Mitigated |
| `R-02` | Job portal DOM schema drift breaking client scraper selectors | 3 | 3 | 9 | Implemented layered DOM selector fallbacks in `content.js` with automated fallback to parent semantic container extraction. FastAPI validation catches incomplete payload schemas. | 🟢 Mitigated |
| `R-03` | Chrome Extension scoring divergence from production ML model | 1 | 4 | 4 | Extension connects directly via HTTP to **FastAPI backend (`POST /api/v1/score`)** running the actual calibrated model and SHAP explainer in <15ms. `legitimacy.js` serves purely as an offline fallback when network is unavailable. | 🟢 Mitigated |
| `R-04` | False positives discouraging applicants from genuine opportunities | 2 | 4 | 8 | **Platt calibration** minimizes probability overconfidence (Brier Score = 0.0167, ECE = 0.0220). Borderline listings ($0.40 \le P < 0.70$) route to the **Multi-Tool Verification Agent** for secondary multi-signal adjudication before surfacing warnings. | 🟢 Mitigated |
| `R-05` | Candidate PII & resume data leakage over network | 1 | 5 | 5 | Zero-Knowledge architecture: PDF parsing (`pdf.js`) and TF-IDF matching occur **100% client-side** inside Chrome's sandboxed `storage.local`. No resume payload is ever sent over the wire. | 🟢 Mitigated |
| `R-06` | Cross-fold entity data leakage during model training | 1 | 5 | 5 | Fit all target encodings and employer aggregations strictly inside training folds via `LeakageFreeFeatureExtractor`. Employed **5-Fold GroupKFold strictly partitioned by Employer**. Automated pytest gate halts CI on any entity overlap. | 🟢 Mitigated |
| `R-07` | Model metric degradation / concept drift over time | 2 | 3 | 6 | Established **Population Stability Index (PSI)** monitoring (`src/monitoring/drift_detector.py`) and CI metric regression gates failing any build if holdout ROC-AUC drops below 0.9000. | 🟢 Mitigated |
| `R-08` | Stale domain skill ontology for emerging tech roles | 2 | 2 | 4 | Decoupled skill dictionary in `data/` from code; augmented with 64-d Dense Semantic LSA vector similarity capturing fuzzy semantic equivalence without rigid dictionary constraints. | 🟢 Mitigated |
| `R-09` | Cross-sectional age misinterpretation in job postings | 2 | 3 | 6 | Replaced unverified survival claims with **cross-sectional listing-age distributions** (`src/analytics/listing_age_analysis.py`), computing empirical percentiles without artificial event assumptions. | 🟢 Mitigated |
| `R-10` | Regional market specialization (India tech ecosystem focus) | 4 | 2 | 8 | Explicitly bounded scope to Indian tech hubs (Bengaluru, Hyderabad, Pune, NCR). Normalization handles LPA compensation structures and Tier-1 city hierarchies. Out-of-market portability documented for future work. | 🟡 Accepted & scoped |

<br/>

## Risk Heat Map

```mermaid
quadrantChart
    title Risk Likelihood vs Impact (Post-v4 Mitigations)
    x-axis Low Impact --> High Impact
    y-axis Low Likelihood --> High Likelihood
    quadrant-1 Critical — Act First
    quadrant-2 Monitor Closely
    quadrant-3 Low Priority
    quadrant-4 Contain Impact
    India-only scope (R-10): [0.4, 0.8]
    Selector breakage (R-02): [0.6, 0.6]
    Metric drift (R-07): [0.6, 0.4]
    Skill dict staleness (R-08): [0.4, 0.4]
    Age misinterpretation (R-09): [0.6, 0.4]
    Weak supervision bias (R-01): [0.8, 0.4]
    False positives (R-04): [0.8, 0.4]
    Resume sensitivity (R-05): [1.0, 0.2]
    Extension divergence (R-03): [0.8, 0.2]
    Entity leakage (R-06): [1.0, 0.2]
```

<br/>

## Legend

| Status | Meaning |
|---|---|
| 🟢 Mitigated | An active algorithmic, architectural, or automated CI control neutralizes this risk |
| 🟡 Accepted & scoped | Risk is bounded by architectural scope and explicitly documented |
| 🔴 Open | Critical unaddressed vulnerability *(0 open risks across v4 codebase)* |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README_BA_package.md">← Back to BA Package Index</a></i></div>
