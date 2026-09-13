# Fraud Detection Platform

A production-grounded credit-card fraud detection platform built on the real
[Worldline / ULB Machine Learning Group Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
(European cardholders, September 2013; 284,807 transactions, 492 fraud,
0.172% fraud rate), following a top-tier-bank-aligned methodology.

> **Fill-in-before-publishing checklist:** every `[[REAL: ...]]` placeholder
> below must be replaced with a real number from your own run before this
> README goes public. Do not publish with placeholders still in place — an
> unfilled bracket is more honest than a guessed number.

## What this is

An end-to-end fraud detection pipeline: EDA → class-imbalance-aware model
benchmarking (RandomForest / XGBoost / CatBoost / LightGBM, Stage A screen →
Stage B 5-fold CV → bootstrap CI → temporal-split validation) → two-gate
validation (structural + statistical/concentration) → drift monitoring
(PSI/KS/PR-AUC-drop) → adversarial robustness testing → a containerized
FastAPI scoring service → full model-risk governance documentation
(Three Lines of Defense, four-tier sign-off).

## Real results

| Metric | Value |
|---|---|
| Champion model | `[[REAL: e.g. XGBoost]]` |
| Cross-validated PR-AUC (mean ± bootstrap 95% CI) | `[[REAL: e.g. 0.87 (0.83–0.91)]]` |
| Temporal-split PR-AUC | `[[REAL]]` |
| Precision @ chosen threshold | `[[REAL]]` |
| Recall @ chosen threshold | `[[REAL]]` |
| Comparison to external published benchmark (RF: 0.9996 acc / 0.9333 prec / 0.7467 recall / F1 0.8296) | `[[REAL: consistent / investigate]]` |
| Adversarial boundary-search evasion rate (within 90% amount-cut budget) | `[[REAL]]` |

## Why this is different from a typical Kaggle fraud-detection notebook

- **Cost-aware, not accuracy-aware.** The decision threshold is chosen by
  minimizing real total cost, using two independently sourced industry
  benchmarks: LexisNexis's $4.41-per-$1-of-fraud total cost multiplier, and
  the ~9.2x false-decline-to-fraud-loss severity ratio (Aite-Novarica /
  Statista, via Riskified) — not an arbitrary 0.5 threshold.
- **Temporal validation, not just k-fold.** A time-based split is run
  alongside cross-validation, because in production, fraud patterns drift
  over time — a model that only looks good under random k-fold can still
  fail on tomorrow's transactions.
- **Adversarial robustness is tested, not assumed.** Fraud is an
  adversarially contested domain: a perturbation-sensitivity test and a
  greedy boundary-search evasion test (grounded in USENIX Security research
  on evading tree-ensemble fraud/security classifiers) quantify how easily
  the model could be evaded by realistic amount-structuring.
- **Governance is real, not decorative.** A four-tier sign-off (Technical
  Lead → Model Risk Manager → Chief Compliance Officer → Business Owner),
  modeled on SR 11-7 / the emerging SR 26-2-style unified model-risk
  lifecycle standard.
- **Every financial-impact number is labeled Measured, Assumed, or
  Out-of-Scope** — there is no unlabeled blended estimate anywhere in this
  repository.

## Known limitations (stated up front, not buried)

- Features V1–V28 are PCA-anonymized by the dataset's original publisher —
  no protected-attribute fairness testing is possible on this dataset.
  Equity of impact is checked via Amount-band and hour-of-day segments
  instead, which is a real but partial substitute.
- Single-node scale, evaluated on `[[REAL: your machine's spec]]` — a
  Polars/Dask scale-up path is designed but not yet benchmarked.
- `[[REAL: list any further limitation your own run surfaces]]`

## Repository structure

```
notebooks/           01_eda.ipynb, 02_modeling.ipynb, 03_validation.ipynb, 04_governance.ipynb
fraud_detection_modules/   reusable Python modules (class imbalance, validation,
                            drift monitoring, adversarial robustness, model cards)
deployment/           FastAPI scoring service + Dockerfile + docker-compose
governance_signoff_template.md   fillable four-tier sign-off document
docs/                 Master Playbook (Word), gap analyses
```

## Running it

```
pip install -r fraud_detection_modules/requirements.txt
python fraud_detection_modules/_smoke_test.py   # confirms the code itself works (synthetic data)
# then run the real notebooks against the real dataset
```

## Attribution

Dataset: Worldline and the Machine Learning Group (ULB) — see the dataset's
own citation requirements on Kaggle. Cost benchmarks: LexisNexis Risk
Solutions *True Cost of Fraud™* study; Aite-Novarica / Statista (via
Riskified). Adversarial-robustness grounding: USENIX Security research on
evasion of tree-ensemble security classifiers.
