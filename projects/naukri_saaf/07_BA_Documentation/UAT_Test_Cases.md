<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=UAT%20Test%20Cases&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

User Acceptance Test cases mapped 1:1 to the Requirements Traceability Matrix — each test case exists specifically to sign off one BRD requirement.

<br/>

| Test ID | Traces to | Scenario | Steps | Expected result | Pass criteria |
|---|---|---|---|---|---|
| `UAT-01` | BR-01 | Verify unified schema across portals | Run staging → cleaning SQL scripts against a fresh raw export | Cleaned table contains listings from all 3 portals with consistent typed columns | Zero NULL values in required fields (title, company, source) after cleaning |
| `UAT-02` | BR-02 | Verify weak-supervision label is deterministic | Run the labeling logic twice on the same input data | Identical `ghost_label` output both runs | 100% label consistency on repeat runs |
| `UAT-03` | BR-03 | Verify model beats a random baseline | Compare GBM AUC against a random-guess baseline (AUC 0.5) | GBM AUC 0.716 | AUC > 0.65 on held-out temporal fold |
| `UAT-04` | BR-04 | Verify SHAP explains a specific flagged listing | Select a high-risk listing, inspect its SHAP values | `days_live` and/or `listing_age_bucket` appear among top contributing features for a stale listing | Top SHAP feature is directionally consistent with the listing's actual attributes |
| `UAT-05` | BR-05 | Verify employer clustering groups make behavioral sense | Inspect "High-Risk Ghost Poster" cluster members | Cluster members show elevated ghost rate and repost count vs. dataset average | Cluster ghost rate ≥ 1.5× the dataset-wide average |
| `UAT-06` | BR-06 | Verify dashboard renders all 7 tabs without error | Launch `app.py`, click through every tab | Every tab loads and displays charts/tables sourced from the model artifacts | Zero unhandled exceptions across all 7 tabs |
| `UAT-07` | BR-07 | Verify real-time reading on a live listing | Open a real job posting on each of the 4 supported portals, click ↻ | Overview tab populates with title, company, and skills within 2 seconds | Successful extraction on at least 3 of 4 portals without needing the generic fallback |
| `UAT-08` | BR-08 | Verify resume-fit scoring reacts to resume content | Save two different resumes against the same listing | Fit scores differ meaningfully based on skill overlap | Score delta ≥ 2 points between a strong-match and weak-match resume |
| `UAT-09` | BR-09 | Verify manual-check signals are never silently scored | Inspect the Legitimacy tab's risk-score calculation for a listing missing salary/date data | Missing signals appear under "Needs a manual check", excluded from the score itself | Risk score formula excludes any signal with `status: manual` |
| `UAT-10` | BR-10 | Verify zero network calls from the extension | Open Chrome DevTools → Network tab, use the extension fully (read job, save resume, view legitimacy) | No outbound requests appear in the Network tab | 0 network requests logged during a full extension session |

<br/>

## Sign-off Criteria

A build is considered **accepted** for release when:

- [ ] All 10 UAT test cases pass
- [ ] No `R-01`–`R-10` risk has moved from its documented status to 🔴 Open
- [ ] README limitations section accurately reflects current behavior (re-verified against the live build, not just written once)
- [ ] Extension manifest permissions match actual runtime network behavior (UAT-10 re-confirmed after any code change touching `background.js`, `content.js`, or `sidepanel.js`)

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
