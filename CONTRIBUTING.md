# Contributing

This repo follows a small set of non-negotiable rules carried across every notebook in it. Read this before adding or editing anything.

## The rules

1. **Zero-fabrication.** Every number that appears in a notebook, report, or dashboard must be computed live by real code against real data (or a real prior notebook's real on-disk output). Anything that isn't — a placeholder, a projection, a round number — must be labeled `ASSUMPTION` with a one-line source/rationale, never presented as a measured result.
2. **RANDOM_SEED = 42**, set once, used everywhere a random process appears (train/test splits, CV folds, bootstrap resampling, model `random_state`).
3. **WARP** — before any heavy ML import, set thread-ceiling environment variables (`OMP_NUM_THREADS`, etc.) via `os.environ.setdefault(...)` so the notebook never claims 100% of the machine's CPU/RAM. Target ~92–93%, never higher.
4. **One notebook = one markdown intro cell + one consolidated code cell.** Keeps every notebook copy-paste-runnable and diff-friendly.
5. **Idempotent, path-safe output.** Every notebook writes to a fixed `reports/nb<N>_results/` path and can be re-run safely — never appends duplicate files, never assumes a hardcoded absolute path exists (use the repo-root-detection pattern already in every notebook).
6. **Downstream notebooks (NB10+) never recompute.** If a report or dashboard needs a number NB1–NB9 already computed, it reads that notebook's real JSON/JSONL output — never re-derives it. If a prerequisite notebook hasn't been run, fail loudly (`SystemExit` naming exactly what's missing), never silently substitute a guess.
7. **Never fabricate a human decision.** Sign-off checkboxes, approvals, names, dates, and signatures are always left blank for a real person to fill in — no notebook may auto-approve anything.

## Before opening a PR

- Run `python scripts/check_notebook_syntax.py` — validates every notebook under `notebooks/` parses and its code cell is syntactically valid Python.
- Run `pytest tests/test_app_smoke.py -v` and `python tests/_smoke_test.py` — both use synthetic data only and check code correctness, not project results.
- If you touched `src/`, make sure every notebook that imports the changed module still runs end-to-end on the real dataset before merging (CI only checks syntax, not real-data correctness — that verification is manual, per this project's standing execution-boundary rule).

## Style

- Google/NumPy-style docstrings, type hints on new functions, PEP 8.
- No hardcoded secrets, credentials, or PII.
- No absolute local file paths printed in notebook output (this repo is public).
