> Every number below is real, taken from the actual notebook run — nothing
> is a placeholder. Review the phrasing before posting, but the figures
> themselves don't need filling in.

---

After 27 years as a refinery engineer at BPCL, I've spent the last several months building toward a transition into Credit Risk / Financial Risk Analytics. Sharing the second project in that portfolio: **FraudShield**, an enterprise-grade fraud detection platform — 13 notebooks carrying one model from raw transaction data through governance, monitoring, regulatory oversight, and four different executive-reporting formats.

Built on the real Worldline/ULB Credit Card Fraud dataset (284,807 European card transactions, 0.17% fraud rate).

A few things I focused on that I think matter more than raw accuracy in a real bank setting:

→ The decision threshold isn't 0.5 by default — it's chosen to minimize real financial cost, using two independently sourced industry benchmarks (a $4.41-per-$1-of-fraud total-cost multiplier from LexisNexis, and a ~9.2x false-decline severity ratio from Aite-Novarica/Statista via Riskified). Real result: cost-optimal threshold 0.0443, saving €199,450.76 (≈ $231.2K) versus not using a model at all.

→ I validated on a time-ordered split, not just k-fold cross-validation — because fraud patterns drift. CV PR-AUC came in at 0.8482 (95% CI 0.8162–0.8784); the honest temporal-split number was 0.7692. Reporting both, not just the flattering one.

→ I tested the model's adversarial robustness directly: what fraction of the fraud it currently catches could be evaded just by structuring the transaction amount down? Real result: 0.61% evadable within a 90% amount-reduction budget — genuinely low, but not zero, and disclosed either way.

→ I built and ran a real BCBS 239 data-governance mapping and a four-tier governance sign-off dry-run (Technical Lead → Model Risk Manager → CCO → Business Owner) — every Approve/Reject checkbox and signature field is deliberately left blank in the repo, because a model producing its own sign-off would defeat the point of having one.

Champion model: CatBoost. Precision/recall at the cost-optimal threshold: 69.64% / 82.52%.

Full pipeline, governance templates, and an honest readiness scorecard (currently 8.89/10, with the remaining gaps named explicitly, not glossed over): https://github.com/rnanda19/FraudShield_Enterprise_Risk_Intelligence_Platform

#CreditRisk #FraudDetection #DataScience #CareerTransition #MachineLearning
