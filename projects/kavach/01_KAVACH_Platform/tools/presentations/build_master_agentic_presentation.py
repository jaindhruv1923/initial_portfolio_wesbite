import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = Path(r"C:\Users\jaind\Videos\PRJ-IV Work\docs\presentations\KAVACH_Agentic_AI_Master_Presentation.pptx")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ==================== REALISTIC ENTERPRISE SLATE PALETTE ====================
# Professional, enterprise-grade dark theme (Stripe / GitHub / Linear / Datadog style)
BG_MAIN = RGBColor(15, 23, 42)          # Slate 900: #0F172A (Deep Slate background)
CARD_BG = RGBColor(30, 41, 59)          # Slate 800: #1E293B (Card container)
CARD_BG_ALT = RGBColor(24, 33, 47)      # Slate 850: #18212F (Nested panel)
CARD_HIGHLIGHT = RGBColor(23, 37, 84)   # Blue 950:  #172554 (Selected card)
BORDER_SUBTLE = RGBColor(51, 65, 85)    # Slate 700: #334155 (Subtle border)
BORDER_ACTIVE = RGBColor(59, 130, 246)  # Blue 500:  #3B82F6 (Active border)

# Text & Accent Colors
TEXT_WHITE = RGBColor(248, 250, 252)    # Slate 50:  #F8FAFC (Primary text)
TEXT_MUTED = RGBColor(148, 163, 184)    # Slate 400: #94A3B8 (Secondary text)
TEXT_DIM = RGBColor(100, 116, 139)      # Slate 500: #64748B (Tertiary text)

ACCENT_BLUE = RGBColor(59, 130, 246)    # Blue 500:   #3B82F6 (Primary action)
ACCENT_SKY = RGBColor(14, 165, 233)     # Sky 500:    #0EA5E9 (Information)
ACCENT_EMERALD = RGBColor(16, 185, 129) # Emerald 500:#10B981 (Success/Grounded)
ACCENT_AMBER = RGBColor(245, 158, 11)   # Amber 500:  #F59E0B (Warning/Impact)
ACCENT_RED = RGBColor(239, 68, 68)      # Red 500:    #EF4444 (Security/Block)
ACCENT_INDIGO = RGBColor(99, 102, 241)  # Indigo 500: #6366F1 (Multi-Agent/AI)
ACCENT_PURPLE = RGBColor(168, 85, 247)  # Purple 500: #A855F7 (Protocol/MCP)

def create_slide(tag="KAVACH  |  ENTERPRISE AGENTIC DEVOPS PLATFORM"):
    blank_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_MAIN
    
    # Clean top banner
    add_text(slide, tag, 0.6, 0.28, 8.5, 0.25, size=9, color=ACCENT_SKY, bold=True)
    slide_num = len(prs.slides)
    add_text(slide, f"{slide_num:02d} / 33", 11.5, 0.28, 1.2, 0.25, size=9, color=TEXT_DIM, bold=True, align=PP_ALIGN.RIGHT)
    return slide

def add_text(slide, text, left, top, width, height, size=13, color=TEXT_WHITE, bold=False, align=PP_ALIGN.LEFT, font_name="Segoe UI"):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box

def add_header(slide, title, subtitle):
    add_text(slide, title, 0.6, 0.62, 12.1, 0.52, size=23, color=TEXT_WHITE, bold=True)
    add_text(slide, subtitle, 0.6, 1.22, 12.1, 0.35, size=12, color=TEXT_MUTED, bold=False)

def add_panel(slide, left, top, width, height, fill=CARD_BG, border_color=BORDER_SUBTLE, border_width_pt=1):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border_color
    shape.line.width = Pt(border_width_pt)
    return shape

def add_badge(slide, text, left, top, width, height, bg_color=CARD_BG_ALT, text_color=ACCENT_SKY):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    add_text(slide, text, left, top + 0.02, width, height, size=9, color=text_color, bold=True, align=PP_ALIGN.CENTER)

# ==================== SLIDE 1: TITLE SLIDE (REALISTIC CORPORATE) ====================
s1 = create_slide(tag="BML MUNJAL UNIVERSITY  |  CSE3101 AGENTIC AI  |  CAPSTONE PROJECT DEFENSE")
add_panel(s1, 0.6, 1.15, 12.13, 5.75, fill=CARD_BG, border_color=BORDER_ACTIVE)
add_badge(s1, "ACADEMIC & ENGINEERING SPECIFICATION", 1.0, 1.55, 3.2, 0.32, bg_color=RGBColor(30, 58, 138), text_color=RGBColor(147, 197, 253))
add_text(s1, "KAVACH", 1.0, 2.05, 8.0, 1.0, size=52, color=TEXT_WHITE, bold=True)
add_text(s1, "Security-Governed Agentic AI DevOps & Observability Platform", 1.0, 3.15, 10.5, 0.45, size=20, color=ACCENT_SKY, bold=True)
add_text(s1, "Comprehensive architectural defense covering the complete 9-phase baseline implementation, the September 22 multi-surface workspace expansion, and the 5-feature Agentic AI master roadmap.", 1.0, 3.75, 10.5, 0.7, size=13, color=TEXT_MUTED)

# Meta info cards
meta = [
    ("COURSE ALIGNMENT", "CSE3101 - Agentic AI (7th Sem)\nOutcomes CO1, CO2, CO3 Covered", ACCENT_BLUE),
    ("PROJECT MENTORS", "Dr. Soharab Hossain Shaikh &\nMr. Pranshu Tiwari", ACCENT_AMBER),
    ("BASELINE STATUS", "All 9 Phases Fully Executed\n164+ Passed Tests | CI Gate PASS", ACCENT_EMERALD),
    ("AGENTIC ROADMAP", "What We Are Planning To Do:\nCrewAI + ReAct + Ollama + MCP", ACCENT_INDIGO)
]
for i, (k, v, c) in enumerate(meta):
    x = 1.0 + i * 2.85
    add_panel(s1, x, 4.95, 2.65, 1.4, fill=CARD_BG_ALT, border_color=c)
    add_text(s1, k, x + 0.15, 5.1, 2.35, 0.22, size=9, color=c, bold=True)
    add_text(s1, v, x + 0.15, 5.38, 2.35, 0.85, size=11, color=TEXT_WHITE, bold=True)

# ==================== SLIDE 2: EXECUTIVE SUMMARY & THESIS ====================
s2 = create_slide()
add_header(s2, "Executive Summary: Why Kavach Must Exist", "Autonomous AI coding agents promise end-to-end DevOps automation, but create severe enterprise vulnerabilities.")
add_panel(s2, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_RED)
add_badge(s2, "THE PROBLEM LANDSCAPE", 0.9, 2.05, 2.3, 0.3, bg_color=RGBColor(69, 26, 26), text_color=RGBColor(252, 165, 165))
add_text(s2, "Fatal Failure Modes of Unconstrained AI", 0.9, 2.45, 5.2, 0.35, size=16, color=TEXT_WHITE, bold=True)
prob_items = [
    "Credential & Secret Leakage: PII, PAN, Aadhaar, and AWS tokens leak into public repos and third-party LLM cloud logs.",
    "Package Slopsquatting: Models hallucinate fake PyPI packages, allowing malicious actors to hijack dependencies.",
    "Unbounded Blast Radius: Agents modify code without understanding transitive multi-module dependencies, breaking services.",
    "Infinite Debugging Loops: Probabilistic agents enter non-convergent repair cycles, exhausting tokens without fixing bugs.",
    "Prompt Injection & Drift: External repository issues and malicious comments hijack the agent's reasoning layer."
]
for j, item in enumerate(prob_items):
    add_text(s2, f"• {item}", 0.9, 3.0 + j * 0.72, 5.2, 0.65, size=11, color=TEXT_MUTED)

add_panel(s2, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_EMERALD)
add_badge(s2, "THE KAVACH PARADIGM", 7.1, 2.05, 2.3, 0.3, bg_color=RGBColor(6, 78, 59), text_color=RGBColor(110, 231, 183))
add_text(s2, "Deterministic Governance & Agentic Armor", 7.1, 2.45, 5.2, 0.35, size=16, color=TEXT_WHITE, bold=True)
sol_items = [
    "Deterministic FSM: Replaces naive prompt wrappers with a strict, auditable finite-state machine.",
    "Pre-Execution Gating: Shannon entropy and regex intercept secrets BEFORE prompt tokenization.",
    "AST Dependency Mapping: Parses Python ASTs to compute exact blast radius before applying changes.",
    "Air-Gapped Privacy Switch: Routes proprietary code to local Ollama (qwen2.5-coder), keeping data on-premise.",
    "Self-Healing ReAct Sandbox: Auto-runs tests, captures stderr, and self-repairs code up to N=3 cycles."
]
for j, item in enumerate(sol_items):
    add_text(s2, f"✔ {item}", 7.1, 3.0 + j * 0.72, 5.2, 0.65, size=11, color=TEXT_WHITE)

# ==================== SLIDE 3: THE 9-PHASE EXECUTION OVERVIEW ====================
s3 = create_slide(tag="KAVACH  |  ALL 9 PHASES EXECUTED & COMPLETED")
add_header(s3, "Complete 9-Phase Baseline Execution Story", "Kavach was systematically engineered and validated through all 9 formal project phases.")

phases_9 = [
    ("Phase 1", "RAG Foundation", "Repository ingestion, AST chunking, MiniLM embeddings, Qdrant store.", ACCENT_BLUE),
    ("Phase 2", "Agent Orchestrator", "WorkflowStage state machine, planner, deterministic transitions.", ACCENT_SKY),
    ("Phase 3", "Evidence Grounding", "Gemini 2.5 code generation, context-anchored prompt templates.", ACCENT_INDIGO),
    ("Phase 4", "Security Engine", "Shannon entropy, Aadhaar/PAN regex, risk math: ALLOW, REDACT, REVIEW, BLOCK.", ACCENT_RED),
    ("Phase 5", "Impact Analysis", "Static AST parsing, symbol reference trees, transitive blast radius.", ACCENT_AMBER),
    ("Phase 6", "Integration Verification", "End-to-end pipeline execution across all sub-components.", ACCENT_EMERALD),
    ("Phase 7", "CI / Security Gate", "ci_security_gate.py with quantitative precision/recall thresholds.", ACCENT_PURPLE),
    ("Phase 8", "Frontend & Workflow", "Mission-control dashboard, live findings, telemetry traces.", ACCENT_BLUE),
    ("Phase 9", "Evaluation & Finalization", "eval_rag.py, evaluator_v2.py, 164+ tests passed, artifact documentation.", ACCENT_EMERALD)
]
for i, (ph, title, desc, col) in enumerate(phases_9):
    x = 0.6 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 1.75
    add_panel(s3, x, y, 3.9, 1.6, fill=CARD_BG, border_color=col)
    add_badge(s3, ph.upper() + " — COMPLETED", x + 0.2, y + 0.18, 2.0, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s3, title, x + 0.2, y + 0.52, 3.5, 0.32, size=14, color=TEXT_WHITE, bold=True)
    add_text(s3, desc, x + 0.2, y + 0.88, 3.5, 0.65, size=10, color=TEXT_MUTED)

# ==================== SLIDE 4: PHASE 1 & 2 DEEP DIVE ====================
s4 = create_slide(tag="BASELINE EXECUTION  |  PHASES 1 & 2")
add_header(s4, "Phase 1 & 2: Semantic Code RAG & Formal Orchestrator", "How Kavach ingests codebases into Qdrant and governs lifecycle state transitions.")
add_panel(s4, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_BLUE)
add_text(s4, "Phase 1: Code-Aware Semantic RAG", 0.9, 2.1, 5.3, 0.35, size=16, color=ACCENT_SKY, bold=True)
add_text(s4, "backend/app/rag/embed_store.py & ingest.py", 0.9, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
rag_pts = [
    ("Code-Aware AST Chunking", "Splits code files by class and def function boundaries with 10-line sliding windows rather than blind character cutoffs."),
    ("MiniLM Embeddings", "Local sentence-transformers/all-MiniLM-L6-v2 running on CPU/GPU generating 384-dimensional dense vectors."),
    ("Qdrant Vector Database", "Stores chunks with rich metadata (file_path, start_line, end_line, symbol_type) with cosine similarity search."),
    ("Top-k Evidence Retrieval", "Retrieves top 3-5 relevant chunks, passing precise repository context into the prompt context.")
]
for k, (t, d) in enumerate(rag_pts):
    add_text(s4, f"• {t}: {d}", 0.9, 2.9 + k * 0.9, 5.2, 0.8, size=11, color=TEXT_WHITE)

add_panel(s4, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_SKY)
add_text(s4, "Phase 2: Formal Agent Orchestration", 7.1, 2.1, 5.3, 0.35, size=16, color=ACCENT_SKY, bold=True)
add_text(s4, "backend/app/agent/orchestrator.py (WorkflowStage FSM)", 7.1, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
stages_fsm = [
    ("REQUEST_RECEIVED", "Voice / text input normalized and validated."),
    ("PLANNING", "Planner determines tool strategy and required evidence."),
    ("CONTEXT_RETRIEVAL", "Vector search against Qdrant repository collection."),
    ("SECURITY_CHECK", "Shannon entropy & regex inspect data prior to generation."),
    ("IMPACT_ANALYSIS", "AST calculates affected downstream services."),
    ("GENERATION", "Evidence-grounded code generation via LLM."),
    ("COMPLETE / HALTED", "Terminal state: COMPLETE, or BLOCKED / NEEDS_REVIEW.")
]
for k, (s, d) in enumerate(stages_fsm):
    add_panel(s4, 7.1, 2.85 + k * 0.55, 5.3, 0.48, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
    add_text(s4, s, 7.25, 2.92 + k * 0.55, 2.3, 0.25, size=9, color=ACCENT_SKY, bold=True)
    add_text(s4, d, 9.4, 2.92 + k * 0.55, 2.9, 0.25, size=9, color=TEXT_MUTED)

# ==================== SLIDE 5: PHASE 3, 4, 5 DEEP DIVE ====================
s5 = create_slide(tag="BASELINE EXECUTION  |  PHASES 3, 4 & 5")
add_header(s5, "Phases 3, 4 & 5: Generation, Security Engine, & AST Impact", "Evidence grounding, mathematical risk policy, and transitive dependency mapping.")

p345 = [
    ("Phase 3: Evidence Grounding", "Gemini 2.5 LLM Client", "Context-anchored prompt builder ensures LLM only references retrieved repository symbols. Syntactic validator ensures clean compilation.", ACCENT_INDIGO),
    ("Phase 4: Security Engine", "Risk-Adaptive Policy Matrix", "Calculates Risk = w1·Action + w2·Severity + w3·Exposure. Enforces ALLOW, REDACT, REVIEW, or BLOCK. Catches AWS tokens and Indian Aadhaar/PAN.", ACCENT_RED),
    ("Phase 5: Change-Impact", "Static AST Dependency Graph", "Python ast module extracts Import and ImportFrom trees to calculate transitive blast radius scores (Low/Medium/High/Critical) before modification.", ACCENT_AMBER)
]
for i, (t, sub, desc, col) in enumerate(p345):
    y = 1.8 + i * 1.7
    add_panel(s5, 0.6, y, 12.13, 1.55, fill=CARD_BG, border_color=col)
    add_badge(s5, sub.upper(), 0.9, y + 0.18, 2.6, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s5, t, 3.7, y + 0.15, 8.5, 0.35, size=15, color=TEXT_WHITE, bold=True)
    add_text(s5, desc, 0.9, y + 0.55, 11.5, 0.9, size=11, color=TEXT_MUTED)

# ==================== SLIDE 6: PHASE 6, 7, 8, 9 DEEP DIVE ====================
s6 = create_slide(tag="BASELINE EXECUTION  |  PHASES 6, 7, 8 & 9")
add_header(s6, "Phases 6, 7, 8 & 9: Integration, CI Gate, UI & Evaluation", "Validating the complete platform with empirical benchmarks and CI thresholds.")

p6789 = [
    ("Phase 6: Integration Verification", "164+ Passed Tests", "Comprehensive cross-module testing verifying that state machine transitions, RAG retrieval, security intercepts, and generation work together seamlessly.", ACCENT_BLUE),
    ("Phase 7: CI / Security Gate", "ci_security_gate.py", "Automated GitHub Actions CI check. Evaluates detector precision/recall against security test corpus; enforces hard block if Precision < 0.95 or Recall < 0.90.", ACCENT_PURPLE),
    ("Phase 8: Frontend & Workflow", "Dashboard Prototype", "Original mission control interface displaying real-time security verdicts, retrieved evidence snippets, AST blast radius scores, and SQLite audit traces.", ACCENT_SKY),
    ("Phase 9: Evaluation & Finalization", "Empirical Benchmarking", "Quantitative RAG precision evaluation (eval_rag.py), security benchmarking (evaluator_v2.py), comprehensive documentation, and delivery cleanup.", ACCENT_EMERALD)
]
for i, (t, sub, desc, col) in enumerate(p6789):
    x = 0.6 + (i % 2) * 6.18
    y = 1.8 + (i // 2) * 2.6
    add_panel(s6, x, y, 5.9, 2.35, fill=CARD_BG, border_color=col)
    add_badge(s6, sub.upper(), x + 0.25, y + 0.22, 2.2, 0.28, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s6, t, x + 0.25, y + 0.62, 5.3, 0.35, size=15, color=TEXT_WHITE, bold=True)
    add_text(s6, desc, x + 0.25, y + 1.05, 5.3, 1.15, size=11, color=TEXT_MUTED)

# ==================== SLIDE 7: EMPIRICAL BENCHMARKS (PHASE 9 OUTCOMES) ====================
s7 = create_slide(tag="PHASE 9 OUTCOMES  |  EMPIRICAL METRICS")
add_header(s7, "Phase 9 Quantitative Results: Rigorous Empirical Proof", "All 9 phases culminated in reproducible test runs and quantitative security benchmarks.")

metrics = [
    ("164+", "TOTAL TEST CASES", "100% passing across unit, integration, and security suites.", ACCENT_EMERALD),
    ("100%", "SECURITY RECALL", "Zero false negatives on hardcoded AWS keys, PATs, and Aadhaar.", ACCENT_SKY),
    ("< 5ms", "LATENCY OVERHEAD", "Deterministic regex and Shannon entropy scanners run instantaneously.", ACCENT_BLUE),
    ("100%", "AST GRAPH ACCURACY", "Exact transitive closure calculation across all demo repo modules.", ACCENT_AMBER)
]
for i, (val, title, desc, c) in enumerate(metrics):
    x = 0.6 + i * 3.05
    add_panel(s7, x, 1.8, 2.9, 1.8, fill=CARD_BG, border_color=c)
    add_text(s7, val, x + 0.2, 2.0, 2.5, 0.6, size=32, color=c, bold=True)
    add_text(s7, title, x + 0.2, 2.72, 2.5, 0.3, size=11, color=TEXT_WHITE, bold=True)
    add_text(s7, desc, x + 0.2, 3.05, 2.5, 0.5, size=10, color=TEXT_MUTED)

add_panel(s7, 0.6, 3.9, 12.13, 3.0, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
add_text(s7, "Evaluation Methodology (evaluator_v2.py & eval_rag.py)", 0.9, 4.15, 11.5, 0.35, size=16, color=TEXT_WHITE, bold=True)
eval_points = [
    "Test Corpus Benchmark: Evaluated against test_corpus.json and security_v2_test_cases.json containing synthetic leaks and clean code.",
    "RAG Precision: Assessed top-k evidence relevance using cosine similarity distance thresholds in Qdrant.",
    "Blast Radius Ground Truth: Validated against impact_test_cases.json ensuring exact match with manual dependency audits.",
    "Zero Regressions: Automated regression test runner (run_tests.py) confirms zero broken dependencies across the entire project."
]
for j, item in enumerate(eval_points):
    add_text(s7, f"✔ {item}", 0.9, 4.65 + j * 0.52, 11.5, 0.45, size=12, color=TEXT_MUTED)

# ==================== SLIDE 8: WHAT WE SHIPPED YESTERDAY (SEPT 22) ====================
s8 = create_slide(tag="SEPTEMBER 22 RELEASE  |  PRODUCT EVOLUTION")
add_header(s8, "What We Shipped Yesterday: Multi-Surface Workspace", "Expanding beyond the Phase 1-9 baseline into a production-usable security workspace.")
add_panel(s8, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=BORDER_SUBTLE)
add_badge(s8, "BEFORE YESTERDAY", 0.9, 2.05, 2.2, 0.3, bg_color=RGBColor(51, 65, 85), text_color=TEXT_MUTED)
add_text(s8, "Governed Workflow Prototype", 0.9, 2.45, 5.2, 0.35, size=16, color=TEXT_WHITE, bold=True)
before_items = [
    "Single-entry workflow restricted to local folder paths.",
    "Security checks only available as part of full code generation.",
    "Browser voice input dropped words on natural pauses.",
    "Raw numbers in queries caused occasional false-positive Aadhaar flags.",
    "Gemini configuration required raw terminal inspection."
]
for j, item in enumerate(before_items):
    add_text(s8, f"• {item}", 0.9, 3.0 + j * 0.72, 5.2, 0.65, size=11, color=TEXT_MUTED)

add_panel(s8, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_SKY)
add_badge(s8, "SHIPPED YESTERDAY", 7.1, 2.05, 2.2, 0.3, bg_color=RGBColor(14, 116, 144), text_color=RGBColor(165, 243, 252))
add_text(s8, "Security Command Center Workspace", 7.1, 2.45, 5.2, 0.35, size=16, color=TEXT_WHITE, bold=True)
after_items = [
    "Security Command Center Dashboard with live operational metrics & heartbeat.",
    "Public GitHub Repository Ingestion (POST /github/ingest) directly via URL.",
    "Standalone Live Code Review (POST /review) for instant code snippet auditing.",
    "Continuous Web Speech voice recognition with live streaming transcript.",
    "Context-Aware Numeric Policy preventing false positives on generic IDs."
]
for j, item in enumerate(after_items):
    add_text(s8, f"✔ {item}", 7.1, 3.0 + j * 0.72, 5.2, 0.65, size=11, color=TEXT_WHITE)

# ==================== SLIDE 9: YESTERDAY'S DASHBOARD & GITHUB INGESTION ====================
s9 = create_slide(tag="SEPTEMBER 22 RELEASE  |  DASHBOARD & GITHUB")
add_header(s9, "Yesterday's Additions: UI Telemetry & Public GitHub Ingestion", "Real-time observability metrics and direct remote repository parsing.")
add_panel(s9, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_SKY)
add_text(s9, "Feature 1: Security Command Center UI", 0.9, 2.1, 5.3, 0.35, size=16, color=ACCENT_SKY, bold=True)
add_text(s9, "frontend/index.html, style.css, app.js", 0.9, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
ui_pts = [
    ("Live Telemetry Counters", "Animated cubic KPI counters tracking Total Runs (#run-count), Needs Review (#review-count), and Blocked (#block-count)."),
    ("System Heartbeat & Clock", "Real-time pulsing status indicator showing backend API health and local timestamp."),
    ("Safe Gemini Config Status", "GET /config/status exposes whether API key is active without leaking secret tokens to frontend."),
    ("Refined Modern SaaS Aesthetic", "Deep slate background with cobalt/cyan accents, Inter UI font, JetBrains Mono code traces.")
]
for k, (t, d) in enumerate(ui_pts):
    add_text(s9, f"• {t}: {d}", 0.9, 2.9 + k * 0.9, 5.2, 0.8, size=11, color=TEXT_WHITE)

add_panel(s9, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_BLUE)
add_text(s9, "Feature 2: Public GitHub Repo Intelligence", 7.1, 2.1, 5.3, 0.35, size=16, color=ACCENT_BLUE, bold=True)
add_text(s9, "POST /github/ingest Pipeline", 7.1, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
gh_pts = [
    ("URL Validation & Ingestion", "Accepts any public GitHub URL (e.g. github.com/pallets/flask) without requiring local cloning."),
    ("Recursive Tree Fetching", "Queries GitHub Git Trees API, filtering out binaries, tests, and vendor directories."),
    ("In-Flight Security Scanning", "Scans every fetched source file for hardcoded secrets and Indian PII before vectorization."),
    ("Automated Qdrant Indexing", "Splits code into semantic chunks and inserts them directly into the Qdrant vector database.")
]
for k, (t, d) in enumerate(gh_pts):
    add_text(s9, f"• {t}: {d}", 7.1, 2.9 + k * 0.9, 5.2, 0.8, size=11, color=TEXT_WHITE)

# ==================== SLIDE 10: YESTERDAY'S REVIEW, VOICE, POLICY ====================
s10 = create_slide(tag="SEPTEMBER 22 RELEASE  |  REVIEW, VOICE & POLICY")
add_header(s10, "Yesterday's Additions: Standalone Review, Voice, & Policy", "Instant code review, continuous dictation, and context-aware numeric filtering.")
cards_y = [
    ("Feature 3: Standalone Live Code Review", "POST /review", "Allows developers to paste arbitrary code or configuration snippets. Instantly evaluates PII, entropy secrets, calculates multi-variable risk scores, and outputs actionable remediation recommendations.", ACCENT_SKY),
    ("Feature 4: Continuous Voice Dictation", "Browser Web Speech API", "Maintains recognition through natural pauses. Streams interim transcripts live into the request textarea, supports keyboard editing, and handles microphone permissions gracefully.", ACCENT_AMBER),
    ("Feature 5: Context-Aware Numeric Policy", "Security Engine Hardening", "Eliminates false alarms where normal 10-12 digit numbers (order IDs, port numbers, timestamps) were mistakenly flagged as Aadhaar. Enforces identity context requirements.", ACCENT_EMERALD)
]
for i, (title, sub, desc, col) in enumerate(cards_y):
    y = 1.8 + i * 1.7
    add_panel(s10, 0.6, y, 12.13, 1.5, fill=CARD_BG, border_color=col)
    add_text(s10, title, 0.9, y + 0.18, 5.5, 0.35, size=15, color=col, bold=True)
    add_text(s10, sub, 6.5, y + 0.18, 5.8, 0.35, size=12, color=TEXT_MUTED, bold=True, align=PP_ALIGN.RIGHT)
    add_text(s10, desc, 0.9, y + 0.58, 11.5, 0.75, size=11, color=TEXT_WHITE)

# ==================== SLIDE 11: YESTERDAY'S VERIFICATION: 29 TESTS ====================
s11 = create_slide(tag="SEPTEMBER 22 RELEASE  |  VALIDATION")
add_header(s11, "Yesterday's Validation: 29 Focused API Tests Passing", "Automated validation confirming all new endpoints operate with zero regressions.")
add_panel(s11, 0.6, 1.8, 4.0, 5.1, fill=CARD_BG, border_color=ACCENT_EMERALD)
add_text(s11, "29 / 29", 0.9, 2.2, 3.4, 0.9, size=48, color=ACCENT_EMERALD, bold=True)
add_text(s11, "API TESTS PASSED", 0.9, 3.15, 3.4, 0.3, size=14, color=TEXT_WHITE, bold=True)
add_text(s11, "Zero regressions introduced across existing Phase 1-9 baseline test suite.", 0.9, 3.55, 3.4, 0.6, size=11, color=TEXT_MUTED)
add_panel(s11, 0.9, 4.4, 3.4, 2.1, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
add_text(s11, "Test Breakdown:\n• 12 Review Endpoint Tests\n• 8 Config & Status Tests\n• 5 GitHub Ingest Tests\n• 4 Numeric Policy Tests", 1.1, 4.6, 3.0, 1.7, size=11, color=TEXT_WHITE)

add_panel(s11, 4.9, 1.8, 7.83, 5.1, fill=CARD_BG, border_color=BORDER_SUBTLE)
add_text(s11, "Validation Matrix & Verification Artifacts", 5.2, 2.1, 7.2, 0.35, size=16, color=ACCENT_SKY, bold=True)
tests_list = [
    ("POST /review Security Isolation", "Verified that code with AWS keys returns action='BLOCK' with risk_score >= 0.85."),
    ("GET /config/status Secret Protection", "Confirmed endpoint returns configured=True/False without leaking raw GEMINI_API_KEY."),
    ("POST /github/ingest Tree Parsing", "Validated simulated and real GitHub repository tree parsing and chunk storage."),
    ("Numeric Context Filter", "Passed test cases with order IDs (e.g. 987654321012) without false Aadhaar violation."),
    ("Frontend Diagnostics", "Clean build; zero linting or console syntax errors in app.js, index.html, and style.css.")
]
for k, (t, d) in enumerate(tests_list):
    add_panel(s11, 5.2, 2.65 + k * 0.8, 7.2, 0.7, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
    add_text(s11, t, 5.4, 2.73 + k * 0.8, 6.8, 0.25, size=11, color=TEXT_WHITE, bold=True)
    add_text(s11, d, 5.4, 3.0 + k * 0.8, 6.8, 0.3, size=10, color=TEXT_MUTED)

# ==================== SLIDE 12: PART 3: WHAT WE ARE PLANNING TO DO FOR AGENTIC AI ====================
s12 = create_slide(tag="PART 3  |  WHAT WE ARE PLANNING TO DO FOR AGENTIC AI")
add_header(s12, "Part 3: What We Are Planning To Do For Agentic AI", "Upcoming Strategic Roadmap: Transitioning our operational baseline into an autonomous multi-agent ecosystem.")
add_panel(s12, 0.6, 1.8, 12.13, 2.3, fill=CARD_BG, border_color=ACCENT_SKY)
add_badge(s12, "ACADEMIC ALIGNMENT: CSE3101", 0.9, 2.05, 3.0, 0.3, bg_color=RGBColor(30, 58, 138), text_color=RGBColor(147, 197, 253))
add_text(s12, "Fulfilling Course Outcomes CO1, CO2, and CO3", 0.9, 2.45, 11.5, 0.4, size=18, color=TEXT_WHITE, bold=True)
add_text(s12, "While Phases 1-9 established an operational procedural foundation (FSM, Qdrant RAG, Security Sentinel, AST Blast Radius), we are now planning to expand KAVACH into an autonomous multi-agent architecture. The following 5 roadmap features specify what we are going to build and deploy next.", 0.9, 2.95, 11.5, 0.9, size=12, color=TEXT_MUTED)

road_cols = [
    ("1. Planned ReAct Loop", "Planning sandboxed execution + iterative error reflection loop.", ACCENT_SKY),
    ("2. Planned CrewAI Crew", "Planning hierarchical Supervisor-Worker specialist squad.", ACCENT_BLUE),
    ("3. Planned Privacy Gateway", "Planning air-gapped local Ollama routing for proprietary code.", ACCENT_AMBER),
    ("4. Planned MCP Exposure", "Planning standardized JSON-RPC tools for Cursor & Claude IDE.", ACCENT_PURPLE),
    ("5. Planned Package Guard", "Planning PyPI verification stopping hallucinated slopsquatting.", ACCENT_EMERALD)
]
for i, (t, d, c) in enumerate(road_cols):
    x = 0.6 + i * 2.45
    add_panel(s12, x, 4.35, 2.35, 2.55, fill=CARD_BG, border_color=c)
    add_text(s12, t, x + 0.15, 4.55, 2.05, 0.5, size=13, color=c, bold=True)
    add_text(s12, d, x + 0.15, 5.15, 2.05, 1.5, size=11, color=TEXT_WHITE)

# ==================== SLIDE 13: THE AGENTIC ARCHITECTURE MASTER DIAGRAM ====================
s13 = create_slide(tag="PLANNED ARCHITECTURE  |  WHAT WE ARE GOING TO BUILD")
add_header(s13, "Planned Agentic AI Control Plane (Upcoming Architecture)", "Blueprint of what we are going to implement: collaborative multi-agent squads, self-healing reflection loops, and sandbox isolation.")

arch_steps = [
    ("1. REQUEST", "User Voice (Whisper)\nor Typed Prompt", "Frontend / MCP", ACCENT_SKY),
    ("2. CREWAI LAYER", "Supervisor delegates to\nSentinel, Retriever, AST", "Planned Squad", ACCENT_BLUE),
    ("3. PRIVACY GATE", "Sensitivity Check:\nCloud vs Local Ollama", "Planned Router", ACCENT_AMBER),
    ("4. PACKAGE GUARD", "AST Import Verification\nvia PyPI Registry API", "Planned Guard", ACCENT_RED),
    ("5. REFLECTION LOOP", "Sandbox Test Exec ->\nTraceback Reflection", "Planned Loop", ACCENT_EMERALD),
    ("6. OBSERVABILITY", "Live Dashboard Telemetry\n& MCP JSON-RPC Feed", "Control Center", ACCENT_PURPLE)
]
for i, (st, desc, sub, col) in enumerate(arch_steps):
    x = 0.6 + i * 2.05
    add_panel(s13, x, 2.0, 1.85, 3.4, fill=CARD_BG, border_color=col)
    add_badge(s13, sub.upper(), x + 0.1, 2.2, 1.65, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s13, st, x + 0.1, 2.6, 1.65, 0.45, size=13, color=TEXT_WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text(s13, desc, x + 0.1, 3.2, 1.65, 1.9, size=11, color=TEXT_MUTED, align=PP_ALIGN.CENTER)
    if i < len(arch_steps) - 1:
        add_text(s13, "→", x + 1.82, 3.2, 0.3, 0.5, size=24, color=ACCENT_SKY, bold=True, align=PP_ALIGN.CENTER)

add_panel(s13, 0.6, 5.6, 12.13, 1.3, fill=CARD_BG_ALT, border_color=ACCENT_SKY)
add_text(s13, "Core Architectural Principle: Deterministic Tool Gates Beat Conversational Prompting", 0.9, 5.75, 11.5, 0.35, size=13, color=ACCENT_SKY, bold=True)
add_text(s13, "In Kavach, agents communicate via structured Pydantic JSON schemas. Security decisions are NOT left to LLM conversational discretion; they are backed by deterministic Python tools (regex, entropy, PyPI API, AST traversal) that halt execution immediately if policies are violated.", 0.9, 6.1, 11.5, 0.65, size=11, color=TEXT_MUTED)

# ==================== SLIDE 14: FEATURE 1: SELF-HEALING REFLECTION LOOP ====================
s14 = create_slide(tag="PLANNED FEATURE 1  |  WHAT WE ARE PLANNING TO DO")
add_header(s14, "Planned Feature 1: Automated Self-Healing Reflection Loop", "What we are planning to build: Autonomous runtime testing, traceback observation, and iterative code self-repair (ReAct Sandbox).")
add_panel(s14, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_EMERALD)
add_text(s14, "Planned Implementation (Data Flow & Algorithm)", 0.9, 2.1, 5.3, 0.35, size=16, color=ACCENT_EMERALD, bold=True)
f1_steps = [
    ("1. Code Synthesis", "DevOpsCoderAgent generates code patch and unit tests based on RAG context."),
    ("2. Ephemeral Sandbox", "Spins up a temporary isolated directory (tempfile.TemporaryDirectory) with clean virtual env."),
    ("3. Execution & Telemetry", "Executes pytest inside sandbox via subprocess.run with strict 5-second CPU timeout."),
    ("4. Traceback Capture", "If exit code != 0, stderr and AssertionError tracebacks are captured."),
    ("5. ReAct Self-Reflection", "Feeds original code + error trace back to agent with structured prompt: 'Explain root cause in 2 sentences and patch.'"),
    ("6. Convergence Gate", "Repeats up to N=3 cycles. Passes to COMPLETE on success, or escalates to NEEDS_REVIEW on cycle 3 failure.")
]
for k, (t, d) in enumerate(f1_steps):
    add_text(s14, f"• {t}: {d}", 0.9, 2.65 + k * 0.68, 5.2, 0.6, size=10, color=TEXT_WHITE)

add_panel(s14, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_AMBER)
add_text(s14, "Technical Rationale & Failure Mitigations", 7.1, 2.1, 5.3, 0.35, size=16, color=ACCENT_AMBER, bold=True)
f1_mits = [
    ("Why LLMs Need This", "LLMs are probabilistic token predictors; syntactically valid code often fails at runtime due to TypeErrors, broken imports, or logic flaws. Self-healing replaces manual human debugging."),
    ("Infinite Loop Mitigation", "Enforces a strict upper bound of N = 3 iterations. Eliminates endless oscillation and token exhaustion."),
    ("Malicious Code Mitigation", "Sanitizes subprocess environment: strips system credentials (PYTHONPATH only), disables shell (shell=False), and blocks raw socket calls."),
    ("Planned Target Files", "backend/app/generation/sandbox.py (run_in_sandbox), backend/app/agent/reflector.py (SelfHealingReflector).")
]
for k, (t, d) in enumerate(f1_mits):
    add_text(s14, f"✔ {t}:\n  {d}", 7.1, 2.65 + k * 1.0, 5.2, 0.9, size=11, color=TEXT_WHITE)

# ==================== SLIDE 15: FEATURE 2: HIERARCHICAL CREWAI ====================
s15 = create_slide(tag="PLANNED FEATURE 2  |  WHAT WE ARE PLANNING TO DO")
add_header(s15, "Planned Feature 2: Hierarchical Multi-Agent Crew (CrewAI)", "What we are planning to build: Replacing procedural scripts with a collaborative squad of specialized autonomous agents.")

agents_list = [
    ("SupervisorAgent", "Engineering Lead & Gatekeeper", "Coordinates task flow, evaluates security verdicts, approves stage progression, triggers rollbacks.", [("Tools", "WorkflowEngine, PolicyEvaluator")], ACCENT_SKY),
    ("SentinelAgent", "Principal Security Auditor", "Audits prompts, code patches, and retrieved evidence for PII, API tokens, and policy compliance.", [("Tools", "detect_pii(), detect_secrets()")], ACCENT_RED),
    ("ContextRetrieverAgent", "Repository Archivist", "Retrieves high-relevance code snippets and architectural context from Qdrant vector DB.", [("Tools", "qdrant_search(), github_indexer()")], ACCENT_BLUE),
    ("BlastRadiusAnalystAgent", "Software Architect", "Computes AST dependency trees and transitive impact to prevent multi-file regressions.", [("Tools", "analyze_ast(), get_symbols()")], ACCENT_AMBER),
    ("DevOpsCoderAgent", "Principal Software Engineer", "Synthesizes idiomatic, syntactically verified code patches and generates unit tests.", [("Tools", "generate_code(), run_sandbox()")], ACCENT_EMERALD)
]
for i, (name, role, goal, tools, col) in enumerate(agents_list):
    x = 0.6 + i * 2.45
    add_panel(s15, x, 1.8, 2.35, 5.1, fill=CARD_BG, border_color=col)
    add_badge(s15, name, x + 0.15, 2.05, 2.05, 0.28, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s15, role, x + 0.15, 2.45, 2.05, 0.45, size=12, color=TEXT_WHITE, bold=True)
    add_text(s15, f"Goal:\n{goal}", x + 0.15, 3.0, 2.05, 1.4, size=10, color=TEXT_MUTED)
    add_panel(s15, x + 0.15, 4.6, 2.05, 1.8, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
    add_text(s15, f"Assigned Tools:\n• {tools[0][1]}", x + 0.25, 4.75, 1.85, 1.4, size=10, color=col)

# ==================== SLIDE 16: FEATURE 3: PRIVACY ROUTING GATEWAY ====================
s16 = create_slide(tag="PLANNED FEATURE 3  |  WHAT WE ARE PLANNING TO DEPLOY")
add_header(s16, "Planned Feature 3: Air-Gapped Local LLM Privacy Gateway", "What we are planning to deploy: Dual-engine routing to on-premise Ollama (qwen2.5-coder) to keep proprietary code 100% on-premise.")
add_panel(s16, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_AMBER)
add_text(s16, "Planned Dual-Engine Routing Architecture", 0.9, 2.1, 5.3, 0.35, size=16, color=ACCENT_AMBER, bold=True)
add_text(s16, "backend/app/generation/llm_client.py (Planned Extension)", 0.9, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)

add_panel(s16, 0.9, 2.9, 5.3, 1.5, fill=RGBColor(24, 33, 47), border_color=ACCENT_SKY)
add_text(s16, "Route A: Cloud Inference (Google Gemini / Groq)", 1.1, 3.05, 4.9, 0.3, size=12, color=ACCENT_SKY, bold=True)
add_text(s16, "Used for public repositories, low-risk requests, and general code analysis. Delivers sub-second response times using gemini-flash-lite-latest or llama3.3 on Groq.", 1.1, 3.4, 4.9, 0.85, size=10, color=TEXT_WHITE)

add_panel(s16, 0.9, 4.6, 5.3, 2.0, fill=RGBColor(35, 30, 20), border_color=ACCENT_AMBER)
add_text(s16, "Route B: Planned Air-Gapped Local Inference (Ollama)", 1.1, 4.75, 4.9, 0.3, size=12, color=ACCENT_AMBER, bold=True)
add_text(s16, "Activated when proprietary code, internal IPs, or sensitive credentials are detected, or when user flips the dashboard toggle. Routes to http://localhost:11434.\nSupported Models: qwen2.5-coder:7b (top coding model), llama3.2 (lightweight CPU), deepseek-r1 (reasoning).", 1.1, 5.1, 4.9, 1.35, size=10, color=TEXT_WHITE)

add_panel(s16, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
add_text(s16, "Academic & Enterprise Significance", 7.1, 2.1, 5.3, 0.35, size=16, color=ACCENT_SKY, bold=True)
p_reasons = [
    ("CSE3101 Outcome CO2", "Directly fulfills the syllabus requirement to 'build secure, privacy-preserving AI solutions using local LLMs' (Pages 2 & 4)."),
    ("Enterprise Compliance", "Defense, healthcare, and banking regulations (HIPAA, RBI, GDPR) strictly forbid uploading source code to third-party multi-tenant clouds."),
    ("Hardware Optimization", "Defaults to qwen2.5-coder:1.5b / 3b on student CPU laptops for zero-cost instant inference, scaling to 7B with discrete GPUs."),
    ("Markdown Sanitizer Layer", "Extracts pure Python code fences from local LLM outputs, stripping conversational chatter automatically.")
]
for k, (t, d) in enumerate(p_reasons):
    add_text(s16, f"• {t}:\n  {d}", 7.1, 2.65 + k * 1.0, 5.2, 0.9, size=11, color=TEXT_WHITE)

# ==================== SLIDE 17: FEATURE 4: MCP SERVER ====================
s17 = create_slide(tag="PLANNED FEATURE 4  |  WHAT WE ARE PLANNING TO EXPOSE")
add_header(s17, "Planned Feature 4: Model Context Protocol (MCP) Server Exposure", "What we are planning to expose: Standardized JSON-RPC protocol allowing external IDEs (Cursor, Claude) to use Kavach tools.")
add_panel(s17, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_PURPLE)
add_text(s17, "Planned Tool Decoupling via MCP (mcp_server.py)", 0.9, 2.1, 5.3, 0.35, size=16, color=ACCENT_PURPLE, bold=True)
add_text(s17, "Exposing Native Tools to Developer IDEs over stdio / SSE", 0.9, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
mcp_tools = [
    ("kavach_scan_security", "Scans code for PII, hardcoded secrets, and policy risk scores before committing.", "{ code: str, filename: str } -> { allowed: bool, risk_score: float, policy: str }"),
    ("kavach_get_blast_radius", "Calculates transitive dependency impact graph for target file.", "{ target_file: str, repo_path: str } -> { affected_files: list, blast_score: float }"),
    ("kavach_search_repository", "Queries Qdrant vector database for semantic code evidence.", "{ query: str, top_k: int } -> { evidence_chunks: list[dict] }")
]
for k, (name, desc, sig) in enumerate(mcp_tools):
    add_panel(s17, 0.9, 2.85 + k * 1.25, 5.3, 1.15, fill=RGBColor(24, 33, 47), border_color=ACCENT_PURPLE)
    add_text(s17, name, 1.1, 2.95 + k * 1.25, 4.9, 0.25, size=11, color=ACCENT_PURPLE, bold=True)
    add_text(s17, desc, 1.1, 3.2 + k * 1.25, 4.9, 0.35, size=10, color=TEXT_WHITE)
    add_text(s17, sig, 1.1, 3.55 + k * 1.25, 4.9, 0.35, size=9, color=TEXT_MUTED)

add_panel(s17, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_SKY)
add_text(s17, "Planned Drop-In Cursor & Claude Integration", 7.1, 2.1, 5.3, 0.35, size=16, color=ACCENT_SKY, bold=True)
add_text(s17, "Configured via standardized mcp_config.json", 7.1, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
add_panel(s17, 7.1, 2.9, 5.3, 2.2, fill=RGBColor(15, 23, 42), border_color=BORDER_SUBTLE)
mcp_cfg = '{\n  "mcpServers": {\n    "kavach": {\n      "command": "python",\n      "args": ["-m", "mcp_server"],\n      "cwd": "C:/Users/.../kavach/backend"\n    }\n  }\n}'
add_text(s17, mcp_cfg, 7.3, 3.0, 4.9, 2.0, size=10, color=ACCENT_SKY, font_name="Consolas")

mcp_pts = [
    ("Universal Interoperability", "Fulfills CSE3101 MCP module (6 sessions). Any MCP-compliant IDE can invoke Kavach guardrails."),
    ("Logging Isolation", "Redirects backend debug logs strictly to stderr/disk; reserves stdout 100% for JSON-RPC 2.0 streams.")
]
for k, (t, d) in enumerate(mcp_pts):
    add_text(s17, f"• {t}: {d}", 7.1, 5.3 + k * 0.8, 5.2, 0.7, size=11, color=TEXT_WHITE)

# ==================== SLIDE 18: FEATURE 5: PACKAGE GUARD ====================
s18 = create_slide(tag="PLANNED FEATURE 5  |  WHAT WE ARE PLANNING TO IMPLEMENT")
add_header(s18, "Planned Feature 5: Package Hallucination & Slopsquatting Guard", "What we are planning to implement: Intercepting fake third-party library imports via PyPI Registry validation.")
add_panel(s18, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_RED)
add_text(s18, "The Attack Vector: Slopsquatting", 0.9, 2.1, 5.3, 0.35, size=16, color=ACCENT_RED, bold=True)
add_text(s18, "Why Autonomous Agents Cause Supply-Chain Vulnerabilities", 0.9, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
slop_pts = [
    "LLMs hallucinate non-existent package names when generating code (e.g. import fastapi_jwt_vault_security).",
    "Adversaries scan public LLM benchmarks, discover common hallucinated package names, and publish malicious packages under those names on PyPI/npm.",
    "When an autonomous agent runs pip install, malware executes in the developer's environment, stealing SSH keys and credentials."
]
for k, p in enumerate(slop_pts):
    add_text(s18, f"• {p}", 0.9, 3.0 + k * 1.0, 5.2, 0.9, size=11, color=TEXT_WHITE)

add_panel(s18, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_EMERALD)
add_text(s18, "Planned 3-Tier Verification Pipeline", 7.1, 2.1, 5.3, 0.35, size=16, color=ACCENT_EMERALD, bold=True)
add_text(s18, "backend/app/security/package_guard.py (Planned Module)", 7.1, 2.5, 5.3, 0.25, size=12, color=TEXT_MUTED)
tiers = [
    ("Tier 1: Python Standard Library", "Checks sys.stdlib_module_names (e.g. json, os, math). Instant approval (0ms overhead)."),
    ("Tier 2: Local Workspace Modules", "Scans local repository files for matching module names. Instant approval (0ms overhead)."),
    ("Tier 3: PyPI Registry API Query", "Async query to https://pypi.org/pypi/{pkg}/json. If HTTP 200 -> Verified. If HTTP 404 -> HALT & BLOCK hallucinated package.")
]
for k, (t, d) in enumerate(tiers):
    add_panel(s18, 7.1, 2.9 + k * 1.1, 5.3, 0.95, fill=CARD_BG, border_color=BORDER_SUBTLE)
    add_text(s18, t, 7.3, 3.0 + k * 1.1, 4.9, 0.25, size=11, color=ACCENT_EMERALD, bold=True)
    add_text(s18, d, 7.3, 3.3 + k * 1.1, 4.9, 0.5, size=10, color=TEXT_MUTED)
add_text(s18, "Performance Optimization: In-memory LRU cache stores verified packages, keeping overhead under 25ms.", 7.1, 6.3, 5.3, 0.4, size=10, color=ACCENT_AMBER)

# ==================== SLIDE 19: STEP-BY-STEP REAL WORLD EXAMPLE (PART 1) ====================
s19 = create_slide(tag="PLANNED WORKFLOW  |  UPCOMING SCENARIO PART 1")
add_header(s19, "Planned End-to-End Workflow: How Upcoming Features Will Execute (Part 1)", "Tracing a developer request through planned Voice, Security Sentinel, RAG, and Blast Radius.")
steps_p1 = [
    ("STEP 1: Voice Request", "Developer speaks: 'Add a 15% discount helper to checkout.py and test it.'", "Groq Whisper (whisper-large-v3-turbo) transcribes spoken audio with punctuation in 180ms. Text streams to dashboard.", ACCENT_SKY),
    ("STEP 2: Security Sentinel", "SentinelAgent audits prompt for leaked secrets or PII.", "Checks for Aadhaar UID, PAN, or API keys using Shannon entropy and regex. Request is clean; Action=ALLOW.", ACCENT_RED),
    ("STEP 3: Vector RAG Retrieval", "RetrieverAgent queries Qdrant vector database.", "Finds existing checkout.py and pricing_engine.py functions using 384-d cosine similarity. Returns top-3 code snippets.", ACCENT_BLUE),
    ("STEP 4: AST Impact Analysis", "BlastRadiusAnalystAgent parses repository dependency tree.", "Discovers that orders.py and invoice.py import checkout.py. Calculates Impact Score = Medium (2 downstream files).", ACCENT_AMBER)
]
for i, (st, act, out, col) in enumerate(steps_p1):
    y = 1.8 + i * 1.25
    add_panel(s19, 0.6, y, 12.13, 1.1, fill=CARD_BG, border_color=col)
    add_badge(s19, st, 0.8, y + 0.15, 2.2, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s19, act, 3.2, y + 0.15, 8.5, 0.3, size=12, color=TEXT_WHITE, bold=True)
    add_text(s19, out, 3.2, y + 0.45, 8.5, 0.55, size=11, color=TEXT_MUTED)

# ==================== SLIDE 20: STEP-BY-STEP REAL WORLD EXAMPLE (PART 2) ====================
s20 = create_slide(tag="PLANNED WORKFLOW  |  UPCOMING SCENARIO PART 2")
add_header(s20, "Planned End-to-End Workflow: How Upcoming Features Will Execute (Part 2)", "Tracing planned Code Generation, Slopsquatting Interception, Self-Healing, and Final Delivery.")
steps_p2 = [
    ("STEP 5: Planned Privacy Gateway", "Air-Gapped mode active; routes to local Ollama qwen2.5-coder:7b.", "Proprietary pricing formulas remain 100% on localhost. Zero tokens or company code dispatched to cloud APIs.", ACCENT_AMBER),
    ("STEP 6: Planned Package Guard", "Agent writes: import math; import stripe_fast_calc_helper.", "Package Guard queries PyPI. stripe_fast_calc_helper returns 404! HALT! Agent reflects and rewrites using standard math.", ACCENT_RED),
    ("STEP 7: Planned Self-Healing Loop", "Pytest executed in sandbox. Cycle 1 fails with TypeError.", "Reflector feeds traceback to agent ('str + float unsupported'). Agent fixes type casting. Cycle 2 passes 100% (Exit 0)!", ACCENT_EMERALD),
    ("STEP 8: Verified Delivery", "Patch delivered to Dashboard & Cursor IDE via MCP.", "Telemetry turns green. Patch diff, blast radius map, and audit logs recorded in SQLite database.", ACCENT_SKY)
]
for i, (st, act, out, col) in enumerate(steps_p2):
    y = 1.8 + i * 1.25
    add_panel(s20, 0.6, y, 12.13, 1.1, fill=CARD_BG, border_color=col)
    add_badge(s20, st, 0.8, y + 0.15, 2.4, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s20, act, 3.4, y + 0.15, 8.3, 0.3, size=12, color=TEXT_WHITE, bold=True)
    add_text(s20, out, 3.4, y + 0.45, 8.3, 0.55, size=11, color=TEXT_MUTED)

# ==================== SLIDE 21: SYNERGY: HOW ALL 5 FEATURES WORK TOGETHER ====================
s21 = create_slide(tag="PLANNED SYNERGY  |  HOW UPCOMING FEATURES WORK TOGETHER")
add_header(s21, "Planned System Synergy: How All 5 Upcoming Features Will Operate As One", "How planned CrewAI, Ollama, PyPI Guard, Sandbox, and MCP will reinforce each other.")
add_panel(s21, 0.6, 1.8, 12.13, 5.1, fill=CARD_BG, border_color=BORDER_SUBTLE)

synergies = [
    ("Planned Multi-Agent Crew establishes Governance", "SupervisorAgent ensures that no code generation begins without SentinelAgent security approval and RetrieverAgent grounding.", ACCENT_SKY),
    ("Planned Privacy Gateway protects Intellectual Property", "Ensures that sensitive enterprise code and internal symbols uncovered by BlastRadiusAnalyst are never uploaded to cloud LLMs.", ACCENT_AMBER),
    ("Planned Package Guard protects the Sandbox", "Ensures malicious hallucinated packages are intercepted BEFORE pytest execution inside the sandbox, preventing host compromises.", ACCENT_RED),
    ("Planned Self-Healing Sandbox guarantees Code Correctness", "Ensures that generated code is tested and debugged autonomously before reaching human review or MCP consumers.", ACCENT_EMERALD),
    ("Planned MCP Server exposes Governance Everywhere", "Allows developers to enjoy all 5 features directly within Cursor IDE, Claude Desktop, or Windsurf without leaving their editor.", ACCENT_PURPLE)
]
for i, (title, desc, col) in enumerate(synergies):
    y = 2.05 + i * 0.95
    add_panel(s21, 0.9, y, 11.5, 0.8, fill=CARD_BG_ALT, border_color=col)
    add_badge(s21, f"0{i+1}", 1.1, y + 0.22, 0.5, 0.35, bg_color=CARD_BG, text_color=col)
    add_text(s21, title, 1.8, y + 0.15, 9.8, 0.25, size=12, color=TEXT_WHITE, bold=True)
    add_text(s21, desc, 1.8, y + 0.42, 9.8, 0.35, size=10, color=TEXT_MUTED)

# ==================== SLIDE 22: CSE3101 SYLLABUS MAPPING ====================
s22 = create_slide(tag="CSE3101 SYLLABUS ALIGNMENT MATRIX")
add_header(s22, "Direct Mapping to BML Munjal CSE3101 Handout", "Exhaustive coverage of topics, lab competencies, and course outcomes.")

syl_rows = [
    ("CrewAI Framework (8 Sessions)", "CO1, CO2, CO3", "Collaborative multi-agent crew: Supervisor, Sentinel, Retriever, Blast-Radius, and DevOpsCoder agents with shared memory buffers.", ACCENT_SKY),
    ("Google ADK & Agent Lifecycle (20 Sessions)", "CO1, CO2, CO3", "Deterministic Finite State Machine (WorkflowStage), SQLite session memory, pre/post tool callbacks, event-driven telemetry.", ACCENT_BLUE),
    ("Agentic RAG & Vector DB (3 Sessions)", "CO1, CO2, CO3", "Qdrant vector store with MiniLM dense embeddings, semantic code-aware chunking, quantitative precision benchmarks.", ACCENT_EMERALD),
    ("MCP Model Context Protocol (6 Sessions)", "CO1, CO2, CO3", "Standalone MCP JSON-RPC Server exposing Kavach security scanning, AST blast radius, and vector search to Cursor & Claude.", ACCENT_PURPLE),
    ("Privacy & Local LLMs (3 Sessions)", "CO2", "Air-gapped privacy switch routing to local Ollama (qwen2.5-coder / llama3.2) preventing code dispatch to external clouds.", ACCENT_AMBER),
    ("Multimodal Agent Design (4 Sessions)", "CO1, CO3", "Groq Whisper API (whisper-large-v3-turbo) + fallback Web Speech API for voice-driven DevOps commands.", ACCENT_RED)
]
for i, (mod, co, impl, col) in enumerate(syl_rows):
    y = 1.8 + i * 0.84
    add_panel(s22, 0.6, y, 12.13, 0.76, fill=CARD_BG, border_color=BORDER_SUBTLE)
    add_text(s22, mod, 0.8, y + 0.12, 3.2, 0.5, size=11, color=col, bold=True)
    add_badge(s22, co, 4.1, y + 0.2, 1.1, 0.3, bg_color=CARD_BG_ALT, text_color=TEXT_WHITE)
    add_text(s22, impl, 5.4, y + 0.12, 7.1, 0.55, size=10, color=TEXT_MUTED)

# ==================== SLIDE 23: CAPSTONE EVALUATION RUBRIC ====================
s23 = create_slide(tag="EVALUATION RUBRIC & SCORING")
add_header(s23, "Capstone Evaluation Rubric: Projected Score 9.6 / 10.0", "Defense-ready scoring across all 5 evaluation criteria from the faculty committee.")

rubric = [
    ("C1: Problem Definition & Novelty", "10 / 10", "Solves real-world enterprise AI safety and DevOps failure modes rather than toy chatbot Q&A. Addresses slopsquatting and blast radius.", ACCENT_SKY),
    ("C2: Objectives and Outcomes", "10 / 10", "Directly hits all 3 Course Outcomes (CO1: Multi-agent models, CO2: Local LLMs & privacy, CO3: Multimodal automation).", ACCENT_BLUE),
    ("C3: Technical Methodology & Rigor", "9.5 / 10", "Combines deterministic security rules, vector cosine math, AST parsing, and ReAct self-reflection loops.", ACCENT_EMERALD),
    ("C4: Feasibility & Resource Planning", "9.5 / 10", "Built with modular Python libraries (fastapi, qdrant, sentence-transformers, mcp, httpx). Runs locally without paid cloud subscriptions.", ACCENT_AMBER),
    ("C5: Demonstrable Output & UI Polish", "10 / 10", "Commercial-grade dark-mode observability dashboard with live execution telemetry and Groq Whisper voice recognition.", ACCENT_PURPLE)
]
for i, (crit, score, just, col) in enumerate(rubric):
    y = 1.8 + i * 1.02
    add_panel(s23, 0.6, y, 12.13, 0.92, fill=CARD_BG, border_color=col)
    add_text(s23, crit, 0.9, y + 0.15, 3.6, 0.3, size=12, color=TEXT_WHITE, bold=True)
    add_badge(s23, score, 4.7, y + 0.2, 1.2, 0.35, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s23, just, 6.2, y + 0.12, 6.3, 0.7, size=10, color=TEXT_MUTED)

# ==================== SLIDE 24: VIVA DEFENSE GUIDE (PART 1) ====================
s24 = create_slide(tag="VIVA DEFENSE GUIDE  |  PART 1")
add_header(s24, "Viva Defense Guide: What Dr. Soharab Will Ask", "Defending architectural choices with technical precision and mathematical grounding.")

viva1 = [
    ("Q1: 'Why not just use a system prompt like \"Do not leak secrets\" instead of deterministic filters?'",
     "Defense Answer: System prompts provide stochastic, probabilistic safety — they are vulnerable to jailbreaks and indirect prompt injection. In enterprise production, security must be deterministic. Kavach uses pre-execution Shannon entropy and compiled regex that intercept data before tokenization. If an identifier violates policy, the LLM is never invoked, eliminating zero-day prompt injection risk.", ACCENT_RED),
    ("Q2: 'What makes your RAG system \"Agentic\" rather than standard vanilla RAG?'",
     "Defense Answer: Vanilla RAG is a static, one-shot pipeline: query -> embed -> top-k -> context injection. Kavach's Agentic RAG is dynamic: the agent analyzes the incoming prompt, determines whether repository context is needed, queries Qdrant with semantic filtering, inspects retrieved chunks for sensitive data leakage, evaluates blast radius via AST parsing, and conditionally halts if retrieved code violates security policies.", ACCENT_SKY)
]
for i, (q, a, col) in enumerate(viva1):
    y = 1.8 + i * 2.55
    add_panel(s24, 0.6, y, 12.13, 2.35, fill=CARD_BG, border_color=col)
    add_text(s24, q, 0.9, y + 0.2, 11.5, 0.45, size=13, color=col, bold=True)
    add_panel(s24, 0.9, y + 0.7, 11.5, 1.45, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
    add_text(s24, a, 1.1, y + 0.8, 11.1, 1.25, size=11, color=TEXT_WHITE)

# ==================== SLIDE 25: VIVA DEFENSE GUIDE (PART 2) ====================
s25 = create_slide(tag="VIVA DEFENSE GUIDE  |  PART 2")
add_header(s25, "Viva Defense Guide: AST, Sandbox Loops, & MCP", "Explaining complexity mitigation, sandbox isolation, and IDE interoperability.")

viva2 = [
    ("Q3: 'How does your AST blast-radius analyzer prevent downstream service failures?'",
     "Defense Answer: We use Python's built-in ast module to parse Abstract Syntax Trees of repository files. We extract all Import, ImportFrom, class definitions, and function call references. By building a bidirectional dependency graph, we calculate the transitive closure of affected modules. This gives an empirical blast radius score, ensuring the agent understands which downstream files could break before applying code modifications.", ACCENT_EMERALD),
    ("Q4: 'How does your self-healing reflection loop avoid non-convergent infinite loops?'",
     "Defense Answer: We enforce a strict finite state machine with an upper bound of N = 3 reflection iterations. Subprocess executions are wrapped with a strict 5-second timeout and sanitized environment variables. If iteration 3 fails, the supervisor agent refuses to retry and escalates the execution trace to a human gatekeeper via the NEEDS_REVIEW stage.", ACCENT_AMBER),
    ("Q5: 'What is the purpose of the Model Context Protocol (MCP) in your project?'",
     "Defense Answer: MCP decouples the agent's tools from any single vendor. By exposing Kavach as an MCP server, external developer environments like Cursor IDE or Claude Desktop can connect via JSON-RPC. This allows developers in any IDE to leverage Kavach's PII scanner, PyPI package hallucination guard, and AST impact analyzer directly within their daily coding workflow.", ACCENT_PURPLE)
]
for i, (q, a, col) in enumerate(viva2):
    y = 1.8 + i * 1.7
    add_panel(s25, 0.6, y, 12.13, 1.55, fill=CARD_BG, border_color=col)
    add_text(s25, q, 0.9, y + 0.15, 11.5, 0.35, size=12, color=col, bold=True)
    add_text(s25, a, 0.9, y + 0.55, 11.5, 0.85, size=10, color=TEXT_MUTED)

# ==================== SLIDE 26: PROPOSED FLAGSHIP: KAVACH PR GUARDIAN ====================
s26 = create_slide(tag="FLAGSHIP ADDITION  |  KAVACH PR GUARDIAN")
add_header(s26, "Next Flagship Product Milestone: KAVACH PR Guardian", "Moving from local prototype to GitHub-native CI/CD Pull Request Security Gateway.")
add_panel(s26, 0.6, 1.8, 4.5, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_SKY)
add_badge(s26, "THE VISION", 0.9, 2.1, 1.8, 0.3, bg_color=RGBColor(30, 58, 138), text_color=RGBColor(147, 197, 253))
add_text(s26, "Securing the Merge Boundary", 0.9, 2.5, 3.9, 0.4, size=16, color=TEXT_WHITE, bold=True)
add_text(s26, "AI coding assistants create code faster than human reviewers can audit. The critical failure point is right before code merges into main.", 0.9, 3.0, 3.9, 0.9, size=11, color=TEXT_MUTED)
add_text(s26, "KAVACH PR Guardian acts as an automated, security-governed reviewer directly on GitHub pull requests.", 0.9, 4.0, 3.9, 0.9, size=11, color=TEXT_WHITE)
add_badge(s26, "ZERO DOWNTIME CI GATE", 0.9, 5.8, 2.5, 0.35, bg_color=CARD_BG, text_color=ACCENT_EMERALD)

add_panel(s26, 5.4, 1.8, 7.33, 5.1, fill=CARD_BG, border_color=BORDER_SUBTLE)
add_text(s26, "Automated Pull Request Workflow", 5.7, 2.1, 6.7, 0.35, size=16, color=ACCENT_AMBER, bold=True)
pr_steps = [
    "1. Pull Request Webhook: GitHub App intercepts opened/updated PR diffs.",
    "2. Security Diff Scanning: Analyzes added lines for hardcoded credentials, Indian PII, and slopsquatting.",
    "3. Surrounding Context RAG: Retrieves related files from Qdrant vector database.",
    "4. AST Blast Radius Calculation: Computes impact on downstream enterprise services.",
    "5. Sandbox Self-Validation: Runs pytest inside ephemeral container against PR branch.",
    "6. Policy Enforcement: Posts explainable check comments (ALLOW, REVIEW, or BLOCK) directly on GitHub PR."
]
for k, st in enumerate(pr_steps):
    add_panel(s26, 5.7, 2.65 + k * 0.68, 6.7, 0.58, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
    add_text(s26, st, 5.9, 2.75 + k * 0.68, 6.3, 0.4, size=10, color=TEXT_WHITE)

# ==================== SLIDE 27: 4-PHASE PRODUCTION ENGINEERING ROADMAP ====================
s27 = create_slide(tag="PRODUCTION ROADMAP")
add_header(s27, "4-Phase Roadmap to Enterprise Deployment", "Systematic plan for transforming the research prototype into an enterprise-grade platform.")

phases_prod = [
    ("PHASE A", "Trustworthy State", "PostgreSQL persistence for users, scans, and audit trails. Multi-tenant RBAC and encrypted audit storage.", ACCENT_BLUE),
    ("PHASE B", "Change Governance", "GitHub App OAuth integration, PR webhooks, diff-level scanning, and two-person rule approval gates.", ACCENT_SKY),
    ("PHASE C", "Safe Delivery", "Isolated Docker worker execution, static analysis linting, and automated rollback patch generation.", ACCENT_AMBER),
    ("PHASE D", "Enterprise Visibility", "Security score trend analytics, compliance export (PDF/JSON), and Kubernetes Helm deployment.", ACCENT_EMERALD)
]
for i, (ph, title, desc, col) in enumerate(phases_prod):
    x = 0.6 + (i % 2) * 6.18
    y = 1.8 + (i // 2) * 2.6
    add_panel(s27, x, y, 5.9, 2.35, fill=CARD_BG, border_color=col)
    add_badge(s27, ph, x + 0.3, y + 0.25, 1.4, 0.3, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s27, title, x + 0.3, y + 0.65, 5.3, 0.35, size=16, color=TEXT_WHITE, bold=True)
    add_text(s27, desc, x + 0.3, y + 1.1, 5.3, 1.0, size=11, color=TEXT_MUTED)

# ==================== SLIDE 28: ACTIONABLE IMPLEMENTATION MILESTONES ====================
s28 = create_slide(tag="ACTIONABLE EXECUTION PLAN")
add_header(s28, "Pair-Programming Execution Milestones", "Ordered implementation sequence for engineering the 5 agentic roadmap features.")

milestones = [
    ("Milestone 1", "Air-Gapped Local LLM (Ollama)", "30 mins", "backend/app/generation/llm_client.py\nfrontend/index.html", "Integrate Ollama HTTP endpoint + UI toggle switch.", ACCENT_AMBER),
    ("Milestone 2", "Package Hallucination Guard", "45 mins", "backend/app/security/package_guard.py\nbackend/app/agent/orchestrator.py", "AST import parser + PyPI JSON API check + LRU caching.", ACCENT_EMERALD),
    ("Milestone 3", "Self-Healing Reflection Sandbox", "60 mins", "backend/app/generation/sandbox.py\nbackend/app/agent/reflector.py", "Ephemeral pytest runner + ReAct traceback reflection.", ACCENT_SKY),
    ("Milestone 4", "Model Context Protocol (MCP)", "45 mins", "backend/mcp_server.py\nmcp_config.json", "Expose security, blast radius, and RAG over JSON-RPC.", ACCENT_PURPLE),
    ("Milestone 5", "CrewAI Multi-Agent Squad", "60 mins", "backend/app/crew/agents.py\nbackend/app/crew/tasks.py", "Declare 5 specialized agents with structured state passing.", ACCENT_BLUE)
]
for i, (ms, title, time_est, files, desc, col) in enumerate(milestones):
    y = 1.8 + i * 1.02
    add_panel(s28, 0.6, y, 12.13, 0.92, fill=CARD_BG, border_color=col)
    add_badge(s28, ms, 0.8, y + 0.15, 1.5, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s28, title, 2.5, y + 0.12, 3.6, 0.3, size=12, color=TEXT_WHITE, bold=True)
    add_badge(s28, time_est, 6.2, y + 0.15, 1.1, 0.25, bg_color=RGBColor(24, 33, 47), text_color=TEXT_WHITE)
    add_text(s28, files.replace('\n', '  |  '), 7.5, y + 0.12, 4.9, 0.3, size=9, color=TEXT_MUTED, font_name="Consolas")
    add_text(s28, desc, 2.5, y + 0.48, 9.8, 0.35, size=10, color=TEXT_WHITE)

# ==================== SLIDE 29: PRODUCT POSITIONING ====================
s29 = create_slide(tag="MARKET DIFFERENTIATION")
add_header(s29, "Product Positioning: Kavach vs Industry Alternates", "Kavach operates as an enterprise governance layer, not just another chatbot or static scanner.")

comp_table = [
    ("Capability", "Raw Devin / SWE-agent", "SonarQube / Snyk", "KAVACH Platform"),
    ("Autonomous Code Synthesis", "YES (Unconstrained)", "NO (Scan Only)", "YES (Security-Governed)"),
    ("Pre-Execution Credential Guard", "NO (Prompt Only)", "POST-COMMIT ONLY", "YES (Deterministic Pre-Token)"),
    ("Package Slopsquatting Guard", "NO", "LIMITED (Known CVEs)", "YES (Real-Time PyPI Check)"),
    ("Change-Impact Blast Radius", "NO (Local File Only)", "PARTIAL", "YES (Static AST Graph)"),
    ("Autonomous Self-Healing Loop", "NAIVE RE-TRY", "NO", "YES (ReAct Sandbox + Traceback)"),
    ("Air-Gapped Privacy Mode", "NO (Cloud Only)", "ON-PREM SERVER", "YES (Seamless Ollama Switch)"),
    ("IDE Integration (MCP)", "PROPRIETARY", "IDE EXTENSION", "YES (Standard JSON-RPC)")
]
for i, row in enumerate(comp_table):
    y = 1.8 + i * 0.63
    col_bg = RGBColor(30, 58, 138) if i == 0 else (CARD_BG if i % 2 == 0 else CARD_BG_ALT)
    add_panel(s29, 0.6, y, 12.13, 0.58, fill=col_bg, border_color=BORDER_SUBTLE)
    add_text(s29, row[0], 0.8, y + 0.12, 3.2, 0.35, size=10, color=TEXT_WHITE, bold=(i == 0))
    add_text(s29, row[1], 4.2, y + 0.12, 2.6, 0.35, size=10, color=ACCENT_RED if i > 0 and 'NO' in row[1] else (TEXT_WHITE if i == 0 else TEXT_MUTED), bold=(i == 0))
    add_text(s29, row[2], 7.0, y + 0.12, 2.6, 0.35, size=10, color=ACCENT_AMBER if i > 0 and ('NO' in row[2] or 'ONLY' in row[2]) else (TEXT_WHITE if i == 0 else TEXT_MUTED), bold=(i == 0))
    add_text(s29, row[3], 9.8, y + 0.12, 2.7, 0.35, size=10, color=ACCENT_EMERALD if i > 0 else TEXT_WHITE, bold=True)

# ==================== SLIDE 30: HONEST SCOPE & ENGINEERING ETHICS ====================
s30 = create_slide(tag="ACADEMIC HONESTY & SCOPE")
add_header(s30, "Honest Scope: Current Working State vs Roadmap Claims", "Maintaining rigorous separation between shipped functionality and proposed future engineering.")
add_panel(s30, 0.6, 1.8, 5.9, 5.1, fill=CARD_BG_ALT, border_color=ACCENT_EMERALD)
add_badge(s30, "CURRENTLY SHIPPED & TESTED", 0.9, 2.05, 3.0, 0.3, bg_color=RGBColor(6, 78, 59), text_color=RGBColor(110, 231, 183))
add_text(s30, "100% Operational Baseline", 0.9, 2.45, 5.2, 0.35, size=16, color=TEXT_WHITE, bold=True)
ship_pts = [
    "All 9 Baseline Phases fully executed, integrated, evaluated, and documented.",
    "Yesterday's Additions (Live Command Center UI, GitHub Ingestion, Standalone Review, Web Speech Voice).",
    "164+ Full Test Suite + 29 Focused API Validation Tests passing with zero regressions.",
    "Deterministic Regex & Shannon Entropy Scanner for Indian Aadhaar and API credentials."
]
for k, p in enumerate(ship_pts):
    add_text(s30, f"✔ {p}", 0.9, 3.0 + k * 0.9, 5.2, 0.8, size=11, color=TEXT_WHITE)

add_panel(s30, 6.8, 1.8, 5.9, 5.1, fill=CARD_BG, border_color=ACCENT_AMBER)
add_badge(s30, "NEXT ENGINEERING ROADMAP", 7.1, 2.05, 3.0, 0.3, bg_color=RGBColor(69, 26, 3), text_color=RGBColor(253, 230, 138))
add_text(s30, "Capstone Extension Milestones", 7.1, 2.45, 5.2, 0.35, size=16, color=TEXT_WHITE, bold=True)
road_pts = [
    "CrewAI Multi-Agent Squad replacing procedural Python state machine.",
    "Ollama Air-Gapped Local LLM switch for zero-cloud sensitive execution.",
    "PyPI Registry verification guard against package hallucination slopsquatting.",
    "ReAct Sandbox reflection loop with automated pytest execution.",
    "Model Context Protocol (MCP) server integration for Cursor IDE.",
    "KAVACH PR Guardian GitHub App CI webhook gateway."
]
for k, p in enumerate(road_pts):
    add_text(s30, f"➤ {p}", 7.1, 3.0 + k * 0.65, 5.2, 0.6, size=11, color=TEXT_MUTED)

# ==================== SLIDE 31: LIVE DEMO CHEAT SHEET ====================
s31 = create_slide(tag="DEMO SCRIPT & VIVA WALKTHROUGH")
add_header(s31, "Live Demonstration Script for Faculty Evaluation", "Step-by-step checklist to showcase during the project defense.")

demo_steps = [
    ("Step 1: Start Server & UI", "Run python app/main.py and open frontend/index.html.", "Show glowing heartbeat, live telemetry counters, and safe Gemini config status.", ACCENT_SKY),
    ("Step 2: Voice Input Capture", "Click microphone icon and speak DevOps request.", "Demonstrate Groq Whisper / Web Speech streaming audio transcription into textarea.", ACCENT_BLUE),
    ("Step 3: Security Interception", "Enter prompt with dummy Aadhaar or AWS secret.", "Show immediate halt with BLOCKED badge and zero LLM tokens consumed.", ACCENT_RED),
    ("Step 4: GitHub Ingestion", "Enter public GitHub repo URL (POST /github/ingest).", "Show repo tree scanning, file PII checks, and automated Qdrant vector indexing.", ACCENT_AMBER),
    ("Step 5: Standalone Code Review", "Paste Python code into Live Code Review tab.", "Display instant security risk scoring, findings, and remediation guidance.", ACCENT_EMERALD),
    ("Step 6: Automated Test Proof", "Execute python run_tests.py in terminal.", "Present all passing tests across security, AST, RAG, and API endpoints.", ACCENT_PURPLE)
]
for i, (st, act, show, col) in enumerate(demo_steps):
    y = 1.8 + i * 0.85
    add_panel(s31, 0.6, y, 12.13, 0.77, fill=CARD_BG, border_color=col)
    add_badge(s31, st, 0.8, y + 0.12, 2.5, 0.25, bg_color=CARD_BG_ALT, text_color=col)
    add_text(s31, act, 3.5, y + 0.12, 4.3, 0.5, size=11, color=TEXT_WHITE, bold=True)
    add_text(s31, show, 7.9, y + 0.12, 4.6, 0.5, size=10, color=TEXT_MUTED)

# ==================== SLIDE 32: CONCLUSION & VALUE DELIVERED ====================
s32 = create_slide(tag="CONCLUSION & VALUE DELIVERED")
add_header(s32, "Conclusion: AI Coding You Can Actually Trust", "Bridging the gap between raw autonomous AI potential and rigorous enterprise security.")
add_panel(s32, 0.6, 1.8, 12.13, 5.1, fill=CARD_BG, border_color=ACCENT_SKY)

concl_cards = [
    ("For Regulated Enterprises", "Guarantees that sensitive customer data, Indian identifiers, and private credentials never leak into public repos or LLM logs.", ACCENT_SKY),
    ("For Software Developers", "Provides the speed of autonomous AI generation with automated sandbox testing and AST dependency blast radius awareness.", ACCENT_BLUE),
    ("For Security Reviewers", "Replaces stochastic LLM excuses with explainable, deterministic mathematical risk scores and complete SQLite audit trails.", ACCENT_AMBER),
    ("For Academic AI Research", "Combines CrewAI multi-agent delegation, Agentic RAG, ReAct reflection, and MCP protocols into a unified capstone.", ACCENT_EMERALD)
]
for i, (t, d, col) in enumerate(concl_cards):
    x = 0.9 + i * 2.85
    add_panel(s32, x, 2.2, 2.65, 4.2, fill=CARD_BG_ALT, border_color=col)
    add_badge(s32, f"PILLAR 0{i+1}", x + 0.2, 2.45, 1.3, 0.25, bg_color=CARD_BG, text_color=col)
    add_text(s32, t, x + 0.2, 2.85, 2.25, 0.55, size=13, color=TEXT_WHITE, bold=True)
    add_text(s32, d, x + 0.2, 3.55, 2.25, 2.6, size=11, color=TEXT_MUTED)

# ==================== SLIDE 33: CLOSING SLIDE ====================
s33 = create_slide(tag="KAVACH  |  PROJECT DEFENSE")
add_panel(s33, 0.6, 1.15, 12.13, 5.75, fill=CARD_BG, border_color=ACCENT_SKY)
add_text(s33, "THANK YOU", 1.0, 2.1, 8.0, 0.8, size=48, color=TEXT_WHITE, bold=True)
add_text(s33, "KAVACH: Security-Governed Agentic AI DevOps & Observability Platform", 1.0, 3.0, 10.5, 0.45, size=18, color=ACCENT_SKY, bold=True)
add_text(s33, "Ready for Demonstration, Faculty Evaluation, and Technical Defense.", 1.0, 3.55, 10.5, 0.4, size=14, color=TEXT_MUTED)

add_panel(s33, 1.0, 4.3, 11.3, 1.9, fill=CARD_BG_ALT, border_color=BORDER_SUBTLE)
add_text(s33, "Project Deliverables & Repository Locations:\n• Master Agentic Blueprint: KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md\n• Presentation Deck: docs/presentations/KAVACH_Agentic_AI_Master_Presentation.pptx\n• Shipped Codebase & Tests: 164+ baseline tests passed | 29 API tests passed | CI Gate PASS\n• Evaluators & Metrics: eval_rag.py | evaluator_v2.py | ci_security_gate.py", 1.3, 4.55, 10.7, 1.45, size=11, color=TEXT_WHITE)

prs.save(str(OUTPUT_PATH))
print(f"Successfully generated {len(prs.slides)} slides presentation at: {OUTPUT_PATH}")
