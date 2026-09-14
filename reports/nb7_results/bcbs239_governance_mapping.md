# BCBS 239 Data Governance — Fraud Detection Platform

**Generated:** 2026-09-13T16:58:09.248875+00:00
**Real data-quality gate: ALL CHECKS PASSED = True**

## Section A — Real, rerunnable data-quality gate
- [x] no_nulls_anywhere
- [x] amount_non_negative
- [x] time_non_negative
- [x] class_is_binary
- [x] all_numeric_features_finite
- [x] row_count_matches_expected

Fresh duplicate-row count: 1081 (0.3796%) — matches NB1's originally reported 1081: True

## Section B — Concentration / Completeness
Loaded NB2's real concentration report: 120 real segments, worst FP rate 0.3663%

**Disclosed limitation:** this anonymized, single-source dataset has no business-line/legal-entity/region dimensions — Amount-band x hour-of-day is the disclosed real substitute, not a full satisfaction of BCBS 239's Completeness principle.

## Section C — BCBS 239 principle-group mapping (project's own sourced summary; real evidence only)

| Principle group | Status | Evidence |
|---|---|---|
| Governance | evidenced | NB6 real Tier 2 (Moderate materiality -- proportionate, standard oversight); oversight cadence follows NB6's real recommended-next-steps for that tier. |
| Data architecture | limitation disclosed | Single anonymized source table (V1-V28 PCA components, Amount, Time, Class) -- no cross-source identifiers or taxonomy exist to integrate at this project's scope. Not fabricated. |
| Accuracy & integrity | evidenced | NB2 Gate 1 structural checks (real, all_passed=True); this notebook's own real, rerunnable data-quality gate (Section A, all_checks_passed=True). |
| Completeness | limitation disclosed | No business-line/legal-entity/region dimensions exist in this dataset (see Section B). Amount-band x hour-of-day (NB2's real concentration report) is the disclosed substitute. |
| Timeliness | evidenced | NB3's real append-only monitoring cadence + this notebook's own real append-only data-quality gate -- both designed to be rerun against each new real data batch, aggregation frequency scaling with how often new data arrives. |
| Adaptability | evidenced | NB6's real retroactive finding (recommending NB3's monitoring tier parameter be updated from its default) is a live, real example of the system adapting to a new governance decision. |

## Scope note
This maps against the 6 principle-groups this project's own gap-analysis doc already sourced from BCBS 239 (Governance, Data architecture, Accuracy & integrity, Completeness, Timeliness, Adaptability) — not a hand-typed reproduction of the full 14-principle regulatory text, to avoid misstating exact regulatory wording this portfolio project has not independently sourced number-by-number.
