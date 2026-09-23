---
type: feature
nav_path: "Apps → Aura Search → (three different search counts)"
route_name: apps.advanced_search.usage
route_path: /admin/apps/advanced_search/usage
aliases: ["Aura Search usage", "search usage", "why do search numbers differ", "used searches higher than searches", "bot searches", "Storefront Usage", "Backend Operations", "Usage Statistics", "използвани търсения", "защо се различават търсенията", "търсения от ботове"]
tags: [apps, search, usage, billing, analytics]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-09-23
source_count: 5
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, pins, vocabulary, AI, settings, indexing).

# Aura Search — the three counts of "searches"

## Purpose

Aura Search shows a number of searches in more than one place, and the numbers do not match. They are not meant to: each one counts something different, for a different question. This aspect lines them up, and covers the older usage pages that are still reachable by address.

## Where to find it

| Figure | Where |
|---|---|
| **Used** (billed) | **Settings → Plan & usage** ([[apps-advanced-search-plans]]) |
| **Searches** (people) | **Overview** headline card ([[apps-advanced-search-overview]]) |
| **Searches** per term | **Searches** tab ([[apps-advanced-search-analytics]]) |
| Usage by page and operation | `/admin/apps/advanced_search/usage` (older page, by address only) |

## What the merchant can do here

Read each figure for what it counts. None of them is editable.

## Settings & fields

### Side by side

| | **Used** (billed) | **Searches** (Overview) | **Searches** per term |
|---|---|---|---|
| Dropdown under the search box | ✅ | ✅ | ✅ |
| Full `/search` results page | — | — | ✅ |
| Bots and crawlers | ✅ | — | ✅ when they search |
| Needs analytics on | — | — | ✅ |
| Period | Current month | Header date range | Header date range |

### Why they differ

- **Used is the largest for most stores.** It counts every dropdown request, **bots included**, because that is what the plan pays for. The Overview takes the bots out, because a crawler is not a customer.
- **The Searches tab can be larger or smaller than the Overview.** It adds the full results page, which the other two never count. But it only exists for the days analytics was on, and switching analytics off wiped what came before ([[apps-advanced-search-analytics]]).
- **A term's count is not a count of shoppers.** One shopper typing slowly produces several dropdown searches, each recorded separately — and possibly as different partial words.

The Overview's **No results** rate is a share of the per-term figures, not of Used. The two are never compared directly on screen.

## Business rules

### The older Usage page — every page view the engine served

`/admin/apps/advanced_search/usage` predates the redesign and is no longer in the tab bar. The Settings tab lights up when it is open. It shows a **Total** for the chosen range (3 months at most) and two views:

- **Storefront Usage** — every storefront request the search engine answered, by page: *Search*, *Category*, *Vendor*, *Tag*, *Selection*, *Showcase*, *Home Page*, *Product*, the two dropdown kinds (*Advanced Search*, *Advanced AI Semantic Search*) and others. Each is split **Human** / **Bot**.
- **Backend Operations** — index updates the store's own changes caused: *Price Update*, *Quantity Update*, *Image Update*, *Category Assignment*, *Discount Update*, *Sync Variants* and similar.

This page is a **diagnostic of load, not the bill**. Its Total counts category, vendor and home pages, which are never billed. Only the two dropdown rows count toward the plan, and the plan panel is the place to read that figure.

### The older Analytics page

`/admin/apps/advanced_search/analytics` is the pre-redesign term report. It lists **popular** queries and **no-results** queries over the last 90 days, each capped by its own limit (**10–500**, default **100**). It also holds the only **switch to turn analytics off** — which deletes the recorded terms ([[apps-advanced-search-analytics]]).

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-plans]] — what is billed, and what happens when it runs out.
- [[apps-advanced-search-overview]] — the people-only search count.
- [[apps-advanced-search-analytics]] — the per-term counts.
- [[apps-listing-engine]] — the search index behind the Backend Operations list.

## Open questions

(None currently outstanding for this page.)
