"""
Generate professional 10-slide PowerPoint presentation (.pptx) for PRJ-IV Mid-Term Presentation.
Scheduled: 29/09/2026 at 12-2PM
Evaluator: Prof. Anusha Chhabra
Strictly maps to the 4 grading rubrics (Total 25 marks):
- Comprehensiveness of Literature Review (10 marks)
- Research Gap (5 marks)
- Objective / Problem Definition (5 marks)
- Proposed Methodology (Tools/Techniques/Methods/Data Set) (5 marks)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Theme Colors
BG_COLOR = RGBColor(10, 25, 47)         # Deep Navy Blue
PANEL_COLOR = RGBColor(17, 34, 64)      # Surface Card Navy
CYAN_ACCENT = RGBColor(0, 210, 255)     # Electric Cyan
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(204, 214, 246)
GREEN_ACCENT = RGBColor(100, 255, 218)
GOLD_ACCENT = RGBColor(255, 209, 102)

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_text=""):
    # Header Category / Rubric Badge
    if category_text:
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    # Main Slide Title
    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, title, body_bullets, title_color=CYAN_ACCENT):
    # Background shape
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = PANEL_COLOR
    shape.line.color.rgb = RGBColor(35, 53, 84)
    shape.line.width = Pt(1.5)

    # Content
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = title_color
    p.space_after = Pt(8)

    for bullet in body_bullets:
        p_b = tf.add_paragraph()
        p_b.text = "• " + bullet
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = LIGHT_GRAY
        p_b.space_after = Pt(4)

def generate_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "BML MUNJAL UNIVERSITY | SCHOOL OF ENGINEERING & TECHNOLOGY"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "KAVACH"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "A Security-Governed Multi-Agent AI DevOps & Observability Platform"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = GREEN_ACCENT
    p2.space_after = Pt(24)

    p3 = tf.add_paragraph()
    p3.text = "Project-IV (7th Semester Major Project) — Mid-Term Evaluation Presentation"
    p3.font.size = Pt(14)
    p3.font.color.rgb = LIGHT_GRAY
    p3.space_after = Pt(20)

    # Team Box
    add_card(slide1, Inches(1.0), Inches(4.8), Inches(11.333), Inches(1.8),
             "Team Members & Academic Details", [
                 "Dhruv Jain (230532) | Dev Garg (230487) | Ansh Rohilla (230794) | Ansh Adhikari (230822)",
                 "Department of Computer Science & Engineering | Academic Year 2026–27",
                 "Faculty Evaluator / Coordinator: Prof. Anusha Chhabra | Presentation Date: 29/09/2026"
             ], title_color=GOLD_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 2: PROBLEM DEFINITION & INDUSTRY MOTIVATION (5 MARKS)
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Critical Security Dilemma of Autonomous AI Coding Agents", "Methodology Rubric: Objective & Problem Definition (5 Marks)")

    add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Industry Context & Autonomous Agent Risks", [
                 "High Adoption: Organizations are rapidly deploying autonomous agents (Devin, SWE-agent, AutoPR) for end-to-end software development.",
                 "The Supply-Chain Vector: LLMs operate as probabilistic token predictors and regularly hallucinate non-existent package names.",
                 "Weaponized Slopsquatting: Attackers monitor LLM hallucinations and register malicious packages on PyPI/npm (AI Dependency Confusion).",
                 "Credential Exfiltration: Developers accidentally paste production API keys into prompt logs dispatched to external cloud APIs.",
                 "Unbounded Blast Radius: Agents modify code without architectural dependency awareness, breaking downstream services."
             ], title_color=CYAN_ACCENT)

    add_card(slide2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "The Core Research Problem", [
                 "Core Question: How can enterprises harvest autonomous agent velocity without risking credential leaks, slopsquatting, or regressions?",
                 "Limitation of Existing Defenses: Traditional SCA tools (Snyk, Dependabot) only scan static requirements.txt post-facto.",
                 "Fragility of Prompt Filters: System prompts ('Do not leak secrets') are stochastic and vulnerable to prompt injection jailbreaks.",
                 "The Kavach Mission: Construct a deterministic, pre-execution governance layer combining Shannon entropy, AST import firewalls, and ReAct sandboxing."
             ], title_color=GOLD_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 3: LITERATURE REVIEW — PART 1 (10 MARKS)
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Literature Review: Autonomous Agents & Supply-Chain Vulnerabilities", "Literature Review Rubric: Comprehensiveness (Part 1 / 2 — 10 Marks)")

    add_card(slide3, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "1. Autonomous Coding Agents", [
                 "SWE-agent (Yang et al., 2024): Demonstrated ReAct agent resolving real GitHub issues via terminal interface.",
                 "Identified Flaw: SWE-agent lacks pre-execution security gates, permitting arbitrary destructive shell commands.",
                 "Devin (Cognition, 2024): Highlighted non-convergent debugging oscillations and token exhaustion during unit testing."
             ])

    add_card(slide3, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "2. AI Package Hallucination", [
                 "Bar-Zik (2024) & Lazaar et al. (2024): Proved LLMs regularly invent package names for niche tasks.",
                 "Slopsquatting Threat: Attackers register these packages on PyPI to hijack developer machines upon 'pip install'.",
                 "Ladisa et al. (2023): Traditional SCA tools are blind to runtime agent-synthesized import statements."
             ])

    add_card(slide3, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "3. Prompt Injection & LLM Security", [
                 "OWASP Top 10 for LLMs (2025): Highlights Prompt Injection (LLM01) and Sensitive Data Exposure (LLM06).",
                 "Greshake et al. (2023): Indirect prompt injection in code comments hijacks the agent's internal goal state.",
                 "Defense Consensus: Security must be enforced outside the LLM context window using deterministic filters."
             ])

    # -------------------------------------------------------------
    # SLIDE 4: LITERATURE REVIEW — PART 2 (10 MARKS)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Literature Review: Code RAG, Static Analysis & Privacy", "Literature Review Rubric: Comprehensiveness (Part 2 / 2 — 10 Marks)")

    add_card(slide4, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "4. Code RAG & Embeddings", [
                 "Lewis et al. (2020): Grounded generation using dense vector embeddings.",
                 "Feng et al. (2020) & Guo et al. (2022): CodeBERT and sentence-transformers for code retrieval.",
                 "Existing Limitation: Naive character chunking shatters AST syntax boundaries and separably indexes signatures from bodies."
             ])

    add_card(slide4, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "5. AST & Change Impact", [
                 "Aho et al. (2006): Static Abstract Syntax Trees represent deterministic program structure without execution.",
                 "Ren et al. (2004) & Lehnert (2011): Transitive closure over AST dependency graphs is vital for blast radius prediction.",
                 "Agent Gap: No existing autonomous agent constructs AST impact graphs before applying multi-file code modifications."
             ])

    add_card(slide4, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "6. Regulatory Compliance", [
                 "India DPDP Act (2023): Strict statutory liabilities for leaking national identifiers (Aadhaar, PAN).",
                 "EU AI Act (2024): Transparency and auditability mandates for high-risk autonomous AI systems.",
                 "Jain et al. (2023): Western PII scanners fail on code-mixed Hinglish developer text and bare Indian IDs."
             ])

    # -------------------------------------------------------------
    # SLIDE 5: IDENTIFIED RESEARCH GAPS (5 MARKS)
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Critical Research Gaps in State-of-the-Art Tooling", "Literature Review Rubric: Research Gap (5 Marks)")

    gaps = [
        ("Gap 1: Absence of Pre-Execution Deterministic Guardrails",
         "Existing agents rely on stochastic prompt instructions ('Do not leak keys'). Vulnerable to jailbreaks.",
         "Kavach implements Shannon entropy (H > 4.5) & regex that abort before LLM tokenization."),
        ("Gap 2: Complete Blind Spot on Package Slopsquatting",
         "Snyk/Dependabot only scan requirements.txt. No tool intercepts imports in agent-generated code.",
         "AST Package Firewall parsing imports against official PyPI registry APIs (<5ms latency)."),
        ("Gap 3: Missing AST Dependency & Blast-Radius Grounding",
         "Agents modify target files blindly without transitive caller-callee awareness.",
         "Static AST dependency graph computing transitive closure and empirical regression risk."),
        ("Gap 4: Lack of Closed-Loop Self-Healing Sandboxing",
         "Syntactically valid code fails runtime assertions, causing manual debugging fatigue.",
         "ReAct reflection sandbox executing pytest in isolated environments with auto-repair (max 3x)."),
        ("Gap 5: Disconnection from Open Tool Standards (MCP)",
         "Security tools are closed vendor silos requiring proprietary web portals.",
         "Exposed over Anthropic's Model Context Protocol (MCP) as standard JSON-RPC tools for Cursor/Claude.")
    ]

    for idx, (title, flaw, sol) in enumerate(gaps):
        top_pos = Inches(1.8 + idx * 1.0)
        shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.7), Inches(0.85))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = CYAN_ACCENT
        shape.line.width = Pt(1)

        tb = slide5.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = f"{title}: "
        p_t.font.bold = True
        p_t.font.size = Pt(11.5)
        p_t.font.color.rgb = GOLD_ACCENT

        r_flaw = p_t.add_run()
        r_flaw.text = f"Current Flaw: {flaw}  |  "
        r_flaw.font.size = Pt(10)
        r_flaw.font.color.rgb = LIGHT_GRAY

        r_sol = p_t.add_run()
        r_sol.text = f"Kavach Solution: {sol}"
        r_sol.font.size = Pt(10)
        r_sol.font.bold = True
        r_sol.font.color.rgb = GREEN_ACCENT

    # -------------------------------------------------------------
    # SLIDE 6: OBJECTIVES & SCOPE (5 MARKS)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Concrete Research Objectives & Measurable Target Outcomes", "Methodology Rubric: Objective & Problem Definition (5 Marks)")

    add_card(slide6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Primary Research Objectives", [
                 "Objective 1 (Supply-Chain Defense): Intercept all Python AST imports and validate existence on official PyPI index before execution.",
                 "Objective 2 (Zero-Knowledge Pre-Execution Gate): Detect and block 100% of high-entropy credentials (H > 4.5) and Indian identifiers (Aadhaar/PAN).",
                 "Objective 3 (AST Blast-Radius Scoring): Formulate a static dependency algorithm to quantify downstream regression blast radius.",
                 "Objective 4 (Autonomous Self-Healing Loop): Achieve >90% autonomous recovery on runtime test failures using ReAct reflection loops.",
                 "Objective 5 (Open Interoperability): Expose all tools over Model Context Protocol (MCP) for Cursor IDE and Claude Desktop integration."
             ], title_color=CYAN_ACCENT)

    add_card(slide6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Quantitative Evaluation Targets", [
                 "Supply-Chain Catch Rate: 100% precision and recall on hallucinated packages.",
                 "Credential Catch Rate: 100% detection of production AWS/GitHub/Stripe keys.",
                 "PII Detection Rigor: F1 Score >= 0.95 across Indian national identifiers.",
                 "End-to-End Latency: Average pipeline latency <= 1.5 seconds.",
                 "Security Overhead: All pre-execution guards execute in <= 20 ms (< 2% total time).",
                 "Economic Efficiency: Average inference cost <= $0.0005 USD per governed run.",
                 "Automated Test Coverage: Comprehensive suite of 220+ automated unit & integration tests."
             ], title_color=GREEN_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 7: PROPOSED METHODOLOGY & ARCHITECTURE (5 MARKS)
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Proposed Methodology: 6-Stage Governed Agentic Pipeline", "Methodology Rubric: Proposed Methodology (Tools / Techniques / Methods) (5 Marks)")

    stages = [
        ("1. Sentinel Screening", "Shannon Entropy + Regex", "Detects secrets (H > 4.5) and Aadhaar/PAN before invoking LLM."),
        ("2. Qdrant RAG Context", "Dense Vector Cosine Similarity", "Retrieves AST-aware code chunks from 384-d vector database."),
        ("3. AST Blast Radius", "Static Dependency Analysis", "Parses AST to build dependency graph and compute regression impact."),
        ("4. Dual-Engine LLM", "Gemini 2.5 Flash / Local Ollama", "Air-gapped routing: cloud APIs for public tasks; local Qwen for private code."),
        ("5. Package Firewall", "AST Import Extractor + PyPI", "Intercepts external imports and verifies existence on PyPI index."),
        ("6. ReAct Sandbox", "Subprocess Execution + Reflection", "Executes unit tests in sandbox; captures stderr and reflects to repair.")
    ]

    for idx, (s_name, s_tech, s_desc) in enumerate(stages):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.8 + row * 2.5)

        add_card(slide7, left, top, Inches(3.7), Inches(2.2),
                 f"Stage {s_name}", [
                     f"Tech: {s_tech}",
                     f"Function: {s_desc}"
                 ], title_color=CYAN_ACCENT if row == 0 else GREEN_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 8: TOOLS, TECHNIQUES & ALGORITHMS (5 MARKS)
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Technological Implementation & Mathematical Foundations", "Methodology Rubric: Tools, Techniques & Algorithms (5 Marks)")

    add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Technological Stack & Protocols", [
                 "Backend Framework: FastAPI (Async REST + Server-Sent Events real-time telemetry).",
                 "Vector Store: Qdrant Vector Client running all-MiniLM-L6-v2 dense embeddings.",
                 "Code Graph Parser: Python built-in 'ast' module (NodeVisitor traversal).",
                 "Inference Engines: Google Gemini 2.5 Flash API + Local Ollama (qwen2.5-coder:7b).",
                 "Interoperability Standard: Anthropic Model Context Protocol (MCP SDK, JSON-RPC 2.0).",
                 "DevOps Webhook: GitHub Pre-Merge Gatekeeper evaluating PR diffs automatically.",
                 "Frontend Dashboard: Dark-mode Mission Control with Groq Whisper voice input."
             ], title_color=CYAN_ACCENT)

    add_card(slide8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Mathematical Formulations & Algorithms", [
                 "Shannon Entropy Formula for Secret Detection: H = -sum(p_i * log2(p_i)) over character distributions. High entropy (H > 4.5) flags API keys.",
                 "Risk-Adaptive Policy Scoring: Risk = w1*ActionRisk + w2*FindingSeverity + w3*ExposureLevel. Emits ALLOW, REDACT, REVIEW, or BLOCK.",
                 "Cosine Similarity in Qdrant: cos(u, v) = (u . v) / (||u|| * ||v||) for top-k code retrieval.",
                 "Transitive AST Graph Closure: Computes reachability matrix over function call graph to measure affected files.",
                 "ReAct Reflection Algorithm: Formulates prompt from captured stderr tracebacks with strict upper bound N = 3 iterations."
             ], title_color=GOLD_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 9: EXPERIMENTAL DATASETS & BENCHMARKS (5 MARKS)
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Evaluation Datasets & Empirical Experimental Results", "Methodology Rubric: Datasets & Empirical Evaluation (5 Marks)")

    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Evaluation Datasets Evaluated", [
                 "Dataset 1: Package Hallucination Corpus (100 packages): 50 real PyPI packages + 50 documented LLM hallucinations.",
                 "Dataset 2: Multilingual PII & Credential Corpus (100 prompts): English & Hinglish prompts containing Aadhaar, PAN, and cloud keys.",
                 "Dataset 3: Operational 42-Run Evaluation Dataset (42 persistent runs): Real-world traces across 4 user personas logged in workflow_runs.json.",
                 "Dataset 4: AST Impact Test Cases: 5 multi-module repositories evaluating transitive blast-radius precision."
             ], title_color=CYAN_ACCENT)

    add_card(slide9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Empirical Benchmark Findings", [
                 "Package Slopsquatting Catch Rate: 100% Precision, 100% Recall, 100% F1 Score (0 false negatives).",
                 "PII & Credential Detection: F1 = 0.962 on Indian identifiers; 100% catch rate on AWS/GitHub secret tokens.",
                 "Autonomous Self-Healing Rate: 90.0% autonomous recovery within 2 ReAct reflection cycles.",
                 "Pipeline Latency: Average latency 1,370 ms; security guardrails contribute < 20 ms (< 2% overhead).",
                 "LLM-as-a-Judge Accuracy: Average 4.90 / 5.0 rating across 42 evaluated workflow runs."
             ], title_color=GREEN_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 10: IMPLEMENTATION STATUS & CONCLUSION
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Current Implementation Status, Test Evidence & Next Steps", "Project Deliverables & Summary Conclusion")

    add_card(slide10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Verified System Deliverables Completed", [
                 "Automated Test Suite: 220 automated unit & integration tests passing with 100% success rate.",
                 "Live Endpoints: 18 FastAPI endpoints operational (RAG ingest, review, package firewall, self-heal, MCP).",
                 "Open Interoperability: Standalone MCP server successfully exposes tools to Cursor and Claude IDEs.",
                 "Mission Control Dashboard: Deployed with real-time SSE telemetry stream, live KPI counters, and voice input.",
                 "Persistent Data: 42 comprehensive evaluation runs with full stage logs saved in workflow_runs.json."
             ], title_color=CYAN_ACCENT)

    add_card(slide10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Summary & Phase 2 Roadmap", [
                 "Conclusion: Kavach successfully bridges the gap between autonomous agent productivity and enterprise DevSecOps governance.",
                 "Academic Impact: Eliminates supply-chain slopsquatting, stops credential leakage, and guarantees AST blast-radius containment.",
                 "Phase 2 Milestone Plan (October 2026): Integration with enterprise PostgreSQL database, GitHub App OAuth authentication, and continuous pull request gating.",
                 "Submission Ready: All source code, datasets, and benchmarks maintained under a public GitHub repository."
             ], title_color=GOLD_ACCENT)

    # Save
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "PRJ_IV_Documentation"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "PRJ_IV_Midterm_Presentation_8_10_Slides.pptx")
    prs.save(out_path)
    print(f"Successfully generated 10-slide PowerPoint presentation at: {out_path}")

if __name__ == "__main__":
    generate_presentation()
