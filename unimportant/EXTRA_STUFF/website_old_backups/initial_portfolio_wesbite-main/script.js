// ============================================================
// DHRUV JAIN — PORTFOLIO SCRIPT ENGINE
// Powers: Loader, Scroll, Glow, Counters, SQL Lab, Filters, Lightbox
// ============================================================

// ---------- Page loader ----------
function dismissLoader() {
  const loader = document.getElementById("loader");
  if (loader && !loader.classList.contains("done")) {
    loader.classList.add("done");
  }
}
window.addEventListener("load", () => setTimeout(dismissLoader, 150));
document.addEventListener("DOMContentLoaded", () => setTimeout(dismissLoader, 500));
setTimeout(dismissLoader, 900); // Guarantee loader never hangs if external CDN is slow

// ---------- Scroll Scrub Bar & Parallax Storytelling (Slide 01) ----------
function initScrollStorytelling() {
  const scrubBar = document.getElementById("scroll-scrub-bar") || document.getElementById("scroll-progress");
  const navSwitcherBtns = document.querySelectorAll(".nav-switch-btn");
  const sections = document.querySelectorAll("header.hero, section[id]");

  let ticking = false;

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const scrollY = window.scrollY || window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;

        // 1. Scrub Progress Bar
        if (scrubBar && docHeight > 0) {
          const scrollPct = Math.min(100, Math.max(0, (scrollY / docHeight) * 100));
          scrubBar.style.width = `${scrollPct}%`;
        }

        // 2. Parallax Layers
        if (window.innerWidth > 800) {
          document.querySelectorAll(".parallax-layer").forEach((layer) => {
            const speed = parseFloat(layer.getAttribute("data-parallax-speed") || "0.06");
            if (scrollY < 1200) {
              layer.style.transform = `translate3d(0, ${scrollY * speed}px, 0)`;
            }
          });
        }

        // 3. Scroll-Spy for Segmented Dock
        let currentSectionId = "about";
        sections.forEach((sec) => {
          const top = sec.offsetTop - 120;
          const height = sec.offsetHeight;
          if (scrollY >= top && scrollY < top + height) {
            currentSectionId = sec.getAttribute("id") || "about";
          }
        });

        navSwitcherBtns.forEach((btn) => {
          const target = btn.getAttribute("data-nav") || (btn.getAttribute("href") || "").replace("#", "");
          if (target === currentSectionId) {
            btn.classList.add("active");
          } else {
            btn.classList.remove("active");
          }
        });

        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}
initScrollStorytelling();

// ---------- Reveal on Scroll & Stagger (Slide 02) ----------
function initScrollReveals() {
  const targets = document.querySelectorAll(".reveal-on-scroll, .stagger-container, .reveal");
  if (!("IntersectionObserver" in window)) {
    targets.forEach((el) => {
      el.classList.add("is-revealed");
      el.classList.add("in");
    });
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-revealed");
        entry.target.classList.add("in");
      }
    });
  }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });

  targets.forEach((el, i) => {
    el.style.setProperty("--d", (i % 4) * 60 + "ms");
    observer.observe(el);
  });
}
initScrollReveals();

if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.querySelectorAll(".reveal, .reveal-on-scroll, .stagger-container").forEach((el) => {
    el.classList.add("is-revealed");
    el.classList.add("in");
  });
}

// ---------- Cursor Glow & Spotlight Cards (Slide 03) ----------
const glow = document.getElementById("cursor-glow");
if (glow) {
  window.addEventListener("mousemove", (e) => {
    glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`;
  });
}

// Cult UI / Aceternity Spotlight Card Effect
function initSpotlightCards() {
  const spotlightCards = document.querySelectorAll(".spotlight-card, .project-card, .hero-kpi, .artifact-card, .cert-card, .pillar-card");
  spotlightCards.forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty("--mouse-x", `${x}px`);
      card.style.setProperty("--mouse-y", `${y}px`);
      card.style.setProperty("--mx", `${(x / rect.width) * 100}%`);
      card.style.setProperty("--my", `${(y / rect.height) * 100}%`);
    });
  });
}
initSpotlightCards();

// ---------- Magnetic Buttons (Excluding tight nav-switchers) ----------
function initMagneticButtons() {
  const magneticBtns = document.querySelectorAll(".magnetic-btn, .btn-serious-lg, .btn-secondary-lg, .cert-open");
  magneticBtns.forEach((btn) => {
    btn.addEventListener("mousemove", (e) => {
      const rect = btn.getBoundingClientRect();
      const x = (e.clientX - rect.left - rect.width / 2) * 0.18;
      const y = (e.clientY - rect.top - rect.height / 2) * 0.18;
      btn.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      btn.style.transition = "transform 0.08s ease-out";
    });

    btn.addEventListener("mouseleave", () => {
      btn.style.transform = "translate3d(0, 0, 0)";
      btn.style.transition = "transform 0.38s cubic-bezier(0.34, 1.56, 0.64, 1)";
    });
  });
}
initMagneticButtons();

// ---------- Dynamic Click Ripple & Press-Spring (Slide 04) ----------
function initClickRipple() {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("button, .btn, .btn-serious, .nav-switch-btn, .cb-tool-btn, .nav-cta");
    if (!btn) return;

    const rect = btn.getBoundingClientRect();
    const circle = document.createElement("span");
    const diameter = Math.max(rect.width, rect.height);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - rect.left - radius}px`;
    circle.style.top = `${e.clientY - rect.top - radius}px`;
    circle.classList.add("click-ripple");

    const existing = btn.querySelector(".click-ripple");
    if (existing) existing.remove();

    btn.appendChild(circle);
    setTimeout(() => circle.remove(), 600);
  });
}
initClickRipple();

// ---------- Animated counters ----------
function animateCount(el) {
  const raw = el.getAttribute("data-count");
  const suffix = el.getAttribute("data-suffix") || "";
  const prefix = el.getAttribute("data-prefix") || "";
  const numeric = parseFloat(raw.replace(/,/g, ""));
  if (isNaN(numeric)) return;
  const decimals = (raw.split(".")[1] || "").length;
  const duration = 1200;
  const start = performance.now();
  function step(now) {
    const p = Math.min(1, (now - start) / duration);
    const eased = 1 - Math.pow(1 - p, 3);
    const val = numeric * eased;
    el.textContent = prefix + val.toLocaleString("en-IN", { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
const countIO = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        countIO.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.3 }
);
document.querySelectorAll("[data-count]").forEach((el) => countIO.observe(el));

// ---------- Headline typewriter effect ----------
const scrambleTargets = document.querySelectorAll("[data-scramble]");
function typewrite(el) {
  const final = el.textContent;
  el.textContent = "";
  const cursor = document.createElement("span");
  cursor.textContent = "|";
  cursor.style.cssText = "color:var(--gold); animation: blink 0.9s step-end infinite; font-weight: 400;";
  el.appendChild(cursor);

  let i = 0;
  const speed = 28;
  function tick() {
    if (i < final.length) {
      cursor.insertAdjacentText("beforebegin", final[i]);
      i++;
      setTimeout(tick, speed);
    } else {
      cursor.remove();
    }
  }
  tick();
}
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  scrambleTargets.forEach((el) => setTimeout(() => typewrite(el), 350));
}

// ============================================================
// INTERACTIVE SQL BENCHMARK LAB DATA & RUNNER
// ============================================================
const SQL_DATA = {
  profitara: {
    comment: "-- Profitara Retail Analytics: Isolating high-value accounts at severe churn risk",
    query: `<span class="sql-keyword">SELECT</span> customer_id, segment_cluster, total_spend_inr, predicted_clv, churn_probability, action_recommendation<br>` +
           `<span class="sql-keyword">FROM</span> v_customer_clv_risk<br>` +
           `<span class="sql-keyword">WHERE</span> churn_probability &gt; <span class="sql-function">0.65</span> <span class="sql-keyword">AND</span> total_spend_inr &gt; <span class="sql-function">25000</span><br>` +
           `<span class="sql-keyword">ORDER BY</span> total_spend_inr <span class="sql-keyword">DESC</span><br>` +
           `<span class="sql-keyword">LIMIT</span> <span class="sql-function">5</span>;`,
    time: "14.8ms",
    headers: ["customer_id", "segment_cluster", "total_spend_inr", "predicted_clv", "churn_probability", "action_recommendation"],
    rows: [
      ["<code>CUST-10492</code>", "Champion (Cluster 3)", "₹84,250.00", "₹1,42,100.00", "<span class='status-pill danger'>0.82 (High)</span>", "<span class='status-pill warning'>Priority Win-Back Concierge</span>"],
      ["<code>CUST-10819</code>", "Loyal High-Spender", "₹62,110.00", "₹98,400.00", "<span class='status-pill danger'>0.76 (High)</span>", "<span class='status-pill warning'>Custom Renewal Incentive</span>"],
      ["<code>CUST-11204</code>", "At-Risk Wholesale", "₹49,870.00", "₹74,500.00", "<span class='status-pill danger'>0.71 (High)</span>", "<span class='status-pill warning'>Dedicated Account Call</span>"],
      ["<code>CUST-11755</code>", "Frequent Buyer", "₹38,920.00", "₹58,200.00", "<span class='status-pill danger'>0.69 (High)</span>", "<span class='status-pill info'>Targeted Push Notification</span>"],
      ["<code>CUST-12011</code>", "Core Spender", "₹31,450.00", "₹46,900.00", "<span class='status-pill danger'>0.67 (High)</span>", "<span class='status-pill info'>Automated Win-Back Voucher</span>"]
    ]
  },
  naukri: {
    comment: "-- Naukri Saaf Intelligence: Cross-portal ghost job distribution and median listing age",
    query: `<span class="sql-keyword">SELECT</span> portal_name, <span class="sql-function">COUNT</span>(*) <span class="sql-keyword">AS</span> total_listings, <span class="sql-function">ROUND</span>(<span class="sql-function">AVG</span>(ghost_probability)*<span class="sql-function">100</span>, <span class="sql-function">1</span>) <span class="sql-keyword">AS</span> ghost_rate_pct,<br>` +
           `       <span class="sql-function">ROUND</span>(<span class="sql-function">AVG</span>(days_live), <span class="sql-function">1</span>) <span class="sql-keyword">AS</span> avg_days_open, primary_ghost_indicator<br>` +
           `<span class="sql-keyword">FROM</span> job_listings_staging<br>` +
           `<span class="sql-keyword">GROUP BY</span> portal_name, primary_ghost_indicator<br>` +
           `<span class="sql-keyword">ORDER BY</span> ghost_rate_pct <span class="sql-keyword">DESC</span>;`,
    time: "18.2ms",
    headers: ["portal_name", "total_listings", "ghost_rate_pct", "avg_days_open", "primary_ghost_indicator"],
    rows: [
      ["<code>Glassdoor India</code>", "951", "34.2%", "63.8 days", "<span class='status-pill danger'>Stale Unmonitored Pipeline</span>"],
      ["<code>LinkedIn Jobs</code>", "1,000", "28.1%", "37.2 days", "<span class='status-pill warning'>Continuous Repost Without Hires</span>"],
      ["<code>Indeed India</code>", "900", "25.6%", "0.3 days", "<span class='status-pill info'>Opaque Salary / Employer Ambiguity</span>"]
    ]
  },
  kavach: {
    comment: "-- KAVACH Security Engine: Automated CI gate telemetry and PII scanner evaluation log",
    query: `<span class="sql-keyword">SELECT</span> scan_id, identifier_type, pattern_rule, precision_score, recall_score, f1_score, gate_status<br>` +
           `<span class="sql-keyword">FROM</span> security_audit_log<br>` +
           `<span class="sql-keyword">WHERE</span> test_corpus_size = <span class="sql-function">42</span><br>` +
           `<span class="sql-keyword">ORDER BY</span> scan_id <span class="sql-keyword">ASC</span>;`,
    time: "11.5ms",
    headers: ["scan_id", "identifier_type", "pattern_rule", "precision_score", "recall_score", "f1_score", "gate_status"],
    rows: [
      ["<code>SCAN-001</code>", "Aadhaar Number", "Verhoeff Algorithm Checksum", "1.00", "1.00", "<span class='status-pill success'>1.00 F1</span>", "<span class='status-pill success'>PASS / BLOCKED</span>"],
      ["<code>SCAN-002</code>", "Permanent Account (PAN)", "5 Alpha + 4 Digit + 1 Alpha", "1.00", "1.00", "<span class='status-pill success'>1.00 F1</span>", "<span class='status-pill success'>PASS / BLOCKED</span>"],
      ["<code>SCAN-003</code>", "Indian Mobile Formats", "+91 / Standard 10-Digit RFC", "1.00", "1.00", "<span class='status-pill success'>1.00 F1</span>", "<span class='status-pill success'>PASS / BLOCKED</span>"],
      ["<code>SCAN-004</code>", "Enterprise API Secrets", "High-Entropy Hex / Bearer Keys", "1.00", "1.00", "<span class='status-pill success'>1.00 F1</span>", "<span class='status-pill success'>PASS / BLOCKED</span>"],
      ["<code>SCAN-005</code>", "AST Dependency Graph", "Acyclic Call-Graph Blast Radius", "0.74", "0.70", "<span class='status-pill info'>0.72 F1</span>", "<span class='status-pill success'>PASS / AUDITED</span>"]
    ]
  },
  udaghosh: {
    comment: "-- Udaghosh Operations: Social welfare program KPIs and volunteer allocation variance",
    query: `<span class="sql-keyword">SELECT</span> program_name, beneficiary_reach, active_volunteers, target_completion_pct, q3_variance_pct<br>` +
           `<span class="sql-keyword">FROM</span> v_udaghosh_ops_kpis<br>` +
           `<span class="sql-keyword">ORDER BY</span> beneficiary_reach <span class="sql-keyword">DESC</span>;`,
    time: "16.1ms",
    headers: ["program_name", "beneficiary_reach", "active_volunteers", "target_completion_pct", "q3_variance_pct"],
    rows: [
      ["<code>Rural Education Drive</code>", "4,250 students", "68 volunteers", "98.4%", "<span class='status-pill success'>+12.4% vs Target</span>"],
      ["<code>Nutrition & Food Relief</code>", "8,920 families", "112 volunteers", "102.1%", "<span class='status-pill success'>+18.7% vs Target</span>"],
      ["<code>Health & Sanitation Camps</code>", "3,100 citizens", "45 volunteers", "94.2%", "<span class='status-pill success'>+6.5% vs Target</span>"],
      ["<code>Digital Literacy Workshops</code>", "1,850 youth", "32 volunteers", "91.0%", "<span class='status-pill info'>+3.2% vs Target</span>"]
    ]
  },
  archon: {
    comment: "-- Archon AI Evaluation: Empirical LLM benchmark correctness and latency comparison (Lab 4, N=78)",
    query: `<span class="sql-keyword">SELECT</span> evaluated_model, param_size_b, <span class="sql-function">ROUND</span>(avg_correctness*<span class="sql-function">100</span>, <span class="sql-function">1</span>) <span class="sql-keyword">AS</span> correctness_pct,<br>` +
           `       avg_latency_sec, code_pass_rate_pct, total_hallucinations, local_judge_cost_usd<br>` +
           `<span class="sql-keyword">FROM</span> v_llm_benchmark_evaluation<br>` +
           `<span class="sql-keyword">ORDER BY</span> avg_correctness <span class="sql-keyword">DESC</span>;`,
    time: "9.4ms",
    headers: ["evaluated_model", "param_size_b", "correctness_pct", "avg_latency_sec", "code_pass_rate_pct", "total_hallucinations", "local_judge_cost_usd"],
    rows: [
      ["<code>gemma3:4b (Google)</code>", "4.3B", "<span class='status-pill success'>71.2% (Champion)</span>", "15.75s", "66.7%", "5 / 26", "$0.00 (Local CoT)"],
      ["<code>codellama:7b (Meta)</code>", "7.0B", "<span class='status-pill warning'>45.8%</span>", "25.09s", "<span class='status-pill success'>100.0% (Perfect)</span>", "<span class='status-pill success'>1 / 26 (Lowest)</span>", "$0.00 (Local CoT)"],
      ["<code>starcoder2:3b (BigCode)</code>", "3.0B", "50.6%", "63.25s", "33.3%", "4 / 26", "$0.00 (Local CoT)"]
    ]
  }
};

let currentQueryKey = "profitara";

function renderQuery(key) {
  currentQueryKey = key;
  const data = SQL_DATA[key];
  if (!data) return;

  const codeArea = document.getElementById("sqlCodeDisplay");
  const timeArea = document.getElementById("sqlExecTime");
  const table = document.getElementById("sqlResultsTable");
  if (!codeArea || !timeArea || !table) return;

  codeArea.innerHTML = `<span class="sql-comment">${data.comment}</span><br>${data.query}`;
  timeArea.innerHTML = `<span>⚡ Query executed in ${data.time}</span> · <span>${data.rows.length} rows returned</span>`;

  // Render headers
  let thHtml = "<tr>";
  data.headers.forEach(h => { thHtml += `<th>${h}</th>`; });
  thHtml += "</tr>";
  table.querySelector("thead").innerHTML = thHtml;

  // Render rows
  let trHtml = "";
  data.rows.forEach(r => {
    trHtml += "<tr>";
    r.forEach(cell => { trHtml += `<td>${cell}</td>`; });
    trHtml += "</tr>";
  });
  table.querySelector("tbody").innerHTML = trHtml;
}

// Hook tab click events
const sqlTabs = document.querySelectorAll(".sql-tab");
sqlTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    sqlTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    renderQuery(tab.getAttribute("data-query"));
  });
});

// ---------- Universal Toast Engine ----------
let toastTimeout = null;
function showToast(message, icon = "✓") {
  const toast = document.getElementById("toast");
  if (!toast) return;
  const msgEl = document.getElementById("toast-message") || toast;
  const iconEl = document.getElementById("toast-icon");
  if (msgEl) msgEl.textContent = message;
  if (iconEl) iconEl.textContent = icon;
  toast.classList.add("show");
  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2600);
}
window.showToast = showToast;

// ---------- Live Real-Time Executive Clocks (IST UTC+5:30) ----------
function initLiveExecutiveClocks() {
  function updateTime() {
    const now = new Date();
    const options = { timeZone: "Asia/Kolkata", hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" };
    const istTime = now.toLocaleTimeString("en-GB", options);

    const headerClock = document.getElementById("header-live-clock");
    if (headerClock) {
      headerClock.textContent = `IST ${istTime} · Gurugram / NCR`;
    }

    const execClock = document.getElementById("executive-live-clock");
    if (execClock) {
      execClock.innerHTML = `IST ${istTime} &middot; Gurugram / NCR &middot; <strong style="color:var(--safe);">Open for Roles</strong> &middot; Immediate Joining`;
    }
  }
  updateTime();
  setInterval(updateTime, 1000);
}
initLiveExecutiveClocks();

// ---------- Recruiter Quick Action Handlers ----------
window.copyRecruiterBrief = function() {
  const brief = `DHRUV JAIN — Executive Data Analyst & Analytics Engineer
Location: Gurugram & Delhi NCR, India (Open to Relocation & Hybrid/Remote)
Education: B.Tech CSE (AI & Data Science) at BML Munjal University (2023-2027)
Key Verified Metrics:
- ₹66.95L Quick-Commerce Revenue & 10k transactions analyzed (Profitara)
- 2,851 Real Job Postings scraped across LinkedIn/Indeed/Glassdoor (Naukri Saaf)
- 0.930 Random Forest CLV R² & 0.920 Calibrated ROC-AUC
- 164 Passing Tests (100%) in CI/CD pipeline
Core Competencies: SQL (DuckDB, PostgreSQL, MySQL), Python (Scikit-Learn, Pandas, SHAP), Power BI (DAX, Star Schema), FastAPI, Docker, Git.
Phone: +91 99118 50506
Email: jaindhruv1923@gmail.com
LinkedIn: https://www.linkedin.com/in/jaindhruv1923/
GitHub: https://github.com/jaindhruv1923`;

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(brief).then(() => {
      showToast("Recruiter Brief copied to clipboard! ⚡", "⚡");
    }).catch(() => {
      showToast("1-Page Brief Ready for ATS! 📋", "📋");
    });
  } else {
    showToast("1-Page Brief Ready! 📋", "📋");
  }
};

window.copyEmail = function(e) {
  if (e) e.preventDefault();
  const email = "jaindhruv1923@gmail.com";
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(email).then(() => {
      showToast("Email copied: jaindhruv1923@gmail.com ✉", "✉");
    });
  } else {
    showToast("Email: jaindhruv1923@gmail.com ✉", "✉");
  }
};

window.copyCurrentSQL = function() {
  const data = SQL_DATA[currentQueryKey];
  if (!data) return;
  const temp = document.createElement("div");
  temp.innerHTML = data.comment + "\n" + data.query.replace(/<br\s*[\/]?>/gi, "\n");
  const plainSQL = temp.textContent || temp.innerText || "";
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(plainSQL.trim()).then(() => {
      showToast("SQL Query copied to clipboard! 📋", "📋");
    });
  } else {
    showToast("SQL Query copied! 📋", "📋");
  }
};

// ---------- Enhanced Run Current Query with Animated Sweep ----------
function runCurrentQuery() {
  const timeArea = document.getElementById("sqlExecTime");
  const table = document.getElementById("sqlResultsTable");
  const runBtn = document.getElementById("sqlRunBtn");
  
  if (runBtn) {
    runBtn.disabled = true;
    runBtn.style.opacity = "0.7";
    runBtn.innerHTML = `<span>⏳ Running...</span>`;
  }
  
  timeArea.innerHTML = `<span style="color:var(--accent);">⚡ Executing on DuckDB v1.2 in-memory engine...</span>`;
  if (table) {
    table.style.opacity = "0.45";
    table.style.transition = "opacity 0.15s ease";
  }

  setTimeout(() => {
    const randomMs = (3.8 + Math.random() * 4.2).toFixed(1);
    const data = SQL_DATA[currentQueryKey];
    timeArea.innerHTML = `<span>⚡ Query executed in ${randomMs}ms</span> &middot; <span>${data.rows.length} rows returned</span> &middot; <span style="color:var(--safe);font-weight:600;">STATUS: 0 ERRORS</span>`;
    
    if (table) {
      table.style.opacity = "1";
      table.querySelectorAll("tbody tr").forEach(row => {
        row.style.background = "rgba(37, 99, 235, 0.08)";
        setTimeout(() => row.style.background = "", 350);
      });
    }

    if (runBtn) {
      runBtn.disabled = false;
      runBtn.style.opacity = "1";
      runBtn.innerHTML = `▶ Re-Run Query`;
    }

    showToast(`Query executed in ${randomMs}ms on DuckDB v1.2 ✓`, "⚡");
  }, 240);
}
window.runCurrentQuery = runCurrentQuery;

// ============================================================
// PROJECT FILTER TABS (Smooth Scale & Fade Animation)
// ============================================================
const projectFilterBtns = document.querySelectorAll("#projectFilterTabs .filter-btn");
const projectCards = document.querySelectorAll(".project-card");

projectFilterBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    projectFilterBtns.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const filter = btn.getAttribute("data-filter");

    projectCards.forEach(card => {
      const cat = card.getAttribute("data-category");
      const match = (filter === "all" || cat === filter);
      if (match) {
        card.style.display = "flex";
        setTimeout(() => {
          card.style.opacity = "1";
          card.style.transform = "translateY(0) scale(1)";
        }, 20);
      } else {
        card.style.opacity = "0";
        card.style.transform = "translateY(8px) scale(0.97)";
        setTimeout(() => {
          card.style.display = "none";
        }, 180);
      }
    });
  });
});

// ============================================================
// CERTIFICATIONS FILTER TABS
// ============================================================
const certFilterBtns = document.querySelectorAll("#certFilterTabs .filter-btn");
const certCards = document.querySelectorAll(".cert-card");

certFilterBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    certFilterBtns.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const filter = btn.getAttribute("data-cert");

    certCards.forEach(card => {
      const cat = card.getAttribute("data-category");
      const match = (filter === "all" || cat === filter);
      if (match) {
        card.style.display = "flex";
        setTimeout(() => {
          card.style.opacity = "1";
          card.style.transform = "translateY(0) scale(1)";
        }, 20);
      } else {
        card.style.opacity = "0";
        card.style.transform = "translateY(8px) scale(0.97)";
        setTimeout(() => {
          card.style.display = "none";
        }, 180);
      }
    });
  });
});

// ============================================================
// ENHANCED LIGHTBOX CONTROLLER (Wide Frame, Zoom & Gallery Nav)
// ============================================================
(function initEnhancedLightbox() {
  const lightbox = document.getElementById("lightbox");
  if (!lightbox) return;

  // Ensure high-end structure inside #lightbox
  let dialog = lightbox.querySelector(".lightbox-dialog");
  let stage = lightbox.querySelector(".lightbox-stage");
  let lbImg = lightbox.querySelector(".lightbox-img") || lightbox.querySelector("img");
  let captionEl = lightbox.querySelector(".lightbox-caption-text");
  let counterEl = lightbox.querySelector(".lightbox-counter");
  let filenameEl = lightbox.querySelector(".lightbox-filename");
  let zoomBtn = lightbox.querySelector("#lb-zoom-toggle");
  let prevBtn = lightbox.querySelector("#lb-prev-btn");
  let nextBtn = lightbox.querySelector("#lb-next-btn");
  let closeBtn = lightbox.querySelector("#lb-close-btn") || lightbox.querySelector(".close");

  if (!dialog) {
    // Dynamically structure #lightbox
    const currentImgSrc = lbImg ? lbImg.src : "";
    const currentImgAlt = lbImg ? lbImg.alt : "";

    lightbox.innerHTML = `
      <div class="lightbox-dialog" role="dialog" aria-modal="true">
        <div class="lightbox-toolbar">
          <div class="lightbox-meta">
            <span class="lightbox-counter">1 / 1</span>
            <span class="lightbox-filename">Image Preview</span>
          </div>
          <div class="lightbox-actions">
            <button class="lightbox-tool-btn" id="lb-zoom-toggle" type="button" title="Toggle zoom scale">🔍 Fit / Zoom</button>
            <button class="lightbox-tool-btn" id="lb-prev-btn" type="button" title="Previous image (←)">← Prev</button>
            <button class="lightbox-tool-btn" id="lb-next-btn" type="button" title="Next image (→)">Next →</button>
            <button class="lightbox-tool-btn close-btn" id="lb-close-btn" type="button" title="Close preview (Esc)">✕ Close</button>
          </div>
        </div>
        <div class="lightbox-stage">
          <img class="lightbox-img" src="${currentImgSrc}" alt="${currentImgAlt}" />
        </div>
        <div class="lightbox-caption-bar">
          <span class="lightbox-caption-text"></span>
        </div>
      </div>
    `;

    dialog = lightbox.querySelector(".lightbox-dialog");
    stage = lightbox.querySelector(".lightbox-stage");
    lbImg = lightbox.querySelector(".lightbox-img");
    captionEl = lightbox.querySelector(".lightbox-caption-text");
    counterEl = lightbox.querySelector(".lightbox-counter");
    filenameEl = lightbox.querySelector(".lightbox-filename");
    zoomBtn = lightbox.querySelector("#lb-zoom-toggle");
    prevBtn = lightbox.querySelector("#lb-prev-btn");
    nextBtn = lightbox.querySelector("#lb-next-btn");
    closeBtn = lightbox.querySelector("#lb-close-btn");
  }

  // Active gallery tracking for navigation
  let activeGallery = [];
  let currentIndex = 0;

  function collectActiveGallery(triggerEl) {
    const parentSection = triggerEl.closest("section") || document.body;
    const items = Array.from(parentSection.querySelectorAll(".gallery-item, .cert-card, .dash-embed"));
    
    if (items.length > 0 && items.includes(triggerEl.closest(".gallery-item, .cert-card, .dash-embed"))) {
      activeGallery = items.map(item => {
        const img = item.querySelector("img");
        const cap = item.querySelector(".cap") || item.querySelector(".label") || item.querySelector("figcaption");
        const desc = cap ? cap.textContent.replace(/🔎\s*Zoom/gi, "").trim() : (img ? img.alt : "");
        const rawSrc = img ? img.getAttribute("src") : "";
        return { src: rawSrc, caption: desc, el: item };
      }).filter(item => item.src);
      
      const currentParent = triggerEl.closest(".gallery-item, .cert-card, .dash-embed");
      currentIndex = activeGallery.findIndex(i => i.el === currentParent);
      if (currentIndex === -1) currentIndex = 0;
    } else {
      // Fallback: single image
      const img = triggerEl.tagName === "IMG" ? triggerEl : triggerEl.querySelector("img");
      const cap = triggerEl.querySelector ? triggerEl.querySelector(".cap") : null;
      const desc = cap ? cap.textContent.replace(/🔎\s*Zoom/gi, "").trim() : (img ? img.alt : "");
      activeGallery = [{ src: img ? img.getAttribute("src") : "", caption: desc }];
      currentIndex = 0;
    }
  }

  function displayCurrent() {
    if (!activeGallery.length || currentIndex < 0 || currentIndex >= activeGallery.length) return;
    const item = activeGallery[currentIndex];
    lbImg.src = item.src;
    lbImg.alt = item.caption || "Preview";
    
    // Reset zoom state on image switch
    stage.classList.remove("is-zoomed");
    zoomBtn.textContent = "🔍 Fit / Zoom";
    
    // Update caption
    if (captionEl) {
      captionEl.textContent = item.caption || item.src.split("/").pop();
    }
    
    // Update counter
    if (counterEl) {
      counterEl.textContent = `${currentIndex + 1} / ${activeGallery.length}`;
    }
    
    // Update filename
    if (filenameEl) {
      const filename = item.src.split("/").pop();
      filenameEl.textContent = filename;
    }

    // Toggle navigation button visibility
    if (prevBtn) prevBtn.style.visibility = activeGallery.length > 1 ? "visible" : "hidden";
    if (nextBtn) nextBtn.style.visibility = activeGallery.length > 1 ? "visible" : "hidden";
  }

  function openLightbox(triggerEl) {
    collectActiveGallery(triggerEl);
    displayCurrent();
    lightbox.classList.add("active");
    lightbox.classList.add("open");
    document.body.style.overflow = "hidden"; // Prevent background scroll
  }

  function closeLightbox() {
    lightbox.classList.remove("active");
    lightbox.classList.remove("open");
    if (stage) stage.classList.remove("is-zoomed");
    document.body.style.overflow = "";
  }

  function nextImage() {
    if (activeGallery.length <= 1) return;
    currentIndex = (currentIndex + 1) % activeGallery.length;
    displayCurrent();
  }

  function prevImage() {
    if (activeGallery.length <= 1) return;
    currentIndex = (currentIndex - 1 + activeGallery.length) % activeGallery.length;
    displayCurrent();
  }

  function toggleZoom() {
    if (!stage) return;
    const isZoomed = stage.classList.toggle("is-zoomed");
    zoomBtn.textContent = isZoomed ? "🔍 Fit Width" : "🔍 Zoom 100%";
    if (isZoomed) {
      lbImg.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
    }
  }

  // Bind clicks to all gallery items, caption bars, zoom buttons, cert cards, and images
  document.querySelectorAll(".gallery-item, .cert-card, .dash-embed, .flow-thumb").forEach(item => {
    item.addEventListener("click", (e) => {
      // Don't trigger if user clicked an external link
      if (e.target.closest("a")) return;
      openLightbox(e.currentTarget);
    });
  });

  // Also bind any standalone images or captions with zoom cursor
  document.querySelectorAll(".dash-body img, .cap").forEach(el => {
    el.addEventListener("click", (e) => {
      if (e.target.closest(".gallery-item, .cert-card, .dash-embed, .flow-thumb")) return; // already handled
      openLightbox(e.currentTarget);
    });
  });

  // Lightbox toolbar buttons
  if (closeBtn) closeBtn.addEventListener("click", (e) => { e.stopPropagation(); closeLightbox(); });
  if (prevBtn) prevBtn.addEventListener("click", (e) => { e.stopPropagation(); prevImage(); });
  if (nextBtn) nextBtn.addEventListener("click", (e) => { e.stopPropagation(); nextImage(); });
  if (zoomBtn) zoomBtn.addEventListener("click", (e) => { e.stopPropagation(); toggleZoom(); });

  // Clicking directly on the image toggles zoom
  lbImg.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleZoom();
  });

  // Clicking on stage or dialog background outside controls does NOT close, but clicking outer backdrop does
  dialog.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });

  // Keyboard navigation
  window.addEventListener("keydown", (e) => {
    if (!lightbox.classList.contains("open") && !lightbox.classList.contains("active")) return;
    if (e.key === "Escape") {
      closeLightbox();
    } else if (e.key === "ArrowRight") {
      nextImage();
    } else if (e.key === "ArrowLeft") {
      prevImage();
    } else if (e.key === "z" || e.key === "Z") {
      toggleZoom();
    }
  });
})();

// ---------- Footer local clock (IST) ----------
const clockEl = document.getElementById("footer-clock");
if (clockEl) {
  function tick() {
    const now = new Date().toLocaleTimeString("en-IN", { timeZone: "Asia/Kolkata", hour: "2-digit", minute: "2-digit", second: "2-digit" });
    clockEl.textContent = `${now} IST · Gurugram / Delhi, India`;
  }
  tick();
  setInterval(tick, 1000);
}

// ---------- Resume download handler ----------
document.querySelectorAll("#resume-link, .nav-cta").forEach(link => {
  link.addEventListener("click", (e) => {
    // Open in new tab natively or trigger download
  });
});

// ============================================================
// INTERACTIVE MOUSE PARTICLE CONSTELLATION WEB (Canvas Option 3)
// ============================================================
function initInteractiveParticleWeb() {
  const canvas = document.getElementById("interactive-particle-web");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  let width = window.innerWidth;
  let height = window.innerHeight;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
  }
  resize();
  window.addEventListener("resize", resize, { passive: true });

  const PARTICLE_COUNT = Math.min(115, Math.max(65, Math.floor((width * height) / 13000)));
  const particles = [];

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const isCyan = Math.random() > 0.65;
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.55,
      vy: (Math.random() - 0.5) * 0.55,
      radius: Math.random() * 1.8 + 1.8,
      color: isCyan ? "rgba(14, 165, 233, 0.75)" : "rgba(37, 99, 235, 0.68)",
      pulse: Math.random() * Math.PI * 2
    });
  }

  const mouse = { x: -1000, y: -1000, active: false };

  window.addEventListener("mousemove", (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  }, { passive: true });

  window.addEventListener("mouseleave", () => {
    mouse.active = false;
  });

  window.addEventListener("touchstart", (e) => {
    if (e.touches && e.touches[0]) {
      mouse.x = e.touches[0].clientX;
      mouse.y = e.touches[0].clientY;
      mouse.active = true;
    }
  }, { passive: true });

  window.addEventListener("touchmove", (e) => {
    if (e.touches && e.touches[0]) {
      mouse.x = e.touches[0].clientX;
      mouse.y = e.touches[0].clientY;
      mouse.active = true;
    }
  }, { passive: true });

  window.addEventListener("touchend", () => {
    mouse.active = false;
  });

  function renderParticles() {
    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    // Update and draw particles
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.pulse += 0.03;

      // Wrap around edges
      if (p.x < 0) p.x = width;
      else if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      else if (p.y > height) p.y = 0;

      // Interactive mouse attraction and laser line
      if (mouse.active) {
        const dxM = p.x - mouse.x;
        const dyM = p.y - mouse.y;
        const distM = Math.sqrt(dxM * dxM + dyM * dyM);

        if (distM < 190) {
          const mAlpha = (1 - distM / 190) * 0.75;
          ctx.strokeStyle = `rgba(14, 165, 233, ${mAlpha.toFixed(2)})`;
          ctx.lineWidth = 1.3;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.stroke();

          // Gentle magnetic pull toward cursor
          if (distM > 20) {
            p.x -= (dxM / distM) * 0.35;
            p.y -= (dyM / distM) * 0.35;
          }
        }
      }

      // Draw particle dot
      const rad = p.radius + Math.sin(p.pulse) * 0.35;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, rad, 0, Math.PI * 2);
      ctx.fill();

      // Connect nearby particles to form neural constellation
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 135) {
          const alpha = (1 - dist / 135) * 0.35;
          ctx.strokeStyle = `rgba(37, 99, 235, ${alpha.toFixed(2)})`;
          ctx.lineWidth = 0.9;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }

    // Draw active cursor constellation hub
    if (mouse.active && mouse.x > 0 && mouse.y > 0) {
      ctx.fillStyle = "rgba(14, 165, 233, 0.75)";
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 3.2, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = "rgba(14, 165, 233, 0.3)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 8, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
    requestAnimationFrame(renderParticles);
  }

  requestAnimationFrame(renderParticles);
}
initInteractiveParticleWeb();

// ============================================================
// FIXED TELEMETRY RAILS NAVIGATION & SCROLL ENGINE (Options 1 & 2)
// ============================================================
function initTelemetryRails() {
  const railItems = document.querySelectorAll(".telemetry-rail-left .rail-nav-item");
  const scrollTopBtn = document.getElementById("railScrollTopBtn");
  const sections = [
    "about",
    "sql-lab",
    "math-foundations",
    "projects",
    "models",
    "artifacts",
    "certifications",
    "experience"
  ];

  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY || window.pageYOffset;

    // Show / Dim Back-to-Top Button
    if (scrollTopBtn) {
      if (scrollY > 400) {
        scrollTopBtn.style.opacity = "1";
        scrollTopBtn.style.pointerEvents = "auto";
      } else {
        scrollTopBtn.style.opacity = "0.3";
      }
    }

    // Scroll-Spy for Left Rail Items
    let current = "about";
    sections.forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        const top = el.offsetTop - 140;
        const height = el.offsetHeight;
        if (scrollY >= top && scrollY < top + height) {
          current = id;
        }
      }
    });

    railItems.forEach((item) => {
      const target = item.getAttribute("data-rail-target");
      if (target === current) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });
  }, { passive: true });
}
initTelemetryRails();

// ============================================================
// INTERACTIVE 3D DATA TELEMETRY GLOBE (Canvas WebGL-Style Math)
// ============================================================
function initInteractive3DGlobe() {
  const canvas = document.getElementById("interactive-data-globe");
  const container = document.getElementById("globe-drag-area") || (canvas ? canvas.parentElement : null);
  if (!canvas || !container) return;

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  // High DPI Canvas Scaling
  let width = container.clientWidth || 460;
  let height = container.clientHeight || 400;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  function resizeCanvas() {
    width = container.clientWidth || 460;
    height = container.clientHeight || 400;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
  }
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas, { passive: true });

  const GLOBE_RADIUS = Math.min(width, height) * 0.38;

  // Lat / Lon conversion helper
  function latLonToVec3(lat, lon, r = 1) {
    const phi = (lat * Math.PI) / 180;
    const theta = ((lon + 180) * Math.PI) / 180;
    const x = -r * Math.cos(phi) * Math.cos(theta);
    const y = -r * Math.sin(phi);
    const z = r * Math.cos(phi) * Math.sin(theta);
    return { x, y, z };
  }

  // 1. Generate Fibonacci Sphere Lattice (~420 points)
  const POINT_COUNT = 440;
  const points = [];
  const phi = Math.PI * (3 - Math.sqrt(5)); // Golden ratio angle

  for (let i = 0; i < POINT_COUNT; i++) {
    const y = 1 - (i / (POINT_COUNT - 1)) * 2; // y goes from 1 to -1
    const radiusAtY = Math.sqrt(1 - y * y);
    const theta = phi * i;
    const x = Math.cos(theta) * radiusAtY;
    const z = Math.sin(theta) * radiusAtY;
    points.push({ x, y, z });
  }

  // 2. Verified Enterprise Data Telemetry Hubs
  const hubs = [
    { name: "Gurugram HQ", lat: 28.4595, lon: 77.0266, isHQ: true, color: "#2563EB", pulseR: 0 },
    { name: "Mumbai Node", lat: 19.0760, lon: 72.8777, isHQ: false, color: "#0284C7" },
    { name: "Bengaluru Node", lat: 12.9716, lon: 77.5946, isHQ: false, color: "#0284C7" },
    { name: "Singapore Cloud", lat: 1.3521, lon: 103.8198, isHQ: false, color: "#10B981" },
    { name: "London Node", lat: 51.5074, lon: -0.1278, isHQ: false, color: "#6366F1" },
    { name: "New York Endpoint", lat: 40.7128, lon: -74.0060, isHQ: false, color: "#8B5CF6" }
  ];

  // Convert hubs to 3D unit coordinates
  hubs.forEach(h => {
    const v = latLonToVec3(h.lat, h.lon, 1);
    h.x = v.x;
    h.y = v.y;
    h.z = v.z;
  });

  // 3. Arcs connecting Gurugram HQ (index 0) to other remote hubs
  const arcs = hubs.slice(1).map(dest => ({
    from: hubs[0],
    to: dest,
    pulsePos: Math.random() // current progress (0 to 1) of the light packet
  }));

  // Rotation State (Initial tilt toward India: lat ~25°, lon ~75°)
  let rotX = 0.28;
  let rotY = -1.25;
  let velX = 0;
  let velY = 0.0028; // Gentle autonomous rotation
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;

  // Mouse & Touch Drag Listeners
  container.addEventListener("mousedown", (e) => {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
    velX = 0;
    velY = 0;
  });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;
    velY = dx * 0.005;
    velX = dy * 0.005;
    rotY += velY;
    rotX += velX;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
  });

  // Touch Support
  container.addEventListener("touchstart", (e) => {
    if (e.touches.length === 1) {
      isDragging = true;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
      velX = 0;
      velY = 0;
    }
  }, { passive: true });

  window.addEventListener("touchmove", (e) => {
    if (!isDragging || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - lastMouseX;
    const dy = e.touches[0].clientY - lastMouseY;
    velY = dx * 0.005;
    velX = dy * 0.005;
    rotY += velY;
    rotX += velX;
    lastMouseX = e.touches[0].clientX;
    lastMouseY = e.touches[0].clientY;
  }, { passive: true });

  window.addEventListener("touchend", () => {
    isDragging = false;
  });

  // 3D Point Rotation Helper
  function rotatePoint(p, rx, ry) {
    // 1. Rotate around X axis
    const cosX = Math.cos(rx);
    const sinX = Math.sin(rx);
    const y1 = p.y * cosX - p.z * sinX;
    const z1 = p.y * sinX + p.z * cosX;

    // 2. Rotate around Y axis
    const cosY = Math.cos(ry);
    const sinY = Math.sin(ry);
    const x2 = p.x * cosY + z1 * sinY;
    const z2 = -p.x * sinY + z1 * cosY;

    return { x: x2, y: y1, z: z2 };
  }

  // Great Circle Arc Interpolator with elevation arch
  function getArcPoint(p1, p2, t, peakElevation = 0.22) {
    // Spherical linear interpolation between two 3D vectors
    const dot = Math.max(-1, Math.min(1, p1.x * p2.x + p1.y * p2.y + p1.z * p2.z));
    const omega = Math.acos(dot);
    
    let x, y, z;
    if (Math.abs(omega) < 0.001) {
      x = p1.x; y = p1.y; z = p1.z;
    } else {
      const sinOmega = Math.sin(omega);
      const a = Math.sin((1 - t) * omega) / sinOmega;
      const b = Math.sin(t * omega) / sinOmega;
      x = a * p1.x + b * p2.x;
      y = a * p1.y + b * p2.y;
      z = a * p1.z + b * p2.z;
    }

    // Parabolic arch above globe surface
    const arch = Math.sin(t * Math.PI) * peakElevation;
    const norm = Math.sqrt(x * x + y * y + z * z) || 1;
    const scale = (1 + arch) / norm;
    return { x: x * scale, y: y * scale, z: z * scale };
  }

  // Main Render Loop
  let animTime = 0;

  function renderGlobe() {
    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;
    const R = Math.min(width, height) * 0.38;

    // Autonomous rotation damping & drift
    if (!isDragging) {
      velY *= 0.96;
      velX *= 0.96;
      if (Math.abs(velY) < 0.002) velY = 0.0022; // Base continuous orbit
      rotY += velY;
      rotX += velX;
      // Clamp vertical tilt between -60° and +60°
      rotX = Math.max(-1.0, Math.min(1.0, rotX));
    }

    animTime += 0.02;

    // 1. Draw Globe Atmosphere / Outer Glow Disc
    const glowGrad = ctx.createRadialGradient(cx, cy, R * 0.75, cx, cy, R * 1.15);
    glowGrad.addColorStop(0, "rgba(37, 99, 235, 0.06)");
    glowGrad.addColorStop(0.7, "rgba(56, 189, 248, 0.04)");
    glowGrad.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.fillStyle = glowGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, R * 1.15, 0, Math.PI * 2);
    ctx.fill();

    // Globe Base Disc
    const baseGrad = ctx.createRadialGradient(cx - R * 0.25, cy - R * 0.25, R * 0.1, cx, cy, R);
    baseGrad.addColorStop(0, "rgba(255, 255, 255, 0.95)");
    baseGrad.addColorStop(0.85, "rgba(241, 245, 249, 0.75)");
    baseGrad.addColorStop(1, "rgba(226, 232, 240, 0.4)");
    ctx.fillStyle = baseGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.fill();

    // Subtle Globe Perimeter Ring
    ctx.strokeStyle = "rgba(37, 99, 235, 0.22)";
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // 2. Render Rotated Point Cloud (Dot Matrix)
    points.forEach((p) => {
      const rot = rotatePoint(p, rotX, rotY);
      // Only render points visible on front hemisphere
      if (rot.z > -0.15) {
        const px = cx + rot.x * R;
        const py = cy + rot.y * R;
        
        // Depth-based sizing & opacity
        const depthAlpha = Math.max(0.12, Math.min(0.85, (rot.z + 0.3) / 1.3));
        const ptSize = Math.max(1, 1.2 + rot.z * 1.4);

        ctx.fillStyle = `rgba(37, 99, 235, ${depthAlpha.toFixed(2)})`;
        ctx.beginPath();
        ctx.arc(px, py, ptSize, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // 3. Render Curved 3D Great-Circle Arcs
    arcs.forEach((arc) => {
      const p1Rot = rotatePoint(arc.from, rotX, rotY);
      const p2Rot = rotatePoint(arc.to, rotX, rotY);

      // Advance pulse packet along the arc
      arc.pulsePos = (arc.pulsePos + 0.007) % 1;

      // Draw Arc Path using sampled points
      const SAMPLES = 28;
      ctx.beginPath();
      let firstVisible = false;

      for (let s = 0; s <= SAMPLES; s++) {
        const t = s / SAMPLES;
        const pt3D = getArcPoint(arc.from, arc.to, t, 0.24);
        const rotPt = rotatePoint(pt3D, rotX, rotY);
        const ax = cx + rotPt.x * R;
        const ay = cy + rotPt.y * R;

        if (rotPt.z > -0.1) {
          if (!firstVisible) {
            ctx.moveTo(ax, ay);
            firstVisible = true;
          } else {
            ctx.lineTo(ax, ay);
          }
        }
      }

      ctx.strokeStyle = "rgba(14, 165, 233, 0.35)";
      ctx.lineWidth = 1.2;
      ctx.setLineDash([3, 3]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw Light Pulse Packet moving along arc
      const pulse3D = getArcPoint(arc.from, arc.to, arc.pulsePos, 0.24);
      const pulseRot = rotatePoint(pulse3D, rotX, rotY);
      if (pulseRot.z > -0.1) {
        const pulseX = cx + pulseRot.x * R;
        const pulseY = cy + pulseRot.y * R;

        ctx.fillStyle = "#38BDF8";
        ctx.shadowColor = "#0284C7";
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(pulseX, pulseY, 2.8, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0; // reset
      }
    });

    // 4. Render City Hub Pins & Dynamic Halo Indicators
    hubs.forEach((hub) => {
      const rot = rotatePoint(hub, rotX, rotY);
      if (rot.z > -0.1) {
        const hx = cx + rot.x * R;
        const hy = cy + rot.y * R;

        // Pulsing rings for Gurugram HQ
        if (hub.isHQ) {
          hub.pulseR = (animTime * 18) % 24;
          const pulseOpacity = Math.max(0, 1 - hub.pulseR / 24);

          ctx.strokeStyle = `rgba(37, 99, 235, ${pulseOpacity.toFixed(2)})`;
          ctx.lineWidth = 1.4;
          ctx.beginPath();
          ctx.arc(hx, hy, 4 + hub.pulseR, 0, Math.PI * 2);
          ctx.stroke();

          // HQ Marker (Golden core with blue halo)
          ctx.fillStyle = "#F59E0B";
          ctx.beginPath();
          ctx.arc(hx, hy, 5.5, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = "#FFFFFF";
          ctx.beginPath();
          ctx.arc(hx, hy, 2.2, 0, Math.PI * 2);
          ctx.fill();

          // HQ Text Tag
          ctx.font = "bold 10px 'JetBrains Mono', monospace";
          ctx.fillStyle = "#0F172A";
          ctx.fillText("HQ: Gurugram", hx + 9, hy + 3);
        } else {
          // Remote nodes
          ctx.fillStyle = hub.color;
          ctx.beginPath();
          ctx.arc(hx, hy, 3.8, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = "#FFFFFF";
          ctx.beginPath();
          ctx.arc(hx, hy, 1.4, 0, Math.PI * 2);
          ctx.fill();

          if (rot.z > 0.4) {
            ctx.font = "9px 'Inter', sans-serif";
            ctx.fillStyle = "#475569";
            ctx.fillText(hub.name.split(" ")[0], hx + 7, hy + 3);
          }
        }
      }
    });

    ctx.restore();
    requestAnimationFrame(renderGlobe);
  }

  requestAnimationFrame(renderGlobe);
}
initInteractive3DGlobe();

// ============================================================
// MATHEMATICAL & STATISTICAL FORMULATIONS INTERACTIVE ENGINE
// ============================================================

// Live Theoretical CLV Simulator
function updateLiveCLV() {
  const aovInput = document.getElementById("clv-aov");
  const freqInput = document.getElementById("clv-freq");
  const marginInput = document.getElementById("clv-margin");
  const retInput = document.getElementById("clv-ret");

  if (!aovInput || !freqInput || !marginInput || !retInput) return;

  const aov = parseFloat(aovInput.value) || 2450;
  const freq = parseFloat(freqInput.value) || 8.4;
  const marginPct = parseFloat(marginInput.value) || 32;
  const retPct = parseFloat(retInput.value) || 78;
  const discount = 0.10; // 10% annual capital discount rate

  // Update slider label indicators
  const aovLabel = document.getElementById("clv-aov-val");
  const freqLabel = document.getElementById("clv-freq-val");
  const marginLabel = document.getElementById("clv-margin-val");
  const retLabel = document.getElementById("clv-ret-val");
  const display = document.getElementById("clv-result-display");

  if (aovLabel) aovLabel.textContent = `₹${aov.toLocaleString("en-IN")}`;
  if (freqLabel) freqLabel.textContent = freq.toFixed(1);
  if (marginLabel) marginLabel.textContent = `${marginPct}%`;
  if (retLabel) retLabel.textContent = `${retPct}%`;

  // Analytical Geometric CLV formula: (AOV * f * m) / (1 + d - r)
  const m = marginPct / 100;
  const r = retPct / 100;
  const denom = Math.max(0.01, 1 + discount - r);
  const clv = (aov * freq * m) / denom;

  if (display) {
    display.textContent = `₹${Math.round(clv).toLocaleString("en-IN")}.00`;
  }
}

// Math Formula Category Filter Switcher
function initMathFormulasFilter() {
  const filterBtns = document.querySelectorAll(".math-filter-btn");
  const cards = document.querySelectorAll(".math-card");
  if (!filterBtns.length || !cards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter") || "all";
      cards.forEach(card => {
        const cat = card.getAttribute("data-category");
        if (filter === "all" || cat === filter) {
          card.style.display = "flex";
          card.style.opacity = "1";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
}

// Interactive Architecture & Flowchart Engine
function initInteractiveFlowcharts() {
  const flowcharts = document.querySelectorAll(".interactive-flowchart");
  flowcharts.forEach((fc) => {
    const nodeBtns = fc.querySelectorAll(".flow-node-btn");
    const stageContents = fc.querySelectorAll(".flow-stage-content");
    const simBtn = fc.querySelector(".flow-sim-btn");
    const prevBtn = fc.querySelector(".flow-step-btn.prev");
    const nextBtn = fc.querySelector(".flow-step-btn.next");
    const statusText = fc.querySelector(".flow-status-text");
    const pulseDot = fc.querySelector(".flow-pulse-dot");
    const currentLabel = fc.querySelector(".flow-current-label");
    const consoleText = fc.querySelector(".flow-console-text");

    let currentIdx = 0;
    let simInterval = null;
    let isSimulating = false;

    function activateStage(index, isFromSim) {
      if (index < 0) index = 0;
      if (index >= nodeBtns.length) index = nodeBtns.length - 1;
      currentIdx = index;

      // Update Node Buttons
      nodeBtns.forEach((btn, i) => {
        btn.classList.toggle("active", i === currentIdx);
        if (isFromSim && i === currentIdx) {
          btn.classList.add("sim-active");
          setTimeout(() => btn.classList.remove("sim-active"), 1200);
        } else {
          btn.classList.remove("sim-active");
        }
      });

      // Update Stage Content Panels
      stageContents.forEach((content, i) => {
        if (i === currentIdx) {
          content.style.display = "block";
          content.style.opacity = "0";
          content.style.transform = "translateY(6px)";
          setTimeout(() => {
            content.style.transition = "opacity 0.25s ease, transform 0.25s ease";
            content.style.opacity = "1";
            content.style.transform = "translateY(0)";
          }, 10);
        } else {
          content.style.display = "none";
        }
      });

      // Update Header Info
      const activeBtn = nodeBtns[currentIdx];
      const stageName = activeBtn ? activeBtn.querySelector(".flow-node-title").textContent.trim() : `Stage 0${currentIdx + 1}`;
      if (currentLabel) {
        currentLabel.textContent = `Stage 0${currentIdx + 1}: ${stageName}`;
      }

      // Update Console Log
      const stageLog = activeBtn ? activeBtn.getAttribute("data-log") : null;
      if (consoleText && stageLog) {
        const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false });
        consoleText.textContent = `[${timeStr}] ${stageLog}`;
      }

      if (!isFromSim && isSimulating) {
        stopSimulation();
      }
    }

    function startSimulation() {
      isSimulating = true;
      if (simBtn) {
        simBtn.innerHTML = "⏸ Pause Simulation";
        simBtn.style.background = "linear-gradient(135deg, #D97706, #B45309)";
      }
      if (statusText) statusText.textContent = "Simulating Live Pipeline...";
      if (pulseDot) pulseDot.classList.add("simulating");

      currentIdx = 0;
      activateStage(currentIdx, true);

      simInterval = setInterval(() => {
        currentIdx++;
        if (currentIdx >= nodeBtns.length) {
          currentIdx = 0;
        }
        activateStage(currentIdx, true);
      }, 2200);
    }

    function stopSimulation() {
      isSimulating = false;
      if (simInterval) clearInterval(simInterval);
      if (simBtn) {
        simBtn.innerHTML = "▶ Run Pipeline Simulation";
        simBtn.style.background = "";
      }
      if (statusText) statusText.textContent = "Interactive Mode (Ready)";
      if (pulseDot) pulseDot.classList.remove("simulating");
    }

    // Attach click events
    nodeBtns.forEach((btn, i) => {
      btn.addEventListener("click", () => activateStage(i, false));
    });

    if (simBtn) {
      simBtn.addEventListener("click", () => {
        if (isSimulating) stopSimulation();
        else startSimulation();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        let prev = currentIdx - 1;
        if (prev < 0) prev = nodeBtns.length - 1;
        activateStage(prev, false);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        let next = currentIdx + 1;
        if (next >= nodeBtns.length) next = 0;
        activateStage(next, false);
      });
    }

    // Initialize first stage
    if (nodeBtns.length > 0) {
      activateStage(0, false);
    }
  });
}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  updateLiveCLV();
  initMathFormulasFilter();
  initInteractiveFlowcharts();
  
  if (window.renderMathInElement) {
    const mathSec = document.getElementById("math-foundations");
    if (mathSec) {
      renderMathInElement(mathSec, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false }
        ],
        throwOnError: false
      });
    }
  }
});


