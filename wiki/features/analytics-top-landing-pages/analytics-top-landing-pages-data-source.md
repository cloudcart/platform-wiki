---
type: feature
nav_path: "Analytics → Landing pages by visits"
route_name: analytics
route_path: /admin/analytics
aliases: ["Landing pages by visits data source", "Landing pages attribution model", "What counts as a landing-page view", "Homepage page_id zero", "Целеви страници — източник на данни"]
tags: [analytics, ccanalytics, landing-pages, traffic, top-landing-pages]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---

> Part of [[analytics-top-landing-pages]]. See the hub for the other aspects (UI surface, export + cache).

# Landing pages by visits — data source & attribution

## Purpose

Explains what a "view" means in the **Landing pages by visits** box, where the numbers come from, and how repeat views are de-duplicated. This is the page to read when a merchant asks "why does this count look low/high?" or "does refreshing the page inflate the number?" The UI surface is in [[analytics-top-landing-pages-ui]]; the export flow is in [[analytics-top-landing-pages-export]].

## Where to find it

The data behind the **Landing pages by visits** box (Analytics dashboard, `navigationSort: 16.1`) is aggregated server-side; there is no merchant screen for the raw events. The merchant only sees the resulting dashboard top-5, Details table, and ViewMore chart described in [[analytics-top-landing-pages-ui]].

## What the merchant can do here

- Understand why a number is what it is (per-UUID-per-hour-per-device counting).
- Know that their own admin previews do not inflate traffic.
- Know that renaming a content page preserves its history, while re-creating it starts fresh.
- Filter Details to a single page id (or `[0]` for homepage only) — the filter behaviour is documented below.

## Settings & fields

### Metric definition — what counts as a "view"

A "view" is **one `viewPage` or `homePageView` event** as ingested by the visitor tracking pipeline (the `landingPagesPerDay.json` aggregation). Multiple page refreshes within the same hour by the same visitor on the same device count as **one** view. The homepage uses a distinct event name (`homePageView`); content pages use `viewPage`; the pipeline merges both into the same `analytics.landing_pages` collection.

The Details `views` column is labelled "Views / Sessions" because the number is neither strictly unique-visitors nor strictly raw page-views — it is per-UUID-per-hour-per-device counts summed across the period.

### Data source — `analytics.landing_pages` collection

The backend aggregates from the `analytics.landing_pages` collection on the `the analytics store-analytics` connection, hinted with `idx_dashboard`. Documents are written by the hourly landing-pages aggregation (rolling 1-hour interval). Each document represents one (`page_id`, `hour`, `device`) bucket. The `device` field is `mobile` or `desktop` (fallback `desktop`) and feeds the per-row mobile/desktop split tooltip.

### Filter narrowing — `ids` parameter

When filtered by specific page ids, the `ids` list is passed through to a `page_id in [ids]` filter. Otherwise the match is `page_id != null`. Passing `[0]` returns only the homepage row.

## Business rules

### Homepage is page_id = 0

The ingest pipeline maps `event = "homePageView"` → `page_id = 0` and `event = "viewPage"` → `page_id = external_id` (the content page id). The **homepage is always page-id zero** in the collection.

The Dashboard aggregation has a special case: in the `$addFields` stage, if `id > 0` the row keeps its `name` and `url` from the page record; if `id == 0`, it overrides `name = "Home page"` and `url = site->getSiteUrl('primary')`. So the homepage row always shows as **"Home page"** regardless of any stored page name, and each store sees its own primary domain. The Dashboard sets `viewMore = $id` directly (no `> 0` guard), so the homepage row (id 0) also has a non-null `viewMore = 0` and is drillable — useful for spotting homepage redesign impact or promotional traffic spikes.

### Attribution model — UUID × hour × device de-duplication

The `landingPagesPerDay` ingest job performs a two-stage `$group`:

1. Matches raw `events` with `event ∈ {homePageView, viewPage}` within the job's hour window, excluding `uuid_id` matching `/^admin-.*/i` (admin previews never inflate this box).
2. First `$group` by `(uuid_id, stringDate-hour, external_id, device)` — collapses repeat views by the same visitor on the same page within the same hour-bucket on the same device into one `totalForUuidInDate`.
3. Second `$group` by `(stringDate-hour, page_id, device)` — sums all per-UUID hourly counts into `total`, and counts distinct UUIDs into `unique`. `page_id` becomes `0` for homepage events.

The box reads `total`. A visitor refreshing the homepage 50 times in an hour from one device → 1 unique, 1 total. Coming back the next hour adds another 1+1. Tabs / re-opening the same page within the same hour-bucket all collapse to 1.

### Same-day vs cross-day visitor caveat

Because the dedup is keyed on `stringDate = "Y-m-d-H"` (one bucket per hour), a visitor who returns at a later hour the same day counts as a new view. This is why the column is labelled "Views / Sessions".

### What is NOT in this box

"Landing page" here means: homepage OR a custom Content Page. The naming is slightly misleading — the box does not show "the first page a visitor landed on in a session" (that is an entry-page concept); it shows "views of the platform's Content Pages collection". Product (`viewProduct`), category (`viewCategory`), brand (`viewVendor`), and checkout-flow page views are covered by the sibling boxes — see Related.

### `viewPage` external_id source

Content pages emit `viewPage` events with an `external_id` supplied by the storefront's analytics view-creator (matched on the `page` route). The page id is whatever the merchant's CMS assigned to that Content Page record — NOT the URL slug. A renamed content page keeps its `page_id`, so its history stays intact; a re-created page gets a fresh id and starts fresh.

### Drill-down levels (verified against backend)

| Level | Returns |
|-------|---------|
| Dashboard | Top 5 pages (`TABLE_RECORDS_LIMIT`) |
| Details | Full paginated table (page size 100) of all viewed pages in period |
| ViewMore | Per-date series for one page id |
| Details export | Unpaginated CSV export |
| ViewMore export | Unpaginated CSV export |

ViewMore intervals are pre-generated date buckets, capped at `DETAILS_FORCE_LIMIT = 1000`.

### Pipeline shape

The 6-stage Dashboard pipeline: `$match` (site_id + date window + page id filter) → `$group` by `page_id` (sums `total` into `aggregate`, picks last `page_name` / `page_url` / `device`, splits mobile vs desktop) → `$sort` (`aggregate` DESC) → `$limit` (top 5) → `$addFields` (homepage overrides + `device` object + `viewMore = page_id`) → `$project` (drops `_id`). Run with `allowDiskUse: true`, `hint: 'idx_dashboard'`. Details is the same pipeline without the `$limit` stage; the details-count query runs a two-stage group for the distinct page count. ViewMore groups the same collection by date bucket sized by the period picker and zip-joins the result to the pre-generated intervals so empty periods render as zero-rows.

### Tenant scoping & overrides

All queries are tenant-scoped (`site_id` + date window). This box has no per-merchant or per-store overrides: same hour-uuid-device deduplication, same admin-uuid exclusion, same homepage-id-zero convention, same `idx_dashboard` hint across every store. Only the homepage URL differs per store (each sees its own primary domain).

## Related

- [[analytics-top-landing-pages]] — hub.
- [[analytics-top-landing-pages-ui]] — the dashboard / Details / ViewMore surface that renders this data.
- [[analytics-top-landing-pages-export]] — CSV export of this data.
- [[analytics-landing-pages-by-sales]] — sister box; same page dimension ranked by revenue (different collection).
- [[analytics-top-products-by-traffic]] — same logic at the product level (`viewProduct`).
- [[analytics-top-categories-by-traffic]] — same logic at the category level (`viewCategory`).
- [[analytics-top-brands-by-traffic]] — same logic at the vendor level (`viewVendor`).
- [[analytics-cart-conversion-funnel]] — checkout-flow page metrics (separate from this box).
- [[analytics]] — parent hub.

## Open questions

_None._
