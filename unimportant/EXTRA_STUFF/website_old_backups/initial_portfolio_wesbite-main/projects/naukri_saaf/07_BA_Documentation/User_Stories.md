<div align="center">

![header](https://capsule-render.vercel.app/api?type=waving&color=0:4C1D95,100:B8860B&height=130&section=header&text=User%20Stories%20%26%20Acceptance%20Criteria&fontSize=26&fontColor=FAF8F4&animation=fadeIn&fontAlignY=48&desc=Naukri%20Saaf&descAlignY=78&descSize=15)

</div>

Format: `As a [role], I want [capability], so that [benefit]` — each with Gherkin-style acceptance criteria, the way a BA hands these to a dev team for sprint planning.

<br/>

## 🧑‍💻 Epic 1 — Job Seeker: Legitimacy Check

### US-01 — Read the listing I'm viewing
> **As a** job seeker, **I want** the extension to automatically read the job posting I'm currently viewing, **so that** I don't have to copy-paste anything.

```gherkin
Given I am on a job listing page on LinkedIn, Naukri, Indeed, or Glassdoor
When I click the ↻ refresh button in the side panel
Then the Overview tab shows the job title, company, and extracted skills within 2 seconds

Given the page's markup doesn't match any known site-specific selector
When I click ↻
Then the generic fallback returns the largest visible text block as the description
And the Overview tab still populates, rather than showing a blank error
```

<br/>

### US-02 — See a legitimacy risk score
> **As a** job seeker, **I want** a risk score for the listing I'm viewing, **so that** I can decide whether it's worth my time before applying.

```gherkin
Given a job listing has been read successfully
When I open the Legitimacy tab
Then I see a verdict label (e.g. "Looks genuine", "Suspect", "Likely ghost")
And a risk score out of 100
And the percentage of the model's total signal weight that could be computed from this page

Given fewer than 35% of the model's signal weight could be computed from this page
When I view the verdict
Then the label reads "Insufficient data" instead of a false-confidence verdict
```

<br/>

### US-03 — Know what the tool couldn't verify
> **As a** job seeker, **I want** to see which signals the tool couldn't check from this page alone, **so that** I know what to verify myself before trusting the score.

```gherkin
Given the Legitimacy tab has rendered
When I scroll to "Needs a manual check"
Then I see each unverifiable signal (e.g. employer repost count, application velocity)
And a one-click search link to help me verify it manually

Given a signal was computed directly from the page
When I view "Signals checked on this page"
Then I see its status (good/bad/neutral), its note, and its real model weight (%)
```

<br/>

## 🎯 Epic 2 — Job Seeker: Resume Fit

### US-04 — Save my resume once
> **As a** job seeker, **I want** to save my resume once, **so that** I don't have to re-enter it for every listing I check.

```gherkin
Given I have not yet saved a resume
When I paste text or upload a PDF/.txt file and click "Save resume"
Then my resume text is stored in chrome.storage.local
And a "✓ Saved locally" confirmation appears
And the text is never sent over the network

Given I upload a scanned-image PDF with no extractable text
When the extension attempts to parse it
Then I see an error asking me to paste the text instead, not a silent failure
```

<br/>

### US-05 — See my fit score for this specific listing
> **As a** job seeker, **I want** a 0–10 fit score against the listing I'm viewing, **so that** I know how well my resume matches before I invest time tailoring it.

```gherkin
Given I have a saved resume and an active job listing
When I open the Resume Match tab
Then I see a score from 0-10
And a list of skills I have that the posting wants
And a list of skills the posting wants that aren't in my resume
And 2-3 concrete, listing-specific next steps (not generic advice)

Given my score is 8 or above
When I view the advice list
Then it suggests reordering my resume to lead with the matched keywords

Given my score is below 5
When I view the advice list
Then it names the specific missing keywords and asks me to honestly assess transferable exposure
```

<br/>

## 📊 Epic 3 — Analyst: Dashboard Exploration

### US-06 — Explore ghost-detection results without writing code
> **As an** analyst (or recruiter evaluating this project), **I want** a dashboard covering the full model output, **so that** I can explore findings without touching the notebook.

```gherkin
Given the Streamlit dashboard is running
When I navigate the 7 tabs
Then I can view: Overview, Platforms, Ghost Detection, Employers, Model Performance, Cluster, and Explore
And each tab renders from the same underlying predictions_v3.csv / model artifacts

Given I am on the Model Performance tab
When I view model comparison
Then I see AUC, F1, Precision, and Recall for all 5 benchmarked models
```

<br/>

### US-07 — Understand employer-level risk patterns
> **As an** analyst, **I want** to see employers grouped by posting behavior, **so that** I can spot which companies post responsibly vs. which don't.

```gherkin
Given the Cluster tab is open
When I view the cluster breakdown
Then I see all 6 employer clusters with their ghost rate, average days live, and average repost count
And the "High-Risk Ghost Poster" cluster (1,361 employers, 32.8% ghost rate) is clearly distinguishable from lower-risk clusters
```

<br/>

## 🛠️ Epic 4 — Maintainer: Extensibility

### US-08 — Add a new job portal
> **As the** project maintainer, **I want** the content-script scraping logic isolated per portal, **so that** I can add a new portal without touching the scoring logic.

```gherkin
Given content.js has a scrapeX() function per portal plus a host-based dispatcher
When I add a new portal
Then I only need to write a new scrapeX() function and add its hostname to the dispatcher
And the legitimacy scoring and resume-match logic require no changes
```

<br/>

### US-09 — Retrain the model on fresh data
> **As the** project maintainer, **I want** the extension's signal weights sourced from a single exported file, **so that** retraining the model updates the extension automatically.

```gherkin
Given a new feature_importance_v3.csv is exported after retraining
When MODEL_WEIGHTS in legitimacy.js is regenerated from that file
Then every displayed weight percentage across the extension updates without touching UI code
```

<br/>

<div align="center"><i>NAUKRI SAAF · Dhruv Jain · <a href="./README.md">← back to index</a></i></div>
