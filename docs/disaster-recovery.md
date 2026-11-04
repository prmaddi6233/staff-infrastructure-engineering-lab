# Recovery objectives and design

Status: illustrative proposals for a hypothetical app; not CMB requirements or measured results.

| Journey / data | Proposed cloud RTO | Proposed cloud RPO | Recovery validation |
|---|---|---|---|
| Login / identity configuration | 60 minutes | 15 minutes for configuration changes | Synthetic account can authenticate and cannot cross user boundary |
| Accepted messages and matches | 60 minutes | 5 minutes | Reconcile acknowledged IDs; read/write and deduplicate replay |
| Discovery / recommendations | 4 hours | 24 hours for derived results | Rebuild from durable inputs; serve bounded stale results |
| Cache | 60 minutes as part of API recovery | Rebuild; no durable-data RPO | Prevent cache-miss stampede during warm-up |

Targets require product/security approval, data residency review and cost evaluation. A
five-minute message RPO is not met by a daily snapshot; measure continuous recovery or
incremental copy lag and verify the selected service's supported recovery behavior.

RTO starts at customer-impact onset and ends after independent journeys validate restored
service, including detection, authorization, rebuild, restore, replay and traffic cutover.
RPO compares acknowledged writes at incident time with the recovered durable state. If the
source is unavailable, use an independent synthetic acknowledgement ledger and report unknown
loss when the ledger is incomplete. Do not infer zero data loss from a successful restore job.

## Proposed isolation

Copy supported backups to a separate recovery account and evaluate a second region based on
regional outage requirements. Protect independent restore roles, artifacts and key access.
Backup copies, replication and immutable retention address different failure modes;
replication alone can propagate logical corruption. Retention changes need a deliberate
review because locked retention can prevent deletion and incur unavoidable storage charges.

For each resource record engine/version, source encryption type, source and destination
key policies, copy support, retention, restore role, destination region and actual restore
steps. AWS Backup support and encryption behavior vary by service. Do not assume direct
cross-account restore or all combined copy operations are supported. Restore to the permitted
account/region using the documented copy path and validate key access before a real incident.
This matrix and cloud proof remain outstanding; no paid resources are provisioned here.

The [game-day runbook](runbooks/recovery-game-day.md) separates local rehearsal from future
cloud exercises. [ADR-001](adr/0001-recovery-isolation.md) records the alternatives.

Primary references checked 2026-11-04:
[cross-account copies](https://docs.aws.amazon.com/aws-backup/latest/devguide/create-cross-account-backup.html),
[backup encryption](https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html),
[vault lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html).
