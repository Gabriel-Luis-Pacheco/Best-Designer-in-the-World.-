# Operational readiness, observability and recovery UX

Use for running systems and transactional/production-critical features; not an obligatory SRE checklist for artwork or a small visual patch. This concerns user-facing resilience and acceptance, not a claim that the assistant can operate infrastructure without authorization.

## Beyond the happy-path render
- Before rollout: know the critical route, version, user/role, dependency, fallback, smoke checks, performance budget, responsible owner and verified rollback path.
- When a provider/model/payment/email fails: show accurate degraded mode and what still works, whether user data was saved, what is pending and how to retry safely.
- Distinguish payment pending vs successful; upload received vs processed; email queued vs delivered; task complete vs progress persisted.
- For partial success, conflicts, timeouts and offline transitions, preserve context and identify a safe retry, cancel/undo or support path when implemented. A second click must not double-charge or silently duplicate a destructive operation.
- After recovery: reconcile client/server status, resume the real user job, correct stale data and provide accurate status documentation.

## Observability connected to actual user value
Define events and errors with privacy/consent, route, state, action, outcome, build version, device/locale and recoverability. Avoid logging secrets. Measure real field behavior (task completion, abandonment, recovery, error rate, latency, LCP/INP/CLS where relevant). A synthetic green test, production telemetry and an actual user interview are different forms of evidence.

## Release handoff
For consequential changes report source of truth, roles, checks run, test environment, browser/device states, release/feature-flag owner, monitoring, support/escalation and rollback. Make incident communication accessible and factual. Keep PASS/FAIL/UNKNOWN tied to inspected evidence. Without deployment/log access, never invent uptime, conversion, feature flags or incident closure.
