---
type: entity
aliases: ["Smart Collection vs Category", "Smart Collection vs Bundle", "Smart Collection vs tag", "Collection relationships", "Rule-based vs manual grouping", "Колекция срещу категория"]
tags: [catalog, products, collections, smart-grouping, relationships, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[smart-collection]]. See the hub for the other aspects (rule builder, evaluation, storefront, discount link, management).

# Smart Collection — relationships & contrasts

## Identity

This aspect maps how a [[smart-collection|Smart Collection]] relates to the other catalog grouping concepts, and — crucially — how it **differs** from each. The defining distinction is **rule-based and auto-populating** vs **manual**: the merchant maintains rules, not a product list. Getting this contrast right is what keeps merchants from confusing a Smart Collection with a [[category|Category]], a [[bundle|Bundle]], a tag, or a Linked-products list.

## Aliases

- "Rule-based grouping" vs "manual grouping" — the framing of the core contrast.
- "Dynamic collection" vs "category" — the most common merchant confusion this page resolves.
- Bulgarian: "Колекция срещу категория".

## Key Attributes

### What a Smart Collection relates to

A Smart Collection:

- **Dynamically includes many** [[product|Products]] — membership is computed from the rules and cached on the record. The relationship is **rule-based, not a hard FK**: there is no `selection_product` pivot the merchant maintains. Adding a product whose data matches adds it on the next evaluation cycle; editing a product so it no longer matches removes it. See [[smart-collection-entity-evaluation]].
- **References** [[category|Categories]] (via the Categories rule field), [[vendor|Vendors / Manufacturers]] (via the Manufacturer field), product tags (via the Tags field), [[discount|Discounts]] (via the Discounts field — active fixed / percent / flat, non-shipping, non-customer-restricted), and [[category-property|Category Properties]] + options (via the Category property field). See [[smart-collection-entity-rule-builder]].
- **Is referenced by** [[discount|Discounts]] as a selection target — the discount's effective set follows the collection's rules. See [[smart-collection-entity-discount-link]].
- **Is referenced by** storefront navigation / menu items — a menu entry can link to `/selection/<url-handle>`. See [[smart-collection-entity-storefront]].
- **Is NOT referenced by** [[order|Orders]] directly — orders snapshot product lines, not collection memberships.

### What a Smart Collection is NOT

| Concept | How it differs from a Smart Collection |
|---------|----------------------------------------|
| **[[category|Category]]** | Categories are a hierarchical, manually-curated taxonomy with a tree of parents / children and explicit per-product assignment. Smart Collections are flat, rule-based, and auto-populating. (Category is also one of the criteria *fields*.) |
| **[[bundle|Bundle]]** | Bundles are fixed sets of specific products sold as one SKU. Smart Collections are dynamic groupings used for browsing / discounting, not for selling as one unit. |
| **Product tag** | Tags are free-form labels without a landing page or rules. Smart Collections have both a landing page and rules. (Tags are also one of the criteria fields.) |
| **Linked products** | The per-product "Linked products" cross-sell list on the product editor is **manual**. Smart Collections are rule-based. |

### Why merchants reach for each

- **Smart Collection** — "I want a page / promotion that auto-updates as my catalog changes" (e.g. everything on sale, everything under 50 BGN).
- **Category** — "I want a stable, hand-curated navigation taxonomy."
- **Bundle** — "I want to sell several products together as one purchasable item."
- **Tag** — "I want a lightweight label for filtering / search, no landing page needed."

## Where it appears

- [[products-smart-collections]] — Smart Collections live here; contrast surfaces when merchants ask "should this be a collection or a category?".
- [[products-categories]] — the manual alternative.
- [[products-products]] — Linked products (the manual cross-sell list) lives on the product editor.

## Related

- [[smart-collection]] — hub.
- [[category]] — manual hierarchical alternative; also a criteria field.
- [[bundle]] — fixed product set sold as one SKU.
- [[product]] — the entity collections dynamically include.
- [[vendor]] — referenced via the Manufacturer field.
- [[category-property]] — referenced via the Category property field.
- [[discount]] — references the collection as a selection target.
- [[order]] — does NOT reference collection memberships (snapshots product lines).

## Open Questions

None.
