---
type: concept
nav_path: "Concept → SEO handling → Sharing card and RSS feed"
aliases: ["Open Graph image", "og:image", "Sharing module", "AddThis", "RSS feed", "Product feed", "Skroutz feed", "Pricerunner feed", "Sharing card"]
tags: [seo, open-graph, sharing, rss, feed, social, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, canonical / noindex, meta tags, redirects, plan overrides, route catalog).

# SEO — sharing card (Open Graph) and RSS feed

## Definition

Two unrelated SEO surfaces share this aspect because both came out of the same legacy era and both have one detail that confuses merchants:

- **Sharing card on [[marketing-seo-sharing]]** — historically configured an AddThis-style social-sharing toolbar on product detail pages. **AddThis shut down in May 2023.** Every modern theme (echappe / flair / patriciarado families) ships with the toolbar render hard-disabled. The only field on this card that still matters is the **Main sharing picture** — the default `og:image`.
- **RSS feed at `<primary-host>/feed`** — a public RSS 2.0 feed containing **only products**, ordered by product ID descending (newest created first), limited to `rss_feed_count` (1-100, default 20). **No cache layer** — every request hits the DB.

The sharing card also POSTs to a **legacy route** that the rest of [[marketing-seo]] no longer uses — see Contrasts.

## Scope

Covered:

- The dead AddThis module + the practical "only `og:image` matters" guidance.
- Open Graph tags emitted by the storefront: `og:image`, `og:title`, `og:description`.
- The RSS feed: products-only, no cache, ordering, item body, channel title source.
- The 300-char-truncated description + embedded store contact / social block in each RSS item (verify).
- Sharing-card route divergence: every other card on [[marketing-seo]] posts to `/admin/api/core/seo/settings/*`; the sharing card posts to **`/admin/marketing/seo/add-this`** (legacy sitecp router) (verify).
- RSS URL host derived from primary domain — re-paste required if the merchant changes primary domain.

Not covered here:

- The admin UI of the sharing card → [[marketing-seo-sharing]].
- The RSS admin card → [[marketing-seo-rss]].
- Google Shopping / Skroutz / Pricerunner FULL product feeds (the storefront's `/feed` is a coarse fallback only) — a dedicated Product Feed app is required for full Google Shopping support.
- Per-entity OG image overrides → [[seo-meta-tags]] + the entity editors.

## Contrasts

- **Sharing module vs. Open Graph image** — same admin card, very different outcomes. The module (AddThis-style) is dead UX on every modern theme since AddThis shut down in May 2023. The `og:image` is the default Open Graph image used by Facebook / LinkedIn / Viber for link previews — the only field on that card that still has merchant impact. Practical guidance: ignore every module toggle on the sharing card, upload the og:image (1200 × 630 px recommended by Facebook), click Save.
- **Sharing card POSTs to LEGACY route** — every other card on the Main SEO page posts to `/admin/api/core/seo/settings/*` (new Core/Core API), but the Sharing card posts to `/admin/marketing/seo/add-this` (legacy sitecp router). The Core/Core admin API does not expose an `add-this` endpoint at all (verify).
- **Sitemap.xml vs. RSS feed** — sitemap is the "here are my indexable URLs" catalog for crawlers ([[seo-sitemap-robots]]). RSS is a third-party product feed (Pricerunner, Skroutz, "RSS-to-email" automations) — NOT a search-engine submission. The merchant should submit sitemap to Google Search Console; submit RSS to Skroutz / Mailchimp / blog readers.
- **`/feed` RSS vs. full Google Shopping feed** — the storefront's `/feed` is a coarse fallback. Google Shopping (older Merchant Center setups) accepts it, but modern Merchant Center requires the structured Product Feed app.

## Where it applies

### Sharing module — dead UX on every modern theme

[[marketing-seo-sharing]] historically configured an AddThis-style social-sharing toolbar on product detail pages. AddThis shut down in **May 2023**. Every modern storefront theme (echappe family, flair family, patriciarado) ships with the toolbar render hard-disabled — so toggling "Share product", choosing Format, picking which networks show, etc. has **no visible effect on the storefront** for any modern theme.

The only field that still matters on this card is the **Main sharing picture** — the default `og:image` URL. The storefront uses this image when a page being shared (home, contacts, generic CMS page, brand index, blog index, or any entity whose own OG image is blank) needs an Open Graph cover image. Facebook recommends **1200 × 630 px**.

Practical guidance: ignore every module toggle on the sharing card, upload the og:image, click Save.

### Sharing card legacy POST route

Every other card on [[marketing-seo]] posts to `/admin/api/core/seo/settings/*` (new Core/Core API). The Sharing card alone posts to **`/admin/marketing/seo/add-this`** (legacy sitecp router). The Core/Core admin API does not expose an `add-this` endpoint at all (verify). Merchants who proxy admin traffic via custom infra need to allow both endpoints, not just the Core API.

### Open Graph tags emitted by the storefront

- `<meta property="og:image">` — falls back to the Main sharing picture on [[marketing-seo-sharing]] if per-entity OG image is blank.
- `<meta property="og:title">` — per-entity override → per-section meta → language file (see [[seo-meta-tags]]).
- `<meta property="og:description">` — same fallback chain.

These tags are emitted on every indexable page; they're not gated by the dead AddThis module toggles.

### RSS feed — products-only, no cache, newest-first

The storefront serves a public RSS 2.0 feed at `<primary-host>/feed`. The feed contains **only products**, ordered by product ID descending (newest created first), limited to `rss_feed_count` (1-100, default 20). Each `<item>` carries:

- title
- image
- HTML description with embedded image, 300-char-truncated description, price (verify)
- link
- guid
- category breadcrumb
- a separate block with the store's contact details (address / phone / city / postal code / country) and social-media links (verify)

The feed has **NO cache layer** — every request runs a fresh DB query.

Used by:

- Google Shopping (older Merchant Center setups).
- Skroutz / Pricerunner / EU comparison engines.
- Mailchimp / Sendinblue / Brevo "RSS-to-email" automations.
- The merchant's own blog / news site.

The feed URL is derived from the **primary domain** ([[settings-domains]]) — if the merchant changes their primary domain, the feed URL changes and the merchant has to re-paste the new URL into every third party that subscribed.

The feed channel `<title>` is the store's `site_name` setting ([[settings-general]]). No per-product field control, no order option, no filter — the merchant cannot exclude products from the feed beyond the platform's `visible` filter.

## Related

- [[seo-handling]] — hub.
- [[seo-meta-tags]] — the `og:title` / `og:description` fallback chain that runs alongside `og:image`.
- [[seo-sitemap-robots]] — sitemap.xml as the canonical search-engine submission (RSS is for product feeds, not crawlers).
- [[marketing-seo-sharing]] — admin card for sharing module + og:image (6th card on [[marketing-seo]]).
- [[marketing-seo-rss]] — admin card for RSS feed count + URL (7th card).
- [[marketing-seo]] — Main SEO settings hub.
- [[settings-domains]] — primary domain determines the RSS feed URL host.
- [[settings-general]] — `site_name` becomes the RSS feed's channel `<title>`.
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] — per-entity OG image overrides.

## Open Questions

None.
