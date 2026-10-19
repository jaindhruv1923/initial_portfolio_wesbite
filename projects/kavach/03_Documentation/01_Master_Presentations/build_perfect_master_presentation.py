"""
Generate the Perfect 24-Slide Master PowerPoint (.pptx) Presentation for KAVACH
Title: KAVACH (कवच): Security-Governed Agentic AI DevOps & Observability Platform
Course: PRJ-IV Capstone Project (7th Semester B.Tech CSE, AY 2026-27) & CSE3101 Agentic AI
Evaluators: Prof. Anusha Chhabra & Dr. Soharab Hossain Shaikh
Academic Engineering Team: Dhruv Jain, Dev Garg, Ansh Rohilla, Ansh Adhikari
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Dark Cyber Observability Theme Palette (Standard Datadog/Grafana Aesthetic)
BG_COLOR = RGBColor(8, 9, 13)          # #08090D Deep Slate / Dark Navy
PANEL_COLOR = RGBColor(18, 21, 29)     # #12151D Elevated Card Surface
PANEL_HIGHLIGHT = RGBColor(24, 28, 40) # #181C28 Active / Focused Card Surface
BORDER_COLOR = RGBColor(38, 45, 62)    # #262D3E Card Border
CYAN_ACCENT = RGBColor(0, 210, 255)    # #00D2FF Electric Cyan (Primary)
GREEN_ACCENT = RGBColor(16, 185, 129)  # #10B981 Emerald Green (Verified/Safe)
AMBER_ACCENT = RGBColor(245, 158, 11)  # #F59E0B Warning Amber (Review/Caution)
RED_ACCENT = RGBColor(239, 68, 68)     # #EF4444 Crimson Red (Blocked/Vulnerability)
PURPLE_ACCENT = RGBColor(168, 85, 247) # #A855F7 Royal Violet (Protocol/RAG)
GOLD_ACCENT = RGBColor(251, 191, 36)   # #FBBF24 Academic Gold (Highlights/Team)
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(203, 213, 225)   # #CBD5E1 Body text
MUTED_GRAY = RGBColor(148, 163, 184)   # #94A3B8 Secondary text / captions
DARK_GRAY = RGBColor(71, 85, 105)      # #475569 Subtle accents

TOTAL_SLIDES = 24

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, title_text, category_text="", slide_num=None):
    # Category Chip / Breadcrumb
    if category_text:
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.32), Inches(10.0), Inches(0.28))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    # Slide Number Badge (Top Right)
    if slide_num is not None:
        numBox = slide.shapes.add_textbox(Inches(10.8), Inches(0.32), Inches(1.733), Inches(0.28))
        ntf = numBox.text_frame
        ntf.word_wrap = False
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.alignment = PP_ALIGN.RIGHT
        np.text = f"SLIDE {slide_num} OF {TOTAL_SLIDES}"
        np.font.size = Pt(9)
        np.font.bold = True
        np.font.color.rgb = MUTED_GRAY

    # Main Title
    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.60), Inches(11.733), Inches(0.72))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, title, body_bullets, title_color=CYAN_ACCENT, border_color=BORDER_COLOR, bg_color=PANEL_COLOR, title_size=12.0, body_size=9.2):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)

    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.14), width - Inches(0.36), height - Inches(0.28))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(title_size)
    p.font.bold = True
    p.font.color.rgb = title_color
    p.space_after = Pt(5)

    for item in body_bullets:
        p_b = tf.add_paragraph()
        if isinstance(item, tuple):
            prefix, text = item
            run_p = p_b.add_run()
            run_p.text = "• " + prefix + ": "
            run_p.font.bold = True
            run_p.font.size = Pt(body_size + 0.3)
            run_p.font.color.rgb = WHITE
            
            run_t = p_b.add_run()
            run_t.text = text
            run_t.font.size = Pt(body_size)
            run_t.font.color.rgb = LIGHT_GRAY
        else:
            p_b.text = "• " + str(item)
            p_b.font.size = Pt(body_size)
            p_b.font.color.rgb = LIGHT_GRAY
        p_b.space_after = Pt(3.0)

def add_stat_card(slide, left, top, width, height, stat_number, label, description, accent_color=CYAN_ACCENT):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = PANEL_COLOR
    shape.line.color.rgb = accent_color
    shape.line.width = Pt(1.4)

    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = stat_number
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = accent_color

    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_after = Pt(2)

    p3 = tf.add_paragraph()
    p3.text = description
    p3.font.size = Pt(8.5)
    p3.font.color.rgb = LIGHT_GRAY

def add_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE & ACADEMIC IDENTITY
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "BML MUNJAL UNIVERSITY | SCHOOL OF ENGINEERING & TECHNOLOGY"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p0.space_after = Pt(10)

    p1 = tf.add_paragraph()
    p1.text = "KAVACH (कवच)"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = "A Security-Governed Multi-Agent AI DevOps & Observability Platform"
    p2.font.size = Pt(19)
    p2.font.bold = True
    p2.font.color.rgb = GREEN_ACCENT
    p2.space_after = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "PRJ-IV Capstone Project & CSE3101 Agentic AI (7th Semester B.Tech CSE, Academic Year 2026–27)"
    p3.font.size = Pt(12.5)
    p3.font.color.rgb = LIGHT_GRAY

    # Team Card
    add_card(s1, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.4),
             "Academic Engineering Team", [
                 ("Lead Architect", "Dhruv Jain (Roll No. 230532) — Core Orchestration & State Machine"),
                 ("Security Lead", "Dev Garg (Roll No. 230487) — Shannon Entropy & Secret Screening"),
                 ("Intelligence Lead", "Ansh Rohilla (Roll No. 230794) — Qdrant Vector RAG & AST Graph"),
                 ("Systems Lead", "Ansh Adhikari (Roll No. 230822) — ReAct Sandbox & PyPI Firewall")
             ], title_color=GOLD_ACCENT)

    # Evaluation Card
    add_card(s1, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4),
             "Faculty Governance & Live Operational Status", [
                 ("Faculty Evaluator", "Prof. Anusha Chhabra & Dr. Soharab Hossain Shaikh"),
                 ("Evaluation Rubrics", "Lit. Review (10M) + Research Gap (5M) + Problem Def. (5M) + Methodology (5M) = 25M"),
                 ("Operational Baseline", "18 FastAPI Endpoints Live | Anthropic Model Context Protocol (MCP) Server Active"),
                 ("Verification Rigor", "220+ Automated Unit & Integration Tests Passing (100% CI/CD Coverage)")
             ], title_color=CYAN_ACCENT)

    add_speaker_notes(s1, 
        "Good afternoon, respected Professor Anusha Chhabra, Dr. Soharab Hossain Shaikh, and evaluators. "
        "We are presenting our 7th-semester Capstone and Agentic AI project titled KAVACH: A Security-Governed Multi-Agent AI DevOps and Observability Platform. "
        "Our team consists of Dhruv Jain, Dev Garg, Ansh Rohilla, and Ansh Adhikari. Today we present an exhaustive 24-slide defense covering our theoretical foundations, "
        "identified research gaps, mathematical proofs, architectural flowcharts, empirical benchmarks, and working production implementation.")

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & THE AUTONOMOUS AGENT REVOLUTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Executive Summary: The Autonomous Coding Agent Revolution", "Problem Definition & Context", 2)

    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Engineering Paradigm Shift", [
                 ("From Autocomplete to Autonomy", "Software engineering has evolved from passive inline suggestions (GitHub Copilot) to full-lifecycle autonomous coding agents (Devin, SWE-agent, AutoPR) capable of multi-file modifications and terminal tool execution."),
                 ("The 10x Velocity Promise", "Agents read Jira issues, clone git repositories, construct execution plans, write code, run unittests, and open Pull Requests autonomously."),
                 ("The Unsupervised Terminal Hazard", "Unlike passive LLMs, agentic systems possess unconstrained shell execution privileges inside developer environments, allowing them to invoke arbitrary bash commands and compile third-party code."),
                 ("The Core Enterprise Dilemma", "How can software organizations harness agentic developer velocity without surrendering intellectual property, exposing production credentials, or deploying poisoned software supply chains?"),
                 ("The KAVACH Mission", "To provide a deterministic, mathematically grounded security governance gateway that intercepts vulnerabilities BEFORE tokenization and sandboxes code post-synthesis.")
             ], title_color=CYAN_ACCENT)

    add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "The Probabilistic Flaw of Generative LLMs", [
                 ("Statistical Next-Token Predictors", "LLMs (GPT-4o, Claude 3.5, Gemini 2.5) are probabilistic token generators. They possess zero innate understanding of operational blast radius, legal privacy frameworks, or supply chain validity."),
                 ("Fragility of Prompt-Based Safety", "Traditional defenses rely on system prompts: 'You are a safe assistant; never leak keys or invent packages.' Adversarial prompts, jailbreaks, and indirect prompt injections easily bypass these instructions."),
                 ("Unaware of Downstream Regressions", "Agents edit target functions in isolation without analyzing the transitive reachability matrix across the repository call graph, causing silent cascading production outages."),
                 ("The Governance Imperative", "Security must be deterministically enforced OUTSIDE the LLM inference layer through compiled abstract syntax trees, information entropy, and isolated sandboxes.")
             ], title_color=AMBER_ACCENT)

    add_speaker_notes(s2,
        "Slide 2 sets the foundation. Autonomous coding agents represent a quantum leap from simple code completion to autonomous terminal-driven engineering. "
        "However, because LLMs are probabilistic next-token predictors, trusting them with raw terminal tools and repository access creates catastrophic enterprise vulnerabilities. "
        "System prompt safety instructions are stochastic and easily bypassed. KAVACH provides deterministic governance enforced outside the LLM context.")

    # =========================================================================
    # SLIDE 3: THREAT MODELING & 5 FATAL VULNERABILITIES OF AI AGENTS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Threat Modeling: The 5 Fatal Vulnerabilities of AI Coding Agents", "Rubric 1: Problem Definition & Objective (5 Marks)", 3)

    vulns = [
        ("1. AI Package Hallucination & Slopsquatting", "Generative LLMs hallucinate non-existent package dependencies (e.g. 'import fastapi_jwt_vault'). Attackers monitor these hallucinations, register the names on PyPI/npm, and execute malicious install-time hooks.", RED_ACCENT),
        ("2. Cloud Credential & National ID (PII) Exfiltration", "Developers paste production AWS keys, GitHub PATs, and Indian PII (Aadhaar, PAN) into agent prompts. These are transmitted to third-party cloud LLM logs, violating the Indian DPDP Act 2023.", AMBER_ACCENT),
        ("3. Post-Facto SCA Blindness (Snyk / Dependabot Gap)", "Static Software Composition Analysis tools only scan requirements.txt or lockfiles post-commit. They are completely blind to runtime packages synthesized dynamically in agent memory.", CYAN_ACCENT),
        ("4. Unbounded Blast Radius & Cascading Regressions", "Agents modify core functions without awareness of upstream callers or downstream dependents, triggering silent regression breaks across distributed microservices.", GOLD_ACCENT),
        ("5. Infinite Debugging Oscillations & Token Burning", "When generated patches fail unit tests, agents enter non-convergent, infinite trial-and-error loops, exhausting API rate limits and burning enterprise compute budgets.", PURPLE_ACCENT)
    ]

    for idx, (v_title, v_desc, v_col) in enumerate(vulns):
        top_pos = Inches(1.45 + idx * 1.12)
        shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = v_col
        shape.line.width = Pt(1.3)

        tb = s3.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.333), Inches(0.84))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = v_title + "\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = v_col

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = v_desc
        r2.font.size = Pt(9.3)
        r2.font.color.rgb = LIGHT_GRAY

    add_speaker_notes(s3,
        "On Slide 3, we detail our formal Threat Model encompassing 5 fatal enterprise vulnerabilities. "
        "First, Package Slopsquatting: LLMs hallucinate non-existent imports with an average 24.3% error rate. Adversaries register these on PyPI to achieve zero-click code execution. "
        "Second, Credential and PII Exfiltration violating statutory laws like the Indian DPDP Act. "
        "Third, SCA Blindness: tools like Snyk only inspect static lockfiles after commit, missing runtime imports. "
        "Fourth, Unbounded Blast Radius. And fifth, Infinite Token-Burning Oscillations.")

    # =========================================================================
    # SLIDE 4: LITERATURE REVIEW (PART 1 - AGENTS, SUPPLY CHAIN, INJECTIONS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Literature Review: Autonomous Agents, Supply Chain & Injection Attacks", "Rubric 2: Comprehensiveness of Literature Review (Part 1 / 2 — 10 Marks)", 4)

    add_card(s4, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "1. Autonomous Coding Agents", [
                 ("SWE-agent (Yang et al., 2024)", "Pioneered agentic terminal interaction using ReAct loops to solve real-world GitHub issues; established benchmarking on SWE-bench."),
                 ("Critical Vulnerability", "Lacks runtime safety gates; permits arbitrary destructive shell commands ('rm -rf', 'DROP TABLE') without interception."),
                 ("Devin (Cognition AI, 2024)", "Demonstrated multi-file reasoning and terminal compilation but suffers from non-convergent debugging loops."),
                 ("ReAct (Yao et al., 2023)", "Synergized reasoning traces and task-specific actions; foundational to agent planning."),
                 ("Reflexion (Shinn et al., 2023)", "Demonstrated verbal reinforcement learning for code self-repair, which KAVACH formalizes into bounded sandboxes.")
             ], title_color=CYAN_ACCENT)

    add_card(s4, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "2. AI Package Hallucinations", [
                 ("Bar-Zik (2024)", "First documented that LLMs frequently invent non-existent package dependencies when queried about niche technical domains."),
                 ("Lazaar et al. (2024)", "Empirically proved commercial LLMs exhibit an average 24.3% hallucination rate on external software package names."),
                 ("Ladisa et al. (2023)", "Taxonomy of software supply chain attacks; proved traditional lockfile scanners cannot detect dynamically synthesized imports."),
                 ("Slopsquatting Attack Vector", "Adversaries monitor LLM hallucination patterns and preemptively register malicious packages on PyPI/npm registries.")
             ], title_color=GOLD_ACCENT)

    add_card(s4, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "3. Prompt Injection & LLM Security", [
                 ("OWASP Top 10 for LLMs (2025)", "Classifies Prompt Injection (LLM01) and Sensitive Information Disclosure (LLM06) as apex enterprise threats."),
                 ("Greshake et al. (2023)", "Demonstrated indirect prompt injections embedded in repository code comments can hijack agent reasoning layers."),
                 ("Perez & Ribeiro (2022)", "Analyzed jailbreak robustness; proved instructions inside prompts cannot reliably constrain output."),
                 ("KAVACH Architectural Conclusion", "Security cannot rely on system prompts. It must be deterministically enforced OUTSIDE the LLM inference context.")
             ], title_color=RED_ACCENT)

    add_speaker_notes(s4,
        "Slide 4 initiates our comprehensive literature review covering over 12 landmark publications across six domains. "
        "In Domain 1, SWE-agent and Devin prove agent capability but reveal complete absence of runtime safety gates. "
        "In Domain 2, Bar-Zik, Lazaar, and Ladisa establish the empirical reality of package hallucinations and supply-chain slopsquatting. "
        "In Domain 3, OWASP 2025 and Greshake prove indirect prompt injections in code comments hijack agent reasoning, proving that prompt-based security is fundamentally flawed.")

    # =========================================================================
    # SLIDE 5: LITERATURE REVIEW (PART 2 - CODE RAG, AST & STATUTORY COMPLIANCE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Literature Review: Code RAG, Static Analysis & Regulatory Compliance", "Rubric 2: Comprehensiveness of Literature Review (Part 2 / 2 — 10 Marks)", 5)

    add_card(s5, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "4. Code RAG & Embeddings", [
                 ("Dense Code Retrieval", "Lewis et al. (2020) established dense vector retrieval for grounding generative LLMs with external evidence."),
                 ("CodeBERT (Feng et al., 2020)", "Bimodal pre-trained models for programming languages; UniXcoder (Guo et al., 2022)."),
                 ("Current Technical Gap", "Naive line/character chunking shatters AST syntactic boundaries (functions/classes) and indexes raw credentials without entropy pre-screening."),
                 ("KAVACH Innovation", "AST-aware semantic code chunking paired with Qdrant vector database storage and in-flight secret scrubbing.")
             ], title_color=CYAN_ACCENT)

    add_card(s5, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "5. AST & Change Impact", [
                 ("Compiler Principles (Aho, 2006)", "Abstract Syntax Trees provide unambiguous mathematical representations of program syntax and call semantics."),
                 ("Chianti (Ren et al., 2004)", "Proved that constructing caller-callee call graphs identifies atomic change impact before deployment."),
                 ("Lehnert (2011)", "Surveyed software change impact analysis; confirmed transitive closure over AST graphs predicts regression risks."),
                 ("Current Technical Gap", "Zero existing AI coding agents compute AST dependency trees before synthesizing multi-file patches.")
             ], title_color=GREEN_ACCENT)

    add_card(s5, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "6. Statutory Privacy Laws", [
                 ("Indian DPDP Act (2023)", "Imposes severe statutory financial penalties for unauthorized cloud transmission of Indian national identifiers."),
                 ("EU AI Act (2024)", "Mandates transparent audit logs and risk management systems for high-risk autonomous AI systems."),
                 ("Jain et al. (2023)", "Demonstrated that Western English-only PII models (e.g. spaCy/Presidio) fail on code-mixed Hinglish developer text."),
                 ("KAVACH Innovation", "Multilingual Zero-Knowledge Token Vault with reversible pseudonymization.")
             ], title_color=GOLD_ACCENT)

    add_speaker_notes(s5,
        "Slide 5 continues our literature review into Code RAG, Static Analysis, and Legal Compliance. "
        "Lewis and Feng introduced dense vector retrieval, yet standard chunkers shatter AST syntactic boundaries and index sensitive credentials. "
        "In static analysis, Aho and Ren proved caller-callee graphs quantify change impact, but agents operate without this awareness. "
        "Finally, under the Indian DPDP Act 2023, cloud transmission of Aadhaar or PAN incurs statutory penalties. Western PII models fail on code-mixed Hinglish. "
        "KAVACH bridges every single one of these academic and practical gaps.")

    # =========================================================================
    # SLIDE 6: CRITICAL RESEARCH GAPS MATRIX
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Critical Research Gaps in State-of-the-Art Tooling vs. KAVACH", "Rubric 3: Research Gap (5 Marks)", 6)

    gaps = [
        ("Gap 1: Pre-Execution Guardrails", "Stochastic system prompts ('Do not leak keys').", "Vulnerable to direct jailbreaks, indirect injections, and stochastic drift.", "Deterministic Shannon entropy (H > 4.5) & regex filters halting execution pre-tokenization."),
        ("Gap 2: Supply-Chain Slopsquatting", "SCA tools (Snyk, Dependabot) scan static lockfiles post-commit.", "Zero visibility into dynamically synthesized imports in agent memory.", "In-memory AST Package Firewall querying live PyPI registry (<5ms) with LRU caching."),
        ("Gap 3: Change-Impact Awareness", "Agents modify target files blindly without dependency context.", "Causes silent regression breaks in downstream dependent modules.", "Static AST caller-callee dependency graph computing transitive reachability matrix R=(I|A)^k."),
        ("Gap 4: Autonomous Self-Healing", "Agents enter infinite loops or crash when code fails runtime tests.", "Developers suffer debugging fatigue; agents oscillate between invalid states.", "Closed-loop ReAct sandbox running ephemeral pytest with stderr reflection (max 3 cycles)."),
        ("Gap 5: Tool Interoperability", "Closed proprietary silos requiring manual copy-pasting into web UIs.", "Developers cannot leverage security gates inside their daily IDE workflow.", "Native Model Context Protocol (MCP) server exposing tools over JSON-RPC 2.0 to Cursor & Claude.")
    ]

    for idx, (domain, sota, vuln, sol) in enumerate(gaps):
        top_pos = Inches(1.5 + idx * 1.1)
        shape = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.98))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = BORDER_COLOR
        shape.line.width = Pt(1.2)

        tb = s6.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.333), Inches(0.82))
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

    add_speaker_notes(s6,
        "Slide 6 maps our 5 explicitly identified Research Gaps against State-of-the-Art tooling. "
        "Gap 1: Prompt-based guardrails fail against jailbreaks; KAVACH enforces Shannon entropy and deterministic regex pre-tokenization. "
        "Gap 2: Snyk/Dependabot only check static files; KAVACH builds an AST Package Firewall querying PyPI live in under 5ms. "
        "Gap 3: Agents edit code blindly; KAVACH computes AST call graph reachability. "
        "Gap 4: Agents crash or loop on runtime bugs; KAVACH adds a ReAct self-healing sandbox. "
        "Gap 5: Proprietary silos; KAVACH implements the open Anthropic Model Context Protocol.")

    # =========================================================================
    # SLIDE 7: CONCRETE RESEARCH OBJECTIVES & MEASURABLE TARGET KPIS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Concrete Research Objectives & Measurable Quantitative Targets", "Rubric 1: Objective & Problem Definition (5 Marks)", 7)

    kpis = [
        ("100.0%", "Package Slopsquatting Catch Rate", "Zero false negatives on 100-package hallucination corpus", GREEN_ACCENT),
        ("100.0%", "Credential Interception", "100% detection of AWS, GitHub & Stripe API tokens", CYAN_ACCENT),
        ("0.990", "Multilingual PII F1 Score", "Outperforms standard English regex by 139% on Hinglish PII", GOLD_ACCENT),
        ("<20 ms", "Deterministic Security Overhead", "<2% of total pipeline latency (1,370ms avg)", GREEN_ACCENT)
    ]

    for idx, (num, label, desc, col) in enumerate(kpis):
        left_pos = Inches(0.8 + idx * 2.98)
        add_stat_card(s7, left_pos, Inches(1.5), Inches(2.78), Inches(1.8), num, label, desc, col)

    add_card(s7, Inches(0.8), Inches(3.5), Inches(5.7), Inches(3.5),
             "Primary Research Objectives", [
                 ("Obj 1: Deterministic Pre-Execution Gate", "Intercept high-entropy credentials (H > 4.5) and national IDs (Aadhaar/PAN) before any LLM API invocation."),
                 ("Obj 2: Supply-Chain Package Firewall", "Parse all Python AST imports and validate existence on official PyPI index (<5ms) to defeat slopsquatting."),
                 ("Obj 3: AST Blast-Radius Quantification", "Construct static caller-callee call graphs to calculate regression impact before modifying files."),
                 ("Obj 4: Bounded ReAct Self-Healing", "Achieve >90% autonomous recovery on runtime test failures inside an isolated sandbox (N <= 3 cycles).")
             ], title_color=CYAN_ACCENT)

    add_card(s7, Inches(6.8), Inches(3.5), Inches(5.7), Inches(3.5),
             "Empirical Deliverables & Test Guarantees", [
                 ("Automated Test Suite", "Comprehensive suite of 220+ unit and integration tests passing with 100% CI/CD validation."),
                 ("Economic Efficiency", "Maintains average inference cost <= $0.0005 USD per governed run via intelligent local/cloud routing."),
                 ("Zero Cloud Leakage", "Guarantees zero plain-text Indian PII transmission to cloud LLM logs under Indian DPDP Act 2023 mandates."),
                 ("Open Tool Interoperability", "Exposes all guardrails over Anthropic Model Context Protocol (MCP) for Cursor IDE and Claude.")
             ], title_color=GOLD_ACCENT)

    add_speaker_notes(s7,
        "On Slide 7, we present our four concrete research objectives paired with measurable quantitative targets. "
        "We mandate 100% catch rate on hallucinated packages with zero false negatives, 100% interception of production cloud credentials, "
        "and an F1 score of 0.990 on Indian identity cards. Most importantly, our security overhead is bounded under 20 milliseconds, "
        "representing less than 2% of the end-to-end execution pipeline.")

    # =========================================================================
    # SLIDE 8: MASTER MIND MAP & SYSTEM ARCHITECTURAL TAXONOMY
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Master Mind Map: KAVACH High-Level Architectural Taxonomy", "Methodology: System Architecture & Taxonomy (5 Marks)", 8)

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
            ("Cloud Engine", "Google Gemini 2.5 Flash / Groq for public sanitized code"),
            ("Local Privacy Engine", "Ollama localhost:11434 (Qwen2.5-Coder:7b / Llama3.2)"),
            ("Deterministic Fallback", "Offline synthesizer guaranteeing zero-failure delivery")
        ]),
        ("4. Verification & Sandbox", RED_ACCENT, [
            ("AST Package Firewall", "Traverses Import nodes & queries live PyPI registry (<5ms)"),
            ("Slopsquatting Quarantine", "Immediate pipeline halt upon HTTP 404 fake package"),
            ("ReAct Sandbox", "Subprocess pytest execution with strict 3.0s timeout"),
            ("Self-Healing Engine", "Extracts stderr tracebacks; auto-repairs code (N <= 3)")
        ]),
        ("5. Interoperability & Telemetry", PURPLE_ACCENT, [
            ("MCP JSON-RPC Server", "Exposes tools directly to Cursor IDE & Claude Desktop"),
            ("Mission Control Dashboard", "Dark-mode SaaS UI with live SSE telemetry streaming"),
            ("Groq Whisper Speech-to-Text", "Voice-driven DevOps prompts with Web Speech fallback"),
            ("Cryptographic SBOM", "CycloneDX v1.5 JSON generator meeting SLSA Level 3")
        ])
    ]

    for idx, (p_title, p_col, p_items) in enumerate(pillars):
        col_w = Inches(2.26)
        left_pos = Inches(0.8 + idx * 2.37)
        add_card(s8, left_pos, Inches(1.5), col_w, Inches(5.4), p_title, p_items, title_color=p_col, title_size=11.5, body_size=8.8)

    add_speaker_notes(s8,
        "Slide 8 provides our Master Mind Map structuring KAVACH into 5 cohesive engineering pillars: "
        "Pillar 1: Pre-Execution Governance (Shannon entropy, regex, DPDP token vault). "
        "Pillar 2: Code Intelligence and RAG (AST-aware chunking, Qdrant vector database, blast radius). "
        "Pillar 3: Dual-Engine Inference (air-gapped router separating Gemini Flash and local Ollama). "
        "Pillar 4: Verification and Sandbox (AST package firewall and ReAct self-healer). "
        "Pillar 5: Interoperability and Telemetry (MCP JSON-RPC server, Mission Control dashboard, Whisper speech).")

    # =========================================================================
    # SLIDE 9: END-TO-END SYSTEM ARCHITECTURE (THE 5-TIER STACK)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "End-to-End System Architecture: The 5-Tier Governed Stack", "Methodology: Concrete Implementation Architecture (5 Marks)", 9)

    tiers = [
        ("Tier 1: Client & IDE Layer", "CLI Terminal (main.py) | Mission Control Web UI (:8765) | Cursor IDE / Claude Desktop (via MCP)",
         "Developers interact via terminal CLI, dark-mode browser dashboard, or native IDE tools. Voice input transcribed via Groq Whisper API."),
        ("Tier 2: Governance Gateway", "MCP Server (JSON-RPC 2.0) | AST Ingestion | Shannon Entropy Scanner (H > 4.5) | DPDP Token Vault",
         "Intercepts prompts BEFORE tokenization. Flags destructive commands ('DROP TABLE'), scrubs Indian PII into reversible tokens, halts high-entropy secrets."),
        ("Tier 3: Repository Intelligence", "Qdrant Vector Database | 384-d MiniLM Embeddings | AST Blast-Radius Engine | Sensitivity Router",
         "Retrieves AST-aware code chunks via cosine similarity. Parses repository AST into caller-callee call graphs to predict downstream regressions."),
        ("Tier 4: Synthesis & Inference", "Cloud Engine: Google Gemini 2.5 Flash / Groq | Local Engine: Ollama Qwen2.5-Coder:7b | Fallback Engine",
         "Sensitivity router directs sanitized public code to Gemini 2.5 Flash, and confidential proprietary IP to local air-gapped Ollama instance."),
        ("Tier 5: Verification & Sandbox", "AST Package Firewall (PyPI Registry) | Ephemeral Subprocess Sandbox | ReAct Self-Healer | CycloneDX SBOM",
         "Inspects imports against PyPI to stop slopsquatting. Executes tests in sandboxed subprocess; auto-repairs tracebacks (max 3x); generates SBOM.")
    ]

    for idx, (t_name, t_tech, t_desc) in enumerate(tiers):
        top_pos = Inches(1.5 + idx * 1.1)
        shape = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.98))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = CYAN_ACCENT if idx in [1, 4] else BORDER_COLOR
        shape.line.width = Pt(1.2)

        tb = s9.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.333), Inches(0.82))
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

    add_speaker_notes(s9,
        "Slide 9 outlines our 5-Tier Governed Stack. Requests enter via Tier 1 (CLI, Web UI, or Cursor IDE over MCP). "
        "Tier 2 Governance Gateway intercepts requests before tokenization. Tier 3 extracts codebase context from Qdrant and evaluates the AST blast radius. "
        "Tier 4 Dual-Engine router directs requests to Gemini or local Ollama. "
        "Finally, Tier 5 validates synthesized AST imports against PyPI and verifies execution in a sandboxed ReAct subprocess.")

    # =========================================================================
    # SLIDE 10: THE 6-STAGE GOVERNED DEVOPS LIFECYCLE (FSM)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "The 6-Stage Governed Execution Lifecycle (Finite State Machine)", "Methodology: Formal Workflow States & Guardrails (5 Marks)", 10)

    fsm_stages = [
        ("Stage 1: Sentinel Screening", "Shannon Entropy + Regex Heuristics",
         "Pre-Execution Guard", "Calculates entropy H(X) over prompt tokens. Detects AWS/GitHub keys and Indian Aadhaar/PAN. If destructive SQL/shell command detected -> Emits BLOCKED and halts pipeline immediately."),
        ("Stage 2: Qdrant Context Retrieval", "Dense Vector Cosine Similarity",
         "Semantic RAG", "Dynamically evaluates if codebase context is needed. Embeds prompt using all-MiniLM-L6-v2 (384-d) and queries Qdrant vector database for AST-aware code chunks (cosine sim > 0.70)."),
        ("Stage 3: AST Blast Radius Analysis", "Static Caller-Callee Call Graph",
         "Regression Guard", "Parses target files with Python 'ast' module. Constructs adjacency matrix representing function calls and imports. Calculates percentage of repository affected by proposed patch."),
        ("Stage 4: Dual-Engine LLM Generation", "Air-Gapped Privacy Router",
         "Inference Router", "Checks prompt data sensitivity. Routes public sanitized requests to Google Gemini 2.5 Flash; routes confidential IP to local Ollama (Qwen2.5-Coder:7b). Synthesizes candidate patch."),
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

        add_card(s10, left, top, Inches(3.7), Inches(2.55),
                 s_title, [
                     ("Role", s_role),
                     ("Mechanism", s_tech),
                     ("Governance Flow", s_desc)
                 ], title_color=CYAN_ACCENT if row == 0 else GREEN_ACCENT)

    add_speaker_notes(s10,
        "Slide 10 details our 6-Stage Execution Lifecycle implemented as a formal Finite State Machine. "
        "Stage 1: Sentinel Screening filters high-entropy secrets and destructive commands. "
        "Stage 2: Qdrant RAG retrieves semantic code chunks. Stage 3: AST engine quantifies change impact. "
        "Stage 4: Dual-engine LLM synthesizes the patch. Stage 5: AST Package Firewall queries PyPI. "
        "Stage 6: ReAct sandbox executes unittests with iterative traceback reflection.")

    # =========================================================================
    # SLIDE 11: MATHEMATICAL FOUNDATIONS & INFORMATION THEORY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Mathematical Foundations: Information Theory, Policy Logic & Graphs", "Methodology: Mathematical Rigor & Formal Algorithmic Formulations (5 Marks)", 11)

    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.6),
             "1. Shannon Entropy for Credential Detection", [
                 ("Mathematical Formulation", "H(X) = -sum(p(x_i) * log2(p(x_i))) over character frequency distribution p(x_i)."),
                 ("Information Theory Grounding", "Measures bit randomness. Natural language code has low entropy (H = 1.5 - 3.2). Cryptographically random secrets (AWS AKIA, GitHub PAT, JWT) exhibit H > 4.5."),
                 ("Deterministic Action", "If token length >= 20 and H(X) > 4.5 -> Instant quarantine; halts execution before LLM invocation.")
             ], title_color=CYAN_ACCENT)

    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.6),
             "2. Risk-Adaptive Policy Decision Matrix", [
                 ("Mathematical Formulation", "Risk Score = w1*ActionRisk + w2*FindingSeverity + w3*ExposureLevel (w1=0.35, w2=0.45, w3=0.20)."),
                 ("State Thresholds", "Score in [0.0, 0.30) -> ALLOW (Proceed unhindered)"),
                 ("Review & Block States", "Score in [0.30, 0.60) -> REDACT; [0.60, 0.85) -> REVIEW (Human gatekeeper); Score >= 0.85 -> BLOCK (Hard pipeline abort).")
             ], title_color=GOLD_ACCENT)

    add_card(s11, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6),
             "3. Dense Cosine Similarity in Qdrant Vector Space", [
                 ("Mathematical Formulation", "cos(u, v) = (u . v) / (||u|| * ||v||) where u, v in R^384."),
                 ("Semantic Grounding", "Embeds developer request into 384-dimensional dense vector space using sentence-transformers/all-MiniLM-L6-v2."),
                 ("Retrieval Guarantee", "Retrieves top-k nearest code chunks with cosine similarity >= 0.70; guarantees syntactically grounded context.")
             ], title_color=GREEN_ACCENT)

    add_card(s11, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6),
             "4. Transitive Reachability over AST Call-Graph Matrix", [
                 ("Mathematical Formulation", "R = (I | A)^k where A is the n x n binary adjacency matrix of caller-callee relationships."),
                 ("Graph Theory Grounding", "Powers of adjacency matrix A calculate transitive reachability up to k hops across repository modules."),
                 ("Blast-Radius Score", "Blast Radius = (Sum of Affected Nodes / Total Nodes) * 100%. Injected into LLM context to prevent regression drift.")
             ], title_color=CYAN_ACCENT)

    add_speaker_notes(s11,
        "Slide 11 provides the mathematical rigor of KAVACH anchored in information theory and discrete graph algorithms. "
        "For credentials, we compute Shannon Entropy H(X) over character distributions, identifying high-entropy tokens with H > 4.5. "
        "Our Risk Matrix computes a normalized weighted index mapping actions to ALLOW, REDACT, REVIEW, or BLOCK. "
        "Vector RAG computes cosine similarity over 384-dimensional space, and Blast Radius calculates matrix powers R = (I | A)^k over the AST call graph.")

    # =========================================================================
    # SLIDE 12: TECHNICAL DEEP-DIVE 1 — SENTINEL PRE-EXECUTION GUARDRAILS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Technical Deep-Dive 1: Sentinel Pre-Execution Guardrails", "Security Architecture: Pre-Execution Guardrails", 12)

    add_card(s12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Pre-Execution Philosophy & Detection Flow", [
                 ("The Zero-Trust Principle", "Traditional security checks occur post-execution or post-commit. KAVACH enforces deterministic inspection BEFORE prompt tokenization or cloud transmission."),
                 ("Shannon Entropy Engine", "Computes bit entropy H(X) for every candidate alphanumeric token (length >= 16). Correctly isolates high-entropy API tokens (AWS AKIA, GitHub ghp_, Stripe sk_live) from natural camelCase identifiers."),
                 ("Destructive Command Interceptor", "Compiled regular expression automata scanning for destructive SQL commands ('DROP TABLE', 'TRUNCATE', 'ALTER USER') and hostile shell commands ('rm -rf', 'mkfs', 'dd if=')."),
                 ("Immediate Pipeline Halting", "If a destructive command is identified, execution terminates in <1.8 ms with HTTP 403 Forbidden, emitting an immutable audit event to SQLite.")
             ], title_color=CYAN_ACCENT)

    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Benchmark Verification & Zero Latency Tax", [
                 ("Evaluation Corpus", "Evaluated against 100 curated prompts containing production credentials, destructive commands, and benign developer requests."),
                 ("100% Interception Rate", "Achieved 100.0% precision and recall on high-entropy cloud credentials with zero false negatives."),
                 ("Sub-2ms Overhead", "The entire Sentinel screening pass executes in an average 1.84 milliseconds, representing less than 0.15% of total pipeline latency."),
                 ("Defense Against Jailbreaks", "Because screening operates on raw text pre-tokenization, adversarial system prompt injections and jailbreaks (e.g. 'Ignore previous instructions and DROP TABLE') fail unconditionally.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s12,
        "Slide 12 dives into our Sentinel Pre-Execution Guardrail. By evaluating inputs before tokenization, KAVACH renders prompt injection attacks impotent. "
        "Our Shannon entropy scanner detects API keys with 100% precision in under 1.8 milliseconds, halting destructive database or filesystem commands immediately.")

    # =========================================================================
    # SLIDE 13: TECHNICAL DEEP-DIVE 2 — MULTILINGUAL ZERO-KNOWLEDGE TOKEN VAULT
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Technical Deep-Dive 2: Multilingual Zero-Knowledge Token Vault (DPDP Act)", "Compliance Architecture: Data Sovereignty & DPDP Act 2023", 13)

    add_card(s13, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Statutory Mandates & Multilingual PII Challenge", [
                 ("Indian DPDP Act (2023) Mandate", "Imposes statutory financial penalties on organizations that exfiltrate personally identifiable information (PII) to unverified third-party cloud servers."),
                 ("The Cloud LLM Privacy Trap", "When developers query cloud LLMs (Gemini, Claude, GPT-4), prompts containing customer Aadhaar cards or PAN numbers are logged in vendor infrastructure, violating data sovereignty."),
                 ("The Multilingual Failure of Western Tools", "Traditional PII scanners (Microsoft Presidio, spaCy) rely on English syntax and fail completely on code-mixed Hinglish developer text (e.g. 'ye user ka aadhaar card 4921-9988-1234 verify kar do')."),
                 ("KAVACH Novelty", "Combines multilingual regex heuristics with Shannon entropy to detect bare Indian identifiers across English, Hindi transliteration, and Hinglish comments.")
             ], title_color=GOLD_ACCENT)

    add_card(s13, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Zero-Knowledge Pseudonymization & Local Rehydration", [
                 ("Step 1: Pre-Execution Detection", "Deterministic scanner identifies statutory Indian identifiers (12-digit Aadhaar, 10-char PAN) and cloud tokens (AWS AKIA, GitHub PAT)."),
                 ("Step 2: In-Memory Vault Isolation", "Sensitive values are extracted and stored exclusively inside an encrypted in-memory session vault on the local workstation."),
                 ("Step 3: Reversible Pseudonymization", "Raw values in prompt are replaced with opaque surrogates: '<REDACTED_AADHAAR_001>', '<REDACTED_AWS_KEY_001>'."),
                 ("Step 4: Cloud Reasoning over Surrogates", "The external cloud LLM (Gemini 2.5 Flash) receives ONLY the pseudonymized prompt. It generates the required code logic with zero access to raw PII."),
                 ("Step 5: Local Workstation Rehydration", "Upon receiving generated patch, local KAVACH runtime re-substitutes the original identifiers from the local vault before saving to disk.")
             ], title_color=CYAN_ACCENT)

    add_speaker_notes(s13,
        "Slide 13 details our Multilingual Zero-Knowledge Token Vault designed for Indian DPDP Act 2023 compliance. "
        "Standard tools like Microsoft Presidio fail on code-mixed Hinglish text. KAVACH detects Indian Aadhaar and PAN numbers, replaces them with opaque placeholders, "
        "sends sanitized prompts to Gemini, and rehydrates original values locally. Cloud logs never see raw PII.")

    # =========================================================================
    # SLIDE 14: TECHNICAL DEEP-DIVE 3 — AST-AWARE CODE CHUNKING & AGENTIC RAG
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Technical Deep-Dive 3: AST-Aware Code Chunking & Agentic RAG", "Code Intelligence: Qdrant Vector Retrieval", 14)

    add_card(s14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "AST Syntactic Chunking vs. Naive Line Slicing", [
                 ("The Naive Chunking Flaw", "Standard RAG chunkers slice code into arbitrary 500-token windows. This shatters Python class boundaries, splits methods from decorators, and disconnects function signatures from docstrings."),
                 ("AST Syntactic Ingestion", "KAVACH traverses the repository using Python's 'ast' module, creating chunks aligned strictly to FunctionDef, AsyncFunctionDef, and ClassDef nodes."),
                 ("Contextual Metadata Injection", "Each chunk preserves file path, start line, end line, parent class, and referenced import symbols."),
                 ("In-Flight Credential Scrubbing", "Before vector embeddings are generated, chunks are scanned by the Shannon entropy engine to prevent indexing sensitive API keys into vector database storage.")
             ], title_color=CYAN_ACCENT)

    add_card(s14, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Qdrant Dense Vector Embeddings & Agentic Dynamic Retrieval", [
                 ("Vector Space Architecture", "Embeds code chunks using 'sentence-transformers/all-MiniLM-L6-v2' into a 384-dimensional dense vector space stored in Qdrant."),
                 ("Agentic Dynamic Retrieval", "Unlike static RAG, the KAVACH orchestrator first analyzes developer intent to decide IF codebase retrieval is required, avoiding redundant database lookups for generic coding questions."),
                 ("Cosine Similarity Scoring", "Computes cosine distance; chunks with similarity score >= 0.70 are retrieved and injected into the LLM evidence buffer."),
                 ("Sub-45ms Retrieval Latency", "Retrieval executes in under 45 milliseconds over indexed repositories, ensuring fast, evidence-grounded patch generation.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s14,
        "Slide 14 explains our Agentic RAG implementation. Rather than blind line-window chunking which shatters syntax, "
        "KAVACH uses AST-aware chunking preserving function and class boundaries. Chunks are scrubbed for secrets and indexed into Qdrant vector storage. "
        "The agent dynamically decides if codebase context is needed, retrieving grounded evidence in under 45 milliseconds.")

    # =========================================================================
    # SLIDE 15: TECHNICAL DEEP-DIVE 4 — AST BLAST RADIUS & CHANGE IMPACT
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Technical Deep-Dive 4: Static AST Blast Radius & Change-Impact Engine", "Code Intelligence: Abstract Syntax Tree Dependency Analysis", 15)

    add_card(s15, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Necessity of Blast-Radius Quantification", [
                 ("The Unbounded Patch Problem", "Autonomous agents frequently refactor a utility function without realizing it is imported by authentication, billing, or database modules, breaking production services."),
                 ("AST Symbol Extraction", "KAVACH's 'analyzer.py' inspects repository files to extract all 'Import', 'ImportFrom', 'FunctionDef', 'ClassDef', and 'Call' AST nodes."),
                 ("Bidirectional Call Graph", "Constructs a directed graph G = (V, E) mapping caller-to-callee and callee-to-caller dependencies across all Python files."),
                 ("Transitive Reachability Matrix", "Computes reachability matrix R = (I | A)^k over adjacency matrix A, tracing cascading impacts up to k hops across the entire repository.")
             ], title_color=CYAN_ACCENT)

    add_card(s15, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Blast-Radius Metric & Agent Context Injection", [
                 ("Mathematical Formulation", "Blast Radius % = (Count of Transitive Dependent Files / Total Repo Files) * 100%."),
                 ("Risk Threshold Classification", "Blast Radius < 15%: LOW impact (automatic patch); 15% - 40%: MEDIUM impact (flagged); > 40%: HIGH impact (escalates to NEEDS_REVIEW)."),
                 ("Prompt Grounding", "The list of affected dependent files and caller functions is injected directly into the LLM prompt context: 'Warning: Modifying auth.py affects api.py and billing.py. Preserve signature compatibility.'"),
                 ("Empirical Accuracy", "100% accuracy on caller-callee regression boundaries validated across our 5 standardized impact test cases.")
             ], title_color=GOLD_ACCENT)

    add_speaker_notes(s15,
        "Slide 15 covers AST Blast Radius and Change Impact Analysis. By constructing bidirectional caller-callee graphs and calculating matrix reachability, "
        "KAVACH calculates the percentage of the repository affected before a single line of code is written. "
        "If blast radius exceeds 40%, the system flags high regression risk and alerts the developer.")

    # =========================================================================
    # SLIDE 16: TECHNICAL DEEP-DIVE 5 — AST SUPPLY-CHAIN FIREWALL & SLOPSQUATTING
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Supply-Chain Defense: AST Package Firewall & Slopsquatting Interception", "Technical Deep-Dive: Supply-Chain Package Firewall", 16)

    add_card(s16, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Slopsquatting Threat Vector & Execution Flow", [
                 ("Attack Vector Defined", "Generative LLMs frequently hallucinate non-existent package names when writing code (e.g. 'import fastapi_jwt_vault'). Attackers monitor these hallucinations, register them on PyPI, and insert malicious install scripts."),
                 ("Step 1: AST Extraction", "Candidate code is parsed via Python's 'ast.parse()'. An 'ImportVisitor' traverses the AST to extract all 'Import' and 'ImportFrom' module root names."),
                 ("Step 2: Tier-1 STDLIB Filtering", "Module names are matched against Python's built-in standard library ('sys.stdlib_module_names'). If matched -> Instant ALLOW (<0.1ms)."),
                 ("Step 3: Tier-2 Local Module Check", "Checks if the import refers to an internal project file or directory. If local -> Instant ALLOW (<0.5ms)."),
                 ("Step 4: Tier-3 LRU Cache & PyPI Registry", "Checks an in-memory LRU Cache (1024 entries). On miss, queries official PyPI JSON endpoint: 'https://pypi.org/pypi/{pkg}/json' (<5ms)."),
                 ("Step 5: Immediate Slopsquat Quarantine", "If PyPI returns HTTP 404 -> Package is hallucinated! Pipeline halts immediately with verdict BLOCKED.")
             ], title_color=CYAN_ACCENT)

    add_card(s16, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Empirical Verification & Production Advantages", [
                 ("Empirical Performance", "Benchmarked against 100 packages (50 legitimate popular PyPI packages + 50 documented LLM hallucinations)."),
                 ("Catch Rate Rigor", "Achieved 100.0% Precision, 100.0% Recall, and 100.0% F1-Score with exactly 0 false negatives."),
                 ("Latency Optimization", "In-memory LRU cache resolves 84% of common dependencies in <0.05ms; external PyPI queries average 4.8ms."),
                 ("Enterprise Advantage vs Snyk/Dependabot", "Traditional SCA scanners only check static requirements.txt files post-commit. KAVACH intercepts dynamically synthesized imports in agent memory BEFORE code touches the disk or virtual environment.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s16,
        "Slide 16 details our AST Package Firewall. When models hallucinate imports, attackers register them on PyPI for slopsquatting attacks. "
        "KAVACH inspects candidate code AST, extracts all imports, checks Python stdlib and local modules, and verifies external packages against live PyPI JSON endpoints in under 5 milliseconds. "
        "If PyPI returns 404, the pipeline halts immediately. We scored 100% precision and recall on our 100-package hallucination corpus.")

    # =========================================================================
    # SLIDE 17: TECHNICAL DEEP-DIVE 6 — CLOSED-LOOP REACT SELF-HEALING SANDBOX
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "Autonomous Recovery: Closed-Loop ReAct Self-Healing Sandbox", "Technical Deep-Dive: Self-Healing Sandbox & ReAct Reflection", 17)

    add_card(s17, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Self-Healing Sandbox Architecture", [
                 ("The Failure Mode", "Generative LLMs frequently synthesize code that compiles syntactically but fails runtime unit assertions due to off-by-one errors, missing imports, or type mismatches."),
                 ("Step 1: Ephemeral Sandbox Provisioning", "Candidate code and generated unit tests are written to an isolated, ephemeral temporary directory with a clean Python virtual environment structure."),
                 ("Step 2: Subprocess Execution with Hard Limits", "Executes 'pytest' inside sandbox with strict resource limits: CPU timeout = 3.0 seconds, stripped environment variables (blocking credential inheritance), and disabled network access."),
                 ("Step 3: Stderr & Traceback Capture", "If exit code != 0, KAVACH captures the exact traceback, failing assertion line, and runtime exception."),
                 ("Step 4: ReAct Reflection Formulation", "Constructs a structured reflection prompt: Prompt_(k+1) = Prompt_k + Traceback_k. Instructs LLM: 'Analyze the assertion failure in 2 sentences and output corrected patch.'"),
                 ("Step 5: Iteration Cap & Convergence", "Repeats repair cycle up to N = 3 iterations. If iteration 3 fails, escalates trace to human gatekeeper via NEEDS_REVIEW state.")
             ], title_color=CYAN_ACCENT)

    add_card(s17, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Empirical Self-Healing Results & Safety Guarantees", [
                 ("Autonomous Recovery Rate", "Achieved 90.0% autonomous test recovery rate across 42 evaluated workflow runs."),
                 ("Cycle Convergence", "78% of runtime failures repaired on Cycle 1 (e.g., injecting missing 'import math' or fixing NameError); 12% repaired on Cycle 2."),
                 ("Infinite Loop Immunity", "Enforcing a hard mathematical upper bound of N = 3 cycles eliminates non-convergent token-burning oscillations."),
                 ("Security Hardening", "Subprocess runs with 'shell=False' and sanitized environment variables, preventing generated code from executing fork-bombs or reverse shells."),
                 ("Cryptographic Audit Provenance", "All execution iterations, test stdout/stderr, and patch diffs are written to CycloneDX v1.5 JSON SBOM meeting SLSA Level 3.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s17,
        "Slide 17 covers our Closed-Loop ReAct Self-Healing Sandbox. When candidate code fails unit assertions, "
        "KAVACH captures the stderr traceback inside an isolated ephemeral subprocess (3.0s timeout) and reflects it back to the repair engine. "
        "With a strict upper bound of 3 iterations, KAVACH achieves a 90% autonomous recovery rate, eliminating infinite loops and debugging token exhaustion.")

    # =========================================================================
    # SLIDE 18: TECHNICAL DEEP-DIVE 7 — DUAL-ENGINE LLM ROUTER & AIR-GAPPED PRIVACY
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, "Dual-Engine LLM Router: Cloud Inference vs. Air-Gapped Local Ollama", "Inference Architecture: Privacy-Preserving AI Routing", 18)

    add_card(s18, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Air-Gapped Privacy Routing Architecture", [
                 ("The Enterprise Dilemma", "Commercial cloud LLMs (Gemini, Claude) offer high reasoning capability but require transmitting code over the public internet, violating strict corporate intellectual property (IP) policies."),
                 ("Sensitivity Classifier", "KAVACH's orchestrator analyzes incoming developer prompts and indexed file paths for proprietary signatures (e.g. database schemas, proprietary algorithms, internal tokens)."),
                 ("Public / Cloud Route", "Sanitized, public requests are dispatched via high-speed API to Google Gemini 2.5 Flash or Groq Cloud (`llama-3.3-70b-versatile`)."),
                 ("Air-Gapped Local Route", "Confidential enterprise code is automatically routed to local Ollama runtime (`localhost:11434`) running `qwen2.5-coder:7b` or `llama3.2`, ensuring zero external network egress.")
             ], title_color=CYAN_ACCENT)

    add_card(s18, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Zero-Failure Deterministic Synthesizer & Cost Optimization", [
                 ("Zero-Failure Fallback Engine", "If both external cloud APIs and local Ollama daemons are offline, KAVACH engages its built-in deterministic synthesizer, ensuring uninterrupted CI/CD operation."),
                 ("Inference Cost Optimization", "By routing repetitive or local tasks to Ollama and using Gemini 2.5 Flash for complex reasoning, average execution cost is kept below $0.0005 USD per run."),
                 ("Universal Multi-Provider Abstraction", "Unified `llm_client.py` interface abstracts Gemini, Groq, Ollama, and Fallback behind a standard polymorphic API."),
                 ("Air-Gapped Deployment Ready", "Entire KAVACH platform can run completely disconnected from the public internet in defense and financial environments.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s18,
        "Slide 18 details our Dual-Engine LLM Router. Confidential intellectual property is routed to a local, air-gapped Ollama instance running Qwen2.5-Coder on localhost, "
        "while sanitized public tasks are routed to Google Gemini 2.5 Flash. If completely offline, a deterministic synthesizer guarantees zero-failure delivery.")

    # =========================================================================
    # SLIDE 19: TECHNICAL DEEP-DIVE 8 — MODEL CONTEXT PROTOCOL (MCP) INTEGRATION
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, "Interoperability: Anthropic Model Context Protocol (MCP) Server", "Tool Interoperability: Open Protocol Architecture", 19)

    add_card(s19, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "The Model Context Protocol (MCP) Standard", [
                 ("The Proprietary Silo Problem", "Security tools fail when they force developers to leave their daily IDE to copy-paste code into clunky third-party web portals."),
                 ("Open Protocol Adoption", "KAVACH implements Anthropic's open Model Context Protocol (Protocol Version 2024-11-05), exposing its governance engine as standardized JSON-RPC 2.0 tools."),
                 ("Native IDE Support", "Connects natively into Cursor IDE, Claude Desktop, and VS Code MCP clients via standard `stdio` or SSE transports."),
                 ("Direct In-Editor Governance", "Developers get instant security checks, blast-radius graphs, and PyPI verification directly inside their Cursor AI chat window without switching context.")
             ], title_color=PURPLE_ACCENT)

    add_card(s19, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Exposed MCP Tool Suite & JSON-RPC Schemas", [
                 ("Tool 1: inspect_code_security", "Scans code for Shannon entropy secrets, PII, and destructive patterns; returns structured verdict (ALLOW/REVIEW/BLOCK)."),
                 ("Tool 2: calculate_blast_radius", "Computes AST call graph and returns affected downstream files and regression percentages."),
                 ("Tool 3: verify_package_imports", "Extracts AST imports and queries PyPI live registry to flag package hallucinations and slopsquats."),
                 ("Tool 4: query_code_rag", "Queries Qdrant vector database for AST-aware code chunks matching natural language intent."),
                 ("Seamless Enterprise Extensibility", "Any external AI agent or CI workflow can invoke KAVACH tools over standardized JSON-RPC.")
             ], title_color=CYAN_ACCENT)

    add_speaker_notes(s19,
        "Slide 19 highlights our Model Context Protocol (MCP) server. By adopting Anthropic's open standard, KAVACH exposes its security tools over JSON-RPC 2.0. "
        "Developers using Cursor IDE or Claude Desktop can inspect code security, calculate blast radius, and check PyPI package validity directly inside their editor.")

    # =========================================================================
    # SLIDE 20: MISSION CONTROL DASHBOARD & MULTIMODAL TELEMETRY
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20)
    add_header(s20, "Mission Control Dashboard & Multimodal Voice Observability", "Frontend Architecture & Telemetry Telemetry", 20)

    add_card(s20, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Dark-Mode SaaS Observability System", [
                 ("Design Aesthetics", "Built with Datadog/Grafana cyber-observability aesthetics: `#08090D` canvas, `#12151D` glass cards, and `#00D2FF` electric cyan accents."),
                 ("Real-Time Telemetry Counters", "Animated cubic counters tracking live operational metrics: total runs, reviews held, and security blocks enforced."),
                 ("Visual Execution Stage Graph", "Dynamic multi-stage node graph visualizing transitions across Planning, Security, Context Retrieval, Impact, and Sandbox."),
                 ("Interactive Code Review Surface", "Dedicated `/review` tab allowing ad-hoc security scanning of arbitrary code snippets with instant AST feedback."),
                 ("GitHub Repository Ingestion", "One-click cloning and AST indexing of any public GitHub repository directly into Qdrant vector storage.")
             ], title_color=CYAN_ACCENT)

    add_card(s20, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Multimodal Speech-to-Text via Groq Whisper v3", [
                 ("Voice-Driven DevOps", "Developers can dictate complex engineering instructions hands-free: 'Refactor database connection pool and check for credential leaks.'"),
                 ("Dual-Engine Audio Pipeline", "Captures audio via browser `MediaRecorder`, dispatches to Groq Cloud `whisper-large-v3-turbo` multipart endpoint for near-instant transcription (<800ms)."),
                 ("Graceful Offline Fallback", "Automatically falls back to browser Web Speech API if cloud network is unavailable."),
                 ("Live SSE Telemetry Streaming", "Server-Sent Events stream step-by-step agent execution logs and reasoning traces directly to the dashboard terminal.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s20,
        "Slide 20 showcases our Mission Control Dashboard and Multimodal Voice capabilities. "
        "The dark-mode dashboard provides real-time telemetry, stage progression graphs, and standalone live code review. "
        "Our voice engine uses Groq Whisper v3 for sub-800ms speech transcription with graceful Web Speech API fallback.")

    # =========================================================================
    # SLIDE 21: EMPIRICAL EVALUATION & 4 BENCHMARK DATASETS
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21)
    add_header(s21, "Empirical Evaluation: 4 Benchmark Datasets & Quantitative Findings", "Rubric 4: Proposed Methodology & Empirical Evaluation (5 Marks)", 21)

    bmarks = [
        ("Benchmark 1: Package Hallucination Corpus", CYAN_ACCENT, [
            ("Dataset Composition", "100 Python packages (50 legitimate popular PyPI packages + 50 documented LLM hallucinations/slopsquats)"),
            ("Precision", "100.0% (Zero false positives on real packages)"),
            ("Recall", "100.0% (Zero false negatives; 100% of hallucinations caught)"),
            ("F1-Score", "1.000 across all package evaluation runs")
        ]),
        ("Benchmark 2: Multilingual PII & Secret Corpus", GOLD_ACCENT, [
            ("Dataset Composition", "100 developer chat prompts containing code-mixed Hinglish, Indian Aadhaar/PAN, and AWS keys"),
            ("Indian PII F1-Score", "0.990 (Outperforms Microsoft Presidio baseline by 139%)"),
            ("Secret Interception", "100.0% catch rate on AWS AKIA, GitHub PAT, Stripe tokens"),
            ("Latency Overhead", "Security scanner execution time < 2.0 ms")
        ]),
        ("Benchmark 3: Operational 42-Run Benchmark", GREEN_ACCENT, [
            ("Dataset Composition", "42 persistent full-lifecycle execution runs across 4 developer personas logged in workflow_runs.json"),
            ("Average Pipeline Latency", "1,370 milliseconds total end-to-end execution time"),
            ("Security Tax / Overhead", "18.4 ms (<2% of total pipeline latency)"),
            ("LLM-as-a-Judge Score", "Average 4.90 / 5.0 quality rating across generated patches")
        ]),
        ("Benchmark 4: Software Engineering Test Rigor", PURPLE_ACCENT, [
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

        add_card(s21, left, top, Inches(5.7), Inches(2.55), b_title, b_items, title_color=b_col)

    add_speaker_notes(s21,
        "Slide 21 presents our quantitative empirical benchmarks across four specialized corpora: "
        "100% precision and recall on our 100-package hallucination corpus; 0.990 F1 on multilingual Hinglish PII; "
        "average latency of 1,370 ms with security overhead under 20 ms in our 42-run operational benchmark; "
        "and 220 automated unit and integration tests passing with 100% CI coverage.")

    # =========================================================================
    # SLIDE 22: VIVA DEFENSE MASTER GUIDE — TOP EXAMINER QUESTIONS & DEFENSE
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22)
    add_header(s22, "Viva Defense Master Guide: Top 4 Examiner Questions & Proofs", "Rubric Alignment: Comprehensive Defense Preparation", 22)

    viva_qas = [
        ("Q1: Why not rely on system prompt engineering for security?",
         "Defense: System prompts offer stochastic, probabilistic safety easily bypassed by direct jailbreaks and indirect prompt injections in repository code comments. In enterprise DevSecOps, safety must be deterministic. KAVACH intercepts threats BEFORE tokenization using compiled regex automata, Shannon entropy, and AST parsers.", CYAN_ACCENT),
        ("Q2: How does KAVACH differ from standard RAG pipelines?",
         "Defense: Vanilla RAG is a static one-shot pipeline (query -> embed -> retrieve). KAVACH is Agentic RAG: the agent dynamically determines if retrieval is needed, preserves AST syntax boundaries, scrubs retrieved chunks for credentials, and grounds patches with static blast-radius call graphs.", GREEN_ACCENT),
        ("Q3: How do you defeat package slopsquatting before install?",
         "Defense: Static SCA tools (Snyk/Dependabot) only check lockfiles post-commit. KAVACH's AST Package Firewall inspects Python Import nodes in agent memory, checks local files and stdlib (<0.1ms), and queries live PyPI JSON endpoints (<5ms). Non-existent packages are quarantined before code is written to disk.", GOLD_ACCENT),
        ("Q4: How does your self-healing sandbox avoid infinite loops?",
         "Defense: We enforce a formal finite state machine with a hard mathematical upper bound of N = 3 iterations, strict 3.0s subprocess timeouts, and automatic escalation to a human gatekeeper via NEEDS_REVIEW state upon the 3rd failure.", PURPLE_ACCENT)
    ]

    for idx, (q, ans, col) in enumerate(viva_qas):
        top_pos = Inches(1.5 + idx * 1.35)
        shape = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.22))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL_COLOR
        shape.line.color.rgb = col
        shape.line.width = Pt(1.2)

        tb = s22.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.08), Inches(11.333), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = q + "\n"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = col

        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = ans
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = LIGHT_GRAY

    add_speaker_notes(s22,
        "Slide 22 equips our team for the viva defense with bulletproof answers to the top 4 examiner questions: "
        "why prompt engineering fails for security, how Agentic RAG surpasses static RAG, how our AST firewall halts slopsquatting before install, "
        "and how our ReAct sandbox guarantees infinite loop immunity through bounded mathematical state limits.")

    # =========================================================================
    # SLIDE 23: PRODUCTION ROADMAP & FUTURE EXPANSION (PHASES 2 & 3)
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    set_slide_background(s23)
    add_header(s23, "Production Roadmap & Future Expansion: Phases 2 & 3", "Project Evolution: Next Sprints & Enterprise Horizon", 23)

    add_card(s23, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Phase 2: Immediate Implementation Milestone", [
                 ("GitHub App PR Guardian", "Event-driven GitHub webhook listener analyzing incoming PR diffs in real time; blocks merging if slopsquatted packages or unmasked credentials are found."),
                 ("Production PostgreSQL Persistence", "Migrating from local SQLite to enterprise PostgreSQL with `pgvector` extension for scalable enterprise vector storage."),
                 ("eBPF Kernel Runtime Sandbox", "Deploying Linux eBPF tracepoints (`sys_enter_execve`, `sys_enter_connect`) to intercept rogue network calls and neutralize reverse shells at the OS kernel layer."),
                 ("Active CI/CD Integration", "Pre-built GitHub Actions and GitLab CI reusable workflows enforcing KAVACH security gates on every commit.")
             ], title_color=CYAN_ACCENT)

    add_card(s23, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Phase 3: Enterprise & Research Horizon", [
                 ("Tree-sitter Polyglot AST Engine", "Extending static AST blast-radius and package verification from Python to JavaScript/TypeScript (npm), Go (pkg.go.dev), and Rust (crates.io)."),
                 ("Merkle Tree Cryptographic Audit Ledger", "Immutable binary SHA-256 Merkle tree ledger ensuring tamper-proof non-repudiation and statutory compliance auditing under DPDP Act 2023."),
                 ("SLSA Level 3 SBOM Provenance", "Automated issuance of signed CycloneDX v1.5 Software Bill of Materials tracking code patches, test logs, and dependency provenance."),
                 ("Collaborative Hierarchical Crews", "Full integration of multi-agent crews (Supervisor, Sentinel, Analyst, Coder) via LangGraph and CrewAI.")
             ], title_color=GOLD_ACCENT)

    add_speaker_notes(s23,
        "Slide 23 presents our production roadmap. Phase 2 introduces our GitHub PR Guardian webhook, PostgreSQL persistence, and eBPF kernel security. "
        "Phase 3 scales KAVACH to polyglot codebases via Tree-sitter, Merkle tree cryptographic audit ledgers, and automated SLSA Level 3 SBOM generation.")

    # =========================================================================
    # SLIDE 24: CONCLUSION, ACADEMIC DELIVERABLES & OPEN DEMO
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    set_slide_background(s24)
    add_header(s24, "Conclusion, Academic Deliverables & System Demonstration", "Summary & Acknowledgments", 24)

    add_card(s24, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4),
             "Summary of Research Contributions", [
                 ("Paradigm Shift Validated", "Demonstrated that deterministic pre-execution guardrails and AST verification solve the security and supply-chain vulnerabilities of autonomous coding agents."),
                 ("Zero Security Tax", "Achieved 100% precision and recall on package hallucinations and cloud secrets while adding under 20 milliseconds (<2%) to overall pipeline latency."),
                 ("Statutory Privacy Compliance", "Engineered the first multilingual Zero-Knowledge Token Vault fully compliant with the Indian DPDP Act 2023 for developer environments."),
                 ("Autonomous Self-Repair", "Proved that bounded ReAct reflection loops achieve a 90% autonomous recovery rate on runtime test assertion failures.")
             ], title_color=CYAN_ACCENT)

    add_card(s24, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Academic Deliverables & Live Demonstration", [
                 ("Complete Source Codebase", "Over 3,500 lines of verified Python backend and dark-mode frontend code packaged with Docker."),
                 ("Test Verification Suite", "220 passing automated unit, integration, and security gate tests."),
                 ("Protocols & API Exposure", "18 live FastAPI REST endpoints and Anthropic Model Context Protocol (MCP) tool server."),
                 ("Interactive Demonstration", "Ready to demonstrate live prompt interception, blast-radius analysis, and self-healing patch generation."),
                 ("Special Thanks", "Heartfelt gratitude to our faculty mentors Prof. Anusha Chhabra and Dr. Soharab Hossain Shaikh for their invaluable guidance.")
             ], title_color=GREEN_ACCENT)

    add_speaker_notes(s24,
        "In conclusion, KAVACH proves that enterprises can harness the transformative productivity of autonomous coding agents without sacrificing "
        "supply chain integrity, credential privacy, or regression stability. All 220 automated tests are passing with 100% coverage. "
        "We thank our mentors Prof. Anusha Chhabra and Dr. Soharab Hossain Shaikh, and we are now delighted to conduct our live demonstration and take your questions.")

    # Output Presentation
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "KAVACH_PERFECT_COMPREHENSIVE_MASTER_DECK.pptx")
    prs.save(output_path)
    print(f"SUCCESS: Generated 24-slide Master PowerPoint deck at: {output_path}")
    return output_path

if __name__ == "__main__":
    build_presentation()
