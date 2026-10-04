<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Gap%20Analysis&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

## 1. Capability Gap Table

| Capability | Current state (As-Is) | Desired state (To-Be) | Gap | How Naukri Saaf closes it |
|---|---|---|---|---|
| Cross-portal legitimacy check | None — each portal judged in isolation, if at all | One consistent risk score regardless of source portal | No unified signal set existed | Content-script scraping normalized into one job-data schema across 4 portals; same `legitimacy.js` scorer runs on all of them |
| Ghost-listing ground truth | Doesn't exist publicly | A usable proxy label to train against | No labeled data to learn from | Weak-supervision labeling scheme built from observable posting-behavior signals (age, reposting, salary disclosure) |
| Employer-level risk visibility | Invisible — only individual listings are seen | Employers should be evaluated on their pattern, not one posting | No aggregation layer existed | K-Means-style clustering into 6 employer behavior profiles, surfaced in the dashboard's Cluster tab |
| Real-time, in-context checking | Would require leaving the job page to check elsewhere | Score available on the exact page, at the exact moment of deciding to apply | No in-browser tool existed | Chrome extension side panel, reads the active tab, scores instantly, no navigation away |
| Trust in an automated score | A single black-box number invites distrust | Score should be explainable and honest about its blind spots | No explainability or limitation-disclosure layer existed | SHAP per-listing explainability (dashboard) + "checked on this page" vs "needs manual check" split (extension) |
| Resume-fit judgment | Manual, subjective, redone per listing | Fast, consistent, listing-specific fit signal | No automated matching existed | Local TF-based cosine similarity + skill dictionary, 0–10 score with concrete next steps |
| Data privacy | N/A (no tool existed) | Resume and browsing data must never leave the user's device | — | Zero network calls by design; `chrome.storage.local` only |

<br/>

## 2. Root Cause View

For each gap, the underlying *why* — the kind of analysis a BA does before jumping to "build a feature":

| Gap | Root cause |
|---|---|
| No cross-portal check | Job portals are walled gardens; no portal has an incentive to flag its own low-quality listings |
| No ground truth for ghost labels | "Ghost job" is a behavioral pattern (how it's posted, reposted, aged), not a field any portal captures or discloses |
| No employer-level visibility | Portals present listings, not employers, as the unit of browsing — the aggregation simply isn't offered to the end user |
| No real-time in-context tool | Most legitimacy-checking advice online is generic ("look for red flags") rather than an actual computed tool |
| Distrust in automated scores | Most scoring tools present a single number with no reasoning — this is a UX/trust gap as much as a technical one |

<br/>

## 3. Gap Closure Priority

Ranked by (a) how large the gap was and (b) how directly the closure serves the primary stakeholder (the job seeker):

| Priority | Gap closed | Why it ranked here |
|:---:|---|---|
| 1 | Real-time, in-context checking | Directly changes candidate behavior at the moment of decision — the highest-leverage point |
| 2 | Trust in the score (explainability + honesty about limits) | Without this, priority 1 is not credible enough to actually change behavior |
| 3 | Employer-level risk visibility | Second-order but high-value — catches patterns a single listing can't reveal |
| 4 | Cross-portal consistency | Necessary infrastructure, but invisible to the end user if done well |
| 5 | Resume-fit scoring | High daily utility, but a secondary problem to the core ghost-detection mission |

<br/>

## 4. Residual Gaps (not closed by this build)

Documented honestly, the way a BA would flag known limitations rather than hide them:

- **No live cross-platform duplicate detection** — the extension cannot check whether the exact listing is also posted elsewhere; flagged manual-check
- **No live application-velocity or portal-baseline data** — these require live web/API access, which conflicts with the "100% local, no network calls" design principle
- **No verified ground truth** — the model's AUC of 0.716 is measured against weak-supervision labels, not confirmed real-world outcomes
- **No non-English or non-Indian job market coverage** — city-tier and salary-format logic (LPA, ₹) is India-specific

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
