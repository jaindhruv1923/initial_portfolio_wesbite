"""
Full Production Machine Learning Training & Validation Pipeline
=============================================================
1. Enforces zero data leakage with `LeakageFreeFeatureExtractor`.
2. GroupKFold cross-validation (5 folds) strictly grouped by `company_name`
   to ensure the model generalizes to unseen employers.
3. Evaluates 4 architectures: GBM, Random Forest, Logistic Regression, Stacking.
4. Fits Platt probability calibration on out-of-fold predictions.
5. Benchmarks all models on the 180-listing holdout Gold Standard set.
6. Computes authentic TreeSHAP feature attributions.
7. Saves models, diagnostics, and final calibrated predictions.
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd

# Add workspace root to sys.path
sys.path.insert(0, os.path.abspath("."))

from src.models.leakage_free_features import LeakageFreeFeatureExtractor
from src.models.classifiers import NumPyGradientBoosting, NumPyRandomForest, NumPyLogisticRegression, NumPyStackingClassifier
from src.models.calibration import PlattCalibrator, compute_calibration_metrics
from src.models.shap_explainer import AuthenticTreeSHAP

def compute_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.50) -> dict:
    y_pred = (y_prob >= threshold).astype(int)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    
    acc = (tp + tn) / max(1, len(y_true))
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2.0 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
    
    # Mann-Whitney U exact ROC-AUC
    n1 = int(np.sum(y_true == 1))
    n0 = int(np.sum(y_true == 0))
    if n1 == 0 or n0 == 0:
        auc = 0.5
    else:
        ranks = np.argsort(np.argsort(y_prob)) + 1
        auc = (np.sum(ranks[y_true == 1]) - n1 * (n1 + 1) / 2.0) / (n0 * n1)
        
    return {
        "ROC-AUC": round(float(auc), 4),
        "F1 Score": round(float(f1), 4),
        "Precision": round(float(prec), 4),
        "Recall": round(float(rec), 4),
        "Accuracy": round(float(acc), 4)
    }

def run_group_kfold(df_train: pd.DataFrame, y_train: np.ndarray, n_splits: int = 5, seed: int = 42):
    """Groups folds strictly by company_name so companies in test folds are unseen in train folds."""
    rng = np.random.RandomState(seed)
    companies = np.array(df_train["company_name"].astype(str).str.lower().str.strip().unique())
    rng.shuffle(companies)
    
    splits = np.array_split(companies, n_splits)
    folds = []
    
    comp_series = df_train["company_name"].astype(str).str.lower().str.strip()
    for fold_comps in splits:
        val_mask = comp_series.isin(set(fold_comps)).values
        train_idx = np.where(~val_mask)[0]
        val_idx = np.where(val_mask)[0]
        folds.append((train_idx, val_idx))
        
    return folds

def run_pipeline():
    print("=" * 80)
    print("  NAUKRI SAAF — PRODUCTION ML PIPELINE v4 (LEAKAGE-FREE, GROUP-CV, CALIBRATED)")
    print("=" * 80)
    
    # 1. Load Data
    raw_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
    weak_path = "data/weak_supervision_labels.csv"
    gold_path = "data/gold_labeling_sheet.csv"
    
    df_raw = pd.read_csv(raw_path)
    df_weak = pd.read_csv(weak_path)
    df_gold = pd.read_csv(gold_path)
    
    # Attach Snorkel weak labels
    df_raw["target"] = df_weak["weak_label_ghost"].values
    
    # Isolate Gold Holdout Set
    gold_ids = set(df_gold["listing_id"].values)
    is_gold = df_raw["listing_id"].isin(gold_ids)
    
    train_df = df_raw[~is_gold].reset_index(drop=True)
    y_train = train_df["target"].values
    
    gold_eval_df = df_gold.merge(df_raw, on="listing_id", suffixes=("", "_raw"))
    y_gold = gold_eval_df["gold_label"].astype(int).values
    
    print(f"Dataset Partitioning:")
    print(f"  Training Set (with Snorkel weak labels): {len(train_df):,} listings ({len(train_df['company_name'].unique()):,} unique companies)")
    print(f"  Holdout Gold Standard Test Set        : {len(gold_eval_df):,} listings (hand-verified ground truth)")
    
    # 2. 5-Fold GroupKFold Cross-Validation
    print("\n[Step 1/4] Running 5-Fold GroupKFold Cross-Validation (Grouped by Company)...")
    folds = run_group_kfold(train_df, y_train, n_splits=5, seed=42)
    
    models = {
        "Gradient Boosting (GBM)": lambda: NumPyGradientBoosting(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42),
        "Random Forest (Tuned)": lambda: NumPyRandomForest(n_estimators=80, max_depth=7, min_samples_leaf=4, random_state=42),
        "Logistic Regression": lambda: NumPyLogisticRegression(lr=0.05, max_iter=300, l2_reg=0.1, class_weight="balanced")
    }
    
    oof_predictions = {name: np.zeros(len(train_df)) for name in models}
    
    for fold_num, (tr_idx, val_idx) in enumerate(folds, start=1):
        fold_train = train_df.iloc[tr_idx]
        fold_val = train_df.iloc[val_idx]
        y_tr, y_val = y_train[tr_idx], y_train[val_idx]
        
        # Fit feature extractor strictly on train fold
        fe = LeakageFreeFeatureExtractor()
        fe.fit(fold_train)
        
        X_tr = fe.transform(fold_train).values
        X_val = fe.transform(fold_val).values
        
        for name, model_factory in models.items():
            clf = model_factory()
            clf.fit(X_tr, y_tr)
            p_val = clf.predict_proba(X_val)
            oof_predictions[name][val_idx] = p_val
            
    # Stacking OOF
    stacking_oof = np.zeros(len(train_df))
    for fold_num, (tr_idx, val_idx) in enumerate(folds, start=1):
        S_tr = np.column_stack([oof_predictions[m][tr_idx] for m in models])
        S_val = np.column_stack([oof_predictions[m][val_idx] for m in models])
        meta_lr = NumPyLogisticRegression(lr=0.08, max_iter=250, l2_reg=0.2)
        meta_lr.fit(S_tr, y_train[tr_idx])
        stacking_oof[val_idx] = meta_lr.predict_proba(S_val)
    oof_predictions["Stacking Ensemble"] = stacking_oof
    
    # Calculate GroupKFold OOF Metrics
    cv_results = []
    for name, oof_probs in oof_predictions.items():
        m = compute_metrics(y_train, oof_probs)
        m["Model"] = name
        cv_results.append(m)
        
    cv_df = pd.DataFrame(cv_results)[["Model", "ROC-AUC", "F1 Score", "Precision", "Recall", "Accuracy"]].sort_values("ROC-AUC", ascending=False).reset_index(drop=True)
    cv_df.index += 1
    
    print("\n--- 5-Fold GroupKFold Out-of-Fold Leaderboard (Unseen Employers) ---")
    print(cv_df.to_string())
    os.makedirs("data", exist_ok=True)
    cv_df.to_csv("data/model_benchmark_group_cv.csv", index=False)
    
    # 3. Probability Calibration
    print("\n[Step 2/4] Fitting Platt Scaling Probability Calibration...")
    best_model_name = cv_df.iloc[0]["Model"]
    best_oof_raw = oof_predictions[best_model_name]
    
    calibrator = PlattCalibrator()
    calibrator.fit(best_oof_raw, y_train)
    cal_oof_probs = calibrator.predict_proba(best_oof_raw)
    
    cal_metrics = compute_calibration_metrics(y_train, best_oof_raw, cal_oof_probs)
    print(f"Calibration on {best_model_name}:")
    for k, v in cal_metrics.items():
        print(f"  {k:<28}: {v}")
    pd.DataFrame([cal_metrics]).to_csv("data/calibration_metrics_v4.csv", index=False)
    
    # 4. Train Full Models on Complete Training Set & Evaluate on Gold Holdout
    print("\n[Step 3/4] Retraining Full Models and Evaluating on 180 Gold Holdout Set...")
    fe_full = LeakageFreeFeatureExtractor()
    fe_full.fit(train_df)
    X_train_full = fe_full.transform(train_df).values
    X_gold_test = fe_full.transform(gold_eval_df).values
    
    fitted_models = {}
    gold_results = []
    
    for name, model_factory in models.items():
        clf = model_factory()
        clf.fit(X_train_full, y_train)
        fitted_models[name] = clf
        
        gold_probs = clf.predict_proba(X_gold_test)
        m = compute_metrics(y_gold, gold_probs)
        m["Model"] = name
        gold_results.append(m)
        
    # Calibrated best model evaluation on Gold
    best_clf = fitted_models[best_model_name]
    raw_gold_probs = best_clf.predict_proba(X_gold_test)
    cal_gold_probs = calibrator.predict_proba(raw_gold_probs)
    
    m_cal = compute_metrics(y_gold, cal_gold_probs)
    m_cal["Model"] = f"{best_model_name} (Calibrated)"
    gold_results.append(m_cal)
    
    gold_df = pd.DataFrame(gold_results)[["Model", "ROC-AUC", "F1 Score", "Precision", "Recall", "Accuracy"]].sort_values("F1 Score", ascending=False).reset_index(drop=True)
    gold_df.index += 1
    
    print("\n" + "=" * 80)
    print("  FINAL BENCHMARK: EVALUATION ON 180 HOLDOUT GOLD STANDARD LISTINGS")
    print("=" * 80)
    print(gold_df.to_string())
    gold_df.to_csv("data/model_benchmark_gold_test.csv", index=False)
    
    # 5. TreeSHAP Feature Attributions
    print("\n[Step 4/4] Computing Authentic TreeSHAP Explanations...")
    tree_model = fitted_models.get("Gradient Boosting (GBM)", fitted_models.get("Random Forest (Tuned)"))
    feature_names = fe_full.get_feature_names_out()
    
    explainer = AuthenticTreeSHAP(tree_model, feature_names)
    explainer.fit_baseline(X_train_full[:300])
    
    X_all = fe_full.transform(df_raw).values
    shap_df = explainer.explain(X_all)
    shap_df.insert(0, "listing_id", df_raw["listing_id"].values)
    
    imp_df = explainer.get_global_importance(shap_df)
    print("\n--- Top 10 TreeSHAP Feature Importances ---")
    print(imp_df.head(10).to_string(index=False))
    imp_df.to_csv("data/shap_importances_v4.csv", index=False)
    
    # 6. Generate Final Scored Predictions for all 2,851 listings
    full_raw_probs = best_clf.predict_proba(X_all)
    full_cal_probs = calibrator.predict_proba(full_raw_probs)
    
    # Find top contributing feature per listing
    shap_cols = [c for c in shap_df.columns if c.endswith("_shap")]
    top_feature_indices = np.argmax(shap_df[shap_cols].abs().values, axis=1)
    top_feature_names = [feature_names[i] for i in top_feature_indices]
    
    q60, q85 = np.percentile(full_cal_probs, [60, 85])
    
    pred_df = df_raw.copy()
    pred_df["calibrated_ghost_prob"] = full_cal_probs.round(4)
    pred_df["predicted_ghost_label"] = (full_cal_probs >= 0.50).astype(int)
    pred_df["ghost_status"] = pd.cut(
        full_cal_probs,
        bins=[-0.01, q60, q85, 1.01],
        labels=["Genuine", "Suspect", "Ghost"]
    )
    pred_df["top_shap_driver"] = top_feature_names
    
    pred_path = "data/predictions_v4.csv"
    pred_df.to_csv(pred_path, index=False)
    print(f"\nFinal calibrated predictions exported to: {pred_path}")
    print("\nGhost Status Breakdown across 2,851 listings:")
    print(pred_df["ghost_status"].value_counts())
    
    # 7. Serialize Models
    model_dir = "outputs/models"
    os.makedirs(model_dir, exist_ok=True)
    with open(f"{model_dir}/best_model_v4.pkl", "wb") as f:
        pickle.dump(best_clf, f)
    with open(f"{model_dir}/calibrator_v4.pkl", "wb") as f:
        pickle.dump(calibrator, f)
    with open(f"{model_dir}/feature_extractor_v4.pkl", "wb") as f:
        pickle.dump(fe_full, f)
        
    print(f"\nAll models, calibrators, and transformers saved to {model_dir}/")
    print("=" * 80)
    print("  PHASE 2 COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    run_pipeline()
