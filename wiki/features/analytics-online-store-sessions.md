---
type: feature
nav_path: "Analytics → Total Visits"
route_name: analytics
route_path: /admin/analytics
aliases: ["Total Visits", "Online store sessions", "Visitors over time", "Сесии", "Посетители за периода"]
tags: [analytics, ccanalytics, visitors, sessions, online-store-sessions]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 10
---
# Total Visits (Online store sessions)

## Purpose

A merchant-facing chart showing the **total number of visits to the storefront over the selected period** — the topline traffic metric and the denominator the conversion-rate boxes implicitly compare against. It counts visits, not unique people: a returning shopper across two days is counted twice. Usually the first metric a merchant checks when opening Analytics.

## Where to find it

Analytics dashboard → **Total Visits** box (Bulgarian subtitle: "Посетители за периода").

`navigationSort: 3` — high on the dashboard, just below the order-value metrics. The box `key: "online-store-sessions"`, `type: "chart"` — a single numeric headline with a sparkline over time.

## What the merchant can do here

- See the **headline visit count** (e.g. "12,847") and the trend chart underneath.
- Compare to the **previous period** (delta shown) and against the **industry benchmark**.
- Change the **date range** in the page-level picker.
- Change the **grouping**: hourly / daily / weekly / monthly / quarterly / yearly.
- Hover the chart for per-bucket tooltips: `"125 visitor for 2026-05-22"` / `"125 visitors for 2026-05-22"` (singular/plural).

### Box card surface

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box title** | Always | "Total Visits" (EN) / "Сесии" (BG). Plain text. |
| **Box tooltip (dotted)** | Always on hover | "Number of visits in your online store." |
| **Headline number** (`text1`) | Always | The total session count for the period. `numberFormat` (thousand separators). |
| **Subtitle** | Below headline | "Visitors over time" (EN) / Bulgarian equivalent. |
| **Previous period delta** (`text3`) | Compare `period` / `year` | "Previous period: 11 232". If previous range begins before `collectDataFrom = 2023-01-01`, shows "N/A" with cutoff tooltip. |
| **Trend arrow** | Compare set | Up arrow green / down red. |
| **View details link** | Hidden | `hasDetails` not set → no per-bucket drill-in from this card. |
| **Industry compare badge** | `hasIndustryCompare: true` AND benchmark loaded | Pill with above/below industry text. |
| **No-data state** | Empty range | "No data available for the selected range." |
| **Period-cutoff alert** | `dateFrom` < `2023-01-01` | "There is no data for the selected period. Please select a period after 01.01.2023 to view data." |
| **504 timeout** | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |

### Dashboard Settings panel (cog icon)

The shared dashboard Settings modal (documented on [[analytics]]) affects this box in two ways:

- **Order statuses** — does NOT change Total Visits, because visits are tracked from storefront events with no order required.
- **Industry** — drives the industry-compare benchmark on this box (recompute lag up to 1 week).

The box can also be hidden or repositioned within the `chart` group via the drag-and-drop sort tree.

## Settings & fields

### Box configuration

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `online-store-sessions` | Unique box identifier. |
| `type` | `chart` | Number headline + over-time line chart. |
| `collectDataFrom` | `2023-01-01` | Earliest date with session data — older than the cart pipelines (which start 2023-01-13). |
| `hasIndustryCompare` | `true` | Industry-benchmark line available. |
| `navigationSort` | `3` | Display position, high on the dashboard. |

### Tooltip text (exact UI quote)

EN: `"Number of visits in your online store."`
BG: `"Брой посещения във Вашия онлайн магазин."`

## Business rules

### What counts as a "session"

A "session" is one visitor (identified by a cookie-based tracker UUID) within one **hour-bucket**, for one inbound source / referrer / UTM combination. The headline sums these session-rows. Consequences a merchant should know:

- **Same visitor browsing for 2 hours = 2 sessions** (one row per hour-bucket).
- **Same visitor switching UTM source mid-hour** (e.g. a Facebook ad then a Google ad) = 2 sessions.
- **Same visitor switching device mid-hour** (desktop → mobile) = 2 sessions, because the UUID is per-browser.
- A visitor who lands and bounces (one page view, then leaves) still counts as 1 session.

The count rolls up storefront **view events** only — home-page view, page view, category, product, collection, vendor, and search. API calls and admin views never count.

### Hourly vs all other groupings

The box answers from two data sets. **Hourly** grouping reads raw per-session records (the only mode with sub-day detail, and the more expensive query). **Every other** grouping (daily / weekly / monthly / quarterly / yearly / auto / none) reads a smaller pre-aggregated per-day rollup, so wide date ranges stay fast.

### Mobile vs desktop categorisation

Same convention as the rest of the Analytics dashboard:
- `device == 'mobile'` → mobile.
- `device != 'mobile'` → desktop (tablet sessions fold into desktop).
- `total = mobile + desktop`.

There is **no cross-device merge**: a shopper on mobile in the morning and desktop in the evening is two sessions, splitting correctly across the device rows but possibly double-counting one person.

### Who is excluded from the count

- **Admin browsing** — tracker UUIDs matching `/^admin-.*/i` are filtered out, so a merchant browsing their own store doesn't inflate Total Visits.
- **Known crawlers** — bots (Googlebot, Bingbot, AhrefsBot, etc.) are detected at page-render time and never emit tracking events. An undetected new bot will pollute counts until the detection library is updated.
- **Internal navigation** — events whose referrer type is `self` are dropped, so 10 internal clicks in an hour contribute one session, not ten.
- **Disabled sites** — a store on the analytics disabled-sites list writes no data and shows 0.

### Data freshness — 1-hour aggregation lag

Sessions data is **not real-time**. An hourly job reads raw events; a follow-up job rolls them into the per-day rollup shortly after. A visitor who arrives at 10:42 may appear in the box 1–2 hours later.

### Site timezone matters

The query window is shifted into the store's timezone (`site('timezone')`, defaulting to `UTC`). A "day" in this box matches the merchant's local day, not UTC — important for stores in non-UTC timezones.

### Industry comparison

`hasIndustryCompare: true` — the box overlays a comparison against the per-industry aggregate. The merchant's own number is never shared with peers; only the aggregate flows back. Recompute lag up to 1 week.

Session counting has no per-merchant overrides — the hour-bucket dedup, admin-exclusion, crawler filter, timezone shift, and device split are the same for every store.

### Visitor vs Session terminology

CloudCart uses "visit" and "session" interchangeably. "Visit" appears in the headline and tooltip ("Number of visits…"); "Session" appears in detail tables (e.g. `Session {value}|Sessions {value}` in [[analytics-sessions-by-country]] and the social-source boxes). For unique-people counts a merchant should use customer-centric boxes (Customer value, Returning customers) instead.

### Why this number differs from the cart funnel

The cart pipeline counts only `addToCart` + `initiatedCheckout` events — never plain page views. A visitor who landed but never added to cart appears here but not in the cart data. This is the usual reason Total Visits exceeds the denominators on [[analytics-cart-conversion-rate]] and [[analytics-cart-conversion-funnel]].

## Related

- [[analytics]] — parent hub.
- [[analytics-sessions-by-device]] — same data broken down by device (mobile/desktop/tablet).
- [[analytics-sessions-by-country]] — same data broken down by visitor location.
- [[analytics-sessions-by-social-source]] — same data broken down by UTM source / medium.
- [[analytics-sessions-by-traffic-source]] — same data broken down by referrer (Google, Facebook, Direct, etc.).
- [[analytics-cart-conversion-rate]] — the conversion-rate metric that uses a *cart-pipeline*-derived visitor count (a closely-related but slightly-different denominator).
- [[analytics-cart-conversion-funnel]] — the funnel whose top stage is the cart, which itself depends on Total Visits.

## Open questions

_None._
