# IEEE Paper Submission & Overleaf Publication Guide

This guide details how to compile, review, and submit the **KAVACH** research paper to IEEE conferences and journals.

---

## 1. Quick Local Benchmark Reproduction

To reproduce all empirical results and regenerate the LaTeX tables, run:

```bash
cd "research/ieee_publication"
python experiments/run_ieee_benchmarks.py
```

This updates:
* `tables/table1_comparative_baselines.tex`
* `tables/table2_ablation_study.tex`
* `tables/table3_latency_breakdown.tex`
* `datasets/ieee_benchmark_results.json`

---

## 2. Compiling the Paper in Overleaf (Recommended)

1. Open [Overleaf](https://www.overleaf.com/) and create a **New Project $\rightarrow$ Blank Project**.
2. Upload the following files from `research/ieee_publication/`:
   * `paper/paper.tex` (set as Main document)
   * `paper/references.bib`
   * `tables/table1_comparative_baselines.tex`
   * `tables/table2_ablation_study.tex`
   * `tables/table3_latency_breakdown.tex`
3. Click **Recompile**.
4. Overleaf will render the two-column IEEE PDF matching official publication standards.

---

## 3. Recommended IEEE Publication Venues

| Venue | Focus / Track | Why KAVACH is a Perfect Fit | Review Timeline |
| :--- | :--- | :--- | :--- |
| **IEEE SecDev** *(IEEE Secure Development Conference)* | Secure DevOps, static analysis, LLM agent security | Specifically solicits tooling that secures software pipelines and developer workflows. | Annual (Spring/Fall cycle) |
| **IEEE COMPSAC** *(Computers, Software, and Applications)* | AI & Autonomous Software Engineering | Highly receptive to agentic workflows, software architectures, and automated testing. | Annual (Submissions ~Dec-Jan) |
| **IEEE/ACM ICSE-SEIP** *(Software Engineering in Practice)* | Industrial and applied software engineering | Values working prototypes, real benchmarks, and developer productivity metrics over pure theory. | Annual (Submissions ~Oct-Nov) |
| **IEEE Access** *(High Impact Open Access Journal)* | Software Engineering / Applied AI Security | Fast-track 4–6 week peer review. Ideal if you need an indexed Scopus/SCI publication quickly. | Rolling submissions (year-round) |
| **COMSNETS** *(Security & Privacy Track)* | India premier systems and networking conference | Directly values the DPDP Act 2023 compliance and code-mixed evaluation. | Annual (Submissions ~Sept-Oct) |

---

## 4. Pre-Submission Reviewer Checklist

Before final submission to EasyChair / IEEE Author Portal:
- [x] **Formal Threat Model**: Explicitly defined under STRIDE and OWASP Top 10 for LLMs 2025.
- [x] **Governing Equations**: Multi-factor dynamic risk score and hybrid blast-radius metrics formatted in LaTeX.
- [x] **Controlled Baselines**: Compared against Raw Gemini 1.5, Heuristic Stdlib, and Microsoft Presidio.
- [x] **Ablation Study**: 5 distinct architectural configurations evaluated across safety and validity.
- [x] **Latency Profile**: P50, P90, P99 microbenchmarks demonstrating $<47$ ms overhead.
- [x] **Intellectual Honesty**: Documented limitations regarding bare numeric sequence disambiguation.
- [x] **Double-Blind Check**: If the venue enforces double-blind review (e.g., IEEE SecDev), temporarily replace author names and GitHub URL with `[Anonymous for Peer Review]`.
