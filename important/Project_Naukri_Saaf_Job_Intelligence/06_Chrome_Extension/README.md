# Naukri Saaf — Job Fit & Ghost Check (Chrome Extension v4)

**Zero-Knowledge Client-Side Resume Privacy + Dual-Mode Real-Time Scoring (FastAPI Service with Offline Heuristic Fallback).**

The Naukri Saaf Chrome Extension operates in your browser toolbar/sidepanel, analyzing job listings on **LinkedIn, Indeed, Glassdoor, and Naukri** in real time.

---

## 🚀 Key Capabilities

1. **Dual-Mode ML Scoring**:
   - **Live Production Mode**: Connects to the local FastAPI microservice (`http://localhost:8000/api/v1/score`) to run the actual **calibrated ensemble model** and **TreeSHAP explainer** in `<15ms`.
   - **Offline Standalone Mode**: If the local backend is not running, the extension automatically falls back to client-side heuristic evaluation (`legitimacy.js`), ensuring zero downtime or broken interfaces.
2. **Zero-Knowledge Resume Privacy**:
   - Resumes uploaded (PDF or text) are extracted client-side via `lib/pdfjs/` and stored strictly in `chrome.storage.local`.
   - **Zero network egress**: Resume text and personal contact information never touch any cloud server.
3. **Multi-Tool Verification Links**:
   - One-click deep-dive links to verify corporate Mandate on Glassdoor, AmbitionBox, MCA registry, and news archives.
4. **Keyword & Skill Gap Matrix**:
   - Computes local TF-IDF cosine similarity and skill ontology coverage, highlighting exact matched competencies vs critical missing skills.

---

## 🛠️ Installation (Chrome Developer Mode)

1. Open `chrome://extensions` in Google Chrome or any Chromium browser.
2. Enable **Developer mode** (toggle in top-right corner).
3. Click **Load unpacked**.
4. Select the `06_Chrome_Extension/` folder from this repository.
5. Pin **Naukri Saaf** to your browser toolbar.

---

## 🔌 Running with Live Backend (Recommended)

To enable live calibrated ML inference with TreeSHAP explanations:
```powershell
# In terminal, launch the FastAPI microservice
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Now, whenever you click **Scan Listing** in the Chrome extension, it automatically queries `http://localhost:8000/api/v1/score` for exact calibrated risk probabilities!

If the FastAPI service is not running, the extension will display:
`Offline Mode (Client Heuristics)` and provide transparent rule-based scoring without throwing unhandled errors.

---

## 📋 File Architecture (`06_Chrome_Extension/`)

```
06_Chrome_Extension/
├── manifest.json         # Manifest V3 configuration (sidepanel, permissions, match rules)
├── sidepanel.html        # Main sidepanel UI panel with tab navigation (Overview, Resume Match, Legitimacy)
├── sidepanel.js          # UI controller, event handlers, and API bridge
├── sidepanel.css         # Modern dark-theme stylesheet
├── background.js         # Service worker handling sidepanel triggers
├── bootstrap.js          # Sidepanel initialization bootstrap
├── content.js            # In-page DOM parser for LinkedIn, Indeed, Glassdoor, Naukri
├── icons/                # Extension icon assets (16x16, 48x48, 128x128)
└── lib/                  # Bundled dependencies
    ├── legitimacy.js     # Client-side heuristic scorecard (offline fallback)
    ├── nlp.js            # Client-side tokenizer, TF-IDF, and skill dictionary
    └── pdfjs/            # Sandboxed PDF parser for zero-knowledge resume ingestion
        ├── pdf.min.js
        └── pdf.worker.min.js
```

---

## 🔒 Security & Privacy Audit

- **Permissions**: `sidePanel`, `storage`, `activeTab`. Zero broad wildcard web-request interception.
- **Network Traffic**: Only makes outbound HTTP requests to `http://localhost:8000/api/v1/score` if enabled by the user; resume text is never transmitted over the wire.
