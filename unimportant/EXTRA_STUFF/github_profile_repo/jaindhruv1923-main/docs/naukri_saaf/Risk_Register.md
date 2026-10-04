<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Risk%20Register&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

Risk score = Likelihood (1–5) × Impact (1–5). Scored honestly, including risks the project explicitly chose to accept rather than solve.

<br/>

| ID | Risk | Likelihood | Impact | Score | Mitigation | Status |
|---|---|:---:|:---:|:---:|---|---|
| `R-01` | Weak-supervision labels encode bias — the model learns the label-design's assumptions, not verified truth | 4 | 4 | 16 | Documented explicitly in the BRD and README as a limitation; AUC reported as "above chance," never as certainty | 🟡 Accepted & disclosed |
| `R-02` | Portal page markup changes, breaking content-script selectors | 4 | 3 | 12 | Generic largest-text-block fallback ships alongside every site-specific selector set | 🟢 Mitigated |
| `R-03` | Extension's heuristic score diverges meaningfully from the trained GBM model's actual output | 3 | 4 | 12 | README explicitly states the extension is "not your trained GBM model running in the browser" and frames the score as a triage flag | 🟡 Accepted & disclosed |
| `R-04` | False positives — a genuine listing flagged as high-risk, discouraging a candidate from a real opportunity | 3 | 4 | 12 | Manual-check signals are excluded from the score rather than defaulted to "bad"; verdict includes "Insufficient data" state when coverage is low | 🟢 Mitigated |
| `R-05` | Resume text sensitivity — candidates may be wary of pasting personal data into a browser extension | 2 | 4 | 8 | Zero network calls by design; explicit on-screen copy stating data never leaves the browser; verifiable via `manifest.json` permissions | 🟢 Mitigated |
| `R-06` | Temporal data leakage in model evaluation (training on future data) | 2 | 4 | 8 | Temporal cross-validation used instead of random split (`temporal_cv_results_v3.csv`) | 🟢 Mitigated |
| `R-07` | Model AUC (0.716) is only moderately above chance — risk of over-trusting the score | 3 | 3 | 9 | Explicitly communicated as "fast triage flag, not a 0.72-AUC-grade decision" in both the extension README and dashboard framing | 🟢 Mitigated |
| `R-08` | Skill dictionary in `nlp.js` becomes stale as job-market vocabulary shifts | 3 | 2 | 6 | Documented as an easy extension point ("Expand SKILL_DICTIONARY as target roles change") | 🟡 Accepted, low priority |
| `R-09` | Employer clustering groups are sensitive to re-clustering — labels ("High-Risk Ghost Poster") could shift on retraining | 2 | 2 | 4 | Cluster profiles versioned alongside the model (`cluster_profiles_v3.csv` tied to `v3` model artifacts) | 🟢 Mitigated |
| `R-10` | India-specific logic (LPA salary format, Tier-1 city list) limits portability to other job markets | 5 | 2 | 10 | Explicitly out of scope in the BRD; documented as a known constraint, not a hidden gap | 🟡 Accepted, out of scope |

<br/>

## Risk Heat Map

```mermaid
quadrantChart
    title Risk Likelihood vs Impact
    x-axis Low Impact --> High Impact
    y-axis Low Likelihood --> High Likelihood
    quadrant-1 Critical — Act First
    quadrant-2 Monitor Closely
    quadrant-3 Low Priority
    quadrant-4 Contain Impact
    Label bias (R-01): [0.8, 0.8]
    Selector breakage (R-02): [0.6, 0.8]
    Heuristic drift (R-03): [0.8, 0.6]
    False positives (R-04): [0.8, 0.6]
    Resume data sensitivity (R-05): [0.8, 0.4]
    Temporal leakage (R-06): [0.8, 0.4]
    Moderate AUC (R-07): [0.6, 0.6]
    Skill dict staleness (R-08): [0.4, 0.6]
    Cluster drift (R-09): [0.4, 0.4]
    India-only scope (R-10): [0.4, 1.0]
```

<br/>

## Legend

| Status | Meaning |
|---|---|
| 🟢 Mitigated | An active engineering or design control reduces this risk |
| 🟡 Accepted & disclosed | Risk remains, but is explicitly documented so stakeholders aren't misled |
| 🔴 Open | Not yet addressed *(none currently — all identified risks have at least a disclosure-level mitigation)* |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
