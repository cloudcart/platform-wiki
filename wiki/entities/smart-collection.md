---
type: entity
aliases: ["Smart Collection", "Collection", "Selection", "Dynamic collection", "Smart group", "Rule-based collection", "Колекция", "Селекция", "Динамична колекция"]
tags: [catalog, products, collections, smart-grouping, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Smart Collection

## Identity

A **Smart Collection** is a **rule-based, dynamic product grouping** in the merchant's catalog — a named container whose membership is computed from criteria the merchant defines, not hand-picked. The merchant writes a set of rules like *"all products with price above 100 BGN AND in category Electronics"* or *"all products tagged 'summer' that are on sale"*, and CloudCart continuously evaluates which products match. The merchant doesn't maintain the product list — they maintain the rules; the platform refreshes membership whenever any underlying product changes (price, category, vendor, tags, properties, etc.). Each Smart Collection has its own storefront landing page at `/selection/<url-handle>`, can be linked from menu navigation, and can be referenced as a selection target by a [[discount]] so promotional pricing follows the rules automatically.

A Smart Collection is distinct from a [[category|Category]] (a manually-curated hierarchical taxonomy where the merchant assigns products one-by-one), a **product tag** (a free-form label without rules or a landing page), and a [[bundle|Bundle]] (a fixed set of specific products sold as one SKU). It is also distinct from the per-product **Linked products** list (a manual cross-sell list). For the full distinction and the relationship map, see [[smart-collection-entity-vs-category]]. For the management screen see [[products-smart-collections]].

## Aliases

- "Smart Collection" — the canonical merchant-facing wiki term.
- "Collection" — the short form; the wiki prefers "Smart Collection" because [[category|Category]] is sometimes called "Collection" by other platforms.
- "Selection" — the platform's internal label, surfacing in the URL pattern (`/selection/<slug>`) and the AJAX endpoint names (`ajax.selection`, `ajax.products.selection`, `ajax.filters-ts.selection`).
- "Dynamic collection" / "Smart group" / "Rule-based collection" — informal merchant language emphasising the auto-updating behaviour.
- Bulgarian: "Колекция", "Селекция", "Динамична колекция".

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[smart-collection-entity-rule-builder]] — the criteria model: 10 supported Fields, per-field Operators, Values, AND-combination, and why there is no collection-level OR.
- [[smart-collection-entity-evaluation]] — async evaluation, the cached `products` list, the `executing` Status flag (Pending / Finished), `last_generated_at`, latency at scale, debounce, and save / delete side effects.
- [[smart-collection-entity-storefront]] — the `/selection/<url-handle>` landing page, AJAX lazy-load endpoints, the Advanced SEO section (URL handle, SEO title / description, canonical), and image / thumbnail handling.
- [[smart-collection-entity-discount-link]] — how a [[discount]] targets a Smart Collection so promotional pricing follows the rules, plus the Pending-link and re-evaluation semantics.
- [[smart-collection-entity-vs-category]] — relationships and contrasts: vs Category, vs Bundle, vs tag, vs Linked products; what references a collection and what does not.
- [[smart-collection-entity-management]] — the lifecycle states, the `collections` plan gate, the permission section, and where per-product membership surfaces on the product editor.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** | Set on create / edit on [[products-smart-collections]] | Required. Used as the storefront landing page heading, the admin list label, and the in-product "Smart Collections" aside section. |
| **Description** | Free text on the edit modal | Long-form description shown on the storefront landing page above the product grid. |
| **Image** | Single image upload on the edit modal | Shown on collection cards and storefront listings. See [[smart-collection-entity-storefront]]. |
| **Conditions / criteria** (`rows[]`) | Rule builder on the edit modal | One or more rows; each row is one rule (Field + Operator + Value) with a `sort_order`. See [[smart-collection-entity-rule-builder]]. |
| **URL handle / SEO / canonical** | Advanced section of the edit modal | Storefront slug + `<title>` / `<meta description>` / `rel="canonical"` overrides. See [[smart-collection-entity-storefront]]. |
| **Status** (`executing`) | n/a (set by the platform) | `Pending` = membership being re-evaluated; `Finished` = cached list current. See [[smart-collection-entity-evaluation]]. |
| **Last generated at** (`last_generated_at`) | n/a | Timestamp of the most recent membership refresh. |
| **Cached product list** (`products`) | n/a (computed from rules) | Resolved product IDs denormalised onto the record; the storefront reads this cache. See [[smart-collection-entity-evaluation]]. |
| **Products count** | n/a (derived) | Shown in the Products column on the list page; number-formatted; sortable. |
| **Discounts linked** | n/a (derived) | When a linked discount exists, a Discounts column surfaces it. See [[smart-collection-entity-discount-link]]. |

## Where it appears

- [[products-smart-collections]] — the master management screen (List + Add / Edit modal). Where the merchant creates, edits, deletes, and bulk-deletes collections.
- [[products-products]] — the product editor surfaces a Smart Collections aside section showing which collections this product currently belongs to (read-only). See [[smart-collection-entity-management]].
- [[products-categories]] — categories appear as one of the criteria fields (Categories).
- [[products-vendors]] — vendors appear as one of the criteria fields (Manufacturer).
- [[products-property]] — category properties and their options appear as the Category property criteria field.
- [[marketing-discounts]] — discounts can target Smart Collections as their selection scope.
- Storefront landing page at `/selection/<url-handle>` — auto-generated. See [[smart-collection-entity-storefront]].
- Menu navigation entries can link to a Smart Collection landing page.

## Related

- [[products-smart-collections]] — the management feature.
- [[product]] — every Smart Collection dynamically includes many Products via rule matching; product changes trigger re-evaluation.
- [[category]] — manual, hierarchical alternative; also a criteria field.
- [[vendor]] — appears as the Manufacturer criteria field.
- [[discount]] — discounts can target Smart Collections.
- [[bundle]] — fixed product set sold as one SKU; contrasts with Smart Collection.
- [[category-property]] — properties appear in the Category property criteria field.
- [[plan]] — the `collections` plan feature caps how many Smart Collections the merchant can create.
- [[merchant-roles]] — permission section that gates this feature for Moderators.

## Open Questions

No outstanding questions — all items resolved or distributed to sub-pages.
