---
type: feature
nav_path: "Products → Smart Collections → Storefront & side effects"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections storefront", "Selection storefront URL", "/selection route", "Smart Collections side effects", "Smart Collections search re-index", "Smart Collections AJAX endpoints"]
tags: [products, collections, selections, storefront, ajax, side-effects, search]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, editor, rule builder, rule types, evaluation, rules and limits).

# Smart Collections — storefront & save-time side effects

## Purpose

What happens once a collection is saved and the regeneration finishes: the storefront landing page becomes reachable, the search index updates so storefront search reflects the new grouping, the storefront page cache flushes, and any linked discounts re-evaluate. This page catalogues the storefront URL contract, the AJAX endpoints the theme uses to lazy-load collection content, and the side-effect chain triggered by Save and Delete.

## Where to find it

The storefront landing page is at `/selection/<url-handle>` on the merchant's storefront — the URL handle is configured on [[smart-collections-editor]]. The admin entry points are [[smart-collections-list-view]] and the editor — the side-effects fire automatically; there is no merchant-facing settings screen for them.

## What the merchant can do here

The merchant cannot configure the storefront URL prefix or the side-effect chain — they are platform behaviours. What they can do is:

- **Configure the URL handle** for each collection on [[smart-collections-editor]] — this controls the slug after `/selection/`.
- **Configure SEO** (title, description, canonical) for the landing page on [[smart-collections-editor]].
- **Link collections to storefront modules** (e.g., a collection grid block) via the storefront theme / design surface — not from this feature directly.

## Settings & fields

### Storefront route — `/selection/<slug>`

CloudCart auto-generates a storefront landing page at `/selection/<url-handle>` showing all products matching the collection. The `/selection/` prefix is **hardcoded** — not merchant-configurable. The slug comes from the `url_handle` field on the selection record (see [[smart-collections-editor]]).

### AJAX endpoints under `/selection/`

The theme lazy-loads collection content via three AJAX endpoints rooted under the same prefix:

| Endpoint name | Purpose |
|---|---|
| `ajax.selection` | Products lazy-load — paginated product list for the landing page. |
| `ajax.products.selection` | Products-only render — the product grid block without the page chrome. |
| `ajax.filters-ts.selection` | Filter sidebar — the faceted-filter facet counts for the collection's product set. |

The theme calls these endpoints when the customer scrolls or applies a filter — keeping initial-page weight light.

### Time-series tracking on `/selection/` routes

All routes under `/selection/` carry time-series-statistic middleware — every storefront visit is captured for time-series analytics. This feeds downstream reports such as [[reports-customers]] and similar visit-based dashboards.

## Business rules

### The `/selection/` prefix is platform-wide and cannot be changed

The merchant configures only the slug after the prefix (the `url_handle`). Even with a custom storefront theme, the route registration for `/selection/<slug>` is owned by the platform. To present a collection under a different URL (e.g., `/sale-2026`), the merchant would need to use a storefront redirect rule (see [[marketing-seo-301-redirects]]) — but the canonical URL remains `/selection/<slug>`.

### Side effects on Save and Delete

When the merchant saves or deletes a smart collection, three side-effect chains fire automatically:

- **Search re-index.** The platform updates the search index for the products in the (new or old) collection's product set so the storefront search reflects the new grouping. For very large collections this can mean a sizeable re-index batch — see [[background-queue-inventory]] for the relevant queue behaviour.
- **Storefront page cache flush.** The collection's landing page (`/selection/<slug>`) and any storefront module showing the collection are flushed from the storefront page cache. The next customer visit re-renders from the cached `products` field on the selection (see [[smart-collections-evaluation]]).
- **Discount re-evaluation.** If discounts are linked to the collection, they are re-evaluated to apply to the new product set. Linked-discount visibility on the list page (the Discounts column on [[smart-collections-list-view]]) reflects this binding.

### Adding a new product can ripple into the collection's storefront cache

Because the platform re-evaluates affected collections on product changes (see [[smart-collections-evaluation]]), a new product that matches a collection's rules ripples into that collection's storefront landing page after the regeneration job finishes AND the page-cache flush triggers. The merchant should expect a short delay — typically seconds — between adding a product and seeing it on `/selection/<slug>`.

### Removing a collection does not cascade to its discounts

Deleting a collection from [[smart-collections-list-view]] removes the collection record but does NOT delete any discount that was scoped to it. The discount remains, now scoped to a no-longer-existing collection — the merchant must re-target the discount manually. (verify cascade semantics)

### Per-product membership is read-only from the product editor

On the product Edit page (Smart Collections aside section in [[products-products]]), the merchant sees which collections the product currently belongs to. They cannot manually add the product to a collection from there — they would need to modify the collection's rules to include the product. This is by design — smart collections are rule-defined, not list-defined.

### Discounts can target collections

A common pattern: the merchant creates a collection ("Summer Sale 2026") with rules, then creates a discount in the Discounts feature scoped to that collection. The discount applies to whatever products currently match the collection's rules — when the merchant adds new products that match, they automatically get the discount; when products are removed, they lose it. The Discounts column on [[smart-collections-list-view]] surfaces the linked discount(s) per collection so the merchant can see at a glance which collections drive promotional campaigns.

### Storefront landing page metadata

SEO title, description, canonical, and URL handle on [[smart-collections-editor]] control the page's `<head>` metadata. Blank SEO fields fall back to platform defaults (collection name as `<title>`, no `<link rel=canonical>`).

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-editor]] — where URL handle + SEO are configured.
- [[smart-collections-list-view]] — surfaces the Discounts column showing linked discounts.
- [[smart-collections-evaluation]] — the regeneration job whose output feeds the storefront cache.
- [[selection]] — the storefront-page wiki entry for `/selection/<slug>`.
- [[products-products]] — per-product collection memberships visible on the product editor.
- [[marketing-seo-301-redirects]] — the only way to surface a collection under a non-`/selection/` URL.
- [[background-queue-inventory]] — the search-re-index queue pressure on bulk operations.
- [[reports-customers]] — visit-based reports that consume the time-series tracking.

## Open questions

- (verify) Does deleting a collection cascade to remove or re-scope any discount that referenced it, or does the discount silently lose its scope?
