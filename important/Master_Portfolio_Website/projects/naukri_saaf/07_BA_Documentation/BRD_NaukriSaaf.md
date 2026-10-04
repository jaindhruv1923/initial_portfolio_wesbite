<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Business%20Requirements%20Document&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Naukri%20Saaf%20%C2%B7%20Ghost%20Job%20Listing%20Detection%20Platform&descAlignY=68&descSize=15)

![Status](https://img.shields.io/badge/status-complete-1F7A54?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0-4C1D95?style=flat-square)
![Author](https://img.shields.io/badge/author-Dhruv_Jain-B8860B?style=flat-square)

</div>

> **Note:** written retrospectively against a completed build, in BRD structure/language, as it would have been scoped at kickoff. Requirements derived from job-seeker and placement-cell needs, not live client interviews.

<br/>

## 1. Purpose

Defines the business problem, requirements, and success criteria for **Naukri Saaf** — built on **125,457 raw listings** scraped from LinkedIn, Indeed, and Glassdoor, cleaned/deduplicated to **2,852 unique listings**, labeled under a weak-supervision scheme (no ground-truth ghost/real labels exist).

<br/>

## 2. Business Problem

| Problem | Impact if unaddressed |
|---|---|
| No way to tell a genuine listing from a ghost one before applying | Candidates lose hours tailoring applications for roles that were never real |
| Ghost-listing signals are scattered and platform-specific | No portable legitimacy check across LinkedIn, Naukri, Indeed, Glassdoor |
| Job tools optimize for volume, not listing quality | No trust signal for candidates; no friction for low-quality employers |

<br/>

## 3. Stakeholders

| Stakeholder | Interest |
|---|---|
| 🧑‍💻 Job seeker / candidate | Fast, trustworthy signal before investing application time |
| 🎓 University career services | A way to vet postings before circulating to students |
| 📊 Analytics recruiter (evaluating this project) | Evidence of the full lifecycle — scrape → clean → model → explain → ship |
| 🛠️ Future maintainer | Documented signal set so the system can be extended/retrained |

<br/>

## 4. Scope

<table>
<tr><td width="50%" valign="top">

### ✅ In scope
- Scraping 125,457 listings across 3 portals (Apify)
- 32-query SQL analytical layer (8 categories)
- Weak-supervision ghost-probability labeling
- 5-model benchmark + SHAP explainability + employer clustering
- 7-tab Streamlit dashboard
- Chrome extension (real-time, local, no API)

</td><td width="50%" valign="top">

### ❌ Out of scope
- Running the trained `.pkl` model inside the browser (needs ONNX/TF.js)
- Any backend/API calls from the extension — 100% local by design
- Manual employer outreach for verification

</td></tr>
</table>

<br/>

## 5. Business Requirements

| ID | Requirement | Delivered as |
|---|---|---|
| `BR-01` | Unify listings from multiple portals | SQL staging + cleaning pipeline (Glassdoor, Indeed, LinkedIn) |
| `BR-02` | Produce a ghost label with no ground truth | Weak-supervision scheme from posting-behavior signals |
| `BR-03` | Predict ghost-listing probability | 5 classifiers benchmarked; **GBM — AUC 0.716, F1 0.527** |
| `BR-04` | Explain *why* a listing is flagged | Per-listing, per-feature SHAP values |
| `BR-05` | Segment employers by behavior | 6 clusters — e.g. "High-Risk Ghost Poster": 1,361 employers, 32.8% ghost rate |
| `BR-06` | Analyst-facing exploration, no code | 7-tab Streamlit dashboard |
| `BR-07` | Real-time check on a live listing | Chrome extension side panel, zero network calls |
| `BR-08` | Resume-fit scoring per listing | 0–10 fit score, local keyword + cosine similarity |
| `BR-09` | Be honest about unverifiable signals | Legitimacy tab splits "checked" vs "manual check", with search links |
| `BR-10` | Preserve user privacy | All data in `chrome.storage.local`, never transmitted |

<br/>

## 6. Non-Functional Requirements

| Requirement | Definition of done |
|---|---|
| **Privacy** | Zero network/API calls; all scoring client-side |
| **Portability** | Works across 4 portals via selectors + generic fallback |
| **Resilience** | Layout change on a portal still returns a usable description via fallback |
| **Transparency** | Every signal shown carries its real model weight from `feature_importance_v3.csv` |

<br/>

## 7. Assumptions & Constraints

- No public ground-truth ghost-job labels exist; weak-supervision is a documented judgment call
- The Chrome extension is a rule-based scorecard weighted by real feature importances — **not** the trained GBM running client-side; explicitly framed as a triage flag, not a 0.72-AUC-grade decision
- ~10 of 26 signals can't be computed from a static page and are flagged manual-check, not guessed
- No live stakeholder interviews conducted (solo academic build)

<br/>

## 8. Success Metrics

| Metric | Target | Status |
|---|:---:|---|
| Model meaningfully better than chance | AUC > 0.65 | ✅ GBM AUC 0.716 |
| Per-listing explainability | Yes | ✅ SHAP for all 2,852 listings |
| Usable, private, real-time end-user tool | Yes | ✅ Chrome extension live on 4 portals |
| Honest disclosure of unverifiable signals | Yes | ✅ 10/26 flagged manual-check |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
