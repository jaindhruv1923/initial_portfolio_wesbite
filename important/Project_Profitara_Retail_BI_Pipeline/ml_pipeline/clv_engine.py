import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter, GammaGammaFitter

from ml_pipeline.models import (
    LinearRegressionModel,
    RandomForestRegressor,
    GradientBoostingRegressor,
    compute_r2,
    compute_mae,
    compute_rmse,
    compute_bootstrap_ci,
    compute_permutation_importance
)

SEED = 42
CUTOFF_DATE = pd.to_datetime("2011-09-01 00:00:00")
DATA_PATH = os.path.join("data", "real", "online_retail_II.csv")
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "figures"), exist_ok=True)

def load_and_clean_data(path=DATA_PATH):
    print(f"[CLV Engine] Loading real retail dataset: {path}")
    df = pd.read_csv(path)
    df = df.dropna(subset=["CustomerID"]).copy()
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    # Clean positive valid transactions
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
    return df

def build_time_split_features(df, cutoff=CUTOFF_DATE):
    print(f"[CLV Engine] Splitting at cutoff: {cutoff}")
    obs_df = df[df["InvoiceDate"] < cutoff].copy()
    pred_df = df[df["InvoiceDate"] >= cutoff].copy()

    # Features calculated strictly in observation window
    obs_cust = obs_df.groupby("CustomerID").agg(
        first_date=("InvoiceDate", "min"),
        last_date=("InvoiceDate", "max"),
        frequency=("InvoiceNo", "nunique"),
        monetary_obs=("TotalAmount", "sum"),
        total_quantity=("Quantity", "sum"),
        unique_products=("StockCode", "nunique"),
        avg_item_price=("UnitPrice", "mean")
    ).reset_index()

    obs_cust["recency_days"] = (cutoff - obs_cust["last_date"]).dt.total_seconds() / (24 * 3600)
    obs_cust["tenure_days"] = (cutoff - obs_cust["first_date"]).dt.total_seconds() / (24 * 3600)
    obs_cust["avg_basket_items"] = obs_cust["total_quantity"] / obs_cust["frequency"]

    # Target: Actual customer spend in next 90 days (prediction window)
    pred_spend = pred_df.groupby("CustomerID")["TotalAmount"].sum().reset_index()
    pred_spend.columns = ["CustomerID", "target_spend_90d"]

    dataset = pd.merge(obs_cust, pred_spend, on="CustomerID", how="left")
    dataset["target_spend_90d"] = dataset["target_spend_90d"].fillna(0.0)

    print(f"[CLV Engine] Total cohort customers: {len(dataset):,}")
    print(f"[CLV Engine] Customers active in next 90 days: {(dataset['target_spend_90d'] > 0).sum():,} ({(dataset['target_spend_90d'] > 0).mean()*100:.1f}%)")
    print(f"[CLV Engine] Average 90-day future spend: £{dataset['target_spend_90d'].mean():.2f}")
    return dataset, obs_df, pred_df

def run_clv_pipeline():
    df = load_and_clean_data()
    dataset, obs_df, pred_df = build_time_split_features(df)

    feature_cols = [
        "recency_days", "frequency", "monetary_obs",
        "tenure_days", "avg_basket_items", "unique_products", "avg_item_price"
    ]

    # Train / Test split by customer ID with fixed seed
    rng = np.random.RandomState(SEED)
    cust_ids = dataset["CustomerID"].values
    n = len(dataset)
    indices = np.arange(n)
    rng.shuffle(indices)
    
    n_train = int(0.70 * n)
    train_idx = indices[:n_train]
    test_idx = indices[n_train:]

    train_data = dataset.iloc[train_idx].copy()
    test_data = dataset.iloc[test_idx].copy()

    X_train = train_data[feature_cols].values
    y_train = train_data["target_spend_90d"].values
    X_test = test_data[feature_cols].values
    y_test = test_data["target_spend_90d"].values
    test_ids = test_data["CustomerID"].values

    print(f"[CLV Engine] Training size: {len(train_data)} | Testing size: {len(test_data)}")

    # 1. Baseline: Predict Mean
    mean_val = float(np.mean(y_train))
    preds_mean = np.full_like(y_test, fill_value=mean_val)

    # 2. Baseline: Linear Regression (OLS)
    print("[CLV Engine] Fitting Linear Regression baseline...")
    lr = LinearRegressionModel(alpha=1e-3)
    lr.fit(X_train, y_train)
    preds_lr = np.clip(lr.predict(X_test), 0.0, None)

    # 3. Baseline: BG/NBD + Gamma-Gamma Probabilistic Model
    print("[CLV Engine] Fitting BG/NBD + Gamma-Gamma via lifetimes...")
    cust_orders = obs_df.groupby(["CustomerID", "InvoiceNo"]).agg(
        InvoiceDate=("InvoiceDate", "min"),
        OrderAmount=("TotalAmount", "sum")
    ).reset_index()

    cutoff_ts = CUTOFF_DATE
    lifetimes_rfm = cust_orders.groupby("CustomerID").agg(
        first_order=("InvoiceDate", "min"),
        last_order=("InvoiceDate", "max"),
        total_orders=("InvoiceNo", "count"),
        monetary_mean=("OrderAmount", "mean")
    ).reset_index()

    lifetimes_rfm["frequency_repeat"] = lifetimes_rfm["total_orders"] - 1
    lifetimes_rfm["recency_weeks"] = (lifetimes_rfm["last_order"] - lifetimes_rfm["first_order"]).dt.total_seconds() / (7 * 24 * 3600)
    lifetimes_rfm["T_weeks"] = (cutoff_ts - lifetimes_rfm["first_order"]).dt.total_seconds() / (7 * 24 * 3600)

    train_rfm = lifetimes_rfm[lifetimes_rfm["CustomerID"].isin(train_data["CustomerID"])].copy()
    test_rfm = lifetimes_rfm[lifetimes_rfm["CustomerID"].isin(test_data["CustomerID"])].copy()

    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(train_rfm["frequency_repeat"], train_rfm["recency_weeks"], train_rfm["T_weeks"])

    repeat_train = train_rfm[train_rfm["frequency_repeat"] > 0]
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(repeat_train["frequency_repeat"], repeat_train["monetary_mean"])

    test_rfm_merged = pd.DataFrame({"CustomerID": test_ids}).merge(test_rfm, on="CustomerID", how="left")
    t_weeks = (pd.to_datetime("2011-12-09") - cutoff_ts).total_seconds() / (7 * 24 * 3600)

    exp_trans = bgf.predict(
        t_weeks, test_rfm_merged["frequency_repeat"], test_rfm_merged["recency_weeks"], test_rfm_merged["T_weeks"]
    )
    exp_val = ggf.conditional_expected_average_profit(
        test_rfm_merged["frequency_repeat"], test_rfm_merged["monetary_mean"]
    )
    exp_val = exp_val.fillna(train_rfm["monetary_mean"].mean())
    preds_bgnbd = np.clip((exp_trans * exp_val).fillna(0.0).values, 0.0, None)

    # 4. Random Forest Regressor
    print("[CLV Engine] Training Random Forest Regressor...")
    rf = RandomForestRegressor(n_estimators=40, max_depth=5, min_samples_leaf=15, random_state=SEED)
    rf.fit(X_train, y_train)
    preds_rf = np.clip(rf.predict(X_test), 0.0, None)

    # 5. Gradient Boosting Regressor
    print("[CLV Engine] Training Gradient Boosting Regressor...")
    gb = GradientBoostingRegressor(n_estimators=50, learning_rate=0.06, max_depth=3, min_samples_leaf=20, random_state=SEED)
    gb.fit(X_train, y_train)
    preds_gb = np.clip(gb.predict(X_test), 0.0, None)

    # Evaluate all models
    models = {
        "Predict Mean": preds_mean,
        "Linear Regression (OLS)": preds_lr,
        "BG/NBD + Gamma-Gamma": preds_bgnbd,
        "Random Forest": preds_rf,
        "Gradient Boosting": preds_gb
    }

    results = []
    print("\n" + "="*80)
    print(f"{'Model':<25} {'R²':<10} {'95% CI (R²)':<20} {'MAE (£)':<10} {'95% CI (MAE)':<20} {'RMSE (£)':<10}")
    print("="*80)

    for name, pred in models.items():
        r2 = compute_r2(y_test, pred)
        mae = compute_mae(y_test, pred)
        rmse = compute_rmse(y_test, pred)

        r2_ci = compute_bootstrap_ci(y_test, pred, compute_r2, n_boot=1000, seed=SEED)
        mae_ci = compute_bootstrap_ci(y_test, pred, compute_mae, n_boot=1000, seed=SEED)

        r2_ci_str = f"[{r2_ci[0]:.3f}, {r2_ci[1]:.3f}]"
        mae_ci_str = f"[{mae_ci[0]:.1f}, {mae_ci[1]:.1f}]"

        print(f"{name:<25} {r2:<10.3f} {r2_ci_str:<20} {mae:<10.2f} {mae_ci_str:<20} {rmse:<10.2f}")

        results.append({
            "model": name,
            "r2": round(float(r2), 4),
            "r2_ci_lower": round(r2_ci[0], 4),
            "r2_ci_upper": round(r2_ci[1], 4),
            "mae": round(float(mae), 2),
            "mae_ci_lower": round(mae_ci[0], 2),
            "mae_ci_upper": round(mae_ci[1], 2),
            "rmse": round(float(rmse), 2)
        })

    # Save benchmark metrics to CSV
    metrics_df = pd.DataFrame(results)
    metrics_path = os.path.join(OUTPUT_DIR, "clv_model_benchmarks.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"\n[CLV Engine] Saved benchmark metrics to: {metrics_path}")

    # Decile Calibration Analysis (for best predictive model)
    print("\n[CLV Engine] Computing Decile Calibration for Random Forest...")
    cal_df = pd.DataFrame({"CustomerID": test_ids, "y_true": y_test, "y_pred": preds_rf})
    cal_df["decile"] = pd.qcut(cal_df["y_pred"], q=10, labels=False, duplicates="drop") + 1
    decile_summary = cal_df.groupby("decile").agg(
        customers=("y_true", "count"),
        mean_predicted=("y_pred", "mean"),
        mean_actual=("y_true", "mean")
    ).reset_index()
    decile_summary["calibration_gap"] = decile_summary["mean_predicted"] - decile_summary["mean_actual"]
    
    decile_path = os.path.join(OUTPUT_DIR, "clv_decile_calibration.csv")
    decile_summary.round(2).to_csv(decile_path, index=False)
    print(decile_summary.round(2))

    # Decile Calibration Bar Chart
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x_pos = np.arange(len(decile_summary))
    width = 0.35
    ax.bar(x_pos - width/2, decile_summary["mean_actual"], width, label="Actual Spend (£)", color="#146B5E")
    ax.bar(x_pos + width/2, decile_summary["mean_predicted"], width, label="Predicted Spend (£)", color="#C98A2E")
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"D{int(d)}" for d in decile_summary["decile"]])
    ax.set_xlabel("Predicted Value Decile (D1 = Lowest, D10 = Highest)")
    ax.set_ylabel("Average Spend (£)")
    ax.set_title("Out-of-Time CLV Decile Calibration: Actual vs Predicted", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    chart_path = os.path.join(OUTPUT_DIR, "figures", "clv_decile_calibration.png")
    plt.savefig(chart_path, dpi=150)
    plt.close()
    print(f"[CLV Engine] Saved decile calibration chart to: {chart_path}")

    # Permutation Feature Importance
    print("\n[CLV Engine] Computing Permutation Feature Importance (Random Forest)...")
    importances = compute_permutation_importance(rf, X_test, y_test, compute_mae, n_repeats=5, seed=SEED)
    imp_df = pd.DataFrame({"feature": feature_cols, "mae_increase_when_permuted": importances})
    imp_df = imp_df.sort_values("mae_increase_when_permuted", ascending=False).reset_index(drop=True)
    imp_path = os.path.join(OUTPUT_DIR, "clv_feature_importance.csv")
    imp_df.to_csv(imp_path, index=False)
    print(imp_df.round(2))

    # Feature Importance Plot
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.barh(imp_df["feature"][::-1], imp_df["mae_increase_when_permuted"][::-1], color="#146B5E")
    ax.set_xlabel("Increase in MAE (£) when feature is permuted")
    ax.set_title("CLV Permutation Feature Importance (Random Forest)", fontweight="bold")
    plt.tight_layout()
    imp_chart_path = os.path.join(OUTPUT_DIR, "figures", "clv_feature_importance.png")
    plt.savefig(imp_chart_path, dpi=150)
    plt.close()
    print(f"[CLV Engine] Saved feature importance chart to: {imp_chart_path}")

    # Export test predictions
    test_preds_df = pd.DataFrame({
        "CustomerID": test_ids,
        "ActualSpend_90d": np.round(y_test, 2),
        "PredSpend_Mean": np.round(preds_mean, 2),
        "PredSpend_OLS": np.round(preds_lr, 2),
        "PredSpend_BGNBD": np.round(preds_bgnbd, 2),
        "PredSpend_RF": np.round(preds_rf, 2),
        "PredSpend_GB": np.round(preds_gb, 2)
    })
    preds_out_path = os.path.join(OUTPUT_DIR, "clv_test_predictions.csv")
    test_preds_df.to_csv(preds_out_path, index=False)
    print(f"[CLV Engine] Exported predictions to: {preds_out_path}")

    return metrics_df

if __name__ == "__main__":
    run_clv_pipeline()
