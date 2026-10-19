# IEEE Research & Publication Workspace

This directory contains the academic research paper, reproducible experimental testbeds, benchmark datasets, LaTeX templates, formal threat models, and submission materials for:

> **KAVACH: A Multi-Stage Security-Governed Agentic DevOps Framework with AST Supply-Chain Firewalls and Multilingual Guardrails**

## Directory Structure

```
research/
└── ieee_publication/
    ├── paper/
    │   ├── paper.tex                  # Full IEEE 2-column conference manuscript
    │   ├── references.bib             # 30+ BibTeX citations for SOTA SE & AI security
    │   ├── IEEEtran.cls               # Official IEEE LaTeX document class
    │   └── PAPER_DRAFT.md             # Complete human-readable markdown version with math
    ├── experiments/
    │   ├── run_ieee_benchmarks.py     # Master benchmark runner (generates all paper tables)
    │   ├── test_slopsquatting.py      # Experiment 1: Package hallucination & firewall defense
    │   ├── test_multilingual_pii.py   # Experiment 2: Code-mixed PII detection benchmark
    │   ├── test_ablation.py           # Experiment 3: System component ablation study
    │   └── profile_latency.py         # Experiment 4: Multi-stage latency breakdown & percentiles
    ├── datasets/
    │   ├── package_hallucination_corpus.json  # 100 real vs hallucinated PyPI packages
    │   ├── multilingual_pii_corpus.json       # 100+ code-mixed developer prompts & labels
    │   └── dependency_blast_radius.json       # Repository AST impact evaluation cases
    ├── tables/
    │   ├── table1_comparative_baselines.tex   # LaTeX Table: KAVACH vs Baselines
    │   ├── table2_ablation_study.tex          # LaTeX Table: Component Ablation
    │   └── table3_latency_breakdown.tex       # LaTeX Table: Latency Profile & Overhead
    ├── figures/
    │   ├── figure1_architecture.svg           # Vector architecture & trust boundary diagram
    │   └── figure2_latency_overhead.svg       # Overhead vs payload size chart
    ├── SUBMISSION_GUIDE.md                    # Target IEEE venues, deadlines & submission checklist
    └── README.md                              # Guide to running benchmarks & generating LaTeX
```
