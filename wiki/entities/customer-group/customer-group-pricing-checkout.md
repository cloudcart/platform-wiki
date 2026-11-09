---
type: entity
nav_path: "Entity → Customer Group → Pricing & checkout"
aliases: ["Customer Group pricing", "Group-based pricing", "Group payment restrictions", "Group shipping restrictions", "B2B pricing tier", "Wholesale discount group", "Групово ценообразуване", "Ограничения по група"]
tags: [entity, customers, groups, pricing, discounts, checkout]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[customer-group]]. See the hub for the other aspects (attributes, system groups, lifecycle & deletion, segmentation, API).

# Customer Group — Pricing & checkout

## Identity

This aspect documents what a [[customer-group|Customer Group]] drives at checkout: **pricing**, through group-targeted discounts and [[apps-cart-rules|Cart Rules]] with a customer-group condition. The group is just a label. **Payment and shipping methods cannot be shown or hidden per group**: they carry no group field, and neither discounts nor Cart Rules (whose only action is a discount) change which methods appear.

## Aliases

- **Customer Group pricing** / **Group-based pricing** / **Групово ценообразуване** — the discount-targeting angle.
- **B2B pricing tier** / **Wholesale discount group** — the common merchant use case.
- **Group payment restrictions** / **Group shipping restrictions** / **Ограничения по група** — what merchants ask for; not available per group (see below).

## Key Attributes

| Gate | Lives on | Mechanism | Empty means |
|------|----------|-----------|-------------|
| **Pricing** | [[discount\|Discount]] (incl. free-shipping discounts, [[marketing-discounts-code-pro\|Code PRO]]) | `customer_group_ids` filter — discount applies only to in-group customers. | Discount applies to all customers. |
| **Pricing (rules)** | [[cart-rule\|Cart Rule]] (customer-group condition) | A rule's discount applies only to the selected groups. | — |
| **Payment / shipping visibility** | Nothing group-based | Checkout narrows methods by order amount limits, the products' categories ([[products-categories-cart-restrictions]]), the chosen shipping method and some apps — never by group. | — |

### Group is the gate for differentiated pricing

The CloudCart pattern for differentiated pricing is: create a Customer Group → create one or more [[discount|Discounts]] that target that group via `customer_group_ids` → assign relevant customers to the group. The discount applies automatically at checkout for in-group customers; out-of-group customers never see it.

This means the group itself stores no pricing modifier (see [[customer-group-attributes]]). A merchant who wants *"Wholesale = 30% off everything"* creates a Discount of type `percent` with `customer_group_ids = [wholesale]` and `apply_to = all_products`.

### No group gating of payment or shipping methods

A merchant who wants *"invoice payment only for B2B"* cannot set it per group: providers and shipping methods have no group field, and [[apps-cart-rules|Cart Rules]] only discount. What a group can change is the price, including shipping: a free-shipping [[discount]] with a `customer_groups` filter, or a Cart Rule's free-shipping action on a group condition. Method restrictions exist only per product category ([[products-categories-cart-restrictions]]).

### Group changes do NOT propagate to historical orders

Moving a customer from "Retail" to "VIP" does NOT retroactively re-price or re-flag the customer's PAST orders. Past orders snapshotted the customer's group at order time; future orders use the new group. This is intentional — historical accounting stays stable. The differentiation (discounts) is evaluated at the moment of checkout against the customer's group *then*, never re-run against old orders.

## Where it appears

- [[marketing-discounts]] (and variants [[marketing-discounts-fixed]], [[marketing-discounts-percent]], etc.) — the discount editor's group-restriction picker.
- [[apps-cart-rules]] — the Cart Rule editor's customer-group condition (discounts only).
- [[checkout-flow]] — where group membership is read to decide which discounts apply.

## Related

- [[customer-group]] — hub.
- [[discount]] — stores the group-targeted pricing rule (and group-gated free shipping).
- [[cart-rule]] / [[apps-cart-rules]] — the customer-group condition on a rule's discount.
- [[checkout-flow]] — evaluates group membership at order time.

## Open Questions

None.
