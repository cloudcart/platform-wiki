---
type: feature
nav_path: "Apps → Advanced Search → Analytics"
route_name: apps.advanced_search.analytics
route_path: /admin/apps/advanced_search/analytics
aliases: ["Advanced Search Analytics", "Popular queries", "No-hits queries", "No results searches", "Search demand"]
tags: [apps, others, search, analytics]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (settings, usage, orders, indexing, support).

# Advanced Search — Analytics

## Purpose

The **Analytics** tab turns raw storefront searches into demand insight: which terms customers search most, and — most actionably — which terms returned **zero** results. A frequent no-hit query is unmet customer demand, signalling a product to add or an SEO / naming gap to close.

## Where to find it

Sidebar → Apps → **Advanced Search** → **Analytics** tab (`apps.advanced_search.analytics`). The no-hits view is the sub-route **Analytics → No-hits** (`apps.advanced_search.analytics.nohits`).

## What the merchant can do here

- **Popular queries** — most-searched terms with their frequency.
- **No-hits queries** (sub-route) — search terms that returned ZERO results. The most actionable view: e.g., customers searching "vegan boots" the store doesn't stock = an opportunity.
- **Set list limits** — Popular-queries limit and No-results-queries limit, each 10–500.
- **Master toggle** — enable / disable analytics tracking entirely.

### What the merchant CANNOT do here

- Query data older than 90 days — events beyond that window are pruned from aggregates (see Business rules).
- See per-customer identity behind a query — analytics is aggregated by term, not by shopper.

## Settings & fields

| Field | Notes |
|-------|-------|
| `analytics.popular_limit` | Integer **10–500**; how many popular queries are shown. Default **100**. |
| `analytics.nohits_limit` | Integer **10–500**; how many no-hits queries are shown. Default **100**. |
| Analytics master toggle | Enable / disable tracking of search analytics events. |

Setting either limit below 10 or above 500 is rejected at save time.

## Business rules

### No-hits is the most actionable view

The No-hits sub-page surfaces demand the merchant ISN'T meeting. Each frequent no-hit query is a candidate product to stock or a naming / synonym gap to close — and since synonyms aren't configurable (see [[apps-advanced-search-settings]]), renaming or re-tagging products is often the fix.

### Retention = 90 days

The retention window for search-analytics events is 90 days. Popular-queries and no-hits aggregations only consider events from the last 90 days; raw events older than that are no longer counted. The Usage tab additionally caps the visible date range at 3 months — see [[apps-advanced-search-usage]] — so older data is effectively invisible to the merchant.

### Storefront vs system searches

Analytics aggregates storefront searches; system / backend "patches" searches are separated out on the Usage tab so they don't pollute demand signal. See [[apps-advanced-search-usage]].

## Related

- [[apps-advanced-search]] — hub.
- [[apps-listing-engine]] — logs the search-analytics events these views aggregate.
- [[products-products]] — products to add in response to no-hit demand.
- [[products-missing-product]] — back-in-stock demand signal (complementary insight).

## Open questions

(None currently outstanding for this page.)
