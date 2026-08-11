---
type: feature
nav_path: "Orders → Order details → Status → Transition rules"
route_name: admin.orders.change-status
route_path: /admin/orders/action/status/:order_id/:status
aliases: ["Order transition rules", "Status transition gates", "Allowed status transitions", "validateChangeStatus", "Status guard rails"]
tags: [orders, status, validation, rules]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, side effects, notification, fulfillment gate, bulk, API).

# Order status change — Transition rules

## Purpose

The platform enforces **hard transition gates** for the most operationally consequential status changes. The merchant can change most statuses freely, but four situations are gated: the `Completed` target, the `Cancelled` target, ANY transition on an archived order, and ANY transition on a cancelled / refunded order that already carries a reversal. On top of that, an order whose payment authorisation is smaller than its total cannot change status at all. This page is the canonical catalogue of those gates; the breadcrumb pill (see [[orders-status-change-pill]]), the bulk action, and the JSON-API v2 PATCH endpoint (see [[orders-status-change-api]]) all run through the same validation.

## Where to find it

The gates are surfaced as errors when the merchant attempts a blocked transition — either as a toast on the order-details page, in the bulk-action error banner on [[orders]], or as a JSON-API v2 422 error response. There is no dedicated "allowed transitions" UI; the rules apply silently and only surface on rejection.

## What the merchant can do here

The merchant attempts a transition and the platform either accepts it (running the full side-effect chain — see [[orders-status-change-side-effects]]) or rejects it with one of the messages below.

### Correction of the older "any-to-any" framing

Earlier wiki copy described status transitions as "any-to-any allowed (no state machine)". That framing is INCORRECT. The platform DOES enforce hard rules for `Completed` and `Cancelled`, locks archived orders entirely, and permanently locks a cancelled / refunded order once a reversal has been recorded against it. The "any-to-any" framing is roughly correct only for custom statuses and the remaining canonical statuses (Paid / Refunded / Authorized / Pending) — those bypass the target-specific gates but are still subject to the archived lock, the reversal lock and the authorised-amount check.

### Hard transition rules

| Target | Allowed only when | Error message |
|--------|-------------------|---------------|
| **Completed** | Order is currently `paid` **OR** fulfillment is `fulfilled` — either is enough | *"Only paid and/or fulfilled orders can be marked as Completed"* |
| **Cancelled** | Order is NOT currently `paid` or `completed` | *"Only open orders can be canceled."* |
| ANY status | Order is NOT archived | *"Cannot change the status of archived order. Unarchive first."* |
| ANY status | The order is not a cancelled / refunded order carrying a return record or an issued credit number — the **reversal lock** | *"The order is locked after a cancellation/refund — its status can no longer be changed."* |

So the merchant CAN go `Pending → Paid → Completed → Pending` (legal — each step satisfies its gate), and CAN mark a `paid` but unshipped order `Completed` (the gate is OR, not AND). The merchant CANNOT:

- Go `Completed → Cancelled` or `Paid → Cancelled` (blocked — refund the order instead).
- Change ANY status on an archived order (locked — must unarchive first).
- Re-open a cancelled / refunded order that already carries a return or a credit note — only a `Cancelled` ↔ `Refunded` toggle is accepted.

**`Abandoned` is not a status at all.** It is a separate flag on the order, not a value the status field can hold and not an option in the pill. Asking any status endpoint for `abandoned` is rejected up front as *"Invalid status"*, before any transition rule is even considered. The same applies to the five gateway-driven statuses.

### Authorised-amount check — blocks EVERY transition, not just paying ones

If the order carries a payment authorisation, the platform compares the **authorised amount against the order total** before doing anything else. There is exactly one failure reason: the authorisation does not cover the total. The error names both figures — *"The order amount is `<total>` and cannot exceed the authorized payment `<amount>`."*

Two things about this check matter in practice:

- **It runs before the target status is looked at.** So an under-authorised order cannot be moved to `Cancelled` either — the check fires first and refuses everything. The merchant has to edit the order down to the authorised amount (or remove the line they added after the authorisation) before any status change goes through.
- **It is one check, not a family of gateway reasons.** There is no separate "authorisation expired", "card on file unavailable", "chargeback hold" or "fraud review" rejection at this layer; those, if they happen, surface from the gateway during the capture itself — see [[orders-payment-capture]].

The check runs identically from the admin pill, the bulk action, and JSON-API v2.

### Custom statuses and the remaining canonical statuses — bypass the target-specific gates

Custom statuses (merchant-defined in [[settings-statuses]]) and these canonical statuses bypass the `Completed` / `Cancelled` gates:

- `Paid`
- `Refunded`
- `Failed` (settable only via gateway / API; not in the admin dropdown — see [[orders-status-change-pill]])
- `Voided` (same)
- `Disputed` (same)
- `Chargebacked` (same)
- `Timeouted` (same)
- `Authorized`

So the merchant CAN freely move an order between Paid / Refunded / Authorized / Pending / custom statuses without hitting a target-specific gate — but the archived block, the reversal lock and the authorised-amount check still apply. Note that `Failed` / `Voided` / `Disputed` / `Chargebacked` / `Timeouted` are not reachable from the pill, the bulk action, or JSON-API v2: those endpoints validate the requested status against the merchant-pickable set and reject anything outside it.

## Settings & fields

The transition rules are NOT configurable. The merchant cannot, for example, allow `Cancelled` on paid orders via a setting toggle. The gates are code-level and apply uniformly.

## Business rules

- Gates execute BEFORE any side effect. A rejected transition writes NO history row, fires NO notification, moves NO stock — the order state is untouched.
- The target-specific gates apply to a single canonical-status name each. Custom statuses that happen to be named "Completed" or "Cancelled" by the merchant still bypass — only the canonical status codes are gated.
- The archived block is **absolute** — no status change is permitted on an archived order, including back to its previous status. The merchant must Unarchive first via the 3-dot dropdown or the bulk **Unarchive** action. Unlike the reversal lock, it lifts as soon as the order is unarchived.
- The **reversal lock** is permanent for practical purposes: a cancelled / refunded order carrying a return or a credit number only ever toggles between those two statuses. It does not lock the order's *payments*, so the actual money refund can still be processed, and a delayed gateway notification can still correct a spurious cancel — that recovery path does not run through this validation.
- Bulk-status processing runs every selected order through the same gates. The bulk processor is fail-fast — the first order to fail any gate rolls back the WHOLE batch. See [[orders-status-change-bulk]] for the transaction behaviour.
- The transition gates do NOT consider customer notification or stock side effects — those are downstream of the gate check. A rejected transition fires neither.

## Programmatic access

The JSON-API v2 PATCH of `status` runs the SAME validation as the admin pill — same target gates, same archived block, same reversal lock, same authorised-amount check, same error messages. See [[orders-status-change-api]] for the API-specific notes (history namespace, side-effect parity, the five hidden gateway statuses).

## Related

- [[orders-status-change]] — hub.
- [[orders-status-change-pill]] — UI surface; the dropdown does NOT preview these gates.
- [[orders-status-change-side-effects]] — what runs AFTER a gate passes.
- [[orders-status-change-bulk]] — fail-fast on first failing gate.
- [[orders-status-change-api]] — same gates apply via JSON-API v2.
- [[orders-payment-capture]] — what happens at capture time, after this check passes.
- [[settings-statuses]] — status taxonomy; canonical-status-vs-custom-status distinction.
- [[orders-archive]] — archive / unarchive flow that determines the archived gate.
- [[order-status-negative-semantics]] — the reversal lock and the return record that arms it.

## Open questions

- Whether merchants can configure per-status transition rules in a future update `(verify — currently code-level only)`.
