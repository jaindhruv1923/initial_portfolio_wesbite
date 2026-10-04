// Naukri Saaf — content script
// Scrapes visible job posting fields from LinkedIn / Naukri / Indeed / Glassdoor.
// No network calls. Pure DOM reading.

function text(el) {
  return el ? el.innerText.trim().replace(/\s+/g, " ") : "";
}

function firstMatch(selectors) {
  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el && text(el)) return el;
  }
  return null;
}

function findByHeadingText(headingText) {
  // Finds a heading matching headingText, returns the text of everything after it
  // up to the next heading-like element. Works for LinkedIn's split-pane
  // job-search-results view, where class names are less stable than the
  // standalone /jobs/view/ page.
  const headings = Array.from(document.querySelectorAll("h1, h2, h3, strong, b"));
  const heading = headings.find((h) => text(h).toLowerCase() === headingText.toLowerCase());
  if (!heading) return "";
  let node = heading.closest("section, div") || heading.parentElement;
  return node ? text(node) : "";
}

function scrapeLinkedIn() {
  const title = firstMatch([
    ".job-details-jobs-unified-top-card__job-title h1",
    ".jobs-unified-top-card__job-title h1",
    ".job-details-jobs-unified-top-card__job-title-link",
    ".top-card-layout__title",
    ".jobs-details__main-content h1",
    "h1"
  ]);
  const company = firstMatch([
    ".job-details-jobs-unified-top-card__company-name a",
    ".jobs-unified-top-card__company-name a",
    ".topcard__org-name-link",
    ".job-details-jobs-unified-top-card__company-name",
    ".jobs-unified-top-card__company-name"
  ]);
  const meta = firstMatch([
    ".job-details-jobs-unified-top-card__primary-description-container",
    ".jobs-unified-top-card__primary-description",
    ".topcard__flavor-row"
  ]);
  let desc = firstMatch([
    "#job-details",
    ".jobs-description__content",
    ".jobs-box__html-content",
    ".description__text",
    ".jobs-details__main-content"
  ]);
  let descText = text(desc);
  if (!descText) {
    // Split-pane search-results view (or other layout variants): anchor off whichever
    // description heading LinkedIn happens to render.
    for (const heading of ["About the job", "Job description", "About this job"]) {
      descText = findByHeadingText(heading);
      if (descText) break;
    }
  }
  return {
    portal: "LinkedIn",
    title: text(title),
    company: text(company),
    meta: text(meta),
    description: descText,
    url: location.href
  };
}

function scrapeNaukri() {
  const title = firstMatch([".styles_jd-header-title__rZwM1", "h1.jd-header-title", "h1"]);
  const company = firstMatch([
    ".styles_jd-header-comp-name__MvqAI a",
    ".jd-header-comp-name a",
    ".jd-header-comp-name"
  ]);
  const meta = firstMatch([".styles_jhc__jd-stats__KrIxK", ".jhc__stat"]);
  const desc = firstMatch([".styles_JDC__dang-inner-html__h0K4t", ".dang-inner-html"]);
  const salary = firstMatch([".styles_jhc__salary__jdfEC", ".salary"]);
  return {
    portal: "Naukri",
    title: text(title),
    company: text(company),
    meta: text(meta) + (salary ? " | " + text(salary) : ""),
    description: text(desc),
    url: location.href
  };
}

function scrapeIndeed() {
  const title = firstMatch([".jobsearch-JobInfoHeader-title", "h1"]);
  const company = firstMatch([
    '[data-testid="inlineHeader-companyName"]',
    ".jobsearch-InlineCompanyRating div"
  ]);
  const meta = firstMatch([
    '[data-testid="inlineHeader-companyLocation"]',
    ".jobsearch-JobInfoHeader-subtitle"
  ]);
  const desc = firstMatch(["#jobDescriptionText"]);
  return {
    portal: "Indeed",
    title: text(title),
    company: text(company),
    meta: text(meta),
    description: text(desc),
    url: location.href
  };
}

function scrapeGlassdoor() {
  const title = firstMatch([".JobDetails_jobTitle__Rw_gn", "h1"]);
  const company = firstMatch([".EmployerProfile_employerName__Xemli", ".employerName"]);
  const meta = firstMatch([".JobDetails_locationAndPay__XGFmY"]);
  const desc = firstMatch([".JobDetails_jobDescription__uW_fK", "#JobDescriptionContainer"]);
  return {
    portal: "Glassdoor",
    title: text(title),
    company: text(company),
    meta: text(meta),
    description: text(desc),
    url: location.href
  };
}

function genericFallback() {
  // Grab the largest text block on the page as a best-effort description.
  const candidates = Array.from(document.querySelectorAll("article, main, section, div"))
    .filter((el) => el.innerText && el.innerText.length > 400)
    .sort((a, b) => b.innerText.length - a.innerText.length);
  const desc = candidates[0] ? text(candidates[0]) : text(document.body).slice(0, 5000);
  return {
    portal: "Unknown",
    title: text(document.querySelector("h1")),
    company: "",
    meta: "",
    description: desc,
    url: location.href
  };
}

function scrapeJob() {
  const host = location.hostname;
  let data;
  if (host.includes("linkedin.com")) data = scrapeLinkedIn();
  else if (host.includes("naukri.com")) data = scrapeNaukri();
  else if (host.includes("indeed.com")) data = scrapeIndeed();
  else if (host.includes("glassdoor.")) data = scrapeGlassdoor();
  else data = genericFallback();

  // If the site-specific selectors came up empty (site redesigned), fall back.
  if (!data.title && !data.description) {
    const fb = genericFallback();
    data = { ...data, ...fb, portal: data.portal };
  }
  return data;
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "GET_JOB_DATA") {
    sendResponse(scrapeJob());
  }
  return true;
});
