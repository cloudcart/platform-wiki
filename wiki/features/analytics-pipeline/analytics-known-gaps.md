---
type: feature
nav_path: "Concept → Analytics pipeline → Known gaps"
route_name: ""
route_path: ""
aliases: ["Analytics known gaps", "Analytics limitations", "Analytics currency model", "Analytics retention", "Export limit"]
tags: [analytics, pipeline, limitations, currency, retention]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[analytics-pipeline]]. See the hub for the other aspects (event capture, event processing, aggregation, dashboard reads, backfill commands).

# Analytics — known gaps + by-design limitations

## Purpose

This page collects the **by-design limitations and traps** in the analytics pipeline that produce surprising merchant questions: multi-currency arithmetic, DST "missing hour" charts, the ad-blocker blind spot, 504 hot spots, kill switches, export caps, and retention. Read it when the answer is "the pipeline is working as designed — here's why the number looks wrong".

## Where to find it

Invisible to the merchant — there's no "known gaps" admin screen. These are documentation-only callouts for diagnosing tickets outside the happy paths in [[analytics-event-capture]] / [[analytics-event-processing]] / [[analytics-aggregation]] / [[analytics-dashboard-reads]].

## What the merchant can do here

Nothing directly — these are by-design limits. The merchant can only pick work-arounds:

- Multi-currency stores → chart each currency's site separately, or read the per-order amount on [[order]].
- Ad-blocker blind spot → run [[apps-google-analytics]] in parallel on a different domain.
- 504 timeouts on broad ranges → narrow the date window, or trigger an async CSV export (150 000-row cap).
- Industry-comparison asymmetry → keep the analytics-statuses Settings filter aligned with platform defaults if comparison parity matters.

## Settings & fields

Not applicable — these are limits, not configurable knobs. Ops-side levers (not in the merchant UI) that interact with the gaps:

| Lever | Effect |
|-------|--------|
| `uuid.enabled` | Platform-wide kill switch — when off, all analytics writes stop. |
| `uuid.disabled_sites` | Per-site opt-out — listed stores get an empty dashboard. |
| Platform disable message | When set, the dashboard returns a 400 with the message. |
| `export.limit` (default 150000) | Export row cap. |
| Load-balancer request timeout | Drives the 504 hot spots — typically 60s. |

## Business rules

**Currency — no FX, no multi-currency aggregation.** Every analytics number (`amount`, `subtotal`, `discount_amount`, `shipping_amount`, `tax_amount`, etc.) is stored as the raw value from the order, in the order's own currency at sale time — never converted to a base currency, snapped to an FX rate, or tagged with a currency code. For a single-currency store this is invisible and Total Sales is correct. For a **multi-currency store** (e.g. BGN on the primary site, EUR on a co-site / B2B portal) Total Sales is the arithmetic sum of mixed-currency amounts — **NOT a true cross-currency total**. Chart each currency's store separately, or read individual amounts on [[order]].

**Retention — indefinite, no TTL.**
- Aggregated rollups and per-order analytics are **kept indefinitely** — this is why merchants can chart sales going back years. Per-order records are keyed by `{site_id}-{order_id}`, so re-running the per-order job upserts the same record (idempotent — see [[analytics-event-processing]]).
- Raw events / sessions data is retained by the separate events-ingest service; its TTL / archival policy lives on the ops side, not in CloudCart's own code.
- Deleting a product / category / customer does NOT retroactively delete analytics — they keep the order-time snapshot. Top Products by Sales for a deleted product shows a "deleted product" placeholder.

**Bot / crawler filtering — layered at 3 levels**, so neither external crawlers nor staff previews pollute Total Visits:
1. The tracker script is not emitted on crawler requests (see [[analytics-event-capture]]).
2. No UUID cookie is set for crawlers.
3. At aggregation, UUIDs matching `^admin-.*` are excluded — catches admin-panel previews and merchant-logged-in test sessions (see [[analytics-aggregation]]).

**Ad-blocker / corporate-proxy blind spot.** The storefront tracker posts to a separate analytics hostname, distinct from the storefront and admin. Ad blockers or corporate proxies that block it mean the events **never arrive**, so those visitors don't appear in Total Visits at all. There is no first-party fallback — a structural limit. Work-around: run [[apps-google-analytics]] in parallel on a different domain.

**Industry-comparison asymmetry.** The "above / below average for {industry}" badge uses a **hardcoded status set (Paid, Completed, Pending, Authorized, Fulfilled)** — NOT the merchant's saved analytics-statuses Settings filter (see [[analytics-dashboard-reads]]) — so the comparison stays apples-to-apples across merchants. A merchant who narrows their Settings filter gets a stricter numerator than the benchmark, which can read "below industry" even when nothing has actually deteriorated.

**DST → "off-by-one" hourly charts.** Buckets are rolled up in the store's primary timezone, so bucket "10:00" really is 10:00 local, not 10:00 UTC. On a store in a DST timezone (e.g. `Europe/Sofia`) the spring-forward / fall-back days can show an **apparent missing or doubled hour bucket** — hourly charts on those days look "off by one".

**504 hot spots — broad date ranges + table boxes.** A 504 is the upstream load-balancer timeout (typically 60s; not analytics-specific). "Last 5 years" on a high-volume store may hit it on the heavier **table boxes** (Top Products by Sales, Landing Pages by Sales) before the chart boxes (see [[analytics-dashboard-reads]] for the error model). Work-around: narrow the date window, or trigger an async CSV export.

**Kill switches — platform-wide + per-site**, checked on every job; they suspend writes instantly with no partial / half-aggregated rows:
1. `uuid.enabled` — platform-wide. When off, every analytics job skips (emergency maintenance).
2. `uuid.disabled_sites` — per-site opt-out array (currently `[17987]`). Listed stores have an **empty Analytics Dashboard**.
3. Platform disable message (currently inactive) — when set, all analytics pause AND the dashboard returns the message as a 400.

**Export caps + lock.**
- Cap: **150 000 rows** per report (`export.limit`). Exports run independently of the aggregation tick, so a big export does not stall live dashboard rollups.
- Merchant-facing string: "This report shows up to {total} results. To see all results, you can [export]" (EN) / "Този отчет показва до {total} резултата. Имате възможност да направите експорт до {limit} реда" (BG).
- **CSV only** — no `.xlsx`. The file lands in [[settings-files]] as `.csv`. A compare export (current + previous) produces **two separate files**, not a zip or multi-sheet workbook.
- **One active export per box, per merchant.** A second request for the same box while one is in progress is refused: *"You already have a request for this file. Please wait for it to be generated."* The lock is per-box (Total Sales and Top Products can export together) but not per-mode. It releases when the file is written.

**Parallel pipelines that are NOT this one** — independent systems consuming the same storefront events but never sharing data with the main Analytics Dashboard:
- A separate browser-data collector stores browser / OS / device statistics for the marketing-segments module.
- [[apps-google-analytics]] pushes the same events to GA4 via the merchant's measurement ID, in parallel.
- [[reports-customers]] and the other `/admin/reports/*` siblings (Sales, Products, Payments) are a legacy stack on a different database.

## Related

- [[analytics-pipeline]] — hub (sibling aspects are linked inline above).
- [[order]] — per-order line for true cross-currency reporting.
- [[settings-files]] — where the CSV export lands.
- [[apps-google-analytics]] — parallel GA4 pipeline.
- [[reports-customers]] — legacy reports (separate stack).

## Open questions

- Exact TTL / archival policy on the raw events / sessions data — declared on the ops side, not in CloudCart's own code. `(verify)` with infra if a merchant asks how far back visits can be charted.
