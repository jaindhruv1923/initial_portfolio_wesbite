"""
Naukri Saaf — Ghost Job Listing Detector Dashboard
====================================================
Run with:  streamlit run app.py

Upload the master dataset (predictions_v3.csv, the final ML pipeline output)
to unlock the dashboard. Optional supplementary files (model comparison,
SHAP values, feature importance, cluster profiles, temporal CV results) can
be uploaded from the sidebar to unlock extra detail in the Model
Performance tab, but every core tab works from the single main file alone.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG + THEME
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Naukri Saaf | Ghost Job Detector",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLOR_GENUINE = "#22C55E"
COLOR_SUSPECT = "#F59E0B"
COLOR_GHOST = "#EF4444"
COLOR_ACCENT = "#8B5CF6"
STATUS_COLORS = {"Genuine": COLOR_GENUINE, "Suspect": COLOR_SUSPECT, "Ghost": COLOR_GHOST}
PLATFORM_COLORS = {"Glassdoor": "#0CAA41", "Indeed": "#2557A7", "LinkedIn": "#0A66C2"}
PLOTLY_TEMPLATE = "plotly_dark"

CUSTOM_CSS = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at 10% 0%, #171225 0%, #0B0E14 45%);
}

section[data-testid="stSidebar"] {
    background-color: #10131C;
    border-right: 1px solid #262B3A;
}

h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.02em; }

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #C4B5FD 0%, #8B5CF6 45%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.hero-subtitle { color: #9CA3AF; font-size: 1.05rem; margin-top: -6px; }

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #171B29 0%, #12151F 100%);
    border: 1px solid #262B3A;
    border-radius: 14px;
    padding: 16px 18px 10px 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
div[data-testid="stMetricLabel"] { color: #9CA3AF !important; font-size: 0.82rem !important; }
div[data-testid="stMetricValue"] { font-size: 1.75rem !important; }

.status-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    text-align: center;
}
.pill-genuine { background: rgba(34,197,94,0.15); color: #4ADE80; border: 1px solid rgba(34,197,94,0.4);}
.pill-suspect { background: rgba(245,158,11,0.15); color: #FBBF24; border: 1px solid rgba(245,158,11,0.4);}
.pill-ghost   { background: rgba(239,68,68,0.15); color: #F87171; border: 1px solid rgba(239,68,68,0.4);}

.section-card {
    background: #12151F;
    border: 1px solid #262B3A;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.small-note { color: #6B7280; font-size: 0.82rem; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background-color: #12151F;
    border-radius: 8px 8px 0 0;
    padding: 8px 16px;
    color: #9CA3AF;
}
.stTabs [aria-selected="true"] {
    background-color: #1E1830 !important;
    color: #C4B5FD !important;
    border-bottom: 2px solid #8B5CF6 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# DATA LOADING HELPERS
# ──────────────────────────────────────────────────────────────────────────
REQUIRED_COLS = [
    "listing_id", "job_title", "company_name", "source",
    "ghost_status", "predicted_ghost_prob", "ghost_label", "predicted_ghost_label",
]

NUMERIC_COERCE_COLS = [
    "days_live", "salary_min", "salary_max", "salary_median", "keyword_match_pct",
    "company_overall_rating", "applications_count", "employer_repost_count",
    "predicted_ghost_prob", "ghost_risk_score", "ghost_label", "predicted_ghost_label",
    "kmeans_cluster", "dbscan_cluster", "dbscan_is_noise", "isolation_anomaly_flag",
    "ci_lower_95", "ci_upper_95", "bootstrap_mean", "stacking_prob",
    "salary_vs_market_gap", "keyword_stuffing_ratio", "description_lexical_diversity",
    "urgency_language_score", "contact_bypass_flag", "cross_platform_duplicate_flag",
]


@st.cache_data(show_spinner=False)
def load_main(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = [c.strip() for c in df.columns]
    for c in ["date_published", "date_scraped"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", format="mixed")
    for c in NUMERIC_COERCE_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "company_name" in df.columns:
        df["company_name"] = df["company_name"].astype(str).str.strip()
    if "ghost_status" in df.columns:
        df["ghost_status"] = df["ghost_status"].astype(str).str.strip().str.title()
        df.loc[~df["ghost_status"].isin(STATUS_COLORS.keys()), "ghost_status"] = np.nan
    return df


@st.cache_data(show_spinner=False)
def load_optional(file):
    if file is None:
        return None
    try:
        return pd.read_csv(file)
    except Exception:
        return None


def fmt_pct(x, decimals=1):
    if pd.isna(x):
        return "—"
    return f"{x * 100:.{decimals}f}%" if abs(x) <= 1.0001 else f"{x:.{decimals}f}%"


def display_df(d: pd.DataFrame) -> pd.DataFrame:
    """Return a display-only copy with NaN shown as a blank instead of
    Streamlit's dataframe grid rendering it as the literal text 'None'."""
    return d.where(pd.notna(d), "")


def status_pill_html(status):
    cls = {"Genuine": "pill-genuine", "Suspect": "pill-suspect", "Ghost": "pill-ghost"}.get(status, "")
    return f'<span class="status-pill {cls}">{status}</span>'


# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR — UPLOAD
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👻 Naukri Saaf")
    st.caption("Ghost Job Listing Detector — control panel")
    st.markdown("---")
    st.markdown("**Step 1 — Upload the master dataset**")
    main_file = st.file_uploader(
        "predictions_v3.csv (final ML pipeline output)",
        type=["csv"],
        help="This is the single combined file produced at the end of the ML pipeline — "
             "it contains all 3 platforms merged, engineered features, and model predictions.",
    )

    with st.expander("⚙️ Optional: extra ML diagnostic files"):
        st.caption("Upload these to unlock extra detail in the Model Performance tab. "
                   "Everything else works from the main file alone.")
        model_comp_file = st.file_uploader("model_comparison_v3.csv", type=["csv"], key="mc")
        shap_file = st.file_uploader("shap_values_v3.csv", type=["csv"], key="shap")
        feat_imp_file = st.file_uploader("feature_importance_v3.csv", type=["csv"], key="fi")
        cluster_file = st.file_uploader("cluster_profiles_v3.csv", type=["csv"], key="cp")
        temporal_file = st.file_uploader("temporal_cv_results_v3.csv", type=["csv"], key="tcv")

# ──────────────────────────────────────────────────────────────────────────
# LANDING (no file yet)
# ──────────────────────────────────────────────────────────────────────────
if main_file is None:
    st.markdown('<p class="hero-title">👻 Naukri Saaf</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Ghost Job Listing Detector — real multi-platform ML analytics dashboard</p>',
        unsafe_allow_html=True,
    )
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="section-card"><h4>📂 Step 1</h4>'
            'Upload <code>predictions_v3.csv</code> from the sidebar — the final output of the '
            'Naukri Saaf ML pipeline (3 platforms merged + 25 engineered features + 5-model ghost predictions).</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="section-card"><h4>⚙️ Step 2 (optional)</h4>'
            'Add the supplementary ML diagnostic CSVs (model comparison, SHAP, cluster profiles) '
            'for deeper model-performance detail.</div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="section-card"><h4>🚀 Step 3</h4>'
            'Explore 7 tabs: Overview, Platforms, Ghost Detection, Employers, Model Performance, '
            'Clustering, and a searchable Data Explorer.</div>',
            unsafe_allow_html=True,
        )
    st.info("Nothing is uploaded to any server — the file stays in this browser session only.")
    st.stop()

# ──────────────────────────────────────────────────────────────────────────
# LOAD + VALIDATE
# ──────────────────────────────────────────────────────────────────────────
try:
    df = load_main(main_file)
except Exception as e:
    st.error(f"Couldn't read that file as CSV. Error: {e}")
    st.stop()

missing = [c for c in REQUIRED_COLS if c not in df.columns]
if missing:
    st.error(
        "This doesn't look like the predictions_v3.csv master file — it's missing columns: "
        f"**{', '.join(missing)}**.\n\nPlease upload the final ML pipeline output "
        "(the file with `ghost_status`, `predicted_ghost_prob`, etc.)."
    )
    st.stop()

if len(df) == 0:
    st.error("The uploaded file has no rows.")
    st.stop()

model_comp_df = load_optional(model_comp_file)
shap_df = load_optional(shap_file)
feat_imp_df = load_optional(feat_imp_file)
cluster_df = load_optional(cluster_file)
temporal_df = load_optional(temporal_file)

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTERS
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("**Filters**")

    platform_opts = sorted(df["source"].dropna().unique().tolist()) if "source" in df.columns else []
    sel_platforms = st.multiselect("Platform", platform_opts, default=platform_opts)

    status_opts = [s for s in ["Genuine", "Suspect", "Ghost"] if s in df["ghost_status"].dropna().unique()]
    sel_statuses = st.multiselect("Ghost status", status_opts, default=status_opts)

    if "experience_level" in df.columns and df["experience_level"].notna().any():
        exp_opts = sorted(df["experience_level"].dropna().unique().tolist())
        sel_exp = st.multiselect("Experience level", exp_opts, default=exp_opts)
    else:
        sel_exp = None

    company_search = st.text_input("Search company name", "")

    date_range = None
    if "date_published" in df.columns and df["date_published"].notna().any():
        min_d, max_d = df["date_published"].min(), df["date_published"].max()
        if pd.notna(min_d) and pd.notna(max_d) and min_d.date() < max_d.date():
            date_range = st.slider(
                "Date published range",
                min_value=min_d.date(), max_value=max_d.date(),
                value=(min_d.date(), max_d.date()),
            )

    st.markdown("---")
    if st.button("🔄 Reset filters"):
        st.rerun()

# apply filters
fdf = df.copy()
if sel_platforms:
    fdf = fdf[fdf["source"].isin(sel_platforms)]
if sel_statuses:
    fdf = fdf[fdf["ghost_status"].isin(sel_statuses)]
if sel_exp:
    fdf = fdf[fdf["experience_level"].isin(sel_exp) | fdf["experience_level"].isna()]
if company_search:
    fdf = fdf[fdf["company_name"].str.contains(company_search, case=False, na=False)]
if date_range:
    start, end = date_range
    fdf = fdf[(fdf["date_published"].dt.date >= start) & (fdf["date_published"].dt.date <= end)]

if len(fdf) == 0:
    st.warning("No listings match the current filters. Try widening them from the sidebar.")
    st.stop()

# ──────────────────────────────────────────────────────────────────────────
# HEADER + KPI ROW
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">👻 Naukri Saaf</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Ghost Job Listing Detector — real multi-platform ML analytics dashboard</p>',
    unsafe_allow_html=True,
)
st.caption(f"Showing **{len(fdf):,}** of {len(df):,} listings after filters")
st.write("")

ghost_rate = (fdf["ghost_status"] == "Ghost").mean() if "ghost_status" in fdf.columns else np.nan
suspect_rate = (fdf["ghost_status"] == "Suspect").mean() if "ghost_status" in fdf.columns else np.nan
n_companies = fdf["company_name"].nunique() if "company_name" in fdf.columns else np.nan
avg_days_live = fdf["days_live"].mean() if "days_live" in fdf.columns else np.nan
avg_prob = fdf["predicted_ghost_prob"].mean() if "predicted_ghost_prob" in fdf.columns else np.nan

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Listings", f"{len(fdf):,}")
k2.metric("Ghost Rate", fmt_pct(ghost_rate) if pd.notna(ghost_rate) else "—",
          help="Share of listings flagged 'Ghost' by the calibrated model")
k3.metric("Suspect Rate", fmt_pct(suspect_rate) if pd.notna(suspect_rate) else "—")
k4.metric("Unique Employers", f"{n_companies:,}" if pd.notna(n_companies) else "—")
k5.metric("Avg. Days Live", f"{avg_days_live:.1f}" if pd.notna(avg_days_live) else "—")

st.write("")

# ──────────────────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────────────────
tab_overview, tab_platform, tab_ghost, tab_employer, tab_model, tab_cluster, tab_explore = st.tabs(
    ["🏠 Overview", "🌐 Platforms", "👻 Ghost Detection", "🏢 Employers",
     "🤖 Model Performance", "🧩 Clustering", "🔍 Explore Data"]
)

# ---------------------------------------------------------------- OVERVIEW
with tab_overview:
    c1, c2 = st.columns([1, 1.3])

    with c1:
        st.markdown("##### Ghost status breakdown")
        status_counts = fdf["ghost_status"].value_counts().reindex(["Genuine", "Suspect", "Ghost"]).dropna()
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index, values=status_counts.values, hole=0.55,
            marker=dict(colors=[STATUS_COLORS[s] for s in status_counts.index]),
            textinfo="label+percent",
        )])
        fig.update_layout(template=PLOTLY_TEMPLATE, showlegend=False, height=340,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("##### Listings by platform")
        plat_counts = fdf["source"].value_counts()
        fig = px.bar(
            x=plat_counts.values, y=plat_counts.index, orientation="h",
            color=plat_counts.index, color_discrete_map=PLATFORM_COLORS,
            labels={"x": "Listings", "y": ""}, text=plat_counts.values,
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(template=PLOTLY_TEMPLATE, showlegend=False, height=340,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    if "date_published" in fdf.columns and fdf["date_published"].notna().sum() > 5:
        st.markdown("##### Postings over time, by ghost status")
        tdf = fdf.dropna(subset=["date_published"]).copy()
        tdf["month"] = tdf["date_published"].dt.to_period("M").dt.to_timestamp()
        trend = tdf.groupby(["month", "ghost_status"]).size().reset_index(name="count")
        fig = px.area(
            trend, x="month", y="count", color="ghost_status",
            color_discrete_map=STATUS_COLORS,
            category_orders={"ghost_status": ["Genuine", "Suspect", "Ghost"]},
        )
        fig.update_layout(template=PLOTLY_TEMPLATE, height=320, legend_title="",
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    if "job_category" in fdf.columns:
        st.markdown("##### Top job categories")
        top_cat = fdf["job_category"].value_counts().head(12).sort_values()
        fig = px.bar(x=top_cat.values, y=top_cat.index, orientation="h",
                     labels={"x": "Listings", "y": ""}, color_discrete_sequence=[COLOR_ACCENT])
        fig.update_layout(template=PLOTLY_TEMPLATE, height=380,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------- PLATFORMS
with tab_platform:
    st.markdown("##### Platform comparison")
    agg_dict = {"listing_id": "count"}
    if "days_live" in fdf.columns:
        agg_dict["days_live"] = "mean"
    if "ghost_label" in fdf.columns:
        agg_dict["ghost_label"] = "mean"
    if "salary_disclosed_num" in fdf.columns:
        agg_dict["salary_disclosed_num"] = "mean"
    if "company_overall_rating" in fdf.columns:
        agg_dict["company_overall_rating"] = "mean"

    plat_summary = fdf.groupby("source").agg(agg_dict).rename(columns={
        "listing_id": "Listings", "days_live": "Avg Days Live",
        "ghost_label": "Ghost Rate", "salary_disclosed_num": "Salary Disclosure Rate",
        "company_overall_rating": "Avg Company Rating",
    })
    if "Ghost Rate" in plat_summary.columns:
        plat_summary["Ghost Rate"] = (plat_summary["Ghost Rate"] * 100).round(1)
    if "Salary Disclosure Rate" in plat_summary.columns:
        plat_summary["Salary Disclosure Rate"] = (plat_summary["Salary Disclosure Rate"] * 100).round(1)
    plat_summary = plat_summary.round(1)
    st.dataframe(display_df(plat_summary), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        if "ghost_label" in fdf.columns:
            st.markdown("##### Ghost rate by platform")
            gr = (fdf.groupby("source")["ghost_label"].mean() * 100).sort_values()
            fig = px.bar(x=gr.values, y=gr.index, orientation="h",
                         color=gr.index, color_discrete_map=PLATFORM_COLORS,
                         labels={"x": "Ghost Rate (%)", "y": ""}, text=gr.round(1))
            fig.update_traces(textposition="outside")
            fig.update_layout(template=PLOTLY_TEMPLATE, showlegend=False, height=320,
                               margin=dict(l=10, r=10, t=10, b=10),
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("##### Ghost status mix by platform")
        mix = fdf.groupby(["source", "ghost_status"]).size().reset_index(name="count")
        fig = px.bar(mix, x="source", y="count", color="ghost_status", barmode="stack",
                     color_discrete_map=STATUS_COLORS,
                     category_orders={"ghost_status": ["Genuine", "Suspect", "Ghost"]},
                     labels={"source": "", "count": "Listings"})
        fig.update_layout(template=PLOTLY_TEMPLATE, height=320, legend_title="",
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    if "salary_disclosed_num" in fdf.columns:
        st.markdown("##### Data completeness by platform")
        st.caption("Different platforms structurally expose different fields (e.g. LinkedIn has no public salary field) — "
                   "this isn't a data-quality bug, it's a real scrape characteristic.")
        completeness_cols = [c for c in ["salary_disclosed_num", "company_overall_rating", "applications_count"]
                             if c in fdf.columns]
        comp = fdf.groupby("source")[completeness_cols].apply(lambda x: x.notna().mean() * 100).round(1)
        comp = comp.rename(columns={"salary_disclosed_num": "Salary Field %",
                                     "company_overall_rating": "Company Rating %",
                                     "applications_count": "Applications Count %"})
        st.dataframe(display_df(comp), use_container_width=True)

# ---------------------------------------------------------------- GHOST DETECTION
with tab_ghost:
    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.markdown("##### Predicted ghost probability distribution")
        fig = px.histogram(fdf, x="predicted_ghost_prob", color="ghost_status",
                           color_discrete_map=STATUS_COLORS, nbins=40,
                           category_orders={"ghost_status": ["Genuine", "Suspect", "Ghost"]})
        fig.update_layout(template=PLOTLY_TEMPLATE, height=340, legend_title="",
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("##### Model confidence (bootstrap CI)")
        if "ci_lower_95" in fdf.columns and "ci_upper_95" in fdf.columns:
            fdf_ci = fdf.dropna(subset=["ci_lower_95", "ci_upper_95"]).copy()
            fdf_ci["ci_width"] = fdf_ci["ci_upper_95"] - fdf_ci["ci_lower_95"]
            st.metric("Avg. 95% CI width", f"{fdf_ci['ci_width'].mean():.3f}",
                      help="Narrower = model is more confident about its ghost-probability estimates")
            fig = px.histogram(fdf_ci, x="ci_width", color_discrete_sequence=[COLOR_ACCENT], nbins=30)
            fig.update_layout(template=PLOTLY_TEMPLATE, height=270,
                               margin=dict(l=10, r=10, t=10, b=10),
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Bootstrap CI columns not found in this file.")

    st.markdown("##### Ghost rate by dimension")
    dim_options = [c for c in ["job_category", "experience_level", "city_tier", "job_type", "remote_type"]
                   if c in fdf.columns]
    if dim_options:
        dim = st.selectbox("Break down by:", dim_options)
        top_n = st.slider("Show top N categories", 5, 25, 12)
        grp = fdf.groupby(dim).agg(listings=("listing_id", "count"), ghost_rate=("ghost_label", "mean"))
        grp = grp[grp["listings"] >= 5].sort_values("ghost_rate", ascending=False).head(top_n)
        grp["ghost_rate"] = (grp["ghost_rate"] * 100).round(1)
        fig = px.bar(grp.sort_values("ghost_rate"), x="ghost_rate", y=grp.sort_values("ghost_rate").index,
                     orientation="h", color="ghost_rate", color_continuous_scale=["#22C55E", "#F59E0B", "#EF4444"],
                     labels={"ghost_rate": "Ghost Rate (%)", "y": ""},
                     hover_data={"listings": True})
        fig.update_layout(template=PLOTLY_TEMPLATE, height=420, showlegend=False,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Only categories with 5+ listings shown, to avoid noisy small-sample rates.")

    st.markdown("##### Top red-flag listings")
    show_cols = [c for c in ["job_title", "company_name", "source", "predicted_ghost_prob", "ghost_status",
                             "days_live", "employer_repost_count", "salary_disclosed_num"] if c in fdf.columns]
    top_risk = fdf.sort_values("predicted_ghost_prob", ascending=False)[show_cols].head(20).reset_index(drop=True)
    st.dataframe(display_df(top_risk), use_container_width=True, height=380)

# ---------------------------------------------------------------- EMPLOYERS
with tab_employer:
    st.markdown("##### Employer risk explorer")
    agg_dict = {"listing_id": "count"}
    if "ghost_label" in fdf.columns:
        agg_dict["ghost_label"] = "mean"
    if "predicted_ghost_prob" in fdf.columns:
        agg_dict["predicted_ghost_prob"] = "mean"
    if "employer_repost_count" in fdf.columns:
        agg_dict["employer_repost_count"] = "max"
    if "days_live" in fdf.columns:
        agg_dict["days_live"] = "mean"
    if "company_overall_rating" in fdf.columns:
        agg_dict["company_overall_rating"] = "mean"

    emp = fdf.groupby("company_name").agg(agg_dict).rename(columns={
        "listing_id": "Listings", "ghost_label": "Ghost Rate", "predicted_ghost_prob": "Avg Ghost Prob",
        "employer_repost_count": "Max Reposts", "days_live": "Avg Days Live",
        "company_overall_rating": "Avg Rating",
    })
    min_listings = st.slider("Minimum listings per employer", 1, 10, 2,
                             help="Employers with very few listings can show noisy 0%/100% ghost rates — "
                                  "default of 2 filters that out. Lower it to see everyone.")
    emp = emp[emp["Listings"] >= min_listings]
    if "Ghost Rate" in emp.columns:
        emp["Ghost Rate"] = (emp["Ghost Rate"] * 100).round(1)
    emp = emp.round(3).sort_values("Ghost Rate" if "Ghost Rate" in emp.columns else "Listings", ascending=False)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**⚠️ Highest-risk employers**")
        st.dataframe(display_df(emp.head(15)), use_container_width=True, height=420)
    with c2:
        st.markdown("**✅ Most trusted employers**")
        trusted = emp[emp["Listings"] >= max(2, min_listings)].sort_values(
            "Ghost Rate" if "Ghost Rate" in emp.columns else "Listings")
        st.dataframe(display_df(trusted.head(15)), use_container_width=True, height=420)

    if "employer_repost_count" in fdf.columns:
        st.markdown("##### Repost count vs. ghost probability")
        fig = px.scatter(fdf, x="employer_repost_count", y="predicted_ghost_prob",
                         color="ghost_status", color_discrete_map=STATUS_COLORS,
                         hover_data=["company_name", "job_title"],
                         category_orders={"ghost_status": ["Genuine", "Suspect", "Ghost"]},
                         opacity=0.6)
        fig.update_layout(template=PLOTLY_TEMPLATE, height=380, legend_title="",
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------- MODEL PERFORMANCE
with tab_model:
    st.markdown("##### Model leaderboard")
    if model_comp_df is not None:
        mc = model_comp_df.copy()
        st.dataframe(mc.style.highlight_max(subset=[c for c in mc.columns if c != "Model"], color="#2D2050"),
                    use_container_width=True)
        metric_col = "AUC" if "AUC" in mc.columns else mc.columns[1]
        fig = px.bar(mc.sort_values(metric_col), x=metric_col, y="Model", orientation="h",
                     color=metric_col, color_continuous_scale="Purples",
                     text=mc.sort_values(metric_col)[metric_col].round(3))
        fig.update_layout(template=PLOTLY_TEMPLATE, height=320, showlegend=False,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📎 Upload `model_comparison_v3.csv` from the sidebar to see the full 5-model leaderboard "
               "(AUC / F1 / Precision / Recall).")

    # We can always compute a live confusion matrix from the main file itself,
    # since it already contains both the weak-supervision label and the model's prediction.
    if "ghost_label" in fdf.columns and "predicted_ghost_label" in fdf.columns:
        st.markdown("##### Live confusion matrix (this filtered slice)")
        st.caption("Comparing the calibrated model's binary prediction against the weak-supervision ghost label, "
                   "recomputed on whatever filters are currently applied.")
        y_true = fdf["ghost_label"].dropna().astype(int)
        y_pred = fdf.loc[y_true.index, "predicted_ghost_label"].astype(int)
        tp = int(((y_true == 1) & (y_pred == 1)).sum())
        tn = int(((y_true == 0) & (y_pred == 0)).sum())
        fp = int(((y_true == 0) & (y_pred == 1)).sum())
        fn = int(((y_true == 1) & (y_pred == 0)).sum())
        cm = np.array([[tn, fp], [fn, tp]])
        fig = px.imshow(cm, text_auto=True, color_continuous_scale="Purples",
                        x=["Pred: Genuine", "Pred: Ghost"], y=["Actual: Genuine", "Actual: Ghost"])
        fig.update_layout(template=PLOTLY_TEMPLATE, height=340,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            precision = tp / (tp + fp) if (tp + fp) else np.nan
            recall = tp / (tp + fn) if (tp + fn) else np.nan
            f1 = 2 * precision * recall / (precision + recall) if precision and recall else np.nan
            st.metric("Precision", f"{precision:.3f}" if pd.notna(precision) else "—")
            st.metric("Recall", f"{recall:.3f}" if pd.notna(recall) else "—")
            st.metric("F1 Score", f"{f1:.3f}" if pd.notna(f1) else "—")

    if temporal_df is not None:
        st.markdown("##### Temporal cross-validation (5 folds)")
        fig = px.line(temporal_df, x="fold", y="auc", color="model", markers=True)
        fig.update_layout(template=PLOTLY_TEMPLATE, height=320, legend_title="",
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Feature importance")
    if feat_imp_df is not None:
        fi = feat_imp_df.copy()
        fi.columns = ["feature", "importance"] if len(fi.columns) == 2 else fi.columns
        fi = fi.sort_values("importance", ascending=True).tail(20)
        fig = px.bar(fi, x="importance", y="feature", orientation="h",
                     color="importance", color_continuous_scale="Purples")
        fig.update_layout(template=PLOTLY_TEMPLATE, height=520, showlegend=False,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    elif shap_df is not None:
        shap_cols = [c for c in shap_df.columns if c.endswith("_shap") and c not in
                    ("shap_ghost_total", "shap_genuine_total")]
        if shap_cols:
            mean_abs = shap_df[shap_cols].abs().mean().sort_values(ascending=True).tail(20)
            mean_abs.index = [c.replace("_shap", "") for c in mean_abs.index]
            fig = px.bar(x=mean_abs.values, y=mean_abs.index, orientation="h",
                         color=mean_abs.values, color_continuous_scale="Purples",
                         labels={"x": "Mean |SHAP value|", "y": ""})
            fig.update_layout(template=PLOTLY_TEMPLATE, height=520, showlegend=False,
                               margin=dict(l=10, r=10, t=10, b=10),
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📎 Upload `feature_importance_v3.csv` or `shap_values_v3.csv` from the sidebar to see this chart.")

# ---------------------------------------------------------------- CLUSTERING
with tab_cluster:
    st.markdown("##### K-Means employer archetypes")
    if "kmeans_cluster_label" in fdf.columns:
        if cluster_df is not None:
            st.dataframe(display_df(cluster_df), use_container_width=True)
        else:
            agg_dict = {"listing_id": "count"}
            if "ghost_label" in fdf.columns:
                agg_dict["ghost_label"] = "mean"
            if "days_live" in fdf.columns:
                agg_dict["days_live"] = "mean"
            if "employer_repost_count" in fdf.columns:
                agg_dict["employer_repost_count"] = "mean"
            live_cluster = fdf.groupby("kmeans_cluster_label").agg(agg_dict).rename(columns={
                "listing_id": "count", "ghost_label": "ghost_rate",
                "days_live": "avg_days_live", "employer_repost_count": "avg_repost",
            })
            if "ghost_rate" in live_cluster.columns:
                live_cluster["ghost_rate"] = (live_cluster["ghost_rate"] * 100).round(1)
            st.dataframe(display_df(live_cluster.round(1)), use_container_width=True)

        clus_counts = fdf["kmeans_cluster_label"].value_counts()
        fig = px.bar(x=clus_counts.values, y=clus_counts.index, orientation="h",
                     color_discrete_sequence=[COLOR_ACCENT],
                     labels={"x": "Listings", "y": ""})
        fig.update_layout(template=PLOTLY_TEMPLATE, height=340, showlegend=False,
                           margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("`kmeans_cluster_label` column not found in this file.")

    st.markdown("##### DBSCAN ghost-contagion rings")
    if "dbscan_cluster" in fdf.columns and "dbscan_is_noise" in fdf.columns:
        n_rings = fdf.loc[fdf["dbscan_cluster"] >= 0, "dbscan_cluster"].nunique()
        n_noise = int(fdf["dbscan_is_noise"].sum())
        c1, c2 = st.columns(2)
        c1.metric("Contagion rings found", f"{n_rings}")
        c2.metric("Isolated listings (noise)", f"{n_noise:,}")
        ring_sizes = fdf[fdf["dbscan_cluster"] >= 0]["dbscan_cluster"].value_counts().sort_values(ascending=False).head(15)
        if len(ring_sizes):
            fig = px.bar(x=ring_sizes.index.astype(str), y=ring_sizes.values,
                        labels={"x": "Ring ID", "y": "Listings in ring"},
                        color_discrete_sequence=[COLOR_GHOST])
            fig.update_layout(template=PLOTLY_TEMPLATE, height=320,
                               margin=dict(l=10, r=10, t=10, b=10),
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("DBSCAN columns not found in this file.")

# ---------------------------------------------------------------- EXPLORE
with tab_explore:
    st.markdown("##### Full filtered data table")
    st.caption("Search, sort (click column headers), and download whatever slice you're looking at.")

    text_search = st.text_input("Quick search (job title / company / description)", "")
    edf = fdf.copy()
    if text_search:
        mask = pd.Series(False, index=edf.index)
        for col in ["job_title", "company_name", "description_text"]:
            if col in edf.columns:
                mask |= edf[col].str.contains(text_search, case=False, na=False)
        edf = edf[mask]

    default_cols = [c for c in [
        "listing_id", "job_title", "company_name", "source", "location_city",
        "days_live", "salary_min", "salary_max", "ghost_status", "predicted_ghost_prob",
        "kmeans_cluster_label",
    ] if c in edf.columns]
    all_cols = list(edf.columns)
    show_cols = st.multiselect("Columns to show", all_cols, default=default_cols)

    st.dataframe(display_df(edf[show_cols] if show_cols else edf), use_container_width=True, height=460)
    st.caption(f"{len(edf):,} rows match")

    csv_bytes = edf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download this filtered slice as CSV", csv_bytes,
                       file_name="naukri_saaf_filtered.csv", mime="text/csv")

st.markdown("---")
st.caption("Naukri Saaf — Ghost Job Listing Detector · Built by Dhruv Jain · "
          "Real data via Apify (Glassdoor, Indeed, LinkedIn) · scikit-learn ML pipeline")
