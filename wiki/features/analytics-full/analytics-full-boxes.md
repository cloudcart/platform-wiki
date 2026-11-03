---
type: feature
nav_path: "Analytics → Full → Available boxes"
route_name: analytics.viewMore
route_path: /admin/analytics/full/:box/:record
aliases: ["View more boxes", "Full list eligible boxes", "viewMore boxes", "Breadcrumb building", "Кои таблици имат пълен изглед"]
tags: [ccanalytics, analytics, full, view-more, boxes, breadcrumb]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Full — available boxes

> Part of [[analytics-full]]. See the hub for the drill model and the other aspects (chart & pagination, CSV export).

## Purpose

This aspect answers "**which** dashboard cards have a View more full list, and **how** the breadcrumb that gets you back is built". It covers the eligibility rule (`viewMore: true`), the special string-valued `viewMore` redirect, the per-box sort order, and the dynamic breadcrumb construction.

## Where to find it

The **View more** link appears in the footer of an eligible dashboard table card, or as a per-row "View more" column action inside [[analytics-details]]. Both route to `/admin/analytics/full/:box/:record`. The breadcrumb at the top of the resulting screen is the way back.

## What the merchant can do here

- Reach the full list **only** from boxes that ship with View more enabled — clicking is a no-op (no link) on chart-only cards.
- Use the **breadcrumb** at the top to step back to the dashboard or to the [[analytics-details]] drill-in.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| Breadcrumb | Clickable navigation back to dashboard / Details. | `Analytics → {box title}` | Built dynamically from box labels + backend `titleValue`. |
| (box `viewMore` flag) | Decides whether the card even has a View more link. | varies per box | Boxes without it are unreachable here (router 404). |

## Business rules

### Boxes available here

Only boxes with `viewMore: true` in their config can be reached at this URL. If the merchant navigates to `/admin/analytics/full/<box-without-viewMore>/...` the router's `beforeEnter` guard rejects them to `/admin/error-404`. Across the 31 dashboard boxes, the ones eligible are:

| Group | Eligible boxes |
|-------|---------------|
| **Products** | Top Products by units sold, Top Products by sales, Top Products by traffic, Top Bundles by sales, Top Bundles by traffic |
| **Brands** | Vendors by sales, Vendors by traffic |
| **Categories** | Categories by sales, Categories by traffic |
| **Landing pages** | Landing pages by sales, Landing pages by visits |
| **Geography** | Sales by location, Visits by location (the latter ships with `viewMore: true` commented out — currently not reachable) |
| **Sources** | Sales by traffic source (referral), Visits by traffic source (referral), Sales by Source / Medium, Traffic by Source / Medium |
| **Discounts** | Order discounts, Product discounts |
| **Charts** | Total Sales — uniquely sets `viewMore: 'top-order-products-by-units-sold'` (a STRING, not boolean) — clicking View more on the Total Sales chart jumps the merchant to the View more list for top-products-by-units-sold instead. |

Chart-only boxes (Total Orders, Total Customers, Total Visits, Conversion Rate, Customer Value, Average Order Value, Abandoned carts, Abandoned checkouts) do NOT have `viewMore` enabled — the chart IS the full data, no "more" rows below it. For those, the drill ends at [[analytics-details]].

### `viewMore` as a string vs `true`

If `viewMore` is set to a STRING (e.g., Total Sales → `'top-order-products-by-units-sold'`), the View more link jumps to a DIFFERENT box's View more screen — useful for chart cards that want their drill-in to lead the merchant to the related table. If `viewMore` is set to `true`, View more goes to this same box's full list.

### Sorting

The columns are NOT clickable to sort on the client (`sortable: false` in the column definition). The order of rows is whatever the backend pipeline returns, which is usually descending by the box's headline metric (e.g., Top Products by units sold → sorted by units sold DESC). Default sorting can be overridden per box via `viewMore.defaultSorting` in the box config (currently most boxes leave this as `[]`).

### Breadcrumb building

The breadcrumb is constructed dynamically:

1. **Analytics** (clickable → returns to the dashboard with same date range).
2. **{box title}** — uses `labels.title_viewMore` if defined, else falls back to `labels.title`. Clickable to [[analytics-details]] for this box IF the box also has `hasDetails: true`.
3. **{titleValue}** — only if the backend returned a `titleValue` (i.e., the merchant drilled in via a specific record). Can be a single string (one breadcrumb step) or an array of `{text, id}` (multiple clickable steps to mid-drill states).

Example for Sales by Source / Medium:
- Top-level: `Analytics → Sales by Source / Medium / Campaign`.
- Drilled into "Google": `Analytics → Sales by Source / Medium / Campaign → Google` (last step is a text label, not clickable).

## Related

- [[analytics-full]] — hub.
- [[analytics]] — the dashboard the merchant came from.
- [[analytics-details]] — the per-metric drill-in (alternative path); the breadcrumb's middle step links here.
- [[analytics-more-details]] — third-level drill (only Sales by Source / Medium → Campaign).
- [[product]] — Top Products rows link out to product pages.
- [[category]] — Top Categories rows link out to category pages.
- [[vendor]] — Top Brands rows link out to vendor pages.
- [[bundle]] — Top Bundles rows.
- [[order]] — sales rows can link to specific orders.

## Open questions

_None._
