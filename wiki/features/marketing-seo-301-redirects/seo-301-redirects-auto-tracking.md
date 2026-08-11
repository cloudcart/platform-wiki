---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → Auto-tracking & cascade"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["URL handle history", "30-day TTL on slug rename", "Auto-redirect on rename", "Entity-delete cascade redirects", "Implicit 301 on product rename", "Auto-tracking redirects"]
tags: [marketing, seo, redirects, auto-tracking, cascade, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (types, validation, CSV import, middleware, wildcards, marketing pass-through).

# 301 Redirects — Auto-tracking & cascade

## Purpose

This aspect covers the **two implicit redirect mechanisms** that run in the background, independent of the rows on [[marketing-seo-301-redirects]]:

1. **URL-handle-history auto-redirect** — when a [[product]] / [[category]] / [[vendor]] / [[marketing-landing-pages|page]] / blog / [[blog-article]] is renamed (URL slug changed), the platform records the old slug into a URL-handle-history collection with a **30-day TTL** and the storefront serves an internal 301 from the old slug to the new URL for that window.
2. **Entity-delete cascade** — when one of those entities is deleted, every redirect rule that points to it (entity-type rules only) is automatically deleted. Manual / External / Section rules survive.

Together these mean the merchant rarely has to manually create a redirect on slug renames (within 30 days) — but DOES need to add a permanent rule on this page if they care about SEO past the 30-day window.

## Where to find it

Both mechanisms are invisible from the [[marketing-seo-301-redirects]] page — there are no rows there for auto-tracked slug history, and rows that get cascaded out simply disappear from the table. The merchant sees the auto-redirect working on the storefront (old URLs keep loading) but has no admin surface to inspect the 30-day window.

## What the merchant can do here

- Rename a product / category / vendor / page / blog / article URL slug from its own edit screen, and watch the old slug keep working on the storefront for 30 days afterwards — no manual redirect rule needed.
- Delete an entity (product / category / vendor / page / blog / article) and trust that every entity-type redirect rule pointing to it is cleaned up automatically — no orphaned rules to maintain.
- Create a **permanent** redirect rule on [[marketing-seo-301-redirects]] before the 30-day window expires if the merchant cares about SEO past that point (the auto-tracked old slug has no UI, no extend mechanism, and silently expires).

### What the merchant CANNOT do here

- Extend the 30-day TTL on URL-handle-history (verify whether a config exists).
- See the auto-tracked slug history from the admin UI — there is no "Old URLs for this product" panel on the product editor.
- Recover a deleted entity's redirect rules after the cascade has run — the rows are gone, and re-creating the entity creates a new ID that the old rules wouldn't have pointed at anyway.
- Disable the cascade per rule (e.g., "delete the product but keep the redirect pointing to its old URL").

## Settings & fields

### URL-handle-history collection

When a product's `url_handle` is edited (or a category / vendor / page / blog / article URL slug changes), the platform writes the old slug into a URL-handle-history collection with a **30-day TTL** (the collection auto-purges entries older than 30 days).

The collection is invisible to the merchant — no admin UI exposes it. The storefront's controllers consult it when a 404 would otherwise happen and serve an internal 301 to the entity's current URL.

This is separate from the rows on [[marketing-seo-301-redirects]] — the rows are merchant-explicit redirects with no TTL; the auto-tracked history is implicit and time-limited.

### Cascade on entity delete

When a product / category / vendor / page / blog / article is deleted, all redirect rows on [[marketing-seo-301-redirects]] that point to it are deleted automatically (cascade through the redirect model's deleted callback). The merchant doesn't have to manually clean up redirect rows for entities they removed.

| Entity type deleted | Cascade affects | Survives |
|---|---|---|
| [[product]] | `item_type=product` rules with that `item_id` | `manual` / `external` / `section` rules — even those with paths that name the product |
| [[category]] | `item_type=category` rules | Same |
| [[vendor]] | `item_type=vendor` rules | Same |
| [[marketing-landing-pages\|page]] | `item_type=page` rules | Same |
| Blog category | `item_type=blog` rules | Same |
| [[blog-article]] | `item_type=article` rules | Same |

## Business rules

### 30-day TTL — after the window, the auto-redirect stops

After 30 days, the auto-tracked old slug stops working. At that point, if the merchant cares about preserving SEO from the old URL, they should manually create a row on [[marketing-seo-301-redirects]] (which has no TTL) — ideally before the 30-day window expires, but the rule still works retroactively if Google has cached the old URL.

**Support pattern:** "a URL that used to redirect now returns 404" — check whether the entity was renamed more than 30 days ago and no manual rule was created. Solution: create a manual rule pointing the old URL to the entity's current URL.

### The redirect middleware does NOT consult URL-handle-history

The middleware on [[seo-301-redirects-middleware]] checks ONLY the explicit redirect rows. The URL-handle-history auto-redirect is served by the storefront's controllers AFTER a 404 would otherwise happen. The two mechanisms are independent:

1. Customer hits `/old-slug` → middleware checks redirect rows → no match → request continues to the controller.
2. Controller tries to resolve `/old-slug` to a product/category/vendor → no match → controller checks URL-handle-history → match found (within 30 days) → serves internal 301 to the entity's current URL.

This ordering means an explicit rule on [[marketing-seo-301-redirects]] for the same `old_url` ALWAYS wins over the auto-tracked history — useful if the merchant wants to redirect an old slug to a different destination than the entity's new URL.

### Cascade is type-scoped — manual / external / section survive

Only entity-typed rules cascade on entity delete. `manual`, `external`, and `section` rules live until the merchant removes them. A merchant who deletes a product but had a `manual` redirect from `/old-product-slug` to `/related-category` keeps the redirect.

### Recreating a deleted entity does NOT restore its rules

If the merchant deletes a product and then re-creates a new product (even with the same name and slug), the new product gets a new ID. The cascaded redirect rules are gone — they were pointing to the old ID.

### Auto-tracking does not span across stores

URL-handle-history is per-store. Renaming a product on one store does NOT auto-redirect on another store, even in multi-tenant setups. Each store maintains its own URL-handle-history collection.

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-301-redirects-types]] — the entity types that participate in the cascade.
- [[seo-301-redirects-middleware]] — the middleware that runs BEFORE the URL-handle-history fallback.
- [[seo-redirect-auto-tracking]] — entity-side documentation of the same auto-tracking + cascade (data-model view).
- [[product]] — slug rename triggers auto-tracking; delete triggers cascade.
- [[category]] — same.
- [[blog-article]] — same.
- [[marketing-landing-pages]] — same.

## Open questions

- ⏸️ **30-day TTL on URL-handle-history.** Auto-tracked old slugs expire 30 days after the slug change. After the TTL, the redirect stops working unless the merchant has explicitly added a permanent redirect entry on [[marketing-seo-301-redirects]]. No admin UI exists to extend the TTL.
- Whether the cascade fires on soft-delete only, hard-delete only, or both (verify against the redirect trait's `deleted` callback).
- Whether a config exists to change the 30-day TTL globally (verify).
