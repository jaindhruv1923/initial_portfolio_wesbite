<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:1B3A5C,100:C9971F&height=140&section=header&text=Process%20Flow&fontSize=34&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=As-Is%20%E2%86%92%20To-Be%20%C2%B7%20Profitara&descAlignY=68&descSize=16)

</div>

## 🔴 As-Is — before Profitara

```mermaid
flowchart TD
    A[📄 Raw transaction data\nsits in spreadsheets] --> B[🧮 Manual, ad-hoc\nExcel analysis]
    B --> C[💸 Discounting decisions\nmade on gut feel]
    B --> D[⚠️ Churn noticed only\nafter 90+ days inactive]
    B --> E[🔗 Cross-sell decisions\nmade without data]
    C --> F[Margin erodes\nsilently]
    D --> G[Win-back attempted late,\nmore expensive]
    E --> H[Missed cross-sell\nrevenue]

    style A fill:#8f8a9e,color:#fff
    style B fill:#8f8a9e,color:#fff
    style F fill:#9C3B34,color:#fff
    style G fill:#9C3B34,color:#fff
    style H fill:#9C3B34,color:#fff
```

<details>
<summary><b>Pain points (click to expand)</b></summary>
<br/>

- No single source of truth for whether the business is healthy right now
- Churn is reactive — flagged only once a customer has already gone quiet
- Discount policy is not tied to a profit-maximizing benchmark
- Cross-sell decisions rely on intuition, not co-purchase evidence

</details>

<br/>

---

## 🟢 To-Be — with Profitara

```mermaid
flowchart TD
    A[📄 Raw transaction CSV] --> B[🧹 Automated cleaning +\nfeature engineering]
    B --> C[🐘 PostgreSQL layer +\nlive DuckDB SQL Lab]
    B --> D[🤖 ML pipeline:\nRF · LogReg · KMeans ·\nApriori · IsoForest]
    C --> E[📊 13-page Streamlit\ndashboard]
    D --> E
    E --> F[Business Health Score\n+ plain-English narrative]
    E --> G[Ranked win-back list\nwith ₹ value]
    E --> H[Profit-maximizing\ndiscount per sub-category]
    E --> I[Cross-sell rules\nranked by lift]
    F --> J[✅ Faster, evidence-based\nbusiness decisions]
    G --> J
    H --> J
    I --> J

    style A fill:#1B3A5C,color:#fff
    style E fill:#C98A2E,color:#1A1F2B
    style J fill:#2F7D4F,color:#fff
```

<br/>

## 🔀 What changed, step by step

| Step | 🔴 As-Is | 🟢 To-Be |
|---|---|---|
| **Data readiness** | Manual Excel wrangling | Automated cleaning + feature engineering pipeline |
| **Business health check** | No single number; scattered reports | 0–100 Business Health Score, recomputed on any uploaded CSV |
| **Churn detection** | Noticed after 90+ days of inactivity | RFM segmentation flags "Warming" and "At Risk" before full churn |
| **Win-back prioritization** | Not prioritized, or by recency alone | Ranked by revenue at stake, in ₹ |
| **Discount policy** | Set by gut feel per category | Elasticity curve recommends an exact profit-maximizing discount |
| **Cross-sell** | Based on merchandiser intuition | Apriori-derived rules ranked by statistical lift |
| **Ad-hoc questions** | A new spreadsheet pivot each time | Answered live via the SQL Analytics Lab, no rebuild needed |

<br/>

---

## 🎓 Why this matters for a Business Analyst read

This flow is the kind of before/after mapping a BA produces during requirements gathering: pin down the current process, name where it breaks down, and show how the proposed solution closes each gap — quantified in ₹ wherever the data supports it, not left as a vague "improves efficiency" claim.

<br/>

<div align="center"><i>PROFITARA · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
