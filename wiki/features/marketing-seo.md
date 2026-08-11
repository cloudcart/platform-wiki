---
type: feature
nav_path: "Marketing → Seo"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Main SEO settings", "SEO settings", "SEO", "Marketing SEO", "Главни SEO настройки", "СЕО", "Сео настройки"]
tags: [marketing, seo, sitemap, robots, canonical, rss, sharing]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 14
---
# Main SEO settings

## Purpose

The Main SEO screen is where the merchant controls the storefront-wide search-engine signals — the **canonical tag** strategy, the **noindex rule** for filter/sort query parameters, the **pagination word** added to repeated meta titles, the **robots.txt** content, the **sitemap.xml** location, the **social-share module** for product pages (including the default Open Graph image), and the **RSS feed** size. These are the platform-wide knobs that determine how Google, Bing, Facebook, and other crawlers see the storefront.

This is a **hub page**. The screen is laid out as seven self-contained cards, and each card has its own deep-dive page (see [[marketing-seo-canonical]], [[marketing-seo-deindex]], [[marketing-seo-meta-title]], [[marketing-seo-sitemap]], [[marketing-seo-robots]], [[marketing-seo-sharing]], [[marketing-seo-rss]]). The page-level mechanics that span every card — layout, the per-card save model, the full field reference, the save endpoints, and the trial-store crawl block — are split into the `marketing-seo-overview-*` aspects listed below.

This page does NOT contain per-page meta titles/descriptions for specific sections like Home / Products / Blog — those live on [[marketing-seo-meta]]. It also doesn't contain per-URL 301 redirects — those live on [[marketing-seo-301-redirects]]. For AI-generated content variations of product / category descriptions, see [[apps-seo-spinner]] (a separate paid app).

## Sub-pages (in this cluster)

Page-level aspects (cross-cutting, NOT per-card) — drill into the one that matches the question:

- [[marketing-seo-overview-layout]] — where to find the screen, the seven-card layout, the legacy escape-hatch cookie, and what the merchant can / cannot do here.
- [[marketing-seo-overview-card-save]] — the independent per-card Save / Revert model, dirty detection, the Robots confirm modal, and the Canonical instant-save exception.
- [[marketing-seo-overview-settings-map]] — the complete field-by-field reference table (every control, default, and validation rule) across all seven cards.
- [[marketing-seo-overview-save-endpoints]] — the per-card save routes, the single on-mount load, and the one card that posts to the legacy route.
- [[marketing-seo-overview-trial-block]] — why trial / expired / development / demo stores are forced to `Disallow: /` (or noindex meta) regardless of what the merchant types.

Per-card deep dives (one card = one page):

- [[marketing-seo-canonical]] — the `<link rel="canonical">` store-wide switch.
- [[marketing-seo-deindex]] — noindex meta for filtered / sorted pages past a parameter threshold.
- [[marketing-seo-meta-title]] — the pagination word prepended to meta titles on page 2+.
- [[marketing-seo-sitemap]] — read-only sitemap.xml URL display.
- [[marketing-seo-robots]] — the robots.txt body editor.
- [[marketing-seo-sharing]] — the social-share toolbar + default Open Graph image.
- [[marketing-seo-rss]] — the newest-products RSS feed size.

## Where to find it

Sidebar → Marketing → **SEO** (the first SEO sub-entry, labelled "Main SEO"). Route name `seo-main`, path `/admin/marketing-new/seo`. The page header shows the Searchengin brand icon (`fa-brands fa-searchengin`) and the title "Main SEO settings". Breadcrumb reads "Marketing → SEO settings". The page is the new Vue rewrite of the legacy `/admin/marketing/seo` Smarty page; full navigation + the escape-hatch cookie are on [[marketing-seo-overview-layout]].

## What the merchant can do here

The screen pairs an info column with a setting column in each of seven cards, each saving independently. Briefly, the merchant can:

- Toggle the **Canonical tag** store-wide — see [[marketing-seo-canonical]].
- **Deindex filtered & sorted pages** past a parameter-count threshold — see [[marketing-seo-deindex]].
- Set the **pagination word** prepended to repeated meta titles — see [[marketing-seo-meta-title]].
- Copy the read-only **sitemap.xml** URL — see [[marketing-seo-sitemap]].
- Edit the **robots.txt** body — see [[marketing-seo-robots]].
- Configure the **product social-share** toolbar + default Open Graph image — see [[marketing-seo-sharing]].
- Set the **RSS feed** product count and copy the feed URL — see [[marketing-seo-rss]].

What the merchant **cannot** do here: per-page meta titles/descriptions per section ([[marketing-seo-meta]]), per-URL 301 redirects ([[marketing-seo-301-redirects]]), per-product meta overrides (on [[product]]), per-category meta overrides (on [[category]]), domain-level redirects ([[apps-domain-redirect]]), or editing the sitemap content. Full breakdown on [[marketing-seo-overview-layout]].

## Settings & fields

There are seven cards, each with its own controls. The complete field-by-field reference (every control, default, and validation message across all cards) lives on [[marketing-seo-overview-settings-map]]; per-card behaviour lives on each card's deep-dive page (see Sub-pages above).

## Business rules

The page-level rules that apply to the screen as a whole:

- **Each card saves independently** — there is no global "save all" button; the Canonical card is an instant-save exception. See [[marketing-seo-overview-card-save]].
- **Every card posts to its own endpoint**, and one card (Sharing) hits a legacy route. See [[marketing-seo-overview-save-endpoints]].
- **Trial / expired / development / demo stores are crawl-blocked** regardless of the robots.txt text the merchant saves — the single biggest source of "why isn't my new store on Google?" tickets. See [[marketing-seo-overview-trial-block]].
- **Permission** — the underlying API endpoints (`/admin/api/core/seo/settings/*`, `/admin/api/core/seo/meta/*`, `/admin/api/core/seo/redirects/*`) sit behind the `marketing.seo` permission.
- **Plan gates** — none on the screen itself; trial / expired stores are still allowed in to configure robots/sitemap, but the storefront crawl-blocks them (see the trial-block aspect).

Card-specific business rules (how canonical actually renders, how the noindex threshold counts parameters, what robots.txt appends, etc.) live on each card's deep-dive page.

## Related

- [[marketing]] — parent navigation hub.
- [[seo-handling]] — the platform-wide SEO concept (canonical / noindex / meta / sitemap / redirects) this screen configures.
- [[marketing-seo-overview-layout]] — page layout + navigation aspect.
- [[marketing-seo-overview-card-save]] — per-card save model aspect.
- [[marketing-seo-overview-settings-map]] — full field reference aspect.
- [[marketing-seo-overview-save-endpoints]] — save endpoints aspect.
- [[marketing-seo-overview-trial-block]] — trial-store crawl block aspect.
- [[marketing-seo-canonical]] — Canonical tag card.
- [[marketing-seo-deindex]] — Deindex filtered/sorted card.
- [[marketing-seo-meta-title]] — Pagination word card.
- [[marketing-seo-sitemap]] — Sitemap.xml card.
- [[marketing-seo-robots]] — Robots.txt card.
- [[marketing-seo-sharing]] — Social-share + OG image card.
- [[marketing-seo-rss]] — RSS feed card.
- [[marketing-seo-meta]] — per-section meta titles & descriptions.
- [[marketing-seo-301-redirects]] — per-URL 301 redirects manager.
- [[apps-seo-spinner]] — AI content-variation generator for descriptions + meta.
- [[apps-domain-redirect]] — whole-domain (cross-domain) 301 redirects.
- [[product]] — per-product meta-tag overrides.
- [[category]] — per-category meta-tag overrides.
- [[settings-domains]] — primary domain affects sitemap / RSS / canonical URL host.
- [[apps-google-analytics]] / [[apps-google-tags]] — third-party tracking pasted into theme settings, not here.

## Open questions

- 📡 **Trial-store auto-block.** Plan upgrade flips the crawl response back automatically — no manual merchant intervention — and it isn't surfaced in merchant-facing help. See [[marketing-seo-overview-trial-block]].
