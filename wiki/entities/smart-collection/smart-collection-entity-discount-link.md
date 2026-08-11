---
type: entity
aliases: ["Smart Collection discount link", "Discount targeting a collection", "Selection discount scope", "Promotional pricing follows rules", "Отстъпка върху колекция"]
tags: [catalog, products, collections, smart-grouping, discounts, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[smart-collection]]. See the hub for the other aspects (rule builder, evaluation, storefront, vs category, management).

# Smart Collection — discount linking

## Identity

A [[discount|Discount]] can be **scoped to a Smart Collection** as its selection target. When that happens, the discount applies to whatever products currently match the [[smart-collection|Smart Collection]]'s rules — so promotional pricing **follows the rules automatically**. As the collection adds or removes products (because product data changed, or the merchant edited a rule), the discount's effective set follows. This aspect covers the linking pattern, where it is managed, and the timing semantics when a collection is still evaluating.

## Aliases

- "Discount link" / "linked discount" — a discount scoped to a collection.
- "Selection target" — the platform's framing of a collection used as a discount scope.
- Bulgarian: "Отстъпка върху колекция".

## Key Attributes

### Discounts target collections — promotional pricing follows the rules

A common pattern: create a Smart Collection (e.g. "Summer Sale 2026") with its rules, then create a [[discount|Discount]] scoped to that collection. The discount applies to whatever products currently match the rules:

- When the merchant adds new products that match → they automatically get the discount.
- When products stop matching → they lose the discount.

The link is to the **collection**, not to a snapshot of its products at link time — see the Pending-evaluation note below.

### The link is managed from the discount form, not the collection

The merchant creates and manages the link **from the discount form** (see [[marketing-discounts]]), choosing the Smart Collection as the discount's scope. The collection's edit modal does not link discounts. On the [[products-smart-collections]] list, when at least one collection has a linked discount, an extra **Discounts column** surfaces the linked discount name(s) per row, so the merchant can see at a glance which collections drive promotional campaigns.

### Linking during a Pending evaluation

If the merchant links a discount to a **Pending** collection (one still being evaluated — see [[smart-collection-entity-evaluation]]), the discount IS re-evaluated automatically when the collection's evaluation settles, because the link is to the **collection**, not to a snapshot. The discount applies to whatever set the collection resolves to once it reaches Finished. Practical guidance: assigning while Pending is safe in that the link follows the settled set — but the merchant should confirm the collection reaches Finished before relying on the promotion being live.

### Re-evaluation keeps the discount in sync

Whenever the collection's membership is re-evaluated (rule edit or underlying product change), any linked discounts are **re-evaluated against the new product set** as a save / delete side effect (see [[smart-collection-entity-evaluation]]). The merchant does not need to re-touch the discount.

### Eligible discount types as a criteria field too

Note the inverse relationship: **Discounts** is also one of the criteria *Fields* in the rule builder (see [[smart-collection-entity-rule-builder]]), limited to currently-active fixed / percent / flat, non-shipping, non-customer-restricted discounts. That lets a collection select "products that currently have discount X" — distinct from a discount targeting the collection.

## Where it appears

- [[marketing-discounts]] — where the discount → collection link is created and managed.
- [[products-smart-collections]] — the Discounts column surfaces linked discounts per collection.

## Related

- [[smart-collection]] — hub.
- [[discount]] — the entity that targets the collection.
- [[smart-collection-entity-evaluation]] — membership settling drives discount re-evaluation.
- [[smart-collection-entity-rule-builder]] — Discounts is also a criteria field (the inverse relationship).
- [[marketing-discounts]] — the discount management feature.

## Open Questions

None.
