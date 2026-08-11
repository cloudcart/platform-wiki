---
type: feature
nav_path: "Apps → Advanced Search → Usage"
route_name: apps.advanced_search.usage
route_path: /admin/apps/advanced_search/usage
aliases: ["Advanced Search Usage", "Search usage", "Storefront vs Patches", "Search statistics charts", "Listing Engine Statistics"]
tags: [apps, others, search, analytics, statistics]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (settings, analytics, orders, indexing, support).

# Advanced Search — Usage & Statistics

## Purpose

The **Usage** tab tracks how much search the store is doing over time, split between real customer searches and system-triggered ones. The sibling **Statistics** tab rolls the same data into aggregated charts. Together they answer "how heavily is search being used, and by whom?" — useful for capacity planning and for understanding what is consuming search resources.

## Where to find it

Sidebar → Apps → **Advanced Search** → **Usage** tab (`apps.advanced_search.usage`), with sub-routes **Usage → Bot** (`apps.advanced_search.usage.bot`) and **Usage → Backend** (`apps.advanced_search.usage.backend`). The **Statistics** tab is a sibling (`apps.advanced_search.statistic`).

## What the merchant can do here

- **Pick a date range** — limited to a MAX 3-month back interval (older data isn't queryable from this UI).
- **Read a Grand Total** counter for the selected period.
- **Switch between two main tabs:**
  - **Storefront** — customer-side searches from the website; sub-tabs may break this down further.
  - **Patches** — backend / system-triggered searches (e.g. admin product picker, API consumers).
- **Read per-tab tables** of counts.
- **On Statistics**: read aggregated charts — Listing Engine Statistics + Search-driven Orders Overview.

### What the merchant CANNOT do here

- Query usage older than 3 months from this UI.
- See the search index operator metrics — query latency (p50 / p95), cache hit rate, or shard health are platform-operator metrics surfaced on [[apps-listing-engine]], not here.

## Settings & fields

| Field | Notes |
|-------|-------|
| Date-range picker | `max-back-interval: 3` — limited to 3 months back. |
| Grand Total | Aggregate count for the selected period. |
| Storefront / Patches tabs | Customer searches vs system/backend searches; Bot and Backend sub-routes break out further. |
| Statistics charts | Listing Engine Statistics + Search-driven Orders Overview. |

## Business rules

### Storefront vs Backend / Patches

The Usage tab distinguishes real customer searches (**Storefront**) from system-triggered ones (**Backend / Patches** — admin product picker, API consumers, indexing patches). The separation matters for capacity planning and for keeping demand analytics (see [[apps-advanced-search-analytics]]) free of system noise. The platform's storefront usage middleware tracks searches per route; counts are grouped by route on this tab. See [[apps-listing-engine]] for the route keys counted and how usage is incremented.

### 3-month cap aligns with retention

The 3-month date cap pairs with the 90-day analytics retention window (see [[apps-advanced-search-analytics]]): events beyond ~90 days are pruned from aggregates, so a longer range would show nothing anyway.

### Search-driven Orders Overview chart

The Statistics tab's Search-driven Orders Overview summarises orders attributed to search; the per-order list lives on the Orders tab — see [[apps-advanced-search-orders]].

## Related

- [[apps-advanced-search]] — hub.
- [[apps-listing-engine]] — usage counts and route keys originate here.
- [[apps-advanced-search-analytics]] — demand insight from storefront searches.
- [[apps-advanced-search-orders]] — the per-order search-attribution list behind the Statistics chart.

## Open questions

(None currently outstanding for this page.)
