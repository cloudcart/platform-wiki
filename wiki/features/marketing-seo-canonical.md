---
type: feature
nav_path: "Marketing → SEO → Canonical tag"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Canonical tag", "Canonical URL", "rel canonical", "Self-canonical", "Каноничен таг", "Каноничен URL"]
tags: [marketing, seo, canonical, indexing]
plan_gates: []
created: 2026-05-23
updated: 2026-05-27
source_count: 5
---
# Canonical tag (storefront `<link rel="canonical">`)

## Purpose

The Canonical tag card is the first setting on [[marketing-seo]]. It is a single store-wide switch that controls whether every storefront page renders a `<link rel="canonical" href="…">` tag inside its `<head>`. The canonical tag tells Google "this URL is the master copy of this page" — so if the same content is reachable via several URLs (filters, sort orders, tracking parameters, paginated lists), Google merges them and credits the master URL with all the ranking signals. Without it, the same product or category page can compete with itself across dozens of URL variants and dilute its ranking.

Most stores should leave this ON. The switch exists mainly to let merchants whose custom theme already injects its own canonical tag avoid double-tagging.

## Where to find it

Sidebar → Marketing → SEO → **Main SEO settings** → the first card on the page, labelled **Canonical tag**. The card sits at the top because it is the most consequential SEO toggle on the page.

## What the merchant can do here

- Toggle the canonical tag on or off store-wide using a single switch.
- See the change reflected immediately — the switch saves on toggle (no Save / Revert buttons on this card).

### What the merchant CANNOT do here

- Set a canonical URL for a specific page from this card. Per-page overrides live on the CMS Page editor (Pages admin) and the Curated product list ("Selection") editor — see Business rules.
- Choose which URL the canonical points to, or strip query parameters selectively. The builder is fixed: it always self-references the current URL (query params stripped, `?page=N` re-added on paginated lists). For actual 301 redirects see [[marketing-seo-301-redirects]].
- Add `og:url`, `hreflang`, or alternate-language canonical tags — those are handled separately by the storefront theme.
- Turn canonical off for only one route (e.g., search results). The switch is global.

## Settings & fields

The card renders one control — a switch labelled "Canonical tag".

| Control | What it does | Default | Validation / notes |
|---------|--------------|---------|--------------------|
| **Canonical tag** (switch) | Toggle `setting('canonical_is_active')`. When ON, every storefront page renders `<link rel="canonical" href="…">` for itself. | ON (`1`) | Inline save on toggle — no Save / Revert buttons. The switch values are the string `"1"` (ON) and `"0"` (OFF). On success a toast reads **"Canonical tag status changed successfully"**. |

## Business rules

### What the storefront renders when canonical is ON

When `canonical_is_active = 1`:

- Every storefront page emits `<link rel="canonical" href="<current URL>">` in the `<head>` pointing to itself (the "self-canonical" pattern). The host portion comes from the store's primary domain — see [[settings-domains]].
- **Paginated lists**: query parameters are stripped from the canonical and `?page=N` is re-added. So `/category/shoes?filter=red&sort=price&page=3` canonicalizes to `/category/shoes?page=3`. This is the **self-canonical-per-page** strategy — page 2 says "I am page 2", page 3 says "I am page 3", so each paginated page is indexed on its own without competing with page 1.
- **Indexable category / vendor / search pages** with `?filter=…` or `?sort=…` query parameters canonicalize to the **same URL plus the kept query params** (subject to the noindex threshold — see [[marketing-seo-deindex]]). The first few "meaningful" parameters are kept in the canonical; the rest are stripped and the page is marked noindex. This applies on the filter-eligible routes: `category.view`, `products.list`, `selection`, `site.vendor.view`, `site.tag`, `products.search`, `showcase.list`, `bundles.list.list`, `bundles.list.category`.
- **CMS Page canonical override**: if the merchant set a custom canonical URL on a specific CMS page (via the Pages admin editor's "Canonical URL" field), that override wins over the auto-generated value. Merchant-set paths are stored relative (e.g., `/home`); the storefront prepends scheme + host.
- **Curated product list ("Selection") canonical override**: if the merchant set a canonical URL on a curated product list, the storefront uses that.
- **Vendor-contact carve-out**: contact pages reached via a vendor sub-URL (e.g., `/contacts/some-vendor`) get a canonical override pointing to the main `contacts` route — so a vendor's contact variant doesn't compete with the store's main contacts page. This is hardcoded; there is no merchant toggle.
- **Noindexed pages get no canonical.** If a page is `noindex, nofollow` (checkout, cart, account, etc.) the storefront skips emitting a canonical so it doesn't accidentally signal that URL as the master.
- **`products.list` and `ajax.*` routes** emit no `<meta name="robots">` tag at all (neither indexable nor noindex); they silently opt out of robot directives. The canonical still emits if canonical is ON and the route is otherwise indexable.
- **No `og:url` sync**: the canonical tag does not also update `<meta property="og:url">`. Open Graph URL is rendered separately by the theme template and may diverge from the canonical (a theme bug to watch for).

### What the storefront renders when canonical is OFF

When `canonical_is_active = 0` no `<link rel="canonical">` is rendered anywhere on the storefront. The merchant's theme is then responsible for injecting one (if it injects one at all).

### Pagination word interaction

Self-canonical-per-page solves the "Google sees pages 2/3/4 as duplicates of page 1" problem, but creates a second one: each paginated page has the SAME meta title and description, which Google flags as duplicate meta. That's why the platform prepends "Page N — " to the meta title and description on page 2 and beyond, using the configurable word from [[marketing-seo-meta-title]]. The two work together: canonical makes each paginated URL self-reference; the pagination word makes its meta unique.

### Special-case: cc-demo plan

Stores on the `cc-demo` plan always render `<meta name="robots" content="noindex, nofollow">` regardless of any setting on this page. They still render the canonical tag if it's ON — but Google never indexes them anyway because of the noindex.

### When to turn this OFF

Almost never. Two scenarios: (1) the merchant's custom theme already injects its own `<link rel="canonical">` and the storefront would double-emit if left ON; (2) a one-off campaign/test where every URL variant should compete for ranking (very rare). If unsure, leave it ON.

### Plan gates & permission

Included with every plan; no plan gate. The toggle endpoint sits behind the `marketing.seo` API permission. The store-wide value lives in `setting('canonical_is_active')`, default `1` (ON) — so a store that has never touched the setting renders canonical tags. Toggling saves immediately via `POST /admin/api/core/seo/settings/canonical-activity/{0|1}` (value in the URL, constrained to `0` or `1`) and confirms with the toast "Canonical tag status changed successfully".

## Related

- [[marketing-seo]] — Main SEO settings hub (this card lives here).
- [[marketing-seo-deindex]] — controls the `noindex` directive on filtered/sorted pages; works hand-in-hand with canonical (canonical keeps similar-but-not-duplicate pages from competing; noindex hides truly redundant variants).
- [[marketing-seo-meta-title]] — pagination word prepended to meta title/description on paginated pages, which complements the self-canonical-per-page strategy.
- [[marketing-seo-meta]] — per-section meta titles and descriptions for Home / Contacts / Products / Vendors / Blog.
- [[marketing-seo-301-redirects]] — per-URL 301 redirects (different from canonical; a 301 changes the URL the browser sees, canonical only tells Google which URL is master).
- [[product]] — per-product meta-tag overrides (no per-product canonical override on the product editor; product pages always self-canonicalize).
- [[category]] — category pages canonicalize to their own URL with kept filter params.
- CMS Page editor — per-page canonical override field (reachable from the storefront Pages admin).
- [[settings-domains]] — the primary domain determines the host portion of every canonical URL.

## Open questions

No outstanding questions.
