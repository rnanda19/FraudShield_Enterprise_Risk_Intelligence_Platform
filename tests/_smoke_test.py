"""
Code-correctness smoke test ONLY — synthetic random data, not project data.
This verifies the modules run without bugs; it produces no real project
result and must never be cited as one. Mirrors the "fixture run" step of
the Master Playbook's own financial-impact verification sequence.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

np.random.seed(0)
n = 500
X = pd.DataFrame(np.random.randn(n, 5), columns=[f"f{i}" for i in range(5)])
y = pd.Series(np.random.binomial(1, 0.05, n))
amounts = np.abs(np.random.randn(n) * 50)

print("Testing class_imbalance_utils...")
import class_imbalance_utils as ciu
cw = ciu.get_class_weight(y)
assert isinstance(cw, dict) and len(cw) == 2
scores = np.random.rand(n)
bt = ciu.best_threshold_by_cost(y.values, scores, 4.41, 9.2, amounts)
assert "threshold" in bt
print("  OK")

print("Testing two_gate_validation...")
import two_gate_validation as tgv
df_fake = X.copy()
df_fake["Class"] = y
g1 = tgv.run_gate1_structural_checks(df_fake, list(X.columns), "Class")
assert isinstance(g1.all_passed, bool)
df_fake["Time"] = np.random.randint(0, 172792, n)
df_fake["Amount"] = amounts
df_fake["pred"] = np.random.binomial(1, 0.05, n)
conc = tgv.concentration_report_by_amount_and_time(df_fake, "Amount", "Time", "Class", "pred")
assert len(conc) > 0
stress = tgv.stress_test_scenario(df_fake, "Amount", 2.0, 3.0, 0.0017)
assert "projected_fraud_loss_usd_or_eur" in stress
print("  OK")

print("Testing drift_monitoring...")
import drift_monitoring as dm
psi = dm.population_stability_index(np.random.randn(300), np.random.randn(300) + 0.1)
assert isinstance(psi, float)
report = dm.compute_drift_report(
    X.iloc[:250], X.iloc[250:], np.random.rand(250), np.random.rand(250),
    0.75, 0.70, list(X.columns)[:3], tier=1,
)
assert isinstance(report.any_alert, bool)
early, late = dm.early_vs_late_window_proxy(df_fake, "Time")
assert len(early) + len(late) == n
print("  OK")

print("Testing model_benchmark...")
import model_benchmark as mb
candidates = {"rf1": RandomForestClassifier(n_estimators=10, random_state=42),
              "rf2": RandomForestClassifier(n_estimators=20, random_state=42)}
stage_a = mb.run_stage_a_screening(X, y, candidates)
assert len(stage_a) == 2
top2 = {"rf1": RandomForestClassifier(n_estimators=10, random_state=42),
        "rf2": RandomForestClassifier(n_estimators=20, random_state=42)}
stage_b = mb.run_stage_b_cv(X, y, top2, n_splits=3, n_bootstrap=50)
champ = mb.select_champion(stage_b)
assert champ in top2
temporal_auc = mb.temporal_split_validation(df_fake, "Time", list(X.columns), "Class",
                                             RandomForestClassifier(n_estimators=10, random_state=42))
assert isinstance(temporal_auc, float)
cmp_ext = mb.compare_to_external_benchmark(0.90, 0.70)
assert "investigate_flag" in cmp_ext
print("  OK")

print("Testing model_card_generator...")
import model_card_generator as mcg
card = mcg.ModelCardData(
    model_name="fraud-champion", version="v1.0.0-smoketest",
    training_data_snapshot_id="synthetic", code_commit_hash="abc123",
    intended_use="test", out_of_scope_uses=["n/a"],
    training_data_provenance="synthetic smoke test data",
    known_limitations=["synthetic data only"],
    pr_auc_cv=0.75, pr_auc_cv_bootstrap_ci=(0.70, 0.80),
    pr_auc_temporal_split=0.72, precision_at_threshold=0.9,
    recall_at_threshold=0.7, operating_threshold=0.5,
    external_benchmark_comparison={"note": "synthetic"},
)
md = mcg.render_markdown(card)
html = mcg.render_html(card)
assert "fraud-champion" in md and "<table>" in html
print("  OK")

print("\nALL MODULES PASS THE CODE-CORRECTNESS SMOKE TEST (synthetic data only).")
