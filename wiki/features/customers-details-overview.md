---
type: feature
nav_path: "Customers → Customer details → Overview"
route_name: customers-details-overview.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer overview", "Customer order distribution", "Преглед на клиент", "Поръчки по статус"]
tags: [customers, overview, insights, chart]
plan_gates: ["customers"]
created: 2026-05-21
updated: 2026-05-27
source_count: 5
---
# Customer overview

## Purpose

The **default sub-tab** on a customer's details page. It breaks the customer's order history down by order status — six cards showing per-status counts and amounts, plus a doughnut chart of the proportional distribution. The merchant uses it to gauge the customer's relationship with the store at a glance: a healthy buyer (mostly completed/paid), a problem account (high cancellation/refund rate), or a new customer (sparse data).

## Where to find it

From [[customers-details]] → **Overview** tab (default — no path suffix on `/admin/customers-new/details/:id`).

## What the merchant can do here

### Six order-status cards (left half)

A 2x3 grid of cards. Each card shows:

- **Status icon + label** (the card label is clickable — see "Card label navigates" below).
- **`<count>` orders** — number of orders in this status.
- **`<quantity>` products** — total products across those orders.
- **Order amount `<total>`** — total monetary amount (currency-formatted).

The six statuses shown are:

| Status | Icon | Color (chart) |
|--------|------|---------------|
| **Completed orders** | Check-circle (green) | `#7CCFAF` (mint green) |
| **Paid orders** | Check-circle (green) | `#00B894` (dark green) |
| **Cancelled orders** | Times-circle (red) | `#FFB3B3` (light pink) |
| **Refunded orders** | Times-circle (red) | `#FF999C` (pink) |
| **Pending orders** | Clock (orange) | `#B38AF4` (purple) |
| **Failed orders** | Minus-circle (gray) | `#D6D9E9` (light gray) |

### Doughnut chart (right half)

On wider viewports (window width > 430px), the right side shows a doughnut chart with:

- **80% cutout** (thin donut style).
- Six color-coded segments corresponding to the six status cards.
- **Legend** on the right (or bottom when viewport is < 900px wide). Each legend entry shows: `<status label>` + `<percentage>%`.
- Hover tooltips show the exact value and percentage per segment.

### Mobile-friendly legend (≤ 430px)

When the viewport is 430px or narrower, the chart is replaced by a vertical legend list. Each row shows a colored square + label + percentage. (Note: mobile legend colors are slightly different from the desktop chart — see business rules below.)

### Card label navigates to filtered orders

Clicking the icon-and-label area of any card navigates to the [[customers-details-orders]] tab with a pre-applied status filter — e.g. clicking "Completed orders" opens the Orders tab filtered to that status for this customer. This is the canonical drill from "summary" to "specifics".

### Empty state

When the customer has zero orders across all six statuses, the chart area is replaced by the SVG illustration `sitecp/img/empty/no-orders-customer.svg` with the text *"No orders by this customer yet"*. The six cards still render (with 0s) so the layout stays consistent for brand-new customers.

### What the merchant CANNOT do here
- Filter or change the time window — this view is always lifetime (no "last 30 days" toggle).
- Drill into specific orders directly from the chart (only via card labels).
- Customise which statuses appear — the six are fixed.

## Settings & fields

The page is read-only summary. No editable fields. Data is fetched from the customer-overview API by customer ID.

## Business rules

### Always exactly six statuses (not mutually exclusive)

The six cards (Completed, Paid, Cancelled, Refunded, Pending, Failed) are hard-coded and map to the platform's standard order-status taxonomy (per [[settings-statuses]]) — the merchant cannot add, remove, or rename them here. Custom statuses the merchant defined in [[settings-statuses]] do **not** appear as separate cards; they fall into one of the six platform buckets per their template.

The cards are **not** mutually exclusive: "Completed" counts both explicit `status='completed'` orders AND any order with `status_fulfillment='fulfilled'` whose status is not in the negative set (voided/timeouted/cancelled/failed/refunded/chargebacked/disputed). So a paid-and-fulfilled order is counted in **both** the Completed card (via the fulfilled merge) and the Paid card (via its `status='paid'`).

### Card click pre-filters Orders tab

Each card label is a `router-link` to route `customers-orders.new` with query `filters[status][operator]=in&filters[status][value][]=<status_key>`. This pre-applies the status filter on landing, using the same filter mechanism as the global orders feature — consistent UX across screens.

### Empty-state threshold is zero across ALL statuses

The empty-state illustration triggers only when the SUM of all six statuses' counts is zero (`chartTotal === 0`) AND the viewport is > 430px. One order alone (e.g. a single pending order) switches to the chart view with that single segment. On mobile, the empty case renders the legend with all values = 0 instead.

### Legend percentages are rounded to whole numbers

The legend shows percentages without decimals (e.g. "Completed 67%"). Hover tooltips show one decimal place ("Completed: 4 (66.7%)").

### Desktop chart vs mobile legend colour discrepancy (verified)

The mobile-fallback legend (window width ≤ 430px) uses a different palette than the desktop doughnut chart — e.g. "Paid orders" is `#00B894` (dark green) on desktop but `#ff9500` (orange) on mobile, and Refunded/Cancelled positions are swapped. Pending stays `#B38AF4` on both. Resizing across the 430px breakpoint shows different colours for the same data. This appears to be a visual inconsistency / bug, not intentional design.

### Lifetime-only, refreshed on page load

This view is always lifetime (no date-range picker) — for windowed counts the merchant uses the Orders sub-tab's date filters. The per-status counts are queried fresh at page load and cached on the page; seeing updated numbers requires a manual reload or navigating away and back (no live polling). Note the parent page's Insights module (`income`, `completed_orders`, etc.) is denormalized and updated asynchronously on order-lifecycle events, so the Overview's fresh cards can briefly differ from the eventually-consistent Insights totals.

### Permission

Standard customers permission scope — the underlying endpoint is gated behind the `customers` API permission; moderators without that grant get 403 errors loading the tab.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `customers` | Numeric (max customer records) | Inherited page-level gate from [[customers]]. The cap only blocks creating new customers — viewing an existing customer's distribution is permission-gated only, never capped. |

This read-only summary has no plan surface specific to the sub-tab. The `GET /admin/api/core/customers/{id}/overview` endpoint requires only the `customers` API permission, not a plan-feature value lookup. Numeric gates extend via packs ([[plan-vs-feature-pack]]).

## Related

- [[customers-details]] — parent details page hosting this tab.
- [[customers-details-orders]] — drill-in target for the order-status cards.
- [[settings-statuses]] — defines the underlying order status taxonomy.
- [[customer]] — entity page.
- [[order]] — entity page.

## How it works (verified against backend)

### Data source: `GET /admin/api/core/customers/{id}/overview`

The tab fetches the customer's lifetime aggregates from this endpoint. The response returns THREE blocks:
- **orders**: per-status counts and totals across the platform's full 11-status taxonomy (authorized, pending, voided, timeouted, cancelled, failed, refunded, chargebacked, paid, completed, disputed). The page filters this down to the 6 displayed cards.
- **abandoned**: count and total for the customer's abandoned carts.
- **payments**: per-status totals across `completed`, `refunded`, `chargebacked`, `pending`.

Only the `orders` block is shown on this tab; **abandoned** and **payments** are returned but not rendered. The 5 order statuses with no card (authorized, voided, timeouted, chargebacked, disputed) are not rendered at all — a merchant with, say, a high-volume disputes workflow cannot see them from this Overview.

## Open questions
