# Model Card — Fraud Detection Champion (CatBoost)

**Version:** fraud-champion-v1.0.0
**Tier:** 1 (per Master Playbook Section 3)
**Training data snapshot:** creditcard.csv, 284,807 rows, RANDOM_SEED=42
**Code commit:** 187e3342532b340ad55cb2c073b80a899dca98d3
**Generated:** 2026-09-13T16:06:27.419159+00:00

## Intended Use
Real-time, transaction-level fraud-probability scoring for card-not-present and card-present transactions, to prioritize which transactions a fraud-ops team reviews or holds, at the cost-optimal decision threshold computed in Notebook 01.

## Out-of-Scope Uses
- Any automated account-closure or customer-blocking decision without human review.
- Any use as a credit, lending, or account-opening decision -- this model is trained only on real-time transaction fraud, not creditworthiness.
- Any demographic or fairness-protected-class decisioning -- the training features are anonymized PCA components (V1-V28); no demographic attributes are available or used.

## Training Data Provenance
Kaggle mlg-ulb/creditcardfraud (Worldline / Universite Libre de Bruxelles), real anonymized European cardholder transactions, September 2013, ~48-hour window, 284,807 transactions, 492 fraud (0.173%).

## Performance (real, measured)
| Metric | Value |
|---|---|
| CV PR-AUC | 0.8482 |
| CV PR-AUC 95% bootstrap CI | [0.8162, 0.8784] |
| Temporal-split PR-AUC | 0.7692 |
| Precision @ operating threshold (0.0443) | 0.6951 |
| Recall @ operating threshold | 0.8293 |

## External Benchmark Comparison (Section 19.4)
{'your_precision': 0.6950596252129472, 'reference_precision': 0.9333, 'precision_gap': -0.23824037478705284, 'your_recall': 0.8292682926829268, 'reference_recall': 0.7467, 'recall_gap': 0.08256829268292676, 'investigate_flag': True, 'note': 'Large positive gaps may indicate leakage; large negative gaps may indicate a bug — investigate before trusting either.'}

## Known Limitations
- Anonymized PCA features (V1-V28) make demographic fairness auditing impossible on this dataset -- disclosed per Section 8/18, not silently omitted.
- Only a ~48-hour data window exists; the drift-monitoring baseline above uses an early-vs-late proxy, not genuine multi-period production history (Section 9).
- Adversarial robustness (Section 19): 3 of 492 currently-caught fraud cases (0.61%) were evadable within a 90% amount-cut budget -- see the adversarial robustness section above for the real, measured numbers.
- Gate 2 stress-test multipliers (2x volume, 3x fraud rate) are stated ASSUMPTIONs for a documented hypothetical shock, not a fitted or historically-calibrated scenario.

## Monitoring Plan
See Master Playbook Section 9
