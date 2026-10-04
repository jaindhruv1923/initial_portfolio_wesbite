<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=150&section=header&text=Business%20Analysis%20%E2%80%94%20Full%20Package&fontSize=32&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=Naukri%20Saaf%20%C2%B7%20Ghost%20Job%20Listing%20Detection%20Platform&descAlignY=68&descSize=14)

</div>

## 📁 What's in this package

Every standard BA deliverable, built against the real Naukri Saaf pipeline (125,457 scraped listings → 2,852 modeled → GBM AUC 0.716 → 7-tab dashboard → Chrome extension). Nothing here is generic filler — every artifact traces back to an actual file, model, or feature in the build.

| # | Document | BA discipline it demonstrates |
|---|---|---|
| 1 | [`BRD_NaukriSaaf.md`](./BRD_NaukriSaaf.md) | Requirements elicitation & documentation |
| 2 | [`Stakeholder_Analysis.md`](./Stakeholder_Analysis.md) | Stakeholder mapping, power/interest, RACI |
| 3 | [`User_Stories.md`](./User_Stories.md) | Agile requirements, Gherkin acceptance criteria |
| 4 | [`Gap_Analysis.md`](./Gap_Analysis.md) | Current-vs-future state, capability gaps |
| 5 | [`Functional_Specification.md`](./Functional_Specification.md) | Detailed functional spec, business rules |
| 6 | [`Data_Dictionary.md`](./Data_Dictionary.md) | Data governance, field-level definitions |
| 7 | [`Requirements_Traceability_Matrix.md`](./Requirements_Traceability_Matrix.md) | Traceability from requirement → build → test |
| 8 | [`Risk_Register.md`](./Risk_Register.md) | Risk identification, scoring, mitigation |
| 9 | [`UAT_Test_Cases.md`](./UAT_Test_Cases.md) | Acceptance testing, sign-off criteria |
| 10 | [`KPI_Success_Metrics.md`](./KPI_Success_Metrics.md) | Post-launch measurement framework |
| 11 | [`Executive_Summary_NaukriSaaf.md`](./Executive_Summary_NaukriSaaf.md) | Stakeholder communication, findings synthesis |
| 12 | [`Process_Flow_NaukriSaaf.md`](./Process_Flow_NaukriSaaf.md) | As-Is/To-Be process mapping |

<br/>

## 🧭 How a BA would actually use these, in order

```mermaid
flowchart TD
    A[1. BRD] --> B[2. Stakeholder Analysis]
    B --> C[3. User Stories]
    A --> D[4. Gap Analysis]
    D --> E[5. Functional Specification]
    E --> F[6. Data Dictionary]
    A --> G[7. Requirements Traceability Matrix]
    G --> H[9. UAT Test Cases]
    E --> H
    A --> I[8. Risk Register]
    H --> J[10. KPI / Success Metrics]
    J --> K[11. Executive Summary]
    D --> L[12. Process Flow]

    style A fill:#4C1D95,color:#fff
    style G fill:#B8860B,color:#1A1F2B
    style J fill:#1F7A54,color:#fff
```

<br/>

## 🎯 Reference facts used throughout

<div align="center">

| Metric | Value |
|:---|:---:|
| Raw listings scraped | **125,457** (LinkedIn, Indeed, Glassdoor) |
| Unique listings modeled | **2,852** |
| Best model | **GBM — AUC 0.716, F1 0.527** |
| Ghost-risk model features | **26**, SHAP-explained per listing |
| Highest-risk employer cluster | **1,361 employers · 32.8% ghost rate** |
| Chrome extension coverage | **~62% of model weight** verifiable from a single page; ~38% flagged manual-check |
| Dashboard | **7 tabs** — Overview, Platforms, Ghost Detection, Employers, Model Performance, Cluster, Explore |

</div>

<br/>

<div align="center"><i>Part of the Naukri Saaf project · Dhruv Jain</i></div>
