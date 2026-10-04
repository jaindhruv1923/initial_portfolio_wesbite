import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ml_pipeline.models import (
    LogisticRegressionModel,
    compute_roc_auc,
    compute_bootstrap_ci
)

SEED = 42
CUTOFF_DATE = pd.to_datetime("2011-09-01 00:00:00")
DATA_PATH = os.path.join("data", "real", "online_retail_II.csv")
CONFIG_PATH = os.path.join("config", "business_assumptions.yaml")
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "figures"), exist_ok=True)

def load_assumptions(path=CONFIG_PATH):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg["assumptions"]

def load_data_and_features():
    print("[Churn Engine] Loading transaction data...")
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["CustomerID"]).copy()
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

    obs_df = df[df["InvoiceDate"] < CUTOFF_DATE].copy()
    pred_df = df[df["InvoiceDate"] >= CUTOFF_DATE].copy()

    # Observation features (zero future information)
    obs_cust = obs_df.groupby("CustomerID").agg(
        first_date=("InvoiceDate", "min"),
        last_date=("InvoiceDate", "max"),
        frequency=("InvoiceNo", "nunique"),
        monetary_obs=("TotalAmount", "sum"),
        total_quantity=("Quantity", "sum"),
        unique_products=("StockCode", "nunique"),
        avg_item_price=("UnitPrice", "mean")
    ).reset_index()

    obs_cust["recency_days"] = (CUTOFF_DATE - obs_cust["last_date"]).dt.total_seconds() / (24 * 3600)
    obs_cust["tenure_days"] = (CUTOFF_DATE - obs_cust["first_date"]).dt.total_seconds() / (24 * 3600)
    obs_cust["avg_basket_items"] = obs_cust["total_quantity"] / obs_cust["frequency"]

    # Churn definition: No purchase in 90-day prediction window
    future_purchases = pred_df.groupby("CustomerID")["InvoiceNo"].nunique().reset_index()
    future_purchases.columns = ["CustomerID", "future_order_count"]

    data = pd.merge(obs_cust, future_purchases, on="CustomerID", how="left")
    data["future_order_count"] = data["future_order_count"].fillna(0)
    # Churned = 1 if 0 future orders, 0 if >= 1 future orders
    data["churned_90d"] = (data["future_order_count"] == 0).astype(int)

    # Future spend for ground truth backtesting
    future_spend = pred_df.groupby("CustomerID")["TotalAmount"].sum().reset_index()
    future_spend.columns = ["CustomerID", "actual_future_spend"]
    data = pd.merge(data, future_spend, on="CustomerID", how="left")
    data["actual_future_spend"] = data["actual_future_spend"].fillna(0.0)

    print(f"[Churn Engine] Cohort total: {len(data):,} customers")
    print(f"[Churn Engine] Churned customers: {data['churned_90d'].sum():,} ({data['churned_90d'].mean()*100:.1f}%)")
    print(f"[Churn Engine] Retained customers: {(data['churned_90d'] == 0).sum():,} ({(data['churned_90d'] == 0).mean()*100:.1f}%)")
    return data

def run_churn_decision_pipeline():
    assumptions = load_assumptions()
    data = load_data_and_features()

    feature_cols = [
        "recency_days", "frequency", "monetary_obs",
        "tenure_days", "avg_basket_items", "unique_products", "avg_item_price"
    ]

    # Split train/test (70/30) matching CLV split
    rng = np.random.RandomState(SEED)
    n = len(data)
    indices = np.arange(n)
    rng.shuffle(indices)
    n_train = int(0.70 * n)
    train_idx = indices[:n_train]
    test_idx = indices[n_train:]

    train_df = data.iloc[train_idx].copy()
    test_df = data.iloc[test_idx].copy()

    X_train = train_df[feature_cols].values
    y_train = train_df["churned_90d"].values
    X_test = test_df[feature_cols].values
    y_test = test_df["churned_90d"].values

    # Standardize features for logistic regression
    mean_X = np.mean(X_train, axis=0)
    std_X = np.std(X_train, axis=0) + 1e-12
    X_train_scaled = (X_train - mean_X) / std_X
    X_test_scaled = (X_test - mean_X) / std_X

    # 1. Baseline: Prior probability
    prior_churn = np.mean(y_train)
    probs_prior = np.full_like(y_test, fill_value=prior_churn, dtype=float)

    # 2. Baseline: Recency Heuristic (churn if recency > 90 days)
    recency_col_idx = feature_cols.index("recency_days")
    probs_heuristic = (X_test[:, recency_col_idx] > 90.0).astype(float)

    # 3. Model: Logistic Regression with Calibrated Probabilities
    print("[Churn Engine] Fitting Logistic Regression...")
    clf = LogisticRegressionModel(C=0.5, max_iter=300)
    clf.fit(X_train_scaled, y_train)
    probs_logit = clf.predict_proba(X_test_scaled)[:, 1]

    # Metrics evaluation
    def brier_score(y_true, y_prob):
        return float(np.mean((y_true - y_prob) ** 2))

    def log_loss(y_true, y_prob, eps=1e-12):
        p = np.clip(y_prob, eps, 1.0 - eps)
        return float(-np.mean(y_true * np.log(p) + (1.0 - y_true) * np.log(1.0 - p)))

    models = {
        "Prior Baseline": probs_prior,
        "Recency Heuristic (>90d)": probs_heuristic,
        "Logistic Regression": probs_logit
    }

    results = []
    print("\n" + "="*75)
    print(f"{'Model':<28} {'ROC-AUC':<12} {'95% CI (AUC)':<18} {'Brier Score':<14} {'Log-Loss':<10}")
    print("="*75)

    for name, probs in models.items():
        auc_val = compute_roc_auc(y_test, probs)
        brier = brier_score(y_test, probs)
        ll = log_loss(y_test, probs)

        if name != "Prior Baseline":
            auc_ci = compute_bootstrap_ci(y_test, probs, compute_roc_auc, n_boot=1000, seed=SEED)
            auc_ci_str = f"[{auc_ci[0]:.3f}, {auc_ci[1]:.3f}]"
        else:
            auc_ci = (0.5, 0.5)
            auc_ci_str = "[0.500, 0.500]"

        print(f"{name:<28} {auc_val:<12.3f} {auc_ci_str:<18} {brier:<14.4f} {ll:<10.4f}")

        results.append({
            "model": name,
            "roc_auc": round(float(auc_val), 4),
            "auc_ci_lower": round(auc_ci[0], 4),
            "auc_ci_upper": round(auc_ci[1], 4),
            "brier_score": round(float(brier), 4),
            "log_loss": round(float(ll), 4)
        })

    benchmarks_df = pd.DataFrame(results)
    bench_path = os.path.join(OUTPUT_DIR, "churn_model_benchmarks.csv")
    benchmarks_df.to_csv(bench_path, index=False)
    print(f"[Churn Engine] Saved benchmarks to: {bench_path}")

    # =========================================================================
    # DECISION LAYER: Expected Value of Win-back Optimization
    # =========================================================================
    print("\n[Churn Engine] Building Expected Value Decision Layer...")
    
    # Load CLV test predictions
    clv_preds_path = os.path.join(OUTPUT_DIR, "clv_test_predictions.csv")
    if os.path.exists(clv_preds_path):
        clv_df = pd.read_csv(clv_preds_path)
        clv_df["CustomerID"] = clv_df["CustomerID"].astype(str)
        test_df["CustomerID"] = test_df["CustomerID"].astype(str)
        test_df = pd.merge(test_df, clv_df[["CustomerID", "PredSpend_RF"]], on="CustomerID", how="left")
        test_df["pred_clv"] = test_df["PredSpend_RF"].fillna(test_df["monetary_obs"] * 0.25)
    else:
        test_df["pred_clv"] = test_df["monetary_obs"] * 0.25

    cost = assumptions["campaign_cost_per_contact_gbp"]
    margin = assumptions["retail_gross_margin_pct"]
    resp_rate = assumptions["winback_response_rate"]
    budget = assumptions["marketing_budget_gbp"]
    max_contacts = int(budget // cost)  # e.g. £1,500 / £5 = 300 customers

    test_df["prob_churn"] = probs_logit
    # Expected Value Formula:
    # EV = P(churn) * response_rate * predicted_CLV * margin - campaign_cost
    test_df["expected_gross_recovery"] = test_df["prob_churn"] * resp_rate * test_df["pred_clv"] * margin
    test_df["expected_net_value"] = test_df["expected_gross_recovery"] - cost

    print(f"[Churn Engine] Assumptions: Cost=£{cost:.2f}, Margin={margin*100:.0f}%, Response={resp_rate*100:.0f}%, Budget=£{budget:.0f} (Cap: {max_contacts} contacts)")

    # 4 Policies under same budget cap:
    # Policy 1: Expected Value Optimization (target top EV positive candidates)
    ev_policy = test_df[test_df["expected_net_value"] > 0].sort_values("expected_net_value", ascending=False).head(max_contacts)

    # Policy 2: Top RFM Recency (contact customers with longest inactivity)
    recency_policy = test_df.sort_values("recency_days", ascending=False).head(max_contacts)

    # Policy 3: Top Historic Spenders (contact top past monetary value)
    spend_policy = test_df.sort_values("monetary_obs", ascending=False).head(max_contacts)

    # Policy 4: Random Selection
    random_policy = test_df.sample(n=min(max_contacts, len(test_df)), random_state=SEED)

    policies = {
        "Expected Value Policy (Proposed)": ev_policy,
        "Top Recency Policy (Naive RFM)": recency_policy,
        "Top Spender Policy (High Monetary)": spend_policy,
        "Random Policy (Control)": random_policy
    }

    policy_comparison = []
    for pname, pcohort in policies.items():
        n_targeted = len(pcohort)
        total_cost = n_targeted * cost
        # Ground truth outcomes in prediction window
        actual_churners_reached = pcohort["churned_90d"].sum()
        actual_retained_reached = (pcohort["churned_90d"] == 0).sum()
        simulated_expected_net_profit = pcohort["expected_net_value"].sum()
        total_historical_spend = pcohort["monetary_obs"].sum()
        future_spend_at_stake = pcohort["pred_clv"].sum()

        policy_comparison.append({
            "policy": pname,
            "customers_contacted": n_targeted,
            "total_campaign_cost_gbp": round(total_cost, 2),
            "simulated_net_value_gbp": round(simulated_expected_net_profit, 2),
            "actual_churners_reached": int(actual_churners_reached),
            "actual_churn_capture_rate": f"{actual_churners_reached/n_targeted*100:.1f}%",
            "future_clv_at_stake_gbp": round(future_spend_at_stake, 2)
        })

    policy_df = pd.DataFrame(policy_comparison)
    backtest_path = os.path.join(OUTPUT_DIR, "churn_policy_backtest.csv")
    policy_df.to_csv(backtest_path, index=False)
    print("\n" + "="*80)
    print(policy_df.to_string(index=False))
    print("="*80)
    print(f"[Churn Engine] Saved policy backtest to: {backtest_path}")

    # Sensitivity Analysis across response rates and contact costs
    print("\n[Churn Engine] Computing Sensitivity Analysis Matrix...")
    cost_grid = [2.50, 5.00, 7.50, 10.00]
    resp_grid = [0.05, 0.10, 0.15, 0.20, 0.25]
    sens_rows = []

    for c in cost_grid:
        for r in resp_grid:
            cap = int(budget // c)
            temp_ev = (test_df["prob_churn"] * r * test_df["pred_clv"] * margin) - c
            top_ev = temp_ev[temp_ev > 0].sort_values(ascending=False).head(cap)
            sim_net = top_ev.sum()
            sens_rows.append({
                "campaign_cost_gbp": c,
                "response_rate_pct": f"{int(r*100)}%",
                "budget_gbp": budget,
                "max_contacts": cap,
                "profitable_contacts_count": len(top_ev),
                "simulated_net_return_gbp": round(sim_net, 2)
            })

    sens_df = pd.DataFrame(sens_rows)
    sens_path = os.path.join(OUTPUT_DIR, "churn_policy_sensitivity.csv")
    sens_df.to_csv(sens_path, index=False)
    print(f"[Churn Engine] Saved sensitivity analysis to: {sens_path}")

    # Plot Policy Comparison
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    bars = ax.bar(
        [p.replace(" Policy", "") for p in policy_df["policy"]],
        policy_df["simulated_net_value_gbp"],
        color=["#146B5E", "#C98A2E", "#445158", "#B5482E"]
    )
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f"£{yval:,.0f}", ha='center', va='bottom', fontweight='bold')
    ax.set_ylabel("Simulated Expected Net Return (£)")
    ax.set_title("Win-Back Policy Comparison: Expected Value vs Naive Rules (£1,500 Budget)", fontweight="bold")
    ax.axhline(0, color="black", lw=0.8)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    chart_p = os.path.join(OUTPUT_DIR, "figures", "churn_policy_comparison.png")
    plt.savefig(chart_p, dpi=150)
    plt.close()
    print(f"[Churn Engine] Saved policy comparison chart to: {chart_p}")

    # Export prioritized win-back targets
    ev_policy_export = ev_policy[["CustomerID", "prob_churn", "pred_clv", "expected_gross_recovery", "expected_net_value"]].copy()
    ev_policy_export["prob_churn"] = ev_policy_export["prob_churn"].round(3)
    ev_policy_export["pred_clv"] = ev_policy_export["pred_clv"].round(2)
    ev_policy_export["expected_gross_recovery"] = ev_policy_export["expected_gross_recovery"].round(2)
    ev_policy_export["expected_net_value"] = ev_policy_export["expected_net_value"].round(2)
    targets_path = os.path.join(OUTPUT_DIR, "winback_priority_targets.csv")
    ev_policy_export.to_csv(targets_path, index=False)
    print(f"[Churn Engine] Exported priority win-back targets to: {targets_path}")

    return benchmarks_df, policy_df

if __name__ == "__main__":
    run_churn_decision_pipeline()
