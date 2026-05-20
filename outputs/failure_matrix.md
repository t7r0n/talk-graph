# Failure Matrix: Talk Graph

| Scenario | Failure mode | Metric | Gate | Evidence |
| --- | --- | --- | --- | --- |
| founder evidence replay | founder_drift | founder_coverage | block release until cited evidence is regenerated | ev_0000 |
| fireside operator packet | fireside_blindspot | fireside_latency | accept only if decision claims cite fixture evidence | ev_0007 |
| fireside operator packet | fireside_blindspot | fireside_latency | accept only if decision claims cite fixture evidence | ev_0011 |
| monthly regression harness | monthly_misroute | monthly_precision | open a regression issue with trace and benchmark delta | ev_0014 |
| talks boundary probe | talks_gap | talks_risk | route to reviewer with evidence packet | ev_0021 |
| monthly regression harness | monthly_misroute | monthly_precision | open a regression issue with trace and benchmark delta | ev_0022 |
| founder evidence replay | founder_drift | founder_coverage | block release until cited evidence is regenerated | ev_0028 |
