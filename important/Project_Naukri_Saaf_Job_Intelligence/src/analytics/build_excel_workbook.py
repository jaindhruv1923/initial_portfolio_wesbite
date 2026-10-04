"""
Executive Financial & Risk Excel Workbook Builder (openpyxl)
=============================================================
Builds `04_Excel_Workbook/Naukri_Saaf_Executive_Analytics_v4.xlsx`
containing multi-tab executive KPI dashboards, portal risk pivots,
survival half-life metrics, and scored listing registers.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

def create_executive_workbook():
    print("=" * 80)
    print("  BUILDING NAUKRI SAAF EXECUTIVE ANALYTICS WORKBOOK (v4)")
    print("=" * 80)
    
    pred_path = "data/predictions_v4.csv"
    age_path = "data/listing_age_distribution.csv"
    
    df_pred = pd.read_csv(pred_path)
    df_age = pd.read_csv(age_path) if os.path.exists(age_path) else pd.DataFrame()
    
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default sheet
    
    # Styles
    navy_fill = PatternFill(start_color="1E1830", end_color="1E1830", fill_type="solid")
    purple_fill = PatternFill(start_color="4C1D95", end_color="4C1D95", fill_type="solid")
    gold_fill = PatternFill(start_color="B8860B", end_color="B8860B", fill_type="solid")
    light_purple = PatternFill(start_color="EDE9FE", end_color="EDE9FE", fill_type="solid")
    card_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    
    title_font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True)
    regular_font = Font(name="Calibri", size=11)
    kpi_num_font = Font(name="Calibri", size=20, bold=True, color="4C1D95")
    kpi_lbl_font = Font(name="Calibri", size=9, bold=True, color="6B7280")
    
    thin_border = Border(
        left=Side(style="thin", color="D1D5DB"),
        right=Side(style="thin", color="D1D5DB"),
        top=Side(style="thin", color="D1D5DB"),
        bottom=Side(style="thin", color="D1D5DB")
    )
    
    # -------------------------------------------------------------
    # SHEET 1: Executive KPI Dashboard
    # -------------------------------------------------------------
    ws1 = wb.create_sheet(title="Executive Summary")
    ws1.views.sheetView[0].showGridLines = True
    
    # Header Banner
    ws1.merge_cells("A1:G2")
    ws1["A1"] = "NAUKRI SAAF — EXECUTIVE RISK INTELLIGENCE DASHBOARD"
    ws1["A1"].font = title_font
    ws1["A1"].fill = navy_fill
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    # KPI Cards Row
    kpis = [
        ("Total Analyzed", len(df_pred), "#,##0"),
        ("Confirmed Ghosts", int((df_pred["ghost_status"] == "Ghost").sum()), "#,##0"),
        ("Ghost Rate %", float((df_pred["ghost_status"] == "Ghost").mean()), "0.0%"),
        ("At-Risk Share %", float((df_pred["ghost_status"].isin(["Ghost", "Suspect"])).mean()), "0.0%"),
        ("Overall Mean Age", float(df_pred["days_live"].mean()), "0.0 days"),
        ("Salary Opacity %", float(df_pred["salary_max"].isna().mean()), "0.0%"),
    ]
    
    col_starts = ["A", "B", "C", "D", "E", "F"]
    for idx, (label, val, fmt) in enumerate(kpis):
        col = col_starts[idx]
        ws1[f"{col}4"] = label.upper()
        ws1[f"{col}4"].font = kpi_lbl_font
        ws1[f"{col}4"].alignment = Alignment(horizontal="center", vertical="center")
        ws1[f"{col}4"].fill = light_purple
        ws1[f"{col}4"].border = thin_border
        
        ws1[f"{col}5"] = val
        ws1[f"{col}5"].font = kpi_num_font
        ws1[f"{col}5"].alignment = Alignment(horizontal="center", vertical="center")
        ws1[f"{col}5"].fill = card_fill
        ws1[f"{col}5"].border = thin_border
        if "%" in fmt:
            ws1[f"{col}5"].number_format = fmt
        elif "#" in fmt:
            ws1[f"{col}5"].number_format = fmt
            
    # Risk Distribution Table
    ws1["A8"] = "GHOST RISK STRATIFICATION (PLATT CALIBRATED)"
    ws1["A8"].font = bold_font
    
    strat_headers = ["Risk Tier", "Probability Range", "Listing Count", "Share of Total (%)", "Avg Days Live"]
    for j, h in enumerate(strat_headers, start=1):
        cell = ws1.cell(row=9, column=j, value=h)
        cell.font = header_font
        cell.fill = purple_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        
    tiers = [
        ("Genuine", "0.00 – 0.49", int((df_pred["ghost_status"] == "Genuine").sum()), float((df_pred["ghost_status"] == "Genuine").mean()), float(df_pred.loc[df_pred["ghost_status"] == "Genuine", "days_live"].mean())),
        ("Suspect", "0.50 – 0.74", int((df_pred["ghost_status"] == "Suspect").sum()), float((df_pred["ghost_status"] == "Suspect").mean()), float(df_pred.loc[df_pred["ghost_status"] == "Suspect", "days_live"].mean())),
        ("Ghost", "0.75 – 1.00", int((df_pred["ghost_status"] == "Ghost").sum()), float((df_pred["ghost_status"] == "Ghost").mean()), float(df_pred.loc[df_pred["ghost_status"] == "Ghost", "days_live"].mean())),
    ]
    
    for r_idx, (t_name, t_rng, t_cnt, t_pct, t_age) in enumerate(tiers, start=10):
        ws1.cell(row=r_idx, column=1, value=t_name).font = bold_font
        ws1.cell(row=r_idx, column=2, value=t_rng).alignment = Alignment(horizontal="center")
        c3 = ws1.cell(row=r_idx, column=3, value=t_cnt)
        c3.number_format = "#,##0"
        c4 = ws1.cell(row=r_idx, column=4, value=t_pct)
        c4.number_format = "0.0%"
        c5 = ws1.cell(row=r_idx, column=5, value=t_age)
        c5.number_format = "0.0"
        for c in range(1, 6):
            ws1.cell(row=r_idx, column=c).border = thin_border
            
    # -------------------------------------------------------------
    # SHEET 2: Platform Risk Analysis
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Platform Benchmark")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:E2")
    ws2["A1"] = "CROSS-PLATFORM RISK & COMPLIANCE BENCHMARK"
    ws2["A1"].font = title_font
    ws2["A1"].fill = navy_fill
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    p_headers = ["Platform Source", "Total Listings", "Confirmed Ghosts", "Ghost Rate (%)", "Avg Days Live"]
    for j, h in enumerate(p_headers, start=1):
        cell = ws2.cell(row=4, column=j, value=h)
        cell.font = header_font
        cell.fill = purple_fill
        cell.border = thin_border
        
    p_grp = df_pred.groupby("source").agg(
        total=("listing_id", "count"),
        ghosts=("ghost_status", lambda s: (s == "Ghost").sum()),
        ghost_pct=("ghost_status", lambda s: (s == "Ghost").mean()),
        mean_age=("days_live", "mean")
    ).reset_index()
    
    for r_idx, row in p_grp.iterrows():
        curr_r = 5 + r_idx
        ws2.cell(row=curr_r, column=1, value=row["source"]).font = bold_font
        c2 = ws2.cell(row=curr_r, column=2, value=row["total"])
        c2.number_format = "#,##0"
        c3 = ws2.cell(row=curr_r, column=3, value=row["ghosts"])
        c3.number_format = "#,##0"
        c4 = ws2.cell(row=curr_r, column=4, value=row["ghost_pct"])
        c4.number_format = "0.0%"
        c5 = ws2.cell(row=curr_r, column=5, value=round(row["mean_age"], 1))
        c5.number_format = "0.0"
        for c in range(1, 6):
            ws2.cell(row=curr_r, column=c).border = thin_border
            
    # -------------------------------------------------------------
    # SHEET 3: Listing Age Analysis (Snapshot at Scrape Date)
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Listing Age Analysis")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells("A1:I2")
    ws3["A1"] = "CROSS-SECTIONAL LISTING AGE DISTRIBUTION (SNAPSHOT AT SCRAPE TIME)"
    ws3["A1"].font = title_font
    ws3["A1"].fill = navy_fill
    ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    if len(df_age) > 0:
        s_headers = list(df_age.columns)
        for j, h in enumerate(s_headers, start=1):
            cell = ws3.cell(row=4, column=j, value=h)
            cell.font = header_font
            cell.fill = gold_fill
            cell.border = thin_border
            
        for r_idx, row in df_age.iterrows():
            curr_r = 5 + r_idx
            for j, h in enumerate(s_headers, start=1):
                val = row[h]
                cell = ws3.cell(row=curr_r, column=j, value=val)
                cell.border = thin_border
                cell.font = regular_font
                if isinstance(val, (int, float)):
                    if "Count" in h:
                        cell.number_format = "#,##0"
                    else:
                        cell.number_format = "0.0"
                    
    # -------------------------------------------------------------
    # SHEET 4: High-Risk Listings Register (Top 250)
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="High-Risk Listings")
    ws4.views.sheetView[0].showGridLines = True
    
    reg_headers = ["Listing ID", "Job Title", "Company Name", "Portal", "Days Live", "Ghost Risk Score", "Status Tier", "Top SHAP Driver"]
    for j, h in enumerate(reg_headers, start=1):
        cell = ws4.cell(row=1, column=j, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.border = thin_border
        
    top_risk = df_pred.sort_values("calibrated_ghost_prob", ascending=False).head(250)
    for r_idx, (_, row) in enumerate(top_risk.iterrows(), start=2):
        ws4.cell(row=r_idx, column=1, value=str(row.get("listing_id", "")))
        ws4.cell(row=r_idx, column=2, value=str(row.get("job_title", "")))
        ws4.cell(row=r_idx, column=3, value=str(row.get("company_name", "")))
        ws4.cell(row=r_idx, column=4, value=str(row.get("source", "")))
        
        c5 = ws4.cell(row=r_idx, column=5, value=float(row.get("days_live", 0)))
        c5.number_format = "#,##0"
        
        c6 = ws4.cell(row=r_idx, column=6, value=float(row.get("calibrated_ghost_prob", 0)))
        c6.number_format = "0.0%"
        
        c7 = ws4.cell(row=r_idx, column=7, value=str(row.get("ghost_status", "")))
        c7.font = bold_font
        
        ws4.cell(row=r_idx, column=8, value=str(row.get("top_shap_driver", "")))
        
        for c in range(1, 9):
            ws4.cell(row=r_idx, column=c).border = thin_border
            
    # Auto-adjust column widths across all sheets
    for ws in [ws1, ws2, ws3, ws4]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
            
    out_path = "04_Excel_Workbook/Naukri_Saaf_Executive_Analytics_v4.xlsx"
    wb.save(out_path)
    print(f"Executive workbook successfully generated and saved to: {out_path}")
    print("=" * 80)

if __name__ == "__main__":
    create_executive_workbook()
