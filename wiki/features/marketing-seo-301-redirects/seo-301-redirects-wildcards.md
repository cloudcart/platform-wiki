---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → Wildcards & lookup"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["Wildcard in old_url", "Old URL wildcards", "Asterisk wildcard 301", "7 named prefix fast-path", "Old URL LIKE matching", "Trailing slash 301"]
tags: [marketing, seo, redirects, wildcards, performance, lookup]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (types, validation, CSV import, middleware, marketing pass-through, auto-tracking).

# 301 Redirects — Wildcards & lookup

## Purpose

This aspect covers how the **storefront matches an incoming URL against the saved redirect rows**: the literal `*` → SQL `%` wildcard mapping, the 7-named-prefix fast-path optimization that keeps the lookup cheap, and the trailing-slash variant the lookup also tries. Understanding the prefix list matters for performance on stores with thousands of rules: rules outside the 7 prefixes still match but require a full-table scan.

## Where to find it

Wildcards are a property of the `old_url` value the merchant types into the inline editor on [[marketing-seo-301-redirects]]. The wildcard mechanics are invisible to the merchant beyond the support tip "you can use `*` in the old URL"; the platform handles the LIKE conversion at lookup time.

## What the merchant can do here

- Use a literal `*` anywhere in `old_url` to act as a wildcard. `/old-shop/*` matches `/old-shop/anything`, `/old-shop/category/x`, etc. — useful for migrating whole sections of an old URL tree in one rule.
- Trust that the lookup tries both with and without a trailing slash automatically.
- Implicitly benefit from the fast-path when their `old_url` starts with one of the 7 named prefixes (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`).
- Not be able to write a regex (only `*` is supported, and only as the SQL `%` wildcard).
- Not be able to negate-match or exclude a sub-path from a wildcard.

## Settings & fields

### Wildcard syntax

A literal `*` in `old_url` is converted to `%` for SQL `LIKE` matching at lookup time. The effective query is:

```sql
WHERE ? LIKE REPLACE(`old_url`, '*', '%')
```

So:

| Stored `old_url` | Matches incoming URL |
|---|---|
| `/old-shop/*` | `/old-shop/anything`, `/old-shop/category/x`, `/old-shop/products/123` |
| `/old/*/details` | `/old/foo/details`, `/old/bar/baz/details` |
| `/old?source=*` | `/old?source=newsletter`, `/old?source=fb-ad` |
| `/blog/post-*` | `/blog/post-1`, `/blog/post-old-stuff` |

### The 7 named prefixes — fast-path

The redirect lookup runs a path-prefix optimization to short-circuit the query. The full list of prefixes that trigger this fast-path:

```
product, category, vendor, blog, article, page, selection
```

If the requested path's first segment is one of these, the lookup runs an additional `WHERE old_url LIKE '/<prefix>/%'` filter first to narrow down candidates. For every other first segment, **the full-table scan happens** with the wildcard-substituted LIKE on every row's `old_url`.

This means: a custom merchant-defined prefix that doesn't match those 7 will still match, but the lookup is slower in proportion to the total number of redirect rows in the store.

### Trailing-slash variant

The lookup also tries the URL **with and without trailing slash**. So a rule with `old_url = "/old-page"` matches both `/old-page` and `/old-page/`. The merchant doesn't have to create two rules for the same target.

## Business rules

### `parseOldUrl` strips the fragment, keeps the query

The stored `old_url` is URL-decoded on save and stripped of any `#fragment` (per [[seo-301-redirects-validation]]). The query string IS kept — so a redirect from `/old?source=newsletter` to a new URL only fires when the customer hits `/old?source=newsletter` exactly.

To match the path regardless of query, the merchant uses a wildcard:

| Stored `old_url` | Matches |
|---|---|
| `/old` | Only `/old` exactly (no query string) |
| `/old*` | `/old`, `/old?foo=bar`, `/oldish/path` |
| `/old?*` | `/old?foo=bar`, `/old?source=newsletter` (any query) |

### Performance — stick to the 7 prefixes for large rule sets

Stores with thousands of rules + custom prefixes (`/old-shop/`, `/blog-2/`) may see slower 301 lookup latency because every storefront request with a non-prefix path triggers a full-table scan. For best performance, restructure migrations to keep the legacy URLs under one of the 7 named prefixes, or accept the latency.

Concretely: a store with 5 000 rules and a custom prefix can add ~50–200 ms to first-paint latency on the affected pages (varies by DB size and indexing — verify against the merchant's specific store profile).

### No regex, no negation

The wildcard syntax is the SQL `LIKE %` wildcard, nothing more. Merchants asking for "match all `/blog/2024-*` except `/blog/2024-draft`" have to create two separate rules (one matching the wildcard, one specifically matching `/blog/2024-draft` to override, where the more specific rule wins on the lookup order).

### Same-URL `creating` callback skip

When the merchant creates a `product` / `category` / `vendor` redirect AND the `old_url` is identical to the entity's CURRENT URL, the `creating` callback returns `false` — silently aborting the save with no error message. This is documented on [[seo-301-redirects-validation]]; called out here because it interacts with wildcards: a wildcard that resolves to the entity's current URL still triggers the skip if the wildcard value happens to match the literal current URL.

### Cache memoization is per requested URI, not per rule

The 24-hour `redirects301` cache (see [[seo-301-redirects-middleware]]) caches the lookup result per incoming URI. A wildcard rule `/old-shop/*` that gets hit by `/old-shop/foo` and `/old-shop/bar` produces **two** separate cache entries (one per URI). Both invalidate on any CRUD against any redirect rule (the entire tag is flushed atomically).

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-301-redirects-middleware]] — the middleware that runs this lookup; the `has_301_redirects` short-circuit; the cache.
- [[seo-301-redirects-validation]] — `parseOldUrl` fragment-strip + URL-decode rules.
- [[seo-301-redirects-marketing-passthrough]] — what gets appended to the matched destination at redirect time.

## Open questions

- Exact full-table scan latency at various row counts (verify against a production-scale store).
- Whether the 7-prefix list is extensible via configuration (`config`) or hardcoded (verify).
