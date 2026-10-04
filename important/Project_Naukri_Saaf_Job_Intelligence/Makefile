# Naukri Saaf — Project Automation Makefile
.PHONY: help setup test run_pipeline validate api app clean docker_up docker_down

help:
	@echo "Available commands:"
	@echo "  make setup         - Install all project dependencies"
	@echo "  make test          - Run pytest test suite and coverage gates"
	@echo "  make run_pipeline  - Execute full ML, NLP, and Survival analysis pipelines"
	@echo "  make validate      - Run Pandera schema validation and PSI drift detector"
	@echo "  make api           - Start FastAPI scoring microservice (port 8000)"
	@echo "  make app           - Start Streamlit analytics dashboard (port 8501)"
	@echo "  make docker_up     - Launch Docker containers for API and Dashboard"
	@echo "  make docker_down   - Stop Docker containers"
	@echo "  make clean         - Clean bytecode and cached test files"

setup:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest -v tests/ --cov=src --cov-report=term-missing

run_pipeline:
	python src/labeling/evaluate_labels.py
	python src/models/train_pipeline.py
	python src/features/nlp_pipeline.py
	python src/agent/benchmark.py
	python src/analytics/listing_age_analysis.py
	python scripts/test_live_api.py

validate:
	python src/monitoring/data_validation.py
	python src/monitoring/drift_detector.py

api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

app:
	streamlit run 05_Streamlit_Dashboard/app.py

docker_up:
	docker compose up --build -d

docker_down:
	docker compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
