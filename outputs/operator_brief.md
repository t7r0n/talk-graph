# Operator Brief: Aalto

Aalto gets a local, deterministic pressure test around founder, talks, and monthly. The useful part is not the dashboard; it is the repeatable evidence path from fixture to failure to operator action.

## Highest-leverage checks

- founder evidence replay -> block release until cited evidence is regenerated (founder_coverage, evidence ev_0132).
- fireside operator packet -> accept only if decision claims cite fixture evidence (talks_risk, evidence ev_0099).
- monthly regression harness -> open a regression issue with trace and benchmark delta (monthly_precision, evidence ev_0110).
- talks boundary probe -> route to reviewer with evidence packet (fireside_latency, evidence ev_0033).

## What makes this useful

The workflow is intentionally local and deterministic. A reviewer can run the same fixture set, inspect the evidence IDs, open the dashboard, and see exactly why a recommendation passed, went to review, or blocked.
