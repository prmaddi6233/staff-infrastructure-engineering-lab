# Architecture and assumptions

Status: proposed reference architecture. Implemented slice: local SQLite recovery gate only.

Assume a hypothetical mobile consumer app with authentication, discovery, matching and
messaging. Traffic volume, regulatory residency, team size, existing dependencies, budget
and CMB's actual deployment are unknown. Product and security discovery must precede any
real service selection or migration. EKS is an interview design constraint, not a conclusion
that every small consumer service needs Kubernetes; a managed container service reduces
operational overhead when scheduling requirements do not justify it.

## Boundaries and dependency order

Edge terminates TLS and applies abuse controls; it routes to private API capacity.
PostgreSQL holds acknowledged durable writes; Redis would be an expendable cache, never
the sole store of accepted messages. A transactional outbox should bridge database writes
and asynchronous delivery to avoid acknowledging a message then losing its queue event.
Queue consumers need deduplication and bounded retries with a dead-letter queue. An outbox
and consumers are proposed, not implemented in this lab.

Restore ordering: identity and keys → network and DNS → database → queue/outbox replay →
API → workers → external journey checks → controlled traffic restoration. Cache is rebuilt
from authoritative data. Do not replay side effects such as notifications without an
idempotency boundary. Stateful rollback needs a schema compatibility plan, not just an old image.

## Failure choices

| Failure | Proposed response | Residual risk / evidence required |
|---|---|---|
| API node or AZ loss | Replicas across zones, reserved headroom, bounded load shedding | Spare capacity, IPs and DB failover must be load tested |
| Slow database | Connection cap, per-request deadline, bounded retry only for safe operations | Latency amplification and transaction ambiguity |
| Cache outage | Rate-limited fallback or degraded discovery | Database stampede; never bypass authorization |
| Queue backlog | Backpressure and oldest-message-age alert | Worker scale limited by downstream capacity |
| Bad release | Canary by journey SLIs; stop then revert compatible image | Data migrations may require forward repair |
| Regional loss | Fenced restore into recovery region | Replication lag, identity and DNS dependency |

Start single-region multi-AZ with independently isolated recovery copies. Cross-region
active-active adds conflict resolution, duplicate side effects and cost. Adopt it only if
measured restore duration cannot meet an agreed customer requirement; see ADR-001.

## Architecture review gates

A reviewer must see service owners, load assumptions, data classification, resource-specific
backup support, a tested rollback, capacity during one-zone loss and a comparable cost model.
No Terraform skeleton is included: placeholder IAM and network resources would imply
capabilities the executable local slice cannot verify.
