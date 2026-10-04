#!/usr/bin/env python3
"""
Profitara — End-to-End Pipeline Runner
One-click reproduction script for all models, SQL tables, and tests.
"""

import os
import sys
import subprocess
import time

def run_step(step_name, command):
    print("\n" + "="*80)
    print(f">> STEP: {step_name}")
    print(f"   Command: {command}")
    print("="*80)
    start = time.time()
    res = subprocess.run(command, shell=True)
    duration = time.time() - start
    if res.returncode != 0:
        print(f"\n[FAILED]: {step_name} exited with code {res.returncode}")
        sys.exit(res.returncode)
    print(f"[COMPLETED] in {duration:.1f}s: {step_name}")

def main():
    print("""
    ========================================================
             PROFITARA - RETAIL BI & ML PIPELINE
             Full End-to-End Laptop-Runnable Suite
    ========================================================
    """)

    # 1. Dataset Ingestion (Real UCI Retail)
    run_step("1. Ingest Real Public Retail Dataset", f"{sys.executable} scripts/download_real_data.py")

    # 2. Time-Split Customer Lifetime Value Modeling
    run_step("2. Time-Split CLV Modeling & Baselines", f"{sys.executable} ml_pipeline/clv_engine.py")

    # 3. Churn Decision Engine & Win-Back Optimization
    run_step("3. Churn Modeling & Expected Value Policy", f"{sys.executable} ml_pipeline/churn_decision_engine.py")

    # 4. Customer Segmentation & Market Basket Analysis
    run_step("4. RFM K-Means Segmentation & Apriori", f"{sys.executable} ml_pipeline/segmentation_basket.py")

    # 5. Time-Series Forecasting Rolling-Origin Backtest
    run_step("5. Rolling-Origin Forecasting Backtest", f"{sys.executable} ml_pipeline/forecasting_engine.py")

    # 6. Database Layer & Power BI Clean CSV Export
    run_step("6. DuckDB Analytics Tables Init", f"{sys.executable} sql/init_duckdb.py")
    run_step("7. Export Power BI Clean CSVs", f"{sys.executable} scripts/export_powerbi_data.py")

    # 7. QA Pairs Generation for Retail Analyst Agent
    run_step("8. Generate Agent QA Pairs", f"{sys.executable} scripts/generate_qa_pairs.py")

    # 8. Test Suite Verification
    run_step("9. Execute Pytest Quality Suite", f"{sys.executable} -m pytest tests/ -v")

    print("""
    ========================================================
    ALL PIPELINE MODULES COMPLETED SUCCESSFULLY!
    
    To view the 13-page interactive Streamlit dashboard:
      streamlit run dashboard/app.py
    
    To evaluate the Retail Analyst Agent:
      1. Open QA_PAIRS_TO_REVIEW.csv
      2. Mark pairs as 'correct' or 'incorrect'
      3. Run: python agent/evaluate_agent.py
    ========================================================
    """)

if __name__ == "__main__":
    main()
