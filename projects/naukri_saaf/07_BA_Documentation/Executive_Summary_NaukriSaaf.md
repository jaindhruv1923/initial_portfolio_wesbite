<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Executive%20Summary&fontSize=34&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Naukri%20Saaf%20%C2%B7%20125%2C457%20scraped%20%C2%B7%202%2C852%20modeled&descAlignY=68&descSize=14)

</div>

## 🔮 Headline finding

**Employer posting behavior predicts ghost listings better than any single listing's content.** The two heaviest-weighted features are `days_live` and `listing_age_bucket` — how long a listing stays posted — not what the description says.

<br/>

<div align="center">

| 125,457 | 0.716 | 1,361 | 26 |
|:---:|:---:|:---:|:---:|
| Raw Listings Scraped | Best Model AUC (GBM) | High-Risk Poster Employers | Signals in the Model |

</div>

<br/>

---

## 1️⃣ What makes a listing look like a ghost

- `days_live` (9.8%) and `listing_age_bucket` (9.7%) are the top two features by model weight
- `velocity_x_no_salary` (7.7%) and `employer_repost_count` (6.9%) round out the top four
- Content-level signals (description length, lexical diversity, keyword stuffing) matter, but weigh less collectively than employer-behavior signals

> **✅ Recommendation:** future detection work should prioritize employer-level behavioral history over deeper NLP on individual listings — the ceiling on content-only signals looks lower.

<br/>

## 2️⃣ Not all employers post the same way

- Behavioral clustering split employers into **6 distinct profiles**
- Largest, most concerning: **"High-Risk Ghost Poster"** — 1,361 employers, 32.8% ghost rate, avg. listing age 23.3 days
- A smaller **"Mid-tier Mixed Signals"** cluster (48 employers) reposts far more aggressively (avg. 12.6 reposts) but discloses salary more often — a genuinely different risk shape

> **🟨 Recommendation:** trust signals should be employer-level, not just listing-level — five near-identical postings from one company is itself a signal worth surfacing.

<br/>

## 3️⃣ The model is honest about its own limits

- Best model (GBM) reaches **AUC 0.716, F1 0.527** — real, above-chance signal, not framed as certainty
- **10 of 26 signals** (repost count, application velocity, cross-platform duplicates, portal baseline, market salary gap) can't be computed from a static page — flagged "needs manual check" with search links instead of guessed
- SHAP explainability computed per listing — any flag traces back to specific driving features

> **🟪 Recommendation:** ship the manual-check gap as a first-class product feature, not a footnote — a tool honest about ~38% of its own signal weight builds more trust than a black-box score.

<br/>

---

## 🏁 Bottom line

Naukri Saaf turns 125,457 raw scraped listings into a model with real, above-chance signal (AUC 0.716) — and ships that model's logic into a free, private, real-time Chrome extension usable on the exact listing a candidate is about to apply to.

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
