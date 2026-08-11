---
type: feature
nav_path: "Marketing → Discounts → Audit trail"
route_name: ""
route_path: ""
aliases: ["Discount audit trail", "Discount webhook events", "discount.created", "discount.updated", "discount.deleted", "Discount change log", "No audit log for discounts", "Order discount records", "Per-order discount rows", "Discount uses counter", "Аудит на отстъпки", "Webhook за отстъпки"]
tags: [marketing, discounts, promotions, webhooks, audit, change-log]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Discount audit trail & webhook events

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, eligibility, storefront display, known issues) plus per-type details.

## Purpose

This aspect covers **what record gets written** when a discount is created, updated, or deleted: the three webhook events (`discount.created` / `discount.updated` / `discount.deleted`) that fire to [[settings-hooks]] subscribers, the per-order discount rows that link redemptions to analytics, the `uses` counter mechanics, and the **important non-feature**: CloudCart does **NOT** capture an internal audit log for discount CRUD (no actor identity, no diff, no revision history). Merchants needing a compliance trail must keep their own log externally.

## Where to find it

- **Webhooks**: Sidebar → Settings → Hooks ([[settings-hooks]]).
- **Per-order discount rows**: appear in analytics dashboards at Sidebar → Analytics → [[analytics-top-order-discounts]] and [[analytics-top-order-product-discounts]].
- **Uses counter**: visible in the discount row on Sidebar → Marketing → Discounts (column `uses` / `max_uses`).
- **No internal change-log UI for discounts** — this is the absence by design.

## What the merchant can do here

- Subscribe an external system (CRM / loyalty platform / data warehouse) to discount lifecycle webhooks via [[settings-hooks]].
- Read per-discount and per-product redemption analytics on the analytics dashboards.
- Configure which order statuses cause the `uses` counter to tick (via the **Statuses** modal on the list page — see [[discounts-lifecycle]]).

## What the merchant CANNOT do here

- See "who changed this discount and when" inside CloudCart — there is no audit log.
- Roll back a discount to a previous configuration — no revision history.
- See a diff between today's discount config and yesterday's — same reason.

The merchant's only option for change tracking is to subscribe to `discount.updated` and store the payloads externally.

## Settings & fields

### Webhook events

| HookEvent | When it fires | Payload | Plan-gating |
|-----------|---------------|---------|-------------|
| `discount.created` | A discount is created (any type). | The Discount record. | Via [[settings-hooks]]. |
| `discount.updated` | A discount is edited OR its `active` toggled. Also fires for **per-row toggle**, **bulk-toggle**, and **per-product-attachment-regenerate completions**. | The updated Discount. | Via [[settings-hooks]]. |
| `discount.deleted` | A discount is deleted. | The deleted Discount's last state. | Via [[settings-hooks]]. |

### Order discount records (per-redemption)

When an order is placed with a discount, a per-order-discount row is created linking:

- `discount_id` — the redeemed discount.
- `order_id` — the order it was used on.
- `code_pro_id` (optional) — the specific PRO child code, if applicable.
- `order_product_id` (optional) — the specific line item, for per-line discounts.

These rows feed:

- The async **uses-counter sync** — recalculates `uses` from completed orders.
- [[analytics-top-order-discounts]] — most-used order-level discounts.
- [[analytics-top-order-product-discounts]] — most-used product-level discounts.

## Business rules

### No internal audit log — by design

CloudCart does NOT write an internal audit-log row for discount CRUD — no actor identity, no before / after diff, no revision history. Older wiki phrasing claimed a `api2` source tag was written on JSON-API-driven changes; that claim was **incorrect**.

Merchants needing a compliance trail must: (1) subscribe to `discount.*` via [[settings-hooks]]; (2) store the webhook payloads externally indexed by timestamp; (3) optionally cross-reference with their auth system's admin-login log to attribute changes to staff members. One of the most-requested features in discounts; not on the roadmap as of 2026-06 `(verify)`.

### Webhook events fire identically from API + admin

[[json-api-v2]] POST / PATCH / DELETE triggers the same webhooks as admin-panel saves. The payload does NOT distinguish admin-driven vs API-driven changes — no "source" field. Merchants filtering API-only changes must match on payload shape or correlate with their own API gateway logs.

### Per-code-PRO + Container ops bubble up to parent

Code PRO per-child-code CRUD (create / edit / delete / activate / bulk-generate) does NOT fire per-code webhooks — they all bubble up as `discount.updated` on the parent. Same for bulk-generated Container child codes (`discount_codes` table). The merchant fetches the codes list separately to know which child changed.

### `uses` counter — ticks on counted statuses only

The counter increments only when an order reaches one of the **counted statuses** (`discounts_used_statuses`, defaults `paid` / `completed` / `fulfilled`). A `pending` order does NOT yet consume a `max_uses` slot — reserved when status reaches `paid` (or the configured set). Cancelled / refunded / voided / chargebacked orders **NEVER** count. Same set covers `maxused_user` — see [[discounts-eligibility]]. Recomputed by an async sync job — brief lag between status change and counter update.

### Soft-delete preserves historical order-discount rows

Deleting cascades through targets, customer_groups, customers, per-variant fixed rows, and Code PRO child codes — but does NOT delete historical order-discount rows (preserved for accounting + analytics — [[analytics-top-order-discounts]] continues to show the deleted discount's redemptions, cached by name or shown as "Unknown discount #ID").

### Status-change event side-effect chain

Saving / toggling a discount fires more than just the webhook — it triggers a side-effect chain:

1. The webhook (`discount.created` / `discount.updated` / `discount.deleted`) is dispatched.
2. The per-product attachment regen job is queued — see [[discounts-storefront-display]].
3. The smart-collection refresh runs for any [[products-smart-collections]] affected by the discount's targets.
4. The listing-engine patches the `products_grid` listing rows with the new "from / now" prices.
5. (For deletes) Per-row cascade events delete dependent records (targets, customer_groups, per-variant fixed-price rows, Code PRO codes + their conditions).

The webhook receivers do NOT block any of these — webhooks fire in the same transaction but their delivery is async. A failing webhook receiver does not prevent the discount save.

### Idempotency for webhook receivers

`discount.updated` is **chatty** — it fires on every save, every toggle, every bulk-toggle, and (per the patterns documented for `product.updated` on [[settings-hooks]]) potentially on internal-only regeneration completions. Receivers must be:

- **Idempotent** — the same payload may arrive twice in close succession.
- **Latest-wins** — if two payloads for the same `discount.id` arrive out of order, the receiver should reconcile against the newest timestamp.

## Related

- [[marketing-discounts]] — hub.
- [[discounts-lifecycle]] — the `uses`-counter increment rules (counted statuses) + delete cascade.
- [[discounts-known-issues]] — corrections to older wiki claims (no `api2` source tag).
- [[settings-hooks]] — webhook subscription + delivery infrastructure.
- [[json-api-v2]] — programmatic CRUD that fires the same events.
- [[analytics-top-order-discounts]] — top order-level discount redemptions.
- [[analytics-top-order-product-discounts]] — top product-level discount redemptions.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[order-processing-pipeline]] — status transitions that drive `uses` ticking.

## Open questions

- Whether `discount.updated` fires when the **uses counter** ticks (i.e., on order status change, with no merchant edit) `(verify)`. If yes, receivers should be prepared for high event volume during heavy sale periods.
- Internal audit log: confirm there is no plan to add one in the next release cycle `(verify)`.
