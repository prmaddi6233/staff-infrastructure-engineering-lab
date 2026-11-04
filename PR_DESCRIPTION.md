# Build an independent reliability portfolio with an executable recovery gate

## Problem and resulting behavior

The repository started with a short README and an opaque starter ZIP. This change replaces
the upload with reviewable source, a clearly scoped architecture case study and a local
recovery rehearsal that refuses promotion for corrupted or stale backups and missed local
restore targets. It never provisions cloud resources or switches traffic.

## Scope

- README with implementation status and links to eight inspected related public projects.
- Proposed multi-account, EKS, DR, SLO/observability, security and FinOps designs; Mermaid
  diagrams, three ADRs and a prioritized 30/60/90-day roadmap.
- Python standard-library SQLite recovery, temporary synthetic data, JSON decisions and
  15 automated tests. New target creation refuses to overwrite existing data.
- Read-only, timeout-bounded CI; SHA-pinned checkout, no persisted credentials or cloud identity;
  Dependabot Action updates; local Markdown and identifier regression checks.
- Seven outstanding-work backlog entries with owner roles, dependencies, acceptance and
  verification. They are prepared entries, not claimed GitHub issues.

## Validation

Python 3.12.14 locally: 15 unittest tests passed; Markdown file links and identifier checks
passed. Healthy CLI returns 0; stale/corrupt return 1 as intended. RTO boundary tests use an
injected monotonic clock; no arbitrary sleep. Full evidence is in docs/validation.md.
No remote CI pass is claimed until a GitHub run confirms it. Mermaid rendering not automated.

## Alternatives and risks

SQLite enables free, dependency-free review; PostgreSQL integration is the next milestone.
Local restore duration is not end-to-end DR RTO, and recovery-point age is not observed loss.
Checksums do not provide authenticity; independently trusted signed provenance remains work.
AWS account isolation, KMS, regional restores, SLO telemetry and Kubernetes drills are proposed.
Main branch protection is currently an outstanding owner action. Runner image is mutable.

## Safety and confidentiality

Independent case study relevant to the CMB role; no access, affiliation, vulnerability or
internal-architecture claims. Synthetic data only; no employer configuration, real account
identifiers or secrets. Existing FinOps/vending engines are linked rather than duplicated.
Historical incident assertions and obsolete publishing instructions in the starter are omitted.

## Rollback

Revert this source change. The deleted ZIP remains in baseline Git history. No deployed
infrastructure, persistent demo data or database migration needs rollback. Do not merge
automatically. Issue creation / branch publication must be verified with GitHub.
