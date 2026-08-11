---
type: feature
nav_path: "Marketing → SEO → Deindex Filtered and Sorted pages"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Deindex filtered pages", "Noindex query limit", "Filtered & sorted noindex", "noindex meta tag", "Деиндексиране", "Деиндексирай филтрираните страници"]
tags: [marketing, seo, deindex, noindex, indexing]
plan_gates: []
created: 2026-05-23
updated: 2026-05-27
source_count: 4
---
# Deindex Filtered and Sorted pages (noindex meta tag for parameterized URLs)

## Purpose

The Deindex card is the second setting on [[marketing-seo]]. It blocks Google (and other crawlers) from indexing **category, vendor, search, tag, and showcase pages** when those pages have **more than N "meaningful" query parameters** in the URL — typically pages produced by stacking filters and sort orders.

Why this matters: a category like `/category/shoes` is one URL, but with filters it spawns hundreds of variants — `?color=red&size=42&brand=nike&sort=price` and so on. Each is the same listing in a different order or subset. Google indexes them all, flags the site for thin / duplicate content, and wastes crawl budget on combinations nobody searches for. The card lets the merchant say "anything past 2 active filters is noindex" — so the bare category and the most useful low-filter variants stay indexed, while the rest are hidden from search but still navigable for customers.

It pairs with [[marketing-seo-canonical]]: canonical keeps similar-but-not-duplicate pages from competing; noindex hides truly redundant variants. Most stores use both.

## Where to find it

Sidebar → Marketing → SEO → **Main SEO settings** → the second card, labelled **Deindex Filtered and Sorted pages**.

## What the merchant can do here

- Toggle deindexing of parameterized list pages on or off store-wide.
- Set the threshold — how many meaningful query parameters a URL can have before the page is marked `noindex`.

### What the merchant CANNOT do here

- Block individual URLs from indexing (use [[marketing-seo-301-redirects]] or robots.txt on [[marketing-seo]] for that).
- Choose WHICH parameters count — the exclusion list is fixed (`page`, `per_page`, empty `query`, all `utm_*` are always excluded — see Business rules).
- Set different thresholds per route — one global threshold applies to all affected routes.
- Set the threshold higher than 5 — the cap is hard-coded.
- Deindex search results independently — they follow the same global rule.
- Add a noindex tag to checkout / cart / account pages — those are ALWAYS noindexed regardless of this setting.

## Settings & fields

Two controls — a master switch and a numeric threshold. The threshold is greyed out until the switch is ON.

| Control | What it does | Default | Validation / notes |
|---------|--------------|---------|--------------------|
| **Deindex Filtered and Sorted pages** (switch) | Sets `allow_noindex_query_limit`. When ON, list pages with more than the threshold's worth of meaningful query parameters get `<meta name="robots" content="noindex">`. | OFF (`0`) | When OFF, the threshold field is disabled. |
| **Parameter value** (number input — enabled only when the switch is ON) | Max meaningful query parameters allowed before noindex kicks in. `0` = noindex as soon as ANY meaningful parameter is present. `5` = up to 5 stacked filters stay indexed. | `0` | `int, min:0, max:5`. Error messages: "Minimum value is 0", "Maximum value is 5". |

Saving sends both values together via the shared SEO action bar. On success the toast reads **"Saved Successfully"**.

## Business rules

### Which routes get the noindex tag

Only these storefront routes have their parameter count evaluated:

- Category view (`category.view`)
- Products listing (`products.list`)
- Curated product list ("Selection") (`selection`)
- Vendor view (`site.vendor.view`)
- Product search results (`products.search`)
- Showcase listing (`showcase.list`)
- Tag pages (`site.tag`)
- Bundles listing — flat list and per-category (`bundles.list.list`, `bundles.list.category`)

All other storefront routes are evaluated by other rules:

- **Always noindex regardless of this setting**: checkout (`checkout`, `checkout.*`), cart sub-pages (`cart.*`), compare, the entire customer-account area (`site.account`, `site.account.*`), the storefront auth pages (`site.auth.*`), and vendor-contact sub-URLs (`/contacts/<vendor>`).
- **Product / CMS-page / Home / Blog / Contacts**: governed by per-page noindex flags on the entity itself, not by this setting.
- **`ajax.*` routes never get robots meta** — explicitly opted out of robot directives.

This card cannot force-noindex a parameter-free URL (e.g. `/category/test` with no query). To noindex a specific entity-driven URL, use the per-entity `no_index_meta` toggle (where exposed) or robots.txt.

### How "meaningful parameters" are counted

The threshold count includes every query parameter EXCEPT:

- `page` and `per_page` — always excluded (pagination is governed by canonical, not noindex).
- `query` when its value is empty — so `?query=` doesn't trigger noindex on its own.
- Any parameter whose name starts with `utm_` (case-insensitive: `utm_source`, `utm_campaign`, etc.) — keeping marketing-tracked URLs indexable.

Every other parameter — `filter`, `sort`, `color`, `size`, `brand`, custom property filters — counts. **Multi-value parameters split**: `?color=red,blue,green` counts as 3, not 1 (useful when a merchant says "I set threshold = 2 but the page is still noindex").

### Threshold behaviour

The check is `> threshold` (strictly greater), so threshold = 2 means 2 parameters stay indexed and the 3rd triggers noindex.

| Threshold | What happens on a category page |
|-----------|--------------------------------|
| `0` (switch ON, value 0) | Any meaningful parameter triggers noindex. Only the bare `/category/shoes` is indexed. |
| `1` | `?color=red` is indexed; `?color=red&size=42` is noindex. |
| `2` | `?color=red&size=42` is indexed; adding a 3rd is noindex. |
| `5` (max) | Up to 5 stacked filters are indexed; the 6th triggers noindex. |
| Switch OFF | No noindex applied for parameter count — every combination is indexable. |

### Interaction with canonical (key)

When a URL exceeds the threshold and gets noindex, the canonical tag is **also suppressed** — the page is `noindex, nofollow` with no canonical. This is intentional: Google should not see a canonical for a page hidden from search.

Below the threshold (indexable), the canonical keeps only the first N meaningful parameters (in order) and strips the rest — normalizing filter order so `?color=red&size=42` doesn't compete with `?size=42&color=red`. Because it takes the first N in order, filter ORDER affects which parameters land in the kept canonical.

### Defensive defaults

- A corrupt `noindex_query_limit` (non-numeric or outside 0-5 — e.g. a direct DB edit to `99`) is clamped to `1` at render time, not to the max.
- If the storefront cannot determine the active route (rare fallback), it treats the page as noindex. The merchant cannot trigger this directly.

### Demo store override

Stores on the `cc-demo` plan always render `noindex, nofollow` on every page regardless of this setting.

### Permission & plan gates

Saving requires the `marketing.seo` permission. No plan gate — included with every plan.

## Related

- [[marketing-seo]] — Main SEO settings hub (this card lives here).
- [[marketing-seo-canonical]] — the canonical tag setting; works together with this card (canonical keeps near-duplicates from competing, noindex hides truly redundant variants).
- [[marketing-seo-meta-title]] — pagination word prepended to meta on page 2+; an indexable paginated page still gets a unique meta thanks to this.
- [[marketing-seo-meta]] — per-section meta titles and descriptions.
- [[marketing-seo-301-redirects]] — per-URL 301 redirects (different from noindex; redirect MOVES a URL, noindex just HIDES it).
- [[product]] — per-product meta tags (the product detail page is not affected by the threshold here).
- [[category]] — category list pages are the main beneficiaries of this rule.

## Open questions

No outstanding questions.
