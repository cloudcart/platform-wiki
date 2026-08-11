---
type: entity
nav_path: "Entity → SEO 301 Redirect → Lookup and cache"
aliases: ["301 redirect lookup", "Redirect middleware", "Wildcard redirects", "has_301_redirects", "redirects301 cache", "Path-prefix optimisation", "Indexable routes"]
tags: [entity, seo, marketing, redirects, performance, cache]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[seo-redirect]]. See the hub for the other aspects (types, marketing passthrough, CSV import, auto-tracking, validation and UI).

# 301 Redirect — Lookup and cache

## Identity

When a customer or bot requests a URL on the storefront, the redirect middleware decides — fast — whether any [[seo-redirect|301 rule]] matches. The mechanics matter because they explain (a) why a brand-new rule appears to work immediately, (b) why a rule with a custom URL prefix may feel slower than one with a CloudCart-conventional prefix, and (c) why some redirects keep firing for hours after a delete from external caches.

The lookup runs only on a fixed set of "indexable" storefront routes and short-circuits entirely when the merchant has zero rules.

## Aliases

- **Redirect middleware** — the storefront layer that performs the lookup.
- **`has_301_redirects`** — the site-setting flag that short-circuits the lookup when zero rules exist.
- **`redirects301`** — the cache-tag identifier under which lookups are memoized.
- **Indexable routes** — the storefront routes that trigger the lookup.

## Key Attributes

| Mechanism | What it does | Why merchants need to know |
|---|---|---|
| **`has_301_redirects` short-circuit** | When `false`, the middleware skips the DB lookup entirely on every request. Flips to `true` on first rule saved, back to `false` when the last rule is deleted. | Stores with zero rules pay zero overhead. |
| **Wildcard `*` → SQL `%`** | A literal `*` in `old_url` is converted to `%` for the SQL `LIKE` lookup. `/old-shop/*` matches `/old-shop/anything`, `/old-shop/category/x`, etc. | Lets the merchant migrate a whole URL subtree with one rule. |
| **Trailing-slash tolerance** | The lookup tries the URL both with and without a trailing slash. | Avoids the merchant having to write two rules for `/path` and `/path/`. |
| **Path-prefix optimisation (7 conventional prefixes)** | When the requested URL's first segment is one of `product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`, the lookup runs a prefix-scoped query (`old_url LIKE '/product/%'`) instead of scanning the whole table. | Stick to conventional prefixes for best performance — custom prefixes trigger a wider scan. |
| **24-hour `redirects301` cache** | Each requested URI's lookup result is memoized for 24 hours under the `redirects301` cache tag. Saving / editing / deleting any rule flushes the entire tag. | Internal changes apply on the next request. External CDN / browser caches are out of platform control. |
| **Indexable-route gate** | The middleware only runs on a fixed list of storefront routes (Home, Selection, Showcase, Vendors, Vendor view, Tag, Category view, Category list, Blog list, Blog view, Blog article view, Page, Page preview, Bundles list, Bundles list category, Product view, Contacts). | Admin panel, cart, checkout, account, etc. are NOT redirect-eligible — the merchant cannot redirect away from the cart page using this mechanism. |
| **AJAX / non-storefront skip** | The middleware skips AJAX requests and non-storefront requests entirely. | Theme-internal calls aren't intercepted. |

## Relationships

- **Reads** the `has_301_redirects` site setting (managed automatically by the entity's save / delete hooks).
- **Reads from** the `redirects301` cache tag (which is invalidated by every save / delete).
- **Affects** which routes the lookup runs against — only the indexable list above.

## Lifecycle

For each indexable storefront request:

1. **Gate check** — if `has_301_redirects = false`, return immediately (no DB lookup).
2. **Cache lookup** — check `redirects301` for the requested URI. Hit → return the cached redirect target (or "no match").
3. **DB lookup** — miss → run the `LIKE` query against the `old_url` column, scoped to the path-prefix optimisation if the first segment is one of the 7 conventional prefixes.
4. **Match resolution** — the matching rule is resolved per its type (see [[seo-redirect-types]]).
5. **Cache store** — store the result (target or "no match") under the requested URI for 24 hours.
6. **Marketing parameters** — append the whitelisted query parameters from the original URL — see [[seo-redirect-marketing-passthrough]].
7. **Respond** — HTTP 301 with the `Location` header set.

## Business rules

### The 7-prefix optimisation is performance-critical

Stores with thousands of rules + custom prefixes (`/old-shop/`, `/blog-2/`, `/v1/`) trigger a **broader scan** with wildcard-substituted `LIKE` on every row's `old_url`. Lookup latency grows with rule count for custom prefixes. For best performance, prefer rules whose `old_url` starts with one of the 7 conventional prefixes — `product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`.

### 24-hour internal cache vs external caches

The platform invalidates `redirects301` on every save / delete, so changes apply within the next request from the platform's perspective. But external CDN, browser, and ISP intermediaries may serve stale 301s for much longer. Browsers cache 301 responses **indefinitely** until the URL is purged or the user clears the cache. For bulk migrations, the merchant should pre-warn cache providers or use a controlled rollout. There is no in-admin warning about this.

### Wildcard usage is NOT documented in the UI

The admin help text and placeholders do not explain that `*` substitutes the SQL `%` wildcard at request time — power-users discover this only via support documentation. The feature works as advertised but is undocumented in-product.

### Middleware does NOT run on cart / checkout / account

The "indexable" route list excludes the cart, checkout, account, login, register, wishlist, and search pages. A merchant who tries to redirect `/cart` to `/special-cart` via a 301 rule will find the rule has no effect — those routes bypass the middleware entirely. (Whole-domain forwarding via [[apps-domain-redirect]] DOES affect every route, including those.)

### Always 301 — no 302 option

Every match returns HTTP 301 (permanent). The admin UI doesn't expose a 302 (temporary) option — see [[seo-redirect-validation-and-ui]]. Browsers and search engines update their bookmarks / index permanently, which matches the merchant intent for this screen.

## Where it appears

- [[marketing-seo-301-redirects]] — the manager screen.
- [[seo-redirect-types]] — type-specific destination resolution after a match.
- [[seo-redirect-marketing-passthrough]] — the query-parameter preservation step.
- [[checkout-flow]] — note that the cart / checkout routes are NOT in the indexable list (the middleware does not run for them).
- [[storefront-architecture]] — the storefront's HTTP stack within which the middleware sits.

## Related

- [[seo-redirect]] — hub.
- [[seo-redirect-types]] — what happens after a match (per-type resolution).
- [[seo-redirect-marketing-passthrough]] — what gets appended to the `Location` URL.
- [[marketing-seo-301-redirects]] — where merchants manage rules.

## Open Questions

- Whether the path-prefix optimisation can be extended to merchant-defined custom prefixes (would help large migrations away from `/old-shop/*` patterns) (verify).
