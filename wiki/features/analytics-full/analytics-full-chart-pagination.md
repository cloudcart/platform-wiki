---
type: feature
nav_path: "Analytics → Full → Chart, pagination & limits"
route_name: analytics.viewMore
route_path: /admin/analytics/full/:box/:record
aliases: ["View more chart", "Full list pagination", "Force limit", "DETAILS_FORCE_LIMIT", "Per-row chart", "Inline time-series", "Пагинация на пълния списък"]
tags: [ccanalytics, analytics, full, view-more, chart, pagination, force-limit]
plan_gates: ["cc_analytics.allow_period_compare", "cc_analytics.compare_range"]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Full — chart, pagination & limits

> Part of [[analytics-full]]. See the hub for the drill model and the other aspects (available boxes, CSV export).

## Purpose

This aspect covers the on-screen mechanics of the View more full list: the inline per-row time-series chart above the table, the Compare and Group controls as they behave here, server-side pagination, and the per-box force-limit that caps both the table and the chart. It also documents the shared kill switches, timezone, and timeout behaviour.

## Where to find it

The full list screen at `/admin/analytics/full/:box/:record`. The chart (if any) sits above the table; the Compare / Group pickers and date-range picker sit at the top; the pagination control sits in the table footer.

## What the merchant can do here

- See the **full paginated table** of all rows in this box for the date range (instead of just the top 5 the dashboard showed).
- See an **inline per-row time-series chart** above the table when the box enables it.
- **Change the date range**, **Compare mode**, and **time grouping** — all refresh chart and table.
- **Paginate** through the result set, 100 rows per page.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Date range | Two dates (from/to). | Standard global default (last 30 days). | Max look-back is `cc_analytics.compare_range` plan feature. |
| Compare | `no` / `period` / `year`. | `no` (or URL query). | Gated by `cc_analytics.allow_period_compare`. Box config can override visibility via `details.viewMore.compare` (default `true`). |
| Group | `hourly` / `daily` / `weekly` / `monthly` / `quarterly` / `year` / `none`. | `hourly` (or URL query). | Re-filtered by date range (no Hourly above 7 days; no Daily above 90 days). Box config can override visibility via `details.viewMore.group` (default `true`). |
| Page | Pagination index. | 1 | 100 rows per page (the platform code); enforced server-side. |

## Business rules

### Inline chart (top of page)

When `hasViewMoreChart: true` is set on the box config, the View more screen adds a per-record time-series line chart above the table. This is what makes the screen different from [[analytics-details]]: instead of one aggregate line for the metric, it's several lines (one per row in the table), letting the merchant compare trends across products / brands / categories / etc. The chart is hidden when `group = none` (since "no grouping" means no time axis to chart against).

### Compare on View more

The Compare control behaves the same as in [[analytics-details]] but reads its visibility from `details.viewMore.compare` (default `true`). When set, the table shows side-by-side current/previous columns and the chart overlays both periods. Same plan-gating (`cc_analytics.allow_period_compare`). The Compare parameter is server-validated against the closed list `no` / `period` / `year` — any other value returns HTTP 404 and the screen shows no data (tampering with `?compare=quarter` will silently 404 the API call).

### Group on View more

Same as [[analytics-details]] — but the visibility is `details.viewMore.group` (default `true`). The grouping selector re-filters its own options as the range changes.

### Pagination

100 rows per page is enforced server-side via the platform code. The footer shows the standard pagination control; current page is in the URL `?page=N` for `N > 1`. Changing date range / compare / group resets to page 1.

### `pagination-search` is hidden by design

The component injects custom CSS `.pagination-search { display: none; }` — the standard search-within-pagination input is intentionally not shown here (the dataset is too big for client-side search to be useful; the merchant should export and search offline if needed).

### Force-limit is a per-box capability, not platform-wide

the platform code rows is enforced **per box pipeline** — not globally. The boxes that ship with it active in their `viewMore` query today are:

- Landing pages by sales / by visits
- Top categories by sales (via Products join)
- Top bundles by traffic
- Top products by traffic

For boxes WITHOUT the force-limit (most order-driven boxes — Total Sales, Top Products by Sales, Vendors by Sales, etc.) the full row count is returned and the yellow alert never appears. For boxes WITH the force-limit, a yellow alert shows above the data: *"This report shows up to {total} results. To see all results, you can [Export]"*. The merchant sees a count like "5 642 results — but we're showing 1 000; export to get the rest" and the export goes through the standard 150 000-row cap (see [[analytics-full-csv-export]]).

### Force-limit caps the chart payload too

When the box hits the `DETAILS_FORCE_LIMIT` cap, the per-row chart series shown above the table is also computed from only the first 1 000 records (slice). So the inline chart on View more under the cap shows trend lines for the top 1 000 records, not the merchant's true universe.

### Same kill switches and timezone behaviour

The View more screen inherits all the kill switches of the dashboard (`disabled.cca` shell gate, `uuid.disableInSiteCp` API message, `uuid.disabled_sites` empty-data). The date-range parser uses the store's primary timezone, same as the other Analytics screens. Amounts displayed are raw integer values in the order's own currency — no FX conversion (see the pipeline page for the multi-currency caveat).

### Date interval and 504 mapping

Same as the rest of the Analytics drill-ins: the front-end maps HTTP 504 from the API to *"We cannot generate statistics for the selected period, please reduce it."* Only the affected box shows this; ranging back too far on a high-volume store's view more typically pushes you over the LB timeout (~60s) before the chart timeout.

### Device columns show "N/A" before 17 Jan 2023

Same boundary as [[analytics-details]]: if the period starts before **17 Jan 2023**, every device cell in the table is "N/A" because the storefront tracker didn't record the device attribute on events prior to that date.

## Related

- [[analytics-full]] — hub.
- [[analytics-details]] — the per-metric drill-in; Compare / Group / device behaviour matches it.
- [[analytics-full-csv-export]] — the export path the force-limit alert points the merchant to.
- [[plan-gates]] — `cc_analytics.allow_period_compare` and `compare_range` gates.
- [[settings-statuses]] — the status filter that limits which orders count.

## Open questions

_None._
