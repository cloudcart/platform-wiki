---
type: feature
nav_path: "Products → Tags → Consumers, API & permissions"
route_name: products.tags
route_path: /admin/products/products/edit/:id (Tags section)
aliases: ["Product tag consumers", "Tags in cart rules", "Tags in smart collections", "Product tags API", "products.tags permission", "Tag plan gates"]
tags: [products, tags, classification, taxonomy, api, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

# Product Tags — consumers, API & permissions

> Part of [[products-tags]]. See the hub for the other aspects (assignment, data model, lifecycle).

## Purpose

This aspect documents **what consumes product tags** (the features that match on them), the **programmatic surface** (JSON-API v2 + the internal admin REST endpoint), and the **permission + plan-gate** picture. This is why a tag defined once becomes broadly powerful: many systems read it. For where tags are created see [[products-tags-assignment]]; for how they are stored see [[products-tags-data-model]].

## Where to find it

Each consumer has its own admin screen (linked below). The programmatic surface is reached through the merchant-facing JSON-API v2 ([[json-api-v2]]) and, for full tag CRUD, the internal admin REST endpoint `/admin/api/core/product-tags` (not a merchant-facing surface).

## What the merchant can do here

- Use a tag as a **condition / population criterion** in several downstream features (see Business rules).
- Set tag values **programmatically** on a product via the parent product's `tags` field on [[api-products]] (when the resource accepts it).
- Grant or restrict tag create / update / delete via the `products.tags` permission scope.

What the merchant **cannot** do programmatically: rename, merge, or delete tags through JSON-API v2 — none of those have a JSON-API v2 surface (see Business rules).

## Settings & fields

### JSON-API v2 surface

- **No dedicated JSON-API v2 resource for tags** in the merchant-facing API. Tag values are set via the parent product's `tags` field on [[api-products]] (when the resource accepts it).
- On a product PATCH with new tag strings, the same auto-create resolver runs (lower-cased `firstOrCreate`, trimmed, wildcard-only `%` / `_` dropped, ≤ 191 chars per tag, ≤ 100 tags per product) — identical to the UI save path. The full mechanics are on [[products-tags-lifecycle]].
- No auto-prune of orphan tags happens on either path.
- For renames, merges, or deletes of tags themselves — none of those have a JSON-API v2 surface; the merchant must re-tag products one-by-one (or via [[apps-csv-import]]) and live with orphan tag records.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

### Internal admin REST endpoint

The internal admin endpoint `/admin/api/core/product-tags` supports full tag CRUD including the dormant SEO / image columns (`url_handle`, `description`, `seo_title`, `seo_description`, `image`) documented on [[products-tags-data-model]] — but that endpoint is **not** the merchant-facing JSON-API v2 surface. The search/autocomplete endpoint `/admin/api/core/product-tags/search` backs the editor picker (see [[products-tags-assignment]]).

## Business rules

### Consumers of product tags

Several systems read a product's tags:

- [[apps-cart-rules]] — `condition_type=product, filter_type=tag, record_type=tag` triggers (IN / NOT IN operator).
- [[products-smart-collections]] — collection auto-population by tag.
- [[apps-google-shopping-attributes]] — map a tag to a Google attribute.
- [[apps-size-chart-conditions]] — attach a size chart to all products with a specific tag.
- [[apps-olx-configuration]] — map an OLX category by CloudCart tag.
- Storefront browse filters + search relevance signals (see [[products-tags-data-model]] for the filter, [[products-list]] for the page).

This is why the lightweight tag concept is broadly powerful — the merchant defines a tag once, and many systems consume it. The flip side: a tag change ripples — Smart Collections re-evaluate, Cart Rules re-evaluate at next cart load, the storefront filter recomputes (cached).

### Permission

Tag CRUD lives under the `products` and `products.tags` API permission scopes. The search/autocomplete endpoint (`/admin/api/core/product-tags/search`) is **not** gated — any signed-in admin user can read tags for autocomplete in the product editor; only create / update / delete require the `products.tags` grant.

### Plan gates

The tag feature itself has **no plan-feature gate** — all plans (including the free / Start Up tier) can tag products. Tags are governed only by the standard `products` / `products.tags` permission scopes.

Caps that DO apply are NOT plan-gated — they are platform-wide validation rules (100 tags/product, 191 chars/tag, 191 chars/`url_handle`); see [[products-tags-lifecycle]].

**Downstream consumers have their OWN plan gates** — using a tag in a Smart Collection rule depends on the `product_collections` cap; using one in a Cart Rule depends on the `cart_rules_*` family; etc. The tag itself is plan-neutral. See [[plan-gates]] for the gating concept.

## Related

- [[products-tags]] — hub.
- [[api-products]] — the JSON-API v2 product resource that carries the `tags` field.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[apps-cart-rules]] — uses tags in rule conditions.
- [[products-smart-collections]] — auto-population by tag.
- [[apps-google-shopping-attributes]] — maps tags to Google attributes.
- [[apps-size-chart-conditions]] — maps size charts via tags.
- [[apps-olx-configuration]] — maps tags to OLX categories.
- [[plan-gates]] — the gating concept (consumers gate, the tag does not).

## Open questions

- Whether the merchant-facing [[api-products]] resource always accepts the `tags` field on write across all product types (verify per product type).
