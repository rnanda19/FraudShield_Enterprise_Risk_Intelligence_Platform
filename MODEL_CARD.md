# Model Card — pointer

The real, generated model card for this project's champion model lives at [`reports/nb2_results/model_card.md`](reports/nb2_results/model_card.md) (also rendered as [`model_card.html`](reports/nb2_results/model_card.html)). It is produced by `src/model_card_generator.py` and populated with NB1's real measured metrics — this file is intentionally just a pointer rather than a duplicate, so the two can never drift apart.

**Quick facts** (see the real card for full detail, limitations, and intended use):

- Model: CatBoost, champion of a 6-model Stage A screen
- CV PR-AUC: 0.8482 (95% bootstrap CI 0.8162–0.8784)
- Temporal-split PR-AUC: 0.7692
- Operating threshold: 0.0443 (cost-optimal)
- Training data: Kaggle `mlg-ulb/creditcardfraud`, 284,807 real transactions
- Model tier (NB6): Tier 2 — moderate materiality, standard oversight
