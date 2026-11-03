---
type: feature
nav_path: "Concept → Analytics pipeline → Dashboard reads"
route_name: ""
route_path: /admin/api/analytics/dashboard/{box}
aliases: ["Analytics dashboard reads", "Dashboard API", "Per-box formatter", "Analytics settings panel", "Refresh latency", "Box latency table"]
tags: [analytics, pipeline, dashboard, api]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[analytics-pipeline]]. See the hub for the other aspects (event capture, event processing, aggregation, known gaps, backfill commands).

# Analytics — dashboard reads (Layer 5 — API + settings panel + latency)

## Purpose

This page covers the **read side** of the analytics pipeline: how opening [[analytics]] pulls the pre-aggregated data, the Settings panel that controls global dashboard state, and the question this pipeline exists to answer — *"when does my data appear?"*

## Where to find it

The dashboard itself is at [[analytics]] (`/admin/analytics`). The read API is grouped under the `api/analytics` prefix and gated by the `reports` / `reports.analytics` permission. Each box on the dashboard fires its own request:

```
GET /admin/api/analytics/dashboard/{box}?dateFrom=...&dateTo=...&compare=no|period|year&group=auto|hourly|daily|weekly|monthly|yearly
```

The Settings panel opens from a gear icon labelled **Settings** at the top-right.

## What the merchant can do here

- Open [[analytics]] → each box fires its own `GET /admin/api/analytics/dashboard/{box}` and renders the pre-aggregated data.
- Change the date range / comparison mode / time-bucket group on any box → triggers a new request for that box only.
- Open the Settings panel (gear icon) and adjust which order statuses count, the primary industry, the device split, and box sort / visibility (full detail in Settings & fields below).
- Export a box → asynchronous report-export; the merchant gets an admin alert with the file URL on completion.

## Settings & fields

The Settings panel is a right-sliding modal (gear icon) controlling global state shared by every box.

| Setting | What it controls | Default / notes |
|---|---|---|
| **Section 1 — Order statuses included** | Multi-tag select of order statuses. Applied **at query time** by every revenue-style box; changing it instantly changes those boxes on next refresh. | **Paid, Completed, Pending, Authorized payment, Fulfilled.** Does NOT affect visit / cart event boxes or industry-comparison badges (see Business rules). |
| **Section 2 — Primary industry** | Single-select industry dropdown (e.g. Fashion, Electronics). Drives the industry-compare badge on `hasIndustryCompare` boxes. | Recompute lag **up to 1 week** (helper text: *"If the main industry changes, the data will be updated at the beginning of each week."*). Mirrored on [[settings-general]] (`site.main_industry`) — editing it here updates that field too. |
| **Section 3 — Show devices toggle** | ON: every box with a device split (mobile vs desktop badges, per-row tooltips, cart/funnel custom rows) shows it. OFF: those visuals are suppressed dashboard-wide. | Default **ON**. |
| **Section 4 — Show boxes sort toggle** | Reveals a drag-and-drop tree of every box; each row has a title, visibility toggle, and drag handle. Order stored in `analyticsSettings.defaultBoxesSorting`, persisted on Save. | Drag constraints — see Business rules. |
| (read-only) `cacheHash` | Busts the browser-side response cache on Settings Save. | — |
| **Save** | `POST /admin/api/analytics/settings`; modal closes, dashboard re-fetches with a new `cacheHash`. | Requires `reports.analytics_settings`. |
| **Cancel** | Reverts edits to the last-saved snapshot (`analyticsSettingsOriginal`). No request sent. | — |
| **Reset to default** | `DELETE /admin/api/analytics/settings`. Restores statuses, industry, show-devices, and box sort/visibility to defaults. | Requires `reports.analytics_settings`. |

Dashboard alert above Section 1: "Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled" (BG: "Данните се визуализират според статусите по подразбиране в Настройки и не могат да бъдат променени → Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена").

## Business rules

- Each box loads **independently** — a 504 or error on one box leaves the others working.
- **Permissions**: reading the dashboard and Settings requires `reports.analytics`; Save / Reset require `reports.analytics_settings`. Staff without the write permission can open the modal but get **403** on Save / Reset.
- **"Order statuses included" scope**: affects revenue-style boxes (Total Sales, Customer Value, Sales by Location, Sales by Traffic Source). It does NOT affect visit / cart event boxes (Total Visits, Abandoned Carts/Checkouts, Visits by Traffic Source) — those are driven by storefront events, not orders.
- The **industry-comparison badge** uses a HARDCODED status set (Paid + Completed + Pending+not_fulfilled + Authorized + Fulfilled), regardless of what the merchant picks in Section 1. Narrowing the Section 1 selection can put the merchant's number "below industry" without any real deterioration — see [[analytics-known-gaps]] for the comparison-asymmetry detail.
- **Box-sort constraints**: boxes reorder only within the same `type` group (`chart`, `table`, `bar`, `funnel`) — a chart box cannot move into the table section. Child boxes can ONLY live as children, never top-level; first-level cards with children render a `<select>` dropdown in their title to pick which child renders in the slot.
- **No cache layer** sits between the API and storage — every request reads the pre-aggregated data directly. That pre-rolled-up data IS the cache (see [[analytics-aggregation]]).

## The per-box formatter

Each request resolves to a per-box formatter. It parses the date range; auto-picks the time-bucket group when `group=auto` (short ranges → `hourly`, day-week → `daily`, longer → `weekly` / `monthly` / `yearly`); reads the pre-aggregated data filtered by store + date range + the "Order statuses included" setting; and returns the JSON the chart consumes.

## Refresh latency reference (the merchant question)

Verified numbers, grouped by the two lanes (fast = [[analytics-event-processing]], slow = hourly [[analytics-aggregation]]):

**~1–2 minutes** (order-driven, fast lane):

- **Total Sales**, **Total Orders** (full count consistent within ~1 hour), **Total Customers / New / Returning**, **Top Categories / Top Brands by Sales**, **Orders by Social Source**.
- **Top Products by Sales** — line-level in ~1–2 min; per-bucket aggregates up to 1 hour.
- Sale side of split boxes: **Sales by Traffic Source**, **Orders by Country**, **Landing Pages by Sales / by Traffic**.

**Up to 1 hour** (hourly rollup; the in-flight hour is NOT included until it closes):

- **Total Visits**, **Cart Conversion Rate / Conversion Funnel**, **Abandoned Carts / Abandoned Checkouts**, **Top Products by Traffic**, **Top Categories / Top Brands by Traffic**, **Sessions by Device**, **Sessions by Country**, plus the sessions/traffic side of the split boxes above.

**Up to 1 week**: **Industry comparison** ("above/below average for {industry}") — weekly recompute (Monday 02:05 UTC).

**CSV export of any report**: asynchronous; merchant gets an admin alert with the download URL. Limit **150 000 rows** per report (`export.limit`) — see [[analytics-known-gaps]].

## 504 timeout — broad date ranges

If a date range is so broad that the query times out, the API returns **HTTP 504** with: *"We cannot generate statistics for the selected period, please reduce it."* (EN) / *"Не може да генерираме статистика за избрания период, моля намалете го."* (BG). Only the affected box shows the error; neighbours are unaffected since each loads independently.

The 504 threshold is the upstream load-balancer's timeout (NOT an analytics-specific config) — typically 60 seconds in production. See [[analytics-known-gaps]] for the hot spots (Top Products by Sales, Landing Pages by Sales on multi-year ranges).

## Related

- [[analytics-pipeline]] — hub.
- [[analytics]] — the dashboard the read API powers.
- [[analytics-event-processing]] — fast lane (~1–2 min boxes).
- [[analytics-aggregation]] — slow lane ("up to 1 hour" boxes).
- [[analytics-known-gaps]] — currency model, 504 hot spots, retention, comparison asymmetry.
- [[settings-cart]] — the analytics-statuses setting; same field as the panel's Section 1.
- [[settings-general]] — `site.main_industry`; mirrored in the panel.
- [[reports-customers]] — legacy Smarty reports, separate stack.

## Open questions

None.
