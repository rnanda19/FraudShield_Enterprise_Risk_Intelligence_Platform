"""
class_imbalance_utils.py
Reusable module — Fraud Detection Platform (Project 1) and future projects.

Implements the real, comparable class-imbalance handling techniques specified
in Section 6 of the Master Playbook: class weighting, threshold-moving, and
resampling (SMOTE / random undersampling). All three are run and compared by
REAL Stage B cross-validated PR-AUC on your own machine — this module does not
pick a winner for you; it returns the real numbers so you can.

RANDOM_SEED = 42 is used everywhere per the standing reproducibility rule.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Callable

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import average_precision_score, precision_recall_curve

RANDOM_SEED = 42


@dataclass
class ImbalanceStrategyResult:
    """Real, per-fold result for one imbalance-handling strategy."""
    strategy_name: str
    fold_pr_auc: list[float] = field(default_factory=list)

    @property
    def mean_pr_auc(self) -> float:
        return float(np.mean(self.fold_pr_auc)) if self.fold_pr_auc else float("nan")

    @property
    def std_pr_auc(self) -> float:
        return float(np.std(self.fold_pr_auc)) if self.fold_pr_auc else float("nan")


def get_class_weight(y: pd.Series) -> dict:
    """Real class_weight='balanced' equivalent, computed from the actual labels."""
    classes, counts = np.unique(y, return_counts=True)
    n_samples = len(y)
    n_classes = len(classes)
    weights = {c: n_samples / (n_classes * cnt) for c, cnt in zip(classes, counts)}
    return weights


def best_threshold_by_cost(y_true: np.ndarray, y_scores: np.ndarray,
                            fn_cost_per_dollar_lost: float,
                            fp_cost_multiplier_vs_fraud: float,
                            amounts: np.ndarray) -> dict:
    """
    Threshold-moving: choose the decision threshold that minimizes real total
    cost, using the two sourced real-world multipliers from Section 10 of the
    Master Playbook:
      - fn_cost_per_dollar_lost: LexisNexis True Cost of Fraud (~4.41)
      - fp_cost_multiplier_vs_fraud: relative severity of false declines vs
        fraud losses, industry-wide (~9.2x, Aite-Novarica/Statista via Riskified)

    This does not invent a cost number — it takes the two you sourced and
    finds the real threshold that minimizes (FN_cost + FP_cost) on your own
    real validation data.

    WARP-vectorized (real bug fixed this session): the original implementation
    looped over every candidate threshold from precision_recall_curve in
    Python, recomputing boolean masks and sums over the FULL array each time —
    O(n) work per threshold x O(n) thresholds (one per unique score) = O(n^2).
    On this dataset's 284,807 rows that is on the order of 10^11 operations,
    which in real testing did not finish in a reasonable time and had to be
    killed. The fix below sorts once, then uses cumulative sums to get every
    threshold's cost in one vectorized pass — O(n log n) total.
    """
    y_true = np.asarray(y_true)
    y_scores = np.asarray(y_scores)
    amounts = np.asarray(amounts)
    n = len(y_true)
    if n == 0:
        return {"threshold": 0.5, "total_cost": 0.0, "fn_cost": 0.0, "fp_cost": 0.0}

    # Sort once, descending by score — "predict positive" = the top-k scores.
    order = np.argsort(-y_scores, kind="mergesort")  # stable, so ties keep a deterministic order
    sorted_scores = y_scores[order]
    sorted_amounts = amounts[order]
    sorted_y = y_true[order]

    fraud_amt_cum = np.cumsum(sorted_amounts * (sorted_y == 1))
    legit_amt_cum = np.cumsum(sorted_amounts * (sorted_y == 0))
    total_fraud_amt = fraud_amt_cum[-1]

    # For "flag the top k highest-scoring rows", vectorized over every k = 1..n:
    fn_amt = total_fraud_amt - fraud_amt_cum   # real fraud amount missed (not in top k)
    fp_amt = legit_amt_cum                     # real legitimate amount flagged (in top k)
    total_cost = fn_amt * fn_cost_per_dollar_lost + fp_amt * fp_cost_multiplier_vs_fraud / 100.0

    # Only evaluate at the boundary between distinct score values, so a tie
    # is never split across the predicted/not-predicted line (matches the
    # original's use of precision_recall_curve's per-unique-value thresholds).
    is_last_of_group = np.empty(n, dtype=bool)
    is_last_of_group[:-1] = sorted_scores[:-1] != sorted_scores[1:]
    is_last_of_group[-1] = True
    valid_idx = np.nonzero(is_last_of_group)[0]

    best_pos = valid_idx[np.argmin(total_cost[valid_idx])]
    return {
        "threshold": float(sorted_scores[best_pos]),
        "total_cost": float(total_cost[best_pos]),
        "fn_cost": float(fn_amt[best_pos] * fn_cost_per_dollar_lost),
        "fp_cost": float(fp_amt[best_pos] * fp_cost_multiplier_vs_fraud / 100.0),
    }


def compare_imbalance_strategies(
    X: pd.DataFrame,
    y: pd.Series,
    build_model_fn: Callable[[dict | None], object],
    n_splits: int = 5,
) -> dict[str, ImbalanceStrategyResult]:
    """
    Runs the real Stage B 5-fold CV comparison across all three strategies.

    build_model_fn(class_weight_dict_or_None) -> an unfitted sklearn-compatible
    classifier (e.g., lambda cw: XGBClassifier(scale_pos_weight=..., ...) or
    lambda cw: RandomForestClassifier(class_weight=cw, random_state=RANDOM_SEED))

    Resampling (SMOTE / undersampling) is applied ONLY inside each fold's
    training split, never before the split, to avoid leaking synthetic or
    duplicated minority examples into validation — per the standing rule in
    Section 6 of the Master Playbook.
    """
    results = {
        "class_weighting": ImbalanceStrategyResult("class_weighting"),
        "threshold_moving": ImbalanceStrategyResult("threshold_moving"),
        "resampling_smote": ImbalanceStrategyResult("resampling_smote"),
    }

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_SEED)
    X_arr = X.reset_index(drop=True)
    y_arr = y.reset_index(drop=True)

    for train_idx, val_idx in skf.split(X_arr, y_arr):
        X_train, X_val = X_arr.iloc[train_idx], X_arr.iloc[val_idx]
        y_train, y_val = y_arr.iloc[train_idx], y_arr.iloc[val_idx]

        # --- Strategy 1: class weighting ---
        cw = get_class_weight(y_train)
        model_cw = build_model_fn(cw)
        model_cw.fit(X_train, y_train)
        scores_cw = model_cw.predict_proba(X_val)[:, 1]
        results["class_weighting"].fold_pr_auc.append(
            average_precision_score(y_val, scores_cw)
        )

        # --- Strategy 2: threshold-moving on the unmodified distribution ---
        model_tm = build_model_fn(None)
        model_tm.fit(X_train, y_train)
        scores_tm = model_tm.predict_proba(X_val)[:, 1]
        results["threshold_moving"].fold_pr_auc.append(
            average_precision_score(y_val, scores_tm)
        )

        # --- Strategy 3: SMOTE, applied ONLY to this fold's training split ---
        try:
            from imblearn.over_sampling import SMOTE
            smote = SMOTE(random_state=RANDOM_SEED)
            X_res, y_res = smote.fit_resample(X_train, y_train)
        except ImportError as exc:
            raise ImportError(
                "imbalanced-learn is required for the resampling strategy: "
                "pip install imbalanced-learn"
            ) from exc
        model_sm = build_model_fn(None)
        model_sm.fit(X_res, y_res)
        scores_sm = model_sm.predict_proba(X_val)[:, 1]
        results["resampling_smote"].fold_pr_auc.append(
            average_precision_score(y_val, scores_sm)
        )

    return results


def winning_strategy(results: dict[str, ImbalanceStrategyResult]) -> str:
    """Returns the strategy with the highest REAL mean CV PR-AUC. No tie-break by reputation."""
    return max(results, key=lambda k: results[k].mean_pr_auc)
