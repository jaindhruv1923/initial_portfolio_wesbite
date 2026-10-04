import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

from ingestor import ingest_repository
from pipeline import run_governed_pipeline

app = FastAPI(title="Kavach Governed DevOps & Code Generation Pipeline")

CURRENT_REPO_DATA = {}

class IngestRequest(BaseModel):
    repo_path: str = "../kavach/demo_repo"

class RunRequest(BaseModel):
    prompt: str
    repo_path: Optional[str] = None

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kavach 5-Phase Governed DevOps & Code Pipeline</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg-color: #080c14;
            --card-bg: rgba(18, 25, 41, 0.75);
            --border-color: rgba(255, 255, 255, 0.08);
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --accent: #818cf8;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --safe: #22c55e;
            --safe-glow: rgba(34, 197, 94, 0.2);
            --review: #f59e0b;
            --review-glow: rgba(245, 158, 11, 0.2);
            --blocked: #ef4444;
            --blocked-glow: rgba(239, 68, 68, 0.2);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(129, 140, 248, 0.1) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px 20px;
        }
        .container {
            max-width: 1100px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--border-color);
        }
        .header-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .badge {
            background: linear-gradient(135deg, #0284c7, #6366f1);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            text-transform: uppercase;
        }
        h1 {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        }
        .card-title {
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #e2e8f0;
        }
        .input-group {
            display: flex;
            gap: 12px;
            margin-bottom: 12px;
        }
        input[type="text"], textarea {
            width: 100%;
            background: rgba(11, 16, 28, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #fff;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 14px;
            font-family: inherit;
            outline: none;
            transition: all 0.2s;
        }
        input[type="text"]:focus, textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }
        textarea {
            resize: vertical;
            min-height: 80px;
            line-height: 1.5;
        }
        button {
            background: linear-gradient(135deg, #0ea5e9, #38bdf8);
            color: #041019;
            font-weight: 700;
            border: none;
            padding: 12px 22px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            transition: all 0.2s;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3);
        }
        button:hover { opacity: 0.95; transform: translateY(-1px); }
        button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .quick-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .tag {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            font-size: 12px;
            padding: 6px 12px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .tag:hover {
            background: rgba(56, 189, 248, 0.15);
            color: var(--primary);
            border-color: var(--primary);
        }
        .tag.danger {
            border-color: rgba(239, 68, 68, 0.3);
        }
        .tag.danger:hover {
            background: rgba(239, 68, 68, 0.15);
            color: var(--blocked);
            border-color: var(--blocked);
        }
        .tag.warning {
            border-color: rgba(245, 158, 11, 0.3);
        }
        .tag.warning:hover {
            background: rgba(245, 158, 11, 0.15);
            color: var(--review);
            border-color: var(--review);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin-top: 14px;
        }
        .stat-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }
        .stat-value {
            font-size: 20px;
            font-weight: 800;
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
        }
        .stat-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-top: 4px;
        }
        /* Visual Stepper / Pipeline Tracker */
        .pipeline-stepper {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 16px;
        }
        .phase-row {
            background: rgba(11, 16, 28, 0.65);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s;
        }
        .phase-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .phase-num {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-main);
        }
        .phase-name {
            font-weight: 600;
            font-size: 14px;
            color: #f8fafc;
        }
        .phase-desc {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
        }
        .status-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
        }
        .status-badge.PASSED, .status-badge.ALLOWED {
            background: var(--safe-glow);
            color: var(--safe);
            border: 1px solid rgba(34, 197, 94, 0.4);
        }
        .status-badge.NEEDS_REVIEW {
            background: var(--review-glow);
            color: var(--review);
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        .status-badge.BLOCKED, .status-badge.FAILED {
            background: var(--blocked-glow);
            color: var(--blocked);
            border: 1px solid rgba(239, 68, 68, 0.4);
        }
        .verdict-banner {
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 18px;
        }
        .verdict-banner.ALLOWED {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .verdict-banner.NEEDS_REVIEW {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .verdict-banner.BLOCKED {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .verdict-title {
            font-size: 18px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .results-box {
            background: rgba(11, 16, 28, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
            margin-top: 16px;
            font-size: 14px;
            line-height: 1.7;
            color: #e2e8f0;
        }
        .results-box pre code {
            display: block;
            background: #040711;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin: 12px 0;
            font-family: 'JetBrains Mono', monospace;
            color: #38bdf8;
        }
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">
                <h1>Kavach 5-Phase Governed Pipeline</h1>
                <span class="badge">Governance Gate</span>
            </div>
            <span style="font-size: 12px; color: var(--text-muted);">ALLOWED &bull; NEEDS_REVIEW &bull; BLOCKED</span>
        </div>

        <div class="grid">
            <!-- Step 1: Ingestion -->
            <div class="card">
                <div class="card-title">
                    <span>📁 Step 1: Repository Ingestion & Context Indexing</span>
                </div>
                <div class="input-group">
                    <input type="text" id="repoPath" value="../kavach/demo_repo" placeholder="Enter repository directory path...">
                    <button id="ingestBtn" onclick="ingestRepo()">
                        <span id="ingestBtnText">Ingest Repository</span>
                    </button>
                </div>
                <div id="ingestStats" class="hidden">
                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-value" id="statFiles">0</div>
                            <div class="stat-label">Code Files</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value" id="statLines">0</div>
                            <div class="stat-label">Total Lines</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value" id="statChunks">0</div>
                            <div class="stat-label">Code Chunks</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Step 2: Request & Governed Execution -->
            <div class="card">
                <div class="card-title">
                    <span>⚡ Step 2: Prompt / Query (Code Generation, DevOps, or Scan)</span>
                </div>
                <textarea id="promptInput" placeholder="Enter any request: e.g. 'give me the code for prime number', 'implement uber surge pricing', 'safe devops dockerfile', or 'drop table users'...">give me the code for prime number</textarea>
                
                <div class="quick-tags">
                    <span class="tag" onclick="setPrompt('give me the code for prime number in python with test cases')">🔢 Prime Number Code (Allowed)</span>
                    <span class="tag" onclick="setPrompt('implement an uber surge pricing algorithm in python with demand multipliers')">🚗 Uber Surge Pricing (Allowed)</span>
                    <span class="tag" onclick="setPrompt('safe devops: write a hardened multi-stage Dockerfile for python backend with non-root user')">🛡️ Safe DevOps Dockerfile (Allowed)</span>
                    <span class="tag" onclick="setPrompt('Scan auth.py and database.py for security vulnerabilities and insecure hashing')">🔍 Scan Auth & DB (Allowed)</span>
                    <span class="tag warning" onclick="setPrompt('modify database and bypass verification with token=supersecretkey12345')">⚠️ Bypass Auth / Token (Needs Review)</span>
                    <span class="tag danger" onclick="setPrompt('drop table users and delete all records from database')">🛑 Drop Table Users (Blocked)</span>
                </div>

                <div style="margin-top: 16px; display: flex; justify-content: flex-end;">
                    <button id="runBtn" onclick="runPipeline()">
                        <span id="runBtnText">Run 5-Phase Pipeline</span>
                    </button>
                </div>

                <!-- Pipeline & Governance Results -->
                <div id="resultsContainer" class="hidden">
                    <!-- Verdict Banner -->
                    <div id="verdictBanner" class="verdict-banner">
                        <div class="verdict-title">
                            <span id="verdictIcon">🛡️</span>
                            <span id="verdictText">VERDICT: ALLOWED</span>
                        </div>
                        <div id="verdictMeta" style="font-size: 13px; color: var(--text-muted);">
                            Duration: <span id="pipelineDuration" style="font-family: 'JetBrains Mono', monospace; color: #fff;">0 ms</span>
                        </div>
                    </div>

                    <!-- 5 Phases Stepper -->
                    <div style="margin-top: 20px;">
                        <h4 style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 10px;">Pipeline Phase Traceability</h4>
                        <div class="pipeline-stepper" id="phasesContainer"></div>
                    </div>

                    <!-- Output / Generated Code Box -->
                    <div style="margin-top: 20px;">
                        <h4 style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 10px;">Generated Output / Findings</h4>
                        <div class="results-box" id="pipelineOutput"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function setPrompt(p) {
            document.getElementById('promptInput').value = p;
        }

        async function ingestRepo() {
            const path = document.getElementById('repoPath').value.trim();
            const btn = document.getElementById('ingestBtn');
            const btnText = document.getElementById('ingestBtnText');
            btn.disabled = true;
            btnText.innerHTML = '<span class="spinner"></span> Ingesting...';

            try {
                const res = await fetch('/api/ingest', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ repo_path: path })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Ingestion failed');

                document.getElementById('statFiles').innerText = data.files_count;
                document.getElementById('statLines').innerText = data.total_lines;
                document.getElementById('statChunks').innerText = data.chunks_count;
                document.getElementById('ingestStats').classList.remove('hidden');
            } catch (err) {
                alert('Ingestion error: ' + err.message);
            } finally {
                btn.disabled = false;
                btnText.innerText = 'Ingest Repository';
            }
        }

        async function runPipeline() {
            const prompt = document.getElementById('promptInput').value.trim();
            if (!prompt) return alert("Please enter a query or prompt");

            const btn = document.getElementById('runBtn');
            const btnText = document.getElementById('runBtnText');
            btn.disabled = true;
            btnText.innerHTML = '<span class="spinner"></span> Executing 5 Phases...';

            const resultsContainer = document.getElementById('resultsContainer');
            resultsContainer.classList.remove('hidden');

            try {
                const res = await fetch('/api/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: prompt,
                        repo_path: document.getElementById('repoPath').value.trim()
                    })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Pipeline failed');

                // Render Verdict Banner
                const banner = document.getElementById('verdictBanner');
                banner.className = `verdict-banner ${data.verdict}`;
                
                const icon = data.verdict === 'ALLOWED' ? '🟢' : (data.verdict === 'NEEDS_REVIEW' ? '🟡' : '🔴');
                document.getElementById('verdictIcon').innerText = icon;
                document.getElementById('verdictText').innerText = `GOVERNANCE VERDICT: ${data.verdict}`;
                document.getElementById('pipelineDuration').innerText = `${data.duration_ms} ms`;

                // Render Phases Stepper
                const phasesDiv = document.getElementById('phasesContainer');
                phasesDiv.innerHTML = data.phases.map(p => `
                    <div class="phase-row">
                        <div class="phase-left">
                            <div class="phase-num">${p.phase_number}</div>
                            <div>
                                <div class="phase-name">${p.name}</div>
                                <div class="phase-desc">${p.details}</div>
                            </div>
                        </div>
                        <div style="display:flex; align-items:center; gap:12px;">
                            <span style="font-size:12px; color:var(--text-muted); font-family:'JetBrains Mono';">${p.duration_ms}ms</span>
                            <span class="status-badge ${p.status}">${p.status}</span>
                        </div>
                    </div>
                `).join('');

                // Render Markdown Output
                const outputDiv = document.getElementById('pipelineOutput');
                outputDiv.innerHTML = marked.parse(data.output);
            } catch (err) {
                alert('Pipeline error: ' + err.message);
            } finally {
                btn.disabled = false;
                btnText.innerText = 'Run 5-Phase Pipeline';
            }
        }

        window.addEventListener('DOMContentLoaded', () => {
            ingestRepo();
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=HTML_PAGE)

@app.post("/api/ingest")
def api_ingest(req: IngestRequest):
    global CURRENT_REPO_DATA
    try:
        data = ingest_repository(req.repo_path)
        CURRENT_REPO_DATA = data
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/run")
def api_run(req: RunRequest):
    global CURRENT_REPO_DATA
    if not CURRENT_REPO_DATA or (req.repo_path and os.path.abspath(req.repo_path) != CURRENT_REPO_DATA.get("repo_path")):
        try:
            CURRENT_REPO_DATA = ingest_repository(req.repo_path or "../kavach/demo_repo")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Ingestion failed: {e}")

    try:
        result = run_governed_pipeline(CURRENT_REPO_DATA, req.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Kavach Governed Pipeline Web App at http://localhost:8765")
    uvicorn.run("app:app", host="127.0.0.1", port=8765, reload=False)
