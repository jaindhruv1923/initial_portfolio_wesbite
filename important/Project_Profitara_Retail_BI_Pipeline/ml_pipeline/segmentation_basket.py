import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2
from mlxtend.frequent_patterns import apriori, association_rules

DATA_PATH = os.path.join("data", "real", "online_retail_II.csv")
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "figures"), exist_ok=True)

SEED = 42

def load_and_prep_data(path=DATA_PATH):
    print(f"[Segmentation] Loading data from {path}...")
    df = pd.read_csv(path)
    df = df.dropna(subset=["CustomerID", "Description"]).copy()
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    # Filter positive transactions and exclude administrative items
    admin_items = ["POST", "D", "M", "CRUK", "BANK CHARGES", "DOT"]
    df = df[~df["StockCode"].isin(admin_items)]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
    return df

def build_rfm_table(df):
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("CustomerID").agg(
        recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        frequency=("InvoiceNo", "nunique"),
        monetary=("TotalAmount", "sum"),
        tenure=("InvoiceDate", lambda x: (snapshot_date - x.min()).days)
    ).reset_index()
    return rfm

def compute_silhouette_sample(X, labels, sample_size=1500, seed=SEED):
    # Pure numpy/scipy silhouette score estimation
    rng = np.random.RandomState(seed)
    n = len(X)
    if n > sample_size:
        idx = rng.choice(n, size=sample_size, replace=False)
        X = X[idx]
        labels = labels[idx]
    
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        return 0.0

    sil_values = []
    for i, x in enumerate(X):
        l_curr = labels[i]
        # a(i): mean intra-cluster distance
        same_mask = (labels == l_curr)
        if np.sum(same_mask) <= 1:
            sil_values.append(0.0)
            continue
        dists_same = np.linalg.norm(X[same_mask] - x, axis=1)
        a_i = np.sum(dists_same) / (np.sum(same_mask) - 1)

        # b(i): min mean distance to other clusters
        b_i = float("inf")
        for other_l in unique_labels:
            if other_l == l_curr:
                continue
            other_mask = (labels == other_l)
            dists_other = np.linalg.norm(X[other_mask] - x, axis=1)
            mean_dist = np.mean(dists_other)
            if mean_dist < b_i:
                b_i = mean_dist
        
        sil = (b_i - a_i) / max(a_i, b_i, 1e-12)
        sil_values.append(sil)
    return float(np.mean(sil_values))

def evaluate_kmeans(rfm):
    print("[Segmentation] Evaluating K-Means for k in range 2 to 7...")
    # Standardize log-transformed RFM features for robust geometric clustering
    X_log = np.log1p(rfm[["recency", "frequency", "monetary"]].values)
    mean_X = np.mean(X_log, axis=0)
    std_X = np.std(X_log, axis=0)
    X_scaled = (X_log - mean_X) / std_X

    k_results = []
    seeds = [42, 100, 2024, 7, 999]

    for k in range(2, 8):
        inertias = []
        seed_labels = []
        for s in seeds:
            np.random.seed(s)
            centroids, labels = kmeans2(X_scaled, k, minit="points", iter=25)
            # Inertia: sum of squared distances to closest centroid
            dists = np.sum((X_scaled - centroids[labels]) ** 2)
            inertias.append(dists)
            seed_labels.append(labels)

        mean_inertia = float(np.mean(inertias))
        inertia_std = float(np.std(inertias))
        # Compute silhouette on primary seed
        sil = compute_silhouette_sample(X_scaled, seed_labels[0])
        
        # Stability metric: Pairwise agreement (Rand index equivalent) across seeds
        pair_agreements = []
        for s1 in range(len(seeds)):
            for s2 in range(s1 + 1, len(seeds)):
                # Fraction of pairs grouped similarly
                n_sample = 300
                sub_idx = np.random.choice(len(X_scaled), n_sample, replace=False)
                sub_l1 = seed_labels[s1][sub_idx]
                sub_l2 = seed_labels[s2][sub_idx]
                m1 = sub_l1[:, None] == sub_l1[None, :]
                m2 = sub_l2[:, None] == sub_l2[None, :]
                agree = np.mean(m1 == m2)
                pair_agreements.append(agree)
        stability = float(np.mean(pair_agreements))

        print(f"  k={k}: Inertia={mean_inertia:,.1f} (std={inertia_std:.1f}), Silhouette={sil:.3f}, Seed Stability={stability:.3f}")
        k_results.append({
            "k": k,
            "mean_inertia": round(mean_inertia, 1),
            "inertia_std": round(inertia_std, 1),
            "silhouette_score": round(sil, 3),
            "seed_stability": round(stability, 3)
        })

    k_df = pd.DataFrame(k_results)
    k_eval_path = os.path.join(OUTPUT_DIR, "kmeans_k_evaluation.csv")
    k_df.to_csv(k_eval_path, index=False)

    # Plot Elbow and Silhouette curves
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(k_df["k"], k_df["mean_inertia"], marker="o", color="#146B5E", lw=2)
    axes[0].set_title("Elbow Curve: Inertia vs k", fontweight="bold")
    axes[0].set_xlabel("Number of Clusters (k)")
    axes[0].set_ylabel("Inertia (Sum of Squared Distances)")

    axes[1].plot(k_df["k"], k_df["silhouette_score"], marker="s", color="#C98A2E", lw=2)
    axes[1].axvline(4, color="red", ls="--", label="Selected k=4 (Operational Granularity)")
    axes[1].set_title("Silhouette Score vs k", fontweight="bold")
    axes[1].set_xlabel("Number of Clusters (k)")
    axes[1].set_ylabel("Silhouette Score")
    axes[1].legend()

    plt.tight_layout()
    chart_p = os.path.join(OUTPUT_DIR, "figures", "kmeans_elbow_silhouette.png")
    plt.savefig(chart_p, dpi=150)
    plt.close()
    print(f"[Segmentation] Saved K-Means evaluation plot to: {chart_p}")

    # Fit Chosen k=4 model for operational business segmentation
    best_k = 4
    np.random.seed(SEED)
    centroids, labels = kmeans2(X_scaled, best_k, minit="points", iter=30)
    rfm["cluster"] = labels

    # Profile segments by mean values
    profile = rfm.groupby("cluster").agg(
        customers=("CustomerID", "count"),
        mean_recency=("recency", "mean"),
        median_recency=("recency", "median"),
        mean_frequency=("frequency", "mean"),
        mean_monetary=("monetary", "mean"),
        total_revenue=("monetary", "sum")
    ).reset_index()
    profile["revenue_share_pct"] = (profile["total_revenue"] / profile["total_revenue"].sum() * 100).round(1)

    # Label clusters based on RFM profile
    # Sort by monetary descending
    ranked = profile.sort_values("mean_monetary", ascending=False).reset_index(drop=True)
    labels_map = {}
    actions_map = {}

    for idx, row in ranked.iterrows():
        c_id = int(row["cluster"])
        if idx == 0:
            labels_map[c_id] = "Champions & VIPs"
            actions_map[c_id] = "Exclusive loyalty perks, early access, no heavy discounting"
        elif idx == 1:
            labels_map[c_id] = "Loyal & Steady Buyers"
            actions_map[c_id] = "Cross-sell relevant categories, subscription/recurring reminders"
        elif idx == 2:
            labels_map[c_id] = "At-Risk / Lapsing Spenders"
            actions_map[c_id] = "Targeted win-back outreach, proactive survey on why inactive"
        else:
            labels_map[c_id] = "Hibernating / Low-Value Inactive"
            actions_map[c_id] = "Low-cost automated re-engagement, exclude from high-cost ads"

    profile["segment_name"] = profile["cluster"].map(labels_map)
    profile["recommended_action"] = profile["cluster"].map(actions_map)
    rfm["segment_name"] = rfm["cluster"].map(labels_map)

    profile_path = os.path.join(OUTPUT_DIR, "customer_segment_profiles.csv")
    profile.round(2).to_csv(profile_path, index=False)
    print("\n" + "="*85)
    print(profile[["segment_name", "customers", "revenue_share_pct", "mean_recency", "mean_frequency", "mean_monetary"]].to_string(index=False))
    print("="*85)
    print(f"[Segmentation] Saved customer segment profiles to: {profile_path}")

    # Export customer assignments
    rfm_export = rfm[["CustomerID", "recency", "frequency", "monetary", "cluster", "segment_name"]].copy()
    rfm_path = os.path.join(OUTPUT_DIR, "rfm_segmented_customers.csv")
    rfm_export.to_csv(rfm_path, index=False)
    print(f"[Segmentation] Exported segmented customers to: {rfm_path}")

    return k_df, profile, rfm

def run_market_basket_analysis(df):
    print("\n[Market Basket] Running Apriori Market Basket Analysis on Real Retail Transactions...")
    
    # Filter to top products to avoid sparse memory explosion (keep products bought >= 200 times)
    top_items = df["Description"].value_counts()[lambda x: x >= 200].index
    filtered_df = df[df["Description"].isin(top_items)].copy()
    print(f"[Market Basket] Filtered to top {len(top_items)} frequently purchased items across {filtered_df['InvoiceNo'].nunique():,} invoices.")

    # Create one-hot basket matrix
    basket = (filtered_df.groupby(["InvoiceNo", "Description"])["Quantity"]
              .sum().unstack().fillna(0))
    basket_bool = (basket > 0)

    # Test Apriori at min_support = 0.015 (1.5% of baskets)
    print("[Market Basket] Mining frequent itemsets (min_support = 0.015)...")
    frequent_itemsets = apriori(basket_bool, min_support=0.015, use_colnames=True)
    print(f"[Market Basket] Frequent itemsets discovered: {len(frequent_itemsets)}")

    # Extract association rules with min_lift = 1.2
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
    rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)
    print(f"[Market Basket] Association rules discovered: {len(rules)}")

    # Format human-readable rules
    rules["antecedent_item"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
    rules["consequent_item"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))
    rules["rule_expression"] = rules["antecedent_item"] + "  ===>  " + rules["consequent_item"]

    surviving = rules[[
        "rule_expression", "support", "confidence", "lift", "leverage", "conviction"
    ]].copy()

    rules_path = os.path.join(OUTPUT_DIR, "apriori_surviving_rules.csv")
    surviving.round(3).to_csv(rules_path, index=False)
    print("\nTop 10 Association Rules by Lift:")
    print(surviving.head(10).round(3).to_string(index=False))
    print(f"\n[Market Basket] Saved surviving rules to: {rules_path}")

    # Plot top rules by lift
    top10 = surviving.head(10).copy()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top10["rule_expression"][::-1], top10["lift"][::-1], color="#146B5E")
    ax.set_xlabel("Lift Ratio (Strength of Association)")
    ax.set_title("Top 10 Cross-Sell Rules by Statistical Lift (UCI Online Retail)", fontweight="bold")
    plt.tight_layout()
    chart_p = os.path.join(OUTPUT_DIR, "figures", "apriori_top_rules.png")
    plt.savefig(chart_p, dpi=150)
    plt.close()
    print(f"[Market Basket] Saved cross-sell rules chart to: {chart_p}")

    return surviving

def run_segmentation_basket_pipeline():
    df = load_and_prep_data()
    rfm = build_rfm_table(df)
    k_df, profile, rfm_seg = evaluate_kmeans(rfm)
    rules = run_market_basket_analysis(df)
    return profile, rules

if __name__ == "__main__":
    run_segmentation_basket_pipeline()
