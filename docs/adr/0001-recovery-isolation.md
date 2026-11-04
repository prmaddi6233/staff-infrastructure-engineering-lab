# ADR-001: Separate recovery boundary before active-active

Status: proposed for the hypothetical cloud architecture. Date: 2026-11-04.

Context: multi-AZ availability does not establish recovery after logical corruption or
workload administrative compromise. Actual workload scale and acceptable loss are unknown.

Decision: start with single-region multi-AZ operation and supported copies in a separately
controlled recovery account; evaluate regional copies using agreed objectives and residency.
Test independent key/identity access and restore ordering before adopting the pattern.

Alternatives: same-account backups cost less operational effort but share administrative
blast radius. Cross-account copies add IAM/KMS and retention complexity. Active-active can
reduce outage duration but requires conflict handling and more capacity/operating cost;
it does not protect against replicated corruption by itself.

Consequences: copy lag and rebuild time may miss objectives; organization-wide compromise
remains a risk. Retention can create costs that cannot be immediately undone. No cloud
implementation or protection guarantee is claimed.

Validation / revisit: service-support matrix, denial tests, acknowledged-write reconciliation
and independent restore timings. Revisit topology if repeated drills cannot meet agreed
RTO/RPO at acceptable cost. Roll back a design pilot by stopping new copy policies only
after retention/legal review; do not delete recovery points as routine rollback.
