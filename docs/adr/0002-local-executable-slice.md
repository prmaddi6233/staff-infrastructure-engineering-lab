# ADR-002: Build an offline recovery gate before cloud infrastructure

Status: accepted for this lab. Date: 2026-11-04.

Context: reviewers need reproducible evidence without paid infrastructure or credentials;
existing public projects already cover vending and cost governance.

Decision: Python standard library plus temporary SQLite files. Validate integrity, synthetic
read/write behavior, recovery-point age and local restore duration. Include positive and
negative CLI scenarios and a stable JSON decision. Reuse linked projects rather than clone
their engines. Replace the opaque starter ZIP with normalized source in the feature branch.

Alternatives: PostgreSQL in containers is more realistic but adds runtime/dependency costs;
a cloud restore proves more but violates the no-paid-resource scope and needs explicit
isolation planning. Documentation alone cannot demonstrate failure handling.

Consequences: SQLite does not prove AWS, PostgreSQL or distributed recovery. SHA-256 is an
integrity check, not independent provenance. RTO excludes detection and infrastructure rebuild.
Only selected Python runtime behavior is tested; future integrations require fresh evidence.

Validation: unittest suite plus CLI exit-code checks. Next: disposable PostgreSQL restore
with acknowledgement reconciliation. Revisit storage engine when that issue is implemented;
retain the deterministic tests for objective boundaries. Rollback: revert this source change;
no persistent resources or data migration exist.
