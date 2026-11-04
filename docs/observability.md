# Customer journeys, SLOs and operational signals

Status: illustrative proposals. No production telemetry, dashboard or alert rules implemented.
Assume a rolling 30-day request-based evaluation window, not a time-based uptime assertion.

| Journey | Eligible events | Good event | Proposed SLO |
|---|---|---|---|
| Login | Valid synthetic or consenting-user sign-in attempts | Authorized session issued within 2 seconds | 99.9% |
| Discovery | Authorized requests for a discovery page | Valid bounded-age page within 1 second | 99.9% |
| Send message | Valid authorized sends with idempotency key | Durable acknowledgement within 500 ms, no duplicate logical message | 99.95% |
| Read message | Authorized reads for an existing conversation | Correct bounded-age result within 1 second | 99.9% |

Count attempts at the journey boundary so edge errors, timeouts and unavailable origins do
not disappear from the denominator. Expected invalid credentials and unauthorized requests
are excluded by defined client-intent rules; valid requests rejected due to overload count
as bad. Count a logical attempt once across retries. Record unavailable telemetry as unknown
and alert on collection health; do not label missing samples successful. External identity
provider failures affecting valid sign-ins count toward customer experience, with a separate
dependency breakdown for ownership. Correctness SLIs need application-level validation and
privacy review rather than status-code inference alone.

SLI = good / eligible; allowed bad events = eligible × (1 − target).
Burn rate = observed bad fraction / (1 − target). Example proposed page policy:
14.4× burn in both 1-hour and 5-minute windows OR 6× burn in both 6-hour and 30-minute
windows. Route to the journey owner with runbook and release context. Longer-lived slower
burn creates a ticket. Minimum-volume handling, synthetic probes and alert test fixtures are
required before activation; low traffic makes raw ratios noisy. A depleted budget pauses
risky feature rollouts while the team restores reliability; security fixes are reviewed
separately rather than blocked blindly.

Record request count, errors and duration buckets by bounded journey, route template and
region; never label metrics by user, message ID or URL query. Use sampled OTel traces and
structured redacted logs with correlation IDs and bounded retention. Do not log message
bodies, tokens or credentials. Separate synthetic probes from real traffic in analysis.

Supporting signals: queue oldest age and DLQ growth, DB connection saturation and replication
lag, pod readiness/restarts, Pending pods, node pressure, DNS failure and subnet IP headroom.
These diagnose symptoms; user-impact burn drives paging. Link each alert to an owner,
diagnostic query, mitigation, escalation path and a tested resolution condition.

Reference: [Google SRE multiwindow burn-rate alerting](https://sre.google/workbook/alerting-on-slos/),
checked 2026-11-04. The thresholds here are proposals requiring workload-specific validation.
