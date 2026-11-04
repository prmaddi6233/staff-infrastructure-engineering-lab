# EKS reliability design

Status: proposed; no cluster or manifests are deployed or validated here.

Use a small managed On-Demand node group for critical system components and predictable API
capacity. Evaluate Karpenter for elastic workers after interruption and replacement tests.
Do not promise an exact Spot/On-Demand percentage from scheduling weights. Keep disruption
budgets separate from capacity targets and validate replacement supply during scarcity.

Spread API replicas over nodes and zones with topology constraints. Size requests using
measurements, reserve system resources and model one-zone loss plus rollout surge. An overly
strict spread constraint can leave pods Pending when a zone is unavailable; test the chosen
scheduling trade-off explicitly. PDBs constrain voluntary evictions, not involuntary AZ loss,
and cannot create spare capacity. A one-replica service with zero allowed disruptions can
block drain indefinitely.

Readiness means able to serve; liveness checks local process progress, avoiding restarts
merely because PostgreSQL is slow. Add startup probes for warm-up. On SIGTERM, stop accepting
new work, remove readiness and drain within the termination grace period and load-balancer
deregistration budget. Set application deadlines shorter than upstream request deadlines.

| Control | Proposed verification | Failure signal |
|---|---|---|
| HPA on request rate / queue depth | Load ramp with bounded downstream connection pool | Rising latency despite more pods |
| Node scale-out | Cold start under subnet IP and EC2 quota pressure | Pending pods, exhausted IPs |
| PDB and topology | Drain one node, then simulate zone unavailability separately | Blocked voluntary eviction or missing capacity |
| Overload | Cap concurrency, reject excess work with explicit retry guidance | Retry amplification and DB saturation |
| Upgrade | Check API removals, add-on and CSI compatibility; canary new node group | DNS, network, mount or readiness regression |

Upgrade control planes only after compatibility and backup checks. There is no generic
in-place control-plane downgrade; node-group/image rollback and workload rollback solve
narrower problems. Use a replacement cluster only when rebuild, endpoint and data migration
have already been rehearsed. Treat database schema changes as a separate release risk.

Next milestone is an offline kind integration drill with real pod eviction and continuous
synthetic requests. This is tracked as outstanding work, not implied by the SQLite tests.

References checked 2026-11-04:
[AWS reliability](https://docs.aws.amazon.com/eks/latest/best-practices/reliability.html),
[application availability](https://docs.aws.amazon.com/eks/latest/best-practices/application.html),
[upgrades](https://docs.aws.amazon.com/eks/latest/best-practices/cluster-upgrades.html).
