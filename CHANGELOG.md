# Changelog

All notable changes to this project, in build order. Dates are the real session dates this work was done. This project does not use semantic-version tags per notebook — each entry is a real, verified milestone.

## NB1 — Full Analysis (2026-09-13)
Real end-to-end execution against the full 284,807-row dataset: EDA, imbalance-strategy comparison, Stage A 6-model screening, Stage B 5-fold CV, temporal-split validation, cost-optimal threshold search, SHAP, financial impact. Champion: CatBoost (CV PR-AUC 0.8482, temporal PR-AUC 0.7692). Delivered as executed notebook + Word report + Excel workbook + HTML dashboard.

## NB2 — Validation, Robustness & Deployment Readiness
Two-gate structural/concentration validation, drift-monitoring baseline, adversarial robustness test (perturbation + greedy boundary-search), real model card.

## NB3 — Continuous Monitoring
Reusable `run_monitoring_check()`; appends one real timestamped entry per run to `reports/nb3_results/drift_history.jsonl` — never overwritten.

## NB4 — Serving Consistency & Latency SLA
Runs the real, unmodified `deployment/app.py` in-process via FastAPI TestClient. Real result: exact 0.0 prediction drift across 500 real rows; server-reported P50/P95/P99 latency 0.27/0.34/0.38 ms.

## NB5 — Deepened Stress Testing
3-tier named scenario ladder, vectorized 7×15 scenario grid, reverse stress test, Amount-shock re-scoring of the real trained model.

## NB6 — Model Tiering Matrix
Disclosed 0–3-per-dimension rubric across financial exposure / regulatory scrutiny / customer impact. Real composite score 5/9 → **Tier 2** (not forced to Tier 1).

## NB7 — BCBS 239 Data Governance
Rerunnable data-quality gate (6 checks, all real) + honest mapping of real project evidence against 6 BCBS 239 principle-groups (2 explicitly marked limitation-disclosed, not fabricated compliance).

## NB8 — Regulatory Applicability, Inference Logging & Human Oversight
Regulatory applicability note (BSA/SAR, Reg E, GLBA, PSD2 — informational, not legal advice); real `InferenceLogRecord` schema, 551 real generated log records (SHA-256 feature hash, never raw values); disclosed human-review uncertainty band.

## NB9 — Governance Sign-Off Dry-Run
Auto-populates the real 4-tier `governance_signoff_template.md` from NB1–NB8's on-disk artifacts. Real result: Tier 1 10/12 Pass, Tier 2 7/7 Pass, Tier 3 2/5 Pass, Tier 4 2/6 Pass. Every Approve/Reject and signature field deliberately left blank. **Bug fixed:** a hardcoded line-index in the "Audit trail exists" check grabbed the wrong field from the model card; fixed to search for the real commit-hash line.

## NB10 — Command Center Dashboard
Regenerated to cover all 11 real sections (NB1–NB9, up from NB1-only). Chart.js and 2 real PNGs embedded as base64 for fully offline rendering. **Bug fixed:** embedding the minified Chart.js as a plain Python string corrupted its backslash-heavy regex literals (`Chart is not defined` at runtime); fixed by base64-encoding at generation time.

## NB11 — Executive Rollup Reports
One run produces a PDF (11 real pages), a PPTX deck (10 slides), and an XLSX workbook (10 sheets, including a live Excel formula for savings-vs-no-model). 8 role-based SMART Go/Conditional/Hold decisions, each cited to a real field. **Bugs fixed:** an f-string with an illegal embedded backslash (extracted to a small lookup helper); a leftover placeholder string in the XLSX "Source Notebook" column.

## NB12 — Ultimate Word Report
Full Word document (python-docx): cover page, Executive Summary, 10 numbered sections, 5 real matplotlib charts (including a polar radar of NB6's rubric), sourced-constants appendix. Ran clean on first verification — no bugs found.

## NB13 — World-Class Interactive Dashboard
Extends NB10 to a dark/light-theme design with scroll-reveal animation, animated KPI counters, 2 new slicers, and 6 new real chart sections (confusion-matrix doughnut, model-tiering radar, BCBS239 polarArea, drift-history line, inference-log histogram, reverse-stress line) — 17 sections total, each with an auto-generated 2-line real-data "story". **Bug fixed:** the KPI strip was built dynamically after the page's one-time scroll-reveal observer had already run, so the 7 KPI cards would never have become visible; fixed by re-observing them after they render.

## Repository hardening
Architecture diagram, CI workflow, CONTRIBUTING/ROADMAP/CHANGELOG, and this README rewrite added to bring the repo to the same standard as the AMEX RiskIQ and Home Credit portfolio repos.
