---
type: entity
nav_path: "Entity → Customer Group → Pricing & checkout"
aliases: ["Customer Group pricing", "Group-based pricing", "Group payment restrictions", "Group shipping restrictions", "B2B pricing tier", "Wholesale discount group", "Групово ценообразуване", "Ограничения по група"]
tags: [entity, customers, groups, pricing, discounts, checkout]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customer-group]]. See the hub for the other aspects (attributes, system groups, lifecycle & deletion, segmentation, API).

# Customer Group — Pricing & checkout

## Identity

This aspect documents the three differentiation behaviours a [[customer-group|Customer Group]] drives at storefront / checkout time: **pricing** (via group-targeted discounts), and **payment- / shipping-method visibility** (via [[apps-cart-rules|Cart Rules]] with a customer-group condition). In every case the group is just a label — pricing differentiation is configured on the **discount** (which carries a `customer_group_ids` filter), and checkout-method gating is configured on a **Cart Rule** (a customer-group condition that shows / hides methods). Payment providers and shipping methods themselves carry **no** customer-group field.

## Aliases

- **Customer Group pricing** / **Group-based pricing** / **Групово ценообразуване** — the discount-targeting angle.
- **B2B pricing tier** / **Wholesale discount group** — the common merchant use case.
- **Group payment restrictions** / **Group shipping restrictions** / **Ограничения по група** — the checkout-gating angle.

## Key Attributes

| Gate | Lives on | Mechanism | Empty means |
|------|----------|-----------|-------------|
| **Pricing** | [[discount\|Discount]] (incl. free-shipping discounts, [[marketing-discounts-code-pro\|Code PRO]]) | `customer_group_ids` filter — discount applies only to in-group customers. | Discount applies to all customers. |
| **Payment visibility** | [[cart-rule\|Cart Rule]] (customer-group condition) | A rule conditioned on the buyer's group shows / hides payment methods at checkout. | No group-based payment gating. |
| **Shipping visibility** | [[cart-rule\|Cart Rule]] (customer-group condition) | A rule conditioned on the buyer's group shows / hides shipping methods at checkout. | No group-based shipping gating. |

### Group is the gate for differentiated pricing

The CloudCart pattern for differentiated pricing is: create a Customer Group → create one or more [[discount|Discounts]] that target that group via `customer_group_ids` → assign relevant customers to the group. The discount applies automatically at checkout for in-group customers; out-of-group customers never see it.

This means the group itself stores no pricing modifier (see [[customer-group-attributes]]). A merchant who wants *"Wholesale = 30% off everything"* creates a Discount of type `percent` with `customer_group_ids = [wholesale]` and `apply_to = all_products`.

### Group gates payment- and shipping-method visibility — via Cart Rules

Payment-method and shipping-method visibility-by-group is **not** a field on the provider. It is configured with a [[apps-cart-rules|Cart Rule]] that has a **customer-group condition**: "when the buyer is in group X, hide / show these payment (or shipping) methods." Common use: **Invoice (deferred payment)** shown only to Wholesale / B2B groups while retail customers see only card payments; **Same-day courier** shown only to a "Local Sofia" group. (Group-based **free shipping** is the one exception that lives on the discount side — a free-shipping [[discount]] with a `customer_groups` filter, evaluated per group at checkout.)

### Group changes do NOT propagate to historical orders

Moving a customer from "Retail" to "VIP" does NOT retroactively re-price or re-flag the customer's PAST orders. Past orders snapshotted the customer's group at order time; future orders use the new group. This is intentional — historical accounting stays stable. The differentiation (discount, payment, shipping) is evaluated at the moment of checkout against the customer's group *then*, never re-run against old orders.

## Where it appears

- [[marketing-discounts]] (and variants [[marketing-discounts-fixed]], [[marketing-discounts-percent]], etc.) — the discount editor's group-restriction picker.
- [[apps-cart-rules]] — the Cart Rule editor's customer-group condition that gates payment / shipping methods per group.
- [[checkout-flow]] — where group membership is read to decide which payment / shipping options to present and which discounts to apply.

## Related

- [[customer-group]] — hub.
- [[discount]] — stores the group-targeted pricing rule (and group-gated free shipping).
- [[cart-rule]] / [[apps-cart-rules]] — the customer-group condition that shows / hides payment + shipping methods per group.
- [[checkout-flow]] — evaluates group membership at order time.

## Open Questions

None.
