---
type: entity
nav_path: "Entity → Discount → Lifecycle"
aliases: ["Discount lifecycle", "Discount states", "Discount uses counter"]
tags: [marketing, discounts, entity, lifecycle]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

# Discount — Lifecycle

> Part of [[discount]]. See the hub for related aspects (fields, business rules, stacking, webhooks/API).

## Identity

The set of state transitions a Discount row goes through from creation to expiry / deletion, plus the activation cooldown, the per-product attachment regeneration, and the `uses` counter recompute semantics.

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
- **Expired** — `date_end` is in the past. The daily auto-disable job flips `active` to `no` for discounts expired more than 1 day.
- **Inactive** — `active = no`. Configured but not firing. The merchant can re-enable.

### Status-change rate limit (10-minute cooldown)

The merchant can only toggle a discount's `active` once per **10 minutes**. Within the cooldown, the merchant sees: *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."* This prevents thrashing the per-product attachment regeneration job that fires on every state change.

### Per-product attachment regeneration

When a discount is created, edited, toggled, or deleted, a background job rebuilds the `product_to_discount` attachment rows for each affected product. These rows feed the storefront's "from X / now Y" pricing on category pages and product detail pages. For high-catalog stores (10,000+ products), this regeneration can take minutes — hence the 10-minute activation cooldown and the "Latest update: :date" badge shown on freshly-saved discounts.

### `uses` counter — recomputed, not incremented

Despite the field name, `uses` is **not auto-incremented per redemption** — it is **recomputed from scratch** every time an order using the discount changes status. The recompute logic counts all distinct orders that reference the discount and have reached a counted status (per the `discounts_used_statuses` setting — default: `paid`, `completed`, `fulfilled`).

This means:

- **Cancelling a previously-counted order automatically DECREMENTS the counter.** The cancelled order no longer counts, and the recompute drops it from the total. If `uses` had hit `max_uses`, this can free the discount up to fire again at checkout.
- **Recovering a cancelled order back to a counted status re-counts it.** The recompute picks it back up.
- **The recompute is async** — a job is dispatched with a **10-second delay** to the `order-events6` queue on every order status change. It runs even if the synchronous in-listener step fails (e.g., a clustered-database write conflict) — the async job acts as a reliable fallback. (verify queue name)
- **For Code PRO**, each child code's `uses` is recomputed individually AND the parent's `uses` is recomputed as `SUM(uses)` across all child codes. So a single status change triggers a per-code re-tally + parent-aggregate update.

Orders in negative statuses (`cancelled`, `refunded`, etc.) never count, regardless of `discounts_used_statuses` configuration.

### Counted statuses are configurable per store (with default fallback)

The `discounts_used_statuses` setting holds a JSON array of order statuses that count toward `uses`. The merchant can override the default via [[settings-statuses]]. The default kicks in when:

- The setting is empty or not JSON-decodable.
- The configured statuses don't match any currently-valid order statuses.

Default: `paid`, `completed`, `fulfilled`. Fulfillment-only statuses are checked against the order's `status_fulfillment` column; normal statuses are checked against `status`. Any `NEGATIVE_STATUS` (`cancelled` / `refunded`) is excluded even when `status_fulfillment` matches.

### Code PRO sub-lifecycle

Each code under a Code PRO parent has its OWN `active` flag, date window, max-uses, customer-group restriction, and region. The PRO parent can be active while a specific child code is disabled, or vice versa. Code-level bulk-toggle is supported separately from the parent discount.

### Soft-delete cascade

Deleting a discount also removes related target rows, customer-group restrictions, per-variant attachments, and quantity-tier rows. Historical per-order-discount rows are **preserved** for accounting and analytics — so the discount can be deleted without losing the audit trail of which orders used it. Container / Code PRO parent deletion cascades to all child code rows — see [[discount-entity-business-rules]].

## Where it appears

- [[marketing-discounts]] — list view shows the current lifecycle state per row.
- [[orders-status-change]] — every order status transition triggers the `uses` recompute job.
- [[settings-statuses]] — `discounts_used_statuses` configuration.

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — the `active`, `date_start`, `date_end`, `uses`, `max_uses` fields.
- [[discount-entity-business-rules]] — soft-delete cascade + save-time normalisation that runs on every state change.
- [[discount-entity-webhooks-api]] — the `discount.updated` webhook fires on every `active` toggle.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[order]] / [[orders-status-change]] — status transitions drive the `uses` recompute.

## Open Questions

- ⏸️ **Auto-cleanup of expired Container codes** — does the daily auto-disable job also disable individual child Container codes whose own date has passed, or only the parent discount? Container codes don't carry their own `date_end` column (verified — see [[discount-code]]), so this question is partly moot; the only date check is at the parent level.
