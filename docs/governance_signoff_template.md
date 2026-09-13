---
name: governance_signoff_template
description: >
  Real, fillable four-tier model governance sign-off template for the Fraud
  Detection Platform, carried over from your own Home Credit Risk Suite SOP
  (Three Lines of Defense) and aligned to Master Playbook Sections 11, 17.3,
  and 19. Fill this in with your REAL results once you have run the real
  notebooks — every blank below must be completed with an actual number,
  finding, or decision. A blank left as "TBD" is an honest incomplete
  gate, not a passed one.
---

# Fraud Detection Platform — Model Governance Sign-Off

| Field | Value |
|---|---|
| Model name | `fraud-detection-champion` |
| Model version (semantic, Section 17.3) | |
| Training data snapshot ID | |
| Code commit hash | |
| Date of this review | |
| Reviewed by (this document's author) | |

This document gates go-live. It cannot be approved with placeholder values —
every checklist row requires the real evidence produced by your real run of
Notebooks 01–04 and the modules in this package.

---

## Tier 1 — Technical Lead Review (First Line of Defense)

| Check | Real result | Pass / Fail / N/A |
|---|---|---|
| Gate 1 structural checks (schema, nulls, label binary, no leakage) | | |
| Gate 2 statistical robustness + concentration report (Amount band / hour-of-day) | | |
| Stage A screening completed on 4 candidates | | |
| Stage B 5-fold CV completed on top-2, champion selected by mean CV PR-AUC | | |
| Bootstrap 95% CI on champion PR-AUC (1,000 resamples) | | |
| Temporal (time-based) train/test split result, compared to CV result | | |
| Class-imbalance technique comparison (class weighting / threshold-moving / SMOTE) — winner and why | | |
| External benchmark comparison (vs. RF 0.9996/0.9333/0.7467/0.8296) — investigate flag raised? | | |
| Adversarial robustness: perturbation sensitivity test result | | |
| Adversarial robustness: boundary-search evasion rate within budget | | |
| Drift monitoring wired (PSI / KS / PR-AUC-drop, Tier thresholds) | | |
| Duplicate-row decision (Section 18.1) made and justified in writing | | |

**Technical Lead decision:** ☐ Approve ☐ Conditional ☐ Reject
**Name / Date / Signature:**
**Comments:**

---

## Tier 2 — Model Risk Manager Review (Second Line of Defense)

Independent of the build team. Confirms methodology soundness and
reproducibility — does NOT re-approve Tier 1's numbers, it re-derives or
spot-checks them.

| Check | Finding | Pass / Fail / N/A |
|---|---|---|
| Methodology matches the Master Playbook as documented (no undocumented deviation) | | |
| Environment is pinned (requirements.txt / lockfile) and reproducible | | |
| Random seed (42) used consistently; re-run reproduces reported numbers within tolerance | | |
| Fairness/equity-of-impact scope limitation (PCA-anonymized dataset) explicitly disclosed, not silently omitted | | |
| Known limitations (Section 18) reviewed and none newly discovered | | |
| Challenger model(s) documented, even if not yet promoted | | |
| Model card (Section 11) complete and matches the real numbers above | | |

**Model Risk Manager decision:** ☐ Approve ☐ Conditional ☐ Reject
**Name / Date / Signature:**
**Comments:**

---

## Tier 3 — Chief Compliance Officer Review (Independent Assurance)

| Check | Finding | Pass / Fail / N/A |
|---|---|---|
| SR 11-7 / SR 26-2-style lifecycle governance documentation complete | | |
| Data security & access control confirmed (encryption, least-privilege roles, secrets management) | | |
| Audit trail exists (this document + model card + code commit hash + data snapshot ID) | | |
| Vendor/third-party risk N/A confirmed OR addressed | | |
| Incident response plan (Section 20) reviewed | | |

**CCO decision:** ☐ Approve ☐ Conditional ☐ Reject
**Name / Date / Signature:**
**Comments:**

---

## Tier 4 — Business Owner Sign-Off (Go-Live Decision)

| Check | Finding | Pass / Fail / N/A |
|---|---|---|
| Financial-impact figures reviewed under the Measured / Assumed / Out-of-Scope boundary (Section 10) | | |
| Real cost benchmarks used ($4.41 fraud-loss multiplier; ~9.2x false-decline severity ratio) — no arbitrary placeholders remain | | |
| Total Cost of Ownership (fraud loss prevented net of false-positive friction AND platform run cost) reviewed | | |
| Monitoring cadence (weekly / monthly / quarterly / annual — see appendix) agreed | | |
| Rollback policy (Section 17.3) agreed | | |
| Canary deployment plan agreed before full rollout | | |

**Business Owner decision:** ☐ Approve go-live ☐ Conditional ☐ Reject
**Name / Date / Signature:**
**Comments:**

---

## Appendix A — Monitoring Cadence Commitment

| Cadence | Owner | What is reviewed |
|---|---|---|
| Weekly | | PSI/KS drift alerts, volume anomalies |
| Monthly | | PR-AUC drift, concentration report refresh |
| Quarterly | | Full model card refresh, challenger model comparison |
| Annual | | Full governance re-review (this document, redone) |

## Appendix B — Known Limitations Acknowledged (from Section 18)

List every limitation from the Master Playbook's Section 18 here, with an
explicit acknowledgment that Tier 1–4 reviewers have read and accepted them
as of this sign-off — a limitation this document is silent on is a
limitation nobody has actually reviewed.

1.
2.
3.

---

*This template produces a governance record only once every blank above is
filled with a real result from your real run. An unfilled or "TBD" row
means that gate has not actually been passed — do not read a filled-in
template as evidence of readiness on its own.*
