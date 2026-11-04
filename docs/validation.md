# Validation evidence and limits

Local validation on 2026-11-04 using Python 3.12.14 on Linux. Not production evidence.

| Check | Actual result |
|---|---|
| `python3 -m unittest discover -s tests -v` | 15 tests passed, including subprocess healthy/stale/corrupt scenarios |
| `python3 scripts/check_repository.py` | Local Markdown target and account-identifier regression checks passed after all documents were present |
| `python3 -m reliability --scenario healthy` | Exit 0; eligibility true; 1 restored message; recovery-point age 10 synthetic seconds |
| `python3 -m reliability --scenario stale` | Exit 1 expected; eligibility false; RPO-age breach |
| `python3 -m reliability --scenario corrupt` | Exit 1 expected; eligibility false; checksum mismatch |
| GitHub Actions | Workflow prepared; no remote run verified at preparation time |
| AWS/EKS/production DR | Not deployed or tested |

Local healthy restore duration is measured with a monotonic clock and varies by host;
sub-millisecond or millisecond file copies do not imply any cloud RTO. Objective boundary
and violation tests inject elapsed time deterministically rather than sleeping. Synthetic
incident epochs are fixed fixtures, not historical incident timestamps. The RPO gate measures
age of latest backed-up acknowledged write; real observed data loss requires B01's independent
ledger reconciliation. The local read-after-write probe is rolled back and source data
preservation is asserted.

Tests cover corruption, invalid SQLite schema, empty data, stale/future/invalid timestamps,
invalid objectives, missing source, existing target, invalid clock and inclusive RTO/RPO
boundaries. Trusted small filesystem input and trusted expected digest remain assumptions.
There is no signed provenance, scale/concurrency test, service telemetry, Kubernetes drill,
IAM/KMS proof, full DLP scan or measured end-to-end cloud recovery.

The integrity script validates file existence for local Markdown links, not remote URLs,
anchors, Mermaid rendering or prose accuracy. Mermaid source was manually reviewed; no
renderer-based validation is claimed. Python 3.11+ is intended compatibility; only the runtime
above was executed locally. CI uses runner Python and records its actual version.

## Reproduce

From repository root, run `make verify` and each scenario above. Nonzero status on stale
and corrupt is the intended safety behavior. No install step or credentials are needed.
CI uses the same commands and a SHA-pinned checkout with read-only contents permission.

## Publication state

GitHub reads confirmed the public repository and baseline main commit. Connector writes to
create issues and a feature branch returned 403. This file records local evidence only;
publication must be confirmed independently, never inferred from prepared source or a draft PR
body. Review source and any CI status before merging. No operation in this lab provisions
paid cloud resources.

## PostgreSQL follow-up

Native PostgreSQL scripts implemented. Both passed Bash syntax checks. PostgreSQL 16.2
binaries were available, but this environment maps only UID 0. It cannot launch initdb as
an unprivileged user. End-to-end PostgreSQL validation is pending. The workflow now calls
the five-scenario suite on a GitHub-hosted Ubuntu runner. No remote CI result is available.
