"""
Unit Tests for NLP Feature Extraction: Embeddings, Plagiarism & Vagueness
"""

import pytest
import numpy as np
import pandas as pd
from src.features.text_embeddings import DenseSemanticEncoder
from src.features.plagiarism_detector import CrossCompanyPlagiarismDetector
from src.features.vagueness_scorer import VaguenessScorer

def test_dense_semantic_encoder():
    tech_templates = [
        "Senior Python Engineer with FastAPI and Docker experience in cloud environments.",
        "Lead Python Developer building scalable microservices and REST APIs with Docker.",
        "Full Stack Developer proficient in React, Node, Python, SQL, and Git repositories.",
        "Backend Python Engineer developing asynchronous services using Redis and Postgres.",
        "DevOps Engineer managing Kubernetes clusters, CI/CD pipelines, and Terraform infrastructure.",
        "Machine Learning Engineer building PyTorch models and deploying inference endpoints.",
        "Data Scientist utilizing Pandas, Scikit-learn, and SQL for predictive modeling.",
        "Data Engineer orchestrating Spark pipelines, Airflow DAGs, and Snowflake warehouses.",
        "Cloud Solutions Architect designing AWS serverless systems and Lambda workflows.",
        "Software Development Engineer in Test automating API benchmarks and load testing."
    ]
    biz_templates = [
        "Executive Marketing Assistant managing social media campaigns and newsletter content.",
        "Digital Marketing Specialist optimizing Google Ads and search engine rankings.",
        "Human Resources Manager handling talent acquisition, payroll, and employee onboarding.",
        "Financial Analyst preparing quarterly variance reports, P&L statements, and budgets.",
        "Senior Accountant reconciling balance sheets, general ledgers, and tax compliance.",
        "Account Executive closing enterprise B2B software sales and quota management.",
        "Sales Development Representative prospecting inbound leads and qualifying outbound accounts.",
        "Customer Success Manager driving client retention, onboarding, and platform renewal.",
        "Office Administrative Coordinator managing facility operations and travel schedules.",
        "Supply Chain Analyst optimizing inventory forecasting, logistics, and vendor contracts."
    ]
    texts = tech_templates + biz_templates
    encoder = DenseSemanticEncoder(n_components=16, min_df=1, random_state=42)
    embeddings = encoder.fit_transform(texts)
    
    # Check output shape
    assert embeddings.shape[0] == 20
    assert embeddings.shape[1] == 16
    
    # Check L2 normalization (unit length)
    norms = np.linalg.norm(embeddings, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-4)
    
    # Tech jobs should have higher similarity than Tech vs Marketing
    sim_tech = float(np.dot(embeddings[0], embeddings[1]))
    sim_cross = float(np.dot(embeddings[0], embeddings[2]))
    assert sim_tech > sim_cross

def test_cross_company_plagiarism_detector():
    df = pd.DataFrame({
        "listing_id": ["job_1", "job_2", "job_3"],
        "company_name": ["Alpha Corp", "Beta Staffing", "Alpha Corp"],
        "description_text": [
            "Identical description text for data analyst position with SQL and Python.",
            "Identical description text for data analyst position with SQL and Python.",
            "Identical description text for data analyst position with SQL and Python."
        ]
    })
    # Synthetic identical embeddings
    embeds = np.array([
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0]
    ])
    
    detector = CrossCompanyPlagiarismDetector(similarity_threshold=0.85)
    results = detector.detect(df, embeds)
    
    # Job 1 and Job 2 are different companies with identical text -> must be flagged
    assert results.loc[results["listing_id"] == "job_1", "is_syndicated_description"].iloc[0] == 1
    assert results.loc[results["listing_id"] == "job_2", "is_syndicated_description"].iloc[0] == 1

def test_vagueness_scorer():
    scorer = VaguenessScorer()
    
    tech_text = (
        "We require 4+ years of Python, SQL, PostgreSQL, Docker, AWS, and FastAPI. "
        "The engineer will architect, implement, deploy, and benchmark microservices."
    )
    buzzword_text = (
        "Looking for a rockstar ninja self-starter to join our dynamic team and hit the ground running. "
        "Must have passion for excellence and wear many hats in our fast-paced environment."
    )
    
    tech_res = scorer.score_text(tech_text)
    buzz_res = scorer.score_text(buzzword_text)
    
    assert tech_res["concrete_tech_density"] > buzz_res["concrete_tech_density"]
    assert buzz_res["buzzword_density"] > tech_res["buzzword_density"]
    assert buzz_res["jd_vagueness_index"] > tech_res["jd_vagueness_index"]
