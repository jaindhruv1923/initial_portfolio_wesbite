<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:1B3A5C,100:C9971F&height=150&section=header&text=Business%20Analysis&fontSize=42&fontColor=FAF8F4&animation=fadeIn&fontAlignY=38&desc=Profitara%20%C2%B7%20Requirements%2C%20Findings%20%26%20Process&descAlignY=62&descSize=16)

[![Doc Type](https://img.shields.io/badge/BRD-Business_Requirements-146B5E?style=for-the-badge)](./BRD_Profitara.md)
[![Doc Type](https://img.shields.io/badge/Summary-Executive_Findings-C98A2E?style=for-the-badge)](./Executive_Summary_Profitara.md)
[![Doc Type](https://img.shields.io/badge/Flow-As--Is_%E2%86%92_To--Be-1B3A5C?style=for-the-badge)](./Process_Flow_Profitara.md)

</div>

<br/>

## 📁 What's in this folder

This folder documents the **business-analyst side** of the Profitara build — the requirements, findings, and process thinking that sit behind the ML pipeline and dashboard, presented the way a BA would hand them to a stakeholder.

| Document | What it answers | Read this if you're... |
|---|---|---|
| 📋 [`BRD_Profitara.md`](./BRD_Profitara.md) | What was the business problem, who are the stakeholders, and what exactly was scoped? | Reviewing this as a requirements/scoping exercise |
| 📊 [`Executive_Summary_Profitara.md`](./Executive_Summary_Profitara.md) | What did the data actually find, in plain English with ₹ recommendations? | A non-technical stakeholder who wants the 2-minute version |
| 🔀 [`Process_Flow_Profitara.md`](./Process_Flow_Profitara.md) | How does the business process change before vs. after Profitara? | Interested in the before/after operational impact |

<br/>

## 🧭 How these fit together

```mermaid
flowchart LR
    A[BRD\nProblem + Requirements] --> B[Dashboard build\n13 pages · 12 ML models]
    B --> C[Executive Summary\nFindings + ₹ recommendations]
    A --> D[Process Flow\nAs-Is vs To-Be]
    D --> C
    style A fill:#146B5E,color:#fff
    style C fill:#C98A2E,color:#1A1F2B
    style D fill:#1B3A5C,color:#fff
```

The BRD defines *why* the project exists and *what* it had to deliver. The Executive Summary reports *what was found*. The Process Flow shows *what changed* operationally as a result.

<br/>

## 🎯 Quick facts referenced across all three docs

<div align="center">

| Metric | Value |
|:---|:---:|
| Business Health Score | **75 / 100 — Healthy** |
| Total Revenue | **₹6.70M** |
| Net Profit Margin | **4.15%** |
| Revenue tied to churn risk | **₹4,116K** |
| Recoverable via 20% win-back | **₹823K** |
| Cross-sell rules discovered | **52** (top: Baby Food → Diapers & Wipes, lift 9.58×) |

</div>

<br/>

<div align="center"><i>Part of the <a href="https://github.com/jaindhruv1923/Project-Profitara-Retail-BI-Pipeline">Profitara</a> project · Dhruv Jain</i></div>
