> Fill every `[[REAL: ...]]` with your actual result before publishing. Do
> not submit this notebook to Kaggle with placeholders still in it.

# Cost-Aware Fraud Detection with Temporal Validation & Adversarial Robustness Testing

This notebook goes beyond a standard classification exercise on the
Credit Card Fraud Detection dataset in three specific ways:

**1. The decision threshold is chosen to minimize real financial cost**, not
accuracy or F1. Two industry-sourced cost benchmarks are used: LexisNexis's
finding that North American financial institutions incur $4.41 in total
cost for every $1 of actual fraud loss, and an approximate 9.2x
false-decline-to-fraud-loss severity ratio derived from Aite-Novarica and
Statista figures reported by Riskified. `best_threshold_by_cost()` searches
the threshold space to minimize `(FN_cost + FP_cost)`, not to maximize a
generic metric.

**2. Validation includes a temporal (time-ordered) split alongside
cross-validation.** Real fraud rates and patterns drift over time; a model
that only looks strong under random k-fold CV can still fail on tomorrow's
transaction stream. This notebook reports both numbers side by side:
CV PR-AUC = `[[REAL]]`, temporal-split PR-AUC = `[[REAL]]`.

**3. Adversarial robustness is measured, not assumed.** A greedy
boundary-search test asks: of the fraud this model currently catches, what
fraction could a fraud ring evade just by structuring the transaction
amount down by up to 90%? Real result: `[[REAL]]`% evadable, median amount
cut required = `[[REAL]]`%.

## Results summary

| | |
|---|---|
| Champion model | `[[REAL]]` |
| CV PR-AUC (bootstrap 95% CI) | `[[REAL]]` |
| Temporal-split PR-AUC | `[[REAL]]` |
| Precision / Recall @ chosen threshold | `[[REAL]]` / `[[REAL]]` |
| vs. external published RF benchmark (0.9996/0.9333/0.7467/0.8296) | `[[REAL]]` |

## Honest limitations

The dataset's V1–V28 features are PCA-anonymized, so no protected-attribute
fairness audit is possible here — only Amount-band / time-of-day equity
checks are shown. This is disclosed, not hidden.

**Upvote if you find the cost-aware thresholding or the adversarial
robustness test useful — happy to answer questions in the comments.**
