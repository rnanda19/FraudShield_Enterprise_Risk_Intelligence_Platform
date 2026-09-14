# Regulatory Applicability, Inference Logging & Human Oversight — Fraud Detection Platform

**Generated:** 2026-09-13T17:35:40.694463+00:00
**This section is informational only, not legal advice or a compliance claim.**

## Section A — Regulatory Applicability (informational)

| Framework | Jurisdiction | Relevance to this system |
|---|---|---|
| Bank Secrecy Act (BSA) / Suspicious Activity Report (SAR) filing | US | Confirmed fraud above a bank's SAR filing threshold typically triggers a mandatory SAR filing obligation -- this system's real /score decisions and confirmed-fraud outcomes are the kind of event stream that would feed a SAR workflow. |
| Regulation E (Electronic Fund Transfer Act) | US | Governs consumer liability limits and mandatory dispute-resolution timelines for unauthorized electronic transactions -- directly relevant to how a real false decline or a real missed-fraud case would be handled downstream of this model's decision. |
| Gramm-Leach-Bliley Act (GLBA) Safeguards Rule | US | Requires financial institutions to maintain a documented, reasonable data-security program for customer financial data -- relevant to how this system's real feature data and inference logs would need to be stored/secured in production. |
| PSD2 Strong Customer Authentication & fraud-monitoring obligations | EU | Requires payment service providers to monitor transactions for fraud and apply risk-based authentication -- relevant given this project's EUR figures and dual-currency framing throughout. |

## Section B — Inference-Logging Schema

A real `InferenceLogRecord` dataclass with 10 fields (request_id, timestamp_utc, model_version, decision_threshold_used, fraud_probability, decision, human_review_flag, input_feature_hash, latency_ms_equivalent, ground_truth_class_REPLAY_ONLY) — see the notebook code for the real definition. `input_feature_hash` is a SHA-256 fingerprint, never raw feature values, by design. `ground_truth_class_REPLAY_ONLY` exists only in this historical replay and would never be populated in a true real-time production log.

551 real log records generated and written to `inference_log_sample.jsonl` (51 real in-band + 500 real out-of-band sample, RANDOM_SEED=42).

## Section C — Human Oversight

**Methodology caveat** (same disclosed limitation as NB2's adversarial-robustness section and NB5's Section D): scored in-sample — the real champion model scored on rows it was fit on, not a strictly held-out fold. Treat the counts below as a directional design check for the human-review band, not a claim about real-world out-of-fold performance.

Disclosed-ASSUMPTION uncertainty band: score in [0.0243, 0.0643] (threshold 0.0443 +/- 0.02).

Real transactions routed to human review: 51 / 284,807 (0.0179%) — 0 real fraud, 51 real legit.

Auto-decided subset (outside the band): TP=492 FP=0 FN=0 TN=284264.

Best-case ASSUMPTION only: if every in-band decision were corrected perfectly by a human reviewer, the real-fraud recall ceiling would include all 0 in-band fraud cases — a theoretical upper bound, not a guarantee of real-world reviewer performance. In this in-sample run, 0 of the 51 in-band transactions were real fraud (all 51 were real legit) — at this disclosed band width, human review here would mainly relieve borderline legitimate customers, not catch additional in-sample fraud; a real, out-of-fold rerun could show a different in-band composition and should not be assumed to match.
