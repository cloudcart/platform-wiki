---
type: entity
nav_path: "Entity → Discount → Lifecycle"
aliases: ["Discount lifecycle", "Discount states", "Discount uses counter"]
tags: [marketing, discounts, entity, lifecycle]
created: 2026-06-10
updated: 2026-11-04
source_count: 6
---

# Discount — Lifecycle

> Part of [[discount]]. See the hub for related aspects (fields, business rules, stacking, webhooks/API).

## Identity

The set of state transitions a Discount row goes through from creation to expiry / deletion, plus the status switch, the per-variant row regeneration, and the `uses` counter recompute semantics.

## Aliases

- "Discount states" — the four named lifecycle states below.
- "Uses counter" — the recompute-not-increment behaviour of `uses`.

## Key Attributes

### Discount-level lifecycle

```
created → scheduled (date_start in future)
         → active (date_start <= today AND date_end >= today AND uses < max_uses)
         → expired (date_end passed OR uses >= max_uses)
         → inactive (active = 'no')
```

**State definitions:**

- **Scheduled** — `active = yes` AND `date_start > today`. Configured but not yet firing.
- **Active** — `active = yes` AND inside the date window AND uses-remaining. The platform's discount-lookup engine evaluates this discount at every cart / checkout.
- **Expired** — `date_end` is in the past. An hourly sweep switches `active` to `no` at the first run after 00:00 UTC on the day after `date_end`. It acts on discounts only: Container codes carry no date.
- **Inactive** — `active = no`. Configured but not firing. The merchant can re-enable.

### Status switch

The switch in the Discounts list, the bulk status action, the edit form and GraphQL take effect immediately, any number of times, on every discount type.

### Per-variant rows

When a no-code Flat, Percent, free-shipping or Fixed discount is created or saved through its form, its per-variant rows are written during the save. These rows feed the storefront's "from X / now Y" pricing on category pages and product detail pages. The listing engine and smart collections are refreshed afterwards. The list switch, bulk status and list delete start no rebuild. See [[discount-stacking-product-rows]].


### `uses` counter — recomputed, not incremented

Despite the field name, `uses` is **not auto-incremented per redemption** — it is **recomputed from scratch** every time an order using the discount changes status. The recompute logic counts all distinct orders that reference the discount and have reached a counted status (per the `discounts_used_statuses` setting — default: `paid`, `completed`, `fulfilled`).

This means:

- **Cancelling a previously-counted order automatically DECREMENTS the counter.** The cancelled order no longer counts, and the recompute drops it from the total. If `uses` had hit `max_uses`, this can free the discount up to fire again at checkout.
- **Recovering a cancelled order back to a counted status re-counts it.** The recompute picks it back up.
- **The recompute is async** — a job is dispatched with a **10-second delay** on every order status change. It runs even if the synchronous in-listener step fails (e.g., a clustered-database write conflict) — the async job acts as a reliable fallback.
- **For Code PRO**, each child code's `uses` is recomputed individually AND the parent's `uses` is recomputed as `SUM(uses)` across all child codes. So a single status change triggers a per-code re-tally + parent-aggregate update.

By default, `cancelled` and `refunded` orders do not count. A merchant can add Cancelled or Refunded to the list, and those orders then count; `chargebacked`, `disputed`, `timeouted`, `failed` and `voided` are not selectable.

### Counted statuses are configurable per store (with default fallback)

The `discounts_used_statuses` setting holds a JSON array of order statuses that count toward `uses`. The merchant can override the default via [[settings-statuses]]. The default kicks in when:

- The setting is empty or not JSON-decodable.
- The configured statuses don't match any currently-valid order statuses.

Default: `paid`, `completed`, `fulfilled`. Fulfillment-only statuses are checked against the order's `status_fulfillment` column; normal statuses are checked against `status`, so a pending order marked fulfilled counts under the defaults. The total recount leaves out negative statuses for fulfilled orders; the per-customer count does not.

### Code PRO sub-lifecycle

Each code under a Code PRO parent has its OWN `active` flag, date window, max-uses, customer-group restriction, and region. The PRO parent can be active while a specific child code is disabled, or vice versa. Code-level bulk-toggle is supported separately from the parent discount.

### Delete

A discount used in a smart collection or an XML import / sync task cannot be deleted from the list: *"This discount cannot be deleted because it is still used in: ..."*. Deleting a discount also removes related target rows, customer-group restrictions, per-variant attachments, and quantity-tier rows (verify). Historical per-order-discount rows are **preserved** for accounting and analytics — so the discount can be deleted without losing the audit trail of which orders used it. See [[discount-entity-business-rules]].

## Where it appears

- [[marketing-discounts]] — list view shows the current lifecycle state per row.
- [[orders-status-change]] — every order status transition triggers the `uses` recompute job.
- [[settings-statuses]] — `discounts_used_statuses` configuration.

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — the `active`, `date_start`, `date_end`, `uses`, `max_uses` fields.
- [[discount-entity-business-rules]] — delete + save-time normalisation that runs on every save.
- [[discount-entity-webhooks-api]] — `discount.updated` fires on a save through the form or JSON-API; the Active switch sends none.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[order]] / [[orders-status-change]] — status transitions drive the `uses` recompute.

## Open Questions

None.
