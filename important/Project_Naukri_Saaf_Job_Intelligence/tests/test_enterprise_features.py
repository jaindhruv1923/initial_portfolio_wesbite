"""
Enterprise Feature Test Suite
=============================
Tests ATS Verification Prober, Heterogeneous Syndication Graph,
Requisition Lifecycle Telemetry, and Counterfactual Explainer.
"""

import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from src.grounding.ats_prober import ats_prober
from src.graph.syndication_graph import syndication_graph
from src.analytics.requisition_lifecycle import lifecycle_engine
from src.models.counterfactual import counterfactual_explainer
from src.recommender.safe_alternatives import safe_recommender
from src.security.domain_auditor import recruiter_auditor
from src.analytics.salary_estimator import salary_estimator
from src.agent.defense_playbook import defense_playbook
from src.api.main import app

client = TestClient(app)

def test_ats_prober_enterprise_and_agency():
    # Enterprise authenticated ATS
    res_uber = ats_prober.probe_company("Uber", "Data Scientist")
    assert res_uber["is_grounded"] is True
    assert res_uber["grounding_confidence"] >= 0.80
    assert "Greenhouse" in res_uber["ats_provider"]

    # Third-party agency
    res_agency = ats_prober.probe_company("Apex Staffing & Recruitment Solutions", "Java Developer")
    assert res_agency["is_grounded"] is False
    assert res_agency["grounding_confidence"] <= 0.40
    assert "Third-Party" in res_agency["verification_status"]

def test_syndication_graph_construction():
    mock_df = pd.DataFrame([
        {"company_name": "Company Alpha", "location_city": "Bangalore", "job_category": "Tech"},
        {"company_name": "Company Beta", "location_city": "Bangalore", "job_category": "Tech"},
        {"company_name": "Company Gamma", "location_city": "Mumbai", "job_category": "Sales"}
    ])
    G = syndication_graph.build_from_dataframe(mock_df)
    assert G.number_of_nodes() >= 3
    summary = syndication_graph.get_syndication_summary()
    assert "employer_nodes_count" in summary
    nodes, edges = syndication_graph.get_network_plot_data(max_nodes=10)
    assert isinstance(nodes, list)

def test_requisition_lifecycle_and_cost():
    # Stage classification
    stage_fresh = lifecycle_engine.classify_lifecycle_stage(days_live=10, repost_count=1)
    assert stage_fresh == "Fresh / Active"

    stage_ghost = lifecycle_engine.classify_lifecycle_stage(days_live=140, repost_count=5)
    assert stage_ghost == "Phantom / Ghost"

    # Opportunity cost computation
    cost = lifecycle_engine.compute_opportunity_cost(applications_count=100, days_live=90, ghost_prob=0.80)
    assert cost["wasted_applicants"] == 80
    assert cost["hours_wasted"] > 0
    assert cost["economic_loss_inr"] > 0

def test_counterfactual_explainer():
    res = counterfactual_explainer.explain_counterfactuals(
        current_prob=0.85,
        days_live=95.0,
        salary_disclosed=False,
        desc_length_words=110,
        employer_repost_count=5,
        company_completeness=25.0
    )
    assert res["initial_calibrated_prob"] == 0.85
    assert len(res["individual_counterfactuals"]) >= 3
    assert res["best_attainable_prob"] < 0.85
    assert "attainable_status" in res

def test_new_api_endpoints():
    # ATS Verify Endpoint
    r_ats = client.post("/api/v1/verify-ats", json={"company_name": "Razorpay", "job_title": "Backend Engineer"})
    assert r_ats.status_code == 200
    assert r_ats.json()["is_grounded"] is True

    # Counterfactual Endpoint
    r_cf = client.post("/api/v1/counterfactual", json={
        "current_prob": 0.78,
        "days_live": 75.0,
        "salary_disclosed": False,
        "desc_length_words": 130,
        "employer_repost_count": 3,
        "company_completeness": 30.0
    })
    assert r_cf.status_code == 200
    assert r_cf.json()["best_attainable_prob"] < 0.78

    # Lifecycle Telemetry Endpoint
    r_life = client.post("/api/v1/lifecycle-telemetry", json={
        "applications_count": 120.0,
        "days_live": 65.0,
        "ghost_prob": 0.75
    })
    assert r_life.status_code == 200
    assert "hours_wasted" in r_life.json()

def test_safe_alternative_recommender():
    alts = safe_recommender.recommend_safe_alternatives(
        target_title="Data Scientist",
        target_company="Random Nonexistent Firm",
        city="Bangalore",
        top_k=3
    )
    assert isinstance(alts, list)
    if len(alts) > 0:
        assert "job_title" in alts[0]
        assert "company_name" in alts[0]

def test_recruiter_security_auditor():
    # Phishing / upfront fee scam text
    scam_text = "Urgent opening! Send registration fee of 5000 INR to WhatsApp 9876543210. Email: hr@uber-careers.in"
    res = recruiter_auditor.audit_contact_security("Uber", scam_text)
    assert res["verdict"] in ("DANGEROUS", "SUSPICIOUS")
    assert res["threat_risk_score"] >= 50
    assert len(res["security_flags"]) >= 2

    # Clean authentic text
    clean_text = "Apply on official careers portal. Requirements: Python, SQL. Equal opportunity employer."
    res_clean = recruiter_auditor.audit_contact_security("Google", clean_text)
    assert res_clean["verdict"] == "SAFE"

def test_salary_fair_pay_estimator():
    # Undisclosed salary estimation
    est = salary_estimator.estimate_fair_compensation(
        job_title="Senior Machine Learning Engineer",
        city="Bangalore",
        years_exp=4.0
    )
    assert est["estimated_median_lpa"] > 10.0
    assert est["estimated_p75_lpa"] > est["estimated_p25_lpa"]

    # Clickbait spread audit
    est_spread = salary_estimator.estimate_fair_compensation(
        job_title="Data Analyst",
        city="Pune",
        years_exp=2.0,
        listed_min=300000.0,
        listed_max=2000000.0
    )
    assert est_spread["is_realistic_range"] is False
    assert est_spread["salary_spread_ratio"] > 3.5

def test_defense_playbook_engine():
    qs = defense_playbook.generate_recruiter_screening_questions(
        job_title="Backend Engineer",
        company_name="Acme Corp",
        days_live=45.0
    )
    assert len(qs) == 5
    assert "green_flag_answer" in qs[0]
    assert "red_flag_answer" in qs[0]

    outreach = defense_playbook.generate_hiring_manager_outreach(
        job_title="Backend Engineer",
        company_name="Acme Corp"
    )
    assert "Acme Corp" in outreach
    assert "Backend Engineer" in outreach

def test_candidate_defense_api_endpoints():
    # Recommend Alternatives
    r_alt = client.post("/api/v1/recommend-alternatives", json={
        "job_title": "Software Engineer",
        "company_name": "Unknown Entity",
        "location_city": "Bangalore",
        "top_k": 2
    })
    assert r_alt.status_code == 200

    # Audit Recruiter
    r_sec = client.post("/api/v1/audit-recruiter", json={
        "company_name": "Apex Staffing",
        "description_text": "Send CV to apex@gmail.com on WhatsApp"
    })
    assert r_sec.status_code == 200
    assert "security_grade" in r_sec.json()

    # Estimate Salary
    r_sal = client.post("/api/v1/estimate-salary", json={
        "job_title": "Full Stack Developer",
        "location_city": "Hyderabad",
        "years_experience": 3.0
    })
    assert r_sal.status_code == 200
    assert "estimated_median_lpa" in r_sal.json()

    # Defense Playbook
    r_play = client.post("/api/v1/defense-playbook", json={
        "job_title": "Data Engineer",
        "company_name": "Stripe",
        "days_live": 20.0
    })
    assert r_play.status_code == 200
    assert len(r_play.json()["screening_questions"]) == 5

