# Runbook — elevated HTTP 5xx

**Scope:** disposable SRE Reliability Lab only.

## Detect

Check service health, request counters, and error-rate trends; establish whether the user-facing path is affected. Do not confuse a synthetic failure drill with a production incident.

## Triage

1. Confirm the active Kubernetes context or local process before issuing commands.
2. Inspect `/healthz` and `/metrics` for HTTP error counts and latency.
3. Correlate structured logs by `request_id`.
4. Check if the explicit `ENABLE_FAILURE_ENDPOINT` switch is active.

## Recover

Disable fault injection, restore healthy configuration, and verify at least three successful health requests. Roll back or stop the lab if the effect is not bounded.

## Record

Capture timestamps, impact, evidence, action, and next preventive step in `postmortem-template.md`. Never include private hostnames, tokens or client data.
