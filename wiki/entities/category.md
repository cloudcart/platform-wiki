---
type: entity
nav_path: "Entity → Category"
aliases: ["Category", "Product category", "Catalog category", "Категория", "Категория на продуктите"]
tags: [entity, catalog, products, categories, navigation, taxonomy]
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---

# Category

## Identity

A **Category** is a hierarchical grouping of products in the merchant's catalog — the primary navigation taxonomy customers browse on the storefront and the grouping the merchant uses to find products in admin. Categories form a **tree**: each Category has zero or one parent, and any number of children (with a hard depth cap of 6 levels). The merchant uses categories to organise the catalog (e.g., "Electronics → Phones → Smartphones"), expose menu navigation on the storefront, scope shipping methods and payment providers, drive properties (specifications), and feed marketplace exports (Google Shopping, OLX).

A product can belong to many categories simultaneously; one of them is the **primary category** (the canonical assignment used for breadcrumbs, default sorting, and `category_id` on the [[product|Product]]). Categories carry their own descriptive content (name, description, image), SEO settings (custom URL handle, meta title, meta description), and per-category cart-rule overrides (allowed payment methods and shipping methods). Categories are managed on [[products-categories]] via two tabs — List (for create / edit / delete) and Organize (for drag-and-drop tree reordering).

Categories are distinct from **tags** (free-form labels applied to products without hierarchy), **smart collections** (rule-based product groupings), **vendors / brands** (a single per-product brand reference), and **customer groups** (which group customers, not products).

## Aliases

- **Category** — the standard merchant-facing term across admin and storefront.
- **Product category** / **Catalog category** — used when distinguishing from blog categories ([[blog-category]]) or other taxonomies.
- **Категория** / **Категория на продуктите** — Bulgarian equivalents.

## Key Attributes

The Category is a multi-faceted record split across **five well-scoped aspects**. The AI Assistant should drill into the aspect that matches the question, not read every page.

- [[category-entity-attributes]] — the full per-field schema (name, parent, description, image, `display_child`, `taxonomy_id`, allowed payment / shipping methods, `make_interval`, SEO title / description / URL handle, sort order, icon, dimensions, `seo_generated_through_spinner`, computed `real_products_count` / `properties_count`, materialised path `level`).
- [[category-entity-lifecycle]] — the merchant-controlled states (Draft, Active, Reorganised, Renamed, Deleted), save-time transitions, the **6-level depth cap**, deletion blocked while products remain or an active XML-import task uses the category, URL-handle renames generating 301 redirects, search-index rebuild + cache flush on save, orphan-image-on-delete behaviour.
- [[category-entity-relationships]] — parent / child Categories (self-referential tree), product M2M with primary `category_id`, [[category-property|Category Properties]] for per-category specifications, M2M to [[payment-provider|Payment Providers]] and [[shipping-provider|Shipping Providers]] for cart-rule overrides, SEO entries, app references (Google Shopping, CSV / XML importers), storefront menu and search facet placement, analytics rollups.
- [[category-entity-business-rules]] — `display_child` recursive-inclusion toggle; per-category payment / shipping restrictions **AND-combined** across cart products (empty-intersection pitfall); URL-handle 301 redirects; sibling-scoped name uniqueness; auto-assigned sort order on create; technological-delivery-time (`make_interval`) pushing the earliest delivery slot; per-locale multi-language naming with store-wide Google Shopping mapping; SEO defaults (title → name, description → truncated description, handle → slugified name); duplicate-handle behaviour (manual rejects, CSV / XML auto-suffixes).
- [[category-entity-side-effects-and-api]] — transaction-bound tree-reorder atomicity (Organize tab drag-drop), materialised `category_paths` rebuild on create + parent change, cascade cleanup on delete (path rows + restriction rows + webhook + the application framework events), search-index rebuild, customer-cart cache flush, SEO cache invalidation, JSON-API v2 access via [[api-categories]] (same side effects, same validation, one CSV-vs-API duplicate-handle divergence).

## Why it matters to the merchant

Categories sit at the centre of **storefront navigation, checkout method scoping, SEO discoverability, and catalog organisation**. Five high-impact behaviours the merchant should understand:

- **Deletion is BLOCKED while products remain inside.** The merchant must re-assign or remove every product first — the platform never silently re-parents products. See [[category-entity-lifecycle]].
- **Per-category payment / shipping restrictions intersect across cart products.** If a cart mixes products from two restricted categories and the allowed-methods sets don't overlap, the customer sees no payment / shipping methods at checkout. See [[category-entity-business-rules]].
- **`Display subcategories` controls whether parent-category pages show descendant products.** ON = recursive inclusion; OFF = only directly-assigned. Read only at the level being browsed — deep descendants cannot opt out of an ancestor's recursion. See [[category-entity-business-rules]].
- **URL-handle changes generate 301 redirects automatically.** Bookmarks and search-engine indexes keep working. See [[category-entity-business-rules]].
- **Publish requires at least one category on every product.** A merchant cannot publish anything until they've created at least one category. See [[product]].

## Where it appears

- [[products-categories]] — the core management screen (List tab + Organize tab + Add / Edit modal).
- [[products-products]] — products are assigned to categories from the product editor; the list also supports filtering by category.
- [[products-property]] — Category Properties are attached to categories here, not directly to products.
- [[product]] — every published product has at least one category.
- Storefront menu navigation — categories drive the default menu structure.
- Storefront search facets — categories appear as filter chips.
- [[analytics-top-categories-by-sales]] — category sales rollups.
- [[analytics-top-categories-by-traffic]] — category traffic rollups.
- [[apps-csv-import]] — bulk-import categories from a spreadsheet (not from the Categories page itself).
- [[apps-google-shopping]] — consumes the `taxonomy_id` for Google Shopping feeds.

## Related

### Related entities

- [[product]] — categories contain products; published products require at least one category.
- [[category-property]] — per-category metadata definitions filled in on the product edit page.
- [[payment-provider]] — categories can restrict allowed providers for orders containing their products.
- [[shipping-provider]] — categories can restrict allowed shipping methods.
- [[blog-category]] — distinct entity (blog content taxonomy, not product taxonomy).
- [[seo-meta]] / [[seo-redirect]] — SEO metadata; URL-handle changes create redirects.
- [[smart-collection]] — alternative rule-based product groupings; not hierarchical.
- [[vendor]] — single brand per product; categories are hierarchical and many-to-many.

### Cross-cutting concepts

- [[variants-model]] — how product + variants + parameters + options compose under each category.
- [[multi-language]] — how category names / descriptions / SEO fields and URL handles are translated per-locale.
- [[seo-handling]] — URL handles, redirects, meta tags.
- [[checkout-flow]] — per-category payment / shipping restrictions are evaluated here.
- [[shipping-calculation]] — categories' allowed-shipping-methods filter applies during this calculation.
- [[import-pipeline]] — CSV / XML / app imports populate the category tree.

### Settings & webhooks

- [[settings-files]] — category images are stored here.
- [[settings-payment-providers]] — providers the per-category restriction picks from.
- [[settings-cart]] — global cart and checkout settings; category restrictions OVERLAY these globals.
- [[marketing-seo-301-redirects]] — URL-handle changes generate redirect entries here.
- [[json-api-v2]] — programmatic-access hub; see [[category-entity-side-effects-and-api]] + [[api-categories]].

## Open Questions

Distributed to aspect pages. See:

- [[category-entity-relationships]] — multi-warehouse interaction; when [[apps-store-locations]] is enabled, whether categories carry per-warehouse stock visibility flags.
