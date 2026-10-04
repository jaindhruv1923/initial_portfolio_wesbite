"""
Advanced NLP Feature Engineering Pipeline
=========================================
Executes:
1. Dense Semantic Embedding Extraction (Zero-Dependency Randomized SVD / LSA)
2. Cross-Company Description Plagiarism & Syndication Detection
3. Syntactic & Semantic JD Vagueness Scoring
4. Exports verified data artifacts for modeling and analytics.
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath("."))

from src.features.text_embeddings import DenseSemanticEncoder
from src.features.plagiarism_detector import CrossCompanyPlagiarismDetector
from src.features.vagueness_scorer import VaguenessScorer

def run_nlp_pipeline():
    print("=" * 80)
    print("  NAUKRI SAAF — ADVANCED NLP FEATURE EXTRACTION & PLAGIARISM PIPELINE")
    print("=" * 80)
    
    # 1. Load Data
    raw_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
    pred_path = "data/predictions_v4.csv"
    
    if os.path.exists(pred_path):
        df = pd.read_csv(pred_path)
    else:
        df = pd.read_csv(raw_path)
        
    print(f"Loaded {len(df):,} job listings for NLP processing.")
    
    # 2. Extract Dense Semantic Embeddings
    print("\n[Step 1/3] Extracting 64-dimensional Dense Semantic Embeddings (Randomized SVD)...")
    descriptions = df["description_text"].fillna("").astype(str).tolist()
    
    encoder = DenseSemanticEncoder(n_components=64, max_features=4000, min_df=3, random_state=42)
    embeddings = encoder.fit_transform(descriptions)
    
    os.makedirs("outputs/embeddings", exist_ok=True)
    embed_path = "outputs/embeddings/jd_dense_embeddings.npy"
    np.save(embed_path, embeddings)
    print(f"  Vocabulary size: {len(encoder.vocab):,} unigrams & bigrams")
    print(f"  Dense embedding matrix shape: {embeddings.shape}")
    print(f"  Saved embeddings to: {embed_path}")
    
    # 3. Detect Cross-Company Description Plagiarism
    print("\n[Step 2/3] Detecting Cross-Company Description Plagiarism / Syndication...")
    detector = CrossCompanyPlagiarismDetector(similarity_threshold=0.85)
    plag_df = detector.detect(df, embeddings)
    
    n_syndicated = int(plag_df["is_syndicated_description"].sum())
    syndicated_pct = (n_syndicated / len(df)) * 100.0
    print(f"  Listings with syndicated cross-company descriptions (>=0.85 cos-sim): {n_syndicated:,} ({syndicated_pct:.2f}%)")
    
    # Analyze overlap with ghost status if present
    if "ghost_status" in df.columns:
        print("\n  Syndication Rate by Ghost Status Tier:")
        syn_breakdown = pd.crosstab(df["ghost_status"], plag_df["is_syndicated_description"], normalize="index") * 100.0
        print(syn_breakdown.round(2).to_string())
        
    plag_out_path = "data/cross_company_plagiarism.csv"
    plag_df.to_csv(plag_out_path, index=False)
    print(f"  Exported plagiarism records to: {plag_out_path}")
    
    # 4. Score Job Description Vagueness & Fluff
    print("\n[Step 3/3] Scoring Job Description Vagueness & Corporate Buzzwords...")
    scorer = VaguenessScorer()
    vagueness_df = scorer.score_dataframe(df, text_col="description_text")
    
    avg_vagueness = vagueness_df["jd_vagueness_index"].mean()
    avg_tech_density = vagueness_df["concrete_tech_density"].mean()
    avg_buzzword_density = vagueness_df["buzzword_density"].mean()
    
    print(f"  Average JD Vagueness Index: {avg_vagueness:.3f} (scale 0-1)")
    print(f"  Average Concrete Tech Density: {avg_tech_density:.2f} entities per 100 words")
    print(f"  Average Buzzword Density: {avg_buzzword_density:.2f} buzzwords per 100 words")
    
    vagueness_out_path = "data/jd_vagueness_metrics.csv"
    vagueness_df.to_csv(vagueness_out_path, index=False)
    print(f"  Exported vagueness metrics to: {vagueness_out_path}")
    
    # 5. Build Combined NLP Augmented Feature Set
    print("\n[Summary] Merging NLP Features into Augmented Dataset...")
    nlp_merged = df.copy()
    nlp_merged["cross_company_max_sim"] = plag_df["cross_company_max_sim"]
    nlp_merged["cross_company_plag_count"] = plag_df["cross_company_plag_count"]
    nlp_merged["is_syndicated_description"] = plag_df["is_syndicated_description"]
    nlp_merged["most_similar_company"] = plag_df["most_similar_company"]
    
    nlp_merged["concrete_tech_density"] = vagueness_df["concrete_tech_density"]
    nlp_merged["buzzword_density"] = vagueness_df["buzzword_density"]
    nlp_merged["concrete_to_vague_verb_ratio"] = vagueness_df["concrete_to_vague_verb_ratio"]
    nlp_merged["bullet_point_density"] = vagueness_df["bullet_point_density"]
    nlp_merged["jd_vagueness_index"] = vagueness_df["jd_vagueness_index"]
    
    augmented_path = "data/nlp_augmented_features.csv"
    nlp_merged.to_csv(augmented_path, index=False)
    print(f"  NLP-augmented feature dataset exported to: {augmented_path}")
    print("=" * 80)
    print("  PHASE 3 COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    run_nlp_pipeline()
