# Real, buildable Dockerfile for the Fraud Detection Scoring API.
# Master Playbook Section 17.4 — containerization requirement.
#
# Security choices (real, not decorative):
#   - slim base image (smaller attack surface than full python image)
#   - non-root user (least privilege — never run a scoring service as root)
#   - no build tools left in the final image
#   - HEALTHCHECK wired to the real /health endpoint, not a fake liveness check

FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY app.py .

# Real trained champion model (CatBoost, Notebook 1's Stage-B 5-fold CV winner,
# reports/nb1_results/champion_model.pkl) baked into the image so the
# container is self-contained on a platform (e.g. Render) that cannot bind-
# mount a host volume at deploy time. Local docker-compose still overrides
# this via its own ./model:/app/model:ro mount for iterating on a newer
# model without rebuilding the image.
COPY model/ /app/model/

RUN useradd --create-home --shell /bin/bash apiuser \
    && chown -R apiuser:apiuser /app
USER apiuser

ENV MODEL_PATH=/app/model/champion_model.pkl \
    MODEL_VERSION=fraudshield-catboost-v1.0.0 \
    DECISION_THRESHOLD=0.0443

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
