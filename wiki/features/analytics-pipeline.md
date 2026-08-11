---
type: feature
nav_path: "Analytics → Data pipeline"
route_name: ""
route_path: ""
aliases: ["Analytics pipeline", "Data ingest", "Tracking pipeline", "CcAnalytics", "Analytics data pipeline"]
tags: [analytics, ccanalytics, pipeline, data-ingest, the analytics store]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 15
---

# Analytics data pipeline (end-to-end)

## Purpose

This page is the **hub** for the storefront-event-to-dashboard-chart data pipeline that powers the [[analytics]] dashboard. It explains the high-level shape (five layers, fast lane vs slow lane, ~1–2 minutes vs up to 1 hour) and lists the aspect sub-pages that drill into each stage. It answers the merchant questions *"why doesn't my new order show up in Total Sales yet?"* and *"why does Total Visits jump 30 minutes after I refreshed?"*.

The CloudCart analytics stack is **NOT a real-time stream**. It is a **periodic batch aggregation pipeline** that ticks **once per hour** (`EXECUTION_TIME_IN_HOURS = 1`). Every hourly tick, queued jobs grind through ~13 aggregations and write rolled-up documents into the `analytics.*` collections. The dashboard reads these pre-aggregated documents — **no live query against raw events** runs at dashboard load.

This is why a brand-new order placed at 14:35 typically appears in **Total Orders** within ~1–2 minutes (per-order fast lane with a 60-second initial delay), but may take **up to one full hour** to show in **Total Visits / Conversion Rate / Top Products by Traffic** (those wait for the next hourly aggregation tick).

## Where to find it

This is a **concept page**, not a screen — there is no route or sidebar entry. The pipeline is invisible to the merchant by design: it runs in the background and surfaces only as the chart data on the [[analytics]] dashboard and (for the customers report) on [[reports-customers]].

The pages that READ from this pipeline are [[analytics]] (hub), the drill-ins [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]], and the per-box pages [[analytics-total-sales]] / [[analytics-total-orders]] / [[analytics-abandoned-carts]] / [[analytics-abandoned-checkout]] / [[analytics-cart-conversion-funnel]] / [[analytics-cart-conversion-rate]] / [[analytics-orders-by-social-source]] / [[analytics-sales-by-traffic-source]] / [[analytics-top-brands-by-sales]] / [[analytics-top-bundles-by-traffic]] / [[analytics-top-categories-by-sales]] / [[analytics-top-order-products-by-sales]] / [[analytics-top-products-by-traffic]].

The pages that do NOT use this pipeline (despite looking similar): [[reports-customers]] and the other `/admin/reports/*` siblings (Sales, Products, Payments) — those query the store database directly via the legacy reports stack.

## Sub-pages (in this cluster)

This pipeline is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[analytics-event-capture]] — the storefront tracker (`window.CCE`) and the route-to-event-type map (Layer 1).
- [[analytics-event-processing]] — raw event storage and the per-order fast lane on the `analytics2` queue with 5–60 second delays (Layers 2 + 3).
- [[analytics-aggregation]] — the hourly slow-lane tick (runs HH:01 UTC), the 13 parallel fan-out jobs on the `analytics` queue, and the weekly industry-statistic job (Layer 4).
- [[analytics-dashboard-reads]] — the `/admin/api/analytics/dashboard/{box}` read API, the per-box formatters, the dashboard Settings panel (statuses / industry / show-devices / box sort), and the canonical refresh-latency table (Layer 5).
- [[analytics-known-gaps]] — by-design limits: no multi-currency aggregation, indefinite retention, the ad-blocker blind spot, DST hour-bucket drift, 504 hot spots, kill switches, export caps.

## What the merchant can do here

Nothing directly — this is the **data plumbing** behind the dashboards. The merchant's actions that flow THROUGH this pipeline:

- Place an order → flows in as a `purchase` event and a per-order job; appears in Total Sales within ~1–2 minutes (see [[analytics-event-processing]]).
- Visit a storefront page as an anonymous shopper → tracked event; appears in Total Visits within up to 1 hour (see [[analytics-event-capture]] + [[analytics-aggregation]]).
- Configure which order statuses count as "revenue" via the analytics-statuses setting on [[settings-cart]] → applied at query time by each box (see [[analytics-dashboard-reads]]).
- Configure visible boxes and their sort order on the [[analytics]] settings panel → stored in the `cc_analytics` config cache.
- Set date range, comparison mode, and time-bucket group on any box → driven through `/admin/api/analytics/dashboard/{box}`.
- Export a report (CSV) → queues the export job; merchant gets an admin alert with the file URL on completion (150 000-row cap — see [[analytics-known-gaps]]).

## Business rules — the five layers at a glance

| Layer | What it stores | Write trigger | Read by | Aspect page |
|-------|----------------|---------------|---------|-------------|
| 1. **Storefront tracker** (JS) | Per-page events from the visitor's browser | Every page view, click, addToCart, beginCheckout, purchase | The external analytics ingest endpoint | [[analytics-event-capture]] |
| 2. **Raw events** | One record per tracked browser event | The ingest service stores each posted event | The hourly aggregation jobs | [[analytics-event-processing]] |
| 3. **Per-order records** | One record per platform order, denormalised | Order-created / status-change events trigger a per-order job (60s initial delay; 5s on edits) | Order-driven boxes (Total Sales, Top Products by Sales, etc.) | [[analytics-event-processing]] |
| 4. **Aggregated rollups** | Time-bucketed rollups (per hour / day) grouped by site / device / country / referrer | Hourly tick → 13 parallel per-area jobs on the `analytics` queue | Dashboard chart boxes (Total Visits, Cart Conversion Rate, etc.) | [[analytics-aggregation]] |
| 5. **Dashboard read layer** | Nothing — pure query layer | On demand when the merchant opens the dashboard or changes the date range | The browser — `/admin/api/analytics/dashboard/{box}` | [[analytics-dashboard-reads]] |

Two axes worth distinguishing: **event source** — orders come from the store database, while all other events (visits, page views, addToCart, checkout-started) come from the browser tracker; and **refresh cadence** — order events are processed per-event with a 5–60 second delay, browser events per-hour in batch.

## Settings & fields

Not applicable — this is the pipeline concept, not a settings screen. The configurations that influence the pipeline live on these screens:

| Setting source | Field | Effect on pipeline |
|----------------|-------|--------------------|
| [[settings-cart]] | Analytics statuses (Paid, Completed, Pending, Authorized payment, Fulfilled) | Filter at query time in every revenue-style box |
| [[analytics]] (settings panel) | Visible boxes + box sort order | Stored in `cc_analytics` cache config — see [[analytics-dashboard-reads]] |
| [[analytics]] (settings panel) | Show devices toggle | Toggles device-grouped chart rendering |
| Ops config (not UI) | `disabled_sites` array | Per-site opt-out — the pipeline short-circuits for those sites (see [[analytics-known-gaps]]) |
| Ops config (not UI) | `export.limit = 150000` | Max rows per export report; a platform-wide kill switch also lives here |

## How it interacts with features

- **[[analytics]]** — the dashboard hub that reads from the aggregations; each per-box page (listed under *Where to find it*) and the drill-ins [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]] consume the pre-aggregated collections.
- **[[reports-customers]]** — the Customers report queries the store database directly, NOT this pipeline. Same for the other `/admin/reports/*` siblings (Sales, Products, Payments).
- **[[settings-cart]]** — analytics-statuses setting controls which order statuses count in revenue-style boxes.
- **[[apps-google-analytics]]** — pushes to GA4 in parallel; the two systems do not share data.
- **[[settings-hooks]]** — webhooks fire on the same platform events that drive Layer 3 here.

## Related

- [[analytics]] — dashboard hub.
- Aspects of this cluster (see *Sub-pages* above): [[analytics-event-capture]], [[analytics-event-processing]], [[analytics-aggregation]], [[analytics-dashboard-reads]], [[analytics-known-gaps]].
- [[reports-customers]] — separate legacy reports area.
- [[notification-delivery]] — same platform event bus.
- [[settings-hooks]] — outbound webhooks on the same event stream.
- [[settings-cart]] — analytics-statuses setting.
- [[apps-google-analytics]] — parallel GA4 push.
- [[order-status-workflow]] — status transitions feed the per-order job chain.
- [[subscriber-vs-customer]] — UUID-to-subscriber binding.
- [[cart-vs-order-lifecycle]] — what gets tracked at each stage.
- [[plan-gates]] — analytics access by plan tier `(verify)`.

## Open questions

None.
