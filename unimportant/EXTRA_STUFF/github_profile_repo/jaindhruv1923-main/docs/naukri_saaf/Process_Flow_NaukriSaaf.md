<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=140&section=header&text=Process%20Flow&fontSize=34&fontColor=FAF8F4&animation=fadeIn&fontAlignY=42&desc=As-Is%20%E2%86%92%20To-Be%20%C2%B7%20Naukri%20Saaf&descAlignY=68&descSize=16)

</div>

## 🔴 As-Is — before Naukri Saaf

```mermaid
flowchart TD
    A[🔍 Candidate browses\nLinkedIn/Naukri/Indeed/Glassdoor\nseparately] --> B[👀 Judges legitimacy by\nreading the text once]
    B --> C[❓ Can't see days live\nor employer repost pattern]
    B --> D[📝 Manually compares resume\nto JD, listing by listing]
    B --> E[🚫 No signal on employer's\nghost-posting pattern]
    C --> F[Hours spent on\napplications that were\nnever real]
    D --> F
    E --> F

    style A fill:#8f8a9e,color:#fff
    style F fill:#9C3B3B,color:#fff
```

<details>
<summary><b>Pain points (click to expand)</b></summary>
<br/>

- Ghost-listing signals are scattered and platform-specific
- Individual listing text alone is a weak signal vs. employer-level patterns
- Resume-to-JD fit judged manually, listing by listing
- Zero transparency on what can/can't be verified before applying

</details>

<br/>

---

## 🟢 To-Be — with Naukri Saaf

```mermaid
flowchart TD
    A[📄 125,457 listings scraped\nvia Apify, 3 portals] --> B[🧹 SQL staging + cleaning\n32 queries, 8 categories]
    B --> C[🏷️ Weak-supervision\nghost-probability labeling]
    C --> D[🤖 5 classifiers benchmarked\nGBM best · AUC 0.716]
    D --> E[🔬 SHAP explainability +\n6 employer clusters]
    E --> F[📊 7-tab Streamlit\ndashboard]
    E --> G[🧩 Chrome extension\nreal-time, 100% local]
    F --> H[✅ Fast, private,\nevidence-based decision]
    G --> H

    style A fill:#4C1D95,color:#fff
    style F fill:#B8860B,color:#1A1F2B
    style G fill:#B8860B,color:#1A1F2B
    style H fill:#1F7A54,color:#fff
```

<br/>

## 🔀 What changed, step by step

| Step | 🔴 As-Is | 🟢 To-Be |
|---|---|---|
| **Data coverage** | Portals checked one at a time | 125,457 listings unified in one SQL layer |
| **Legitimacy check** | Gut feel, one read-through | Model-weighted risk score from 26 signals |
| **Employer pattern visibility** | Invisible to candidate | 6 behavioral clusters surfaced |
| **Resume fit** | Manual, per listing | Automatic 0–10 score, computed locally |
| **Transparency** | None | Verified-on-page vs manual-check, weights shown |
| **Privacy** | N/A | 100% local, resume never leaves the browser |

<br/>

## 🎓 Why this matters for a BA read

Identify where the current process breaks down for the end user (no portable trust signal), then trace each To-Be capability back to a specific BRD requirement and build artifact — not a vague "AI-powered" claim.

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
