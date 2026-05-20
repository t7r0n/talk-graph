from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


COMPANY = "Aalto"
REPO = "talk-graph"
PROJECT_TERMS = [
    "founder",
    "talks",
    "monthly",
    "fireside",
    "produces",
    "minutes",
    "dense",
    "unindexed"
]
PROJECT_METRICS = [
    "founder_coverage",
    "talks_risk",
    "monthly_precision",
    "fireside_latency"
]
PROJECT_FAILURES = [
    "founder_drift",
    "talks_gap",
    "monthly_misroute",
    "fireside_blindspot"
]
PROJECT_ARCHETYPES = [
    {
        "name": "founder evidence replay",
        "trigger": "founder signal changes while talks context is stale",
        "expected": "block release until cited evidence is regenerated"
    },
    {
        "name": "talks boundary probe",
        "trigger": "talks handoff crosses a policy or trust boundary",
        "expected": "route to reviewer with evidence packet"
    },
    {
        "name": "monthly regression harness",
        "trigger": "monthly behavior regresses against the last accepted fixture",
        "expected": "open a regression issue with trace and benchmark delta"
    },
    {
        "name": "fireside operator packet",
        "trigger": "fireside output needs a human-readable audit packet",
        "expected": "accept only if decision claims cite fixture evidence"
    }
]
PROJECT_DIRECTION = "A retrieval augmented founder coaching surface that turns every Founder Talk into clickable, citable, searchable advice - and stitches each lesson to the alumni companies it influenced."


def _short(value: str, limit: int = 44) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "..."


def _wrap(value: str, limit: int = 48, max_lines: int = 3) -> list[str]:
    words = " ".join(value.split()).split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if len(candidate) <= limit:
            current.append(word)
            continue
        if current:
            lines.append(" ".join(current))
        current = [word]
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = _short(lines[-1], max(8, limit - 1))
    return lines or [""]


def _text_block(
    value: str,
    *,
    x: int,
    y: int,
    css: str,
    limit: int,
    max_lines: int,
    line_height: int,
) -> str:
    lines = _wrap(value, limit=limit, max_lines=max_lines)
    parts = [f'<text class="{css}" x="{x}" y="{y}">']
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{_escape(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def build_signal_model(rows: list[dict[str, Any]], clusters: list[dict[str, Any]]) -> dict[str, Any]:
    total = max(1, len(rows))
    blocked = sum(1 for row in rows if row["status"] == "block")
    review = sum(1 for row in rows if row["status"] == "review")
    evidence_density = round(sum(len(row["evidence_quote"].split()) for row in rows) / total, 2)
    pressure = round((blocked * 1.9 + review) / total, 4)
    ranked_clusters = sorted(
        clusters,
        key=lambda item: (item["blocks"], item["reviews"], item["mean_severity"]),
        reverse=True,
    )
    leverage = []
    for index, cluster in enumerate(ranked_clusters[:4], start=1):
        metric = PROJECT_METRICS[(index - 1) % len(PROJECT_METRICS)]
        failure = PROJECT_FAILURES[(index - 1) % len(PROJECT_FAILURES)]
        leverage.append(
            {
                "rank": index,
                "scenario": cluster["scenario"],
                "metric": metric,
                "failure_mode": failure,
                "evidence": cluster["top_evidence_id"],
                "operator_action": cluster["recommended_action"],
                "severity": cluster["mean_severity"],
            }
        )
    return {
        "company": COMPANY,
        "repo": REPO,
        "terms": PROJECT_TERMS,
        "metrics": PROJECT_METRICS,
        "failure_modes": PROJECT_FAILURES,
        "evidence_density": evidence_density,
        "pressure_index": pressure,
        "blocked_share": round(blocked / total, 4),
        "review_share": round(review / total, 4),
        "top_leverage_points": leverage,
        "readout": (
            f"{COMPANY} gets a local, deterministic pressure test around "
            f"{PROJECT_TERMS[0]}, {PROJECT_TERMS[1]}, and {PROJECT_TERMS[2]}. "
            f"The useful part is not the dashboard; it is the repeatable evidence path "
            f"from fixture to failure to operator action."
        ),
    }


def write_showcase_assets(
    outputs: Path,
    profile: dict[str, Any],
    rows: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    model: dict[str, Any],
) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    (outputs / "operator_brief.md").write_text(_operator_brief(model), encoding="utf-8")
    (outputs / "architecture.json").write_text(json.dumps(_architecture(model), indent=2), encoding="utf-8")
    (outputs / "project_working.svg").write_text(_working_svg(model), encoding="utf-8")
    (outputs / "evidence_map.svg").write_text(_evidence_svg(model), encoding="utf-8")


def _operator_brief(model: dict[str, Any]) -> str:
    lines = [
        f"# Operator Brief: {COMPANY}",
        "",
        model["readout"],
        "",
        "## Highest-leverage checks",
        "",
    ]
    for point in model["top_leverage_points"]:
        lines.append(
            f"- {point['scenario']} -> {point['operator_action']} "
            f"({point['metric']}, evidence {point['evidence']})."
        )
    lines.extend(
        [
            "",
            "## What makes this useful",
            "",
            "The workflow is intentionally local and deterministic. A reviewer can run the same fixture set, inspect the evidence IDs, open the dashboard, and see exactly why a recommendation passed, went to review, or blocked.",
        ]
    )
    return "\n".join(lines) + "\n"


def _architecture(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "layers": [
            {"name": "synthetic_fixture_replay", "purpose": f"exercise {PROJECT_TERMS[0]} and {PROJECT_TERMS[1]} cases"},
            {"name": "domain_strategy", "purpose": f"score {PROJECT_METRICS[0]} and {PROJECT_METRICS[1]}"},
            {"name": "evidence_lock", "purpose": "reject narrative claims without fixture evidence IDs"},
            {"name": "operator_packet", "purpose": "emit dashboard, SVG readout, CSV, markdown report, and demo pack"},
        ],
        "pressure_index": model["pressure_index"],
        "top_leverage_points": model["top_leverage_points"],
    }


def _working_svg(model: dict[str, Any]) -> str:
    bars = []
    insight_cards = []
    colors = ["#2563eb", "#0891b2", "#10b981", "#f59e0b"]
    for index, point in enumerate(model["top_leverage_points"]):
        width = 214 + int(float(point["severity"]) * 58)
        y = 344 + index * 68
        bars.append(
            f'<text x="84" y="{y - 13}" class="label">{_escape(point["metric"].replace("_", " "))}</text>'
            f'<text x="454" y="{y - 13}" class="evidence">{_escape(point["evidence"])}</text>'
            f'<rect x="84" y="{y}" width="398" height="16" rx="8" fill="#e2e8f0"/>'
            f'<rect x="84" y="{y}" width="{min(width, 398)}" height="16" rx="8" fill="{colors[index % len(colors)]}"/>'
            f'<text x="84" y="{y + 43}" class="caption">{_escape(_short(point["scenario"], 46))}</text>'
        )
        card_x = 620 + (index % 2) * 244
        card_y = 316 + (index // 2) * 154
        insight_cards.append(
            f'<rect class="tile" x="{card_x}" y="{card_y}" width="212" height="126" rx="8"/>'
            f'<text class="rank" x="{card_x + 18}" y="{card_y + 30}">0{index + 1}</text>'
            + _text_block(
                point["operator_action"],
                x=card_x + 18,
                y=card_y + 58,
                css="cardtext",
                limit=24,
                max_lines=3,
                line_height=18,
            )
            + f'<text class="evidence" x="{card_x + 18}" y="{card_y + 108}">{_escape(point["evidence"])}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="650" viewBox="0 0 1120 650" role="img" aria-label="{_escape(COMPANY)} project working dashboard preview">
  <defs>
    <style>
      .bg {{ fill: #f6f8fb; }}
      .panel {{ fill: #ffffff; stroke: #d8e1ec; stroke-width: 1.1; }}
      .tile {{ fill: #ffffff; stroke: #d8e1ec; stroke-width: 1.1; }}
      .title {{ font: 760 31px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #111827; }}
      .sub {{ font: 420 15px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #475569; }}
      .label {{ font: 680 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #1f2937; }}
      .caption {{ font: 500 12px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #64748b; }}
      .small {{ font: 600 12px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #64748b; }}
      .metric {{ font: 760 28px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #0f172a; }}
      .rank {{ font: 760 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #2563eb; }}
      .cardtext {{ font: 640 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #172033; }}
      .evidence {{ font: 680 12px ui-monospace, SFMono-Regular, Menlo, monospace; fill: #334155; }}
    </style>
  </defs>
  <rect class="bg" width="1120" height="650" rx="0"/>
  <rect class="panel" x="28" y="28" width="1064" height="594" rx="8"/>
  <text class="title" x="64" y="76">Talk Graph Control Room</text>
  {_text_block(PROJECT_DIRECTION, x=64, y=108, css="sub", limit=82, max_lines=2, line_height=22)}
  <rect class="tile" x="64" y="160" width="220" height="84" rx="8"/>
  <text class="small" x="84" y="188">pressure index</text>
  <text class="metric" x="84" y="224">{model["pressure_index"]}</text>
  <rect class="tile" x="306" y="160" width="220" height="84" rx="8"/>
  <text class="small" x="326" y="188">evidence density</text>
  <text class="metric" x="326" y="224">{model["evidence_density"]}</text>
  <rect class="tile" x="548" y="160" width="508" height="84" rx="8"/>
  <text class="small" x="568" y="188">highest leverage path</text>
  {_text_block(model["top_leverage_points"][0]["scenario"], x=568, y=218, css="label", limit=54, max_lines=1, line_height=16)}
  <rect class="tile" x="64" y="286" width="472" height="314" rx="8"/>
  <text class="label" x="84" y="316">risk signals from fixture replay</text>
  {''.join(bars)}
  <text class="label" x="620" y="286">operator actions that need evidence</text>
  {''.join(insight_cards)}
</svg>
"""


def _evidence_svg(model: dict[str, Any]) -> str:
    nodes = []
    edges = []
    x_positions = [64, 304, 564, 780]
    for index, point in enumerate(model["top_leverage_points"]):
        y = 116 + index * 90
        nodes.append(
            f'<rect class="scenario" x="{x_positions[0]}" y="{y}" width="186" height="58" rx="8"/>'
            + _text_block(point["scenario"], x=x_positions[0] + 14, y=y + 24, css="node", limit=22, max_lines=2, line_height=17)
        )
        nodes.append(
            f'<rect class="failure" x="{x_positions[1]}" y="{y}" width="190" height="58" rx="8"/>'
            f'<text x="{x_positions[1] + 14}" y="{y + 34}" class="node">{_escape(point["failure_mode"].replace("_", " "))}</text>'
        )
        nodes.append(
            f'<rect class="evidencebox" x="{x_positions[2]}" y="{y}" width="148" height="58" rx="8"/>'
            f'<text x="{x_positions[2] + 28}" y="{y + 36}" class="evidence">{_escape(point["evidence"])}</text>'
        )
        nodes.append(
            f'<rect class="action" x="{x_positions[3]}" y="{y}" width="276" height="58" rx="8"/>'
            + _text_block(point["operator_action"], x=x_positions[3] + 14, y=y + 24, css="node", limit=34, max_lines=2, line_height=17)
        )
        edges.extend([
            f'<path d="M250 {y + 29} L304 {y + 29}" class="edge"/>',
            f'<path d="M494 {y + 29} L564 {y + 29}" class="edge"/>',
            f'<path d="M712 {y + 29} L780 {y + 29}" class="edge"/>',
        ])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="500" viewBox="0 0 1120 500" role="img" aria-label="{_escape(COMPANY)} evidence map">
  <defs>
    <style>
      .bg {{ fill:#f8fafc; }}
      .panel {{ fill:#ffffff; stroke:#d8e1ec; stroke-width:1.1; }}
      .title {{ font: 760 28px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill:#111827; }}
      .node {{ font: 620 13px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill:#1f2937; }}
      .head {{ font: 700 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill:#64748b; }}
      .evidence {{ font: 720 13px ui-monospace, SFMono-Regular, Menlo, monospace; fill:#334155; }}
      .edge {{ stroke:#94a3b8; stroke-width:2; fill:none; marker-end:url(#arrow); }}
      .scenario {{ fill:#eef2ff; stroke:#dbe4ff; }}
      .failure {{ fill:#ecfeff; stroke:#bfecf2; }}
      .evidencebox {{ fill:#fef9c3; stroke:#f5e889; }}
      .action {{ fill:#dcfce7; stroke:#b8efca; }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/></marker>
  </defs>
  <rect class="bg" width="1120" height="500"/>
  <rect class="panel" x="28" y="28" width="1064" height="444" rx="8"/>
  <text x="56" y="70" class="title">{_escape(COMPANY)} evidence path</text>
  <text x="64" y="104" class="head">scenario</text><text x="304" y="104" class="head">failure mode</text><text x="564" y="104" class="head">evidence</text><text x="780" y="104" class="head">operator action</text>
  {''.join(edges)}
  {''.join(nodes)}
</svg>
"""
