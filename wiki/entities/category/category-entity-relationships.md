---
type: entity
nav_path: "Entity → Category → Relationships"
aliases: ["Category relationships", "Category links", "Category to product", "Category tree", "Category properties link"]
tags: [entity, catalog, categories, relationships, taxonomy]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[category]]. See the hub for the other aspects (attributes, lifecycle, business rules, side effects and API).

# Category — Relationships

## Identity

The links between a [[category|Category]] and every other entity in the platform — the **self-referential tree** of parent and child Categories, the **many-to-many** with Products (one product → many categories, one of them primary), the per-category attachments to [[category-property|Category Properties]] and to allowed [[payment-provider|Payment Providers]] / [[shipping-provider|Shipping Providers]], the SEO entries, and the downstream surfaces (storefront menu, analytics, importers, app integrations). Understanding these links is the prerequisite for understanding deletion guards, cache-flush side effects, and the cart-rule intersection rules.

## Aliases

- **Category tree** — parent / child self-reference.
- **Category-product M2M** — products in many categories.
- **Per-category cart-rule overrides** — payment / shipping restrictions stored as M2M to the providers.

## Key Attributes

A [[category|Category]]:

- **Has at most one** parent Category via `parent_id` (self-referential) — empty parent = top-level. Validated against the 6-level depth cap on every save — see [[category-entity-lifecycle]].
- **Has many** child Categories — same self-referential relationship in reverse. Most stores in practice stop at 2-3 levels; the 6-level platform cap is a generous guard rail.
- **Belongs to many** [[product|Products]] via the product-to-category pivot — one product can be in many categories. The product's primary `category_id` is one of them (used for breadcrumbs, default sorting, and the `category_id` reference on the product record). Publish requires at least one category — see [[product]].
- **Has many** [[category-property|Category Properties]] — per-category metadata definitions (e.g., for "Smartphones": Display size, RAM, Battery). Products in the category fill in these property values on the product edit page. Managed on [[products-property]]; the read-only `properties_count` shows how many are attached — see [[category-entity-attributes]].
- **References many** [[payment-provider|Payment Providers]] when "Define custom payment methods" is ON — restricts which providers are offered at checkout for carts containing products from this category. AND-combined across cart products — see [[category-entity-business-rules]].
- **References many** [[shipping-provider|Shipping Providers]] when "Define custom shipping methods" is ON — same pattern for shipping.
- **Has many** SEO entries — per-locale meta tags (title, description) and URL handle drive how the category page appears in search engines. Renames write 301 redirect entries to [[marketing-seo-301-redirects]].
- **Has one** category image stored in [[settings-files]] — uploaded via the dedicated upload pipeline on the edit modal. Not auto-deleted when the category is deleted (orphan in storage).
- **Is referenced by** apps and importers — Google Shopping feed apps (via `taxonomy_id`), CSV imports ([[apps-csv-import]]), and XML sync apps.
- **Appears in** storefront menu navigation (depending on the theme's menu source — categories are the default).
- **Appears in** analytics aggregations — [[analytics-top-categories-by-sales]] and [[analytics-top-categories-by-traffic]] roll up at the category level.

## Materialised path table

The platform maintains a denormalised `category_paths` table that stores one row per **(descendant, ancestor)** pair, with the per-pair level depth. This drives:

- **Breadcrumbs** on the storefront ("Home → Electronics → Phones → Smartphones") — read straight from the path table without walking `parent_id`.
- **Subtree-product queries** ("show me everything under Electronics" — descendants and grand-descendants) for the storefront catalog page.
- **The 6-level depth cap check** at save time — see [[category-entity-lifecycle]].

The path table is rebuilt on category create + parent change + delete via three model hooks — see [[category-entity-side-effects-and-api]].

## Primary vs additional category on Products

A [[product|Product]] can belong to many categories simultaneously. **One** of them is the **primary category** (the `category_id` on the product record), which drives:

- **Storefront breadcrumbs** — the trail shown above the product page.
- **Default sorting** — products list inside a category in `sort_order` then ID order.
- **Required-for-publish check** — a product cannot be `active = yes` without a primary category set.

Additional category assignments are M2M only — they let the product surface on multiple category pages but don't override the breadcrumb or publish guard. The primary `category_id` is set on the product edit page; additional categories are toggled via the category multi-select.

## Storefront menu source

The default storefront theme's main menu reads from the category tree (top-level categories as menu items, children as submenu). Themes can override this to use a different menu source (manual menu items, smart-collection-driven menu, blog categories) — the choice is theme-controlled, not category-controlled. The `icon` field on the category surfaces in the menu when the theme supports it.

## Search facets

Storefront search results expose categories as filter chips. The chip count is derived from `real_products_count` minus search-filter exclusions. Categories with zero matching products are hidden from the facets.

## Where it appears

- [[products-categories]] — parent-child tree (Organize tab) + per-category property attachments + per-category payment / shipping restrictions.
- [[products-property]] — Category Properties attached to categories; the read-only `properties_count` reflects this here.
- [[products-products]] — products' primary + additional category assignments, plus the category filter on the list.
- [[product]] — primary `category_id` field; product → category many-to-many.
- [[settings-payment-providers]] — providers the per-category restriction picks from.
- [[settings-files]] — category images live here.
- [[analytics-top-categories-by-sales]] / [[analytics-top-categories-by-traffic]] — category rollups.
- [[apps-csv-import]] — bulk-import that writes M2M assignments.
- [[apps-google-shopping]] — reads `taxonomy_id`.

## Related

- [[category]] — hub.
- [[category-entity-attributes]] — `parent_id`, `category_path.level`, `real_products_count`, `properties_count` fields.
- [[category-entity-lifecycle]] — depth cap and deletion-blocked-while-products-remain (relationships drive the guard).
- [[category-entity-business-rules]] — AND-combined payment / shipping intersection across cart products.
- [[category-entity-side-effects-and-api]] — cascade cleanup on delete; path-table rebuild on parent change.
- [[product]] — products in many categories with one primary.
- [[category-property]] — per-category property definitions.
- [[payment-provider]] / [[shipping-provider]] — referenced providers.
- [[smart-collection]] — alternative rule-based grouping (NOT hierarchical, NOT M2M with the cart-rule overrides).
- [[blog-category]] — separate hierarchy for blog content (different entity).

## Open Questions

- **Multi-warehouse interaction** — when [[apps-store-locations]] is enabled, do categories carry per-warehouse stock visibility flags, or is that exclusively at the product / variant level? (verify)
