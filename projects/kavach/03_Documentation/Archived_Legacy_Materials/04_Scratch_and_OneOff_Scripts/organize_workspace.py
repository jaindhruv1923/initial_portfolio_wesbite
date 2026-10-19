import os
import shutil
import sys
from pathlib import Path

ROOT = Path(r"c:\Users\jaind\Videos\PRJ-IV Work")

def safe_copy(src, dst):
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        print(f"SKIP (not found): {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)
    print(f"COPIED: {src.name} -> {dst}")

def safe_move(src, dst):
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        print(f"SKIP (not found): {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    print(f"MOVED: {src.name} -> {dst}")

def run():
    print("=== STARTING WORKSPACE REORGANIZATION ===")
    
    important = ROOT / "important"
    unimportant = ROOT / "unimportant"
    
    # -------------------------------------------------------------
    # 1. SETUP IMPORTANT FOLDERS
    # -------------------------------------------------------------
    imp_pres = important / "01_Master_Presentations"
    imp_reports = important / "02_Official_Reports_and_Synopses"
    imp_arch = important / "03_Architecture_and_Flowcharts"
    imp_viva = important / "04_Viva_Defense_and_Evaluation"
    imp_ieee = important / "05_IEEE_Research_Publication"
    imp_kavach = important / "kavach"
    
    for d in [imp_pres, imp_reports, imp_arch, imp_viva, imp_ieee, imp_kavach]:
        d.mkdir(parents=True, exist_ok=True)

    # 1a. Copy Master Presentations
    safe_copy(ROOT / "KAVACH_PERFECT_COMPREHENSIVE_MASTER_DECK.pptx", imp_pres / "KAVACH_PERFECT_COMPREHENSIVE_MASTER_DECK.pptx")
    safe_copy(ROOT / "KAVACH_Interactive_Presentation.html", imp_pres / "KAVACH_Interactive_Presentation.html")
    safe_copy(ROOT / "KAVACH_PERFECT_MASTER_PRESENTATION_24_SLIDES.md", imp_pres / "KAVACH_PERFECT_MASTER_PRESENTATION_24_SLIDES.md")
    safe_copy(ROOT / "pptmaker docs" / "build_perfect_master_presentation.py", imp_pres / "build_perfect_master_presentation.py")

    # 1b. Copy Official Reports & Synopses
    safe_copy(ROOT / "KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md", imp_reports / "KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md")
    safe_copy(ROOT / "PRJ_IV_Documentation" / "mid_sem" / "KAVACH_MidTerm_Synopsis_Report.docx", imp_reports / "KAVACH_MidTerm_Synopsis_Report.docx")
    safe_copy(ROOT / "PRJ_IV_Documentation" / "extras" / "PRJ_IV_SYNOPSIS_REPORT.docx", imp_reports / "PRJ_IV_SYNOPSIS_REPORT.docx")
    safe_copy(ROOT / "PRJ_IV_Documentation" / "extras" / "PRJ_IV_SYNOPSIS_REPORT.md", imp_reports / "PRJ_IV_SYNOPSIS_REPORT.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "PHASE_1_PROJECT_CHARTER.md", imp_reports / "PHASE_1_PROJECT_CHARTER.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "PEAS_AND_PERSONA_SPECIFICATION.md", imp_reports / "PEAS_AND_PERSONA_SPECIFICATION.md")
    safe_copy(ROOT / "docs" / "reference" / "KAVACH_Limitations_and_Part2_Improvement_Blueprint.pdf", imp_reports / "KAVACH_Limitations_and_Part2_Improvement_Blueprint.pdf")

    # 1c. Copy Flowcharts and Architecture
    flowchart_src = ROOT / "pptmaker docs" / "02_Flowcharts_and_Mermaid"
    if flowchart_src.exists():
        for item in flowchart_src.iterdir():
            safe_copy(item, imp_arch / item.name)
    safe_copy(ROOT / "pptmaker docs" / "00_PRIMARY_FLOWCHARTS_AND_EXPLANATION.md", imp_arch / "FLOWCHARTS_AND_EXPLANATION.md")

    # 1d. Copy Viva Defense & Evaluation
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "VIVA_DEFENSE_AND_EVALUATION_GUIDE.md", imp_viva / "VIVA_DEFENSE_AND_EVALUATION_GUIDE.md")
    safe_copy(ROOT / "mid-sem-rough-work" / "VIVA_DEFENSE_CHEATSHEET.md", imp_viva / "VIVA_DEFENSE_CHEATSHEET.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "42_RUNS_EVALUATION_DATASET.md", imp_viva / "42_RUNS_EVALUATION_DATASET.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "CRITICAL_PLAY_AREAS_EVALUATION.md", imp_viva / "CRITICAL_PLAY_AREAS_EVALUATION.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "TEAM_RESPONSIBILITY_MATRIX.md", imp_viva / "TEAM_RESPONSIBILITY_MATRIX.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "PROJECT_TIMELINE_CSE3101.md", imp_viva / "PROJECT_TIMELINE_CSE3101.md")
    safe_copy(ROOT / "Agentic_AI_Documentation" / "midsem" / "extras" / "PROMPT_STRATEGIES_AND_RAG_STUDY.md", imp_viva / "PROMPT_STRATEGIES_AND_RAG_STUDY.md")

    # 1e. Copy Research & IEEE
    safe_copy(ROOT / "research" / "ieee_publication", imp_ieee)

    # 1f. Move/Copy kavach core platform into important/kavach
    safe_move(ROOT / "kavach", imp_kavach)

    # 1g. Copy Launchers into important
    safe_copy(ROOT / "run_kavach.bat", important / "run_kavach.bat")
    safe_copy(ROOT / "run_kavach.ps1", important / "run_kavach.ps1")
    safe_copy(ROOT / "Dockerfile", important / "Dockerfile")
    safe_copy(ROOT / "render.yaml", important / "render.yaml")
    safe_copy(ROOT / "pytest.ini", important / "pytest.ini")

    # -------------------------------------------------------------
    # 2. SETUP UNIMPORTANT FOLDERS
    # -------------------------------------------------------------
    unimp_archive = unimportant / "01_Archived_Legacy_Phases"
    unimp_rough = unimportant / "02_MidSem_Rough_Work"
    unimp_old_docs = unimportant / "03_Older_Documentation_Dumps"
    unimp_scripts = unimportant / "04_Scratch_and_OneOff_Scripts"
    unimp_demos = unimportant / "05_Old_Demo_Prototypes"

    for d in [unimp_archive, unimp_rough, unimp_old_docs, unimp_scripts, unimp_demos]:
        d.mkdir(parents=True, exist_ok=True)

    # 2a. Move archive & rough work
    safe_move(ROOT / "archive", unimp_archive / "archive")
    safe_move(ROOT / "mid-sem-rough-work", unimp_rough / "mid-sem-rough-work")
    safe_move(ROOT / "scratch", unimp_scripts / "scratch")
    safe_move(ROOT / "repo_scanner_demo", unimp_demos / "repo_scanner_demo")
    safe_move(ROOT / "research", unimp_old_docs / "research_raw")

    # 2b. Move older documentation folders
    safe_move(ROOT / "Agentic_AI_Documentation", unimp_old_docs / "Agentic_AI_Documentation")
    safe_move(ROOT / "PRJ_IV_Documentation", unimp_old_docs / "PRJ_IV_Documentation")
    safe_move(ROOT / "docs", unimp_old_docs / "docs")
    safe_move(ROOT / "pptmaker docs", unimp_old_docs / "pptmaker_docs")

    # 2c. Move one-off test scripts at root
    for f in ["test_verify_frontend.py", "test_verify_motion_design.py", "test_verify_terminal_results.py", "security_gate_report.json"]:
        safe_move(ROOT / f, unimp_scripts / f)

    # Clean __pycache__ if exists at root
    if (ROOT / "__pycache__").exists():
        shutil.rmtree(ROOT / "__pycache__", ignore_errors=True)

    print("=== REORGANIZATION COMPLETE ===")

if __name__ == "__main__":
    run()
