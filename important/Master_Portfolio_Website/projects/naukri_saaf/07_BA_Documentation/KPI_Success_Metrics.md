<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=KPI%20%26%20Success%20Metrics&fontSize=28&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

Two tiers, the way a BA separates them: **build-time metrics** (did we deliver what we scoped) and **post-launch operational metrics** (is it actually working for users) — including honest notes on which of the latter this solo/local-only build *can't* measure yet, and why.

<br/>

## 1. Build-Time Metrics (measured, available today)

| Metric | Target | Actual | Status |
|---|:---:|:---:|:---:|
| Model AUC | > 0.65 | **0.716** | ✅ |
| Model F1 score | > 0.45 | **0.527** | ✅ |
| Signals with real model-weight backing (not arbitrary) | 100% | **100%** (26/26 sourced from `feature_importance_v3.csv`) | ✅ |
| BRD requirements traced to build + test | 100% | **100%** (10/10, see RTM) | ✅ |
| Portals supported | ≥ 3 | **4** (LinkedIn, Naukri, Indeed, Glassdoor) | ✅ |
| Network calls made by the extension | 0 | **0** (by design) | ✅ |
| Dashboard tabs functional | 7 | **7** | ✅ |

<br/>

## 2. Post-Launch Operational Metrics (the ideal measurement plan)

*(Framed as what a BA would propose measuring once this ships to real users — honestly noting that a local-only, no-backend extension cannot currently collect these without adding telemetry, which would conflict with the zero-network-calls privacy principle.)*

| Metric | Why it matters | How it *would* be measured | Current measurability |
|---|---|---|---|
| % of "Likely ghost" verdicts that a user later confirms as accurate | Validates the score against real-world outcomes, not just weak-supervision labels | Optional, explicit in-extension feedback prompt ("Was this listing real?") | ❌ Not implemented — would need opt-in local feedback storage |
| Extension weekly active use | Adoption/retention signal | `chrome.storage.local` session counter (still fully local, no network) | ⚠️ Feasible without violating privacy principle — not yet built |
| Average resume-fit score improvement after a user edits their resume based on advice | Measures whether the tool's advice actually helps | Compare stored fit scores across resume-save events, locally | ⚠️ Feasible locally — not yet built |
| Coverage percentage distribution across real listings | Tells us how often users see a confident verdict vs. "Insufficient data" | Log locally, no transmission | ⚠️ Feasible locally — not yet built |
| Portal-specific extraction success rate | Flags when a portal's markup has changed and selectors need updating | Local success/failure counter per portal | ⚠️ Feasible locally — not yet built |

<br/>

## 3. Why the gap between "ideal" and "current" is itself worth documenting

A common BA mistake is to present only the metrics that are convenient to report. Here, the more useful post-launch metrics all require *some* form of local logging that doesn't exist yet — and the honest reason is that building it was deprioritized in favor of shipping the core detection + resume-match functionality first. This table exists so the next iteration has a ready-made backlog, not so the current state looks more measured than it is.

<br/>

## 4. Recommended Next-Iteration Priority

| Priority | Addition | Effort | Unlocks |
|:---:|---|:---:|---|
| 1 | Local-only feedback prompt ("Was this listing real?") | Low | Ground-truth validation of the score, still zero network calls |
| 2 | Local extraction-success counter per portal | Low | Early warning when a portal's selectors break |
| 3 | Local session/usage counter | Low | Basic adoption signal without any privacy trade-off |
| 4 | Optional opt-in anonymized aggregation (still no PII) | Medium | Portal-wide ghost-rate baselines, currently marked "manual check" |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
