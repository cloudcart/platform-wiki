---
type: entity
nav_path: "Entity → Product Status → Lifecycle and management"
aliases: ["Product Status lifecycle", "Default Product Statuses", "Status cache", "Delete Product Status", "Status seed at install", "No active flag"]
tags: [entity, catalog, products, statuses, lifecycle]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Product Status — Lifecycle and management

> Part of [[product-status]]. See the hub for related aspects (attributes, Conditional vs Non-conditional, evaluation precedence, action behaviour, storefront rendering).

## Identity

This page covers the **lifecycle** of a Product Status row — from store-install auto-seeding through merchant edits to deletion — plus the unusual quirks: there is no `active` / `enabled` flag, deletes are silent (NULL the references on every assigned product), and the entire Status table is cached store-wide with a 24-hour TTL.

## Aliases

- **Status lifecycle** — the Create → Active → Re-evaluated → Updated → Deleted sequence.
- **Default Statuses** / **Seeded Statuses** — the 2 rows inserted at store-provisioning.
- **Status cache** — the in-memory full-table load with 24-hour TTL.

## Key Attributes

### Lifecycle states

A Product Status moves through:

1. **Created** — the merchant adds a status in [[products-statuses]] via the Add modal. The modal's quantity operator decides whether the status lands in the Conditional table or the Non-conditional table (see [[product-status-conditional-vs-non-conditional]]).
2. **Active in catalog** — the platform applies the status:
   - **Conditional**: evaluated automatically against the product's aggregate stock count on every storefront query.
   - **Non-conditional**: the merchant manually picks the status on a product (via the product editor's status dropdown OR the bulk action *"Change product status"* on [[products-products]]).
3. **Re-evaluated in real-time** — when an order changes stock (decrement on checkout per [[settings-cart]]'s `order_status_for_quantity_decrease`, increment on cancellation), the product's Conditional status is re-evaluated immediately. The customer browsing the storefront sees the new status on the next page load.
4. **Updated** — the merchant edits the status (rename, change operator, change action). Cache busts on save.
5. **Deleted** — the merchant clicks Delete on the row. References on assigned products are silently NULLed (see *"Deleting a referenced Product Status nulls the references silently"* below).

### Auto-creation: 2 default Statuses are seeded at store install

When a new store is provisioned, the platform inserts two default Conditional Statuses:

1. **In stock** — operator *"Greater than"*, quantity 0 — translation key `product.stock.install.in_stock`.
2. **Out of stock** — operator *"Lower than"*, quantity 1 — translation key `product.stock.install.out_stock`.

The merchant can rename / delete them like any other Status. These exist purely so a freshly-installed storefront has working badges before the merchant has configured anything.

### Deleting a referenced Product Status nulls the references silently

Delete is **NOT blocked** when products still reference the Status — the platform silently sets `Product.status_id` and `Product.out_of_stock_id` to NULL on every product that held the deleted Status. There is no in-use protection. Products without a status reference fall back to default rendering (the next matching Conditional rule, or no badge per the fallback chain in [[product-status-evaluation-precedence]]).

### No active/inactive flag on Product Status

There is no per-status `active` / `enabled` toggle. To temporarily disable a Status, the merchant must either delete it or set its quantity operator to a value that never matches the catalog (e.g., *"Equals 99999"*). This is a deliberate simplification — the Conditional / Non-conditional split + the sort-order priority chain are considered the only knobs the merchant needs.

### Status data is cached store-wide

The full Status table is loaded once per request and cached in memory (24-hour TTL). Renaming, adding, or deleting a Status auto-busts the cache on save — but any code path that has already loaded the Status during the same request sees the OLD value. This means: a bulk-action that flips statuses on hundreds of products in one request sees the pre-edit Status definitions for the entire run.

### Status name change is non-destructive

Renaming a Status updates the `name` field only. The row's `id` stays stable, so every product reference (`status_id` / `out_of_stock_id`) keeps working. The merchant can rename freely without breaking anything — the only impact is on the customer-facing badge text, which updates on the next storefront cache flush.

### No webhook for status changes directly

Product Status changes (create / rename / delete) do NOT fire a webhook of their own. The underlying stock change that triggers status re-evaluation fires `product.updated` via [[settings-hooks]] — but the Status-row CRUD events are silent. Subscribers wanting to detect a status definition change must poll the taxonomy.

### `sorting` auto-assignment on create

When a new Conditional Status is created, the platform auto-assigns `sorting = max(existing sorting) + 1` — appending to the bottom of the list. Non-conditional Statuses get `sorting = 0` and don't participate in the priority chain. See [[product-status-evaluation-precedence]] for how `sorting` drives evaluation.

## Where it appears

- [[products-statuses]] — the management screen where create / edit / delete happen.
- [[product]] — the entity that carries `status_id` and `out_of_stock_id` references that get NULLed on delete.
- [[settings-hooks]] — `product.updated` fires on stock changes that trigger status re-evaluation; no webhook fires for Status-row CRUD itself.

## Related

- [[product-status]] — hub.
- [[products-statuses]] — taxonomy management screen.
- [[product]] — the entity holding the two slot references.
- [[settings-hooks]] — `product.updated` webhook.
- [[settings-cart]] — `order_status_for_quantity_decrease` drives when re-evaluation fires.

## Open Questions

None.
