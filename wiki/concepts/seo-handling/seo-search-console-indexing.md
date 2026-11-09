---
type: concept
nav_path: "Concept → SEO handling → Search Console page indexing"
aliases: ["Search Console page indexing", "Page indexing report", "Excluded by noindex tag", "Page with redirect", "Alternate page with proper canonical tag", "Blocked by robots.txt", "Not found (404)", "Blocked due to access forbidden (403)", "http to https redirect", "www redirect", "Trailing slash redirect", "Индексиране на страници", "Search Console грешки"]
tags: [seo, search-console, indexing, redirects, noindex, canonical, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[seo-handling]]. See the hub for related aspects (canonical / noindex, sitemap / robots, redirects, route catalog).

# SEO — reading Search Console's "Page indexing" report

## Definition

Google Search Console's **Page indexing** report sorts every URL Google knows into "indexed" and a list of "not indexed" reasons. Most reasons a CloudCart store shows are produced on purpose by the storefront: they keep filter, cart and duplicate addresses out of Google. This page maps each reason to the storefront behaviour that causes it, so support can tell an expected entry from one that needs action. Read from the code on `origin/master`, not run in a store.

## Scope

Covered: which storefront behaviour produces each common reason, and whether it is expected. Also the automatic redirects every store applies (scheme, host, trailing slash, renamed addresses).

Not covered: how Google decides to crawl, index or drop a URL ("Crawled / Discovered – currently not indexed" are Google's own decisions; CloudCart sends nothing that forces them), and edge (bot-protection) blocking, which is outside the store's code.

## Contrasts

- **Not indexed ≠ broken.** A URL listed as "not indexed" because of noindex, a canonical or a redirect is the platform consolidating duplicates onto one indexable URL. Only a URL that should be a live, indexable page and is not needs action.
- **Noindex vs robots.txt.** A noindex page is fetched and then left out; a robots.txt-blocked URL is never fetched. See [[seo-canonical-noindex]] and [[seo-sitemap-robots]].

## Where it applies

### Excluded by 'noindex' tag — expected

- **Filtered and sorted listings.** On category, vendor, tag, selection, search and bundles listings, any filter or sort parameter (`?order_by=`, `?brand=`, `?vendors=`, `?sale=`, `?new=`, price, variants, category properties) makes the page `noindex, follow` while the **Deindex Filtered and Sorted pages** switch is OFF, the default. With it ON, only URLs carrying more parameters than its **Parameter value** are noindex. See [[marketing-seo-deindex]].
- **`/products`** (the all-products list) always sends an `X-Robots-Tag: noindex` header.
- **Cart, checkout, account, sign-in, compare** pages and the store's **404 page** are `noindex, nofollow`.
- **Demo stores** are `noindex, nofollow` everywhere ([[seo-plan-overrides]]).

There is no per-product, per-category or per-page noindex switch in the admin.

### Alternate page with proper canonical tag — expected

The URL points its canonical at another URL, which is the one indexed:

- a filtered listing that is noindex points at the clean listing (or, with the Deindex switch ON, at the URL with the allowed parameters);
- any URL with parameters the storefront ignores (`utm_*`, `gclid`, `fbclid`, unknown ones) points at the clean URL;
- a product URL with a preselected variant in the query points at the plain product URL;
- a CMS page or selection with its own canonical set points there.

Paginated listings (`?page=2`) are self-canonical, so they are not in this group.

### Duplicate without user-selected canonical

The storefront produces this only when the **Canonical tag** card is OFF ([[marketing-seo-canonical]]). With it ON every indexable page names its canonical, so a URL listed here is Google's own choice and is checked case by case.

### Page with redirect — expected

Every store answers these with a **301**, keeping the path and query unless noted:

| Request | Goes to |
|---|---|
| `http://` | `https://` on the same host, once the domain has SSL |
| `www.` variant, or any other domain of the store | the same path on the **primary domain** ([[settings-domains-primary]]) |
| a path ending in `/` | the same path without it (the web server's rule) |
| an old product, category, selection, page or blog-category address after a rename | the item's current address, query dropped, for **30 days** after the rename ([[seo-301-redirects-auto-tracking]]) |
| an address matching a rule on [[marketing-seo-301-redirects]] | the rule's target |
| `/products?search=…` | `/search?query=…` |
| `/products/category/…`, `/products/vendor/…`, `/products/selection/…`, `/products/tags/…` | the same address without `/products` (only while the store has at least one 301 rule) |

So `http://www.store.bg/category/shoes/` may answer with more than one 301 in a row before the final URL; Search Console reports each starting URL once as "Page with redirect". The admin panel uses 302 for host changes.

A CMS page assigned as the **home page** answers `/page/<its-slug>` with a 302 to the store's root; this is fixed, not a setting.

### Not found (404)

- A deleted product, page or category, or an **inactive** product or page, returns 404.
- A renamed item's old address returns 404 once the 30-day window has passed, unless a rule on [[marketing-seo-301-redirects]] catches it.
- `?page=N` past the last page of an indexable listing returns 404 (filtered, noindex listings do not).
- Crawlers requesting cart or checkout addresses get a 404 with `noindex` ([[storefront-cart-customisation]]).

Action: if the old address had traffic, add a 301 rule to the closest live page; otherwise nothing is needed, Google drops 404s on its own.

### Blocked by robots.txt — expected

The served robots.txt always adds the platform's own `Disallow` lines for checkout, cart and wishlist ([[seo-robots-served-file]]). A store that never saved its own robots.txt also blocks tag pages (`/tags/…`) and `/contacts/…` sub-pages through the platform default, so those addresses land here too. Trial, expired and development stores serve `Disallow: /` for everything ([[seo-plan-overrides]]), so every URL lands here until the store goes live.

### Blocked due to access forbidden (403) — expected for search

A crawler requesting `/search` gets a 403 with `X-Robots-Tag: noindex`: search results are not meant to be indexed. A 403 on other addresses is not produced by the storefront code; it comes from the security layer in front of the store and is checked per store.

## Related

- [[seo-handling]] — hub.
- [[seo-canonical-noindex]] — the noindex and canonical rules in detail.
- [[seo-route-catalog]] — which routes are indexable, noindex-eligible or always noindex.
- [[seo-sitemap-robots]] — what the sitemap lists and what robots.txt blocks.
- [[seo-301-redirects]] — per-URL rules and the 30-day rename history.
- [[settings-domains-primary]] — non-primary domains redirect to the primary.
- [[apps-google-search-console]] — connecting the store to Search Console.

## Open Questions

- The trailing-slash 301 is the web server's rule in the code's configuration; that production serves the same rule is confirmed only by observation (verify).
