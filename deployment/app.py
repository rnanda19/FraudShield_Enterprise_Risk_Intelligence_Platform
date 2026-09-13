"""
app.py — Real, runnable FastAPI scoring service for the Fraud Detection
Platform — Master Playbook Section 17.4 (API contract + containerization),
Phase 5 of the Section 21 Ultra-Powerful Execution Roadmap.

Design choices, and why (all real, none decorative):
  - Model is loaded ONCE at startup (module-level singleton), not per
    request — this is the HYPER standard's "reused resource" rule and
    matters here because re-loading a pickled ensemble model per request
    would dominate latency.
  - /score never returns or logs the raw input Amount/Time alongside a PII
    identifier — this dataset does not carry account/customer IDs, but the
    contract is written as if it might, per Section 19's data-security
    requirement (least-privilege: this API can score, it cannot read or
    export the underlying training data).
  - The model artifact path, decision threshold, and model version are all
    externalized via environment variables — nothing about a specific
    trained model is hard-coded, so this file works for the real champion
    model you produce, unmodified.
  - Every response includes model_version and threshold_used, so a decision
    made today is always traceable to the exact model/threshold that made
    it — required for the model-card / governance trail in Section 11/19.

Run locally (after you have a real trained model saved to MODEL_PATH):
    MODEL_PATH=./champion_model.pkl MODEL_VERSION=v1.0.0 DECISION_THRESHOLD=0.5 \
      uvicorn app:app --host 0.0.0.0 --port 8000

This file is written, not executed here, per the standing execution-
boundary rule — you run it against your real trained model.
"""

from __future__ import annotations

import logging
import os
import pickle
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional

import numpy as np
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fraud_scoring_api")

MODEL_PATH = os.environ.get("MODEL_PATH", "./champion_model.pkl")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "unset-version")
DECISION_THRESHOLD = float(os.environ.get("DECISION_THRESHOLD", "0.5"))
EXPECTED_FEATURE_COLUMNS = [f"V{i}" for i in range(1, 29)] + ["Amount"]  # matches creditcard.csv schema minus Time/Class

_model = None
_model_load_error: Optional[str] = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Loads the model ONCE at startup (module-level singleton) — the HYPER
    standard's 'reused resource' rule, using FastAPI's current (non-deprecated)
    lifespan pattern rather than the deprecated on_event('startup') hook."""
    global _model, _model_load_error
    try:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        logger.info("Model loaded from %s (version=%s)", MODEL_PATH, MODEL_VERSION)
    except Exception as exc:  # noqa: BLE001 — startup must report, not crash silently
        _model_load_error = str(exc)
        logger.error("MODEL FAILED TO LOAD at startup: %s", exc)
    yield


app = FastAPI(
    title="Fraud Detection Scoring API",
    version=MODEL_VERSION,
    description="Real-time fraud-probability scoring service. See Master Playbook Section 17.4.",
    lifespan=lifespan,
)


class TransactionRequest(BaseModel):
    features: dict[str, float] = Field(
        ..., description="Real feature dict, e.g. {'V1': -1.36, ..., 'V28': -0.02, 'Amount': 149.62}"
    )


class ScoreResponse(BaseModel):
    request_id: str
    fraud_probability: float
    decision: str  # "FLAG" or "PASS"
    threshold_used: float
    model_version: str
    latency_ms: float


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok" if _model is not None else "degraded",
        "model_loaded": _model is not None,
        "model_load_error": _model_load_error,
    }


@app.get("/model_info")
def model_info() -> dict:
    return {
        "model_version": MODEL_VERSION,
        "decision_threshold": DECISION_THRESHOLD,
        "expected_feature_columns": EXPECTED_FEATURE_COLUMNS,
        "model_loaded": _model is not None,
    }


@app.post("/score", response_model=ScoreResponse)
def score(req: TransactionRequest, request: Request) -> ScoreResponse:
    if _model is None:
        raise HTTPException(status_code=503, detail=f"Model not loaded: {_model_load_error}")

    missing = [c for c in EXPECTED_FEATURE_COLUMNS if c not in req.features]
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing required features: {missing}")

    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    row = np.array([[req.features[c] for c in EXPECTED_FEATURE_COLUMNS]], dtype=np.float32)
    try:
        proba = float(_model.predict_proba(row)[0, 1])
    except Exception as exc:  # noqa: BLE001
        logger.error("[%s] scoring failed: %s", request_id, exc)
        raise HTTPException(status_code=500, detail="Scoring failed") from exc

    decision = "FLAG" if proba >= DECISION_THRESHOLD else "PASS"
    latency_ms = (time.perf_counter() - start) * 1000.0

    logger.info("[%s] decision=%s proba=%.6f latency_ms=%.2f", request_id, decision, proba, latency_ms)

    return ScoreResponse(
        request_id=request_id,
        fraud_probability=proba,
        decision=decision,
        threshold_used=DECISION_THRESHOLD,
        model_version=MODEL_VERSION,
        latency_ms=round(latency_ms, 3),
    )
