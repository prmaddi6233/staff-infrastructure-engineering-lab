# Outstanding engineering backlog

Prepared 2026-11-04. GitHub issue creation was attempted but rejected with HTTP 403
`Resource not accessible by integration`. No GitHub issue numbers or URLs are claimed.
B01–B07 are local backlog identifiers, not GitHub issues. Completed foundation work is excluded.

## B01 — P1: Verify PostgreSQL integration on an unprivileged runner

Owner: platform + application. Depends on: an unprivileged Linux runtime with PostgreSQL 16.
The native PostgreSQL drill and five scenario checks are implemented. Runtime verification
is outstanding. Run `bash scripts/test-postgres.sh`, retain server version, exit codes and
proof of cleanup. Review missing-write IDs against the external ledger. Add pinned-container
reproduction and validate the same results before closing this item.

## B02 — P1: Enforce main-branch review and CI requirements

Owner: repository owner. Depends on: foundation CI reviewed and available on main.
Problem: main was reported unprotected during inspection.
Acceptance: require PR review and the validation check; block force pushes and deletion where
repository plan supports it. Document bypass limitations and unavailable controls.
Verification: failing disposable PR cannot merge; restore test and verify check recognition.
Do not merge a failing PR or change repository administration without owner authorization.

## B03 — P1: Instrument journeys and test SLO alert rules

Owner: SRE + application. Depends on: B01 for durable-message integration; alert fixtures can
start independently. Problem: no implemented journey metrics or alert rules.
Acceptance: bounded counters/histograms, defined event denominator, no PII; executable
multiwindow burn and telemetry-health alerts. Test good, bad, zero/low volume, missing samples
and deduplicated retries.
Verification: pinned local rule-test command shows fast/slow burn behavior and no false healthy
state when telemetry is absent. Compare counters with independent synthetic event counts.

## B04 — P1: kind drain and overload drill

Owner: platform + SRE. Depends on: B03 for measured user impact.
Problem: no Kubernetes execution evidence.
Acceptance: pinned kind/Kubernetes runtime, synthetic workload with probes/PDB/topology,
continuous traffic and bounded overload. Show blocked eviction without spare capacity and
successful recovery once capacity is restored. Do not claim an AZ simulation proves EKS behavior.
Verification: one script creates cluster, drains node, captures failures/recovery time and
cleans cluster even on failure. Record versions and expected negative cases. No AWS resources.

## B05 — P1: Authenticate backup provenance

Owner: security + platform. Depends on: local recovery interface only.
Problem: replacing both artifact and checksum defeats current integrity checks.
Acceptance: verify signed manifest with separately trusted verification material, artifact digest,
time/replay policy and signer allowlist. Document custody and rotation. Use a maintained pinned
crypto implementation, not custom cryptography; test keys are never production keys.
Verification: modified backup+digest, manifest, untrusted signer and invalid metadata all fail;
valid signed fixture succeeds. Colocated test keys do not establish real custody.

## B06 — P2: AWS support matrix and recovery tabletop

Owner: recovery + security. Depends on: B01 and B05 for reconciliation/provenance expectations.
Problem: resource-specific key and restore paths are unverified.
Acceptance: dated official-source matrix of engine/resource, key types, copy support, destination
account/region, restore permissions, retention and limitations. Walk identity loss, region loss,
corruption and key-unavailability scenarios. Explicitly mark actual IAM/cloud timings untested.
Verification: peer follows every documented path and identifies credential/key prerequisites,
abort criteria and cleanup constraints. Documentation/tabletop only; no paid deployment.

## B07 — P1: Tested secret scanning and workflow policy checks

Owner: security + platform. Depends on: foundation CI.
Problem: identifier regex is not general credential detection; workflow policy is not enforced.
Acceptance: pinned scanner and checks for SHA pins, minimum token permissions, unsafe PR triggers
and persisted credentials. Safe synthetic fixtures, explicit binary/archive handling and
redacted output. Document false positives/exclusions.
Verification: synthetic prohibited token and unsafe workflow fail; clean source passes;
matched values never appear in output. Revert scanner changes if they leak fixture content.

## Sequencing and scope

Start B01, B05 and B07; B02 follows merge/review authorization. B01 → B03 → B04 provides a
measured reliability path. B06 is a later decision gate. Every task is local/synthetic or
documentation-only; no CMB systems or employer data. Revert failed code changes and remove
all disposable resources. Roadmap's evidence/cost review is a recurring acceptance gate for
these tasks, not a duplicate analytics-engine implementation issue.
