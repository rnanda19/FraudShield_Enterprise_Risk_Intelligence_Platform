# Roadmap & Honest Readiness

Current score: **8.89 / 10** (see `docs/readiness_score_report.md` for the full, versioned derivation — this file summarizes it).

## Done — real, execution-verified

| Phase | Status | Evidence |
|---|---|---|
| 1 — End-to-end model execution | **DONE** | NB1, real 284,807-row run, champion CatBoost, CV PR-AUC 0.8482 |
| 2 — Real-sourced cost assumptions | **DONE** | FN/FP cost constants cited to LexisNexis / Aite-Novarica-Statista via Riskified |
| 3 — Adversarial red-team | **DONE** | NB2, real perturbation + boundary-search attacks against the trained champion |
| 6 — Governance dry-run | **DONE** | NB9, real 4-tier sign-off package auto-populated from NB1–NB8's artifacts |

Plus, beyond the original 8-phase roadmap (built at the user's direct request, not required for the score above): NB5 (deepened stress testing), NB6 (model tiering), NB7 (BCBS 239 governance), NB8 (regulatory/inference-logging/human oversight), NB10–NB13 (four independent executive-reporting formats, all auto-picking from real NB1–NB9 output).

## Partial

| Phase | Status | What's real vs. what's missing |
|---|---|---|
| 5 — Live deployment | **PARTIAL** | `deployment/app.py` is real and TestClient-verified (exact 0.0 prediction drift, real measured latency P50/P95/P99). No real reachable production deployment exists yet — it has never been run behind a live endpoint. |

## Open — genuinely require real-world execution, not more notebook work

| Phase | Status | What it needs |
|---|---|---|
| 4 — Cross-dataset generalization | Readiness only | A second real dataset has been diligenced (see the dataset-swap discussion in this repo's history) but the champion model has not actually been re-trained/re-scored against it. |
| 7 — External validation | Readiness only | Draft external-facing copy exists in `publish_drafts/` — nothing has been published or received real engagement yet. |
| 8 — Sustained monitoring | Not applicable to front-load | `reports/nb3_results/drift_history.jsonl` is real and append-only, but structurally requires real elapsed weeks/months of rerun history — cannot be accelerated. |

## Explicitly not fabricated

- No Approve/Reject decision, name, date, or signature has ever been filled into the governance sign-off package (NB9) — those are real human actions.
- No score above 8.89/10 has been claimed. Reaching higher requires real deployment, real publication engagement, and real elapsed monitoring time — see `docs/readiness_score_report.md`'s scoring formula for exactly how much of each.
