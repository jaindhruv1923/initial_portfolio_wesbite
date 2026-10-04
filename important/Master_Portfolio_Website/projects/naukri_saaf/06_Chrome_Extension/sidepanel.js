(function () {
  if (window.__naukriSaafPanelInit) return; // panel script already ran once in this realm
  window.__naukriSaafPanelInit = true;

const { cosineSimilarity, compareSkills } = window.NaukriSaafNLP;
const { evaluateListing, computeRiskScore, verdict, buildSearchLinks } = window.NaukriSaafLegitimacy;

let currentJob = null;
let currentResume = "";

// ---------- Tabs ----------
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
  });
});

// ---------- Resume storage ----------
function loadResume() {
  chrome.storage.local.get(["resumeText"], (res) => {
    if (res.resumeText) {
      currentResume = res.resumeText;
      document.getElementById("resumeInput").value = res.resumeText;
      document.getElementById("resumeSavedNote").classList.remove("hidden");
    }
  });
}

document.getElementById("saveResumeBtn").addEventListener("click", () => {
  const val = document.getElementById("resumeInput").value.trim();
  currentResume = val;
  chrome.storage.local.set({ resumeText: val }, () => {
    document.getElementById("resumeSavedNote").classList.remove("hidden");
    if (currentJob) renderMatch();
  });
});

// ---------- Resume file upload (PDF via pdf.js, .txt via FileReader — both local, no network) ----------
if (window.pdfjsLib) {
  window.pdfjsLib.GlobalWorkerOptions.workerSrc = chrome.runtime.getURL("lib/pdfjs/pdf.worker.min.js");
}

function showUploadError(msg) {
  const el = document.getElementById("uploadError");
  if (!msg) {
    el.classList.add("hidden");
    el.textContent = "";
    return;
  }
  el.textContent = msg;
  el.classList.remove("hidden");
}

async function extractPdfText(arrayBuffer) {
  const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  let fullText = "";
  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const content = await page.getTextContent();
    const pageText = content.items.map((item) => item.str).join(" ");
    fullText += pageText + "\n";
  }
  return fullText.trim();
}

function saveResumeText(text) {
  currentResume = text;
  document.getElementById("resumeInput").value = text;
  chrome.storage.local.set({ resumeText: text }, () => {
    document.getElementById("resumeSavedNote").classList.remove("hidden");
    if (currentJob) renderMatch();
  });
}

document.getElementById("resumeFile").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  showUploadError(null);
  document.getElementById("uploadFileName").textContent = file.name;

  try {
    if (file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf")) {
      if (!window.pdfjsLib) {
        showUploadError("PDF reader failed to load. Try pasting the resume text instead.");
        return;
      }
      const arrayBuffer = await file.arrayBuffer();
      const text = await extractPdfText(arrayBuffer);
      if (!text || text.length < 20) {
        showUploadError(
          "Couldn't extract readable text from this PDF (it may be a scanned image, not real text). Try pasting the resume text instead."
        );
        return;
      }
      saveResumeText(text);
    } else if (file.type === "text/plain" || file.name.toLowerCase().endsWith(".txt")) {
      const text = await file.text();
      saveResumeText(text);
    } else {
      showUploadError("Only PDF and .txt files are supported right now — paste the text below instead.");
    }
  } catch (err) {
    showUploadError("Couldn't read that file (" + err.message + "). Try pasting the resume text instead.");
  }
});

// ---------- Get job data from content script ----------
function showStatus(msg, isError) {
  const el = document.getElementById("ov-empty");
  el.textContent = msg;
  el.style.color = isError ? "var(--bad)" : "";
  document.getElementById("ov-empty").classList.remove("hidden");
  document.getElementById("ov-data").classList.add("hidden");
}

function askContentScript(tabId, attempt) {
  chrome.tabs.sendMessage(tabId, { type: "GET_JOB_DATA" }, (job) => {
    if (chrome.runtime.lastError || !job) {
      if (attempt === 0) {
        // Most common cause: this tab was open before the extension loaded, so the
        // content script never auto-injected. Inject it manually, then retry once.
        chrome.scripting.executeScript(
          { target: { tabId }, files: ["content.js"] },
          () => {
            if (chrome.runtime.lastError) {
              showStatus(
                `Couldn't read this page (${chrome.runtime.lastError.message}). If this is a LinkedIn/Naukri/Indeed/Glassdoor job page, try a hard refresh (Ctrl/Cmd+R) then hit ↻ again.`,
                true
              );
              return;
            }
            setTimeout(() => askContentScript(tabId, 1), 150);
          }
        );
      } else {
        showStatus(
          "Couldn't read this page. Make sure you're on a job posting (LinkedIn/Naukri/Indeed/Glassdoor), refresh the tab, then click ↻ again.",
          true
        );
      }
      return;
    }
    currentJob = job;
    if (!job.title && !job.description) {
      showStatus(
        `Page responded but no job title/description text was found (portal detected: ${job.portal}). The site's layout may have changed — try opening the job in its own dedicated page rather than a search-results split view.`,
        true
      );
      return;
    }
    renderOverview();
    renderMatch();
    renderLegitimacy();
  });
}

function refresh() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    if (!tab || !tab.id) return;
    askContentScript(tab.id, 0);
  });
}
document.getElementById("refreshBtn").addEventListener("click", refresh);

// ---------- Overview tab ----------
function renderOverview() {
  if (!currentJob || (!currentJob.title && !currentJob.description)) return;
  document.getElementById("ov-empty").classList.add("hidden");
  document.getElementById("ov-data").classList.remove("hidden");

  document.getElementById("ov-title").textContent = currentJob.title || "(title not found)";
  document.getElementById("ov-company").textContent = currentJob.company || "Unknown company";
  document.getElementById("ov-portal").textContent = currentJob.portal;
  document.getElementById("ov-meta").textContent = currentJob.meta || "";
  document.getElementById("ov-desc").textContent = currentJob.description || "(no description text found on this page)";

  const skills = window.NaukriSaafNLP.extractSkills(currentJob.description || `${currentJob.title} ${currentJob.meta}`);
  const skillsEl = document.getElementById("ov-skills");
  skillsEl.innerHTML = "";
  if (skills.length === 0) {
    skillsEl.innerHTML = `<span>No dictionary skills detected — description may be image-based or non-standard.</span>`;
  } else {
    skills.forEach((s) => {
      const chip = document.createElement("span");
      chip.textContent = s;
      skillsEl.appendChild(chip);
    });
  }
}

// ---------- Resume Match tab ----------
function renderMatch() {
  if (!currentResume) {
    document.getElementById("match-empty").classList.remove("hidden");
    document.getElementById("match-data").classList.add("hidden");
    return;
  }
  if (!currentJob || !currentJob.description) {
    document.getElementById("match-empty").classList.remove("hidden");
    document.getElementById("match-data").classList.add("hidden");
    return;
  }
  document.getElementById("match-empty").classList.add("hidden");
  document.getElementById("match-data").classList.remove("hidden");

  const jdText = `${currentJob.title} ${currentJob.description}`;
  const textSim = cosineSimilarity(currentResume, jdText); // roughly 0 - 0.5 in practice
  const { have, missing, jdSkills } = compareSkills(jdText, currentResume);
  const skillRatio = jdSkills.length > 0 ? have.length / jdSkills.length : 0.5;

  const blended = 0.6 * skillRatio + 0.4 * Math.min(1, textSim * 2.5);
  const score10 = Math.max(0, Math.min(10, Math.round(blended * 10)));

  document.getElementById("matchScoreNum").textContent = score10;

  let band, advice;
  if (score10 >= 8) {
    band = "Strong fit.";
    advice = [
      `Lead your resume summary/objective with the ${have.slice(0, 3).join(", ") || "matched"} keywords — they're the first thing an ATS and a recruiter's eye will match on.`,
      missing.length
        ? `You're missing "${missing[0]}" as an explicit keyword — if you've touched it even informally, add one bullet naming it.`
        : `Your keyword coverage is already close to complete for this posting — don't add filler, just make sure ordering puts the strongest overlap first.`,
      `Reorder your Skills section so the categories matching this JD's language come first, not last.`
    ];
  } else if (score10 >= 5) {
    band = "Moderate fit — worth tailoring before applying.";
    advice = [
      missing.length
        ? `Missing keywords this posting cares about: ${missing.slice(0, 4).join(", ")}. If you have real (even project-level) exposure to any of these, add a bullet naming the tool explicitly — don't just imply it.`
        : `Skill overlap is fine, but the phrasing in your resume doesn't closely echo this JD's language — mirror 2-3 of its exact terms.`,
      `Move your ${have[0] || "most relevant"} project bullet higher in the Projects section since it's your strongest overlap with this specific role.`,
      `Consider a one-line tailored objective sentence naming the company and the specific tool stack this JD lists.`
    ];
  } else {
    band = "Weak fit as written.";
    advice = [
      `Large keyword gap: ${missing.slice(0, 5).join(", ") || "core requirements"} aren't showing up in your resume text at all.`,
      `Before applying, decide honestly whether you have transferable exposure to these — if not, this role may be reaching past your current stack.`,
      `If you still want to apply, use the cover letter/note to explicitly bridge the gap (e.g. "haven't used X in production, but built Y using the same underlying concept").`
    ];
  }
  document.getElementById("matchBand").textContent = band;

  const haveEl = document.getElementById("skillsHave");
  haveEl.innerHTML = have.length
    ? have.map((s) => `<span>${s}</span>`).join("")
    : `<span>No direct overlap found.</span>`;

  const missEl = document.getElementById("skillsMissing");
  missEl.innerHTML = missing.length
    ? missing.map((s) => `<span>${s}</span>`).join("")
    : `<span>None — full skill coverage.</span>`;

  const adviceEl = document.getElementById("matchAdvice");
  adviceEl.innerHTML = advice.map((a) => `<li>${a}</li>`).join("");

  // feed keyword_match_pct back into the legitimacy tab's model-weight signal
  window._lastMatchPct = jdSkills.length > 0 ? Math.round((have.length / jdSkills.length) * 100) : null;
  if (currentJob) renderLegitimacy();
}

// ---------- Legitimacy tab ----------
function renderLegitimacy() {
  if (!currentJob || (!currentJob.title && !currentJob.description)) return;
  document.getElementById("legit-empty").classList.add("hidden");
  document.getElementById("legit-data").classList.remove("hidden");

  let signals = evaluateListing(currentJob, currentResume);

  if (window._lastMatchPct !== undefined && window._lastMatchPct !== null) {
    signals = signals.map((s) =>
      s.key === "keyword_match_pct"
        ? { ...s, status: "neutral", note: `Your resume overlaps ${window._lastMatchPct}% of detected JD skills (see Resume Match tab).` }
        : s
    );
  }

  const { riskPct, coveragePct } = computeRiskScore(signals);
  const v = verdict(riskPct, coveragePct);

  const vEl = document.getElementById("legitVerdict");
  vEl.className = `verdict-box ${v.tone}`;
  vEl.textContent = `${v.label} — risk score ${riskPct}/100`;
  document.getElementById("legitCoverage").textContent =
    `${v.detail} (${coveragePct}% of the model's signal weight could be computed directly from this page.)`;

  const computedEl = document.getElementById("legitComputed");
  const manualEl = document.getElementById("legitManual");
  computedEl.innerHTML = "";
  manualEl.innerHTML = "";

  signals
    .sort((a, b) => b.weight - a.weight)
    .forEach((s) => {
      const row = document.createElement("div");
      row.className = "signal-row";
      const dotClass =
        s.status === "good" ? "dot-good" : s.status === "bad" ? "dot-bad" : s.status === "manual" ? "dot-manual" : "dot-neutral";
      row.innerHTML = `
        <div class="signal-dot ${dotClass}"></div>
        <div class="signal-body">
          <div class="signal-title">${prettyName(s.key)} <span class="signal-weight">(${(s.weight * 100).toFixed(1)}% model weight)</span></div>
          <div class="signal-note">${s.note}</div>
        </div>`;
      if (s.status === "manual") manualEl.appendChild(row);
      else computedEl.appendChild(row);
    });

  const links = buildSearchLinks(currentJob);
  const linkEl = document.getElementById("legitLinks");
  linkEl.innerHTML = `
    <a href="${links.glassdoorReviews}" target="_blank">Search Glassdoor reviews for ${currentJob.company || "this company"}</a>
    <a href="${links.ambitionBox}" target="_blank">Search AmbitionBox reviews</a>
    <a href="${links.linkedinCompany}" target="_blank">View company on LinkedIn</a>
    <a href="${links.duplicatePosting}" target="_blank">Check for duplicate/reposted listings</a>
    <a href="${links.newsCheck}" target="_blank">Search recent news/funding</a>
    <a href="${links.nonPaymentCheck}" target="_blank">Search for scam / non-payment complaints</a>
  `;
}

function prettyName(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

// ---------- Init ----------
loadResume();
refresh();

// Auto re-read when the user switches to a different tab...
chrome.tabs.onActivated.addListener(() => {
  setTimeout(refresh, 200);
});
// ...or when the current tab finishes loading/navigating (e.g. clicking a new job card).
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if ((changeInfo.status === "complete" || changeInfo.url) && tab.active) {
    setTimeout(refresh, 200);
  }
});
// ...or, as a safety net: LinkedIn is a single-page app, and clicking a different job
// card in the list often updates the URL via history.pushState without firing a full
// 'complete' tab-update event. Poll periodically so those clicks still get picked up.
let lastPolledUrl = null;
setInterval(() => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    if (!tab) return;
    if (tab.url !== lastPolledUrl) {
      lastPolledUrl = tab.url;
      refresh();
    }
  });
}, 2000);

})();
