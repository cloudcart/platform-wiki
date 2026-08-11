---
type: feature
nav_path: "Analytics → Landing pages by visits"
route_name: analytics
route_path: /admin/analytics
aliases: ["Landing pages by visits", "Top landing pages", "Most visited pages", "Landing pages", "Целеви страници", "Топ страници по посещения"]
tags: [analytics, ccanalytics, landing-pages, traffic, top-landing-pages]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---
# Landing pages by visits

## Purpose

Shows you which **content pages** of your store bring the most visitors — the homepage and every custom content page (Pages → … in admin). Unlike the products / categories / brands traffic boxes which only count product/category/vendor URLs, this box covers the **rest of the site**: homepage, About us, Shipping, FAQ, blog posts, landing campaigns, etc.

Useful for measuring marketing campaigns: when you build a custom landing page for a Facebook ad or an email promotion, this is where you see whether traffic actually arrived. It also exposes how much of your overall traffic goes to the homepage (entry "Home page") vs how much is direct-to-product.

Tooltip (EN / BG): *"Top landing pages where visitors entered your online store."* / *"Най-популярните страници посещавани във Вашия онлайн магазин."*

> Naming note — this is **"Landing pages by visits"**, NOT to be confused with [[analytics-landing-pages-by-sales]] which ranks the same pages by revenue from orders that started on them. Same underlying page dimension, different ranking metric, drawn from a different analytics dataset.

## Where to find it

Analytics dashboard → **Landing pages by visits** box. `navigationSort: 16.1`. Box `key: "landing-pages"`, box `type: "table"` — a top-5 ranked table with per-row mobile/desktop tooltips. Clicking the box title opens **Details**; clicking a page row drills into a per-date time-series chart (**ViewMore**). `collectDataFrom: '2023-01-01'` — date ranges earlier than 2023-01-01 return no data (the platform did not collect this box's data before that date).

## What the merchant can do here

- See the top 5 most-visited content pages (homepage + content pages) on the dashboard, with mobile/desktop split.
- Open **Details** — a paginated table of every page visited in the period.
- Drill into **ViewMore** — a per-date traffic chart for a single page (including the homepage).
- Change the date range and compare against a previous period.
- Filter Details by specific page ids (passing `[0]` shows only the homepage).
- Export Details / ViewMore data as CSV.

The full UI surface (dashboard box, Details columns, ViewMore chart, toolbar) is in [[analytics-top-landing-pages-ui]]. What a "view" means + where the numbers come from is in [[analytics-top-landing-pages-data-source]]. The CSV export modal + 2FA + queue + client cache is in [[analytics-top-landing-pages-export]].

## Sub-pages (in this cluster)

- [[analytics-top-landing-pages-ui]] — the three drill-down levels (dashboard top-5, Details table, per-page ViewMore chart), every column, the Vue box config, and the page-wide date / compare / group / export toolbar.
- [[analytics-top-landing-pages-data-source]] — what counts as a "view", the homepage-is-page-id-0 convention, the UUID × hour × device de-duplication, the admin-traffic exclusion, where the page identifier comes from, the drill-down levels, and how the data is rolled up.
- [[analytics-top-landing-pages-export]] — the Export → modal → 2FA → queue flow, the 150 000-row export cap, the 1000-row ViewMore force-limit, and the 60-second client-side cache.

## Settings & fields

This box has no merchant-editable settings of its own — its behaviour is fixed in the box configuration (`key`, `type`, `collectDataFrom`, `viewMore`, `hasDetails`, `hasViewMoreChart`, `navigationSort`, `details.group`, `details.defaultSorting`). The full table is in [[analytics-top-landing-pages-ui]].

The Details / ViewMore show **only views columns** (Name + "Views / Sessions") — no orders / units / amount / conversion_rate, because this box does not join with the orders dataset. For revenue-side data on the same page dimension, see [[analytics-landing-pages-by-sales]].

The page-wide date / compare / group / export controls and their plan gates are tabulated in [[analytics-top-landing-pages-ui]].

## Business rules

- **"Landing page" means homepage OR a custom Content Page** — not "the first page in a session" (an entry-page concept). Product / category / brand / checkout-flow views live in sibling boxes. See [[analytics-top-landing-pages-data-source]].
- **The homepage is always page-id 0** and renders as "Home page" with the store's primary domain; it is also drillable into a ViewMore chart. See [[analytics-top-landing-pages-data-source]].
- **A "view" is one page-view, deduplicated per visitor UUID × hour × device** — 50 refreshes in an hour by the same visitor count as one view. Full attribution model: [[analytics-top-landing-pages-data-source]].
- **Admin-panel previews are excluded** — visitors whose UUID starts with `admin-` are filtered out. See [[analytics-top-landing-pages-data-source]].
- **Top-N is fixed at 5; Details paginates at 100/page; ViewMore is force-limited to 1000 rows.** The merchant cannot configure these. See [[analytics-top-landing-pages-ui]] + [[analytics-top-landing-pages-export]].
- **All queries are scoped to the store** (store + date window) with no per-store overrides. See [[analytics-top-landing-pages-data-source]].

## Related

- [[analytics]] — parent hub.
- [[analytics-top-landing-pages-ui]] — UI surface aspect.
- [[analytics-top-landing-pages-data-source]] — data-source / attribution aspect.
- [[analytics-top-landing-pages-export]] — export + cache aspect.
- [[analytics-landing-pages-by-sales]] — sister box, ranks the same page dimension by revenue from orders that started there; drawn from a different analytics dataset.
- [[analytics-top-products-by-traffic]] — same logic at the product level.
- [[analytics-top-categories-by-traffic]] — same logic at the category level.
- [[analytics-top-brands-by-traffic]] — same logic at the vendor level.
- [[analytics-cart-conversion-funnel]] — checkout-flow page metrics (separate from this box).

## Open questions

_None._
