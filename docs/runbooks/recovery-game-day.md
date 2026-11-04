# Synthetic recovery game day

Current executable exercise is local only. Future cloud drill is a proposal, not authorized
or provisioned by running any command in this repository.

## Local rehearsal (implemented)

1. Run `make verify` from the repository root. Stop if any test fails.
2. Run `python3 -m reliability --scenario healthy`; require exit 0, one restored message,
   recovery-point age 10 seconds and eligibility true. Restore time varies by host.
3. Run `python3 -m reliability --scenario stale`; require exit 1 and an RPO reason.
4. Run `python3 -m reliability --scenario corrupt`; require exit 1 and checksum mismatch.
5. Record command, runtime, commit, duration, decision and limitations. Temporary databases
   are removed on process completion. No traffic switch or persistent system mutation occurs.

A failed candidate is deleted; a successful candidate exists only within the temporary run.
This tests local copy/read/write behavior; it does not demonstrate cloud RTO, zero data loss
or administrative backup isolation.

## Future isolated cloud drill (planned)

Roles: incident commander owns timing and stop decisions; recovery operator owns restore;
application owner validates correctness; security observer checks identity separation;
scribe captures evidence. Use synthetic data only, isolated authorized test accounts,
explicit cost ceiling, expiry/cleanup owner and prevalidated service/key support matrix.
Do not run during an active incident or against production/third-party infrastructure.

1. Declare scenario and customer-impact start time. Establish an independent ledger of
   acknowledged synthetic IDs, chosen recovery point and immutable artifact digests.
2. Verify restore credentials work without the workload account. Record negative tests
   proving the workload role cannot delete recovery points or alter retention/key access.
3. Simulate workload unavailability using a narrowly scoped reversible test control.
   Preserve backups and the independent ledger. Do not delete accounts or encryption keys.
4. Rebuild identity/network prerequisites, restore durable data, reconcile acknowledged IDs,
   replay outbox idempotently, then enable API and workers in isolation. Warm cache under a cap.
5. Validate authentication, authorization, reads, writes, duplicates and backlog drainage.
   Fence old writers before any cutover. Never allow two independent writable primaries.
6. Only the incident commander approves test traffic cutover after app/security checks.
   Measure end-to-end RTO and observed lost acknowledged writes/time interval for RPO.
   Record unknowns instead of substituting backup completion timestamps for data correctness.
7. Abort on real data, unexpected resource scope, broken isolation, rising unbounded cost,
   missing key access or inconsistent data. Hold traffic on the last known safe test target;
   investigate before retry. Do not blindly reverse a stateful cutover after new writes.
8. Reconcile evidence, actual test spend and remaining resources. Remove disposable resources
   within retention constraints; verify inventory, backup retention and ongoing charges.
   Conduct a blameless review within two working days and file issues only for observed gaps.

Evidence template: scenario; commit/artifacts; owners; start/detect/restore/validate/cutover
UTC times; recovery point; ledger reconciliation; measured RTO; measured/unknown RPO;
IAM denial results; key access; service errors; abort decisions; cost; cleanup inventory.
