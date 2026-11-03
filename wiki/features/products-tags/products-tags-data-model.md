---
type: feature
nav_path: "Products → Tags → Data model & storefront"
route_name: products.tags
route_path: /admin/products/products/edit/:id (Tags section)
aliases: ["Product tag data model", "Tag SEO columns", "Tag landing page", "Storefront tag filter", "/tags/<url-handle>", "Структура на таговете"]
tags: [products, tags, classification, taxonomy, storefront, seo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

# Product Tags — data model & storefront

> Part of [[products-tags]]. See the hub for the other aspects (assignment, lifecycle, consumers + API).

## Purpose

This aspect documents **what a tag IS as stored data** — the flat record, the dormant SEO / image columns that exist in the table but have no admin UI, and the storefront surfaces a tag drives (filter chips on category pages + the dedicated `/tags/<url-handle>` landing page). For how tags get attached, see [[products-tags-assignment]]; for the auto-create / validation mechanics, see [[products-tags-lifecycle]].

## Where to find it

There is no dedicated data-model screen. The merchant only ever sees tags as chips in the product editor's Tags aside ([[products-tags-assignment]]) and as filter chips on the storefront. The richer stored fields below have **no native admin screen** at all.

## What the merchant can do here

- Rely on the **automatic storefront tag filter** appearing on category pages once products in that category carry tags — no explicit configuration needed.
- Link a category to a tag landing page so customers reach `/tags/<url-handle>`.

What the merchant **cannot** do natively: edit any of the tag's SEO / image columns (no screen surfaces them), or give a tag a description, colour, or icon. Tags are pure labels — compare with [[products-categories]], which have full SEO and image support.

## Settings & fields

### Tag record (visible vs dormant)

The merchant-facing picker shows a tag as a bare label, but the underlying `tags__products_tags` table stores more:

| Field | Surfaced in admin UI? | Notes |
|-------|----------------------|-------|
| **id** | No | Internal identifier. |
| **name** (`tag`) | Yes (the chip text) | The label; stored lowercase (see [[products-tags-lifecycle]]). |
| **count** | Yes (derived) | How many products carry this tag. |
| **url_handle** | No (dormant) | Generated from the name on first persist; powers `/tags/<url-handle>`. ≤ 191 chars. |
| **description** | No (dormant) | No admin screen edits it. |
| **seo_title** | No (dormant) | No admin screen edits it. |
| **seo_description** | No (dormant) | No admin screen edits it. |
| **image** | No (dormant) | No admin screen edits it. |
| **max_thumb_size** | No (dormant) | No admin screen edits it. |

The admin Tags REST endpoint (`/admin/api/core/product-tags`) supports full CRUD including these dormant columns, but there is currently **no admin Vue page** that surfaces them, so for merchants they are effectively dormant (data may be set by some imports or apps, but the merchant has no native screen to edit it). See [[products-tags-consumers-api]] for the endpoint surface.

Per-product assignment is **many-to-many** through a junction table.

## Business rules

### Tags are lightweight — no SEO metadata in practice

Tags effectively carry only a `name`. Because no admin screen exposes the SEO / image / description columns, there is no per-tag description, SEO title / meta description, or image / colour / icon that a merchant can manage. They are pure labels used as filter criteria for other features ([[products-smart-collections]], [[apps-cart-rules]], [[apps-google-shopping-attributes]], etc. — catalogued on [[products-tags-consumers-api]]).

### Storefront tag filter

When products in a category have tags, the storefront automatically exposes a tag filter on the category page (see [[products-list]]). The merchant doesn't configure this explicitly. Selecting a tag chip narrows results to products carrying that tag.

### Storefront tag landing page

Beyond filter chips, the storefront has a dedicated `/tags/<url-handle>` route (see [[tag]]) that lists every product carrying that tag. The page is generated from the `url_handle` column, which is derived from the tag name when the tag is first persisted. The landing page is visible to customers if a category links to it.

### No central management page (yet)

Tags are created inline from the product editor's tag picker; there is no separate central admin page for tags. Bulk operations (rename across many products, merge two tags, delete a tag entirely) have to be done by editing individual products. This is a known UX gap — contrast with [[marketing-blog-tags]], which has a central list.

## Related

- [[products-tags]] — hub.
- [[products-categories]] — hierarchical concept with full SEO + image support (the contrast case).
- [[products-smart-collections]] — auto-populates by tag.
- [[products-list]] — storefront category / results page that renders the tag filter.
- [[tag]] — storefront tag landing page (`/tags/<url-handle>`).

## Open questions

- Whether any first-party import or app actually populates the dormant SEO / image columns in practice (verify).
