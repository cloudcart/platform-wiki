---
type: feature
nav_path: "Orders → Ordered Products → Export → Filter scope"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export filters", "Products by orders export scope", "Aggregated product export status filter", "Order products export demand accuracy"]
tags: [orders, products, export, csv, filters, scope]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-ordered-products-export]]. See the hub for related aspects (trigger / 2FA, CSV schema, sync vs async, delivery, permissions / plan).

# Ordered Products export — filter scope

## Purpose

Documents **what data the export captures** — the filters it inherits from the pivot page, when that snapshot is taken, why a status filter matters for demand accuracy, and the consequence of exporting with no filters at all. The export contains exactly what the merchant sees on screen; this page explains the edge cases of that promise.

## Where to find it

Filters are set on the [[orders-ordered-products]] page (supplier when applicable, order date range, order ID range, order status, property option). The merchant sets them BEFORE clicking **Export** — the filter snapshot is taken at export-trigger time.

## What the merchant can do here

- Narrow the pivot by supplier, date range, order ID range, status, and property option before exporting.
- Export the exact filtered view they currently see.

The merchant CANNOT select individual rows (no checkboxes on the parent pivot) — the export uses the filter scope, not row selection. There is also no UI-exposed filter beyond those on the pivot page.

## Settings & fields

The filter controls live on the parent [[orders-ordered-products]] page, not on the export itself. The export reads whichever filters are active at click time:

| Filter | Effect on the export |
|--------|----------------------|
| Order date range | Restricts to orders placed in the range. |
| Order ID range | Restricts to a contiguous order-ID window. |
| Order status | Restricts to selected status(es) — see the demand-accuracy rule below. |
| Property option | Restricts to products carrying a chosen property option. |
| Supplier (Suppliers app) | Restricts to one supplier; also drives the supplier-column rename in [[ordered-products-export-csv-schema]]. |

## Business rules

### Export respects the current filter scope

The export captures the SAME filters the merchant applied on [[orders-ordered-products]]. Whatever the merchant sees in the pivot is what the export contains. The filter snapshot is taken at export-trigger time, then frozen for the run (the async path serialises it — see [[ordered-products-export-sync-vs-async]]).

### Status filter strongly recommended

The pivot includes orders of ALL statuses by default — including cancelled / refunded / failed. Without a status filter (e.g., `paid + completed`), the exported quantities may **overstate real demand**. This is a "should-apply" pattern, not enforced. See [[settings-statuses]] for the status taxonomy.

### Empty filter / unbounded scope

If the merchant clicks Export with no filters applied, the export covers ALL ordered products across the store's entire history. This will almost certainly trigger async mode (see [[ordered-products-export-sync-vs-async]]) and produce a very large file. The merchant should always apply a date / status filter first for meaningful exports.

### Fresh aggregation re-run at export time

The export does NOT reuse a cached aggregation from the page render. It re-runs the pivot query with the filters and produces fresh rows. Small differences may appear between what the merchant saw on screen and what is in the CSV if orders changed between page render and Export click — but this is rare.

### Filters identical between page and export

The pivot's filters and the export use the SAME filter pipeline, ensuring parity between page display and exported rows. Filters that do not appear in the UI are not exposed in the export either.

## Related

- [[orders-ordered-products-export]] — hub.
- [[orders-ordered-products]] — parent pivot page where filters are set.
- [[ordered-products-export-sync-vs-async]] — the click-time snapshot the async path freezes.
- [[ordered-products-export-csv-schema]] — supplier filter drives the supplier-column rename.
- [[settings-statuses]] — status taxonomy used by the status filter.
- [[products-property]] — properties / options used by the Property-option filter.
- [[order]] — entity page (the underlying orders).

## Open questions

None.
