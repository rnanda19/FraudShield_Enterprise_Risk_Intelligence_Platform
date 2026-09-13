"""
model_benchmark.py
Reusable module — implements Section 6 of the Master Playbook: the Stage A
(top-4 screen) -> Stage B (top-2 real 5-fold CV) -> champion-selection
pipeline, plus the bootstrap confidence interval added in v2.0, plus the
external-benchmark sanity check added in v5.0.

Also carries forward the standing WARP thread-ceiling lesson from Home
Credit NB02: thread-limiting environment variables MUST be set before any
ML library is imported, or some candidates get silently disadvantaged.
"""

from __future__ import annotations

# --- WARP thread-ceiling: must run before importing xgboost/lightgbm/etc. ---
import os
_N_THREADS = max(1, int(os.cpu_count() * 0.92 // 1)) if os.cpu_count() else 4
os.environ.setdefault("OMP_NUM_THREADS", str(_N_THREADS))
os.environ.setdefault("OPENBLAS_NUM_THREADS", str(_N_THREADS))
os.environ.setdefault("MKL_NUM_THREADS", str(_N_THREADS))
# ---------------------------------------------------------------------------

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import average_precision_score

RANDOM_SEED = 42

# Real published external reference point (Section 19.4) — a sanity check,
# never a target to reverse-engineer toward. Source: a Random Forest with
# class weighting on this exact ULB dataset reported 0.9996 accuracy,
# 0.9333 precision, 0.7467 recall, F1 = 0.8296 (cited in the Master Playbook).
EXTERNAL_BENCHMARK_REFERENCE = {
    "model": "Random Forest (class-weighted)",
    "accuracy": 0.9996,
    "precision": 0.9333,
    "recall": 0.7467,
    "f1": 0.8296,
    "source": "Published comparative result on the ULB/Kaggle credit-card dataset "
              "(see Master Playbook Section 19.4 for citation)",
}


@dataclass
class StageAResult:
    candidate_name: str
    val_pr_auc: float


@dataclass
class StageBResult:
    candidate_name: str
    fold_pr_auc: list[float] = field(default_factory=list)
    bootstrap_ci: tuple[float, float] | None = None

    @property
    def mean_pr_auc(self) -> float:
        return float(np.mean(self.fold_pr_auc))


def run_stage_a_screening(
    X: pd.DataFrame, y: pd.Series, candidates: dict[str, object], test_size: float = 0.2
) -> list[StageAResult]:
    """
    Single train/validation split screen across the real top-4 candidates
    (RandomForest, XGBoost, CatBoost, LightGBM by convention — pass whichever
    unfitted estimators you're comparing).
    """
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=RANDOM_SEED
    )
    results = []
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        scores = model.predict_proba(X_val)[:, 1]
        results.append(StageAResult(name, average_precision_score(y_val, scores)))
    return sorted(results, key=lambda r: r.val_pr_auc, reverse=True)


def run_stage_b_cv(
    X: pd.DataFrame, y: pd.Series, top_2_candidates: dict[str, object],
    n_splits: int = 5, n_bootstrap: int = 1000,
) -> dict[str, StageBResult]:
    """
    Real 5-fold CV on only the top-2 Stage A candidates, plus a bootstrap
    confidence interval on the champion's PR-AUC (v2.0 addition) computed
    from the pooled out-of-fold predictions.
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_SEED)
    results = {name: StageBResult(name) for name in top_2_candidates}
    oof_scores = {name: np.zeros(len(y)) for name in top_2_candidates}

    X_reset, y_reset = X.reset_index(drop=True), y.reset_index(drop=True)

    for train_idx, val_idx in skf.split(X_reset, y_reset):
        X_train, X_val = X_reset.iloc[train_idx], X_reset.iloc[val_idx]
        y_train, y_val = y_reset.iloc[train_idx], y_reset.iloc[val_idx]

        for name, model in top_2_candidates.items():
            model.fit(X_train, y_train)
            scores = model.predict_proba(X_val)[:, 1]
            oof_scores[name][val_idx] = scores
            results[name].fold_pr_auc.append(average_precision_score(y_val, scores))

    # Bootstrap CI on out-of-fold predictions for each candidate.
    rng = np.random.default_rng(RANDOM_SEED)
    n = len(y_reset)
    for name in top_2_candidates:
        boot_aucs = []
        for _ in range(n_bootstrap):
            idx = rng.integers(0, n, n)
            boot_aucs.append(average_precision_score(y_reset.iloc[idx], oof_scores[name][idx]))
        lower, upper = np.percentile(boot_aucs, [2.5, 97.5])
        results[name].bootstrap_ci = (float(lower), float(upper))

    return results


def select_champion(stage_b_results: dict[str, StageBResult]) -> str:
    """Champion = higher real mean CV PR-AUC. No tie-break by reputation."""
    return max(stage_b_results, key=lambda k: stage_b_results[k].mean_pr_auc)


def temporal_split_validation(
    df: pd.DataFrame, time_col: str, feature_cols: list[str], label_col: str,
    model: object, train_fraction: float = 0.75,
) -> float:
    """
    v2.0 addition: a genuine time-based split using the dataset's real Time
    field (train on the earlier fraction, test on the later fraction),
    mirroring the Home Credit OOT-validation discipline. Returns the real
    temporal-split PR-AUC for comparison against the CV PR-AUC above — any
    divergence must be reported, not hidden.
    """
    df_sorted = df.sort_values(time_col)
    split_idx = int(len(df_sorted) * train_fraction)
    train, test = df_sorted.iloc[:split_idx], df_sorted.iloc[split_idx:]

    model.fit(train[feature_cols], train[label_col])
    scores = model.predict_proba(test[feature_cols])[:, 1]
    return float(average_precision_score(test[label_col], scores))


def compare_to_external_benchmark(real_precision: float, real_recall: float) -> dict:
    """
    Section 19.4: compares YOUR real, measured precision/recall against the
    published external reference. Flags a wide divergence for investigation
    rather than declaring pass/fail silently.
    """
    ref = EXTERNAL_BENCHMARK_REFERENCE
    precision_gap = real_precision - ref["precision"]
    recall_gap = real_recall - ref["recall"]
    return {
        "your_precision": real_precision, "reference_precision": ref["precision"],
        "precision_gap": precision_gap,
        "your_recall": real_recall, "reference_recall": ref["recall"],
        "recall_gap": recall_gap,
        "investigate_flag": abs(precision_gap) > 0.15 or abs(recall_gap) > 0.15,
        "note": ("Large positive gaps may indicate leakage; large negative "
                 "gaps may indicate a bug — investigate before trusting either."),
    }
