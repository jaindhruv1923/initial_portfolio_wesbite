"""
Local Experiment Tracking & Artifact Versioning Engine
======================================================
Logs every ML run with hyperparameters, random seed, training data SHA256 hash,
5-fold GroupKFold cross-validation metrics, holdout Gold set benchmarks,
and serializes reproducible model metadata.
"""

import os
import json
import hashlib
import time
from typing import Dict, Any

class LocalExperimentTracker:
    def __init__(self, experiment_name: str = "naukri_saaf_ghost_detection", tracking_dir: str = "outputs/experiments"):
        self.experiment_name = experiment_name
        self.tracking_dir = tracking_dir
        os.makedirs(self.tracking_dir, exist_ok=True)

    @staticmethod
    def compute_file_hash(filepath: str) -> str:
        """Computes SHA256 hash of a dataset to guarantee lineage."""
        if not os.path.exists(filepath):
            return "file_not_found"
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def log_run(
        self,
        run_name: str,
        model_type: str,
        hyperparameters: Dict[str, Any],
        cv_metrics: Dict[str, float],
        gold_metrics: Dict[str, float],
        dataset_path: str = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv",
        seed: int = 42
    ) -> str:
        run_id = f"run_{int(time.time())}_{model_type.lower().replace(' ', '_')}"
        data_hash = self.compute_file_hash(dataset_path)
        
        record = {
            "run_id": run_id,
            "run_name": run_name,
            "experiment": self.experiment_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "seed": seed,
            "data_lineage": {
                "dataset_path": dataset_path,
                "dataset_sha256": data_hash
            },
            "model_type": model_type,
            "hyperparameters": hyperparameters,
            "group_cv_metrics": cv_metrics,
            "holdout_gold_metrics": gold_metrics,
            "status": "COMPLETED"
        }
        
        run_path = os.path.join(self.tracking_dir, f"{run_id}.json")
        with open(run_path, "w") as f:
            json.dump(record, f, indent=2)
            
        print(f"Logged experiment run [{run_id}] to: {run_path}")
        return run_id

if __name__ == "__main__":
    tracker = LocalExperimentTracker()
    tracker.log_run(
        run_name="Production V4 Tuned Random Forest + Platt Calibration",
        model_type="Random Forest (Calibrated)",
        hyperparameters={"n_estimators": 80, "max_depth": 7, "min_samples_leaf": 4},
        cv_metrics={"ROC-AUC": 0.9961, "F1": 0.9638, "Recall": 0.9864, "Precision": 0.9421},
        gold_metrics={"ROC-AUC": 0.9200, "F1": 0.6949, "Recall": 0.9318, "Precision": 0.5541}
    )
