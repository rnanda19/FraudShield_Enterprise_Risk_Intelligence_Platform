#!/usr/bin/env python3
"""CI-invoked structural/syntax check for every notebook in this repo.

Does NOT execute any notebook (this project's standing rule: Claude/CI never
runs the real pipeline against real data — only the user's own machine does).
Checks only that:
  1. every .ipynb under notebooks/ is valid JSON / valid nbformat,
  2. every code cell's source is syntactically valid Python (ast.parse).

Exit code 0 = all notebooks pass; 1 = at least one failure (details printed).
"""
import ast
import sys
from pathlib import Path

try:
    import nbformat
except ImportError:
    nbformat = None

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"


def check_notebook(path: Path) -> list[str]:
    errors = []
    try:
        if nbformat is not None:
            nb = nbformat.read(str(path), as_version=4)
            cells = nb.cells
        else:
            import json
            nb = json.loads(path.read_text(encoding="utf-8"))
            cells = nb.get("cells", [])
    except Exception as e:  # noqa: BLE001
        return [f"could not parse notebook JSON/nbformat: {e}"]

    for i, cell in enumerate(cells):
        cell_type = cell.get("cell_type") if isinstance(cell, dict) else cell.cell_type
        if cell_type != "code":
            continue
        source = cell.get("source") if isinstance(cell, dict) else cell.source
        if isinstance(source, list):
            source = "".join(source)
        try:
            ast.parse(source)
        except SyntaxError as e:
            errors.append(f"cell {i}: SyntaxError: {e}")
    return errors


def main() -> int:
    if not NOTEBOOKS_DIR.exists():
        print(f"No notebooks/ directory found at {NOTEBOOKS_DIR}")
        return 1

    notebook_paths = sorted(NOTEBOOKS_DIR.rglob("*.ipynb"))
    if not notebook_paths:
        print("No .ipynb files found under notebooks/")
        return 1

    any_failed = False
    for path in notebook_paths:
        rel = path.relative_to(REPO_ROOT)
        errors = check_notebook(path)
        if errors:
            any_failed = True
            print(f"[FAIL] {rel}")
            for err in errors:
                print(f"    {err}")
        else:
            print(f"[OK]   {rel}")

    print()
    if any_failed:
        print("Notebook syntax check: FAILED")
        return 1
    print(f"Notebook syntax check: PASSED ({len(notebook_paths)} notebooks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
