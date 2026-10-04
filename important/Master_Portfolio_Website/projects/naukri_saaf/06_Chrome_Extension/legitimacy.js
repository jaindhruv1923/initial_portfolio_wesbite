(function () {
  if (window.__naukriSaafLegitLoaded) return; // already executed once in this realm
  window.__naukriSaafLegitLoaded = true;

// Naukri Saaf — legitimacy scorer
// Mirrors the signal set from the trained GBM ghost-job model (feature_importance_v3.csv,
// AUC 0.72). Signals computable from the single page you're viewing are scored directly.
// Signals that need live web/portal data (repost count, cross-platform duplicates, market
// salary comparison, application velocity) are flagged as "manual check" with a ready-made
// search link, since this extension makes no network/API calls.

// Raw importances from feature_importance_v3.csv
const MODEL_WEIGHTS = {
  days_live: 0.0984,
  listing_age_bucket: 0.0971,
  velocity_x_no_salary: 0.0767,
  employer_repost_count: 0.0691,
  desc_per_day: 0.0680,
  data_quality_score: 0.0628,
  description_length_words: 0.0579,
  posting_velocity_per_week: 0.0568,
  description_lexical_diversity: 0.0521,
  portal_ghost_baseline: 0.0504,
  company_data_completeness_score: 0.0477,
  keyword_stuffing_ratio: 0.0424,
  keyword_match_pct: 0.0409,
  salary_disclosed_num: 0.0370,
  applications_per_day: 0.0305,
  city_tier: 0.0296,
  experience_range: 0.0259,
  city_opportunity_score: 0.0210,
  salary_range_ratio: 0.0158,
  contact_bypass_flag: 0.0096,
  salary_vs_market_gap: 0.0060,
  remote_ambiguity_flag: 0.0027,
  urgency_language_score: 0.0011,
  cross_platform_duplicate_flag: 0.0005,
  glassdoor_salary_combo: 0.0001,
};

const TIER1_CITIES = ["delhi", "mumbai", "bangalore", "bengaluru", "chennai", "hyderabad", "pune", "kolkata", "gurugram", "gurgaon", "noida"];

const URGENCY_PHRASES = [
  "immediate joiner", "immediate joining", "urgent hiring", "urgently hiring",
  "apply now", "limited seats", "hiring fast", "join immediately", "fast hiring"
];

const CONTACT_BYPASS_PATTERNS = [
  /\bwhatsapp\b/i,
  /\b[a-z0-9._%+-]+@(gmail|yahoo|hotmail|outlook)\.com\b/i,
  /\bcall\s?\/?\s?whatsapp\b/i,
  /\b\+?\d{10,12}\b.{0,15}(whatsapp|call|contact)/i
];

function words(str) {
  return (str || "").trim().split(/\s+/).filter(Boolean);
}

function scoreSignal(key, status, note, value) {
  return { key, weight: MODEL_WEIGHTS[key] || 0, status, note, value };
}

// status: "good" (lowers risk), "bad" (raises risk), "neutral", "manual" (can't compute here)
function evaluateListing(job, resumeText) {
  const desc = job.description || "";
  const meta = job.meta || "";
  const combined = `${job.title} ${job.company} ${meta} ${desc}`;
  const wc = words(desc).length;
  const uniqueWords = new Set(words(desc.toLowerCase())).size;
  const lexicalDiversity = wc > 0 ? uniqueWords / wc : 0;

  const signals = [];

  // description_length_words
  if (wc === 0) {
    signals.push(scoreSignal("description_length_words", "manual", "Couldn't read a description on this page — verify manually.", wc));
  } else if (wc < 60) {
    signals.push(scoreSignal("description_length_words", "bad", `Very thin description (${wc} words). Ghost/low-quality posts are often skeletal.`, wc));
  } else if (wc < 150) {
    signals.push(scoreSignal("description_length_words", "neutral", `Short description (${wc} words).`, wc));
  } else {
    signals.push(scoreSignal("description_length_words", "good", `Reasonably detailed description (${wc} words).`, wc));
  }

  // description_lexical_diversity (proxy for keyword_stuffing_ratio too)
  if (wc >= 30 && lexicalDiversity < 0.35) {
    signals.push(scoreSignal("description_lexical_diversity", "bad", `Low lexical diversity (${(lexicalDiversity * 100).toFixed(0)}%) — reads repetitive/templated.`, lexicalDiversity));
    signals.push(scoreSignal("keyword_stuffing_ratio", "bad", "Repetition pattern suggests possible keyword stuffing.", lexicalDiversity));
  } else if (wc >= 30) {
    signals.push(scoreSignal("description_lexical_diversity", "good", `Healthy lexical diversity (${(lexicalDiversity * 100).toFixed(0)}%).`, lexicalDiversity));
    signals.push(scoreSignal("keyword_stuffing_ratio", "good", "No obvious keyword stuffing detected.", lexicalDiversity));
  } else {
    signals.push(scoreSignal("description_lexical_diversity", "manual", "Too little text to judge.", lexicalDiversity));
    signals.push(scoreSignal("keyword_stuffing_ratio", "manual", "Too little text to judge.", null));
  }

  // salary_disclosed_num
  const salaryMatch = combined.match(/(₹|rs\.?|inr|lpa|lakh)\s?[\d,.]+/i);
  if (salaryMatch) {
    signals.push(scoreSignal("salary_disclosed_num", "good", "Salary/compensation figure disclosed.", true));
  } else {
    signals.push(scoreSignal("salary_disclosed_num", "bad", "No salary figure disclosed anywhere on the listing.", false));
  }

  // salary_range_ratio — only if a range like "5-15 LPA" is present
  const rangeMatch = combined.match(/([\d.]+)\s?-\s?([\d.]+)\s?(lpa|lakh)/i);
  if (rangeMatch) {
    const lo = parseFloat(rangeMatch[1]), hi = parseFloat(rangeMatch[2]);
    const ratio = lo > 0 ? hi / lo : null;
    if (ratio && ratio > 2.5) {
      signals.push(scoreSignal("salary_range_ratio", "bad", `Salary range is suspiciously wide (${rangeMatch[0]}) — often a placeholder range.`, ratio));
    } else if (ratio) {
      signals.push(scoreSignal("salary_range_ratio", "good", `Salary range is reasonably tight (${rangeMatch[0]}).`, ratio));
    }
  } else {
    signals.push(scoreSignal("salary_range_ratio", "manual", "No salary range pattern found to check.", null));
  }

  // contact_bypass_flag
  const bypassHit = CONTACT_BYPASS_PATTERNS.some((re) => re.test(desc));
  signals.push(
    bypassHit
      ? scoreSignal("contact_bypass_flag", "bad", "Personal email/WhatsApp/phone contact pattern found — bypasses the portal's official application flow.", true)
      : scoreSignal("contact_bypass_flag", "good", "No personal-contact-bypass pattern found in the description.", false)
  );

  // urgency_language_score
  const urgencyHits = URGENCY_PHRASES.filter((p) => desc.toLowerCase().includes(p));
  signals.push(
    urgencyHits.length > 0
      ? scoreSignal("urgency_language_score", "bad", `Urgency language found: "${urgencyHits[0]}".`, urgencyHits)
      : scoreSignal("urgency_language_score", "good", "No high-pressure urgency language detected.", [])
  );

  // remote_ambiguity_flag
  const mentionsRemote = /remote/i.test(combined);
  const clarifiesRemote = /(fully remote|remote \(india\)|hybrid|on-?site|work from office)/i.test(combined);
  if (mentionsRemote && !clarifiesRemote) {
    signals.push(scoreSignal("remote_ambiguity_flag", "bad", "\"Remote\" mentioned without clarifying hybrid/onsite/fully-remote terms.", true));
  } else {
    signals.push(scoreSignal("remote_ambiguity_flag", "good", "Work-location terms are reasonably clear.", false));
  }

  // company_data_completeness_score
  if (!job.company) {
    signals.push(scoreSignal("company_data_completeness_score", "bad", "No company name could be read — check the listing directly.", false));
  } else {
    signals.push(scoreSignal("company_data_completeness_score", "good", `Company name present: ${job.company}.`, true));
  }

  // city_tier
  const cityHit = TIER1_CITIES.find((c) => combined.toLowerCase().includes(c));
  signals.push(
    cityHit
      ? scoreSignal("city_tier", "good", `Tier-1 city mentioned (${cityHit}).`, cityHit)
      : scoreSignal("city_tier", "neutral", "No recognizable Tier-1 Indian city found in the listing text.", null)
  );

  // experience_range
  const expMatch = combined.match(/(\d+)\s?-\s?(\d+)\s?(years|yrs)/i) || combined.match(/(\d+)\+?\s?(years|yrs)/i);
  signals.push(
    expMatch
      ? scoreSignal("experience_range", "good", `Experience requirement stated: "${expMatch[0]}".`, expMatch[0])
      : scoreSignal("experience_range", "neutral", "No explicit experience range found.", null)
  );

  // data_quality_score — composite proxy: has company + salary + decent length
  const completeness = [job.company, salaryMatch, wc > 100].filter(Boolean).length;
  signals.push(
    scoreSignal(
      "data_quality_score",
      completeness >= 3 ? "good" : completeness === 2 ? "neutral" : "bad",
      `Listing completeness: ${completeness}/3 core fields present (company, salary, adequate description).`,
      completeness
    )
  );

  // days_live / listing_age_bucket — try to parse "posted X days/weeks/months ago" or a date
  const ageMatch = combined.match(/posted\s+(\d+)\s?(day|days|week|weeks|month|months|hour|hours)\s+ago/i)
    || combined.match(/(\d+)\s?(day|days|week|weeks|month|months|hour|hours)\s+ago/i);
  if (ageMatch) {
    const n = parseInt(ageMatch[1], 10);
    const unit = ageMatch[2].toLowerCase();
    let daysLive = n;
    if (unit.startsWith("week")) daysLive = n * 7;
    if (unit.startsWith("month")) daysLive = n * 30;
    if (unit.startsWith("hour")) daysLive = 0;
    if (daysLive > 45) {
      signals.push(scoreSignal("days_live", "bad", `Listing has been live ~${daysLive} days — unusually long for a genuine, actively-filled role.`, daysLive));
      signals.push(scoreSignal("listing_age_bucket", "bad", "Falls in the 'stale listing' bucket.", daysLive));
    } else {
      signals.push(scoreSignal("days_live", "good", `Listing age looks normal (~${daysLive} days live).`, daysLive));
      signals.push(scoreSignal("listing_age_bucket", "good", "Falls in a normal freshness bucket.", daysLive));
    }
  } else {
    signals.push(scoreSignal("days_live", "manual", "Couldn't read a 'posted X ago' date on this page — check it manually on the listing.", null));
    signals.push(scoreSignal("listing_age_bucket", "manual", "Depends on days_live above.", null));
  }

  // keyword_match_pct — filled in by resume comparison, done in sidepanel.js and merged in
  // (placeholder here; sidepanel.js overwrites this entry after computing resume similarity)
  signals.push(scoreSignal("keyword_match_pct", "neutral", "Computed from your resume match (see Tab 2).", null));

  // Signals that genuinely need live web/portal data — can't compute from a single static page
  const manualKeys = [
    ["velocity_x_no_salary", "How fast this employer posts jobs, cross-referenced with pay transparency."],
    ["employer_repost_count", "How many times this employer has reposted this or similar roles."],
    ["desc_per_day", "How description text changes across this employer's repeated postings."],
    ["posting_velocity_per_week", "How many roles this employer posts per week."],
    ["portal_ghost_baseline", "This portal's overall historical ghost-listing rate."],
    ["applications_per_day", "Applicant volume/velocity on this specific posting."],
    ["city_opportunity_score", "General hiring-market health for this city/role combo."],
    ["salary_vs_market_gap", "How the stated (or typical) salary compares to market rate."],
    ["cross_platform_duplicate_flag", "Whether this exact listing is duplicated across other portals."],
    ["glassdoor_salary_combo", "Whether Glassdoor salary data matches what's advertised here."],
  ];
  for (const [key, note] of manualKeys) {
    signals.push(scoreSignal(key, "manual", note, null));
  }

  return signals;
}

function computeRiskScore(signals) {
  // Only score signals we could actually evaluate (skip "manual").
  const computed = signals.filter((s) => s.status === "good" || s.status === "bad" || s.status === "neutral");
  const totalWeight = computed.reduce((sum, s) => sum + s.weight, 0) || 1;
  const riskWeight = computed
    .filter((s) => s.status === "bad")
    .reduce((sum, s) => sum + s.weight, 0);
  const riskPct = Math.round((riskWeight / totalWeight) * 100);
  const coveragePct = Math.round(
    (computed.reduce((sum, s) => sum + s.weight, 0) /
      Object.values(MODEL_WEIGHTS).reduce((a, b) => a + b, 0)) * 100
  );
  return { riskPct, coveragePct };
}

function verdict(riskPct, coveragePct) {
  if (coveragePct < 35) {
    return { label: "Insufficient data", tone: "neutral", detail: "Too many high-weight signals (repost history, cross-platform duplicates, portal baseline) need a manual check before a verdict is reliable." };
  }
  if (riskPct >= 45) {
    return { label: "Likely ghost / low-quality", tone: "bad", detail: "Multiple high-weight red flags fired on signals your model weighs heavily." };
  }
  if (riskPct >= 22) {
    return { label: "Suspect — verify before investing time", tone: "warn", detail: "Some red flags present. Worth the manual checks below before applying seriously." };
  }
  return { label: "Looks genuine", tone: "good", detail: "Signals that could be computed from this page lean clean." };
}

function buildSearchLinks(job) {
  const q = encodeURIComponent(`${job.company}`);
  const qJob = encodeURIComponent(`${job.company} ${job.title}`);
  return {
    glassdoorReviews: `https://www.google.com/search?q=${q}+glassdoor+reviews`,
    ambitionBox: `https://www.google.com/search?q=${q}+ambitionbox+reviews`,
    linkedinCompany: `https://www.linkedin.com/search/results/companies/?keywords=${q}`,
    duplicatePosting: `https://www.google.com/search?q=${qJob}`,
    newsCheck: `https://www.google.com/search?q=${q}+news+funding`,
    nonPaymentCheck: `https://www.google.com/search?q=${q}+scam+OR+"did+not+pay"+OR+fraud`,
  };
}

if (!window.NaukriSaafLegitimacy) {
  window.NaukriSaafLegitimacy = { evaluateListing, computeRiskScore, verdict, buildSearchLinks, MODEL_WEIGHTS };
}

})();
