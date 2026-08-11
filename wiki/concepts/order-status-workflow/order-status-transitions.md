---
type: concept
nav_path: "Concept → Order status workflow → Transitions"
aliases: ["Order status transitions", "Status change", "Manual status change", "Bulk status change", "Status dropdown", "Archived order lock", "Status rename", "API status change"]
tags: [orders, statuses, transitions, bulk, api, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (taxonomy, custom statuses, auto-transitions, side-effects, negative semantics, action gates).

# Order status — transitions

## Definition

A status transition is any change to the order's `status` field. The platform supports **three ways** to initiate a transition — manual (per-order via the status pill), bulk (multiple orders from the list view), and programmatic (JSON-API v2 or auto-rules — see [[order-status-auto-transitions]] for the auto cases). It is not a full state machine, but it is **not** "any status to any other" either: five validation rules refuse specific transitions outright (see *Enforced rules* below), the status pill and the endpoints behind it only accept the merchant-pickable set, and the 5 gateway-driven statuses are rejected as invalid.

## Scope

Covered:

- Manual single-order changes via the status pill.
- Bulk changes from the list.
- JSON-API v2 status changes ([[api-orders]]).
- The dropdown (merchant-pickable) subset vs the full 11-status list.
- The enforced rules that DO block transitions (`completed` / `cancelled` gates, archived lock, reversal lock, shipping integration lock, authorised-amount check).
- The status-rename safety guarantee.

Not covered here:

- Automatic transitions (auto-promote, banned-IP, gateway events, draft state) — see [[order-status-auto-transitions]].
- What side-effects fire on a successful transition — see [[order-status-side-effects]].
- Per-status action availability (refund, edit, etc.) — see [[order-status-action-gates]].

## Contrasts

- **Manual single-order vs bulk vs JSON-API v2** — three entry points, same validate-then-apply pipeline. The bulk UI ribbon defaults to "Mark as completed"; the endpoint behind it accepts only the same merchant-pickable set the dropdown offers, not "any status".
- **Dropdown subset vs full 11-list** — the merchant-facing dropdown intentionally hides the 5 gateway-driven statuses (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`); they still apply internally (audit log, exports, payloads). Both the single and the bulk status endpoints validate against the same filtered set and reject anything outside it with *"Invalid status"*.
- **Validation rule vs side-effect** — rules BLOCK a transition (the `completed` / `cancelled` gates, archived lock, reversal lock, shipping lock); side-effects ([[order-status-side-effects]]) fire AFTER a rule-passed transition succeeds.
- **Status code vs label** — transitions operate on the code; renaming the label via [[settings-statuses]] never breaks downstream integrations.

## Where it applies

Every status change in the system flows through the same pipeline regardless of source — admin click, bulk action, JSON-API v2 call, or auto-rule. Below are the three transition paths plus the enforced gates.

### The three transition paths

#### Manual — single order

The merchant opens [[orders-details]] and clicks the status pill in the breadcrumb. A dropdown opens with the merchant-pickable statuses (see "Dropdown vs full list" below). Picking a target status submits the change immediately and fires the full side-effect cascade ([[order-status-side-effects]]). The dedicated single-order change endpoint is [[orders-status-change]].

#### Bulk — multiple orders

From the [[orders]] list, the merchant selects multiple orders, opens the bulk action ribbon, and triggers a status change. The UI ribbon prominently shows **Mark as completed** as the default bulk action. The bulk-status endpoint behind it validates the requested status against the **same merchant-pickable set the dropdown shows** — so a script can bulk-transition to `paid` / `cancelled` / `refunded` / `authorized` / `pending` / a custom status, but the 5 gateway-driven statuses are rejected with *"Invalid status"* before anything is touched. Per-order changes for all other statuses currently require [[orders-details]].

#### Programmatic — JSON-API v2

The same [[orders-status-change]] pipeline runs when status is changed through [[api-orders]]. There is **no fast path** or side-effect-skipping mode for API-driven mutations; every status change runs through the same validate-then-apply pipeline regardless of source.

**API-settable subset**: the same 6 merchant-pickable statuses (positive 4 + `cancelled` + `refunded`) plus any custom statuses. The 5 gateway-driven statuses (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) are NOT directly settable via the API — they're emitted only by payment-provider sync.

**Acting party**: when a status change is initiated through JSON-API v2, the resulting [[orders-history]] entry stores `api2` in its namespace field, which renders as **"API"** in the audit timeline. All other side-effects (webhook payload, customer notification, stock effects, discount-uses recount, fulfillment reset, auto-created return, auto-promotion) fire identically.

**Every JSON-API v2 status PATCH also sets the order's `manual` flag** — see "The `manual` flag" below. The same is true of the status pill on the [[orders]] list.

Because API clients often batch status + fulfillment changes (creating a fulfillment via [[api-order-fulfillment]] simultaneously sets `status_fulfillment = fulfilled` and may trigger payment capture for two-phase providers), an order can land in `completed` after a single API call — but the promotion happens *before* the change event fires, so it produces **one** history row and **one** `order.updated`, showing `completed`. See [[order-status-auto-transitions]].

### Dropdown vs full status list

The merchant-facing dropdown on [[orders-status-change]] and the bulk list intentionally hide the 5 gateway-driven statuses (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`). Those are emitted only by payment-provider sync, and exposing them in the merchant's quick-pick list would lead to confusion.

So the dropdown shows:

- The 6 merchant-pickable built-ins: `authorized`, `pending`, `paid`, `completed`, `cancelled`, `refunded`.
- The 2 **fulfillment** values, `fulfilled` and `not_fulfilled`, appended into the SAME list — picking one changes `status_fulfillment`, not `status`.
- Any merchant-added custom statuses ([[order-status-custom]]).

The full 11-status list still applies internally (audit log, webhook payloads, exports, status translation map) — only the **picker** is filtered. `abandoned` is **not** in the list and is not a status at all: it is a separate flag on the order, and asking any status endpoint for it comes back as *"Invalid status"*.

### Enforced rules — what the platform DOES block

| Rule | Effect |
|------|--------|
| **`completed` needs `paid` OR `fulfilled`.** | Refused only when the order is **neither** `paid` **nor** `fulfilled`. Error: *"Only paid and/or fulfilled orders can be marked as Completed"*. A `paid` but unshipped order therefore completes fine. |
| **`cancelled` is refused from `paid` / `completed`.** | Error: *"Only open orders can be canceled."* Refund such an order instead. |
| **A cancelled / refunded order with a reversal on it is locked.** | Once the order carries a return record or an issued credit number, its status can only toggle between `cancelled` and `refunded`. Any other target is refused: *"The order is locked after a cancellation/refund — its status can no longer be changed."* A plain cancel of a never-committed order has no reversal record and stays reversible. See [[order-status-negative-semantics]]. |
| **Archived order's status cannot change.** | Error: *"Cannot change the status of archived order. Unarchive first."* / *"Статусът на архивирана поръчка не може да бъде променен. Първо разархивирай."* The merchant must unarchive via [[orders-archive]] first. |
| **Some shipping integrations lock fulfillment status.** | Error: *"Моля, генерирайте товарителница за тази поръчка. Смяната на статуса от тук, не е възможен."* — the merchant must trigger the courier's waybill flow ([[orders-shipping-waybill]]) instead of picking `fulfilled` from the dropdown. |
| **Under-authorised order: no status change at all.** | When the order carries a payment authorisation and the **authorised amount is lower than the order total**, every status change from the pill / bulk action / API is refused with *"The order amount is `<total>` and cannot exceed the authorized payment `<amount>`."* This check runs **before** the target status is even looked at, so such an order cannot be `cancelled` from the pill either — the merchant must first edit the order down to the authorised amount. |

### The `manual` flag — why the gateway stops moving the order

The status pill on the [[orders]] list and every JSON-API v2 status PATCH set a `manual` marker on the order. From that point on the platform **stops recomputing the order's status from its payment rows**, permanently. A gateway webhook arriving afterwards still updates the payment row, but no longer drags the order's status with it.

That is usually what the merchant wants (their manual decision sticks), but it explains a common report: *"I set this order to Paid by hand, then the customer actually paid online, and the order never moved."* Once flagged, only another manual change moves the status.

### Status rename doesn't break integrations

When the merchant renames `pending` to "Awaiting confirmation" via [[settings-statuses]], the change applies to the admin UI, customer-facing order tracking, and emails. The underlying CODE stays `pending`. Webhooks ([[settings-hooks]]), API responses ([[api-orders]]), exports, and external integrations all see `pending`. Renaming is safe for downstream tooling — see [[order-status-custom]] for the full guarantee.

### Archived orders are status-locked

An order in the Archived state (`date_archived` populated) returns an error if the merchant tries to change its status. The merchant must first unarchive via [[orders-archive]], then change the status, then optionally re-archive. This protects archival as the canonical "frozen" state for accounting (verify).

## Related

- [[order-status-workflow]] — hub.
- [[orders-status-change]] — the single + bulk change flow.
- [[orders-details]] — per-order status pill.
- [[orders]] — list with bulk action.
- [[orders-archive]] — archive state preventing status changes.
- [[orders-shipping-waybill]] — courier waybill flow that locks direct fulfillment edit.
- [[settings-statuses]] — rename / add custom.
- [[api-orders]] — JSON-API v2 endpoint.
- [[json-api-v2]] — API overview.
- [[order-status-side-effects]] — the cascade fired by every successful transition.
- [[order-status-auto-transitions]] — automatic transitions (auto-promote, banned-IP, draft).
- [[order-status-action-gates]] — per-status action availability.
- [[order-status-negative-semantics]] — the reversal lock that permanently closes a committed cancellation / refund.

## Open Questions

None.
