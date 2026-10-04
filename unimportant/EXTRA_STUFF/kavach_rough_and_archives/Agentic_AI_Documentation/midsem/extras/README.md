# AGENTIC AI (CSE3101) — COMPLETE ACADEMIC DOCUMENTATION MASTER FOLDER
**Course:** CSE3101 — Agentic AI (7th Semester, Academic Year 2026–27)  
**Institution:** BML Munjal University, School of Engineering & Technology  
**Course Faculty:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Platform Name:** KAVACH (Security-Governed Multi-Agent AI DevOps & Observability Platform)  

---

## Folder Overview

This folder contains **all official documentation, submission artifacts, empirical benchmark studies, and viva defense guides** specifically prepared for the **Agentic AI (CSE3101)** course, strictly organized according to the faculty's project guidelines and evaluation rubrics.

```
Agentic_AI_Documentation/
│
├── 1. PHASE 1 FORMAL SUBMISSIONS (10% Evaluation — September 3rd Week)
│   ├── PHASE_1_PROJECT_CHARTER.md          # 1-Page Project Charter & Synopsis (C1–C5 Rubrics)
│   ├── PROJECT_TIMELINE_CSE3101.md         # 16-Week Gantt Timeline mapped to CSE3101 syllabus
│   ├── TEAM_RESPONSIBILITY_MATRIX.md       # RACIS matrix with role rotation across all 3 phases
│   └── VIVA_DEFENSE_AND_EVALUATION_GUIDE.md# 10 comprehensive viva questions & answers for evaluators
│
├── 2. CHAPTER SPECIFICATIONS & ACADEMIC REQUIREMENTS
│   ├── PEAS_AND_PERSONA_SPECIFICATION.md   # Chapter 1: Formal PEAS matrix, domain space, 5 Agent & 4 User Personas
│   ├── PROMPT_STRATEGIES_AND_RAG_STUDY.md  # Chapter 2: ReAct vs COTS vs CoT vs Zero-Shot prompting & Qdrant RAG
│   └── CRITICAL_PLAY_AREAS_EVALUATION.md   # Slides 4 & 5: LLM parameters, MAS architectures, MCP vs P2P, bottlenecks
│
├── 3. EMPIRICAL RUNS & LOGS (Slide 2 Row 5 Requirement)
│   └── 42_RUNS_EVALUATION_DATASET.md       # Summary & traces of 42 persistent runs in workflow_runs.json
│
└── 4. ARCHITECTURAL MASTER BLUEPRINT
    └── KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md# 500+ line exhaustive technical specification & roadmap
```

---

## Document Index & Quick Reference

| Document | Purpose & Faculty Alignment | Mapped Rubric / Slide |
| :--- | :--- | :--- |
| [PHASE_1_PROJECT_CHARTER.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/PHASE_1_PROJECT_CHARTER.md) | Official 1-page charter summarizing problem statement, objectives, and tech stack. | Syllabus Page 5 (Phase 1 Submissions) |
| [PROJECT_TIMELINE_CSE3101.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/PROJECT_TIMELINE_CSE3101.md) | Detailed 16-week timeline across Phase 1, Phase 2, and Phase 3. | Syllabus Page 5 (Timeline Requirement) |
| [TEAM_RESPONSIBILITY_MATRIX.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/TEAM_RESPONSIBILITY_MATRIX.md) | RACIS matrix demonstrating role rotation to satisfy the university's "no-silo" policy. | Syllabus Page 7 (Team Responsibility) |
| [PEAS_AND_PERSONA_SPECIFICATION.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/PEAS_AND_PERSONA_SPECIFICATION.md) | Formal PEAS framework and explicit linkage between system runs and 4 Target User Personas. | Slide 2 Row 1 (Chapter 1 Foundations) |
| [PROMPT_STRATEGIES_AND_RAG_STUDY.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/PROMPT_STRATEGIES_AND_RAG_STUDY.md) | Experimental comparison of ReAct, COTS, and CoT prompting strategies alongside Qdrant RAG. | Slide 2 Row 2 (Chapter 2 Prompt Strategy) |
| [CRITICAL_PLAY_AREAS_EVALUATION.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/CRITICAL_PLAY_AREAS_EVALUATION.md) | In-depth answers and benchmark tables for LLM selection, MAS patterns, MCP vs P2P, and bottlenecks. | Slides 4 & 5 (Critical Play Areas) |
| [42_RUNS_EVALUATION_DATASET.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/42_RUNS_EVALUATION_DATASET.md) | Telemetry, stats, and representative traces of the 42 runs in `kavach/backend/data/workflow_runs.json`. | Slide 2 Row 5 (At least 40 runs) |
| [VIVA_DEFENSE_AND_EVALUATION_GUIDE.md](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/Agentic_AI_Documentation/VIVA_DEFENSE_AND_EVALUATION_GUIDE.md) | Model answers for viva questions on deterministic safety, AST graphs, MCP, and ReAct loops. | Final Viva & Faculty Q&A |

---

## Live Verification Commands

To demonstrate the working platform to Dr. Soharab or Mr. Pranshu:
1. **Start the API:**
   ```bash
   cd kavach/backend
   python -m uvicorn app.main:app --reload
   ```
2. **Start the Dashboard:**
   ```bash
   cd kavach/frontend
   python -m http.server 5500
   ```
3. **Verify the 42 Runs:**
   ```bash
   curl http://127.0.0.1:8000/agent/runs
   ```
4. **Run the Full Test Suite (220 Tests Passing):**
   ```bash
   cd kavach
   python run_tests.py
   ```
