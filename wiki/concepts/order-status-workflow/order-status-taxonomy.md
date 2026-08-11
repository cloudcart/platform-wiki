---
type: concept
nav_path: "Concept → Order status workflow → Status taxonomy"
aliases: ["Order status taxonomy", "11 order statuses", "Built-in order statuses", "Positive statuses", "Negative statuses", "Fulfillment status", "status_fulfillment"]
tags: [orders, statuses, taxonomy, fulfillment, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[order-status-workflow]]. See the hub for the other aspects (custom statuses, transitions, auto-transitions, side-effects, negative semantics, action gates).

# Order status — taxonomy

## Definition

The platform defines **11 canonical order statuses** hard-coded into the data model. The merchant can rename their labels via [[settings-statuses]], but the underlying status CODES are fixed — webhooks, JSON-API v2 payloads, exports, and analytics filters all use the CODES, not the labels. In parallel, every order carries a separate `status_fulfillment` field with only 2 values that tracks shipment progress independently of the main status.

The 11 statuses split into **4 positive** (kept in revenue / fulfillment metrics) and **7 negative** (excluded from revenue — see [[order-status-negative-semantics]]).

## Scope

Covered:

- The 4 positive statuses (`authorized`, `pending`, `paid`, `completed`).
- The 7 negative statuses (`voided`, `timeouted`, `cancelled`, `failed`, `refunded`, `chargebacked`, `disputed`).
- The 2-value `status_fulfillment` dimension (`not_fulfilled`, `fulfilled`).
- How the two dimensions combine.

Not covered here:

- The cascade of side-effects that fires when a status changes — see [[order-status-side-effects]].
- Which statuses are gateway-driven vs merchant-set — see [[order-status-transitions]] and [[order-status-auto-transitions]].
- Custom statuses on top of the 11 — see [[order-status-custom]].
- Shared negative-status rules (revenue exclusion, fulfillment reset, etc.) — see [[order-status-negative-semantics]].

## Contrasts

- **Positive vs negative flow** — the 4 positive statuses (`authorized`, `pending`, `paid`, `completed`) are kept in revenue / fulfillment metrics; the 7 negative statuses are excluded. See [[order-status-negative-semantics]] for the shared negative rules.
- **`status` vs `status_fulfillment`** — `status` spans the full 11-value lifecycle; `status_fulfillment` is a parallel 2-value field (`not_fulfilled`, `fulfilled`) tracking only shipment progress. The two combine independently.
- **Merchant-pickable vs gateway-driven** — 6 of the 11 (`authorized`, `pending`, `paid`, `completed`, `cancelled`, `refunded`) are reachable from the admin dropdown / [[api-orders]]; the other 5 (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) are emitted only by payment-provider sync. See [[order-status-transitions]].
- **Order status vs payment status** — different field, different lifecycle. [[payment-status]] tracks the money; this concept tracks the operational state.

## Where it applies

The 11 + 2 taxonomy is the foundation for every screen, side-effect, and integration that touches an order. The headline application surfaces:

### Positive flow

Orders in these four statuses are counted in revenue, customer LTV, segment counts, and fulfillment dashboards.

| Status | What it means | Typical predecessor | Typical next step |
|--------|---------------|---------------------|-------------------|
| `authorized` | Payment authorisation held but not yet captured. Used by capture-style providers (Klarna, Stripe pre-auth, Borica Way4). | Order placed via a pre-auth provider. | `paid` once captured, or `voided` if released. |
| `pending` | Order placed, awaiting payment. **The default** for newly-created orders. | Default for new storefront orders and admin-placed orders awaiting payment. | `paid` once payment confirms, or `cancelled` / `failed` on payment failure. |
| `paid` | Payment captured / confirmed. Money is in. | `pending` after payment confirmation, or admin manual "Mark as Paid". | `completed` after fulfillment, or `refunded` if returned. |
| `completed` | Order is "done". Fulfilled and paid. | `paid` + `status_fulfillment = fulfilled`. | Terminal in the positive flow. Merchant may archive. |

Worth noting: `authorized` counts as a stock-decremented status under **both** decrement settings, exactly like `paid` and `completed` ([[settings-cart]] → `order_status_for_quantity_decrease`). Pre-auth providers therefore deplete inventory at the auth step, not when the capture clears — and stock is never given back while the order sits in `paid` / `authorized` / `completed`. See [[inventory-decrement-timing]].

### Negative flow

Orders in these seven statuses are **excluded** from revenue / income / segment reports. The shared semantics (fulfillment reset, stock restore, payment-auth release) plus the two rules unique to `cancelled` / `refunded` (auto-recorded return, reversal lock) are documented in [[order-status-negative-semantics]].

| Status | What it means | Trigger |
|--------|---------------|---------|
| `voided` | Payment authorisation cancelled before capture. | Merchant voids the auth, or auth expires. |
| `timeouted` | Payment provider did not respond in time. | Gateway timeout. |
| `cancelled` | Order cancelled by merchant or by auto-rule. | Merchant action, or [[settings-banned-ip]] auto-cancel rule. |
| `failed` | Payment failed at the provider. | Gateway rejection / declined card / etc. |
| `refunded` | Money returned to the customer. | Merchant issues refund via payment actions on [[orders-details]]. |
| `chargebacked` | Bank-initiated chargeback. | Payment provider reports a chargeback. |
| `disputed` | Order is under dispute / investigation. | Manual flag set by merchant or by provider event. |

Of the 7, five are **gateway-driven** (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) — not directly settable from the admin dropdown or JSON-API v2. They appear only via payment-provider sync. See [[order-status-transitions]] for the dropdown vs full-list distinction.

### Fulfillment status — the parallel dimension

`status_fulfillment` is its own field, independent of `status`:

- `not_fulfilled` — default. The courier hasn't dispatched yet.
- `fulfilled` — the courier has confirmed pickup or delivery.

The two combine to produce states like:

- `pending` + `not_fulfilled` — new order, awaiting payment and dispatch.
- `paid` + `not_fulfilled` — paid, ready to ship.
- `paid` + `fulfilled` — paid and shipped. Auto-promotes to `completed` if `order_complete = 1` (see [[order-status-auto-transitions]]).
- `completed` + `fulfilled` — done.

When the order flips into any negative status, fulfillment **resets to `not_fulfilled` in the same save** — see [[order-status-negative-semantics]] for the mechanics.

### The 11 are NOT extensible

The 11 built-in statuses are platform-wired — the merchant cannot add a 12th built-in. [[order-status-custom|Custom statuses]] are additional labels but they don't participate in the special semantics (negative-status array, counted-status array, stock-decrement trigger). Workflow needs that require new "built-in" semantics (e.g., a new negative status excluded from revenue) are not supported.

## Related

- [[order-status-workflow]] — hub.
- [[order]] — entity carrying `status` and `status_fulfillment`.
- [[order-status]] — entity page enumerating the 11 + custom values.
- [[shipping-status]] — fulfillment-status taxonomy.
- [[payment-status]] — separate field for the money lifecycle.
- [[settings-statuses]] — rename / add-custom UI.

## Open Questions

None.
