# Model Tiering Matrix — Fraud Detection Platform

**Model:** CatBoost (fraud-champion-v1.0.0)
**Generated:** 2026-09-13T16:48:15.960838+00:00
**Composite score:** 5/9  ->  **TIER 2** — Moderate materiality -- proportionate, standard oversight

## Rubric (disclosed ASSUMPTION bands; all inputs are real, computed by NB1/NB2/NB3/NB4/NB5)

| Dimension | Real input | Score |
|---|---|---|
| Financial Exposure | Worst-case NB5 stress-grid loss is 21.34x today's real cost-optimal total cost (EUR 1,390,976.41 vs. EUR 65,169.00) | 2/3 |
| Regulatory Scrutiny | 2 real open governance flag(s) (see list below) | 2/3 |
| Customer Impact | 179 real false declines / 284,807 real transactions (0.0628%), real-time decisioning | 1/3 |

## Open governance flags feeding the Regulatory Scrutiny score
- NB1 benchmark_check.investigate_flag (real precision/recall gap vs. external reference, unresolved)
- NB2/NB3 drift_monitoring.any_alert (real feature/score drift alert on the early-vs-late proxy)

## Scope and disclosed limitations
- All dollar figures are REAL TOTALS over the actual sampled window (284,807 real transactions, ~48 hours of real data) — not annualized. Annualizing would require a representativeness assumption not sourced for this portfolio project, so it is intentionally not extrapolated here.
- The Financial Exposure and Regulatory Scrutiny band cut points are disclosed ASSUMPTIONs (no universal published cut-point standard exists at this precision for a portfolio project of this scope) — the underlying numbers they are applied to are all real.
- This dataset's V1-V28 features are anonymized PCA components with no demographic attributes (already disclosed in NB2's model card) — Fairness & Bias Testing (gap-analysis priority 1) remains not applicable.

## Retroactive finding
NB3's real drift-monitoring history was computed with an unjustified default tier (1). Future NB3 reruns should pass tier=2 so alert thresholds match this real classification. NB3's existing history entries are left untouched (append-only).

## Recommended next steps for this tier
Standard oversight: scheduled monitoring reruns, documented sign-off before threshold changes.
