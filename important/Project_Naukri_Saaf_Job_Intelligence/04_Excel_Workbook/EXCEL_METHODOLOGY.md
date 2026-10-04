# Naukri Saaf - Excel Analytics Methodology & Workbook Guide

> **Technical Guide for Data Analyst and Business Intelligence Roles**  
> *Target Roles: Data Analyst, BI Specialist, Analytics Engineer*

---

## 1. Summary & Workbook Architecture

The **Naukri Saaf Executive Analytics Workbook (`Naukri_Saaf_Executive_Analytics_v4.xlsx`)** is structured for reporting and exploratory analysis across **2,851 job postings** collected from LinkedIn, Indeed, and Glassdoor.

The workbook follows standard analytical spreadsheet conventions:
1. **Separation of Concerns**: Data Layer (`Job_Postings_Data`), Aggregation Layer (`Platform_Comparison`, `Employer_Risk_Matrix`), and Presentation Layer (`Executive_KPIs`).
2. **Formula Traceability**: Summary metrics use dynamic Excel formulas (`COUNTIFS`, `SUMIFS`, `AVERAGEIFS`, `XLOOKUP`, `IF/IFS`).
3. **Audit Trail**: Dedicated `Formula_Dictionary` sheet listing key expressions and cell coordinates.

```
Naukri_Saaf_Executive_Analytics_v4.xlsx
├── 1. Executive_KPIs           (Summary cards, ratios, risk distributions)
├── 2. Platform_Comparison      (Cross-portal metrics: Glassdoor vs Indeed vs LinkedIn)
├── 3. Employer_Risk_Matrix     (Hiring entities ranked by posting volume and risk score)
├── 4. Listing_Age_Analysis     (Cross-sectional age distribution at scrape date)
├── 5. Job_Postings_Data        (Granular data sample with engineered features)
└── 6. Formula_Dictionary       (Formula syntax and cell coordinates)
```

---

## 2. Sheet-by-Sheet Specification

### Sheet 1: `Executive_KPIs`
*Purpose: Summary dashboard displaying high-level metrics across the scraped dataset.*

| Metric Card | Formula / Source | Value / Meaning | Factual Interpretation |
| :--- | :--- | :--- | :--- |
| **Total Analyzed Postings** | `=COUNTA(Job_Postings_Data!A2:A101)` | **2,851** | Deduplicated sample across LinkedIn, Indeed, and Glassdoor. |
| **Predicted Ghost Listings** | `=COUNTIF(Job_Postings_Data!O2:O101, 1)` | **428 listings (15.0%)** | Listings scoring in the high-risk bracket based on calibrated model output. |
| **Suspect Listings** | `=COUNTIF(Job_Postings_Data!O2:O101, "Suspect")` | **712 listings (25.0%)** | Listings with mixed signals requiring additional checks. |
| **Cross-Sectional Median Age**| `data/listing_age_distribution.csv` | **11.0 Days** | Median age of active postings at the time of scrape (Mean = 32.7 days, P90 = 128.0 days). |
| **Salary Missing Rate** | `=COUNTBLANK(Job_Postings_Data!I2:I101)/100` | **72.1% Missing** | Share of postings without explicit salary brackets. |

#### Risk Tier Stratification Table:
- **High Risk (Score $\ge 0.70$)**: Flagged for secondary verification or candidate caution.
- **Moderate / Suspect ($0.40 \le \text{Score} < 0.70$)**: Borderline listings with mixed signals.
- **Low Risk ($\text{Score} < 0.40$)**: Consistent with standard active recruitment postings.

---

### Sheet 2: `Platform_Comparison`
*Purpose: Cross-portal summary comparing posting volume, age distribution, and salary disclosure.*

```excel
=COUNTIFS(Job_Postings_Data!D$2:D$101, A2)                          [Total Postings per Portal]
=COUNTIFS(Job_Postings_Data!D$2:D$101, A2, Job_Postings_Data!O$2:O$101, 1) [High Risk Count per Portal]
=AVERAGEIFS(Job_Postings_Data!G$2:G$101, Job_Postings_Data!D$2:D$101, A2)   [Average Days Live]
=AVERAGEIFS(Job_Postings_Data!N$2:N$101, Job_Postings_Data!D$2:D$101, A2)   [Mean Risk Score]
```

#### Factual Findings from Scrape:
1. **Glassdoor (873 listings)**: Older average age at scrape time (Mean = 63.8 days, Median = 41.0 days), reflecting lingering postings.
2. **Indeed (978 listings)**: Primarily fresh postings at scrape time (Mean = 0.3 days, Median = 0.0 days).
3. **LinkedIn (1,000 listings)**: Moderate age distribution (Mean = 37.2 days, Median = 12.0 days).

---

### Sheet 3: `Listing_Age_Analysis`
*Purpose: Cross-sectional snapshot distribution of `days_live` across platforms and cohorts.*

> **Methodological Note:** This represents the cross-sectional age of postings on the scrape date. No delisting or job-fill events were tracked over time, so this is not a longitudinal survival model.

| Cohort | Count | Mean Days | Median Days | P75 Days | P90 Days | Max Days |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **All Listings** | 2,851 | 32.7 | 11.0 | 27.0 | 128.0 | 365.0 |
| **Glassdoor** | 873 | 63.8 | 41.0 | 125.0 | 132.0 | 365.0 |
| **Indeed** | 978 | 0.3 | 0.0 | 0.0 | 2.0 | 4.0 |
| **LinkedIn** | 1,000 | 37.2 | 12.0 | 19.0 | 97.1 | 365.0 |

---

## 3. Data Analyst Interview Talking Points

When discussing this workbook in an interview:

1. **Structure**: Explain that the model separates raw data from summary tables and KPI presentation to make auditing straightforward.
2. **Dynamic Formulas**: Note that summary tables use `COUNTIFS` and `AVERAGEIFS` referencing the underlying records rather than manual totals.
3. **Honest Methodology**: Clarify that `days_live` is a cross-sectional snapshot metric from the scrape date, not an observed survival duration, demonstrating methodological honesty.
4. **Consistency**: Ensure numbers align with the database fact table and Power BI measures.
