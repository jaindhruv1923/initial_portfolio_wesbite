"""
Integration Tests for FastAPI Microservice Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["version"] == "4.0.0"

def test_model_info_endpoint():
    resp = client.get("/api/v1/model-info")
    assert resp.status_code == 200
    data = resp.json()
    assert "calibration_method" in data
    assert "training_data_size" in data

def test_score_single_listing():
    payload = {
        "listing_id": "test_lead_01",
        "job_title": "Senior Data Scientist",
        "company_name": "Acme Innovations",
        "source": "LinkedIn",
        "description_text": "Hiring a Senior Data Scientist skilled in Python, PyTorch, SQL, and Docker to build machine learning models.",
        "days_live": 12.0,
        "salary_min": 1800000.0,
        "salary_max": 2800000.0,
        "location_city": "Bangalore"
    }
    resp = client.post("/api/v1/score", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "calibrated_ghost_prob" in data
    assert 0.0 <= data["calibrated_ghost_prob"] <= 1.0
    assert data["risk_status"] in ["Genuine", "Suspect", "Ghost"]
    assert "top_shap_driver" in data
    assert "signals" in data

def test_score_batch_listings():
    jobs = [
        {
            "listing_id": "job_a",
            "job_title": "Frontend Engineer",
            "company_name": "Web Solutions",
            "source": "Indeed",
            "description_text": "React, TypeScript, CSS frontend developer.",
            "days_live": 5.0
        },
        {
            "listing_id": "job_b",
            "job_title": "Urgent Rockstar Intern",
            "company_name": "Ghost Recruiting",
            "source": "Glassdoor",
            "description_text": "Immediate joining urgent hiring rockstar ninja for dynamic team.",
            "days_live": 120.0
        }
    ]
    resp = client.post("/api/v1/score/batch", json=jobs)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert data[0]["listing_id"] == "job_a"
    assert data[1]["listing_id"] == "job_b"
    # Stale buzzword posting should have higher ghost probability
    assert data[1]["calibrated_ghost_prob"] >= data[0]["calibrated_ghost_prob"]
