(function () {
  if (window.__naukriSaafNlpLoaded) return; // already executed once in this realm
  window.__naukriSaafNlpLoaded = true;

// Naukri Saaf — local NLP utilities (pure JS, no API, no external libs)

const STOPWORDS = new Set(
  ("a an the and or but if then else for of to in on at by with from as is are was were be " +
   "been being this that these those it its into you your our we they he she will shall can " +
   "could should would may might must have has had do does did not no nor so such than too " +
   "very s t just don now etc via per role team work working experience years year strong " +
   "good excellent ability skills knowledge understanding looking candidate candidates job " +
   "position company about responsibilities requirements qualifications preferred required")
    .split(" ")
);

// Skill dictionary: canonical skill -> matcher terms (lowercase).
// Seeded from Dhruv's resume skill categories + common Data Analyst / Data Scientist JD vocabulary,
// so both "what I have" and "what the JD wants but I lack" can be detected.
const SKILL_DICTIONARY = {
  "Python": ["python"],
  "SQL": ["sql", "postgresql", "mysql", "mariadb", "t-sql", "pl/sql"],
  "R": [" r ", "r programming", "r language"],
  "Power BI": ["power bi", "powerbi", "pl-300"],
  "Excel": ["excel", "pivot table", "vlookup", "solver"],
  "Tableau": ["tableau"],
  "Streamlit": ["streamlit"],
  "Plotly": ["plotly"],
  "Chart.js": ["chart.js", "chartjs"],
  "DuckDB": ["duckdb"],
  "Pandas": ["pandas"],
  "NumPy": ["numpy"],
  "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
  "Statsmodels": ["statsmodels"],
  "SHAP": ["shap"],
  "Machine Learning": ["machine learning", "ml model", "predictive modeling", "predictive modelling"],
  "Statistical Analysis": ["statistical analysis", "statistics", "hypothesis testing", "a/b testing", "ab testing"],
  "Data Visualization": ["data visualization", "data visualisation", "dashboard", "dashboards"],
  "Data Cleaning": ["data cleaning", "data wrangling", "data mining", "etl"],
  "Business Intelligence": ["business intelligence", " bi "],
  "Git/GitHub": ["git", "github", "version control"],
  "Jupyter": ["jupyter", "google colab", "colab"],
  "VS Code": ["vs code", "visual studio code"],
  "Apify": ["apify", "web scraping", "scraping"],
  "Report Automation": ["report automation", "automated reporting", "reporting workflows"],
  "KPI Tracking": ["kpi", "key performance indicator"],
  "Communication": ["communication", "stakeholder", "cross-functional"],
  "Deep Learning": ["deep learning", "neural network", "tensorflow", "pytorch", "keras"],
  "NLP": ["natural language processing", "nlp", "text mining"],
  "Cloud": ["aws", "azure", "gcp", "google cloud", "cloud computing"],
  "Big Data": ["spark", "hadoop", "big data"],
  "APIs": ["rest api", "api integration"],
  "Forecasting": ["forecasting", "time series"],
};

function tokenize(str) {
  return (str || "")
    .toLowerCase()
    .replace(/[^a-z0-9+.# ]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 1 && !STOPWORDS.has(w));
}

function termFrequency(tokens) {
  const tf = {};
  for (const t of tokens) tf[t] = (tf[t] || 0) + 1;
  return tf;
}

function cosineSimilarity(textA, textB) {
  const tfA = termFrequency(tokenize(textA));
  const tfB = termFrequency(tokenize(textB));
  const allTerms = new Set([...Object.keys(tfA), ...Object.keys(tfB)]);
  let dot = 0, magA = 0, magB = 0;
  for (const term of allTerms) {
    const a = tfA[term] || 0;
    const b = tfB[term] || 0;
    dot += a * b;
    magA += a * a;
    magB += b * b;
  }
  if (magA === 0 || magB === 0) return 0;
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

function extractSkills(rawText) {
  const lower = " " + (rawText || "").toLowerCase() + " ";
  const found = [];
  for (const [canonical, matchers] of Object.entries(SKILL_DICTIONARY)) {
    if (matchers.some((m) => lower.includes(m))) found.push(canonical);
  }
  return found;
}

function compareSkills(jdText, resumeText) {
  const jdSkills = new Set(extractSkills(jdText));
  const resumeSkills = new Set(extractSkills(resumeText));
  const have = [...jdSkills].filter((s) => resumeSkills.has(s));
  const missing = [...jdSkills].filter((s) => !resumeSkills.has(s));
  return { jdSkills: [...jdSkills], resumeSkills: [...resumeSkills], have, missing };
}

// Exposed globally for sidepanel.js (no module bundler in a plain extension)
if (!window.NaukriSaafNLP) {
  window.NaukriSaafNLP = { tokenize, cosineSimilarity, extractSkills, compareSkills, SKILL_DICTIONARY };
}

})();
