"""
drift_monitoring.py
Reusable module — implements Section 9 of the Master Playbook: PSI/CSI/KS
drift computation with the Tier 1 alert thresholds from Section 9's table.

This is the module that turns "we designed a monitoring plan" (v1-v6 of the
playbook) into something you actually run, repeatedly, over real elapsed
time (Section 21 Phase 8) to build a genuine drift history.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from scipy.stats import ks_2samp

# Tier 1 alert thresholds — from Section 9 of the Master Playbook.
# Change these only with a written justification, per Section 3's tiering rule.
TIER_THRESHOLDS = {
    1: {"psi_alert": 0.25, "ks_pvalue_alert": 0.01, "pr_auc_drop_alert": 0.05},
    2: {"psi_alert": 0.35, "ks_pvalue_alert": 0.005, "pr_auc_drop_alert": 0.08},
    3: {"psi_alert": 0.50, "ks_pvalue_alert": 0.001, "pr_auc_drop_alert": 0.12},
}


@dataclass
class DriftReport:
    feature_psi: dict
    score_ks_statistic: float
    score_ks_pvalue: float
    pr_auc_baseline: float
    pr_auc_current: float
    tier: int

    @property
    def pr_auc_drop(self) -> float:
        return self.pr_auc_baseline - self.pr_auc_current

    @property
    def alerts(self) -> dict[str, bool]:
        t = TIER_THRESHOLDS[self.tier]
        return {
            "feature_drift_alert": any(v > t["psi_alert"] for v in self.feature_psi.values()),
            "score_drift_alert": self.score_ks_pvalue < t["ks_pvalue_alert"],
            "performance_drift_alert": self.pr_auc_drop > t["pr_auc_drop_alert"],
        }

    @property
    def any_alert(self) -> bool:
        return any(self.alerts.values())


def population_stability_index(expected: np.ndarray, actual: np.ndarray,
                                n_bins: int = 10) -> float:
    """
    Real PSI computation between a training-time ('expected') and current
    ('actual') distribution of one feature. PSI > 0.25 is the Tier 1 alert
    threshold from Section 9 — this function computes the real number, it
    does not assume a verdict.
    """
    breakpoints = np.linspace(0, 100, n_bins + 1)
    bin_edges = np.percentile(expected, breakpoints)
    bin_edges[0], bin_edges[-1] = -np.inf, np.inf

    expected_pct = np.histogram(expected, bins=bin_edges)[0] / len(expected)
    actual_pct = np.histogram(actual, bins=bin_edges)[0] / len(actual)

    # Avoid division by zero / log(0) on empty bins with a small floor.
    expected_pct = np.where(expected_pct == 0, 1e-6, expected_pct)
    actual_pct = np.where(actual_pct == 0, 1e-6, actual_pct)

    psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return float(psi)


def compute_drift_report(
    training_features: pd.DataFrame,
    current_features: pd.DataFrame,
    training_scores: np.ndarray,
    current_scores: np.ndarray,
    pr_auc_baseline: float,
    pr_auc_current: float,
    top_features: list[str],
    tier: int = 1,
) -> DriftReport:
    """
    Runs the real PSI (per top-SHAP feature), KS (on the score distribution),
    and performance-drift (PR-AUC delta) checks in one call, and evaluates
    them against the Section 9 Tier thresholds.

    top_features should be the real top-10 SHAP features from Section 6's
    explainability step — drift on features the model doesn't actually rely
    on matters far less than drift on the ones driving its decisions.
    """
    feature_psi = {
        feat: population_stability_index(
            training_features[feat].values, current_features[feat].values
        )
        for feat in top_features
    }

    ks_stat, ks_pvalue = ks_2samp(training_scores, current_scores)

    return DriftReport(
        feature_psi=feature_psi,
        score_ks_statistic=float(ks_stat),
        score_ks_pvalue=float(ks_pvalue),
        pr_auc_baseline=pr_auc_baseline,
        pr_auc_current=pr_auc_current,
        tier=tier,
    )


def early_vs_late_window_proxy(df: pd.DataFrame, time_col: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Section 9's documented proxy for this dataset's real limitation: only a
    ~48-hour window exists, so a genuine multi-period drift run isn't
    possible. This splits the real Time column into early vs. late halves
    as the disclosed structural stand-in until real multi-period data exists
    (Section 21 Phase 8).
    """
    midpoint = df[time_col].median()
    early = df[df[time_col] <= midpoint]
    late = df[df[time_col] > midpoint]
    return early, late
