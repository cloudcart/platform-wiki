---
type: feature
nav_path: "Apps → Advanced Search → Orders"
route_name: apps.advanced_search.orders
route_path: /admin/apps/advanced_search/orders
aliases: ["Advanced Search Orders", "Search-driven orders", "Search to order attribution", "Orders from search"]
tags: [apps, others, search, orders, analytics]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (settings, analytics, usage, indexing, support).

# Advanced Search — Orders

## Purpose

The **Orders** tab lists orders that originated from a storefront search query. It answers "which searches actually convert into sales?" — letting the merchant connect search demand (popular / no-hit queries) to revenue and prioritise accordingly.

## Where to find it

Sidebar → Apps → **Advanced Search** → **Orders** tab (`apps.advanced_search.orders`).

## What the merchant can do here

- **See a cross-order listing** of orders that originated from a search query.
- **Filter** with the standard order filter set.
- **Cross-reference** with the Search-driven Orders Overview chart on the Statistics tab — see [[apps-advanced-search-usage]].

### What the merchant CANNOT do here

- Attribute an order whose search context was lost before checkout — attribution is session-based and expires with the session (see Business rules).
- See attribution for orders placed before Advanced Search was installed / tracking began.

## Settings & fields

| Field | Notes |
|-------|-------|
| Order filter set | Standard cross-order filters (status, date, etc.). |
| `advanced_search_term` (order meta) | The search term that led to the order; the tab queries orders that carry this meta. |
| `advanced_search_at` (order meta) | Timestamp of the originating search. |

## Business rules

### Attribution is session-based via order meta

When the customer runs a search, the platform stores `advanced_search.term` and `advanced_search.at` (timestamp) in the customer's **session**. On checkout, the order populator reads those values and persists them as order meta (`advanced_search_term`, `advanced_search_at`). The Orders tab then queries orders that carry an `advanced_search_term` meta entry.

Consequences for the merchant:

- The search context **survives across page navigations** within the same session, so a customer who searches, browses several products, then checks out is still attributed.
- The context is **lost when the session expires** (or if the customer never searched). Such orders simply don't appear on this tab — they are not mis-attributed, just unattributed.
- Only the **most recent** search context per session is what gets persisted at checkout, so a customer who searches twice is attributed to their last search, not their first.

This is attribution for *insight*, not billing — it does not change the order total, commission, or any pricing. It exists purely so the merchant can read which search terms convert and feed that back into stocking and naming decisions (paired with the demand views on [[apps-advanced-search-analytics]]).

## Related

- [[apps-advanced-search]] — hub.
- [[orders]] — the order list this tab filters.
- [[orders-details]] — where order meta such as the search term is recorded.
- [[apps-advanced-search-usage]] — Statistics tab's Search-driven Orders Overview chart.
- [[apps-advanced-search-analytics]] — the demand side (which queries are run).

## Open questions

(None currently outstanding for this page.)
