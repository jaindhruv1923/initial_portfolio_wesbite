<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=Data%20Dictionary&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

Field-level definitions for the model's top signals — the kind of business-facing glossary a BA maintains so analysts, stakeholders, and new team members share one vocabulary. Weights from `feature_importance_v3.csv`.

<br/>

## 1. Top Ghost-Risk Signals (by model weight)

| Field | Business definition | Model weight | Verifiable from a single page? |
|---|---|:---:|:---:|
| `days_live` | How many days the listing has been continuously posted | 9.8% | ⚠️ Only if the page shows a "posted X ago" date |
| `listing_age_bucket` | `days_live` grouped into freshness bands (fresh / normal / stale) | 9.7% | ⚠️ Depends on `days_live` |
| `velocity_x_no_salary` | Interaction term: how fast an employer posts jobs, weighted by whether pay is disclosed | 7.7% | ❌ No — needs employer posting history |
| `employer_repost_count` | Number of times this employer has reposted this or a near-identical role | 6.9% | ❌ No — needs cross-listing history |
| `desc_per_day` | How much a listing's description text changes across an employer's repeated postings | 6.8% | ❌ No — needs repeated-posting comparison |
| `data_quality_score` | Composite: presence of company name, salary, and adequate description length (0–3) | 6.3% | ✅ Yes |
| `description_length_words` | Word count of the job description | 5.8% | ✅ Yes |
| `posting_velocity_per_week` | How many roles this employer posts per week | 5.7% | ❌ No — needs employer-level aggregation |
| `description_lexical_diversity` | Unique words ÷ total words — flags repetitive/templated text | 5.2% | ✅ Yes |
| `portal_ghost_baseline` | This portal's historical overall ghost-listing rate | 5.0% | ❌ No — needs portal-wide statistics |
| `company_data_completeness_score` | Whether a company name/profile is present and populated | 4.8% | ✅ Yes |
| `keyword_stuffing_ratio` | Degree of unnatural keyword repetition in the description | 4.2% | ✅ Yes (proxy via lexical diversity) |
| `keyword_match_pct` | % overlap between JD skills and the candidate's resume skills | 4.1% | ✅ Yes (computed client-side from saved resume) |
| `salary_disclosed_num` | Whether a salary/compensation figure is stated | 3.7% | ✅ Yes |
| `applications_per_day` | Applicant volume/velocity on this specific posting | 3.1% | ❌ No — needs live applicant-count data |
| `city_tier` | Whether the listed city is a recognized Tier-1 Indian metro | 3.0% | ✅ Yes |
| `experience_range` | Stated years-of-experience requirement | 2.6% | ✅ Yes |
| `city_opportunity_score` | General hiring-market health for the city/role combination | 2.1% | ❌ No — needs market-level data |
| `salary_range_ratio` | Ratio of max-to-min in a stated salary range (very wide ranges are a red flag) | 1.6% | ✅ Yes, if a range is stated |
| `contact_bypass_flag` | Presence of personal email/WhatsApp/phone patterns bypassing the portal's apply flow | 1.0% | ✅ Yes |
| `salary_vs_market_gap` | How the stated salary compares to typical market rate for the role | 0.6% | ❌ No — needs market benchmark data |
| `remote_ambiguity_flag` | "Remote" mentioned without clarifying hybrid/onsite/fully-remote terms | 0.3% | ✅ Yes |
| `urgency_language_score` | Presence of high-pressure phrases ("immediate joiner", "apply now") | 0.1% | ✅ Yes |
| `cross_platform_duplicate_flag` | Whether the exact listing is duplicated across other portals | 0.05% | ❌ No — needs cross-portal search |
| `glassdoor_salary_combo` | Whether Glassdoor's salary data matches what's advertised here | 0.01% | ❌ No — needs live Glassdoor lookup |

<br/>

## 2. Coverage Summary

| Category | Combined model weight | Count |
|---|:---:|:---:|
| ✅ Computable from a single static page | ~62% | 16 signals |
| ❌ Requires live/cross-listing data (flagged manual-check) | ~38% | 10 signals |

<br/>

## 3. Model Output Fields (`predictions_v3.csv`)

| Field | Definition |
|---|---|
| `listing_id` | Unique identifier per scraped listing (portal-prefixed, e.g. `LI...` for LinkedIn) |
| `ghost_risk_score` | Final blended risk score for the listing |
| `ghost_label` | The weak-supervision proxy label used for training |
| `predicted_ghost_prob` | Model's predicted probability of the listing being a ghost posting |
| `predicted_ghost_label` | Binary classification at the model's chosen threshold |
| `stacking_prob` | Probability from the Stacking Ensemble model specifically |
| `bootstrap_mean`, `ci_lower_95`, `ci_upper_95` | Bootstrap-resampled mean prediction and 95% confidence interval, for uncertainty quantification |
| `kmeans_cluster`, `kmeans_cluster_label` | Employer/listing behavioral cluster assignment and its human-readable label |
| `isolation_anomaly`, `isolation_anomaly_flag` | Isolation Forest anomaly score and binary flag for unusual listings |

<br/>

## 4. Employer Cluster Reference (`cluster_profiles_v3.csv`)

| Cluster label | Employer count | Ghost rate | Avg. days live | Salary transparency | Avg. reposts |
|---|:---:|:---:|:---:|:---:|:---:|
| High-Risk Ghost Poster | 1,361 | 32.8% | 23.3 | 2.1 | 3.0 |
| Mid-tier Mixed Signals | 48 | 27.1% | 2.4 | 4.2 | 12.6 |
| *(4 additional clusters — see `cluster_profiles_v3.csv` for full breakdown)* | | | | | |

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
