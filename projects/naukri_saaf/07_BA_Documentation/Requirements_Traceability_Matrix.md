<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Requirements%20Traceability%20Matrix&fontSize=24&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

Traces every BRD requirement through to its design artifact, build component, and verification method — proof that nothing was scoped and then forgotten, and that every shipped feature has a documented reason to exist.

<br/>

| Req ID | Requirement | Design artifact | Build component | Verified by |
|---|---|---|---|---|
| `BR-01` | Unify listings from multiple portals | Functional Spec FR-01 | `naukri_saaf_sql_workbench.sql` (staging + cleaning) | UAT-01 |
| `BR-02` | Ghost label without ground truth | Functional Spec FR-02 | Weak-supervision labeling logic in `Naukri_Saaf_ML_Pipeline_v3_1_FINAL.ipynb` | UAT-02 |
| `BR-03` | Predict ghost-listing probability | Functional Spec FR-03 | `gbm_model_v3.pkl` + `model_comparison_v3.csv` | UAT-03 |
| `BR-04` | Explain why a listing is flagged | Functional Spec FR-04 | `shap_values_v3.csv` | UAT-04 |
| `BR-05` | Segment employers by behavior | Functional Spec FR-04 | `cluster_profiles_v3.csv` | UAT-05 |
| `BR-06` | Analyst dashboard, no code required | Functional Spec FR-05 | `app.py` (7 tabs) | UAT-06 |
| `BR-07` | Real-time check on a live listing | Functional Spec FR-06, FR-07 | `content.js`, `legitimacy.js` | UAT-07 |
| `BR-08` | Resume-fit scoring | Functional Spec FR-08 | `nlp.js`, `sidepanel.js` | UAT-08 |
| `BR-09` | Honest disclosure of unverifiable signals | Functional Spec FR-07 | `legitimacy.js` manual-check split | UAT-09 |
| `BR-10` | Preserve user privacy | Functional Spec FR-08 | `chrome.storage.local`, zero network calls (verified via `manifest.json` permissions) | UAT-10 |

<br/>

## Coverage check

| Check | Result |
|---|:---:|
| Every BRD requirement has at least one design artifact | ✅ |
| Every BRD requirement has at least one build component | ✅ |
| Every BRD requirement has at least one UAT test case | ✅ (see `UAT_Test_Cases.md`) |
| Every build component traces back to a requirement (no orphan features) | ✅ |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
