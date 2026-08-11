---
type: concept
nav_path: "Concept → SEO handling → Route catalog"
aliases: ["Storefront route catalog", "Indexable routes", "Noindex routes", "Always-noindex routes", "Redirect middleware routes", "SEO route list"]
tags: [seo, routes, storefront, middleware, indexing, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, canonical / noindex, meta tags, redirects, sharing / RSS, plan overrides).

# SEO — storefront route catalog

## Definition

Different SEO behaviors activate on different sets of storefront route names. This page is the **single authoritative catalog** of those route sets — verbatim — so other SEO aspects can link here instead of repeating the lists.

Four sets:

- **Indexable routes** — the routes the redirect middleware activates on (the routes that emit `<link rel="canonical">`).
- **Noindex-eligible (filtered/sorted) routes** — the routes where the `noindex_query_limit` rule applies.
- **Always-noindex routes** — system pages that always emit `<meta name="robots" content="noindex, nofollow">`.
- **Robots-meta-exempt routes** — the routes that emit no robots meta at all (no indexable, no noindex).

## Scope

Covered:

- The four verbatim route name lists.
- One-line description of what behavior each list governs.
- Pointers back to the aspect that documents the behavior in detail.

Not covered here:

- The actual behavior (canonical emission, noindex emission, redirect activation) — see the linked aspects.
- Per-section meta and per-entity meta fallback chains → [[seo-meta-tags]].
- Plan overrides that bypass all of these route rules → [[seo-plan-overrides]].

## Contrasts

- **Indexable vs. Noindex-eligible vs. Always-noindex** — these are three different sets with different memberships. A route can be both indexable (gets canonical) AND noindex-eligible (gets `noindex` when query-param count exceeds threshold). The always-noindex set is disjoint from the indexable set.
- **`products.list` is a special case** — it's noindex-eligible (the filter-count rule can flip it to `noindex`), and it emits a canonical, but it's also in the robots-meta-exempt list which means it skips the `<meta name="robots">` tag in the indexable-by-default case. The canonical still emits on `products.list`.
- **`ajax.*` routes** — robots-meta-exempt entirely; never emit canonical or robots directives.

## Where it applies

### Indexable routes (redirect middleware activates)

The redirect middleware activates on these route names only. These are also the routes that emit `<link rel="canonical">` by default (see [[seo-canonical-noindex]]):

```
site.home
selection
site.showcase
site.vendors
site.vendor.view
site.tag
category.view
category.list
blog.list
blog.view
blog.article.view
page
site.preview.page
bundles.list.list
bundles.list.category
product.view
contacts
```

### Noindex-eligible routes (filtered / sorted)

The `noindex_query_limit` rule applies on these routes. When the count of "meaningful" query parameters exceeds the threshold, the page renders `<meta name="robots" content="noindex">` AND the canonical is suppressed. See [[seo-canonical-noindex]] for the parameter-counting rules.

```
category.view
products.list
selection
site.vendor.view
site.tag
products.search
showcase.list
bundles.list.list
bundles.list.category
```

### Always-noindex routes

These routes always emit `<meta name="robots" content="noindex, nofollow">` — they never get a canonical either:

```
checkout
checkout.*
cart.*
compare
site.auth.*
site.account
site.account.*
```

### Robots-meta-exempt routes

The `products.list` and `ajax.*` routes are **EXEMPTED from any `<meta name="robots">` tag** entirely (no indexable, no noindex). The canonical tag **still emits on `products.list`**.

```
products.list
ajax.*
```

### How the rules combine on a single request

For any incoming storefront request:

1. **Plan check first** — if the store is trial / `plan_expired` / dev, robots.txt is `Disallow: /` and Google never sees the page anyway. If the store is on `cc-demo`, the page emits `<meta name="robots" content="noindex, nofollow">` and the route catalog doesn't matter. See [[seo-plan-overrides]].
2. **Always-noindex check** — if the route name matches the always-noindex set, emit `noindex, nofollow`, skip canonical, done.
3. **Robots-meta-exempt check** — if the route name matches `products.list` or `ajax.*`, skip the robots meta. Canonical may still emit on `products.list`.
4. **Noindex-eligible check** — if the route is in the noindex-eligible set, count meaningful query params; if over threshold, emit `noindex` and suppress canonical.
5. **Indexable default** — emit canonical, run the redirect-middleware lookup, emit normal meta tags.

## Related

- [[seo-handling]] — hub.
- [[seo-canonical-noindex]] — what canonical / noindex actually mean and how they're emitted on these routes.
- [[seo-301-redirects]] — the redirect middleware activates on the indexable-routes list.
- [[seo-sitemap-robots]] — noindex'd URLs are omitted from the sitemap.
- [[seo-plan-overrides]] — overrides that short-circuit this whole route logic.

## Open Questions

None.
