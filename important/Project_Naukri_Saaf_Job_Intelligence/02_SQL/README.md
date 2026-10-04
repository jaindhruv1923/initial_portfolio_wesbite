# 02 — SQL Database & Analytical Workbench

## 🗄️ MySQL 8.0 Forensic Analytics

This module contains the enterprise SQL analytics workbench developed to query, transform, and detect behavioral anomalies across **2,851 multi-platform job listings**.

- **Primary Workbench Script**: [`naukri_saaf_sql_workbench.sql`](naukri_saaf_sql_workbench.sql)

---

## 📋 Query Catalog (42 Production Queries Across 9 Categories)

| Section | Focus Area | Key SQL Techniques / Concepts |
|---|---|---|
| **1. Database & Schema Initialization** | DDL, constraints, indexing | `CREATE TABLE`, composite indexes, datatype optimization |
| **2. Data Cleaning & Normalization** | Text hygiene & deduplication | `REGEXP_REPLACE`, `TRIM`, `CASE WHEN`, staging tables |
| **3. Descriptive Analytics & KPIs** | Cardinality and platform totals | Aggregations (`COUNT`, `AVG`, `STDDEV`), grouping sets |
| **4. Compensation & Salary Forensics** | Disclosure rates & spreads | Multi-tiered `CASE`, annualization, missingness auditing |
| **5. Geographic & Tech Hub Disparities**| City clusters & metro rates | `GROUP BY`, conditional rollup, tier classification |
| **6. Temporal Dynamics & Staleness** | Requisition decay & lifespan | Date arithmetic (`DATEDIFF`), cohort bucketing |
| **7. Window Functions & Rankings** | Top employer exposure | `ROW_NUMBER()`, `DENSE_RANK()`, `NTILE(4)`, `LAG()` |
| **8. Multi-Table CTE Aggregations** | Enterprise pipeline modeling | Recursive & chained Common Table Expressions (`WITH`) |
| **9. Ghost Job Behavioral Forensics** | Targeted forensic queries (`I1`–`I10`)| Cross-company syndication, zombie listings, opacity CTEs |

---

## 🚀 Execution Guide

1. Ensure MySQL 8.0+ is running locally:
   ```bash
   mysql -u root -p
   ```
2. Run the script:
   ```sql
   SOURCE 02_SQL/naukri_saaf_sql_workbench.sql;
   ```
3. All views, staging tables, and forensic queries will execute sequentially with documented execution plans.
