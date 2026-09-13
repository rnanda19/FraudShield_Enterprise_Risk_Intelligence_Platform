"""
two_gate_validation.py
Reusable module — implements Section 7 of the Master Playbook: the two-gate
validation architecture, extended with the Stress-Test Scenario sub-gate.

Gate 1 = structural integrity (always computable; passing does not mean the
model is good, only that the pipeline ran correctly).
Gate 2 = statistical robustness + concentration + stress-test scenario
(the gate that can actually fail and should block promotion).

This module reports REAL numbers only — it never asserts a verdict for you;
it returns the evidence and a pass/fail against thresholds YOU set explicitly,
so no threshold is silently assumed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# GATE 1 — Structural Integrity
# ---------------------------------------------------------------------------

@dataclass
class Gate1Result:
    checks: dict[str, bool] = field(default_factory=dict)

    @property
    def all_passed(self) -> bool:
        return all(self.checks.values())


def run_gate1_structural_checks(df: pd.DataFrame, required_columns: list[str],
                                 label_column: str) -> Gate1Result:
    result = Gate1Result()

    result.checks["schema_has_required_columns"] = all(
        c in df.columns for c in required_columns
    )
    result.checks["no_null_in_label"] = df[label_column].isna().sum() == 0
    result.checks["label_is_binary"] = set(df[label_column].unique()).issubset({0, 1})
    result.checks["row_count_positive"] = len(df) > 0
    # No-leakage sanity check: label must not equal a trivial function of
    # itself once cast (catches an accidental duplicate/label-copy column).
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    suspicious_leak_cols = [
        c for c in numeric_cols
        if c != label_column and df[c].corr(df[label_column]) > 0.999
    ]
    result.checks["no_perfect_correlation_leakage"] = len(suspicious_leak_cols) == 0
    if suspicious_leak_cols:
        result.checks["_leak_columns_found"] = suspicious_leak_cols  # diagnostic, not boolean

    return result


# ---------------------------------------------------------------------------
# GATE 2 — Statistical Robustness / Concentration / Stress-Test
# ---------------------------------------------------------------------------

@dataclass
class Gate2Result:
    cv_auc_scores: list[float]
    cv_pr_auc_scores: list[float]
    concentration_report: pd.DataFrame
    stress_test_report: dict

    @property
    def cv_stability_ok(self, max_std: float = 0.03) -> bool:
        return float(np.std(self.cv_pr_auc_scores)) <= max_std


def concentration_report_by_amount_and_time(
    df: pd.DataFrame, amount_col: str, time_col: str,
    y_true_col: str, y_pred_col: str, n_amount_bands: int = 5,
) -> pd.DataFrame:
    """
    Real segment-cut breakdown replacing the demographic cuts unavailable on
    this anonymized dataset (Section 2's disclosed limitation) — false-positive
    and false-negative rates broken out by Amount band and hour-of-day, so
    concentration risk is checked on the real segments that ARE available.
    """
    work = df.copy()
    work["_amount_band"] = pd.qcut(work[amount_col], n_amount_bands, duplicates="drop")
    work["_hour_of_day"] = (work[time_col] // 3600) % 24

    rows = []
    for (band, hour), g in work.groupby(["_amount_band", "_hour_of_day"], observed=True):
        fp = ((g[y_true_col] == 0) & (g[y_pred_col] == 1)).sum()
        fn = ((g[y_true_col] == 1) & (g[y_pred_col] == 0)).sum()
        n = len(g)
        rows.append({
            "amount_band": str(band), "hour_of_day": int(hour), "n": n,
            "false_positive_rate": fp / n if n else np.nan,
            "false_negative_rate": fn / n if n else np.nan,
        })
    return pd.DataFrame(rows)


def stress_test_scenario(
    df: pd.DataFrame, amount_col: str, scenario_volume_multiplier: float,
    scenario_fraud_rate_multiplier: float, base_fraud_rate: float,
) -> dict:
    """
    Real, disclosed hypothetical scenario per Section 7/19: since the exact
    confidential Fed severely-adverse scenario file is not available to a
    portfolio project, this applies a documented, labeled hypothetical shock
    (e.g., 2x transaction volume, 3x fraud rate during a stress event) and
    projects the resulting loss impact on THIS dataset's real Amount
    distribution. Every multiplier is a stated ASSUMPTION, never invented
    silently — pass real historical-analogue multipliers if you have them.
    """
    projected_fraud_rate = base_fraud_rate * scenario_fraud_rate_multiplier
    projected_transaction_count = len(df) * scenario_volume_multiplier
    avg_amount = df[amount_col].mean()

    projected_fraud_count = projected_transaction_count * projected_fraud_rate
    projected_loss = projected_fraud_count * avg_amount

    return {
        "ASSUMPTION_scenario_volume_multiplier": scenario_volume_multiplier,
        "ASSUMPTION_scenario_fraud_rate_multiplier": scenario_fraud_rate_multiplier,
        "base_fraud_rate_real": base_fraud_rate,
        "projected_fraud_rate_under_scenario": projected_fraud_rate,
        "projected_transaction_count": projected_transaction_count,
        "projected_fraud_loss_usd_or_eur": float(projected_loss),
    }
