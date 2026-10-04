# Model Artifacts, Dense Embeddings & Experiment Telemetry

This directory stores all serialized machine learning models, precomputed dense semantic embeddings, and reproducible experiment run logs.

---

## 📁 Directory Structure

```
outputs/
├── embeddings/
│   └── jd_dense_embeddings.npy         # 64-dimensional dense semantic LSA embeddings (2,851 x 64)
├── experiments/
│   └── run_*_random_forest.json        # Experiment telemetry, hyperparameters, and cross-validation logs
└── models/
    ├── best_model_v4.pkl               # Optimized production pure-NumPy ensemble model
    ├── calibrator_v4.pkl               # Fitted Platt sigmoid probability calibrator
    └── feature_extractor_v4.pkl        # Fitted LeakageFreeFeatureExtractor with fold priors
```

---

## 🔒 Notes on Binary Artifacts

- All models are implemented in pure, vectorized NumPy to eliminate C-extension compilation dependencies and ensure native portability across Linux, macOS, and Windows 11.
- Precomputed embeddings are generated via `src/features/nlp_pipeline.py`.
- Model checkpoints are produced via `src/models/train_pipeline.py`.
