"""
notebook_01_starter.py
Real, runnable starting point for Fraud Detection Platform Notebook 01
(Business Understanding & EDA) — Master Playbook Section 5.

This is the exact structure needed to produce the real, verified numbers
that Section 2 of the playbook currently states — run this on YOUR machine
against your real creditcard.csv to get YOUR real numbers, replacing the
already-verified ones in Section 2 (they should match, since Section 2 was
built the same way — this script is what makes Phase 1 of Section 21
actually executable end to end rather than something to rebuild from scratch).

Per the standing execution-boundary rule, this script is written but not
executed here — run it yourself and treat its printed output as your real
Section 2/18 evidence.
"""

import pandas as pd
import numpy as np

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

DATA_PATH = "creditcard.csv"  # point this at your real file


def load_and_verify(path: str = DATA_PATH) -> pd.DataFrame:
    """Section 2: load and verify — every fact printed here is real, not assumed."""
    df = pd.read_csv(path)

    print("=" * 70)
    print("SECTION 2 VERIFICATION — real values from THIS run")
    print("=" * 70)
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}  -> {list(df.columns)}")
    print(f"Dtypes:\n{df.dtypes.value_counts()}")
    print(f"Nulls total: {df.isnull().sum().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Class balance:\n{df['Class'].value_counts()}")
    print(f"Class balance (%):\n{(df['Class'].value_counts(normalize=True) * 100).round(4)}")
    print(f"Time range: {df['Time'].min()} to {df['Time'].max()} seconds "
          f"(~{(df['Time'].max() - df['Time'].min()) / 3600:.1f} hours)")
    print(f"Amount: mean={df['Amount'].mean():.2f}, median={df['Amount'].median():.2f}, "
          f"max={df['Amount'].max():.2f}")
    return df


def investigate_duplicates(df: pd.DataFrame) -> dict:
    """
    Section 18.1's duplicate-handling decision, made for real rather than
    assumed: reports whether the duplicate rows are concentrated among fraud
    or legitimate transactions, and whether they cluster in Time — evidence
    for (not a substitute for) your real drop-vs-keep decision.
    """
    dupes = df[df.duplicated(keep=False)]
    report = {
        "n_duplicate_rows": int(df.duplicated().sum()),
        "duplicates_by_class": dupes["Class"].value_counts().to_dict() if len(dupes) else {},
        "duplicate_time_span_seconds": (
            float(dupes["Time"].max() - dupes["Time"].min()) if len(dupes) else None
        ),
    }
    print("=" * 70)
    print("SECTION 18.1 DUPLICATE INVESTIGATION — real evidence, your decision")
    print("=" * 70)
    for k, v in report.items():
        print(f"{k}: {v}")
    print("Decision to drop or retain must be made and justified here, in writing, "
          "based on the real evidence above — not assumed either way.")
    return report


def class_imbalance_summary(df: pd.DataFrame) -> None:
    fraud_rate = df["Class"].mean()
    print("=" * 70)
    print("CLASS IMBALANCE — real number driving Section 6's technique choice")
    print("=" * 70)
    print(f"Real fraud rate: {fraud_rate:.6%}")
    print(f"Real fraud count: {int(df['Class'].sum())} / {len(df):,}")


if __name__ == "__main__":
    df = load_and_verify()
    investigate_duplicates(df)
    class_imbalance_summary(df)
    print("\nNotebook 01 starter complete. Paste the printed output above back "
          "as your real Section 2/18 evidence.")
