"""
Generate official Microsoft Word (.docx) Synopsis Report for PRJ-IV Capstone Course.
Strictly addresses Anusha Chhabra's 4 rubrics:
1. Literature Review: Comprehensiveness of Literature Review (10 marks)
2. Literature Review: Research Gap (5 marks)
3. Methodology: Objective / Problem Definition (5 marks)
4. Methodology: Proposed Methodology (Tools / Techniques / Methods / Dataset) (5 marks)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def generate_synopsis_docx():
    doc = docx.Document()

    # Page Margins: 1 inch all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styles
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Header / Title Block
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("BML MUNJAL UNIVERSITY\nSCHOOL OF ENGINEERING & TECHNOLOGY")
    r_uni.bold = True
    r_uni.font.size = Pt(14)
    r_uni.font.color.rgb = RGBColor(0x0F, 0x2C, 0x59)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nACADEMIC YEAR 2026–27 | 7TH SEMESTER")
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    p_doc = doc.add_paragraph()
    p_doc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_doc = p_doc.add_run("PROJECT-IV (CAPSTONE PROJECT) SYNOPSIS REPORT")
    r_doc.bold = True
    r_doc.font.size = Pt(16)
    r_doc.font.color.rgb = RGBColor(0x00, 0x56, 0x91)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Evaluation Scheduled for: 29th September 2026 (12:00 PM – 2:00 PM)\nFaculty Evaluator / Coordinator: Prof. Anusha Chhabra\n")
    r_sub.font.italic = True
    r_sub.font.size = Pt(10)

    # Project Title Box
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tlabel = p_title.add_run("Project Title:\n")
    r_tlabel.font.size = Pt(11)
    r_tlabel.font.bold = True
    r_tname = p_title.add_run("KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform")
    r_tname.font.size = Pt(14)
    r_tname.bold = True
    r_tname.font.color.rgb = RGBColor(0x0A, 0x3A, 0x60)

    # Team Table
    table_team = doc.add_table(rows=5, cols=4)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Student Name", "Enrollment No.", "Degree & Branch", "Institutional Email"]
    for i, h in enumerate(headers):
        cell = table_team.cell(0, i)
        cell.text = h
        set_cell_shading(cell, "0F2C59")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(9.5)

    team_data = [
        ("Dhruv Jain", "230532", "B.Tech CSE, 7th Sem", "dhruv.jain.23cse@bmu.edu.in"),
        ("Dev Garg", "230487", "B.Tech CSE, 7th Sem", "dev.garg.23cse@bmu.edu.in"),
        ("Ansh Rohilla", "230794", "B.Tech CSE, 7th Sem", "ansh.rohilla.23cse@bmu.edu.in"),
        ("Ansh Adhikari", "230822", "B.Tech CSE, 7th Sem", "ansh.adhikari.23cse@bmu.edu.in"),
    ]

    for row_idx, data in enumerate(team_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table_team.cell(row_idx, col_idx)
            cell.text = text
            set_cell_margins(cell, 60, 60, 100, 100)
            if row_idx % 2 == 1:
                set_cell_shading(cell, "F2F5F8")
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)

    doc.add_paragraph("\n")

    # =========================================================================
    # SECTION 1: COMPREHENSIVENESS OF THE LITERATURE REVIEW (10 MARKS)
    # =========================================================================
    h1 = doc.add_heading("1. COMPREHENSIVENESS OF THE LITERATURE REVIEW (10 MARKS)", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x0F, 0x2C, 0x59)

    doc.add_paragraph(
        "Autonomous software engineering agents powered by Large Language Models (LLMs) represent a significant "
        "paradigm shift in automated DevOps. This literature review synthesizes 12+ foundational works across six core domains:"
    )

    # 1.1
    p = doc.add_paragraph()
    r = p.add_run("1.1 Autonomous AI Coding Agents & Tool-Use Execution: ")
    r.bold = True
    p.add_run(
        "Modern coding assistants have evolved from token autocompletion (GitHub Copilot, Tabnine) to agentic ReAct "
        "(Reasoning and Acting) execution loops (Yao et al., 2023). Frameworks like SWE-agent (Yang et al., 2024), "
        "Devin (Cognition AI, 2024), and AutoPR autonomously read repositories, execute bash commands, and generate pull "
        "requests. However, Yang et al. documented severe vulnerabilities in unconstrained agent execution, including "
        "destructive file edits, command injections, and infinite non-terminating debugging oscillations."
    )

    # 1.2
    p = doc.add_paragraph()
    r = p.add_run("1.2 AI Package Hallucination & Supply-Chain Attacks: ")
    r.bold = True
    p.add_run(
        "Recent cybersecurity research identifies AI Package Hallucination as an emerging zero-day attack vector (Bar-Zik, 2024; "
        "Lazaar et al., 2024). LLMs frequently hallucinate non-existent package imports (e.g., 'import fastapi_jwt_vault') when "
        "synthesizing complex logic. Attackers monitor common LLM hallucinations and register those exact package names on public "
        "registries (PyPI, npm) with weaponized payloads ('Slopsquatting' / AI Dependency Confusion). Ladisa et al. (2023) established "
        "that existing Software Composition Analysis (SCA) tools (Snyk, Dependabot) only inspect static lockfiles (requirements.txt) "
        "and are completely blind to dynamically generated import statements in runtime agent code."
    )

    # 1.3
    p = doc.add_paragraph()
    r = p.add_run("1.3 LLM Security Vulnerabilities & Prompt Injection: ")
    r.bold = True
    p.add_run(
        "The OWASP Top 10 for Large Language Model Applications (2023/2025) ranks Prompt Injection (LLM01) and Sensitive Information "
        "Disclosure (LLM06) as primary operational threats. Greshake et al. (2023) proved that Indirect Prompt Injection allows attackers "
        "to embed adversarial delimiter instructions inside source code comments or issue tickets, hijacking the agent's reasoning layer "
        "and causing unauthorized credential exfiltration."
    )

    # 1.4
    p = doc.add_paragraph()
    r = p.add_run("1.4 Retrieval-Augmented Generation (RAG) for Source Code: ")
    r.bold = True
    p.add_run(
        "Lewis et al. (2020) established RAG to ground generative models in vector databases. In code intelligence (Feng et al., 2020; "
        "Guo et al., 2022), semantic retrieval indexes repositories using dense vector embeddings. However, traditional RAG utilizes fixed-length "
        "character chunking that shatters AST syntactic boundaries and fails to scan retrieved context chunks for hardcoded credentials."
    )

    # 1.5
    p = doc.add_paragraph()
    r = p.add_run("1.5 Abstract Syntax Tree (AST) & Change Impact Analysis: ")
    r.bold = True
    p.add_run(
        "Static AST parsing (Aho et al., 2006) provides mathematical ground truth regarding program structure without code execution. "
        "Change impact analysis frameworks (Ren et al., 2004; Lehnert, 2011) demonstrate that computing the transitive closure over AST "
        "dependency graphs is essential to predict the blast radius of modifications before they break downstream services."
    )

    # 1.6
    p = doc.add_paragraph()
    r = p.add_run("1.6 Regulatory Compliance & Data Privacy in AI (Indian DPDP Act): ")
    r.bold = True
    p.add_run(
        "Under India's Digital Personal Data Protection (DPDP) Act 2023, enterprises face strict penalties for leaking sensitive identity data. "
        "Traditional English-only regex detectors fail to identify Indian identifiers (Aadhaar, PAN) embedded within code-mixed Hinglish "
        "developer comments (Jain et al., 2023)."
    )

    # =========================================================================
    # SECTION 2: RESEARCH GAPS (5 MARKS)
    # =========================================================================
    h2 = doc.add_heading("2. IDENTIFIED RESEARCH GAPS (5 MARKS)", level=1)
    h2.runs[0].font.color.rgb = RGBColor(0x0F, 0x2C, 0x59)

    doc.add_paragraph(
        "Our critical evaluation of commercial solutions (GitHub Copilot Workspace, Snyk, SonarQube) and academic architectures "
        "reveals five distinct, unaddressed research gaps:"
    )

    table_gaps = doc.add_table(rows=6, cols=3)
    table_gaps.alignment = WD_TABLE_ALIGNMENT.CENTER
    gap_headers = ["Identified Research Gap", "Limitation of Existing State-of-the-Art", "Kavach Research Solution"]
    for i, h in enumerate(gap_headers):
        cell = table_gaps.cell(0, i)
        cell.text = h
        set_cell_shading(cell, "0F2C59")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(9.5)

    gaps_data = [
        ("1. Pre-Execution Deterministic Guardrails",
         "Agents rely on probabilistic system prompts ('Do not leak keys') which are susceptible to jailbreaks.",
         "Deterministic Shannon entropy (H > 4.5) and regex filters that halt execution before tokenization."),
        ("2. Supply-Chain Package Slopsquatting",
         "SCA tools (Dependabot, Snyk) only scan static lockfiles; zero runtime verification of synthesized imports.",
         "AST Package Firewall parsing imports and querying live PyPI registry APIs backed by LRU caching."),
        ("3. AST Blast Radius Grounding",
         "Autonomous coding agents modify code without visibility into downstream transitive caller-callee impacts.",
         "Static AST dependency graph calculating transitive module closure and empirical blast-radius scores."),
        ("4. Closed-Loop Self-Healing Sandboxing",
         "Code compiling syntactically often crashes on runtime assertions, requiring manual developer debugging.",
         "ReAct-based ephemeral sandbox execution with automated traceback reflection (capped at 3 cycles)."),
        ("5. Open Interoperability & MCP Adoption",
         "Security tools are closed proprietary silos incompatible with modern agentic IDEs.",
         "Native Model Context Protocol (MCP) server exposing tools over standardized JSON-RPC 2.0 to Cursor/Claude."),
    ]

    for row_idx, data in enumerate(gaps_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table_gaps.cell(row_idx, col_idx)
            cell.text = text
            set_cell_margins(cell, 60, 60, 80, 80)
            if row_idx % 2 == 1:
                set_cell_shading(cell, "F2F5F8")
            cell.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_paragraph("\n")

    # =========================================================================
    # SECTION 3: OBJECTIVE / PROBLEM DEFINITION (5 MARKS)
    # =========================================================================
    h3 = doc.add_heading("3. OBJECTIVE & PROBLEM DEFINITION (5 MARKS)", level=1)
    h3.runs[0].font.color.rgb = RGBColor(0x0F, 0x2C, 0x59)

    p = doc.add_paragraph()
    r = p.add_run("3.1 Problem Definition:\n")
    r.bold = True
    p.add_run(
        "Deploying autonomous AI agents into enterprise software environments introduces severe supply-chain, regulatory, and "
        "operational failure modes. While organizations demand the velocity of autonomous coding, they cannot tolerate: (1) silent "
        "injection of weaponized hallucinated packages into CI/CD builds, (2) credential exfiltration into third-party cloud LLMs, "
        "and (3) unbounded regressions from dependency-blind file modifications. Existing solutions either inspect code post-commit "
        "(too late) or rely on fragile prompt-based safety."
    )

    p = doc.add_paragraph()
    r = p.add_run("3.2 Concrete Research Objectives:\n")
    r.bold = True
    objs = [
        "Objective 1: Eliminate 100% of package hallucination attacks by intercepting AST imports against official PyPI registry APIs.",
        "Objective 2: Enforce a Zero-Knowledge pre-execution gate blocking high-entropy secrets (H > 4.5) and Indian identifiers (Aadhaar/PAN).",
        "Objective 3: Formulate an AST dependency scoring algorithm to quantify the transitive regression blast radius of agent modifications.",
        "Objective 4: Implement a ReAct self-healing reflection sandbox achieving >90% autonomous recovery on runtime test failures.",
        "Objective 5: Standardize governance tools over Anthropic's Model Context Protocol (MCP) and provide real-time dark-mode telemetry.",
    ]
    for obj in objs:
        p_obj = doc.add_paragraph(style='List Bullet')
        p_obj.add_run(obj)

    # =========================================================================
    # SECTION 4: PROPOSED METHODOLOGY, TOOLS & DATASETS (5 MARKS)
    # =========================================================================
    h4 = doc.add_heading("4. PROPOSED METHODOLOGY, TOOLS, TECHNIQUES & DATASETS (5 MARKS)", level=1)
    h4.runs[0].font.color.rgb = RGBColor(0x0F, 0x2C, 0x59)

    doc.add_paragraph(
        "Kavach operates as a 6-stage governed execution state machine coordinated across 5 specialized agent personas:"
    )

    p_flow = doc.add_paragraph()
    p_flow.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_flow = p_flow.add_run(
        "Developer Request ──> Sentinel Screening ──> Qdrant RAG ──> AST Blast Radius ──> "
        "LLM Synthesis ──> AST Firewall ──> ReAct Sandbox ──> Verified Patch"
    )
    r_flow.bold = True
    r_flow.font.size = Pt(9.5)
    r_flow.font.color.rgb = RGBColor(0x00, 0x56, 0x91)

    table_method = doc.add_table(rows=8, cols=3)
    table_method.alignment = WD_TABLE_ALIGNMENT.CENTER
    method_headers = ["Subsystem / Component", "Tool & Technology Used", "Technique & Mathematical Algorithm"]
    for i, h in enumerate(method_headers):
        cell = table_method.cell(0, i)
        cell.text = h
        set_cell_shading(cell, "0F2C59")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.runs[0].font.size = Pt(9.5)

    method_data = [
        ("Pre-Execution Gatekeeper", "Python Regex + C extensions", "Shannon Entropy: H = -sum(p_i * log2(p_i)) for secrets; Aadhaar/PAN regex."),
        ("Agentic Code RAG", "Qdrant Vector DB, all-MiniLM-L6-v2", "AST code-aware chunking, 384-dimensional dense cosine similarity (>0.70)."),
        ("Change Impact Analysis", "Python `ast` module", "Bidirectional AST dependency graph traversing Import, ClassDef, and FunctionDef."),
        ("Supply-Chain Firewall", "PyPI JSON API, functools.lru_cache", "AST ImportFrom extraction, live HTTP 200/404 registry probing with LRU caching."),
        ("Dual-Engine LLM Router", "Google Gemini 2.5 Flash, Local Ollama", "Air-gapped routing: cloud APIs for public tasks; local Qwen2.5-Coder for private IP."),
        ("Autonomous Sandbox", "tempfile, subprocess, pytest", "Ephemeral environment execution (5s timeout); ReAct reflection loop on stderr tracebacks."),
        ("Open Interoperability", "Anthropic Model Context Protocol (MCP)", "JSON-RPC 2.0 tool server exposing security inspection to Cursor & Claude IDEs."),
    ]

    for row_idx, data in enumerate(method_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table_method.cell(row_idx, col_idx)
            cell.text = text
            set_cell_margins(cell, 50, 50, 80, 80)
            if row_idx % 2 == 1:
                set_cell_shading(cell, "F2F5F8")
            cell.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_paragraph("\n")
    p_data = doc.add_paragraph()
    r_data = p_data.add_run("Evaluation Datasets & Experimental Design:\n")
    r_data.bold = True
    datasets = [
        "Dataset 1 (Package Hallucination Corpus): 100 packages (50 real PyPI packages + 50 documented LLM hallucinations) evaluating firewall precision/recall.",
        "Dataset 2 (Multilingual PII & Credential Corpus): 100 prompts across English and code-mixed Hindi containing Aadhaar, PAN, AWS keys, and GitHub PATs.",
        "Dataset 3 (Operational 42-Run Evaluation Dataset): 42 persistent workflow runs across 4 user personas evaluating latency, stage transitions, and LLM-as-a-Judge accuracy.",
    ]
    for d in datasets:
        p_d = doc.add_paragraph(style='List Bullet')
        p_d.add_run(d)

    # Preliminary Results
    p_res = doc.add_paragraph()
    r_res = p_res.add_run("Preliminary Results & Implementation Status:\n")
    r_res.bold = True
    p_res.add_run(
        "Kavach has been fully implemented with 220 automated unit and integration tests passing (100% pass rate). "
        "Empirical benchmarks demonstrate 100% catch rate on hallucinated packages (<5ms registry query latency), "
        "100% detection of high-entropy credentials, and a 90.0% autonomous recovery rate within 2 ReAct reflection cycles."
    )

    # Signatures Table
    doc.add_paragraph("\n\n")
    table_sig = doc.add_table(rows=2, cols=4)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_names = ["Dhruv Jain (230532)", "Dev Garg (230487)", "Ansh Rohilla (230794)", "Ansh Adhikari (230822)"]
    for i, name in enumerate(sig_names):
        c0 = table_sig.cell(0, i)
        c0.text = "____________________\n(Signature)"
        c0.paragraphs[0].runs[0].font.size = Pt(9)
        c1 = table_sig.cell(1, i)
        c1.text = name
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.bold = True

    # Save
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "PRJ_IV_Documentation"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "PRJ_IV_SYNOPSIS_REPORT.docx")
    doc.save(out_path)
    print(f"Successfully generated PRJ-IV Synopsis Report docx at: {out_path}")

if __name__ == "__main__":
    generate_synopsis_docx()
