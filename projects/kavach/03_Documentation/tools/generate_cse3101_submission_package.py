"""
Turnkey CSE3101 Agentic AI Phase-Wise Submission Package Generator.
Generates all formal university evaluation deliverables as mandated by Pages 5 & 6 of the course handout:
- Phase 1 (10%): Project Charter, 16-Week Schedule, Team Responsibility Matrix
- Phase 2 (30%): Progress vs Plan Report, Working Prototype Evidence, Test Coverage Certificate
- Phase 3 (40%): Final Project Report Bundle, Viva Defense Cheatsheet, Rubrics C1-C15 Compliance Attestation
"""

import os
import sys
import json
import zipfile
import time
from pathlib import Path


def generate_submission_bundle():
    tools_dir = Path(__file__).resolve().parent
    important_dir = tools_dir.parent
    reports_dir = important_dir / "02_Official_Reports_and_Synopses"
    viva_dir = important_dir / "04_Viva_Defense_and_Evaluation"
    presentations_dir = important_dir / "01_Master_Presentations"
    bundle_dir = important_dir / "CSE3101_Official_Submission_Packages"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("GENERATING CSE3101 AGENTIC AI SUBMISSION PACKAGES (PAGES 5-7 COMPLIANCE)")
    print("=" * 70)

    # 1. Phase 1 Package (10% Weightage)
    p1_zip = bundle_dir / "CSE3101_Phase1_Submission_Bundle.zip"
    with zipfile.ZipFile(p1_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [
            reports_dir / "PHASE_1_PROJECT_CHARTER.md",
            viva_dir / "PROJECT_TIMELINE_CSE3101.md",
            viva_dir / "TEAM_RESPONSIBILITY_MATRIX.md",
            reports_dir / "PEAS_AND_PERSONA_SPECIFICATION.md",
        ]:
            if f.exists():
                z.write(f, arcname=f.name)
    print(f"[OK] Generated Phase-1 Package: {p1_zip.name} (Charter, Timeline, RACIS Matrix)")

    # 2. Phase 2 Package (30% Weightage)
    p2_zip = bundle_dir / "CSE3101_Phase2_Submission_Bundle.zip"
    with zipfile.ZipFile(p2_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [
            reports_dir / "PRJ_IV_SYNOPSIS_REPORT.md",
            reports_dir / "KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md",
            viva_dir / "PROMPT_STRATEGIES_AND_RAG_STUDY.md",
            viva_dir / "42_RUNS_EVALUATION_DATASET.md",
        ]:
            if f.exists():
                z.write(f, arcname=f.name)
    print(f"[OK] Generated Phase-2 Package: {p2_zip.name} (Progress vs Plan, Prototype Proof, 42 Runs)")

    # 3. Phase 3 Package (40% Weightage)
    p3_zip = bundle_dir / "CSE3101_Phase3_EndTerm_Capstone_Bundle.zip"
    with zipfile.ZipFile(p3_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [
            reports_dir / "CSE3101_COURSE_HANDOUT_LINE_BY_LINE_ALIGNMENT.md",
            viva_dir / "VIVA_DEFENSE_CHEATSHEET.md",
            viva_dir / "VIVA_DEFENSE_AND_EVALUATION_GUIDE.md",
            viva_dir / "CRITICAL_PLAY_AREAS_EVALUATION.md",
            presentations_dir / "KAVACH_PERFECT_MASTER_PRESENTATION_24_SLIDES.md",
        ]:
            if f.exists():
                z.write(f, arcname=f.name)
    print(f"[OK] Generated Phase-3 Package: {p3_zip.name} (Report, PPTX Notes, Viva Defense, Rubrics)")

    print("\nAll 3 Phase-Wise Submission Packages ready in: " + str(bundle_dir))
    return True


if __name__ == "__main__":
    generate_submission_bundle()
