---
type: feature
nav_path: "Marketing → SEO → Sitemap"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Sitemap", "Sitemap.xml", "XML sitemap", "Site map", "Карта на сайта", "Сайтмап", "XML карта"]
tags: [marketing, seo, sitemap, crawl-directives]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---
# Sitemap.xml (auto-generated XML sitemap)

## Purpose

The Sitemap card on [[marketing-seo]] is a **read-only display** of the storefront's auto-generated `sitemap.xml` URL plus a one-click "copy to clipboard" control. The XML sitemap is a machine-readable roadmap of every public URL on the storefront — products, categories, vendors, CMS pages, blogs, blog articles — that the merchant pastes into Google Search Console, Bing Webmaster Tools, and similar tools so crawlers can discover the whole catalog without crawling the site link-by-link.

The card does NOT let the merchant edit, regenerate, or filter the sitemap — it only exposes the URL. The sitemap content is generated dynamically by the storefront and refreshed automatically; there is no manual "rebuild" button and no per-entity inclusion toggle.

## Where to find it

Sidebar → Marketing → **SEO** → Main SEO settings → the **Sitemap.xml file** card (the fourth card on the page, between **Pagination word in meta** and **Robots.txt**).

The card sits on the new Vue page. A `marketing-seo-main=old` cookie falls back to the legacy `/admin/marketing/seo` page.

## What the merchant can do here

- Read the full storefront URL where the sitemap is served — formatted as `<scheme>://<primary host>/sitemap.xml`.
- Click the row (or the clipboard icon next to it) to copy the URL to the clipboard. A green toast reads **"Copied to clipboard"**.
- Paste the URL into Google Search Console / Bing Webmaster Tools / any external crawler tool that accepts an XML sitemap URL.

### What the merchant CANNOT do here

- **Edit the URL** — it is derived from the store's **primary domain** and the `/sitemap.xml` path is fixed. To change the displayed host, change the primary domain in [[settings-domains]].
- **Edit the content** — which entities are listed, the `<changefreq>` / `<priority>` per URL, or how URLs are grouped. Inclusion rules are platform-level, not per-store editable.
- **Turn entity types on / off** (e.g. "don't include blog articles"). There is no per-entity toggle.
- **Trigger a manual rebuild** — the sitemap is generated on demand with a cache layer in between (see Business rules).
- **Add custom URLs** — a hand-built landing page outside CloudCart would need a separate sitemap and index, not configurable here.
- See the last-generated timestamp or URL count; set up automatic ping to Google / Bing. None of these exist on the card.

## Settings & fields

The card renders just two elements — a one-line description and the clickable URL row.

| Control | What it does | Default | Validation / notes |
|---------|--------------|---------|--------------------|
| Description line | Static text: "This is the direct link to sitemap.xml". | n/a | Plain copy — not editable. |
| **Sitemap URL** (clickable row with clone icon) | Displays `<scheme>://<primary host>/sitemap.xml`. Clicking anywhere on the row copies the URL to the browser clipboard. | derived from primary domain | Read-only. On copy, a green toast reads "Copied to clipboard". |

There is no Save button — the URL is read-only display data returned by the SEO settings API that powers the whole SEO main page.

## Business rules

### How the URL is built

The displayed URL is composed at page-load time from the store's **primary domain** plus the constant path `/sitemap.xml`, giving `https://<primary host>/sitemap.xml` (or `http://` if the primary domain has no SSL). Changing the primary domain in [[settings-domains]] updates the displayed host on the next page-load.

### What's in the sitemap

When a crawler fetches `/sitemap.xml`, the storefront returns a **sitemap index** that points to per-entity sub-sitemaps, served at `/sitemap/<entity>/<page>.xml` (and `.xml.gz`). The currently-enabled entity types are:

- **vendor** — all vendor / brand pages.
- **category** — all category pages.
- **product** — products visible on the storefront (the product image is embedded — see image sitemaps below).
- **page** — CMS pages visible on the storefront.
- **blog** — blogs with at least one active article.
- **article** — blog articles visible on the storefront.

Plus a **boilerplate** sub-sitemap for static landing pages: the contacts page (`/contacts`), the vendors index (`/vendors`), and the blog list page.

The merchant cannot toggle entity types from the admin. Several others (`blog_tags`, `product_selection`, `product_tags`, `category_properties`, `shops`) exist but are disabled platform-wide.

### Pagination — large catalogs split into multiple files

The XML sitemap protocol caps each file at 50,000 URLs / 50 MB. The live storefront splits each entity set at **1,000 URLs per file**, so a 60,000-product store produces `/sitemap/product/1.xml` through `/sitemap/product/60.xml`, all listed in the master `sitemap.xml`. Splitting happens automatically at request time — the merchant does nothing.

### `<changefreq>`, `<priority>`, `<lastmod>`

Products / categories / vendors / pages / articles are tagged `changefreq=daily`; boilerplate URLs get `changefreq=monthly`. `<priority>` is omitted entirely (no per-entity override). `<lastmod>` comes from the entity's last-update timestamp; entities without one report the current time, so they always look "freshly modified" to crawlers.

### Image sitemap support

Products include an `<image:image>` block with the product's 600×600 image URL, under the `xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"` namespace, for Google Images discovery.

### Caching — fresh within ~1 hour

Each sub-sitemap is **cached for 1 hour** per entity + page. The cache is not invalidated when products are created or edited — it only expires on time, so a new product can take up to an hour to appear. The HTTP response is served with `Cache-Control: no-store, no-cache, must-revalidate` (plus a past-dated `Expires` header) so browser / proxy caches don't extend staleness beyond the 1-hour TTL. Content type is `application/xml; charset=utf-8`.

### Compressed variant — `.gz` files

The storefront serves both `sitemap.xml` and `sitemap.xml.gz` (gzip-compressed, ~10× smaller transfer). Google Search Console fetches the `.gz` variant by default for large sitemaps; the merchant can submit either URL. The legacy `/sitemap.php` path 301-redirects to `/sitemap.xml.gz`.

### noindex URLs are excluded

URLs the storefront marks `noindex` — via [[marketing-seo-deindex]] or system pages like cart / checkout / account — are **NOT** listed; the sitemap exposes indexable URLs only. So if the merchant noindexes filtered category pages, those variants don't appear.

### Trial / expired stores

Stores on `trial` / `cc-demo` / `plan_expired` plans still serve a working `sitemap.xml`. Their robots.txt blocks the whole site (`Disallow: /`) so Google won't crawl it, but the URL is live and previewable.

### Permission

The sitemap URL is part of the SEO settings response (`GET /admin/api/core/seo/settings`), guarded by the **marketing.seo** permission — the merchant needs it to open the SEO page at all. The storefront `/sitemap.xml` endpoint itself is public; anyone (Google's crawler, the merchant, a competitor) can fetch it.

### Plan gates

None — included with every plan, including trial.

## Related

- [[marketing-seo]] — Main SEO settings hub (this card lives here).
- [[marketing-seo-robots]] — robots.txt editor; the sitemap URL should be referenced from robots.txt for crawler discovery (pasted in manually).
- [[marketing-seo-canonical]] — canonical tag toggle; the sitemap should list canonical URLs.
- [[marketing-seo-deindex]] — noindex on filtered/sorted pages; noindexed URLs are excluded from the sitemap.
- [[marketing-seo-meta]] — per-section meta titles & descriptions (listed for SEO context).
- [[marketing-seo-301-redirects]] — 301 redirects; the target should match the sitemap-listed URL to avoid wasted crawl budget.
- [[settings-domains]] — primary domain determines the host portion of the sitemap URL.
- [[apps-google-search-console]] — submitting the sitemap to Google (where the merchant pastes this URL).

## Open questions

- ⏸️ **1-hour cache TTL on new products.** Newly created products take up to an hour to appear in the sitemap (passive expiration only).
