# Fraud Detection Platform — v7.0 Honest Readiness & Score Report

**Date:** September 13, 2026
**Trigger:** User requested the deepest possible work across all dimensions and a final score of at least 9.8888/10.

## The one governing fact

9.8888/10 was not delivered, and will not be fabricated. That number requires real execution — a real notebook run, a real deployment, a real governance dry-run, real external publish engagement, and real elapsed monitoring time — none of which Claude can do on the user's behalf, per this project's own standing execution-boundary and zero-fabrication rules (set by the user at the start of this project). Inventing that score would be the single worst violation of "no fabricated works, only data-driven true insights" available in this entire project.

## What was actually done this round (all real, all verified)

1. **Adversarial robustness test code** (`adversarial_robustness.py`) — perturbation-sensitivity test and a greedy boundary-search evasion test on Amount/Time, grounded in USENIX Security research on evading tree-ensemble security classifiers. Actually run end-to-end against synthetic data this session; output confirmed correct.
2. **Deployment readiness** — a FastAPI scoring service (`deployment/app.py`), Dockerfile, docker-compose.yml, and a pytest smoke test. The smoke test was actually executed (not just written) and passed, including after fixing a real deprecation issue (`on_event` → `lifespan`).
3. **Governance sign-off template** (`governance_signoff_template.md`) — a fillable four-tier (Technical Lead → Model Risk Manager → CCO → Business Owner) sign-off document, matching the user's own pre-existing Home Credit Three-Lines-of-Defense SOP.
4. **External-publish drafts** — GitHub README, Kaggle notebook description, LinkedIn post, each with every metric explicitly bracketed `[[REAL: ...]]` so a draft can never be mistaken for, or accidentally published as, a real result.
5. **Real dataset diligence for Phase 4** — IEEE-CIS Fraud Detection (561,013 train / 28,527 test rows in the Amazon Science benchmark split; 590,540 total original transactions; 67 features; 3.50% training fraud rate) and PaySim (6,362,620 rows; 0.13% fraud rate; 5 transaction types; 744-step/30-day simulation) — both verified against authoritative sources, including honestly flagging a 99-row discrepancy in PaySim's own source paper (text says 8,312 fraud rows, its own Table I says 8,213) rather than silently picking one.
6. Delivered the previously-built-but-unsent `fraud_detection_modules.zip`, and updated the Master Playbook to **v7.0**.

## The honest score

The scoring model (baseline 6.60/10 from the 5-persona weighted review, +0.425 per fully-completed roadmap phase toward a 9.9999 ceiling) is refined this round to separate **readiness** (real, verified code/artifacts exist) from **execution** (the phase's real Definition of Done is met). Each phase's 0.425 splits into 0.15 readiness + 0.275 execution.

| Phase | Readiness earned | Execution earned |
|---|---|---|
| 1 — End-to-end notebook execution | 0.15 (6 modules built + smoke-tested) | 0 |
| 2 — Real-sourced cost assumptions | — | 0.425 (fully complete, v6.1) |
| 3 — Adversarial red-team | 0.15 (code written + run on synthetic data) | 0 |
| 4 — Cross-dataset generalization | 0.15 (both datasets diligenced, benchmark code reusable) | 0 |
| 5 — Live deployment | 0.15 (API+Docker written, smoke-tested) | 0 |
| 6 — Governance dry-run | 0.15 (template written) | 0 |
| 7 — External validation | 0.15 (drafts written) | 0 |
| 8 — Sustained monitoring | 0 (cannot be front-loaded) | 0 |

**Score = 6.60 + 0.425 + (6 × 0.15) = 7.925 ≈ 7.93 / 10.**

This is up from 7.03/10 before this round, and it is the honest ceiling until the user runs the real notebooks, deploys the real service, exercises the real governance sign-off, publishes for real, and lets real monitoring history accumulate. None of those six remaining steps can be shortcut with more writing — they require the user's own execution, exactly as this project's standing rules require.

## What remains (unchanged from the roadmap, now with less friction)

Phase 1 (real notebook run) is the highest-leverage next step — every other phase's real execution builds on having a real trained champion model.

## Addendum (v7.1) — What it actually takes to reach 9.888/10

The user asked directly: what does the master plan need to reach 9.888? The scoring model already in use gives a precise, checkable answer — this is design math for the plan's target, not a claim about today's score (which remains 7.93/10, above).

| Milestone | Formula | Score |
|---|---|---|
| Baseline (plan + persona review only) | 6.60 | 6.60 |
| Any 7 of the 8 roadmap phases fully completed (real execution — the weights are equal, so it doesn't matter which 7) | 6.60 + 7 × 0.425 | 9.575 |
| All 8 phases fully completed | 6.60 + 8 × 0.425 | 9.9999 (ceiling) |

**The honest finding:** finishing everything except sustained real monitoring (Phase 8) only reaches 9.575 — still short of 9.888. Crossing 9.888 requires at least 7.736 of the 8 phases' worth of real completion, which mathematically requires Phase 8 (real elapsed weeks/months of monitoring history) to be roughly three-quarters done on top of full real execution of Phases 1, 3, 4, 5, 6, and 7. Phase 8 cannot be accelerated with more code or documentation — its own Definition of Done requires real elapsed time. This is now documented in the Master Playbook as Section 21.1 (v7.1).

## Addendum (v8.0) — Real end-to-end execution run

At the user's explicit direction ("okay proceed"), Claude located a public mirror of the real Worldline/ULB Credit Card Fraud Detection dataset, independently verified it against the dataset's known published statistics (284,807 rows, 492 fraud, 0.172749% fraud rate — matched exactly), and executed the real project pipeline against it in this session's cloud sandbox — NOT on the user's own machine. Full results are in Master Playbook Section 22.

**Key real results:**
- Champion model: CatBoost (Stage B real 5-fold CV mean PR-AUC 0.8482, 95% CI 0.8162–0.8784)
- Temporal-split PR-AUC: 0.7692 — a real, honestly-disclosed divergence from the CV number
- Cost-optimal threshold: 0.0443 → real precision 0.6964 / real recall 0.8252 (OOF), flagged for investigation vs. the external benchmark (precision gap -0.237)
- Real financial impact: €265,164.35 (no model) → €73,126.86 (naive 0.5) → €65,713.59 (cost-optimal) — real measured savings of €199,450.76 vs. no model, €7,413.27 vs. naive threshold
- Real adversarial robustness run against the real trained model: ≤0.20% evasion under simple perturbation, 0.61% evadable within a 90% amount-cut budget — with an honestly disclosed in-sample evaluation caveat (real held-out recall is 82.52%, not the in-sample run's 100%)
- Real local API latency signal: p99 = 2.27ms (localhost, not yet a reachable production deployment)
- **A real, serious bug found and fixed live:** the cost-optimal threshold search was an unvectorized O(n²) loop that did not finish in reasonable time on the full 284,807-row dataset and had to be killed mid-run. Rewritten as a vectorized O(n log n) cumulative-sum approach, verified to match the original's brute-force output exactly, benchmarked at 50ms (down from an unbounded multi-hour runtime). Documented in Section 13.

**Updated score:** Phase 1 and Phase 3 move from readiness-only to fully DONE (real execution evidence, with provenance and methodology caveats disclosed). Phase 5 moves to PARTIAL (real local signal, not yet a real reachable deployment) — awarded half its execution weight.

| Phase | Status | Points |
|---|---|---|
| 1 — End-to-end execution | DONE (real, Claude-executed) | 0.425 |
| 2 — Real-sourced cost assumptions | DONE | 0.425 |
| 3 — Adversarial red-team | DONE (real, in-sample caveat disclosed) | 0.425 |
| 4 — Cross-dataset generalization | Readiness only | 0.15 |
| 5 — Live deployment | Partial (real local signal) | 0.2875 |
| 6 — Governance dry-run | Readiness only | 0.15 |
| 7 — External validation | Readiness only | 0.15 |
| 8 — Sustained monitoring | Not applicable to front-load | 0 |

**Score = 6.60 + 0.425 + 0.425 + 0.425 + 0.15 + 0.2875 + 0.15 + 0.15 + 0 = 8.6125 ≈ 8.61 / 10.**

Up from 7.93/10. The remaining gap to 9.9999 still requires: a real reachable deployment (Phase 5 completion), real cross-dataset generalization testing (Phase 4), a real governance dry-run (Phase 6), real external publish with tracked engagement (Phase 7), and — the one constraint no amount of further work today can close — real elapsed monitoring time (Phase 8), as quantified in Section 21.1.

**Important provenance note carried into the playbook:** this run was Claude's execution in the cloud sandbox, at the user's explicit direction, using a verified real public dataset copy — not the user's own machine. This should be stated accurately if these results are used in a portfolio or interview context; the same code is available for the user to re-run themselves for a fully hands-on version.
