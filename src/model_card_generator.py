"""
model_card_generator.py
Reusable module — implements Section 11 of the Master Playbook: the
standardized, version-locked Model Card required alongside the financial-
impact package for every champion model.

Populate ModelCardData from your OWN real run's results, then call
render_markdown() / render_html() — this module formats real data you
provide; it never invents a metric.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ModelCardData:
    model_name: str
    version: str  # e.g., "fraud-champion-v1.0.0" per Section 17.3 versioning
    training_data_snapshot_id: str
    code_commit_hash: str

    intended_use: str
    out_of_scope_uses: list[str]

    training_data_provenance: str
    known_limitations: list[str]  # must include the Section 8/18 fairness-scope limitation

    pr_auc_cv: float
    pr_auc_cv_bootstrap_ci: tuple[float, float]
    pr_auc_temporal_split: float
    precision_at_threshold: float
    recall_at_threshold: float
    operating_threshold: float

    external_benchmark_comparison: dict

    monitoring_plan_reference: str = "See Master Playbook Section 9"
    tier: int = 1

    generated_at_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


def render_markdown(card: ModelCardData) -> str:
    limitations = "\n".join(f"- {item}" for item in card.known_limitations)
    out_of_scope = "\n".join(f"- {item}" for item in card.out_of_scope_uses)

    return f"""# Model Card — {card.model_name}

**Version:** {card.version}
**Tier:** {card.tier} (per Master Playbook Section 3)
**Training data snapshot:** {card.training_data_snapshot_id}
**Code commit:** {card.code_commit_hash}
**Generated:** {card.generated_at_utc}

## Intended Use
{card.intended_use}

## Out-of-Scope Uses
{out_of_scope}

## Training Data Provenance
{card.training_data_provenance}

## Performance (real, measured)
| Metric | Value |
|---|---|
| CV PR-AUC | {card.pr_auc_cv:.4f} |
| CV PR-AUC 95% bootstrap CI | [{card.pr_auc_cv_bootstrap_ci[0]:.4f}, {card.pr_auc_cv_bootstrap_ci[1]:.4f}] |
| Temporal-split PR-AUC | {card.pr_auc_temporal_split:.4f} |
| Precision @ operating threshold ({card.operating_threshold:.4f}) | {card.precision_at_threshold:.4f} |
| Recall @ operating threshold | {card.recall_at_threshold:.4f} |

## External Benchmark Comparison (Section 19.4)
{card.external_benchmark_comparison}

## Known Limitations
{limitations}

## Monitoring Plan
{card.monitoring_plan_reference}
"""


def render_html(card: ModelCardData) -> str:
    md = render_markdown(card)
    # Minimal, dependency-free markdown-to-HTML for the specific structure
    # this card always produces (headers, a table, bullet lists).
    lines = md.splitlines()
    html = ["<div class='model-card'>"]
    in_table = False
    for line in lines:
        if line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("|"):
            if "---" in line:
                continue  # skip the markdown header-separator row
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not in_table:
                html.append("<table>")
                in_table = True
            html.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        else:
            if in_table:
                html.append("</table>")
                in_table = False
            if line.startswith("- "):
                html.append(f"<li>{line[2:]}</li>")
            elif line.strip():
                html.append(f"<p>{line}</p>")
    if in_table:
        html.append("</table>")
    html.append("</div>")
    return "\n".join(html)
