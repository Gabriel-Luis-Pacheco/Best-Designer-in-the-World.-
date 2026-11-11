# System UX — identity, permission, money and irreversible journeys

Activate for product/internal/checkout surfaces with consequential accounts, shared data, authorization, payment or destructive actions. Not for a simple illustration or hero edit. This is a product-interaction acceptance guide, not a backend-security certification.

## Truth and contracts
Inventory the actual user role, organization/tenant, protected object, source of truth, allowed action, session, data owner, billing provider and recovery. Mark OBSERVED, REPORTED, INFERRED, UNKNOWN. Preserve prices, IDs, backend permission controls, payment state and legal language unless the change is explicitly authorized.

## State-by-state acceptance matrix

| Risk-bearing flow | Real scenarios to design and verify | Important guard |
|---|---|---|
| Authentication | anonymous, login, reset, expired link, unverified, rate-limited, lockout, session restored, SSO | Actual server response, password manager, deep links, accessible errors |
| Roles/tenant | member/admin, pending invitation, permission removed, org switch, stale context | Server-side roles and tenant isolation; hiding a button is not authorization |
| Checkout/subscriptions | real total/tax, coupon, pending, failed, duplicate submit, delayed webhook, cancellation, renewal, refund | Payment provider/server state; do not claim paid before verification |
| Destructive/bulk edit | unsaved, pending, version conflict, partial success, retry, cancel, deletion, undo where supported | Prevent silent overwrites, unauthorized changes and misleading confirmations |
| Imports/exports/jobs | validation, progress, timeout, partial results, resume, download, cancellation | Job lifecycle and safe access to generated files, not an invented spinner |
| Data views | empty, stale data, filtering, permissions, long rows, mixed currencies | Correct lineage, units, accessible controls and safe role-specific states |

## Procedure
1. Select the actual primary task and the two or three failure/edge paths with the greatest plausible impact; no blanket requirement to test every hypothetical state on a tiny patch.
2. Test expected user state, errors, permissions and affected routes in a permitted environment. Use provider sandboxes for financial test transactions.
3. Verify server data/status, not just client animation. Show pending vs confirmed and safe retry/undo/cancellation; do not duplicate charges or irreversible operations.
4. Inspect mobile, keyboard, focus, screen-reader where available, empty/error/recovery and actual back/deep-link behavior.
5. Record route, role, test evidence, implementation, regression and unresolved risk. P0/P1 failures stay open until retested; no tool access means UNKNOWN.

Use advanced-product-ux-operations.md for dense interfaces and quality-gates-and-evidence.md for evidence standards. Backend audit, security assessment and payment-compliance certification require specialist tools and responsible owners.
