---
type: feature
nav_path: "Orders → Ordered Products → Filters"
route_name: suppliers.products_by_orders
route_path: /admin/products_by_orders
aliases: ["Ordered Products filters", "Products-by-orders filter rail", "Property-option filter", "Ordered Products date filter", "Поръчани продукти — филтри"]
tags: [orders, products, filters, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-ordered-products]]. See the hub for related aspects (overview, aggregation, status scope, suppliers, API).

# Ordered Products — filters

## Purpose

The filter rail on the [[orders-ordered-products]] pivot: the five visible filters, their operator structure, the two-step property-option picker, and the hidden text-search filter. This aspect answers "how do I narrow the pivot?". The downstream effect of the status / date filters on *what gets counted* is in [[ordered-products-status-scope]]; the supplier filter's cheapest-in-stock logic is in [[ordered-products-suppliers]].

## Where to find it

Sidebar → **Orders** → **Ordered Products** → filter rail (included from `orders/filters/supplier_products`). The rail renders inline on the page — there are no filter modals.

## What the merchant can do here

### Filters (4 — or 5 with the Suppliers app)

| Filter | Key | Visible | Operator structure |
|--------|-----|---------|--------------------|
| **Supplier** | — | Suppliers app only | Single-select from configured suppliers — see [[ordered-products-suppliers]]. |
| **Order date interval** | `fromToDate` | Always | From + To with date+time pickers. Restricts the aggregate to orders placed in the window. |
| **Order ID interval** | `fromToId` | Always | From + To numeric range (e.g. "products from orders 1000–2000"). |
| **Order status** | `orderStatus` | Always | Single-select from the configured order statuses ([[settings-statuses]]). |
| **Property option** | `propertyOption` | Always | Two-step picker: `property_id` (autocomplete) → `option_id` (autocomplete, depends on property). |

### The two-step property-option filter

When the merchant picks **Property option**:

1. First input — autocomplete for the property name (e.g. "Color" from [[products-property]]).
2. After selecting, a second input appears — autocomplete for the option values within that property (e.g. "Red", "Blue"). It is dynamically loaded based on the first.

**Both** must be set for the filter to apply.

## Settings & fields

### Filter operator detail

| Filter | Operator |
|--------|----------|
| Supplier | Single-select dropdown |
| Order date interval | From + To (datetime) |
| Order ID interval | From + To (numeric) |
| Order status | Single-select from configured statuses |
| Property option | `property_id` (autocomplete) → `option_id` (autocomplete, depends on property) |

### Hidden text-search filter

The page exposes a "search" text input that is **not** in the visible filter rail. When used, the platform searches across **product name, SKU, barcode, vendor name, category name** — and, if the term is purely numeric, ALSO against the **order ID**. So typing `1234` finds products from order #1234 as well as products with an SKU containing `1234`.

- Each search word is **AND-ed** (multi-word searches narrow down).
- Matching uses `LIKE %word%` (substring match per field).

### Two date-filter variants

The filter object supports both `fromToDate` (with a time component) and `dateRange` (date only, no time). The UI only exposes the datetime variant ("Order date interval"). API callers may use the date-only variant.

## Business rules

### Property-option filter requires BOTH property AND option

The `option_id` must match the selected `property_id`. If the merchant submits an option that doesn't belong to the property (e.g. via stale autocomplete), the filter silently does nothing — no error, but no narrowing either. If the filter "doesn't seem to work", the merchant should re-pick both fields fresh.

### Property-option filter joins through the catalog link, not order-time values

The filter joins through the catalog's property-option-to-product link — it filters by which products **currently** have that property / option assigned, NOT by which value a product had at order time. Catalog property changes made AFTER an order was placed ARE reflected in this filter.

### Property-option filter targets catalog properties only

It pivots through the catalog's properties ([[products-property]]). It does NOT filter by product TAGS or by category — those are not exposed as filter types here. For tag-based filtering the merchant uses [[products-products]].

### Date filter scope and basis

A date filter narrows the aggregate to orders placed in the window. The comparison is against the order's `date_added` (creation date), NOT `date_paid` or fulfillment date — documented in full in [[ordered-products-status-scope]]. With no date filter, the pivot runs across the entire order history; large stores should apply a date filter early to keep the query responsive and the totals meaningful.

### No saved filter sets — side effects

Every filter is ad-hoc per session. Filtering changes no state (pure read view). The Export button captures whatever filter scope is currently applied — see [[orders-ordered-products-export]].

## Related

- [[orders-ordered-products]] — hub.
- [[products-property]] — properties + options used in the Property-option filter.
- [[settings-statuses]] — order status taxonomy used in the status filter.
- [[orders-ordered-products-export]] — the export captures the current filter scope.
- [[order]] — entity page.
- [[product]] — entity page.

## Open questions

(None.)
