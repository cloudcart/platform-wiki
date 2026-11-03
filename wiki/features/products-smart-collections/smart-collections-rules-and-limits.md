---
type: feature
nav_path: "Products → Smart Collections → Rules & limits"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections business rules", "Smart Collections limits", "Smart Collections AND combination", "Smart Collections plan gate", "Smart Collections anti-circular", "Smart Collections 10-row cap"]
tags: [products, collections, selections, rules, limits, plan-gate, validation]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, editor, rule builder, rule types, evaluation, storefront side-effects).

# Smart Collections — rules, limits & plan gate

## Purpose

Every platform invariant that governs smart collections — the AND-combination rule, the hard cap of 10 rows, the anti-circular safeguards on `discount` and `selection` rule types, the `product_collections` plan-gate behaviour, and the permission section that gates the sidebar entry. The canonical reference for support agents diagnosing *"why was my collection rejected on save"*, *"why can't I add another rule"*, *"why is the Add button greyed out"* support tickets.

## Where to find it

The rules apply on the [[smart-collections-editor]] Save and on the **+ Add collection** button on [[smart-collections-list-view]]. The merchant cannot configure any of these limits — they are platform invariants.

## What the merchant can do here

The merchant cannot edit these limits. This page exists to catalogue the verbatim error strings, the AND semantics, and the plan-gate behaviour so support agents and merchants understand the system's boundaries.

## Settings & fields

There are no merchant-facing settings on this aspect — it is a rules reference. The error message strings, the plan-feature key, and the row cap below are verbatim platform values.

### Plan-feature key

| Mapping | Shape | What it controls |
|---|---|---|
| `product_collections` | Numeric (max smart collections) | Per-plan cap on the total number of smart-collection records the merchant can own. The +Add collection button on [[smart-collections-list-view]] checks the cap before opening the create modal; when reached, it opens the plan-upgrade prompt instead. The plan-feature name in the backend is `product_collections` — NOT `collections` (the front-end label says "Collections" but the backend mapping is `product_collections`). Per-pack add-ons available via [[plan-features]]. |

### Row cap

| Cap | Value |
|---|---|
| Maximum rule rows per collection | **10** |

## Business rules

### Rules are AND-combined within a collection

A collection with three rules:

- Category includes "Shoes"
- Price between 100 and 200
- Tag includes "sale"

Matches a product **only when all three conditions are true**. To express OR logic ("Red shirts OR Blue trousers"), the merchant creates multiple collections with different rules. There is no nested clustering or per-row OR option in the [[smart-collections-rule-builder]]. Within a single row, multi-record selectors (e.g., `category` `In` [Shoes, Boots, Sneakers]) DO behave as OR among the picked records — but across rows the combination remains AND.

### Hard cap of 10 rules per collection

Each smart collection accepts a maximum of **10 condition rows** — the merchant cannot add an 11th row in the rule builder. Attempting to save with 11+ rules fails with the verbatim error *"You may have a maximum of 10 rows"*. This is a platform-wide limit (not plan-gated). To express more complex logic, the merchant must split into multiple collections.

### Anti-circular safeguard — self-referential discount loop

A rule can target products in a specific discount (`discount` type — see [[smart-collections-rule-types]]). If a discount is scoped to *this* collection AND the merchant adds an `Include discount` rule listing that discount, save fails with the verbatim error:

> *"The following discounts use this collection in their conditions: {discount name}"*

The validator only blocks `In` operations — `Not in` is allowed because a self-exclusion resolves cleanly (it just excludes the collection's own products from itself, which is a no-op).

### Anti-circular safeguard — collection-of-collections loop

A rule can target products in another smart collection (`selection` type, UI-hidden — see [[smart-collections-rule-types]]). The platform validates that creating this rule does not introduce a cycle. If the target collection itself already references the current collection, save fails with the verbatim error:

> *"The following collections use collection in their conditions: {collection names}"*

Same `In`-only enforcement — `Not in` is allowed.

### Plan-gate cap-reached behaviour

When the merchant has the maximum number of collections their plan allows, clicking +Add collection on [[smart-collections-list-view]] does NOT open the create modal. Instead, the upgrade prompt appears with the verbatim message:

> *"You have reached the maximum number of collections allowed, you need to purchase more to continue."*

Editing or deleting existing collections is unaffected by the cap. Buying more collection slots on the plans page lifts the cap immediately — the +Add button on the list works without a refresh. See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision and [[plan-features]] for the pack-purchase modal flow.

### Permission gate on sidebar visibility

The Smart Collections sidebar entry requires the products / collections permission section. Moderators without it cannot see the entry at all — the page is not reachable by direct URL either, as the route is permission-checked server-side.

### Price-rule validation rules (cross-link)

The price rule has its own per-type validation (cap of 50,000; strict-greater-than for `between`). Catalogued on [[smart-collections-rule-types]] rather than repeated here.

### AND semantics are commutative — order doesn't matter

Because all rows AND together, the persisted `sort_order` on each row has no effect on which products match. The field exists for forward-compatibility with potential UI drag-reorder. See [[smart-collections-rule-builder]].

### Side effects on Save and Delete

Save and Delete on a collection trigger search re-index, storefront page cache flush, and linked-discount re-evaluation. The mechanics are documented on [[smart-collections-storefront-side-effects]].

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-list-view]] — where the +Add cap-reached prompt fires.
- [[smart-collections-editor]] — where the row-cap save error fires.
- [[smart-collections-rule-builder]] — UI for adding rows; the 10-row cap manifests as the +Add criteria button stopping at 10 rows.
- [[smart-collections-rule-types]] — the `discount` and `selection` types that the anti-circular safeguard guards.
- [[smart-collections-storefront-side-effects]] — what fires after a successful Save.
- [[plan-gates]] — the concept page on plan-based feature gating.
- [[plan-vs-feature-pack]] — pack-vs-upgrade decision when the cap is reached.
- [[plan-features]] — per-pack add-on purchase flow.

## Open questions

None.
