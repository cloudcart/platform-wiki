---
type: feature
nav_path: "Suppliers → Products by orders → Filters"
route_name: suppliers.products_by_orders
route_path: /admin/suppliers/products-by-orders
aliases: ["Products by orders filters", "Supplier products filters", "Order products filter", "Property option filter", "Order status filter products by orders"]
tags: [orders, products, suppliers, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-supplier-products]]. See the hub for the other aspects (overview, aggregation, Suppliers app, export).

# Products by orders — filters

## Purpose

Documents the filter chrome on the **Products by orders** screen — what filters exist, how the single-active two-tier dropdown works, and the non-obvious behaviours (the two-step Property-option injection, the Pending-status fulfillment constraint, and which date the date filter actually uses). Filtering is the merchant's main lever for scoping the cross-order aggregate described on the hub [[orders-supplier-products]].

## Where to find it

On the **Products by orders** page (route `suppliers.products_by_orders`), the filter chrome sits above the grid. It is a **two-tier dropdown**: a master "filter type" select (Select2-styled), then a context-dependent sub-form that becomes visible based on the selected filter type.

**Only ONE filter can be active at a time** — selecting a new filter type replaces the previous one.

## What the merchant can do here

| Filter | Visible | Sub-form | Notes |
|--------|---------|----------|-------|
| **Supplier** | Only when Suppliers app installed | Single-select dropdown of all configured suppliers | Pick a specific supplier from the configured list, to scope the aggregate to one supplier's products. See the display-only quirk on [[orders-supplier-products-suppliers-app]]. |
| **Order date interval** (`fromToDate`) | Always | Two date+time pickers (`from` / `to`) using the site's date+time format | Filters by `orders.date_added` only — NOT by paid / completed / shipped date. |
| **Order ID interval** (`fromToId`) | Always | Two numeric inputs (`from` / `to`) | Order ID range — useful for "products from orders 1000-2000". |
| **Order status** (`orderStatus`) | Always | Single-select dropdown of all order statuses | Includes both system statuses (pending, paid, completed, etc.) and any custom statuses configured in [[settings-statuses]]. |
| **Property option** (`propertyOption`) | Always | Two-step: first an autocomplete for the property (loads from `admin.autocomplete.category-property`), then a second autocomplete for the option (loads from `admin.autocomplete.category-property-option/{property_id}`) | The second field is INJECTED into the DOM via jQuery when the merchant picks a property. The second field only loads options that exist for the selected property. |

## Settings & fields

The status filter draws its options from the order-status taxonomy — both system statuses and custom statuses defined in [[settings-statuses]]. The Property and Option autocompletes draw from the category-property data managed in [[products-property]]. No filter state is persisted between visits.

## Business rules

### Date filter — by `orders.date_added`, not order processing date

The from-to date filter applies to `orders.date_added` (when the order was placed). It does NOT filter by `date_paid`, `date_fulfilled`, or `date_completed`. So "products in orders this month" means "products PLACED in orders this month" — regardless of when those orders were paid or shipped. For "supplied this month" demand analysis, the merchant should account for orders placed at month-end that paid / shipped the following month.

### "Pending" status filter ADDS an unfulfilled-only constraint

Hidden behavior: when the merchant picks the **Pending** status, the query adds `AND status_fulfillment = "not_fulfilled"` ON TOP of `status = 'pending'`. So Pending = orders that are both `status = pending` AND `not_fulfilled`. A pending order that's already fulfilled (rare but possible) is excluded. Other statuses (paid, completed, refunded, etc.) don't add the fulfillment constraint.

### Property-option filter — second field is dynamically injected

The two-step Property option filter doesn't render both fields at page load. The first input (Property) is rendered upfront; the second input (Option) is a placeholder that the jQuery handler populates with a Select2 ajax input ONLY after the merchant picks a property. So a merchant who picks a property and tries to "go back" sees the option input remain — they must clear the form to reset.

If the merchant submits the form without picking BOTH fields, the filter silently does nothing (the backend rejects mismatched property / option pairs).

### Single active filter

Because the master dropdown replaces the active sub-form when a new filter type is chosen, the merchant cannot combine, e.g., a date range AND a supplier in one query. To narrow on two dimensions the merchant filters on one, exports, and filters again — or uses the most selective single filter.

### Side effects

**None** — filtering only changes which rows the grid loads; it never writes data.

## Related

- [[orders-supplier-products]] — hub.
- [[orders-supplier-products-suppliers-app]] — the Supplier filter and its display-only scoping quirk.
- [[settings-statuses]] — order status taxonomy feeding the status filter.
- [[products-property]] — property + options used in the property-option filter.
- [[orders]] — parent list of orders.

## Open questions

None.
