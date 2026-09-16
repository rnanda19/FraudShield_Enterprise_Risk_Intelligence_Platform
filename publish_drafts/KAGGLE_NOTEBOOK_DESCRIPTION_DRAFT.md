# Cost-Aware Fraud Detection with Temporal Validation & Adversarial Robustness Testing

Part of **FraudShield — Enterprise Risk Intelligence Platform**, a 13-notebook pipeline carrying one champion model from raw data through governance, monitoring, regulatory oversight, and executive reporting. This notebook (NB1) is the core model-screening and financial-impact engine everything else builds on.

This goes beyond a standard classification exercise on the Credit Card Fraud Detection dataset in three specific ways:

**1. The decision threshold is chosen to minimize real financial cost**, not accuracy or F1. Two industry-sourced cost benchmarks are used: LexisNexis's finding that North American financial institutions incur $4.41 in total cost for every $1 of actual fraud loss, and an approximate 9.2x false-decline-to-fraud-loss severity ratio derived from Aite-Novarica and Statista figures reported by Riskified. `best_threshold_by_cost()` searches the threshold space to minimize `(FN_cost + FP_cost)`, not to maximize a generic metric — vectorized as an O(n log n) cumulative-sum search after an earlier unvectorized version failed to finish on the full dataset (documented in the repo's CHANGELOG).

**2. Validation includes a temporal (time-ordered) split alongside cross-validation.** Real fraud rates and patterns drift over time; a model that only looks strong under random k-fold CV can still fail on tomorrow's transaction stream. This notebook reports both numbers side by side: CV PR-AUC = **0.8482** (95% bootstrap CI 0.8162–0.8784), temporal-split PR-AUC = **0.7692** — reported honestly even though it's the less flattering number.

**3. Adversarial robustness is measured, not assumed.** A greedy boundary-search test asks: of the fraud this model currently catches, what fraction could a fraud ring evade just by structuring the transaction amount down by up to 90%? Real result: **0.61%** evadable (3 of 492 caught cases), median amount cut required **58%** — with an honest in-sample-evaluation caveat disclosed rather than hidden.

## Results summary

| | |
|---|---|
| Champion model | CatBoost |
| CV PR-AUC (bootstrap 95% CI) | 0.8482 (0.8162–0.8784) |
| Temporal-split PR-AUC | 0.7692 |
| Precision / Recall @ cost-optimal threshold (0.0443) | 69.64% / 82.52% |
| vs. external published RF benchmark (0.9996/0.9333/0.7467/0.8296) | Flagged for investigation — precision gap of -0.237, disclosed rather than smoothed over |
| Real savings vs. no-model baseline | €199,450.76 (≈ $231,203.32) |

## Honest limitations

The dataset's V1–V28 features are PCA-anonymized, so no protected-attribute fairness audit is possible here — only Amount-band / time-of-day equity checks are shown. This is disclosed, not hidden. The full platform (governance tiering, BCBS 239 mapping, regulatory/inference-logging disclosure, and a four-tier sign-off dry-run with every human decision field deliberately left blank) is in the companion GitHub repo, linked below.

Full repo: `https://github.com/rnanda19/FraudShield_Enterprise_Risk_Intelligence_Platform`

**Upvote if you find the cost-aware thresholding or the adversarial robustness test useful — happy to answer questions in the comments.**
