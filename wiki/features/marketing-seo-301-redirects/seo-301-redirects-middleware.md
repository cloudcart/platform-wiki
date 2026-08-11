---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → Middleware & cache"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["Redirect middleware", "has_301_redirects setting", "redirects301 cache", "24-hour redirect cache", "Bulk delete redirects", "Storefront 301 lookup"]
tags: [marketing, seo, redirects, middleware, cache, performance]
plan_gates: []
created: 2026-06-10
updated: 2026-06-25
source_count: 4
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (types, validation, CSV import, wildcards, marketing pass-through, auto-tracking).

# 301 Redirects — Middleware & cache

## Purpose

This aspect covers how the **storefront actually serves a 301 redirect** at request time: the middleware that decides whether to look up a redirect at all, the `has_301_redirects` site-setting short-circuit, the 24-hour per-URI cache under the `redirects301` tag, and the bulk-delete endpoint that recomputes the setting.

Understanding the cache and middleware matters for two patterns: "I added a redirect but it's not firing" (cache hasn't flushed, or middleware skipped the lookup) and "redirects are slow" (the 7-prefix fast-path doesn't match — see [[seo-301-redirects-wildcards]]).

## Where to find it

The redirect middleware runs invisibly in front of every storefront request — no merchant UI. The merchant-visible side is the **Bulk delete** action on [[marketing-seo-301-redirects]] (selected rows → bulk delete endpoint → `has_301_redirects` recomputed → middleware short-circuits future requests if zero rules remain).

## What the merchant can do here

- Trust that the redirect they just saved fires on the very next storefront request (the platform cache is flushed atomically on every CRUD).
- Bulk-delete a selection of rows from the table — this resets the `has_301_redirects` site setting if zero rows remain, so the middleware short-circuits on subsequent requests (no DB lookup overhead).
- Not be able to directly inspect the cache from the admin UI — cache state is invisible to the merchant. Support team can flush it manually if a stale lookup is suspected (verify).

## Settings & fields

### `has_301_redirects` site setting

The site setting `has_301_redirects` is a boolean that controls whether the redirect middleware bothers running the lookup:

- `true` when the store has at least one redirect row (any type).
- `false` when zero rows exist.
- **Flipped to `true` on first save** of any redirect (Create endpoint).
- **Re-evaluated on every save and delete** — if a bulk-delete leaves the table empty, the setting flips back to `false`.

When `false`, the middleware skips the DB query entirely — zero overhead on storefront pageloads.

### `redirects301` cache tag

Redirect lookups are memoized per requested URI for **24 hours** under the `redirects301` cache tag. The cache key is the full requested URI (path + query). On any CRUD (save / update / delete / bulk delete), the entire tag is flushed — every cached URI is invalidated, so the next storefront request rebuilds the cache with the new rule set.

**Caveat:** CDN-edge layers and external caches (Cloudflare, etc.) may continue to serve stale 301 responses for longer than the platform's 24h — out of CloudCart's control. Merchants on a CDN who need a faster cache invalidation must flush the CDN cache themselves.

## Business rules

### The redirect middleware skips the lookup when ANY of:

The middleware sits in front of storefront requests. It SKIPS the redirect lookup when any of these conditions is true:

1. **The current request is not a storefront request.** Admin / API routes never hit the redirect middleware.
2. **The request is AJAX.** XHR requests get their natural response (404 for missing endpoints, 200 for found, etc.) — no 301 substitution.
3. **The current route is not one of the "indexable" routes.** The full list:
   ```
   site.home, selection, site.showcase, site.vendors, site.vendor.view,
   site.tag, category.view, category.list, blog.list, blog.view,
   blog.article.view, page, site.preview.page, bundles.list.list,
   bundles.list.category, product.view, contacts
   ```
   Other routes — checkout, account, search, etc. — never trigger a redirect lookup. This is by design: a 301 from `/checkout` makes no SEO sense.
4. **The store has zero redirects** (`setting('has_301_redirects')` is `false`).

This means redirect lookups don't hammer the DB on every page load — they only run when (a) the store has at least one redirect, AND (b) the requested route is one where a 301 redirect would make sense.

### A matching rule OVERRIDES a live page — it is NOT a 404-only fallback

This is the load-bearing precedence fact. The redirect middleware sits in the **`storefront` route-middleware group**, so it runs **before the page controller renders** and **returns the 301 immediately on a rule match** — it does not wait for the page to fail. So when an **indexable** route resolves to a **live, HTTP-200 page** (the home page, `/blog`, a live category, a live product / vendor / page, contacts, …) **and** a rule's `old_url` matches the requested URI, the **301 fires and pre-empts that live page**. A manual rule on `/blog` therefore *does* redirect away from the working blog page — the manual 301 manager is **not** consulted "only when the path would otherwise 404".

There is a **second activation path** for genuinely missing paths: the storefront's exception handler runs the same redirect lookup **on a 404**. On a 404 there is no resolved route, so the indexable-route gate is bypassed and the lookup runs for **any** non-existent path (not just the indexable list). So a manual rule catches a path that resolves to nothing, too.

Net precedence:

- **Indexable route → live 200 page:** a matching rule **overrides** the page (301 before render).
- **Any path → 404 (no route):** a matching rule fires as a **fallback** via the exception handler.
- **Non-indexable route → live page** (cart, checkout, account, search, …): the middleware **skips**, and since the page isn't a 404 the handler fallback doesn't apply either — so a manual rule on these paths **never fires**. This is the one place a rule is silently ignored.

So for a *"my 301 rule on a live page (e.g. `/blog`) doesn't fire"* ticket, the cause is **not** "rules can't override live pages" (they can, on indexable routes) — look instead at: `has_301_redirects` actually on, the `old_url` matching the exact requested URI (trailing slash / query string / encoding / `*`-wildcard — see [[seo-301-redirects-wildcards]]), and whether the source path is a **non-indexable** route. The 24-hour cache is **not** a cause, because every CRUD flushes the `redirects301` tag (above). This differs from the auto-tracked URL-handle history ([[seo-301-redirects-auto-tracking]]), which is fallback-on-404 only.

### Cache TTL — 24 hours per requested URI

Saving a new redirect or editing/deleting an existing one flushes the `redirects301` tag, so the merchant sees the change immediately on the next request. The 24-hour TTL only matters for URIs that haven't been touched by any save — over time, the cache fills up with hot URIs.

### Bulk delete endpoint

The Vue page's table is wired with `delete-default-bulk-action-url` pointing to `/admin/api/core/marketing/301-redirects` — but there is **NO route registered at this path in the current Core API** (verify). The bulk-delete mechanism on the table falls back to the shared bulk-actions handler, which in turn either issues per-row DELETEs to `/admin/api/core/seo/redirects/{id}` or POSTs the selected IDs to the configured URL.

**Support investigation pattern:** operators investigating bulk-delete failures should check both the Vue resource path and the network panel — the URL string is wired in the Vue page but not yet registered server-side. Per-row delete is the reliable fallback.

After a successful bulk-delete, `has_301_redirects` is re-evaluated: if zero rows remain, the setting flips to `false` and the middleware short-circuits future requests (no DB lookup).

### Physical files bypass the middleware

URLs to physical files served directly by the web server (`.pdf`, `.jpg`, `.css`, `.js`) bypass the application framework routing layer entirely — the redirect middleware never runs for them. A merchant who wants to redirect an old PDF URL has to do it at the host / infrastructure layer — CloudCart staff configure web-server / edge rules; there is no merchant-facing native rule for physical-file URLs (and [[apps-domain-redirect]] is *not* it — it is own-stores geo-routing, see the whole-domain boundary on [[seo-301-redirects-types]]).

### AJAX requests bypass the middleware

The AJAX skip means XHR requests to a redirected URL get the natural response (404 for missing) — not a 301. This is correct behaviour for fetch / the platform code flows, where the client expects a JSON or HTML payload, not a redirect.

### Storefront pages cached at the CDN are unaffected by `has_301_redirects` flips

When `has_301_redirects` flips from `true` to `false` (last redirect deleted), the platform short-circuits future MIDDLEWARE runs — but pages already cached at the CDN with a 301 status code keep serving until the CDN cache expires or is flushed. Same caveat applies in reverse: flipping from `false` to `true` (first redirect created) only affects requests that reach the origin.

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-301-redirects-wildcards]] — the lookup query that the middleware fires (LIKE / wildcard mechanics, 7-prefix optimization).
- [[seo-301-redirects-marketing-passthrough]] — what the middleware appends to the redirected URL.
- [[seo-redirect-lookup-and-cache]] — entity-side documentation of the same middleware / cache (data-model view).
- [[settings-domains]] — primary domain determines the host used for the Location header.
- [[storefront-architecture]] — the broader storefront request pipeline that the middleware sits inside.

## Open questions

- Whether the `delete-default-bulk-action-url` route is registered in any newer release of the Core API (verify).
- Whether there is an admin-side "flush redirects301 cache" action available to support staff (verify).
