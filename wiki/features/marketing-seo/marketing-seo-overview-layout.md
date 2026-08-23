---
type: feature
nav_path: "Marketing → Seo → Page layout"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Main SEO layout", "SEO page layout", "SEO seven cards", "SEO escape hatch cookie", "SEO page navigation", "Оформление на SEO страница"]
tags: [marketing, seo, layout, navigation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-seo]]. See the hub for the other page-level aspects (card-save model, settings map, save endpoints, trial block) and the seven per-card deep dives.

# Main SEO settings — page layout & navigation

## Purpose

This aspect documents how the Main SEO screen is **laid out and reached** — where it lives in the sidebar, the seven-card structure, the legacy fallback cookie, and the precise list of what the merchant can and cannot do on this screen (as opposed to on the related SEO sub-screens). For what each card actually does, drill into that card's deep-dive page; this aspect is purely the page-level frame.

## Where to find it

Sidebar → Marketing → **SEO** (the first SEO sub-entry, labelled "Main SEO"). Route name `seo-main`, path `/admin/marketing-new/seo`. The page header shows the Searchengin brand icon (`fa-brands fa-searchengin`) and the title "Main SEO settings". The breadcrumb reads "Marketing → SEO settings".

The page is the new Vue rewrite of the legacy `/admin/marketing/seo` Smarty page. The legacy version is preserved as an escape hatch: setting the cookie `marketing-seo-main=old` falls back to the old Smarty page. This is the same escape-hatch pattern used by the sibling SEO screens (for example `marketing-301-redirects=old` on [[marketing-seo-301-redirects]]).

## What the merchant can do here

The screen is laid out as **seven self-contained cards**. Each card pairs an info/description column (left, 5/12 width on desktop) with the actual setting (right, 7/12 width). The cards, in order:

- **Canonical tag** — toggle the `<link rel="canonical">` tag on/off store-wide. See [[marketing-seo-canonical]].
- **Deindex filtered & sorted pages** — control whether `?filter=…` / `?sort=…` URLs get `<meta name="robots" content="noindex">`, with a parameter-count threshold. See [[marketing-seo-deindex]].
- **Pagination word in meta** — the literal word ("Page", "Страница", etc.) prefixed to meta titles & descriptions on page 2 of any paginated list. See [[marketing-seo-meta-title]].
- **Sitemap.xml** — read-only display of the sitemap URL with a copy-to-clipboard control. See [[marketing-seo-sitemap]].
- **Robots.txt** — full-content text editor for the robots.txt body, guarded by a confirmation modal. See [[marketing-seo-robots]].
- **Llms.txt file** — the Markdown file published at `/llms.txt` telling AI assistants what the store sells and which pages are worth reading. See [[marketing-seo-llms]].
- **RSS feed** — set how many products go into the RSS feed (1-100) and copy the feed URL. See [[marketing-seo-rss]].

### What the merchant CANNOT do here

- Per-page meta titles/descriptions per section — see [[marketing-seo-meta]].
- Per-URL 301 redirect rules — see [[marketing-seo-301-redirects]].
- Per-product meta tag overrides — see the product details editor on [[product]].
- Per-category meta overrides — see [[category]].
- Add a domain-level redirect from an alternate store domain — see [[apps-domain-redirect]].
- Edit individual sitemap files or change sitemap generation cadence — the sitemap is auto-regenerated and not editable (see [[marketing-seo-sitemap]]).

## Settings & fields

This aspect has no settings of its own — it documents the frame, not the controls. The full field-by-field reference across all seven cards lives on [[marketing-seo-overview-settings-map]]; per-card controls live on each card's deep-dive page.

## Business rules

- The seven cards render top-to-bottom in the fixed order above; the order is not configurable.
- Each card saves independently — there is no global submit. The save model is its own aspect: see [[marketing-seo-overview-card-save]].
- The legacy escape-hatch cookie (`marketing-seo-main=old`) is a temporary fallback for the Vue rewrite; it is not a documented merchant feature and should not be promoted to merchants.

## Related

- [[marketing-seo]] — hub.
- [[marketing]] — parent navigation hub.
- [[marketing-seo-meta]] — per-section meta titles & descriptions (a sibling SEO screen, not a card here).
- [[marketing-seo-301-redirects]] — per-URL 301 redirects (a sibling SEO screen, not a card here).
- [[product]] — per-product meta overrides.
- [[category]] — per-category meta overrides.
- [[apps-domain-redirect]] — whole-domain redirects.

## Open questions

None.
