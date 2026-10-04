import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from ml_pipeline.models import (
    LinearRegressionModel,
    RandomForestRegressor,
    compute_rmse,
    compute_mae
)

DATA_PATH = os.path.join("data", "real", "online_retail_II.csv")
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "figures"), exist_ok=True)

SEED = 42

def load_weekly_revenue_series(path=DATA_PATH):
    print(f"[Forecasting] Loading real retail dataset: {path}...")
    df = pd.read_csv(path)
    df = df.dropna(subset=["CustomerID"]).copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

    # Exclude incomplete initial/final partial calendar weeks
    df = df.set_index("InvoiceDate")
    weekly = df["TotalAmount"].resample("W-SUN").sum().reset_index()
    weekly.columns = ["Week_End", "Revenue"]

    # Trim extreme boundary weeks if partial
    weekly = weekly[(weekly["Week_End"] >= "2010-12-05") & (weekly["Week_End"] <= "2011-12-04")].reset_index(drop=True)
    print(f"[Forecasting] Prepared {len(weekly)} weekly revenue observations.")
    print(f"  Start: {weekly['Week_End'].min().strftime('%Y-%m-%d')} | End: {weekly['Week_End'].max().strftime('%Y-%m-%d')}")
    print(f"  Mean Weekly Revenue: £{weekly['Revenue'].mean():,.2f} (std: £{weekly['Revenue'].std():,.2f})")
    return weekly

class HoltWintersDoubleExponential:
    """
    Holt-Winters double exponential smoothing (level + additive trend).
    Alpha and Beta parameters optimized via L-BFGS-B on in-sample sum of squared errors.
    """
    def __init__(self):
        self.alpha = 0.5
        self.beta = 0.1
        self.level_ = None
        self.trend_ = None

    def fit(self, y):
        y = np.asarray(y, dtype=np.float64)
        n = len(y)

        def sse_loss(params):
            alpha, beta = params
            level = y[0]
            trend = y[1] - y[0] if n > 1 else 0.0
            sse = 0.0
            for t in range(1, n):
                pred = level + trend
                err = y[t] - pred
                sse += err ** 2
                new_level = alpha * y[t] + (1.0 - alpha) * (level + trend)
                new_trend = beta * (new_level - level) + (1.0 - beta) * trend
                level, trend = new_level, new_trend
            return sse

        res = minimize(sse_loss, [0.3, 0.1], bounds=[(0.01, 0.99), (0.001, 0.5)], method="L-BFGS-B")
        self.alpha, self.beta = res.x

        # Final pass to get state at end of series
        self.level_ = y[0]
        self.trend_ = y[1] - y[0] if n > 1 else 0.0
        for t in range(1, n):
            new_level = self.alpha * y[t] + (1.0 - self.alpha) * (self.level_ + self.trend_)
            new_trend = self.beta * (new_level - self.level_) + (1.0 - self.beta) * self.trend_
            self.level_, self.trend_ = new_level, new_trend
        return self

    def forecast(self, h):
        return np.array([self.level_ + (i + 1) * self.trend_ for i in range(h)])

def create_autoregressive_lags(series, n_lags=4):
    y = np.asarray(series, dtype=np.float64)
    X_list, y_list = [], []
    for i in range(n_lags, len(y)):
        lags = y[i - n_lags:i]
        roll_mean = np.mean(lags)
        roll_std = np.std(lags)
        features = list(lags) + [roll_mean, roll_std]
        X_list.append(features)
        y_list.append(y[i])
    return np.array(X_list), np.array(y_list)

def compute_mape(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    mask = (y_true != 0)
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0)

def run_rolling_origin_backtest():
    weekly = load_weekly_revenue_series()
    values = weekly["Revenue"].values
    n_total = len(values)
    horizon = 4  # 4-week forecast horizon

    # 3 Rolling Origins (Fold 1, Fold 2, Fold 3)
    # Origin 1: train up to week 39, test 40..43
    # Origin 2: train up to week 43, test 44..47
    # Origin 3: train up to week 47, test 48..51
    origins = [39, 43, 47]
    fold_records = []
    fold_forecasts = []

    print("\n" + "="*85)
    print(f"[Forecasting] Running Rolling-Origin Backtest (Horizon = {horizon} Weeks, 3 Folds)")
    print("="*85)

    for f_idx, origin in enumerate(origins, 1):
        train_y = values[:origin]
        test_y = values[origin:origin + horizon]
        test_dates = weekly["Week_End"].iloc[origin:origin + horizon].values

        # 1. Model: Seasonal / Moving-Average Naive Baseline (Mean of last 4 observed weeks)
        naive_pred = np.full(horizon, fill_value=np.mean(train_y[-4:]))

        # 2. Model: Holt-Winters Double Exponential Smoothing
        hw = HoltWintersDoubleExponential()
        hw.fit(train_y)
        hw_pred = np.clip(hw.forecast(horizon), 0.0, None)

        # 3. Model: Autoregressive ML (Random Forest with 4 lags & rolling stats)
        X_ar, y_ar = create_autoregressive_lags(train_y, n_lags=4)
        rf_ar = RandomForestRegressor(n_estimators=30, max_depth=4, min_samples_leaf=3, random_state=SEED)
        rf_ar.fit(X_ar, y_ar)

        # Recursive multi-step forecast for horizon
        curr_lags = list(train_y[-4:])
        ml_preds = []
        for _ in range(horizon):
            roll_m = np.mean(curr_lags[-4:])
            roll_s = np.std(curr_lags[-4:])
            feat = np.array([curr_lags[-4:] + [roll_m, roll_s]])
            next_p = float(rf_ar.predict(feat)[0])
            ml_preds.append(next_p)
            curr_lags.append(next_p)
        ml_pred = np.array(ml_preds)

        fold_models = {
            "Naive (4W Moving Avg)": naive_pred,
            "Holt-Winters (Double Exp)": hw_pred,
            "Autoregressive Random Forest": ml_pred
        }

        print(f"\n--- FOLD {f_idx} (Train: Weeks 1..{origin} | Test: Weeks {origin+1}..{origin+horizon}) ---")
        print(f"Test Actuals (£): {[round(x, 1) for x in test_y]}")

        for m_name, pred_y in fold_models.items():
            rmse = compute_rmse(test_y, pred_y)
            mae = compute_mae(test_y, pred_y)
            mape = compute_mape(test_y, pred_y)
            print(f"  {m_name:<30}: RMSE=£{rmse:,.0f} | MAE=£{mae:,.0f} | MAPE={mape:.1f}%")

            fold_records.append({
                "fold": f_idx,
                "origin_week": origin,
                "model": m_name,
                "rmse": round(rmse, 2),
                "mae": round(mae, 2),
                "mape": round(mape, 2)
            })

            for h_idx in range(horizon):
                fold_forecasts.append({
                    "fold": f_idx,
                    "model": m_name,
                    "date": pd.to_datetime(test_dates[h_idx]).strftime("%Y-%m-%d"),
                    "actual": round(float(test_y[h_idx]), 2),
                    "forecast": round(float(pred_y[h_idx]), 2)
                })

    df_eval = pd.DataFrame(fold_records)
    eval_path = os.path.join(OUTPUT_DIR, "forecast_rolling_eval.csv")
    df_eval.to_csv(eval_path, index=False)

    # Average performance across all 3 folds
    overall_summary = df_eval.groupby("model").agg(
        mean_rmse=("rmse", "mean"),
        mean_mae=("mae", "mean"),
        mean_mape=("mape", "mean")
    ).reset_index().sort_values("mean_rmse")

    summary_path = os.path.join(OUTPUT_DIR, "forecast_model_summary.csv")
    overall_summary.round(2).to_csv(summary_path, index=False)

    print("\n" + "="*75)
    print("OVERALL ROLLING-ORIGIN BACKTEST PERFORMANCE (AVERAGE OVER 3 FOLDS):")
    print("="*75)
    print(overall_summary.round(2).to_string(index=False))
    print("="*75)

    # Find which model won each fold
    best_per_fold = df_eval.loc[df_eval.groupby("fold")["rmse"].idxmin()]
    print("\nBest Model by Fold (RMSE):")
    for _, r in best_per_fold.iterrows():
        print(f"  Fold {int(r['fold'])}: {r['model']} won (RMSE: £{r['rmse']:,.0f}, MAPE: {r['mape']:.1f}%)")

    # Plot Rolling-Origin Forecast vs Actuals
    df_fc = pd.DataFrame(fold_forecasts)
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=False)
    
    for f_idx in [1, 2, 3]:
        ax = axes[f_idx - 1]
        sub = df_fc[df_fc["fold"] == f_idx]
        actuals = sub[sub["model"] == "Naive (4W Moving Avg)"][["date", "actual"]]
        ax.plot(actuals["date"], actuals["actual"], "k-o", label="Actual Revenue", lw=2)

        for m_name in sub["model"].unique():
            m_sub = sub[sub["model"] == m_name]
            ax.plot(m_sub["date"], m_sub["forecast"], "--s", label=m_name, alpha=0.8)

        ax.set_title(f"Fold {f_idx}: 4-Week Horizon Backtest", fontweight="bold", fontsize=11)
        ax.set_ylabel("Revenue (£)")
        ax.legend(fontsize=8, loc="upper right")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    chart_p = os.path.join(OUTPUT_DIR, "figures", "forecast_rolling_backtest.png")
    plt.savefig(chart_p, dpi=150)
    plt.close()
    print(f"\n[Forecasting] Saved backtest figure to: {chart_p}")
    print(f"[Forecasting] Saved results to: {eval_path}")

    return overall_summary, df_eval

if __name__ == "__main__":
    run_rolling_origin_backtest()
