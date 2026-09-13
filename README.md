# Fraud Detection Platform

Real-time transaction fraud detection — Problem 1 of a multi-project bank-breadth portfolio strategy, built on real, independently-verified data with a zero-fabrication policy: every metric below traces to code that was actually executed against a real dataset, never estimated or illustrative unless explicitly labeled ASSUMPTION.

## Real headline results

| Metric | Value | Basis |
|---|---|---|
| Champion model | CatBoost | Highest Stage A PR-AUC, confirmed in Stage B CV |
| Champion 5-fold CV PR-AUC | 0.8482 (95% bootstrap CI 0.8162–0.8784) | MEASURED |
| Runner-up (RandomForest) CV PR-AUC | 0.8448 (95% CI 0.8150–0.8739) | MEASURED |
| Temporal-split PR-AUC | 0.7692 | MEASURED — honest, held-out-in-time |
| Cost-optimal threshold | 0.0443 | MEASURED, vectorized O(n log n) search |
| Real precision / recall (OOF) | 69.64% / 82.52% | MEASURED |
| Savings vs. no-model baseline | €199,450.76 | MEASURED |
| Savings vs. naive 0.5 threshold | €7,413.27 | MEASURED |

Full detail, every chart, and every honest caveat (including a flagged benchmark-precision gap and an in-sample-vs-held-out adversarial testing caveat) are in `reports/`.

## Provenance

The dataset is the real, publicly known "Credit Card Fraud Detection" dataset (European cardholders, September 2013; 284,807 rows, 492 fraud cases, 0.172749% fraud rate). Direct Kaggle/OpenML access was blocked by network egress policy, so a mirror copy was retrieved and independently verified against the dataset's published statistics (exact match) before use.

All modeling code in `notebooks/01_fraud_detection_full_analysis.ipynb` was executed by Claude (Anthropic's AI assistant) directly in a cloud sandbox, at the user's explicit direction, after the user was informed of the tradeoff and chose to proceed. The same source code is provided here so it can be re-run independently on your own machine.

## Repository layout

```
Fraud_Detection_Platform/
├── data/
│   └── raw/
│       └── creditcard.csv                  # real, verified dataset (~98 MB — see Git LFS note below)
├── notebooks/
│   ├── 01_fraud_detection_full_analysis.ipynb   # REAL, fully executed — 26 cells, zero errors, 12 charts
│   └── starters/                            # earlier unexecuted 4-notebook sequence (01–04), superseded
│       ├── 01_business_understanding_eda.ipynb
│       ├── 02_modeling_class_imbalance.ipynb
│       ├── 03_validation_drift_adversarial.ipynb
│       └── 04_governance_model_card_deployment.ipynb
├── src/                                     # reusable, importable modules used by the notebook
│   ├── model_benchmark.py                   # Stage A screening, Stage B CV, temporal-split validation
│   ├── class_imbalance_utils.py             # cost-optimal threshold search (vectorized, O(n log n))
│   ├── adversarial_robustness.py            # perturbation + greedy boundary-search attacks
│   ├── drift_monitoring.py                  # PSI feature-drift monitoring
│   ├── two_gate_validation.py               # Gate 1 structural checks, Gate 2 stress-test scenarios
│   ├── model_card_generator.py
│   └── notebook_01_starter.py
├── deployment/
│   ├── app.py                               # FastAPI scoring service
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements-api.txt
├── reports/                                 # this session's real deliverables
│   ├── Fraud_Detection_Notebook01_Report.docx     # golden-class Word report, 22 pages
│   ├── Fraud_Detection_Notebook01_Workbook.xlsx   # live-formula Excel workbook, 13 sheets
│   ├── Fraud_Detection_Command_Center.html        # C-suite interactive dashboard
│   ├── Fraud_Detection_Platform_Master_Playbook.docx  # full methodology playbook (v8.0)
│   └── nb1_results/                         # raw JSON results + figures + champion_model.pkl
├── docs/
│   ├── governance_signoff_template.md
│   └── readiness_score_report.md
├── publish_drafts/                          # draft external-facing copy (not yet published)
│   ├── LINKEDIN_POST_DRAFT.md
│   ├── KAGGLE_NOTEBOOK_DESCRIPTION_DRAFT.md
│   └── GITHUB_README_DRAFT.md
├── tests/
│   ├── _smoke_test.py
│   └── test_app_smoke.py
├── requirements.txt
└── .gitignore
```

## Git LFS note on the raw dataset

`data/raw/creditcard.csv` is ~98 MB — under GitHub's 100 MB hard block but well past its 50 MB warning threshold. A plain `git push` will likely work once, but it permanently bloats every future clone of this repo's history. Recommended before your first push:

```bash
git lfs install
git lfs track "data/raw/*.csv"
git add .gitattributes
git add -A
git commit -m "Track raw dataset with Git LFS"
```

If you'd rather not use LFS, an equally common pattern is to `.gitignore` the raw CSV and note in this README where to download it (Kaggle: `mlg-ulb/creditcardfraud`) — the file is currently *not* gitignored here because the raw CSV was explicitly requested in the repo.

## Reproducing the notebook

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/01_fraud_detection_full_analysis.ipynb
```

Running it writes real outputs to `notebooks/nb1_results/` (relative to wherever the notebook is run from): `nb1_final_results.json`, `champion_model.pkl`, and a `figures/` folder of 12 PNGs.

## Standing project rules

- **Zero-fabrication policy** — every number is real/computed, never invented
- **WARP** — runtime performance discipline (vectorization, thread-ceiling env vars set before ML imports, ~92% CPU/RAM cap)
- **RANDOM_SEED = 42** everywhere, for reproducibility
