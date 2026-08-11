---
type: feature
nav_path: "Marketing → Seo → Settings map"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["SEO settings map", "Main SEO field reference", "SEO fields table", "SEO validation rules", "Карта на SEO настройки", "SEO полета справка"]
tags: [marketing, seo, fields, validation, reference]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[marketing-seo]]. See the hub for the other page-level aspects (layout, card-save model, save endpoints, trial block) and the seven per-card deep dives.

# Main SEO settings — full field reference

## Purpose

This aspect is the **single field-by-field reference table** for every control on the Main SEO screen — what each field stores, its default, and its validation rules / error messages. It is the consolidated "what does this field do and what will the validator reject" lookup. For the deeper behaviour behind any one card (how canonical renders, how the noindex count works, etc.), follow the per-card link in the table.

## Where to find it

Sidebar → Marketing → **SEO**. Route name `seo-main`, path `/admin/marketing-new/seo`. Each field below appears on its card within that screen; the layout is on [[marketing-seo-overview-layout]].

## What the merchant can do here

Use this table to look up any control's stored setting key, default, and validation before changing it — useful when debugging a rejected save or an unexpected default.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Canonical tag** (switch) | Toggle `setting('canonical_is_active')`. When ON, every storefront page renders `<link rel="canonical" href="…">` for itself. | ON (`1`) | Inline save on toggle (`POST /admin/api/core/seo/settings/canonical-activity/{0\|1}`). On success a toast reads "Canonical tag status changed successfully". See [[marketing-seo-canonical]]. |
| **Deindex Filtered and Sorted pages** (switch) | Toggle `setting('allow_noindex_query_limit')`. When ON, list/category/vendor/search pages with query parameters get `<meta name="robots" content="noindex">` past the configured threshold. | OFF (`0`) | When OFF, the threshold field is disabled. See [[marketing-seo-deindex]]. |
| **Parameter value** (number input — only enabled when the switch above is ON) | The max number of "meaningful" query parameters allowed before noindex kicks in. `page`, `per_page`, empty `query`, and all `utm_*` params are excluded from the count. | `0` | `int, min:0, max:5`. Error messages: "Minimum value is 0", "Maximum value is 5". Validation server-side: `required_with:allow_noindex_query_limit`. Save button only enables after change; reverts via the Revert button. |
| **Title** (text input under "Text to add pagination to meta title and description") | Stored as `setting('meta_page')`. The literal word prepended on page 2+ of paginated lists: "Page 2 — Original Title". Used with the self-canonical strategy to avoid duplicate-content penalties on paginated category / vendor lists. | `Page` | `required`. Server returns "Meta page is required" if empty. Per-language — set the word to match the storefront language (e.g., `Страница` for Bulgarian). See [[marketing-seo-meta-title]]. |
| **Sitemap URL** (read-only display + copy button) | Direct link to the auto-generated `sitemap.xml` for the store's primary domain. | `<primary scheme>://<primary host>/sitemap.xml` | Click the row to copy to clipboard; toast reads "Copied to clipboard". The sitemap itself is generated on demand by the storefront and is NOT regenerated from this admin page. See [[marketing-seo-sitemap]]. |
| **Robots.txt body** (textarea, 3 rows) | The literal text content the storefront serves at `/robots.txt`. Stored as `setting('robots.txt')` plus an `update_robots` timestamp. | A default platform robots.txt | No client-side validation — anything the merchant types is accepted. Save shows the confirm modal "Are you sure?" with body "There is a possibility that you will break your site by changing the contents of this file." with primary "OK" button. The platform always appends checkout/cart/wishlist Disallow lines + `Crawl-Delay: 3`. See [[marketing-seo-robots]]. |
| **Share product** (switch) | Master enable for the AddThis-style social sharing toolbar on product detail pages. | OFF | Stored as `module.enabled`. Sub-controls below only matter when ON. See [[marketing-seo-sharing]]. |
| **Show share count** (switch) | Toggle social counters next to share buttons. | `no` | true/false stored as `yes` / `no`. |
| **Show button for other social networks** (switch) | Display the "+" button that exposes additional sharing networks. | `no` | Stored as `module.show_compact`. |
| **Show top networks** (switch) | Show the curated top-network shortcut buttons. | `no` | Stored as `module.show_top_services`. |
| **UI click** (switch) | Trigger sharing on click (vs hover). | `no` | Stored as `module.ui_click`. |
| **Format** (select — Large / Small / Custom) | The visual style of the sharing toolbar. **Custom** unlocks a free-form HTML field. | `Large` | When `custom` is selected, a "Toolbar code" textarea slides down where the merchant can paste arbitrary HTML/JS for the toolbar. |
| **Dropdown direction** (select — Down / Up) | Direction the "more networks" dropdown opens from the share button. | `Down` | Stored as `module.ui_hover_direction` (`1` = Up, `-1` = Down). |
| **Main sharing picture** (image upload module) | Default Open Graph image (`og:image`) used when no product- or page-specific OG image is set. Stored as `setting('og_image_url')`. | empty | Selected via the standard Filemanager image picker. Shown as a 160×100 px thumbnail. Trash icon clears, rotate icon reopens the picker. |
| **Number of products to display in the RSS file** (number input) | `setting('rss_feed_count')` — how many newest products are listed in the auto-generated RSS feed. | `20` | `int, min:1, max:100, required`. Errors: "Minimum value is 1", "Maximum value is 100", "rss_feed_count is required". See [[marketing-seo-rss]]. |
| **Path for the RSS Feed** (read-only display + copy button) | The full storefront URL of the RSS feed. | derived from primary domain | Click to copy — toast "Copied to clipboard". |

## Business rules

- **Validation severity varies by card.** Most numeric fields are clamped server-side (`noindex_query_limit` 0-5, `rss_feed_count` 1-100). The Robots.txt body is the exception: it has **no** server-side validation at all — the confirm modal is the only safety net. See [[marketing-seo-robots]].
- **A blank value is not always "off".** The pagination `Title` field is `required` (blank is rejected), whereas the OG image and per-product threshold accept blank as "unset".
- **Defaults are applied at render, not stored.** A corrupt `noindex_query_limit` (non-numeric or out of 0-5) is treated as `1` on the storefront — see [[marketing-seo-deindex]].

## Related

- [[marketing-seo]] — hub.
- [[marketing-seo-canonical]] — Canonical tag card.
- [[marketing-seo-deindex]] — Deindex filtered/sorted card.
- [[marketing-seo-meta-title]] — Pagination word card.
- [[marketing-seo-sitemap]] — Sitemap.xml card.
- [[marketing-seo-robots]] — Robots.txt card.
- [[marketing-seo-sharing]] — Social-share + OG image card.
- [[marketing-seo-rss]] — RSS feed card.

## Open questions

None.
