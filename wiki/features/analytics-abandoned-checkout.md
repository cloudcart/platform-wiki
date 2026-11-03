---
type: feature
nav_path: "Analytics → Abandoned checkouts rate"
route_name: analytics
route_path: /admin/analytics
aliases: ["Abandoned checkouts rate", "Abandoned checkout", "Checkout abandonment", "Изоставени поръчки", "Изоставени поръчки за периода"]
tags: [analytics, ccanalytics, cart, abandoned-checkout]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 9
---
# Abandoned checkouts rate

## Purpose

A merchant-facing chart that shows what **percentage of shoppers who reached the checkout page never placed the order** — carts that got past the cart drawer (the checkout page loaded) but were never completed because the shopper bailed at delivery, payment, or final confirmation.

This is the "late funnel leak" — the most expensive kind of abandonment, because the shopper already signalled clear purchase intent and the friction that lost them is usually fixable (shipping-cost shock, missing payment method, confusing form, slow validation).

Pair this with [[analytics-abandoned-carts]] (the *earlier* leak — shoppers who added items but never reached checkout) and [[analytics-cart-conversion-funnel]] (the unified visual of all three stages).

## Where to find it

Analytics dashboard → **Abandoned checkouts rate** box (Bulgarian subtitle: "Изоставени поръчки за периода"). It sits next to the Abandoned carts box (`navigationSort: 6`). Box `key: "abandoned-checkout"`, `type: "chart"`.

## What the merchant can do here

- See the **headline percentage** of abandoned checkouts for the period.
- Watch the rate **over time** in the chart underneath; hover for per-bucket counts ("62.5% — 80 abandoned checkouts from 128 for 2026-05-22").
- Compare to the **previous period** (delta next to headline) and against the **industry benchmark** (`hasIndustryCompare: true`).
- See the **mobile vs desktop** split (icons `fa-mobile` and `fa-desktop`).
- Change the **date range** and **grouping** (hourly / daily / weekly / monthly / quarterly / yearly).

### Box card surface

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box title** | Always | "Abandoned checkouts rate" (EN) / Bulgarian equivalent. Plain text, never a dropdown — no child boxes. |
| **Box tooltip (dotted)** | On hover | "Total of abandoned carts of customers reached to checkout." (EN) |
| **Headline number** | Always | The abandonment rate (e.g. "62.5%"), `percentFormat`. |
| **Device rows** | Device data available | Two rows: `fa-mobile` and `fa-desktop`, each percentage + parenthesised count. |
| **Previous period delta** | Compare = `period` or `year` | "Previous period: 58.3%". When the previous period starts before `collectDataFrom = 2023-01-13`, the cell shows **"N/A"** with a cutoff tooltip. |
| **Trend arrow** | Compare is set | Up/down arrow + percent delta, reflecting the raw numeric move. |
| **Industry compare badge** | `hasIndustryCompare: true` AND benchmark loaded | "For period {period} {title}: {value} where is {percent} above/below the average for {industry}". Lower abandonment = better. |
| **No-data state** | Zero events | "No data available for the selected range." |
| **Period-before-cutoff alert** | `dateFrom` < `2023-01-13` | "There is no data for the selected period. Please select a period after 13.01.2023 to view data." |
| **504 timeout** | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |

### Dashboard Settings panel (cog icon)

The cog top-right of the Analytics dashboard opens a right-side modal that affects this box:

- **Order statuses that will be included in the analyses** — multi-select. This setting *does* affect this box: the order-completion deduction is status-filtered (see Business rules), even though the checkout count is not.
- **Please select a primary branch, which is most suitable for your business** — drives the industry-compare benchmark; takes up to 1 week to update.
- **Show devices** — toggling OFF hides the two device rows on this card.
- **Show boxes sort** — drag/visibility tree; this box can be hidden or moved within the `chart` group.
- **Reset to default** — reverts ALL dashboard-level settings (statuses, industry, show-devices, sort, visibility).
- **Save** — `POST /admin/api/analytics/settings`; invalidates the browser-side cache. **Cancel** closes without applying edits.

## Settings & fields

### Box configuration

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `abandoned-checkout` | Unique box identifier. |
| `type` | `chart` | Percentage headline + over-time chart. |
| `collectDataFrom` | `2023-01-13` | Earliest date with data; ranges before this return nothing. |
| `hasIndustryCompare` | `true` | Industry-benchmark comparison enabled. |
| `navigationSort` | `6` | Display order on the dashboard. |

### Metric definition

- **Checkout starts (`uniqueCheckout`)** — unique visitors (by UUID) who reached the checkout page in the bucket.
- **Orders** — completed orders in the merchant's selected analytics statuses (see Business rules).
- **Abandoned checkouts** — `uniqueCheckout − orders`: the absolute count of checkout-starters who didn't complete an order.

### Device split

- `mobile` — counted when `device == 'mobile'`.
- `desktop` — everything else; tablet sessions fold into desktop.
- `total` — sum of mobile + desktop.

## Business rules

### What counts as "abandoned checkout"

The rate is `(uniqueCheckout − orders) / uniqueCheckout` — the fraction of checkout-starters who didn't complete an order. A checkout start is counted the moment the `/checkout` page loads, so **any shopper who reached checkout via any path** (cart drawer, deep-link, abandoned-cart restore email, Fast Order) is included. Each checkout start is counted once per visitor UUID, per device, per bucket.

### Orders are status-filtered, checkout starts are NOT

This is the box's structural asymmetry. The checkout-start count reflects raw shopper intent (every cart that loaded the checkout page), but the deducted **orders** only count toward the merchant's selected analytics statuses. Consequences:

- **Excluding** Pending → unpaid-but-real orders aren't deducted → the rate is inflated.
- **Including** Cancelled → cancelled orders ARE deducted → the rate is deflated.

So changing **Order statuses that will be included in the analyses** does move this box's number, via the orders side of the ratio.

### Cross-bucket carry-over

Abandonment is reckoned per bucket on event time. A shopper who starts checkout on day 1 and completes the order on day 2 adds the checkout start to day 1 and the order to day 2 — there is **no back-attribution**, so day 1's rate stays inflated even though the order eventually happened.

### Data freshness

Same pipeline as [[analytics-abandoned-carts]]: cart and checkout events are aggregated for the dashboard once per hour, so a freshly abandoned checkout appears up to 1 hour later. Visitors flagged as admins are excluded so store-staff testing the checkout doesn't inflate the metric. The metric is computed identically for every store — there is no per-store override.

### Device split before 2023-01-17

If the date range `from` is before **2023-01-17**, the mobile/desktop/total split is forced to `'N/A'` (device attribution is not trustworthy before that date). Tablet sessions fold into the `desktop` bucket, consistent across the Analytics area.

### Industry comparison

The platform aggregates anonymised abandoned-checkout rates per industry and shows the benchmark line on the chart. No store-identifying data is shared between stores.

### Rate can exceed 100%

This box shares its data source with [[analytics-abandoned-carts]] and [[analytics-cart-conversion-funnel]] but exposes a different ratio (abandoned carts use `(unique − uniqueCheckout) / unique`). Because checkout-start and add-to-cart are independent events, a restored cart can produce a checkout start without a same-period add-to-cart, so over very short ranges `uniqueCheckout` can exceed `unique` and the percentage can land outside 0–100%; the formatter does not clamp.

## Related

- [[analytics]] — parent hub.
- [[analytics-abandoned-carts]] — the earlier funnel leak; same data source, different ratio.
- [[analytics-cart-conversion-funnel]] — the unified 3-step funnel visualization.
- [[analytics-cart-conversion-rate]] — site-wide visitor-to-order rate.
- [[analytics-online-store-sessions]] — visitor volume in the same period.
- [[checkout-flow]] — the underlying entity whose abandonment is being tracked.

## Open questions

_None._
