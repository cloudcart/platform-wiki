---
type: feature
nav_path: "Analytics → Visits by traffic source (referral)"
route_name: analytics
route_path: /admin/analytics
aliases: ["Visits by traffic source (referral)", "Sessions by traffic source", "Referrer-based sessions", "По реферал", "Посещения по тип източник на трафик"]
tags: [analytics, ccanalytics, visitors, sessions, sessions-by-traffic-source, referrer]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 10
---
# Visits by traffic source (referral)

## Purpose

A table that breaks down the period's store sessions by the **HTTP referrer** that brought them in — Google, Facebook, Direct, a specific news site, an email domain, etc. CloudCart classifies each referrer into a **group** (search, social, paid, news, email, payments, or unknown) so the merchant sees both the specific referring site (`facebook.com`) and the category it belongs to (`social`).

This is the **organic traffic / referral diagnostic**. Where [[analytics-sessions-by-social-source]] reads UTM tags (campaigns explicitly tagged by the merchant or their advertisers), this box reads the browser-sent referrer header. Together they triangulate where traffic comes from.

## Where to find it

Analytics dashboard → **Visits by traffic source (referral)** box — a `table`-type box positioned middle-bottom of the dashboard. Box `key: "sessions-by-traffic-source"`.

Has both:
- **Details** drill-down — paginated full list of referrers with conversion and amount columns.
- **View More** drill-down with its own per-referrer time-series chart.

## What the merchant can do here

- Read the **top 5 referrers** for the period — each with referrer name, group label, count, percent, and a session-count meta-row (pluralised "Session/Sessions {value}").
- See the **device split** in a per-row tooltip (`Visits: {total}`).
- Click any row to drill into its **per-day breakdown + chart** via View More.
- Open the **Details screen** for pagination + CSV export with conversion-rate and amount columns.

### Box card surface (table-type)

| Surface | When it appears | What it does |
|---------|-----------------|--------------|
| **Box tooltip (dotted)** | On hover | "Number of visits grouped by the type of traffic source." |
| **Top 5 ranked rows** | Always | Top `TABLE_RECORDS_LIMIT = 5` referrer hosts. Each row shows the referrer name followed by an inline group-label pill (e.g. "social", "search"). |
| **Per-row View more link** | Each row | The row name becomes a link that opens the [[analytics-full]] full table with the inline chart for that referrer. |
| **Per-row external-page-link icon** | When a referrer URL is available | Tiny `fa-external-link` icon to the right of the name; opens the referrer's actual URL in a new tab. |
| **No-data state** | Empty range | "No data available for the selected range." |
| **Period-cutoff alert** | Period starts before `2023-01-01` | "There is no data for the selected period. Please select a period after 01.01.2023 to view data." |
| **504 timeout** | Period too large to compute | "We cannot generate statistics for the selected period, please reduce it." |
| **View details link** (top-right) | Box has rows | Opens [[analytics-details]] for this box. |

### Dashboard Settings panel (cog icon)

- **Order statuses** — no effect on these numbers (the box is visit-event-driven, not order-driven).
- **Industry** — no effect (this box has no industry comparison).
- **Show devices** — toggling OFF hides the per-row device badges and tooltips.
- **Show boxes sort** — this box can be hidden or repositioned within the table-type group.
- **Reset to default / Save / Cancel** — dashboard-wide semantics.

## Settings & fields

### Box configuration

- Box `key`: `sessions-by-traffic-source`; renders as a ranked `table` with both View More and Details drill-downs (the View More screen includes a time-series chart).
- Earliest date with referrer data: **2023-01-01**. Periods before this show the period-cutoff alert.

### Referrer-group labels

Each referrer is classified into one of **7 groups**, shown as a pill next to the referrer name. EN labels and what each covers (see Business rules for the full referrer dictionary):

| Group key | EN label | Covers |
|-----------|----------|--------|
| `unknown` | "Unknown" | Direct visits, missing referrer, or unmatched referrer. |
| `search` | "Search" | Google, Bing, Yandex, Yahoo, … |
| `social` | "Social" | Facebook, Instagram, Twitter, TikTok, … |
| `paid` | "Paid" | Ad networks (Outbrain, AdSpirit, Flashtalking, …). |
| `email` | "Email" | Webmail hosts (Abv.bg, Mail.bg, …). |
| `news` | "News" | News sites (24chasa.bg, Webcafe.bg, News.bg, …). |
| `payments` | "Payments" | Payment-gateway return pages (Borica.bg, …). |

The `unknown` row is rendered as "Unknown" for visitors with no referrer or an unrecognised referrer.

### Detail-screen table columns

| Column | EN label |
|--------|----------|
| `page_name` | "Name" |
| `orders` | "Orders" |
| `views` | "Views / Sessions" |
| `amount` | "Amount" |
| `conversion_rate` | "Conversion rate" |

### Tooltip text (exact UI quote)

EN: `"Number of visits grouped by the type of traffic source."`
BG: `"Брой посещения, групирани по типа източник на трафик."`

Per-row tooltip: `Visits: {total}` (with device breakdown).

## Business rules

### Referrer parsing and the referrer dictionary

CloudCart ships a fixed, curated dictionary of **416 known referrers** grouped into the 7 buckets. For each session's referrer the classifier matches the host against the dictionary and returns the first matching group + display name (e.g. Facebook → `social`, Google → `search`). Unmatched hosts fall through to `unknown` with the raw hostname as the display name.

| Group | Named referrers |
|-------|-----------------|
| `search` | 235 (Google, Bing, Yandex, Yahoo, DuckDuckGo, Naver, plus 200+ regional / niche) |
| `social` | 81 (Facebook, Instagram, TikTok, X/Twitter, Pinterest, Snapchat, Telegram, …) |
| `paid` | 47 (ad networks — Outbrain, AdSpirit, Flashtalking, AudienceScience, …) |
| `email` | 38 (webmail hosts — Abv.bg, Mail.bg, Gmail-forwarder hosts, …) |
| `news` | 9 (BG news sites — 24chasa.bg, Dnevnik.bg, News.bg, Webcafe.bg, Btvnovinite, …) |
| `unknown` | 5 (some Google subdomains, Broshura.bg, CloudCart-own domains) |
| `payments` | 1 (Borica.bg + sandbox subdomain) |

The dictionary is curated by CloudCart and updated as a single platform-wide change — merchants **cannot** add custom referrers, and classification is **identical across every store**.

### The Direct row

The special **Direct** referrer (no referrer header) shows the label "Direct" with its group badge suppressed. A buyer who navigated within the same store before ordering also counts as Direct rather than under the store's own domain — internal self-navigation is filtered out.

### Crawler / bot filtering

The tracking pipeline runs only for non-crawler requests. Detected crawlers, uptime/performance monitors (`uptimerobot`, `gtmetrix`, `ptst`), CloudCart's own builder requests, and requests carrying `?___clh` get no visitor cookie, so they never contribute to traffic-source counts.

### Counting: unique visitors vs sessions

The `hourly` grouping counts **unique visitors** per device; every other grouping counts **sessions** from pre-aggregated totals. The two are close but not identical — the same visitor seen in two hour-buckets is counted twice in non-hourly mode.

### Limits

Dashboard shows the top `TABLE_RECORDS_LIMIT = 5` referrers. Details paginates `DETAILS_PAGINATION_LIMIT = 100` per page; both Details and View More cap the displayed total at `DETAILS_FORCE_LIMIT = 1000` (so the merchant may see "1,000 of N"). **CSV export bypasses the cap.**

### Data freshness — 1-hour cadence

Both the raw and grouped traffic-source aggregations refresh hourly. Admin sessions are excluded.

### Drill-down depth

The box drills only one level deeper than the dashboard table: a top-N table on the card, a paginated full list with export (Details), and a per-day time-series for one referrer (View More). There is no second-level breakdown beneath a referrer.

## Related

- [[analytics]] — parent hub.
- [[analytics-online-store-sessions]] — the parent metric (total, no referrer split).
- [[analytics-sessions-by-social-source]] — UTM-based attribution (vs this box's referrer-based attribution).
- [[analytics-sessions-by-country]] — sessions split by visitor country.
- [[analytics-sessions-by-device]] — sessions split by device type.
- [[analytics-details]] — the per-box drill-down screen.
- [[analytics-full]] — View More time-series screen.

## Open questions

_None._
