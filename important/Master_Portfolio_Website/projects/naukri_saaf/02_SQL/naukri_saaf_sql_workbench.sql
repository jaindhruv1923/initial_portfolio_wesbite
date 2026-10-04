-- =====================================================================
-- NAUKRI SAAF — SQL ANALYTICAL WORKBOOK
-- =====================================================================
-- Purpose : End-to-end SQL portfolio pipeline on ~3,000 real scraped
--           job listings (Glassdoor + Indeed + LinkedIn), combined into
--           a single unified dataset (naukri_saaf_combined_raw.csv).
-- Tested  : MariaDB 10.11 (MySQL 8.0 compatible syntax throughout)
-- Author  : Dhruv Jain
-- =====================================================================


-- =====================================================================
-- SECTION 0: DATABASE SETUP
-- =====================================================================
CREATE DATABASE IF NOT EXISTS naukri_saaf;
drop database if exists naukri_saaf;
USE naukri_saaf;


-- =====================================================================
-- SECTION 1: RAW STAGING TABLE
-- =====================================================================
-- This table mirrors naukri_saaf_combined_raw.csv column-for-column.
-- Everything text/salary/date related is kept as VARCHAR here on
-- purpose — real scraped data is messy (mixed date formats, salary
-- as free text, applicant counts as phrases like "Over 200 applicants").
-- We load it as-is first, then clean it properly in Section 2.
-- This mirrors how a real analyst would handle raw vendor data.

DROP TABLE IF EXISTS naukri_jobs_raw;

CREATE TABLE naukri_jobs_raw (
    job_id                VARCHAR(20)   PRIMARY KEY,
    source                VARCHAR(20),
    title                 VARCHAR(150),
    company_name          VARCHAR(150),
    location_raw          VARCHAR(120),
    location_city         VARCHAR(100),
    location_state        VARCHAR(100),
    location_country      VARCHAR(100),
    job_type              VARCHAR(60),
    experience_level      VARCHAR(40),
    years_experience_raw  VARCHAR(400),
    description_text      TEXT,
    salary_min            VARCHAR(30),
    salary_max            VARCHAR(30),
    salary_currency       VARCHAR(10),
    salary_period         VARCHAR(20),
    date_posted           VARCHAR(40),
    posted_time_raw       VARCHAR(30),
    date_scraped          VARCHAR(40),
    age_in_days           VARCHAR(20),
    job_url               VARCHAR(400),
    apply_url             VARCHAR(700),
    search_keyword        VARCHAR(120),
    job_category          VARCHAR(180),
    remote_type           VARCHAR(100),
    company_size          VARCHAR(50),
    company_rating        VARCHAR(20),
    applications_count    VARCHAR(80),
    attributes_combined   TEXT,
    matched_keywords      VARCHAR(300),
    unmatched_keywords    VARCHAR(300)
);


-- =====================================================================
-- SECTION 1B: IMPORT THE DATA  (read the guide below before running)
-- =====================================================================
-- OPTION A (recommended) — MySQL Workbench "Table Data Import Wizard":
--   Right-click "Tables" under naukri_saaf schema in the left Navigator
--   > Table Data Import Wizard > select naukri_saaf_combined_raw.csv
--   > "Use existing table" > choose naukri_jobs_raw > Next > Finish.
--   Skip the LOAD DATA statement below entirely if you use this route.
--
-- OPTION B — LOAD DATA LOCAL INFILE (if you prefer pure SQL):
--   1. Update the file path below to wherever the CSV sits on YOUR machine.
--   2. In Workbench: Edit > Preferences > SQL Editor > check
--      "Enable LOAD LOCAL INFILE", then reconnect.
--   3. Uncomment and run the block below.
SHOW VARIABLES LIKE 'secure_file_priv';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/naukri_saaf_combined_raw.csv'
INTO TABLE naukri_jobs_raw
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(job_id, source, title, company_name, location_raw, location_city,
 location_state, location_country, job_type, experience_level,
 years_experience_raw, description_text, salary_min, salary_max,
 salary_currency, salary_period, date_posted, posted_time_raw,
 date_scraped, age_in_days, job_url, apply_url, search_keyword,
 job_category, remote_type, company_size, company_rating,
 applications_count, attributes_combined, matched_keywords,
 unmatched_keywords);
-- LOAD DATA LOCAL INFILE '/absolute/path/to/naukri_saaf_combined_raw.csv'
-- INTO TABLE naukri_jobs_raw
-- CHARACTER SET utf8mb4
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (job_id, source, title, company_name, location_raw, location_city,
--  location_state, location_country, job_type, experience_level,
--  years_experience_raw, description_text, salary_min, salary_max,
--  salary_currency, salary_period, date_posted, posted_time_raw,
--  date_scraped, age_in_days, job_url, apply_url, search_keyword,
--  job_category, remote_type, company_size, company_rating,
--  applications_count, attributes_combined, matched_keywords,
--  unmatched_keywords);

-- Sanity check after import — should return 3000
SELECT COUNT(*) FROM naukri_jobs_raw;


-- =====================================================================
-- SECTION 2: DATA CLEANING — build a typed, analysis-ready table
-- =====================================================================
-- Raw data problems being fixed here:
--   • date_posted / date_scraped are ISO strings like
--     "2026-06-30T00:00:00.000Z" -> converted to real DATETIME
--   • salary_min / salary_max are numeric-looking text -> DECIMAL
--   • applications_count is free text ("Over 200 applicants",
--     "Be among the first 25 applicants") -> extracted numeric estimate
--   • remote_type: DATA QUALITY FLAG. For the Glassdoor slice, this
--     column is populated from LinkedIn/Glassdoor "job function" style
--     tags rather than a genuine remote/onsite/hybrid flag. It is kept
--     as-is (remote_type_raw) and NOT trusted for a clean remote/onsite
--     split — documented here as an interview talking point rather than
--     silently treated as ground truth.

DROP TABLE IF EXISTS naukri_jobs;

-- NOTE: LOAD DATA / the Import Wizard store blank CSV fields as empty
-- strings ('') in a VARCHAR/TEXT column, NOT as true NULLs. Every text
-- column below is passed through NULLIF(TRIM(...), '') so that blank
-- fields behave as NULL for all the "IS NOT NULL" filters used later.

CREATE TABLE naukri_jobs AS
SELECT
    job_id,
    source,
    TRIM(title)                                            AS title,
    NULLIF(NULLIF(TRIM(company_name), ''), 'nan')          AS company_name,
    NULLIF(TRIM(location_raw), '')                         AS location_raw,
    NULLIF(TRIM(location_city), '')                        AS location_city,
    NULLIF(TRIM(location_state), '')                       AS location_state,
    NULLIF(TRIM(location_country), '')                     AS location_country,
    NULLIF(TRIM(job_type), '')                             AS job_type,
    NULLIF(TRIM(experience_level), '')                     AS experience_level,
    NULLIF(TRIM(years_experience_raw), '')                 AS years_experience_raw,
    NULLIF(TRIM(description_text), '')                     AS description_text,

    CAST(NULLIF(REGEXP_REPLACE(salary_min, '[^0-9.]', ''), '') AS DECIMAL(14,2)) AS salary_min,
    CAST(NULLIF(REGEXP_REPLACE(salary_max, '[^0-9.]', ''), '') AS DECIMAL(14,2)) AS salary_max,
    NULLIF(TRIM(salary_currency), '')                      AS salary_currency,
    NULLIF(TRIM(salary_period), '')                        AS salary_period,

    STR_TO_DATE(NULLIF(LEFT(TRIM(date_posted), 10), ''), '%Y-%m-%d') AS date_posted,
    NULLIF(TRIM(posted_time_raw), '')                      AS posted_time_raw,
    STR_TO_DATE(NULLIF(LEFT(TRIM(date_scraped), 10), ''), '%Y-%m-%d') AS date_scraped,
    CAST(NULLIF(age_in_days, '') AS DECIMAL(10,2))         AS age_in_days,

    NULLIF(TRIM(job_url), '')                              AS job_url,
    NULLIF(TRIM(apply_url), '')                            AS apply_url,
    NULLIF(TRIM(search_keyword), '')                       AS search_keyword,
    NULLIF(TRIM(job_category), '')                         AS job_category,
    NULLIF(TRIM(remote_type), '')                          AS remote_type_raw,
    NULLIF(TRIM(company_size), '')                         AS company_size,
    CAST(NULLIF(company_rating, '') AS DECIMAL(3,2))       AS company_rating,

    NULLIF(TRIM(applications_count), '')                   AS applications_count_raw,
    CASE
        WHEN applications_count REGEXP '^Over [0-9]+'
            THEN CAST(REGEXP_REPLACE(applications_count, '[^0-9]', '') AS UNSIGNED)
        WHEN applications_count REGEXP 'first [0-9]+'
            THEN CAST(REGEXP_REPLACE(applications_count, '[^0-9]', '') AS UNSIGNED)
        ELSE NULL
    END                                                     AS applications_count_est,

    NULLIF(TRIM(attributes_combined), '')                  AS attributes_combined,
    NULLIF(TRIM(matched_keywords), '')                     AS matched_keywords,
    NULLIF(TRIM(unmatched_keywords), '')                   AS unmatched_keywords
FROM naukri_jobs_raw;

ALTER TABLE naukri_jobs ADD PRIMARY KEY (job_id);
ALTER TABLE naukri_jobs ADD INDEX idx_source (source);
ALTER TABLE naukri_jobs ADD INDEX idx_company (company_name);
ALTER TABLE naukri_jobs ADD INDEX idx_category (job_category(50));
ALTER TABLE naukri_jobs ADD INDEX idx_date_posted (date_posted);

-- Sanity check — should return 3000
SELECT COUNT(*) AS total_rows FROM naukri_jobs;


-- =====================================================================
-- SECTION 3: ANALYTICAL QUERIES  (32 queries across 8 categories)
-- =====================================================================

-- ---------------------------------------------------------------------
-- CATEGORY A — DATA PROFILING & QUALITY CHECKS
-- ---------------------------------------------------------------------

-- A1. Row count and null-rate profile per column (core columns)
SELECT
    COUNT(*)                                              AS total_rows,
    SUM(company_name IS NULL)                             AS null_company_name,
    SUM(salary_min IS NULL)                                AS null_salary_min,
    SUM(salary_max IS NULL)                                AS null_salary_max,
    SUM(date_posted IS NULL)                               AS null_date_posted,
    SUM(company_rating IS NULL)                            AS null_company_rating,
    SUM(remote_type_raw IS NULL)                           AS null_remote_type
FROM naukri_jobs;

-- A2. Duplicate job check — same title + company + location appearing
--     more than once across (or within) sources
SELECT title, company_name, location_raw, COUNT(*) AS occurrences
FROM naukri_jobs
GROUP BY title, company_name, location_raw
HAVING COUNT(*) > 1
ORDER BY occurrences DESC
LIMIT 20;

-- A3. Row count and null-rate by source (are some sources messier?)
SELECT
    source,
    COUNT(*)                       AS total_rows,
    SUM(salary_min IS NULL)        AS missing_salary,
    SUM(company_rating IS NULL)    AS missing_rating,
    SUM(remote_type_raw IS NULL)   AS missing_remote_type
FROM naukri_jobs
GROUP BY source;

-- A4. Data-quality flag: remote_type_raw distinct values sample
--     (documents that this field is NOT a clean remote/onsite/hybrid
--     flag for parts of the dataset — see Section 2 comment)
SELECT source, remote_type_raw, COUNT(*) AS cnt
FROM naukri_jobs
WHERE remote_type_raw IS NOT NULL
GROUP BY source, remote_type_raw
ORDER BY cnt DESC
LIMIT 20;


-- ---------------------------------------------------------------------
-- CATEGORY B — SOURCE & CATEGORY OVERVIEW
-- ---------------------------------------------------------------------

-- B1. Total listings per source
SELECT source, COUNT(*) AS total_listings
FROM naukri_jobs
GROUP BY source
ORDER BY total_listings DESC;

-- B2. Top 15 job categories overall
SELECT job_category, COUNT(*) AS listings
FROM naukri_jobs
WHERE job_category IS NOT NULL
GROUP BY job_category
ORDER BY listings DESC
LIMIT 15;

-- B3. Top 15 searched keywords driving the most listings
SELECT search_keyword, COUNT(*) AS listings
FROM naukri_jobs
WHERE search_keyword IS NOT NULL
GROUP BY search_keyword
ORDER BY listings DESC
LIMIT 15;

-- B4. Job type distribution (where available)
SELECT job_type, COUNT(*) AS listings
FROM naukri_jobs
WHERE job_type IS NOT NULL
GROUP BY job_type
ORDER BY listings DESC
LIMIT 15;


-- ---------------------------------------------------------------------
-- CATEGORY C — COMPANY ANALYSIS
-- ---------------------------------------------------------------------

-- C1. Top 15 companies by number of listings
SELECT company_name, COUNT(*) AS listings
FROM naukri_jobs
WHERE company_name IS NOT NULL
GROUP BY company_name
ORDER BY listings DESC
LIMIT 15;

-- C2. Highest-rated companies (Glassdoor-sourced rating) with >= 2 listings
SELECT company_name, AVG(company_rating) AS avg_rating, COUNT(*) AS listings
FROM naukri_jobs
WHERE company_rating IS NOT NULL
GROUP BY company_name
HAVING COUNT(*) >= 2
ORDER BY avg_rating DESC
LIMIT 15;

-- C3. Company size buckets vs average company rating
SELECT company_size, ROUND(AVG(company_rating), 2) AS avg_rating, COUNT(*) AS listings
FROM naukri_jobs
WHERE company_size IS NOT NULL
GROUP BY company_size
ORDER BY listings DESC;

-- C4. Companies posting across the most sources (multi-source presence)
SELECT company_name, COUNT(DISTINCT source) AS sources_used, COUNT(*) AS total_listings
FROM naukri_jobs
WHERE company_name IS NOT NULL
GROUP BY company_name
HAVING COUNT(DISTINCT source) > 1
ORDER BY sources_used DESC, total_listings DESC
LIMIT 15;


-- ---------------------------------------------------------------------
-- CATEGORY D — LOCATION ANALYSIS
-- ---------------------------------------------------------------------

-- D1. Top 15 hiring locations overall
SELECT location_raw, COUNT(*) AS listings
FROM naukri_jobs
WHERE location_raw IS NOT NULL
GROUP BY location_raw
ORDER BY listings DESC
LIMIT 15;

-- D2. Country-level breakdown (Glassdoor + Indeed only — these two
--     sources have structured location fields; LinkedIn's is free text)
SELECT location_country, COUNT(*) AS listings
FROM naukri_jobs
WHERE location_country IS NOT NULL
GROUP BY location_country
ORDER BY listings DESC;

-- D3. Top city + state combinations
SELECT location_city, location_state, COUNT(*) AS listings
FROM naukri_jobs
WHERE location_city IS NOT NULL
GROUP BY location_city, location_state
ORDER BY listings DESC
LIMIT 15;

-- D4. Average salary_max by location (top 10 by listing volume)
SELECT location_raw,
       COUNT(*) AS listings,
       ROUND(AVG(salary_max), 0) AS avg_salary_max
FROM naukri_jobs
WHERE location_raw IS NOT NULL AND salary_max IS NOT NULL
GROUP BY location_raw
ORDER BY listings DESC
LIMIT 10;


-- ---------------------------------------------------------------------
-- CATEGORY E — SALARY ANALYSIS
-- ---------------------------------------------------------------------

-- E1. Overall salary distribution stats (min, max, avg, median-ish via percentile)
SELECT
    MIN(salary_min) AS lowest_salary,
    MAX(salary_max) AS highest_salary,
    ROUND(AVG(salary_min), 0) AS avg_salary_min,
    ROUND(AVG(salary_max), 0) AS avg_salary_max
FROM naukri_jobs
WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL;

-- E2. Top 10 highest-paying job categories by average max salary
--     (only categories with at least 3 salary-tagged listings)
SELECT job_category,
       COUNT(*) AS listings_with_salary,
       ROUND(AVG(salary_max), 0) AS avg_salary_max
FROM naukri_jobs
WHERE salary_max IS NOT NULL AND job_category IS NOT NULL
GROUP BY job_category
HAVING COUNT(*) >= 3
ORDER BY avg_salary_max DESC
LIMIT 10;

-- E3. Salary availability rate per source (what % of listings disclose salary)
SELECT
    source,
    COUNT(*) AS total_listings,
    SUM(salary_max IS NOT NULL) AS listings_with_salary,
    ROUND(100 * SUM(salary_max IS NOT NULL) / COUNT(*), 1) AS pct_with_salary
FROM naukri_jobs
GROUP BY source;

-- E4. Salary currency mix (data quality: confirms multi-currency scraped data)
SELECT salary_currency, COUNT(*) AS listings
FROM naukri_jobs
WHERE salary_currency IS NOT NULL
GROUP BY salary_currency
ORDER BY listings DESC;


-- ---------------------------------------------------------------------
-- CATEGORY F — TIME-BASED / FRESHNESS ANALYSIS
-- ---------------------------------------------------------------------

-- F1. Listings posted per day (recent posting trend)
SELECT date_posted, COUNT(*) AS listings
FROM naukri_jobs
WHERE date_posted IS NOT NULL
GROUP BY date_posted
ORDER BY date_posted DESC
LIMIT 15;

-- F2. Average listing "age" (days since posted) per source
SELECT source, ROUND(AVG(age_in_days), 1) AS avg_age_days, COUNT(*) AS listings
FROM naukri_jobs
WHERE age_in_days IS NOT NULL
GROUP BY source;

-- F3. Freshness buckets — how many listings are "new" vs "stale"
SELECT
    CASE
        WHEN age_in_days <= 7  THEN '0-7 days'
        WHEN age_in_days <= 14 THEN '8-14 days'
        WHEN age_in_days <= 30 THEN '15-30 days'
        ELSE '30+ days'
    END AS freshness_bucket,
    COUNT(*) AS listings
FROM naukri_jobs
WHERE age_in_days IS NOT NULL
GROUP BY freshness_bucket
ORDER BY MIN(age_in_days);

-- F4. Day-of-week posting pattern (which days do companies post most?)
SELECT DAYNAME(date_posted) AS day_of_week, COUNT(*) AS listings
FROM naukri_jobs
WHERE date_posted IS NOT NULL
GROUP BY day_of_week
ORDER BY listings DESC;


-- ---------------------------------------------------------------------
-- CATEGORY G — WINDOW FUNCTIONS & RANKING
-- ---------------------------------------------------------------------

-- G1. Rank companies within each source by number of listings (DENSE_RANK)
WITH company_counts AS (
    SELECT source, company_name, COUNT(*) AS listings
    FROM naukri_jobs
    WHERE company_name IS NOT NULL
    GROUP BY source, company_name
),
ranked AS (
    SELECT source, company_name, listings,
           DENSE_RANK() OVER (PARTITION BY source ORDER BY listings DESC) AS rank_in_source
    FROM company_counts
)
SELECT * FROM ranked WHERE rank_in_source <= 5;

-- G2. Rank job categories by average max salary using RANK()
SELECT job_category, avg_salary_max,
       RANK() OVER (ORDER BY avg_salary_max DESC) AS salary_rank
FROM (
    SELECT job_category, ROUND(AVG(salary_max), 0) AS avg_salary_max
    FROM naukri_jobs
    WHERE salary_max IS NOT NULL AND job_category IS NOT NULL
    GROUP BY job_category
    HAVING COUNT(*) >= 3
) t
ORDER BY salary_rank
LIMIT 15;

-- G3. NTILE — split all salaried listings into 4 salary quartile buckets
SELECT job_id, title, company_name, salary_max,
       NTILE(4) OVER (ORDER BY salary_max) AS salary_quartile
FROM naukri_jobs
WHERE salary_max IS NOT NULL
ORDER BY salary_max DESC
LIMIT 20;

-- G4. LAG/LEAD — compare each day's posting volume to the previous day
SELECT date_posted,
       COUNT(*) AS listings,
       LAG(COUNT(*)) OVER (ORDER BY date_posted)  AS prev_day_listings,
       LEAD(COUNT(*)) OVER (ORDER BY date_posted) AS next_day_listings
FROM naukri_jobs
WHERE date_posted IS NOT NULL
GROUP BY date_posted
ORDER BY date_posted;


-- ---------------------------------------------------------------------
-- CATEGORY H — ADVANCED ANALYTICS (CTEs, subqueries, cross-source)
-- ---------------------------------------------------------------------

-- H1. CTE — companies that appear on 2+ sources AND have above-average
--     salary_max (a "high-value multi-source employer" shortlist)
WITH multi_source_companies AS (
    SELECT company_name
    FROM naukri_jobs
    WHERE company_name IS NOT NULL
    GROUP BY company_name
    HAVING COUNT(DISTINCT source) > 1
),
avg_salary AS (
    SELECT AVG(salary_max) AS overall_avg FROM naukri_jobs WHERE salary_max IS NOT NULL
)
SELECT nj.company_name,
       ROUND(AVG(nj.salary_max), 0) AS avg_company_salary_max,
       COUNT(*) AS listings
FROM naukri_jobs nj
JOIN multi_source_companies msc ON nj.company_name = msc.company_name
CROSS JOIN avg_salary
WHERE nj.salary_max IS NOT NULL
GROUP BY nj.company_name
HAVING AVG(nj.salary_max) > (SELECT overall_avg FROM avg_salary)
ORDER BY avg_company_salary_max DESC
LIMIT 15;

-- H2. Subquery — job categories that pay above the overall average
--     max salary (a data-driven "which skills to target" view)
SELECT job_category, ROUND(AVG(salary_max), 0) AS avg_salary_max
FROM naukri_jobs
WHERE job_category IS NOT NULL AND salary_max IS NOT NULL
GROUP BY job_category
HAVING AVG(salary_max) > (
    SELECT AVG(salary_max) FROM naukri_jobs WHERE salary_max IS NOT NULL
)
ORDER BY avg_salary_max DESC
LIMIT 15;

-- H3. Keyword frequency mining from matched_keywords (which searched
--     skills matched most often across all listings)
SELECT
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(matched_keywords, ';', n.n), ';', -1)) AS keyword,
    COUNT(*) AS frequency
FROM naukri_jobs
JOIN (SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) n
    ON CHAR_LENGTH(matched_keywords)
       - CHAR_LENGTH(REPLACE(matched_keywords, ';', '')) >= n.n - 1
WHERE matched_keywords IS NOT NULL
GROUP BY keyword
HAVING keyword <> ''
ORDER BY frequency DESC
LIMIT 20;

-- H4. Cross-source comparison — average salary_max and listing volume
--     side by side per source, plus each source's share of total listings
SELECT
    source,
    COUNT(*) AS total_listings,
    ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM naukri_jobs), 1) AS pct_of_total,
    ROUND(AVG(salary_max), 0) AS avg_salary_max,
    ROUND(AVG(company_rating), 2) AS avg_company_rating
FROM naukri_jobs
GROUP BY source
ORDER BY total_listings DESC;

-- =====================================================================
-- END OF WORKBOOK
-- =====================================================================
SHOW VARIABLES LIKE 'secure_file_priv';