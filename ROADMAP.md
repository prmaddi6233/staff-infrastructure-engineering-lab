# Prioritized 30/60/90-day roadmap

Proposed portfolio engineering sequence from project kickoff, not CMB's roadmap or a delivery
commitment. One owner may hold several roles. Dependencies and objective checks take
precedence over dates. Existing local recovery gate is the starting baseline.

| Window | Priority / owner role | Outstanding deliverable | Exit evidence |
|---|---|---|---|
| Days 1–30 | P1 / platform + application | Containerized PostgreSQL recovery with independent acknowledgement ledger | Corruption/stale/replay tests; measured local recovery scope |
| Days 1–30 | P1 / repository owner | Required CI/review settings and supply-chain checks | Protected main, blocked failing PR, tested scan fixtures |
| Days 31–60 | P1 / SRE + application | Journey metrics and tested burn-rate alerts | Good/bad/zero/missing/low-volume fixtures; no PII labels |
| Days 31–60 | P1 / platform | kind node-drain and overload drill | Continuous traffic, real eviction and recovery evidence |
| Days 31–60 | P1 / security | Authenticated backup provenance | Replaced backup+digest rejected; key custody documented |
| Days 61–90 | P2 / recovery + security | AWS service/key support matrix and tabletop | Resource-specific documented restore path; no deployment |
| Days 61–90 | P2 / SRE + finance | Integrate recovery/capacity evidence and cost decision review | Repeated comparable trials; explicit unknowns; linked existing FinOps work |

First gate: demonstrate correct PostgreSQL restoration and reconciliation locally before
adding Kubernetes complexity. Second gate: demonstrate journey behavior under real pod drain
and telemetry loss. Third gate: decide whether cloud proof is justified; any future paid
exercise requires separate budget and execution authorization. Missing objectives generate
specific follow-up tasks rather than being declared production ready.

Product owner: agrees user impact and objectives. Platform owner: reliable mechanism and
cleanup. App owner: correctness and replay safety. Security: independent identity and data
handling. Finance: measurement assumptions. SRE: drills, incident roles and error-budget
policy. Capture one ADR per material trade-off, review evidence fortnightly and narrow scope
when a prerequisite fails. See [actual issue backlog](ISSUE_BACKLOG.md).
