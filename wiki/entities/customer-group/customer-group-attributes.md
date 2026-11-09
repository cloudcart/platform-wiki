---
type: entity
nav_path: "Entity → Customer Group → Attributes"
aliases: ["Customer Group attributes", "Group name validation", "Customer Group fields", "Group pricing modifier", "Атрибути на клиентска група", "Име на група"]
tags: [entity, customers, groups, validation, plan-gated]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[customer-group]]. See the hub for the other aspects (system groups, pricing & checkout, lifecycle & deletion, segmentation, API).

# Customer Group — Attributes

## Identity

This aspect documents the **data shape** of a [[customer-group|Customer Group]] — what fields it actually stores, how the **Name** is validated, and why the group itself carries no pricing / payment / shipping modifier. The structural simplicity is intentional: a Customer Group is a **label** that other entities reference, not a container of differentiation rules. The only stored fields on the group record are `id` and `name`.

## Aliases

- **Customer Group attributes** / **Customer Group fields** — the canonical phrasing.
- **Group name validation** — the validation-strings angle (when a merchant hits an error saving a group).
- **Group pricing modifier** — the (mistaken) expectation that the group stores a discount percentage; it does not.
- **Атрибути на клиентска група** / **Име на група** — Bulgarian variants.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** | Required, max **100** chars, case-insensitive unique | The label displayed in customer-list filters, the bulk-edit modal, the per-customer Edit screen, and admin reports. Validation errors: *"Group name is required"* (empty), *"Group name must not exceed 100 characters"* (too long), *"Group name already exists"* (duplicate within the merchant's store, case-insensitive), *"Group name is reserved"* (when the merchant tries to name a group exactly "Default" — case-insensitive match), *"Group limit reached"* (plan cap hit). Placeholder: *"E.g. Loyal, VIP"*. |
| **Customers count** | Auto-computed | How many customers currently sit in this group. Surfaces on the group list and drives the **Has customers: Yes / No** filter. |
| **System / Guest flag** | Platform-controlled | Two special groups (Default + Guests) cannot be deleted or standard-edited — see [[customer-group-system-groups]]. |
| **Timestamps** | Not tracked | The group record has NO `created_at` / `updated_at` columns — the only stored fields are `id` and `name`. Group lists are sorted by `id DESC` (newest-id first) instead of date. |
| **Pricing modifier** | Discount targeting (indirect) | The group itself doesn't carry a pricing field — pricing differentiation is achieved by creating [[discount|Discounts]] that target the group (the Discount's `customer_group_ids` filter). See [[customer-group-pricing-checkout]]. |
| **Payment / shipping restrictions** | Not available per group | Providers and shipping methods have no group field, and [[apps-cart-rules|Cart Rules]] only discount. Method restrictions exist per product category only ([[products-categories-cart-restrictions]]). |

### The group stores no differentiation logic

The single most-misunderstood point about this entity: a Customer Group does **not** store a discount percentage, a price list, or a payment / shipping allow-list. All differentiation lives on the connected entities and points *back* at the group:

- A discount carries `customer_group_ids` → "this discount applies to these groups". See [[customer-group-pricing-checkout]].
- A [[apps-cart-rules|Cart Rule]] carries a customer-group **condition** → "when the buyer is in this group, apply this discount (amount, percent or free shipping)". Nothing shows or hides payment / shipping methods per group.

So "Wholesale gets 30% off" is **not** a property of the Wholesale group — it is a [[discount|Discount]] of type `percent` with `customer_group_ids = [wholesale]`. The group is just the durable label both sides agree on.

### Name uniqueness and the reserved name

The validation *"Group name already exists"* enforces case-insensitive uniqueness within the merchant's store — a merchant CAN have a "VIP" group, but cannot have two ("vip" + "VIP" collide). Separately, *"Default"* is a **reserved** name (case-insensitive) that the platform refuses for any custom group — that rule and the system-group protections are documented on [[customer-group-system-groups]].

## Where it appears

- [[customers-custom-groups]] — the Add / Edit modal where Name is entered and the validation strings surface.
- [[customer]] — every customer carries a `group_id` pointing at one group record.
- [[customers]] — the customer list shows the group name column and the **Has customers** filter (driven by the auto-computed count).
- [[apps-cart-rules]] — group-conditioned discounts (no payment / shipping show-hide).

## Related

- [[customer-group]] — hub.
- [[customer]] — carries the `group_id` FK.
- [[discount]] — the entity that stores the actual pricing differentiation.
- [[plan-gates]] — the `customer_groups` count cap that surfaces as *"Group limit reached"*.

## Open Questions

None.
