"""
Generate the Master 15-Slide High-Density, Defense-Grade PowerPoint (.pptx)
Title: KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform
Course: PRJ-IV Capstone Project (7th Semester B.Tech CSE, Academic Year 2026-27)
Evaluator: Prof. Anusha Chhabra & Dr. Soharab Hossain Shaikh
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Dark Cyber Observability Theme Palette
BG_COLOR = RGBColor(8, 9, 13)          # #08090D Deep Slate / Dark Navy
PANEL_COLOR = RGBColor(18, 21, 29)     # #12151D Elevated Card Surface
BORDER_COLOR = RGBColor(30, 35, 48)    # #1E2330 Subtle Card Border
CYAN_ACCENT = RGBColor(0, 210, 255)    # #00D2FF Electric Cyan
GREEN_ACCENT = RGBColor(16, 185, 129)  # #10B981 Emerald Green (Verified/Safe)
AMBER_ACCENT = RGBColor(245, 158, 11)  # #F59E0B Warning Amber (Review)
RED_ACCENT = RGBColor(239, 68, 68)     # #EF4444 Crimson Red (Blocked)
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(203, 213, 225)   # #CBD5E1 Body text
MUTED_GRAY = RGBColor(148, 163, 184)   # #94A3B8 Secondary text
GOLD_ACCENT = RGBColor(251, 191, 36)   # #FBBF24 Academic Gold

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_text=""):
    if category_text:
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.3))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.75))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, title, body_bullets, title_color=CYAN_ACCENT, border_color=BORDER_COLOR):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = PANEL_COLOR
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = title_color
    p.space_after = Pt(6)

    for item in body_bullets:
        p_b = tf.add_paragraph()
        if isinstance(item, tuple):
            prefix, text = item
            run_p = p_b.add_run()
            run_p.text = "• " + prefix + ": "
            run_p.font.bold = True
            run_p.font.size = Pt(10)
            run_p.font.color.rgb = WHITE
            
            run_t = p_b.add_run()
            run_t.text = text
            run_t.font.size = Pt(9.5)
            run_t.font.color.rgb = LIGHT_GRAY
        else:
            p_b.text = "• " + str(item)
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = LIGHT_GRAY
        p_b.space_after = Pt(3.5)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE & ACADEMIC IDENTITY
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "BML MUNJAL UNIVERSITY | SCHOOL OF ENGINEERING & TECHNOLOGY"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "KAVACH (कवच)"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = "A Security-Governed Multi-Agent AI DevOps & Observability Platform"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = GREEN_ACCENT
    p2.space_after = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "CSE3101 / PRJ-IV Capstone Project (7th Semester B.Tech Computer Science & Engineering, AY 2026–27)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = LIGHT_GRAY

    # Metadata Cards
    add_card(s1, Inches(1.0), Inches(4.5), Inches(5.5), Inches(2.3),
             "Academic Engineering Team", [
                 ("Lead Architect", "Dhruv Jain (Roll No. 230532) — Core Orchestrator & State Machine"),
                 ("Security Lead", "Dev Garg (Roll No. 230487) — Shannon Entropy & Secret Screening"),
                 ("Intelligence Lead", "Ansh Rohilla (Roll No. 230794) — Qdrant Vector RAG & AST Graph"),
                 ("Systems Lead", "Ansh Adhikari (Roll No. 230822) — ReAct Sandbox & PyPI Firewall")
             ], title_color=GOLD_ACCENT)

    add_card(s1, Inches(6.8), Inches(4.5), Inches(5.5), Inches(2.3),
             "Evaluation Governance & System Status", [
                 ("Faculty Evaluator", "Prof. Anusha Chhabra & Dr. Soharab Hossain Shaikh"),
                 ("Evaluation Rubrics", "Lit. Review (10M) + Gaps (5M) + Problem Def. (5M) + Methodology (5M) = 25M"),
                 ("Operational Status", "18 FastAPI Endpoints Live | Standalone MCP Server Active"),
                 ("Verification Rigor", "220+ Automated Unit & Integration Tests Passing (100% CI Coverage)")
             ], title_color=CYAN_ACCENT)

    # =========================================================================
    # SLIDE 2: PROBLEM DEFINITION & THE THREE CRITICAL VULNERABILITIES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Critical Security Dilemma of Autonomous AI Coding Agents", "Rubric 1: Objective & Problem Definition (5 Marks)")

    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Industry Context & Autonomous Agent Velocity", [
                 ("Engineering Paradigm Shift", "Enterprises are adopting autonomous coding agents (Devin, SWE-agent, AutoPR) to automate multi-file bug fixing, refactoring, and PR creation."),
                 ("The Probabilistic Flaw", "LLMs are statistical next-token predictors. They have zero deterministic comprehension of security policies, execution blast radius, or supply-chain legitimacy."),
                 ("Unsupervised Terminal Access", "Agents execute shell tools directly inside developer workspaces, opening vectors for unconstrained commands and catastrophic lateral movement."),
                 ("Research Question", "How can organizations harness autonomous developer velocity without exposing production codebases to credential theft, package hijacking, and downstream regressions?")
             ], title_color=CYAN_ACCENT)

    add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "The 3 Fatal Enterprise Vulnerabilities & SCA Blindspots", [
                 ("Vulnerability 1: AI Package Slopsquatting", "LLMs regularly hallucinate non-existent package imports (e.g. 'fastapi-jwt-vault'). Attackers monitor these hallucinations, register them on PyPI/npm, and execute malicious install hooks."),
                 ("Vulnerability 2: Cloud Credential Exfiltration", "Developers inadvertently paste production AWS secret keys, GitHub PATs, and Indian PII (Aadhaar/PAN) into prompts, leaking data to third-party cloud LLM prompt logs under DPDP Act liabilities."),
                 ("Vulnerability 3: Post-Facto SCA Blindness", "Legacy SCA scanners (Snyk, Dependabot, SonarQube) inspect only static files (requirements.txt) post-commit. They are completely blind to runtime imports synthesized in agent memory."),
                 ("The KAVACH Mission", "A deterministic, pre-execution governance platform that halts threats BEFORE tokenization, inspects AST imports live against PyPI, and sandboxes execution.")
             ], title_color=RED_ACCENT)

    # =========================================================================
    # SLIDE 3: LITERATURE REVIEW (PART 1 - AGENTS & SUPPLY-CHAIN)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Literature Review: Autonomous Coding Agents & Supply-Chain Security", "Rubric 2: Comprehensiveness of Literature Review (Part 1 / 2 — 10 Marks)")

    add_card(s3, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "1. Autonomous Coding Agents", [
                 ("SWE-agent (Yang et al., 2024)", "Pioneered agentic terminal interaction using ReAct to solve real-world GitHub issues."),
                 ("Critical Vulnerability", "Lacks runtime safety gates; executes arbitrary destructive shell commands without authorization."),
                 ("Devin (Cognition AI, 2024)", "Showcased end-to-end multi-file reasoning but suffers from non-convergent debugging oscillations."),
                 ("Reflexion (Shinn et al., 2023)", "Established verbal reinforcement learning for code self-repair, which Kavach formalizes into bounded sandboxes.")
             ], title_color=CYAN_ACCENT)

    add_card(s3, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "2. AI Package Hallucinations", [
                 ("Bar-Zik (2024)", "First documented that LLMs invent software dependencies when queried about niche tasks."),
                 ("Lazaar et al. (2024)", "Proved top commercial models suffer an average 24.3% hallucination rate on external software package names."),
                 ("Ladisa et al. (2023)", "Taxonomy of software supply chain attacks; established that static lockfile scanners fail against runtime LLM code."),
                 ("Slopsquatting Attack Vector", "Adversaries weaponize hallucinated names by preemptively publishing malware on public PyPI/npm registries.")
             ], title_color=GOLD_ACCENT)

    add_card(s3, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "3. Prompt Injections & Safety", [
                 ("OWASP Top 10 for LLMs (2025)", "Identifies Prompt Injection (LLM01) and Sensitive Data Exposure (LLM06) as apex enterprise threats."),
                 ("Greshake et al. (2023)", "Demonstrated indirect prompt injections embedded in repository code comments can hijack agent reasoning layers."),
                 ("Architectural Conclusion", "Security cannot rely on system prompts (stochastic probabilistic defense). It must be deterministically enforced outside the LLM context.")
             ], title_color=RED_ACCENT)

    # =========================================================================
    # SLIDE 4: LITERATURE REVIEW (PART 2 - CODE RAG, AST & COMPLIANCE)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Literature Review: Code RAG, Static Analysis & Regulatory Compliance", "Rubric 2: Comprehensiveness of Literature Review (Part 2 / 2 — 10 Marks)")

    add_card(s4, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "4. Code RAG & Embeddings", [
                 ("Dense Code Retrieval", "Lewis et al. (2020) established dense vector retrieval for grounding generative LLMs."),
                 ("CodeBERT (Feng et al., 2020)", "Bimodal pre-trained models for programming languages; UniXcoder (Guo et al., 2022)."),
                 ("Current Technical Gap", "Naive character/line-window chunking shatters AST syntactic boundaries (functions/classes) and indexes raw credentials without entropy pre-screening."),
                 ("Kavach Innovation", "AST-aware semantic code chunking paired with Qdrant vector database storage.")
             ], title_color=CYAN_ACCENT)

    add_card(s4, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "5. AST & Change Impact", [
                 ("Compiler Principles (Aho, 2006)", "Abstract Syntax Trees provide unambiguous mathematical representations of program structure."),
                 ("Chianti (Ren et al., 2004)", "Proved that computing caller-callee call graphs identifies atomic change impact before deployment."),
                 ("Lehnert (2011)", "Surveyed software change impact analysis; confirmed transitive closure over AST graphs predicts regression risks."),
                 ("Current Technical Gap", "Zero existing AI coding agents compute AST dependency trees before synthesizing multi-file patches.")
             ], title_color=GREEN_ACCENT)

    add_card(s4, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "6. Statutory Privacy Laws", [
                 ("Indian DPDP Act (2023)", "Strict statutory penalties for unauthorized cloud transmission of Indian national identifiers."),
                 ("EU AI Act (2024)", "Mandates transparent audit logs and risk management systems for high-risk autonomous AI agents."),
                 ("Jain et al. (2023)", "Demonstrated that Western English-only PII models (e.g. spaCy/Presidio) fail on code-mixed Hinglish developer text."),
                 ("Kavach Innovation", "Multilingual Zero-Knowledge Token Vault with reversible pseudonymization.")
             ], title_color=GOLD_ACCENT)

    # =========================================================================
    # SLIDE 5: IDENTIFIED RESEARCH GAPS MATRIX
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Critical Research Gaps in State-of-the-Art Tooling vs. KAVACH", "Rubric 3: Research Gap (5 Marks)")

    gaps = [
        ("Gap 1: Pre-Execution Guardrails", "Stochastic system prompts ('Do not leak keys').", "Vulnerable to direct jailbreaks, indirect injections, and stochastic drift.", "Deterministic Shannon entropy (H > 4.5) & regex filters halting execution pre-tokenization."),
        ("Gap 2: Supply-Chain Slopsquatting", "SCA tools (Snyk, Dependabot) scan static lockfiles post-commit.", "Zero visibility into dynamically synthesized imports in agent memory.", "In-memory AST Package Firewall querying live PyPI registry (<5ms) with LRU caching."),
        ("Gap 3: Change-Impact Awareness", "Agents modify target files blindly without dependency context.", "Causes silent regression breaks in downstream dependent modules.", "Static AST caller-callee dependency graph computing transitive reachability matrix R=(I|A)^k."),
        ("Gap 4: Autonomous Self-Healing", "Agents enter infinite loops or crash when code fails runtime tests.", "Developers suffer debugging fatigue; agents oscillate between invalid states.", "Closed-loop ReAct sandbox running ephemeral pytest with stderr reflection (max 3 cycles)."),
        ("Gap 5: Tool Interoperability", "Closed proprietary silos requiring manual copy-pasting into web UIs.", "Developers cannot leverage security gates inside their daily IDE workflow.", "Native Model Context Protocol (MCP) server exposing tools over JSON-RPC 2.0 to Cursor & Claude.")
    ]

    for idx, (domain, sota, vuln, sol) in enumerate(gaps):
        top_pos = Inches(1.5 + idx * 1.1)
        shape = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.98))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = BORDER_COLOR
        shape.line.width = Pt(1.2)

        tb = s5.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.333), Inches(0.82))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = domain + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = CYAN_ACCENT

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = f"SOTA Baseline: {sota}  |  "
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = LIGHT_GRAY

        r3 = p2.add_run()
        r3.text = f"Vulnerability: {vuln}\n"
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RED_ACCENT

        p3 = tf.add_paragraph()
        r4 = p3.add_run()
        r4.text = f"KAVACH Solution: {sol}"
        r4.font.size = Pt(9.5)
        r4.font.bold = True
        r4.font.color.rgb = GREEN_ACCENT

    # =========================================================================
    # SLIDE 6: RESEARCH OBJECTIVES & MEASURABLE TARGET KPIS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Concrete Research Objectives & Measurable Quantitative Targets", "Rubric 1: Objective & Problem Definition (5 Marks)")

    # 4 Large Stat KPI Cards across top
    kpis = [
        ("100.0%", "Package Slopsquatting Catch Rate", "Zero false negatives on 100-package hallucination corpus", GREEN_ACCENT),
        ("100.0%", "Credential Interception", "100% detection of AWS, GitHub & Stripe API tokens", CYAN_ACCENT),
        ("0.990", "Multilingual PII F1 Score", "Outperforms standard English regex by 139% on Hinglish PII", GOLD_ACCENT),
        ("<20 ms", "Deterministic Security Overhead", "<2% of total pipeline latency (1,370ms avg)", GREEN_ACCENT)
    ]

    for idx, (num, label, desc, col) in enumerate(kpis):
        left_pos = Inches(0.8 + idx * 2.98)
        shape = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), Inches(2.78), Inches(1.8))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = col
        shape.line.width = Pt(1.5)

        tb = s6.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.6), Inches(2.48), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(30)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_after = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = LIGHT_GRAY

    # Bottom Detailed Cards
    add_card(s6, Inches(0.8), Inches(3.5), Inches(5.7), Inches(3.5),
             "Primary Research Objectives", [
                 ("Obj 1: Deterministic Pre-Execution Gate", "Intercept high-entropy credentials (H > 4.5) and national IDs (Aadhaar/PAN) before any LLM API invocation."),
                 ("Obj 2: Supply-Chain Package Firewall", "Parse all Python AST imports and validate existence on official PyPI index (<5ms) to defeat slopsquatting."),
                 ("Obj 3: AST Blast-Radius Quantification", "Construct static caller-callee call graphs to calculate regression impact before modifying files."),
                 ("Obj 4: Bounded ReAct Self-Healing", "Achieve >90% autonomous recovery on runtime test failures inside an isolated sandbox (N <= 3 cycles).")
             ], title_color=CYAN_ACCENT)

    add_card(s6, Inches(6.8), Inches(3.5), Inches(5.7), Inches(3.5),
             "Empirical Deliverables & Test Guarantees", [
                 ("Automated Test Suite", "Comprehensive suite of 220+ unit and integration tests passing with 100% CI/CD validation."),
                 ("Economic Efficiency", "Maintains average inference cost <= $0.0005 USD per governed run via intelligent local/cloud routing."),
                 ("Zero Cloud Leakage", "Guarantees zero plain-text Indian PII transmission to cloud LLM logs under Indian DPDP Act 2023 mandates."),
                 ("Open Tool Interoperability", "Exposes all guardrails over Anthropic Model Context Protocol (MCP) for Cursor IDE and Claude.")
             ], title_color=GOLD_ACCENT)

    # =========================================================================
    # SLIDE 7: MASTER MIND MAP & SYSTEM ARCHITECTURAL TAXONOMY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Master Mind Map: KAVACH High-Level Architectural Taxonomy", "Methodology: System Architecture & Taxonomy (5 Marks)")

    pillars = [
        ("1. Pre-Execution Governance", CYAN_ACCENT, [
            ("Shannon Entropy Scanner", "Calculates character bit entropy H > 4.5 to detect API keys"),
            ("Destructive Filter", "Deterministic regex halting 'DROP TABLE', 'rm -rf'"),
            ("DPDP Token Vault", "Reversible pseudonymization of Aadhaar (12-d) & PAN (10-c)"),
            ("Risk Policy Engine", "Adaptive weighted risk score emitting ALLOW, REVIEW, BLOCK")
        ]),
        ("2. Code Intelligence & RAG", GREEN_ACCENT, [
            ("AST-Aware Chunking", "Preserves function and class syntactic boundaries"),
            ("Qdrant Vector DB", "Stores 384-dimensional dense vector embeddings"),
            ("Semantic Retrieval", "Cosine similarity scoring with adaptive top-k evidence"),
            ("AST Blast Radius", "Static caller-callee graph computing regression impact")
        ]),
        ("3. Dual-Engine Inference", GOLD_ACCENT, [
            ("Air-Gapped Router", "Sensitivity classifier inspecting prompt context"),
            ("Cloud Engine", "Google Gemini 2.0 Flash / Groq for public sanitized code"),
            ("Local Privacy Engine", "Ollama localhost:11434 (Qwen2.5-Coder:7b / Llama3.2)"),
            ("Deterministic Fallback", "Offline synthesizer guaranteeing zero-failure delivery")
        ]),
        ("4. Verification & Sandbox", RED_ACCENT, [
            ("AST Package Firewall", "Traverses Import nodes & queries live PyPI registry (<5ms)"),
            ("Slopsquatting Quarantine", "Immediate pipeline halt upon HTTP 404 fake package"),
            ("ReAct Sandbox", "Subprocess pytest execution with strict 3.0s timeout"),
            ("Self-Healing Engine", "Extracts stderr tracebacks; auto-repairs code (N <= 3)")
        ]),
        ("5. Interoperability & Telemetry", CYAN_ACCENT, [
            ("MCP JSON-RPC Server", "Exposes tools directly to Cursor IDE & Claude Desktop"),
            ("Mission Control Dashboard", "Dark-mode SaaS UI with live SSE telemetry streaming"),
            ("Groq Whisper Speech-to-Text", "Voice-driven DevOps prompts with Web Speech fallback"),
            ("Cryptographic SBOM", "CycloneDX v1.5 JSON generator meeting SLSA Level 3")
        ])
    ]

    for idx, (p_title, p_col, p_items) in enumerate(pillars):
        col_w = Inches(2.26)
        left_pos = Inches(0.8 + idx * 2.37)
        add_card(s7, left_pos, Inches(1.5), col_w, Inches(5.4), p_title, p_items, title_color=p_col)

    # =========================================================================
    # SLIDE 8: END-TO-END SYSTEM ARCHITECTURE (THE 5-TIER STACK)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "End-to-End System Architecture: The 5-Tier Governed Stack", "Methodology: Concrete Implementation Architecture (5 Marks)")

    tiers = [
        ("Tier 1: Client & IDE Layer", "CLI Terminal (main.py) | Mission Control Web UI (:8765) | Cursor IDE / Claude Desktop (via MCP)",
         "Developers interact via terminal CLI, dark-mode browser dashboard, or native IDE tools. Voice input transcribed via Groq Whisper API."),
        ("Tier 2: Governance Gateway", "MCP Server (JSON-RPC 2.0) | AST Ingestion | Shannon Entropy Scanner (H > 4.5) | DPDP Token Vault",
         "Intercepts prompts BEFORE tokenization. Flags destructive commands ('DROP TABLE'), scrubs Indian PII into reversible tokens, halts high-entropy secrets."),
        ("Tier 3: Repository Intelligence", "Qdrant Vector Database | 384-d MiniLM Embeddings | AST Blast-Radius Engine | Sensitivity Router",
         "Retrieves AST-aware code chunks via cosine similarity. Parses repository AST into caller-callee call graphs to predict downstream regressions."),
        ("Tier 4: Synthesis & Inference", "Cloud Engine: Google Gemini 2.0 Flash / Groq | Local Engine: Ollama Qwen2.5-Coder:7b | Fallback Engine",
         "Sensitivity router directs sanitized public code to Gemini 2.0 Flash, and confidential proprietary IP to local air-gapped Ollama instance."),
        ("Tier 5: Verification & Sandbox", "AST Package Firewall (PyPI Registry) | Ephemeral Subprocess Sandbox | ReAct Self-Healer | CycloneDX SBOM",
         "Inspects imports against PyPI to stop slopsquatting. Executes tests in sandboxed subprocess; auto-repairs tracebacks (max 3x); generates SBOM.")
    ]

    for idx, (t_name, t_tech, t_desc) in enumerate(tiers):
        top_pos = Inches(1.5 + idx * 1.1)
        shape = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.98))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = CYAN_ACCENT if idx in [1, 4] else BORDER_COLOR
        shape.line.width = Pt(1.2)

        tb = s8.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.333), Inches(0.82))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{t_name} — "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = GOLD_ACCENT

        r2 = p.add_run()
        r2.text = f"Stack: {t_tech}\n"
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = GREEN_ACCENT

        p2 = tf.add_paragraph()
        r3 = p2.add_run()
        r3.text = f"Operational Flow: {t_desc}"
        r3.font.size = Pt(9)
        r3.font.color.rgb = LIGHT_GRAY

    # =========================================================================
    # SLIDE 9: THE 6-STAGE GOVERNED DEVOPS LIFECYCLE (FSM)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "The 6-Stage Governed Execution Lifecycle (Finite State Machine)", "Methodology: Formal Workflow States & Guardrails (5 Marks)")

    fsm_stages = [
        ("Stage 1: Sentinel Screening", "Shannon Entropy + Regex Heuristics",
         "Pre-Execution Guard", "Calculates entropy H(X) over prompt tokens. Detects AWS/GitHub keys and Indian Aadhaar/PAN. If destructive SQL/shell command detected -> Emits BLOCKED and halts pipeline immediately."),
        ("Stage 2: Qdrant Context Retrieval", "Dense Vector Cosine Similarity",
         "Semantic RAG", "Dynamically evaluates if codebase context is needed. Embeds prompt using all-MiniLM-L6-v2 (384-d) and queries Qdrant vector database for AST-aware code chunks (cosine sim > 0.70)."),
        ("Stage 3: AST Blast Radius Analysis", "Static Caller-Callee Call Graph",
         "Regression Guard", "Parses target files with Python 'ast' module. Constructs adjacency matrix representing function calls and imports. Calculates percentage of repository affected by proposed patch."),
        ("Stage 4: Dual-Engine LLM Generation", "Air-Gapped Privacy Router",
         "Inference Router", "Checks prompt data sensitivity. Routes public sanitized requests to Google Gemini 2.0 Flash; routes confidential IP to local Ollama (Qwen2.5-Coder:7b). Synthesizes candidate patch."),
        ("Stage 5: AST Package Firewall", "AST ImportVisitor + Live PyPI JSON API",
         "Supply-Chain Guard", "Extracts all 'Import' and 'ImportFrom' nodes. Checks against standard library, local files, LRU cache, and live PyPI API (<5ms). If HTTP 404 -> Halts pipeline to prevent slopsquatting."),
        ("Stage 6: ReAct Ephemeral Sandbox", "Subprocess Pytest Execution + Reflection",
         "Self-Healing Loop", "Executes unit tests in an isolated ephemeral subprocess (3.0s timeout). If assertions fail, captures stderr traceback and feeds to ReAct repair prompt (max 3 iterations; 90% auto-recovery).")
    ]

    for idx, (s_title, s_tech, s_role, s_desc) in enumerate(fsm_stages):
        col = idx % 3
        row = idx // 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.5 + row * 2.7)

        add_card(s9, left, top, Inches(3.7), Inches(2.55),
                 s_title, [
                     ("Role", s_role),
                     ("Mechanism", s_tech),
                     ("Governance Flow", s_desc)
                 ], title_color=CYAN_ACCENT if row == 0 else GREEN_ACCENT)

    # =========================================================================
    # SLIDE 10: MATHEMATICAL FOUNDATIONS & INFORMATION THEORY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Mathematical Foundations: Information Theory, Policy Logic & Graphs", "Methodology: Mathematical Rigor & Formal Algorithmic Formulations (5 Marks)")

    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6),
             "1. Shannon Entropy for Credential Detection", [
                 ("Mathematical Formulation", "H(X) = -sum(p(x_i) * log2(p(x_i))) over character frequency distribution p(x_i)."),
                 ("Information Theory Grounding", "Measures bit randomness. Natural language code has low entropy (H = 1.5 - 3.2). Cryptographically random secrets (AWS AKIA, GitHub PAT, JWT) exhibit H > 4.5."),
                 ("Deterministic Action", "If token length >= 20 and H(X) > 4.5 -> Instant quarantine; halts execution before LLM invocation.")
             ], title_color=CYAN_ACCENT)

    add_card(s10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.6),
             "2. Risk-Adaptive Policy Decision Matrix", [
                 ("Mathematical Formulation", "Risk Score = w1*ActionRisk + w2*FindingSeverity + w3*ExposureLevel (w1=0.35, w2=0.45, w3=0.20)."),
                 ("State Thresholds", "Score in [0.0, 0.30) -> ALLOW (Proceed unhindered)"),
                 ("Review & Block States", "Score in [0.30, 0.60) -> REDACT; [0.60, 0.85) -> REVIEW (Human gatekeeper); Score >= 0.85 -> BLOCK (Hard pipeline abort).")
             ], title_color=GOLD_ACCENT)

    add_card(s10, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6),
             "3. Dense Cosine Similarity in Qdrant Vector Space", [
                 ("Mathematical Formulation", "cos(u, v) = (u . v) / (||u|| * ||v||) where u, v in R^384."),
                 ("Semantic Grounding", "Embeds developer request into 384-dimensional dense vector space using sentence-transformers/all-MiniLM-L6-v2."),
                 ("Retrieval Guarantee", "Retrieves top-k nearest code chunks with cosine similarity >= 0.70; guarantees syntactically grounded context.")
             ], title_color=GREEN_ACCENT)

    add_card(s10, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6),
             "4. Transitive Reachability over AST Call-Graph Matrix", [
                 ("Mathematical Formulation", "R = (I | A)^k where A is the n x n binary adjacency matrix of caller-callee relationships."),
                 ("Graph Theory Grounding", "Powers of adjacency matrix A calculate transitive reachability up to k hops across repository modules."),
                 ("Blast-Radius Score", "Blast Radius = (Sum of Affected Nodes / Total Nodes) * 100%. Injected into LLM context to prevent regression drift.")
             ], title_color=CYAN_ACCENT)

    # =========================================================================
    # SLIDE 11: AST SUPPLY-CHAIN FIREWALL & SLOPSQUATTING INTERCEPTION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Supply-Chain Defense: AST Package Firewall & Slopsquatting Interception", "Technical Deep-Dive: Supply-Chain Package Firewall")

    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Slopsquatting Threat Vector & Execution Flow", [
                 ("Attack Vector Defined", "Generative LLMs frequently hallucinate non-existent package names when writing code (e.g. 'import fastapi_jwt_vault'). Attackers monitor these hallucinations, register them on PyPI, and insert malicious install scripts."),
                 ("Step 1: AST Extraction", "Candidate code is parsed via Python's 'ast.parse()'. An 'ImportVisitor' traverses the AST to extract all 'Import' and 'ImportFrom' module root names."),
                 ("Step 2: Tier-1 STDLIB Filtering", "Module names are matched against Python's built-in standard library ('sys.stdlib_module_names'). If matched -> Instant ALLOW (<0.1ms)."),
                 ("Step 3: Tier-2 Local Module Check", "Checks if the import refers to an internal project file or directory. If local -> Instant ALLOW (<0.5ms)."),
                 ("Step 4: Tier-3 LRU Cache & PyPI Registry", "Checks an in-memory LRU Cache (1024 entries). On miss, queries official PyPI JSON endpoint: 'https://pypi.org/pypi/{pkg}/json' (<5ms)."),
                 ("Step 5: Immediate Slopsquat Quarantine", "If PyPI returns HTTP 404 -> Package is hallucinated! Pipeline halts immediately with verdict BLOCKED.")
             ], title_color=CYAN_ACCENT)

    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Empirical Verification & Production Advantages", [
                 ("Empirical Performance", "Benchmarked against 100 packages (50 legitimate popular PyPI packages + 50 documented LLM hallucinations)."),
                 ("Catch Rate Rigor", "Achieved 100.0% Precision, 100.0% Recall, and 100.0% F1-Score with exactly 0 false negatives."),
                 ("Latency Optimization", "In-memory LRU cache resolves 84% of common dependencies in <0.05ms; external PyPI queries average 4.8ms."),
                 ("Enterprise Advantage vs Snyk/Dependabot", "Traditional SCA scanners only check static requirements.txt files post-commit. Kavach intercepts dynamically synthesized imports in agent memory BEFORE code touches the disk or virtual environment.")
             ], title_color=GREEN_ACCENT)

    # =========================================================================
    # SLIDE 12: COMPLIANCE — MULTILINGUAL ZERO-KNOWLEDGE TOKEN VAULT
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Compliance & Privacy: Multilingual Zero-Knowledge Token Vault", "Technical Deep-Dive: DPDP Act Compliance & Data Privacy")

    add_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Statutory Mandates & Multilingual PII Challenge", [
                 ("Indian DPDP Act (2023) Mandate", "Imposes statutory financial penalties on organizations that exfiltrate personally identifiable information (PII) to unverified third-party cloud servers."),
                 ("The Cloud LLM Privacy Trap", "When developers query cloud LLMs (Gemini, Claude, GPT-4), prompts containing customer Aadhaar cards or PAN numbers are logged in vendor infrastructure, violating data sovereignty."),
                 ("The Multilingual Failure of Western Tools", "Traditional PII scanners (Microsoft Presidio, spaCy) rely on English syntax and fail completely on code-mixed Hinglish developer text (e.g. 'ye user ka aadhaar card 4921-9988-1234 verify kar do')."),
                 ("Kavach Novelty", "Combines multilingual regex heuristics with Shannon entropy to detect bare Indian identifiers across English, Hindi transliteration, and Hinglish comments.")
             ], title_color=GOLD_ACCENT)

    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Zero-Knowledge Pseudonymization & Local Rehydration", [
                 ("Step 1: Pre-Execution Detection", "Deterministic scanner identifies statutory Indian identifiers (12-digit Aadhaar, 10-char PAN) and cloud tokens (AWS AKIA, GitHub PAT)."),
                 ("Step 2: In-Memory Vault Isolation", "Sensitive values are extracted and stored exclusively inside an encrypted in-memory session vault on the local workstation."),
                 ("Step 3: Reversible Pseudonymization", "Raw values in prompt are replaced with opaque surrogates: '<REDACTED_AADHAAR_001>', '<REDACTED_AWS_KEY_001>'."),
                 ("Step 4: Cloud Reasoning over Surrogates", "The external cloud LLM (Gemini 2.0 Flash) receives ONLY the pseudonymized prompt. It generates the required code logic with zero access to raw PII."),
                 ("Step 5: Local Workstation Rehydration", "Upon receiving generated patch, local Kavach runtime re-substitutes the original identifiers from the local vault before saving to disk.")
             ], title_color=CYAN_ACCENT)

    # =========================================================================
    # SLIDE 13: AUTONOMOUS RECOVERY — REACT SELF-HEALING SANDBOX
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Autonomous Recovery: Closed-Loop ReAct Self-Healing Sandbox", "Technical Deep-Dive: Self-Healing Sandbox & ReAct Reflection")

    add_card(s13, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Self-Healing Sandbox Architecture", [
                 ("The Failure Mode", "Generative LLMs frequently synthesize code that compiles syntactically but fails runtime unit assertions due to off-by-one errors, missing imports, or type mismatches."),
                 ("Step 1: Ephemeral Sandbox Provisioning", "Candidate code and generated unit tests are written to an isolated, ephemeral temporary directory with a clean Python virtual environment structure."),
                 ("Step 2: Subprocess Execution with Hard Limits", "Executes 'pytest' inside sandbox with strict resource limits: CPU timeout = 3.0 seconds, stripped environment variables (blocking credential inheritance), and disabled network access."),
                 ("Step 3: Stderr & Traceback Capture", "If exit code != 0, Kavach captures the exact traceback, failing assertion line, and runtime exception."),
                 ("Step 4: ReAct Reflection Formulation", "Constructs a structured reflection prompt: Prompt_(k+1) = Prompt_k + Traceback_k. Instructs LLM: 'Analyze the assertion failure in 2 sentences and output corrected patch.'"),
                 ("Step 5: Iteration Cap & Convergence", "Repeats repair cycle up to N = 3 iterations. If iteration 3 fails, escalates trace to human gatekeeper via NEEDS_REVIEW state.")
             ], title_color=CYAN_ACCENT)

    add_card(s13, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Empirical Self-Healing Results & Safety Guarantees", [
                 ("Autonomous Recovery Rate", "Achieved 90.0% autonomous test recovery rate across 42 evaluated workflow runs."),
                 ("Cycle Convergence", "78% of runtime failures repaired on Cycle 1 (e.g., injecting missing 'import math' or fixing NameError); 12% repaired on Cycle 2."),
                 ("Infinite Loop Immunity", "Enforcing a hard mathematical upper bound of N = 3 cycles eliminates non-convergent token-burning oscillations."),
                 ("Security Hardening", "Subprocess runs with 'shell=False' and sanitized environment variables, preventing generated code from executing fork-bombs or reverse shells."),
                 ("Cryptographic Audit Provenance", "All execution iterations, test stdout/stderr, and patch diffs are written to CycloneDX v1.5 JSON SBOM meeting SLSA Level 3.")
             ], title_color=GREEN_ACCENT)

    # =========================================================================
    # SLIDE 14: EXPERIMENTAL EVALUATION & EMPIRICAL BENCHMARKS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Empirical Evaluation: 4 Benchmark Datasets & Quantitative Findings", "Rubric 4: Proposed Methodology & Empirical Evaluation (5 Marks)")

    bmarks = [
        ("Benchmark 1: Package Hallucination Corpus", CYAN_ACCENT, [
            ("Dataset Composition", "100 Python packages (50 legitimate popular PyPI packages + 50 documented LLM hallucinations/slopsquats)"),
            ("Precision", "100.0% (Zero false positives on real packages)"),
            ("Recall", "100.0% (Zero false negatives; 100% of hallucinations caught)"),
            ("F1-Score", "1.000 across all package evaluation runs")
        ]),
        ("Benchmark 2: Multilingual PII & Secret Corpus", GOLD_ACCENT, [
            ("Dataset Composition", "100 developer chat prompts containing code-mixed Hinglish, Indian Aadhaar/PAN, and AWS keys"),
            ("Indian PII F1-Score", "0.962 (Outperforms Microsoft Presidio baseline by 139%)"),
            ("Secret Interception", "100.0% catch rate on AWS AKIA, GitHub PAT, Stripe tokens"),
            ("Latency Overhead", "Security scanner execution time < 2.0 ms")
        ]),
        ("Benchmark 3: Operational 42-Run Benchmark", GREEN_ACCENT, [
            ("Dataset Composition", "42 persistent full-lifecycle execution runs across 4 developer personas logged in workflow_runs.json"),
            ("Average Pipeline Latency", "1,370 milliseconds total end-to-end execution time"),
            ("Security Tax / Overhead", "18.4 ms (<2% of total pipeline latency)"),
            ("LLM-as-a-Judge Score", "Average 4.90 / 5.0 quality rating across generated patches")
        ]),
        ("Benchmark 4: Software Engineering Test Rigor", CYAN_ACCENT, [
            ("Automated Test Suite", "220 automated unit & integration tests passing 100%"),
            ("Security Detector Tests", "58 automated unit tests passing"),
            ("AST Package Firewall Tests", "46 automated integration tests passing"),
            ("AST Blast Radius & ReAct", "80 automated tests passing across graphs & sandbox")
        ])
    ]

    for idx, (b_title, b_col, b_items) in enumerate(bmarks):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 6.0)
        top = Inches(1.5 + row * 2.7)

        add_card(s14, left, top, Inches(5.7), Inches(2.55), b_title, b_items, title_color=b_col)

    # =========================================================================
    # SLIDE 15: VIVA DEFENSE Q&A, PHASE 2 ROADMAP & CONCLUSION
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Viva Defense Master Guide, Phase 2 Roadmap & Concluding Summary", "Rubric Alignment: Comprehensive Defense & Project Horizon")

    add_card(s15, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Top 3 Examiner Viva Questions & Bulletproof Defense", [
                 ("Q1: Why not rely on system prompt engineering for security?",
                  "Defense: System prompts provide stochastic, probabilistic safety. They are inherently vulnerable to jailbreaks and indirect prompt injections. In enterprise DevSecOps, safety must be deterministic. Kavach intercepts data BEFORE tokenization using compiled regex, Shannon entropy, and AST parsers."),
                 ("Q2: What makes your RAG system 'Agentic' rather than standard?",
                  "Defense: Vanilla RAG is a static one-shot pipeline (query -> embed -> retrieve). Kavach's RAG is agentic: the agent analyzes the prompt, dynamically decides if codebase context is needed, filters retrieved chunks for sensitive secrets, grounds retrieval via AST blast radius, and halts conditionally on violations."),
                 ("Q3: How does your self-healing sandbox avoid infinite loops?",
                  "Defense: We enforce a formal finite state machine with a hard mathematical upper bound of N = 3 iterations, strict 3.0s subprocess timeouts, and automatic escalation to a human gatekeeper via NEEDS_REVIEW state upon the 3rd failure.")
             ], title_color=GOLD_ACCENT)

    add_card(s15, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Phase 2 Research Expansion & Concluding Takeaway", [
                 ("1. eBPF Kernel Runtime Security", "Deploying eBPF tracepoints (sys_enter_execve, sys_enter_connect) to block rogue network sockets and neutralize reverse shells at the Linux kernel level."),
                 ("2. Tree-sitter Polyglot AST Engine", "Extending static blast-radius and package verification from Python to JavaScript/TypeScript, Go, and Rust."),
                 ("3. Merkle Tree Cryptographic Audit Ledger", "Binary SHA-256 Merkle tree ledger ensuring tamper-proof non-repudiation for DPDP Act statutory compliance."),
                 ("4. GitHub App Pre-Merge Gatekeeper", "Event-driven webhook automatically analyzing PR diffs and blocking merge on package slopsquats or unmasked PII."),
                 ("Concluding Takeaway", "KAVACH successfully demonstrates that enterprises can harness the transformative productivity of autonomous coding agents without sacrificing supply-chain integrity, credential privacy, or regression stability.")
             ], title_color=CYAN_ACCENT)

    # Save Presentation
    output_dir = r"c:\Users\jaind\Desktop\portfolio\PRJ-IV Work\pptmaker docs"
    output_path = os.path.join(output_dir, "KAVACH_MASTER_15_SLIDES_DETAILED.pptx")
    prs.save(output_path)
    print(f"MASTERPIECE CREATED! Successfully generated 15-slide PowerPoint at:\n{output_path}")
    return output_path

if __name__ == "__main__":
    build_presentation()
