---
type: feature
nav_path: "Analytics → Visits by location"
route_name: analytics
route_path: /admin/analytics
aliases: ["Visits by location", "Sessions by country", "Visits by country", "По местоположение", "Посещения по местоположение", "Посещения по държава"]
tags: [analytics, ccanalytics, visitors, sessions, sessions-by-country]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Visits by location

## Purpose

A table that breaks down the period's store sessions by the **visitor's country** (geolocated from IP). Lets the merchant see where their traffic comes from — useful for catching unexpected international spikes, validating that paid campaigns reach the right geography, or noticing language/shipping markets to add.

This is the **geographic-distribution diagnostic** that pairs with [[analytics-online-store-sessions]] (the total, with no location split) and the orders-by-location box ([[analytics-orders-by-country]] if present) to compare *where shoppers come from* vs *where they buy from*.

## Where to find it

Analytics dashboard → **Visits by location** box. `navigationSort: 19` places it mid-bottom of the dashboard. Box `key: "sessions-by-country"`, `type: "table"`.

Click the box header to open the **Visits by location {details}** drill-down screen ([[analytics-details]]) — `hasDetails: true`.

## What the merchant can do here

- Read a **ranked table** of the top 5 countries by session count. Each row: country name, current count (`numberFormat`), percent of total (`percentFormat`).
- See the **device split** for each country in a hover tooltip — `Visits: {total}` (BG: `Посещения: {total}`) followed by a mobile/desktop breakdown.
- Click **View details** (top-right of card) to open a paginated screen with *all* countries (not just top 5), same columns plus a per-row page-link drill-in.
- Compare to the previous period (when comparison mode is active); change date range and grouping.
- The session-count cell pluralises: "Session {value}" / "Sessions {value}" (BG: "Сесия {value}" / "Сесии {value}").

### Box card surface (table-type)

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box title** | Always | "Visits by location". On an in-card sub-drill it morphs to **"Visits by location {details}"** (e.g. "...Bulgaria") via the `title_details` label + active sub-record name. |
| **Back arrow** (`fa-arrow-left`) | After an in-card drill | Top-left; returns to the top-level country list without leaving the dashboard. |
| **Box tooltip (dotted)** | On hover | "Number of visits by location on your online store." |
| **Top 5 ranked rows** | Always | Capped at the platform code; each row clickable for a `PageLink` drill. |
| **Per-row device tooltip** | Hover device badge | `Visits: {total}`. |
| **No-data state** | Empty range | "No data available for the selected range." |
| **Period-cutoff alert** | `dateFrom` < `2023-01-01` | "There is no data for the selected period. Please select a period after 01.01.2023 to view data." |
| **Per-period timeout (504)** | API HTTP 504 | "We cannot generate statistics for the selected period, please reduce it." |
| **View details link** | `hasDetails: true` AND > 0 rows | Routes to `analytics.details.view` → [[analytics-details]] full table. The only deep-link out (`viewMore` disabled — no "View more"). |
| **In-card sub-drill** | Backend returns `details: <id>` on a row | Clicking swaps the card body to the sub-table inline (no route change); back-arrow or a date-range change resets it. |
| **No industry compare** | — | No `hasIndustryCompare` → no industry pill. |

### Dashboard Settings panel (cog icon)

- **Order statuses** — no effect (this box is visit-event-driven, not order-driven).
- **Industry** — no effect (no `hasIndustryCompare`).
- **Show devices** — when OFF, the per-row mobile/desktop tooltips and badges are suppressed.
- **Show boxes sort** — drag/visibility tree; a `table`-type box can only be reordered within its type group.
- **Reset to default / Save / Cancel** — dashboard-wide semantics.

## Settings & fields

### Box configuration

| Property | Value | Meaning |
|----------|-------|---------|
| `key` | `sessions-by-country` | Unique identifier. |
| `type` | `table` | Renders as a ranked table. |
| `collectDataFrom` | `2023-01-01` | Earliest date with country data. |
| `hasDetails` | `true` | Has a paginated drill-down screen. |
| `navigationSort` | `19` | Mid-bottom of the dashboard. |
| `details.group` | `false` | Detail screen hides the time-grouping selector. |
| `details.defaultSorting` | `[{key: 'sales', sortingMode: 'desc'}]` | Detail table sorted by `sales` desc when composed with order data. |
| `details.viewMore.group` | `true` | When drilling into a single country (View More), the time-grouping selector reappears. |
| `details.subDetails.group` | `false` | The per-page sub-level does NOT show grouping. |

### Detail-table columns

| Column key | UI label EN | UI label BG | Type |
|------------|-------------|-------------|------|
| `page_name` | "Name" | (translated separately) | Page link (clickable) |
| `views` | "Views / Sessions" | "Преглеждания / Сесии" | number |

### Tooltip text (exact UI quotes)

- EN: `"Number of visits by location on your online store."`
- BG: `"Брой посещения по местоположение във Вашия онлайн магазин."`
- Per-row: `Visits: {total}` (the country's session count).

### Country identifier

Country is stored as a 2-letter ISO code (e.g. `BG`, `RO`, `US`), or `---` when the IP can't be geolocated. The display name is rendered client-side from the locale's country dictionary. There is no continent / "EU" rollup — Bulgaria, Germany, France stay separate rows, so the merchant scans visually to spot EU-wide patterns.

## Business rules

### Where the country comes from

- **Guest visitors** are geolocated from IP via the **MaxMind GeoLite2-City** database read locally on the server (no per-request external call). The result is cached 30 minutes per IP (`geoip.cache_expires = 30`); a country is resolved at session start and included on each tracked event.
- **Logged-in customers** take their country from their stored address instead of geolocation.
- **`---` fallback** fires only when MaxMind can't resolve the IP (private networks, some IPv6 ranges, malformed IPs) — single-digit percentages in normal traffic.
- **No VPN / proxy detection** — a VPN visitor appears under the proxy's exit-IP country.

### `---` rows are filtered out → totals differ

The box excludes `country == '---'` rows by default, so un-geolocated visits do **not** appear here. They still count in [[analytics-online-store-sessions]] (the total), so the sum of visible rows is strictly less than the total by the number of `---` sessions — a merchant noticing that discrepancy is seeing the geolocation-failure population. (On a single-country drill, the `---` exclusion is replaced by a filter on the supplied ISO list.)

### Crawlers / bots never appear

A request flagged as a crawler (User-Agent detection, an allow-list of `uptimerobot` / `gtmetrix` / `ptst` / internal `builder-google-*`, plus the `___clh` URL override) is held in memory only and gets no visitor cookie. It never reaches the country data — bots are excluded before geolocation runs.

### Top-N limit and detail pagination

The dashboard box shows up to the platform code countries. The Details screen paginates at the platform code per page, with the platform code as the hard cap; the default order is by session count desc. The CSV **Export** button returns the entire result set with no limit.

### "View More" per-country drill

Clicking a country row filters the dataset to that single ISO code and re-aggregates by landing page within that country, so the merchant sees *which pages* visitors from that country land on. The time-grouping selector reappears (`details.viewMore.group: true`).

### Data freshness — 1-hour cadence

Country data is a per-country/per-day rollup refreshed on the standard 1-hour cadence (there is no per-session country collection). A newly-seen country of visit appears in the box within roughly 1–2 hours.

### No per-merchant override

Geolocation logic and the `---` exclusion rule are identical across every store. There is no per-merchant setting.

## Related

- [[analytics]] — parent hub.
- [[analytics-online-store-sessions]] — the total this box decomposes.
- [[analytics-sessions-by-device]] — sessions split by device type instead of country.
- [[analytics-sessions-by-social-source]] — sessions split by UTM source/medium.
- [[analytics-sessions-by-traffic-source]] — sessions split by referrer.
- [[analytics-details]] — the per-box drill-down screen opened from View Details.

## Open questions

_None._
