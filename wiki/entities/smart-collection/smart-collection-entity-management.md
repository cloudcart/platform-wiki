---
type: entity
aliases: ["Smart Collection lifecycle", "Smart Collection management", "Collections plan gate", "Smart Collection permission", "Per-product collection membership", "Управление на колекции"]
tags: [catalog, products, collections, smart-grouping, lifecycle, plan-gate, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[smart-collection]]. See the hub for the other aspects (rule builder, evaluation, storefront, discount link, vs category).

# Smart Collection — lifecycle, plan gate & permission

## Identity

This aspect covers the **operational lifecycle** of a [[smart-collection|Smart Collection]] — from creation through re-evaluation to deletion — plus the two gates that govern access (the `collections` plan feature and the products / collections permission section) and where per-product membership surfaces on the product editor.

## Aliases

- "Lifecycle" — the create → evaluate → live → re-evaluate → delete sequence.
- "Plan gate" / "`collections` feature" — the per-store cap.
- "Smart Collections aside" — the read-only membership panel on the product editor.
- Bulgarian: "Управление на колекции".

## Key Attributes

### Lifecycle states

1. **Created.** On [[products-smart-collections]] the merchant clicks **+ Add collection**, passes the plan-gate check (`collections`), and fills the name + at least one criteria row (see [[smart-collection-entity-rule-builder]]). On submit the record is saved and the async evaluation job is queued; status starts as **Pending**.
2. **Evaluating (Pending).** The platform iterates the catalog against the rules and writes matching product IDs into the cached `products` field. The storefront serves an empty list until the first evaluation completes. See [[smart-collection-entity-evaluation]].
3. **Live (Finished).** Once the job completes, `executing` flips to false and `last_generated_at` updates; the Status badge reads Finished. The storefront landing page now shows the matching products.
4. **Re-evaluated.** A rule / metadata edit OR an underlying product change re-runs evaluation; the collection re-enters Pending until the job completes. See [[smart-collection-entity-evaluation]].
5. **Deleted.** The merchant uses per-row Delete on the list, or the bulk-delete action with multi-row selection. Save / delete side effects (search re-index, storefront cache flush, discount re-evaluation) are covered in [[smart-collection-entity-evaluation]].

### Plan-gated — the `collections` plan feature caps the count

The number of Smart Collections per store is capped by the `collections` plan feature. The page header shows current usage as `<used> / <limit>`. When the cap is reached, **+ Add collection** opens the [[plan-features]] upgrade modal with the message *"You have reached the maximum number of collections allowed, you need to purchase more to continue."* See [[plan-gates]] for the gating concept.

### Permission

The Smart Collections screen requires the products / collections permission section. Moderators without it cannot see the Smart Collections sidebar entry. The Owner holds the permission implicitly. See [[merchant-roles]].

### Per-product membership is visible from the product editor (read-only)

On the product Edit page (the **Smart Collections aside section** in [[products-products]]), the merchant sees which Smart Collections this product currently belongs to. They **CANNOT** manually add the product to a Smart Collection from the product editor — to include a specific product, the merchant must modify the collection's rules. This is the visible consequence of the rule-based, no-pivot relationship described in [[smart-collection-entity-vs-category]].

## Where it appears

- [[products-smart-collections]] — the master management screen (List + Add / Edit modal + bulk delete + usage counter).
- [[products-products]] — the read-only Smart Collections aside section on the product editor.
- [[plan-features]] — the upgrade modal shown when the `collections` cap is reached.

## Related

- [[smart-collection]] — hub.
- [[smart-collection-entity-evaluation]] — the Pending / Finished states and save / delete side effects.
- [[smart-collection-entity-rule-builder]] — the criteria filled in at creation.
- [[smart-collection-entity-vs-category]] — why membership is read-only on the product editor.
- [[products-smart-collections]] — the management feature.
- [[products-products]] — the product editor aside section.
- [[plan]] — the `collections` plan feature.
- [[plan-features]] — the upgrade modal.
- [[plan-gates]] — the plan-gating concept.
- [[merchant-roles]] — the permission section.

## Open Questions

None.
