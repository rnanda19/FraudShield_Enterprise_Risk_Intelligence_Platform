"""
Code-correctness smoke test for the scoring API — synthetic model + synthetic
input only. Confirms the FastAPI app itself has no bugs; produces no real
project result. Run with: pytest test_app_smoke.py -v
(requires: pip install pytest httpx)
"""
import pickle
import numpy as np
from fastapi.testclient import TestClient
from sklearn.ensemble import RandomForestClassifier

import app as app_module

# Build and save a tiny synthetic model so the API's startup model-load path is exercised for real.
X = np.random.RandomState(0).randn(50, 29)
y = np.random.RandomState(0).binomial(1, 0.1, 50)
clf = RandomForestClassifier(n_estimators=5, random_state=42).fit(X, y)
with open("/tmp/_smoke_model.pkl", "wb") as f:
    pickle.dump(clf, f)

app_module.MODEL_PATH = "/tmp/_smoke_model.pkl"


def test_health_and_score():
    with TestClient(app_module.app) as client:
        health = client.get("/health").json()
        assert health["model_loaded"] is True

        features = {c: 0.0 for c in app_module.EXPECTED_FEATURE_COLUMNS}
        resp = client.post("/score", json={"features": features})
        assert resp.status_code == 200
        body = resp.json()
        assert 0.0 <= body["fraud_probability"] <= 1.0
        assert body["decision"] in ("FLAG", "PASS")

        missing_resp = client.post("/score", json={"features": {"V1": 0.0}})
        assert missing_resp.status_code == 422

    print("APP SMOKE TEST PASSED (synthetic model + synthetic input only).")
