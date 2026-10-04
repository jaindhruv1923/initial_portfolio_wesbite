# Human Annotation Rubric for Naukri Saaf Gold Benchmark

This rubric guides the manual verification of 80 job listings in [`data/BLIND_LABELING_SHEET_80.csv`](file:///c:/Users/jaind/Desktop/Project-Naukri-Saaf-Job-Listings-Analysis-main/data/BLIND_LABELING_SHEET_80.csv).

The goal is to create a genuine human-verified ground-truth test set (`GOLD_LABELS_DONE.csv`) that can be defended in technical interviews without circularity or machine-label bias.

---

## 1. Sheet Overview

Open [`data/BLIND_LABELING_SHEET_80.csv`](file:///c:/Users/jaind/Desktop/Project-Naukri-Saaf-Job-Listings-Analysis-main/data/BLIND_LABELING_SHEET_80.csv) in Excel, VS Code, or any CSV editor.

You will see 11 columns:
- `id`: Unique identifier (do not edit).
- `platform`: Source job portal (LinkedIn, Indeed, Glassdoor).
- `company`: Stated hiring organization.
- `title`: Job title.
- `location`: Stated work location.
- `listing_url`: The exact live link to the job posting.
- **`on_company_careers_page`**: *(To be filled by you)*
- **`still_live`**: *(To be filled by you)*
- **`duplicate_or_reposted`**: *(To be filled by you)*
- **`label`**: *(To be filled by you: `real`, `unclear`, `ghost`)*
- **`notes`**: *(To be filled by you: brief reason)*

---

## 2. Step-by-Step Verification Procedure

For each row, perform three quick checks taking 60–90 seconds per listing:

### Check A: Is the Listing URL Still Live? (`still_live`)
- Click the `listing_url` to open it in your browser.
- **`yes`**: The page loads and actively accepts applications.
- **`no`**: The page returns a 404, error, or redirects to homepage.
- **`expired`**: The page loads, but shows "No longer accepting applications", "Job expired", or "Closed".

### Check B: Is it on the Official Company Careers Portal? (`on_company_careers_page`)
- Search Google: `"<Company Name>" careers "<Job Title>"` or navigate to the company's official website careers section.
- **`yes`**: You find an active matching job requisition on their official corporate domain (e.g. `careers.company.com`, `boards.greenhouse.io/company`, `jobs.lever.co/company`).
- **`no`**: The company exists, has an active careers portal, but has no record of this opening.
- **`unverifiable`**: Small agency, unlisted startup, or company lacks a public careers site.

### Check C: Is it a Duplicate / Serial Repost? (`duplicate_or_reposted`)
- Search Google: `"<Company Name>" "<Job Title>" "job"` or copy a unique sentence from the description into Google in quotes.
- **`yes`**: You find the identical description posted across multiple random platforms, or multiple postings reposted repeatedly over several months.
- **`no`**: Appears to be a unique, standard active requisition.
- **`suspected`**: Common boilerplate description used across generic recruitment portals.

---

## 3. Decision Rules for the `label` Column

Assign one of three values:

| Label | Criteria |
| :--- | :--- |
| **`real`** | Verified legitimate opening. Confirmed on company careers page, or active on portal with clear company identity, specific responsibilities, realistic requirements, and standard application flow. |
| **`ghost`** | Strong indicators of deceptive or inactive opening: (a) Listed on third-party portal but completely absent on official careers site, (b) Generic agency resume farming ("building pipeline for future clients"), (c) Contact bypass asking for WhatsApp/personal Gmail, (d) Expired/dormant listing repeatedly refreshed without hiring, or (e) Impossible requirements / generic spam. |
| **`unclear`** | Insufficient public information to confirm or refute legitimacy (e.g. stealth startup, third-party recruitment firm with unnamed enterprise client). |

---

## 4. Example Annotations

| company | title | on_company_careers_page | still_live | duplicate_or_reposted | label | notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| CrowdStrike | Senior Analyst | yes | yes | no | **`real`** | Found active matching req on crowdstrike.com/careers. |
| TechStaff India | Python Dev | no | expired | yes | **`ghost`** | Agency posting, asks for resume to gmail, no actual client named. |
| Stealth AI | Data Scientist | unverifiable | yes | no | **`unclear`** | Seed startup, no public ATS portal yet, but genuine founders on LinkedIn. |

---

## 5. Submission

Once you have annotated the 80 rows:
1. Save your completed file as:
   `data/GOLD_LABELS_DONE.csv`
2. Stop and notify the agent. We will then run our evaluation script against your actual verified human ground truth!
