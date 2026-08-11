---
type: entity
nav_path: "Entity → Order → Lifecycle"
aliases: ["Order lifecycle", "Order status transitions", "Order draft state", "is_draft order", "Order auto-promotion", "Order completed auto-set", "Order archive status gate"]
tags: [entity, orders, lifecycle, status, transitions]
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[order]]. See the hub for the other aspects (identifiers, money, side-effects, API access).

# Order — Lifecycle

## Identity

An Order's **lifecycle** is the path it travels through 11 canonical statuses (plus a Draft sub-state and an independent fulfillment status) — from placement to either completion (positive flow) or a negative end-state (cancel, refund, void, chargeback, dispute, fail, timeout). Three drivers shape it: payment events from the gateway, fulfillment events from the courier, and direct merchant actions on [[orders-details]] / [[orders-status-change]]. Transitions are NOT strictly state-machine-enforced — in principle any status can move to any other — but **action-specific gates** block most in practice (cancel only from `pending`, complete only from `paid + fulfilled`, etc.). Every transition is audited on [[orders-history]].

This page covers **what the Order carries to drive the lifecycle**: the `status` and `status_fulfillment` fields, the Draft sub-state, the three status-change guards, and the auto-promotion / auto-cancel rules. For what fires on each transition see [[order-status-workflow]] and the [[order-status]] aspects.

## Aliases

- **Order status** — the `status` field (one of 11 canonical values).
- **Fulfillment status** / **Shipping status** — the `status_fulfillment` field (`not_fulfilled` / `fulfilled`).
- **Draft order** — the `is_draft = 1` meta state; a separate flag, not a 12th status.
- **Status pill** — the colour-coded badge on [[orders-details]] showing the current status.

## Key Attributes

### Canonical statuses (the 11)

The `status` field is one of these 11 lowercase enum values:

**Positive flow** (4 — kept in revenue / fulfillment metrics):

| Value | Meaning |
|-------|---------|
| `authorized` | Payment authorised (pre-auth hold), not yet captured. Used by capture-style providers. |
| `pending` | Order placed, awaiting payment. **The default** for newly-created orders. |
| `paid` | Payment captured / confirmed. |
| `completed` | Fulfillment complete; the order is "done". Auto-set when `paid` AND `fulfilled` AND `order_complete` is on. |

**Negative flow** (7 — excluded from revenue / fulfillment / many analytics):

| Value | Meaning |
|-------|---------|
| `voided` | Payment authorisation cancelled before capture. |
| `timeouted` | Payment provider timed out without confirming. |
| `cancelled` | Order cancelled by merchant or by [[settings-banned-ip|banned-IP]] auto-cancel. |
| `failed` | Payment failed at the provider. |
| `refunded` | Money returned to the customer. |
| `chargebacked` | Bank-initiated chargeback. |
| `disputed` | Under dispute / investigation. |

The full taxonomy (pill colours, merchant-facing labels) lives on [[order-status-entity-canonical-values]].

### Fulfillment status (independent of `status`)

The `status_fulfillment` field runs in parallel: `not_fulfilled` (default; courier hasn't dispatched) or `fulfilled` (courier confirmed pickup / delivery). Analytics treat the two as **independent dimensions** — "where is the order in the workflow?" vs "has the package gone out?". See [[order-status-workflow]] for the interaction matrix.

### Draft sub-state (NOT in the 11)

An Order created via [[orders-add]] is saved with the meta-flag `is_draft = 1`. While it is set the order is **invisible to the customer**, **no confirmation emails** fire, **stock is NOT decremented**, and it does NOT count toward analytics or discount uses.

The merchant clears draft by clicking **Create order** on [[orders-details]]: `is_draft` is cleared and the normal post-create pipeline runs (confirmation email, stock decrement per the [[settings-cart|`order_status_for_quantity_decrease`]] setting, `order.created` webhook — see [[order-entity-side-effects]]).

### The three status-change guards

The validated status-change path (the status pill / dropdown UI on [[orders-status-change]]) enforces three guards:

| Target status | Guard | Error string |
|---------------|-------|--------------|
| `completed` | Rejected unless the order is `paid` AND `fulfilled` | *"Only paid and fulfilled orders can be completed"* |
| `cancelled` | Rejected if the order is currently `paid` or `completed` | *"Only pending orders can be canceled"* |
| Any change on an archived order | Rejected | *"Status of archived order cannot be changed. Unarchive first."* |

These guards run only on the validated UI path. **Gateway-sync paths skip them** — used where a status the UI would block must be overwritten (e.g. a Stripe webhook marking a `completed` order `refunded`). See [[order-entity-api-access]] for which JSON-API v2 paths go through the guards.

### Auto-promotion: `paid + fulfilled + order_complete` → `completed`

Whenever the Order is saved as `paid` AND `fulfilled` AND the store setting `order_complete` is on, the status is rewritten to `completed` in the **same** write. **Two history rows result**: the explicit transition plus the auto-promotion. This is what makes fulfilling a paid order (generating its waybill) silently complete it in one click. Because promotion shares that write, the moderator lock (see [[order-entity-side-effects]]) covers both — no window for another admin in between. See [[order-status-auto-transitions]] for the full mechanics.

### Auto-cancel: banned-IP on offline-payment orders

The [[settings-banned-ip|banned-IP]] check runs on order creation **only when the payment provider is not online** (`is_online_payment` is false); online providers (Stripe, PayPal, Borica, etc.) handle fraud upstream and are skipped. On a match the order is cancelled **silently**: customer notification is suppressed (`notify_customer = 0`, no email), the ban reason is written to `note_administrator`, and the status moves to `cancelled` with no admin notification. See [[order-entity-side-effects]] for the full cancel effect chain.

### Fulfillment removal walks the order back

When fulfillment is **removed** (fulfillment row actions on [[orders-details]]): `status_fulfillment` resets to `not_fulfilled`; the order rolls back to `paid` if the last payment is `completed`, else to `pending`; and stock is re-credited **only if the decrement trigger is `paid`** (under `pending`-decrement mode stock dropped at placement and isn't tied to fulfillment). See [[orders-shipping-waybill]] for the UI and [[inventory-restock]] for the stock-return rules.

### Archive is gated by status

Archiving a non-draft order is permitted only when its `status` is `completed` OR `cancelled` — any other raises *"Only completed orders can be archived"*. **Draft orders (`is_draft = 1`) bypass this check** and archive from any state. The gate is enforced at the data layer, so both the JSON-API v2 path and the admin UI honour it. See [[orders-archive]] for the merchant flow.

### Custom statuses don't replace the 11

Custom statuses defined in [[settings-statuses]] are **sub-labels layered onto the canonical 11** — each maps to one underlying code, and the gates above check the **underlying canonical status**, not the custom label. See [[order-status-entity-custom-statuses]] for the layering rules.

## Where it appears

- [[orders]] — status filter, bulk "Mark as completed", archive filter.
- [[orders-details]] — status pill; ~40 sub-actions check the current status.
- [[orders-status-change]] — single + bulk status change (goes through the guards).
- [[orders-history]] — every transition writes a history row (two for auto-promotion).
- [[orders-add]] — admin manual order creation starts in Draft.
- [[orders-archive]] — archive / unarchive (status-gated except for drafts).
- [[settings-statuses]] — rename built-ins, add custom statuses, notification toggles.
- [[settings-cart]] — `order_complete` and `order_status_for_quantity_decrease` settings.
- [[settings-banned-ip]] — auto-cancel for offline-payment orders.
- [[order-status-workflow]] — Order × Payment × Fulfillment interaction.
- [[order-processing-pipeline]] — full transition pipeline.

## Related

- [[order]] — hub.
- [[order-status]] — the status taxonomy.
- [[order-status-entity-canonical-values]] — pill colours, merchant-facing labels per status.
- [[order-status-entity-custom-statuses]] — custom-status layering rules.
- [[order-status-auto-transitions]] — auto-promotion + auto-cancel in full.
- [[order-status-action-gates]] — gate matrix per status × action.
- [[order-status-workflow]] — Order × Payment × Fulfillment interaction.
- [[order-processing-pipeline]] — full transition pipeline.
- [[payment-status]] — independent payment-side enum.
- [[shipping-status]] — `status_fulfillment` taxonomy.
- [[inventory-decrement-timing]] — when stock drops per `order_status_for_quantity_decrease`.
- [[inventory-restock]] — stock re-credit on fulfillment removal / cancel.
- [[settings-banned-ip]] — banned-IP auto-cancel.

## Open Questions

- Verify the verbatim strings of the status-change guard error messages against current source.
- Verify the stock re-credit behaviour on fulfillment removal.
