# ADR-003: Evidence gates eligibility; humans own stateful cutover

Status: accepted for the local gate; cloud rollout portions proposed. Date: 2026-11-04.

Context: success from a restore API or checksum alone does not prove service recovery.
Automating a traffic switch before reconciling data can create split brain or duplicate work.

Decision: emit promotion eligibility only after integrity, journey and objective checks.
Never overwrite an existing target. Refuse corrupted, stale, empty or malformed candidates.
CI is read-only and receives no cloud credentials. Future cloud cutover requires writer
fencing, application validation and an authorized operator decision.

Alternatives: automatic cutover reduces decision delay but adds consistency risk; manual
checks alone are slow and easy to skip. Pure health checks miss stale or incorrect data.

Consequences: local gate is conservative and may reject an idle old database with no actual
loss. A checksum plus trusted manifest still cannot prove the application is correct.
Operator time is part of cloud RTO, which must be measured separately.

Validation: refusal-path tests and unchanged-target test. Revisit automatic promotion only
after authenticated provenance, acknowledgement reconciliation and repeatable failback.
Rollback: do not promote a candidate; after cloud writes, prefer tested forward repair over
blind traffic reversal. No current code switches traffic.
