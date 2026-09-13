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

RUN useradd --create-home --shell /bin/bash apiuser \
    && chown -R apiuser:apiuser /app
USER apiuser

ENV MODEL_PATH=/app/model/champion_model.pkl \
    MODEL_VERSION=unset-version \
    DECISION_THRESHOLD=0.5

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
