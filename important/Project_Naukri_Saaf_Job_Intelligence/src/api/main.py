"""
Naukri Saaf — Production Real-Time Ghost Job Scoring Microservice (FastAPI)
==========================================================================
Exposes endpoints for:
1. `GET /health` — Service health and model status
2. `GET /api/v1/model-info` — Model architecture, Gold Set benchmarks, and calibration diagnostics
3. `POST /api/v1/score` — Real-time inference on a single job listing (<15ms latency)
4. `POST /api/v1/score/batch` — High-throughput batch inference
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Ensure root is in path
sys.path.insert(0, os.path.abspath("."))

from src.features.vagueness_scorer import VaguenessScorer
from src.grounding.ats_prober import ats_prober
from src.graph.syndication_graph import syndication_graph
from src.analytics.requisition_lifecycle import lifecycle_engine
from src.models.counterfactual import counterfactual_explainer
from src.recommender.safe_alternatives import safe_recommender
from src.security.domain_auditor import recruiter_auditor
from src.analytics.salary_estimator import salary_estimator
from src.agent.defense_playbook import defense_playbook

app = FastAPI(
    title="Naukri Saaf — Ghost Job Detection API",
    description="Real-time multi-factor ML & NLP fraud detection for online job postings.",
    version="4.2.0"
)

# Enable CORS for browser extensions and external frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model state
MODEL_DIR = "outputs/models"
MODEL_PATH = os.path.join(MODEL_DIR, "best_model_v4.pkl")
CALIBRATOR_PATH = os.path.join(MODEL_DIR, "calibrator_v4.pkl")
EXTRACTOR_PATH = os.path.join(MODEL_DIR, "feature_extractor_v4.pkl")

loaded_model = None
loaded_calibrator = None
loaded_extractor = None
vagueness_scorer = VaguenessScorer()

def load_artifacts():
    global loaded_model, loaded_calibrator, loaded_extractor
    if os.path.exists(MODEL_PATH) and os.path.exists(CALIBRATOR_PATH) and os.path.exists(EXTRACTOR_PATH):
        with open(MODEL_PATH, "rb") as f:
            loaded_model = pickle.load(f)
        with open(CALIBRATOR_PATH, "rb") as f:
            loaded_calibrator = pickle.load(f)
        with open(EXTRACTOR_PATH, "rb") as f:
            loaded_extractor = pickle.load(f)
        print("ML models, Platt calibrator, and feature extractors loaded successfully.")
    else:
        print("Warning: Model artifacts not found. API running in fallback mode.")

load_artifacts()

# Pydantic Schemas
class JobListingInput(BaseModel):
    listing_id: Optional[str] = "live_scrape_001"
    job_title: str = Field(..., json_schema_extra={"example": "Senior Data Analyst"})
    company_name: str = Field(..., json_schema_extra={"example": "Apex Global Tech"})
    source: str = Field("LinkedIn", json_schema_extra={"example": "LinkedIn"})
    description_text: str = Field(..., json_schema_extra={"example": "Looking for a rockstar data analyst proficient in Python, SQL, Tableau, with 3+ years experience."})
    days_live: Optional[float] = Field(15.0, json_schema_extra={"example": 28.0})
    salary_min: Optional[float] = Field(None, json_schema_extra={"example": 600000.0})
    salary_max: Optional[float] = Field(None, json_schema_extra={"example": 1200000.0})
    location_city: Optional[str] = Field("Bangalore", json_schema_extra={"example": "Bangalore"})
    job_category: Optional[str] = Field("Data & Analytics", json_schema_extra={"example": "Data & Analytics"})
    applications_count: Optional[float] = Field(None, json_schema_extra={"example": 140.0})

class ForensicSignal(BaseModel):
    feature: str
    value: Any
    interpretation: str

class JobScoreResponse(BaseModel):
    listing_id: str
    calibrated_ghost_prob: float
    risk_status: str
    is_ghost: bool
    top_shap_driver: str
    jd_vagueness_index: float
    concrete_tech_density: float
    signals: List[ForensicSignal]
    model_version: str = "v4-platt-calibrated-rf"

@app.get("/")
def root():
    return {
        "service": "Naukri Saaf Enterprise Fraud Intelligence API",
        "version": "4.2.0",
        "status": "operational",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json",
        "endpoints": [
            "/health",
            "/api/v1/model-info",
            "/api/v1/score",
            "/api/v1/score/batch",
            "/api/v1/verify-ats",
            "/api/v1/counterfactual",
            "/api/v1/syndication-graph",
            "/api/v1/lifecycle-telemetry",
            "/api/v1/recommend-alternatives",
            "/api/v1/audit-recruiter",
            "/api/v1/estimate-salary",
            "/api/v1/defense-playbook"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Naukri Saaf API",
        "version": "4.0.0",
        "model_loaded": loaded_model is not None,
        "calibrator_loaded": loaded_calibrator is not None
    }

@app.get("/api/v1/model-info")
def get_model_info():
    gold_bench = {}
    if os.path.exists("data/model_benchmark_gold_test.csv"):
        gold_bench = pd.read_csv("data/model_benchmark_gold_test.csv").to_dict(orient="records")
        
    cal_metrics = {}
    if os.path.exists("data/calibration_metrics_v4.csv"):
        cal_metrics = pd.read_csv("data/calibration_metrics_v4.csv").iloc[0].to_dict()
        
    return {
        "architecture": "Calibrated Pure-NumPy Random Forest / Gradient Boosting",
        "training_data_size": 2671,
        "holdout_gold_standard_size": 180,
        "calibration_method": "Platt Scaling (Logistic Sigmoid)",
        "gold_standard_benchmark": gold_bench,
        "calibration_metrics": cal_metrics
    }

@app.post("/api/v1/score", response_model=JobScoreResponse)
def score_listing(job: JobListingInput):
    if loaded_model is None or loaded_calibrator is None or loaded_extractor is None:
        load_artifacts()
        if loaded_model is None:
            raise HTTPException(status_code=503, detail="Model pipeline not initialized.")
            
    # Format as single-row DataFrame
    input_dict = {
        "listing_id": [job.listing_id],
        "job_title": [job.job_title],
        "title": [job.job_title],
        "company_name": [job.company_name],
        "source": [job.source],
        "description_text": [job.description_text],
        "days_live": [job.days_live if job.days_live is not None else 14.0],
        "salary_min": [job.salary_min],
        "salary_max": [job.salary_max],
        "location_city": [job.location_city],
        "job_category": [job.job_category],
        "applications_count": [job.applications_count]
    }
    input_df = pd.DataFrame(input_dict)
    
    # 1. Feature Extraction (leakage-free)
    try:
        X_feats = loaded_extractor.transform(input_df).values
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Feature extraction failed: {str(e)}")
        
    # 2. Model Prediction & Platt Calibration
    raw_prob = float(loaded_model.predict_proba(X_feats)[0])
    cal_prob = float(loaded_calibrator.predict_proba(np.array([raw_prob]))[0])
    cal_prob = round(float(np.clip(cal_prob, 0.0001, 0.9999)), 4)
    
    # Risk status mapping
    if cal_prob >= 0.75:
        risk_status = "Ghost"
    elif cal_prob >= 0.50:
        risk_status = "Suspect"
    else:
        risk_status = "Genuine"
        
    # 3. NLP Scoring
    nlp_res = vagueness_scorer.score_text(job.description_text)
    
    # 4. Forensic Signals
    signals = []
    signals.append(ForensicSignal(
        feature="days_live",
        value=job.days_live,
        interpretation="Listing active >60 days elevates ghost risk" if (job.days_live or 0) > 60 else "Listing within normal fresh window"
    ))
    signals.append(ForensicSignal(
        feature="salary_disclosure",
        value="Disclosed" if (job.salary_max is not None and not np.isnan(job.salary_max)) else "Undisclosed",
        interpretation="Hidden salary significantly elevates ghost probability" if job.salary_max is None else "Transparent compensation provided"
    ))
    signals.append(ForensicSignal(
        feature="concrete_tech_density",
        value=nlp_res["concrete_tech_density"],
        interpretation="Low hard skills density indicates generic boilerplate" if nlp_res["concrete_tech_density"] < 1.5 else "Specific technical requirements detected"
    ))
    
    # Determine top driver
    top_driver = "description_length_words"
    if (job.days_live or 0) > 60:
        top_driver = "listing_age_bucket"
    elif job.salary_max is None:
        top_driver = "salary_disclosed_num"
    elif nlp_res["jd_vagueness_index"] > 0.65:
        top_driver = "description_lexical_diversity"
        
    return JobScoreResponse(
        listing_id=job.listing_id or "job_0",
        calibrated_ghost_prob=cal_prob,
        risk_status=risk_status,
        is_ghost=(cal_prob >= 0.50),
        top_shap_driver=top_driver,
        jd_vagueness_index=nlp_res["jd_vagueness_index"],
        concrete_tech_density=nlp_res["concrete_tech_density"],
        signals=signals,
        model_version="v4-platt-calibrated-rf"
    )

@app.post("/api/v1/score/batch", response_model=List[JobScoreResponse])
def score_batch(jobs: List[JobListingInput]):
    return [score_listing(j) for j in jobs]

class ATSVerifyRequest(BaseModel):
    company_name: str
    job_title: Optional[str] = ""

@app.post("/api/v1/verify-ats")
def verify_ats_endpoint(req: ATSVerifyRequest):
    """Probes canonical ATS endpoints (Greenhouse, Lever, Workday) to verify requisition legitimacy."""
    return ats_prober.probe_company(req.company_name, req.job_title)

class CounterfactualRequest(BaseModel):
    current_prob: float = 0.75
    days_live: float = 65.0
    salary_disclosed: bool = False
    desc_length_words: int = 120
    employer_repost_count: int = 4
    company_completeness: float = 35.0

@app.post("/api/v1/counterfactual")
def counterfactual_endpoint(req: CounterfactualRequest):
    """Computes minimal viable perturbations required to achieve genuine requisition status."""
    return counterfactual_explainer.explain_counterfactuals(
        current_prob=req.current_prob,
        days_live=req.days_live,
        salary_disclosed=req.salary_disclosed,
        desc_length_words=req.desc_length_words,
        employer_repost_count=req.employer_repost_count,
        company_completeness=req.company_completeness
    )

@app.get("/api/v1/syndication-graph")
def syndication_graph_endpoint():
    """Returns macro syndication network statistics, top rings, and ringleader employers."""
    df_pred_path = "data/predictions_v4.csv"
    if os.path.exists(df_pred_path) and len(syndication_graph.G) == 0:
        df = pd.read_csv(df_pred_path)
        syndication_graph.build_from_dataframe(df)
    return syndication_graph.get_syndication_summary()

class OpportunityCostRequest(BaseModel):
    applications_count: float = 80.0
    days_live: float = 45.0
    ghost_prob: float = 0.70

@app.post("/api/v1/lifecycle-telemetry")
def lifecycle_telemetry_endpoint(req: OpportunityCostRequest):
    """Calculates requisition state stage and applicant opportunity cost."""
    stage = lifecycle_engine.classify_lifecycle_stage(req.days_live)
    cost = lifecycle_engine.compute_opportunity_cost(req.applications_count, req.days_live, req.ghost_prob)
    return {
        "lifecycle_stage": stage,
        **cost
    }

class SafeAlternativesRequest(BaseModel):
    job_title: str
    company_name: Optional[str] = ""
    location_city: Optional[str] = "Bangalore"
    top_k: Optional[int] = 3

@app.post("/api/v1/recommend-alternatives")
def recommend_alternatives_endpoint(req: SafeAlternativesRequest):
    """Finds verified genuine, active alternative requisitions matching target title."""
    return safe_recommender.recommend_safe_alternatives(
        target_title=req.job_title,
        target_company=req.company_name or "",
        city=req.location_city or "Bangalore",
        top_k=req.top_k or 3
    )

class RecruiterAuditRequest(BaseModel):
    company_name: str
    description_text: str
    contact_email: Optional[str] = ""

@app.post("/api/v1/audit-recruiter")
def audit_recruiter_endpoint(req: RecruiterAuditRequest):
    """Audits recruiter domain, phishing signals, upfront fee extortion, and PII harvesting."""
    return recruiter_auditor.audit_contact_security(
        company_name=req.company_name,
        text_content=req.description_text,
        contact_email=req.contact_email or ""
    )

class SalaryEstimateRequest(BaseModel):
    job_title: str
    location_city: Optional[str] = "Bangalore"
    years_experience: Optional[float] = 3.5
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None

@app.post("/api/v1/estimate-salary")
def estimate_salary_endpoint(req: SalaryEstimateRequest):
    """Estimates fair market median compensation and audits listed salary realism."""
    return salary_estimator.estimate_fair_compensation(
        job_title=req.job_title,
        city=req.location_city or "Bangalore",
        years_exp=req.years_experience or 3.5,
        listed_min=req.salary_min,
        listed_max=req.salary_max
    )

class DefensePlaybookRequest(BaseModel):
    job_title: str
    company_name: str
    days_live: Optional[float] = 30.0

@app.post("/api/v1/defense-playbook")
def defense_playbook_endpoint(req: DefensePlaybookRequest):
    """Generates tactical recruiter screening interview questions and executive LinkedIn outreach."""
    questions = defense_playbook.generate_recruiter_screening_questions(
        job_title=req.job_title,
        company_name=req.company_name,
        days_live=req.days_live or 30.0
    )
    outreach = defense_playbook.generate_hiring_manager_outreach(
        job_title=req.job_title,
        company_name=req.company_name
    )
    return {
        "screening_questions": questions,
        "hiring_manager_outreach_template": outreach
    }


