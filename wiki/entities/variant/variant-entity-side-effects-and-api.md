---
type: entity
nav_path: "Entity → Variant → Side effects & API"
aliases: ["Variant side effects", "Variant JSON-API v2 access", "Variant API", "Variant save side effects", "Variant API differences from admin", "Variant clamping"]
tags: [entity, catalog, variants, api, side-effects]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[variant]]. See the hub for the other aspects (attributes, lifecycle, relationships, business rules).

# Variant — Side effects & API

## Identity

What happens *around* a [[variant|Variant]] save or delete — the parent Product's `date_modified` tick, the storefront search re-index, the `updateProductsDefaultVariant` re-evaluation, the storefront `product.updated` webhook, the back-in-stock email batch on restock — and how the **JSON-API v2** path differs from the admin path (the one path that does NOT clamp `quantity` to ≥ 0, the silent-vs-loud duplicate-SKU behaviour, the no-standalone-create rule).

This is the page the AI Assistant cites when a merchant integrates a third-party ERP / WMS / replatform tool and the inventory numbers come out unexpected — typically because the integration writes through JSON-API v2 and the admin clamps were never applied.

## Aliases

- **Variant API** — JSON-API v2 access via [[api-variants]].
- **Variant save side effects** — the side-effect chain on every save.
- **API vs admin clamping difference** — the one rule that diverges between the two paths.

## Key Attributes

### Side effects on every Variant save (both paths)

A POST / PATCH / save on a Variant — from any path (admin UI, CSV import, JSON-API v2, ERP sync, GraphQL) — triggers the following side-effect chain:

- **Parent Product's `date_modified` ticks** — the audit timestamp on the Product (NOT the Variant — see [[variant-entity-business-rules]]) updates so the change is observable from product-list sorts and the [[products-change-log|Change log]].
- **Storefront search re-index** — the per-Variant text + price data is re-pushed to the search index via the chunked import on the `searchable-import4` queue. The storefront catalog + filter pages read from the search index, not the primary database, so the storefront reflects the change only after the queue processes the affected product. See [[storefront-architecture]] + [[background-queue-inventory]].
- **`updateProductsDefaultVariant` re-runs** — if the price change makes a different Variant the cheapest, the Product's `default_variant_id` re-points and `price_from` / `price_to` re-compute. See [[variants-matrix-generation]].
- **Storefront cache invalidation** — product-detail, category, and variant-picker fragments are flushed.
- **`product.updated` webhook fires** — chatty; receivers must be idempotent. Every stock decrement, every price edit, every CSV-import row drives one webhook per affected Product. See [[settings-hooks]].
- **Back-in-stock email batch on restock transition** — if the Variant's `quantity` transitions from `<= 0` to `> 0`, the back-in-stock waitlist for that Variant is queried, emails dispatched, and waitlist rows cleared. See [[products-missing-product]].
- **Low-stock email on threshold cross** — if `quantity` drops to or below the per-Variant `threshold` (or the per-Product / store-wide fallback), the `product_quantity_low` admin email fires. See [[settings-cart]] + [[settings-admin-notifications]].
- **Change log entry** — every Variant `quantity` change is recorded in the parent product's [[products-change-log|Change log]] with timestamp + Initiator (admin user / `api2` / import source). See [[inventory-debugging-playbook]].

### JSON-API v2 access — [[api-variants]]

The Variant entity can be read, created, updated, or deleted via **JSON-API v2** — the resource exposes SKU, barcode, price, `compare_at_price`, `cost_price`, quantity, weight, dimensions, image, the `p1` / `p2` / `p3` Parameter Option references, and unit-of-measure metadata. See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

**No standalone create** — Variants always live under a parent product. The API expects a `product_id` (or a nested create under the product). A POST without a parent fails validation.

**Same side effects apply** — a POST / PATCH on a Variant through JSON-API v2 fires the parent product's `date_modified`, runs the search re-index, re-runs `updateProductsDefaultVariant`, fires the `product.updated` webhook, and fires the back-in-stock email if the quantity transitions from `<= 0` to `> 0` (see above). SKU uniqueness is validated store-wide on both paths — duplicates return 422 on the admin + JSON-API paths (the bulk CSV import path is the only one that silently skips duplicates).

### The one key difference: JSON-API does NOT clamp `quantity ≥ 0`

As documented for [[products-inventory]], the **admin inventory grid clamps quantity to ≥ 0** — typing `-5` in the inventory grid is silently coerced to `0`. The **JSON-API v2 path does NOT clamp** — a PATCH can drive a Variant's `quantity` into negative inventory directly (subject to `tracking = yes` + `continue_selling = yes` on the parent product).

This is intentional — integrations that sync from an external WMS / ERP need to faithfully replay the WMS's state, including transient negative numbers during a multi-step sync. But it means a merchant who installs an ERP integration and sees "-3 in stock" is seeing the API behaviour, not a CloudCart bug. See [[inventory-oversell]] for the broader oversell model (stock does NOT go negative on the order-decrement path; only the JSON-API write path can).

### Caps that enforce on both paths

- **500 Variants per product cap** — enforced at product-save validation on both admin and JSON-API. Error reads *"max allowed 500 exceeded"*.
- **3-Parameter-Option-references-per-Variant cap** — the data model has only `p1` / `p2` / `p3` slots; no v4 exists. Both paths reject a 4-slot payload.

### Deletion semantics on either path

Deleting a Parameter Option through either path soft-removes (hard-deletes) the referencing Variants. Order line items' `variant_id` is set NULL via `ON DELETE SET NULL`, and the order's snapshotted SKU + denormalised labels remain readable. See [[variant-entity-business-rules]] + [[variant-entity-lifecycle]].

Deleting a Variant directly via JSON-API v2 has the same cascade — `ImageVariant` rows and external-meta-data rows are removed by the model's `deleting` hook before the Variant row goes.

## Where it appears

- [[api-variants]] — the JSON-API v2 resource.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[products-inventory]] — the admin clamp at ≥ 0.
- [[products-change-log]] — Change log audit trail; first stop for unexpected stock-change tickets.
- [[settings-hooks]] — `product.updated` webhook subscription.
- [[settings-admin-notifications]] — low-stock email gating.
- [[apps-csv-import]] — the silent-skip-duplicates path.

## Related

- [[variant]] — hub.
- [[api-variants]] — JSON-API v2 resource.
- [[json-api-v2]] — JSON-API v2 framework.
- [[product]] — parent record; `date_modified` ticks on every Variant save.
- [[inventory-tracking]] — broader inventory model.
- [[inventory-oversell]] — clamping at 0 on the order-decrement path (the API path can go negative; the order-decrement path cannot).
- [[inventory-decrement-timing]] — order-status-driven decrement.
- [[inventory-restock]] — symmetric re-credit on cancel / refund.
- [[products-missing-product]] — back-in-stock email batch on restock.
- [[storefront-architecture]] — the search index read-side; why storefront lags after a save.
- [[background-queue-inventory]] — the `searchable-import4` queue.
- [[products-change-log]] — Change log audit trail.

## Open Questions

None.
