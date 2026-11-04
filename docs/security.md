# Threat model and security boundaries

Status: design review plus limited local validation; no claim of production hardening.
Assets: durable synthetic messages, recovery artifacts, expected digests, source repository,
CI identity and future restore credentials. Actors: accidental operator, malicious dependency,
compromised workload role and compromised organization administrator.

| Threat | Proposed control | Implemented evidence / remaining gap |
|---|---|---|
| Corrupted backup | Compare independently stored digest before restore | Hash mismatch test; no authenticated provenance yet |
| Both backup and digest replaced | Signature from independently controlled signer | Outstanding; adjacent checksum is insufficient |
| Existing target overwritten | Exclusive new-target creation | Tested refusal; local filesystem still trusted |
| Stale or malformed data | Timestamp/schema, journey and age gates | Tested on synthetic SQLite; no real message reconciliation |
| Compromised workload admin deletes recovery | Separate recovery identity and retention | Proposed only; no IAM/KMS denial tests |
| Privileged PR code | Read-only token, no secrets, no cloud access | CI configuration; runner executes untrusted PR code |
| Dependency supply-chain compromise | No third-party Python dependencies, SHA-pinned checkout | Runner image remains externally managed and mutable |
| PII exposure | Synthetic fixtures, no message-body logging in design | Manual review and identifier check; not comprehensive DLP |

The local API assumes trusted, small backups on a private temporary filesystem. It is not
safe as an arbitrary public upload processor: unbounded file reads, malicious SQLite files,
filesystem races and concurrent candidate mutations are outside its trust model. A future
service needs file size limits, resource isolation and authenticated provenance. A successful
result is eligibility evidence, not an authorization or traffic-switch command.

No current CI secrets, cloud credentials, write token or OIDC permission. Use pull_request,
not pull_request_target for executing PR code. Checkout credentials are not persisted;
timeout and concurrency bound wasted runner time. Dependabot proposes Action pin updates for
review. Branch protection and required reviews remain an owner-controlled outstanding issue;
this PR does not change repository administration settings.

Future cloud roles must split backup copy, restore, audit and traffic cutover, scope resource
and key policies, and restrict federation claims. Recovery key deletion and role changes
need independent detection and emergency procedures. Organization-admin compromise is a
residual risk even with account isolation; evaluate additional independent custody where
required. Security and FinOps changes must preserve recoverability, not merely pass static scans.
