> Fill every `[[REAL: ...]]` with your actual result before posting. This is
> a career-transition post — a placeholder presented as a real result would
> undermine exactly the credibility you're trying to build. Post only once
> every bracket below is a genuine number from your own run.

---

After 27 years as a refinery engineer at BPCL, I've spent the last several
months building toward a transition into Credit Risk / Financial Risk
Analytics. Sharing the second project in that portfolio: a fraud detection
platform built on the real Worldline/ULB Credit Card Fraud dataset
(284,807 European card transactions, 0.172% fraud rate).

A few things I focused on that I think matter more than raw accuracy in a
real bank setting:

→ The decision threshold isn't 0.5 by default — it's chosen to minimize
real financial cost, using two independently sourced industry benchmarks
(a $4.41-per-$1-of-fraud total-cost multiplier from LexisNexis, and a
~9.2x false-decline severity ratio from Aite-Novarica/Statista via
Riskified).

→ I validated on a time-ordered split, not just k-fold cross-validation —
because fraud patterns drift, and a model that only looks good on shuffled
data can fail in production.

→ I tested the model's adversarial robustness directly: what fraction of
the fraud it currently catches could be evaded just by structuring the
transaction amount down? Real result: `[[REAL]]`%.

→ I wrote out the governance side too — a four-tier sign-off process
(Technical Lead → Model Risk Manager → Chief Compliance Officer →
Business Owner), because a model without a governance trail isn't
production-ready, no matter how good its metrics are.

Real numbers from this run: `[[REAL: champion model]]`, PR-AUC
`[[REAL]]` (95% CI `[[REAL]]`), precision `[[REAL]]` / recall `[[REAL]]`
at the cost-optimal threshold.

Full writeup, code, and governance templates: `[[REAL: your GitHub link]]`

#CreditRisk #FraudDetection #DataScience #CareerTransition #MachineLearning
