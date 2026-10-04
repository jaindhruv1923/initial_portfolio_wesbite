<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:146B5E,100:C9971F&height=140&section=header&text=Business%20Requirements%20Document&fontSize=30&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Profitara%20%C2%B7%20Retail%20Business%20Intelligence%20Platform&descAlignY=68&descSize=15)

![Status](https://img.shields.io/badge/status-complete-2F7D4F?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0-146B5E?style=flat-square)
![Author](https://img.shields.io/badge/author-Dhruv_Jain-C98A2E?style=flat-square)

</div>

> **Note on document type:** this BRD is written retrospectively against a completed build, in the structure and language it would have carried had it been scoped at project kickoff. Requirements were derived from standard retail-analytics stakeholder needs, not from live client interviews.

<br/>

## 📖 Contents

- [1. Purpose](#1-purpose)
- [2. Business Problem](#2-business-problem)
- [3. Stakeholders](#3-stakeholders)
- [4. Scope](#4-scope)
- [5. Business Requirements](#5-business-requirements)
- [6. Non-Functional Requirements](#6-non-functional-requirements)
- [7. Assumptions & Constraints](#7-assumptions--constraints)
- [8. Success Metrics](#8-success-metrics)

<br/>

## 1. Purpose

This document defines the business problem, requirements, and success criteria for **Profitara**, a retail analytics platform built on a **10,000-row India quick-commerce transaction dataset** — 4,918 orders, 1,448 customers, 9 categories, 17 sub-categories, generating **₹66.95L** in total revenue.

<br/>

## 2. Business Problem

Retail businesses generate large volumes of transaction data but lack the tooling to convert it into decisions. Three problems drove this project:

| 🎯 Problem | 📉 Business impact if unaddressed |
|---|---|
| No visibility into where margin is leaking | Discount overuse and structurally unprofitable products quietly erode profit every month |
| No early warning for customer churn | By the time a customer is confirmed lost, win-back is far more expensive than retention |
| No demand signal tied to inventory or pricing | Businesses over-stock or run out, and pricing decisions are made on gut feel |

<br/>

## 3. Stakeholders

<details open>
<summary><b>Role-based stakeholders, modeled for the purpose of this exercise</b></summary>
<br/>

| Stakeholder | Interest |
|---|---|
| 🧑‍💼 **Retail Operations Lead** | A single view of business health, updated automatically |
| 📣 **Marketing / CRM team** | A ranked list of at-risk customers and revenue tied to them, to prioritize win-back spend |
| 💰 **Pricing / Category team** | Visibility into over-discounted sub-categories and the profit-maximizing discount level |
| 📊 **Finance** | Revenue, margin, and leakage figures traceable back to source transactions |

</details>

<br/>

## 4. Scope

<table>
<tr>
<td width="50%" valign="top">

### ✅ In scope
- Descriptive analytics — revenue, margin, category & segment performance
- Predictive analytics — churn probability, 12-month CLV, demand forecast
- Prescriptive analytics — discount optimization, win-back prioritization, cross-sell recommendations
- A self-service SQL layer for ad-hoc business questions

</td>
<td width="50%" valign="top">

### ❌ Out of scope
- Real-time transaction ingestion (static, batch dataset)
- Multi-tenant deployment for more than one retail business
- Automated execution of recommendations (e.g. auto-applying a discount change)

</td>
</tr>
</table>

<br/>

## 5. Business Requirements

<details open>
<summary><b>Click to expand all 11 requirements</b></summary>
<br/>

| ID | Requirement | Delivered as |
|---|---|---|
| `BR-01` | Show overall business health at a glance, in a single score | 0–100 Business Health Scorecard — **75/100, Healthy** |
| `BR-02` | Identify customers likely to churn, ranked by revenue at stake | RFM-based churn segmentation + Win-Back Priority List |
| `BR-03` | Quantify revenue recoverable through win-back action | **₹4,116K** tied to at-risk/churned customers; 20% recovery ≈ **₹823K** |
| `BR-04` | Flag where discounting is destroying margin | Discount Elasticity Simulator + Leakage & Abuse module — 299 orders, ₹34K impact |
| `BR-05` | Recommend a profit-maximizing discount per sub-category | Profit-vs-discount elasticity curve, per sub-category |
| `BR-06` | Surface which products should be cross-sold together | Apriori market basket analysis — **52 rules**; top: Baby Food → Diapers & Wipes, lift 9.58× |
| `BR-07` | Predict customer lifetime value to prioritize retention spend | Random Forest CLV model — **R² = 0.930** |
| `BR-08` | Segment customers by value and behavior | K-Means segmentation — silhouette 0.611; 119 Champion customers |
| `BR-09` | Explain retention over time, not just a snapshot | Cohort retention heatmap + survival curve — median half-life ≈ 330 days |
| `BR-10` | Let non-technical stakeholders read findings without opening code | Auto-generated plain-English Executive Narrative |
| `BR-11` | Let analyst users ask custom questions of the data | Live SQL Analytics Lab (DuckDB) with preset queries |

</details>

<br/>

## 6. Non-Functional Requirements

| Requirement | Definition of done |
|---|---|
| **Usability** | Runs with a single command (`run.bat` / `run.sh`) — no setup beyond `pip install` |
| **Portability** | Accepts a user-uploaded CSV and recomputes every module against it |
| **Traceability** | Every headline figure on the Overview page is reproducible from the SQL layer |
| **Accessibility** | Atkinson Hyperlegible typeface used across the dashboard for readability |

<br/>

## 7. Assumptions & Constraints

- Dataset is historical and static; forecasts (Holt-Winters, demand heatmap) reflect this snapshot and would need periodic re-runs in production
- The Business Health Score and its thresholds (e.g. what counts as "at risk") are documented, rule-based judgment calls, not externally benchmarked
- No live stakeholder interviews were conducted for this solo academic build; requirements were derived from standard retail-analytics practice for each function represented above

<br/>

## 8. Success Metrics

| Metric | Target | Status |
|---|:---:|---|
| Business Health Score computed and explained in plain English | ✅ | Delivered |
| At-risk revenue quantified in ₹ | ✅ | ₹4,638K flagged at churn risk |
| Each module ends in a quantified, actionable recommendation | ✅ | Delivered across all 13 pages |
| Dashboard runnable by a non-technical user in under 5 minutes | ✅ | One-click `run.bat` / `run.sh` |

<br/>

<div align="center"><i>PROFITARA · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
