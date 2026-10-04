(function () {
  if (window.__naukriSaafBootstrapped) return;
  window.__naukriSaafBootstrapped = true;

// Naukri Saaf — bootstrap
// Loaded FIRST, before lib/nlp.js, lib/legitimacy.js, and sidepanel.js.
// Catches any uncaught error from any of those and writes it straight into the
// panel UI, so a broken build is visible without opening DevTools.
// (This can't be an inline <script> in the HTML — MV3's default CSP for
// extension pages blocks inline scripts, so it has to be its own file.)
window.addEventListener("error", (e) => {
  try {
    const target = document.getElementById("ov-empty") || document.body;
    target.textContent =
      "Extension error: " + e.message + " (" + (e.filename || "").split("/").pop() + ":" + e.lineno + ")";
    target.style.color = "#F87171";
    target.classList.remove("hidden");
    const dataEl = document.getElementById("ov-data");
    if (dataEl) dataEl.classList.add("hidden");
  } catch (inner) {
    // Last resort — if even the error display breaks, at least log it.
    console.error("Naukri Saaf bootstrap error handler failed:", inner, "original error:", e);
  }
});

})();
