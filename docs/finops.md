# FinOps without weakening reliability

Status: proposed methodology; no savings or live cost results claimed.
Reuse the linked billing analytics, cost intelligence and EKS governance repositories.
This lab adds the decision constraint: an optimization is unacceptable if it exhausts
failure headroom or invalidates a tested recovery objective.

Measure cost per thousand successful logical journey events alongside error-budget burn,
latency and restore-test success. Include compute, DB, storage/backup retention, cross-AZ and
cross-region transfer, NAT/endpoints, logs/traces, CI and on-call operating effort. Failed
requests and retries consume money but must not inflate the successful-event denominator.
For shared infrastructure publish an allocation rule and a separate unallocated balance;
do not manufacture precision from incomplete tags.

| Choice | Cost pressure | Reliability gate |
|---|---|---|
| Spot workers | Lower potential compute cost; interruptions and replacement overhead | Durable queue, idempotent replay, available fallback capacity |
| Smaller API requests | Better packing; higher contention and OOM risk | Peak test with one-zone loss and release surge |
| Recovery region | Copy, key, storage and test costs | Restore exercises and residency approval |
| More telemetry | Ingestion, retention and query cost | Redaction, cardinality budget, minimum diagnostic coverage |
| Commitments | Reduced flexibility | Buy against stable measured baseline after rightsizing |

Use comparable before/after load and a defined observation window. Include rollback and
migration costs and distinguish identified, validated and realized savings. No numerical
savings target is invented. Current local tests incur no cloud resource charges; GitHub
Actions execution remains subject to GitHub's runner and account billing policy.
