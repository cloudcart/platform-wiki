---
type: entity
nav_path: "Entity → Customer Group"
aliases: ["Customer Group", "Custom Group", "Loyalty Group", "Customer Tier", "Pricing Tier", "B2B Group", "Wholesale Group", "Клиентска група", "Лоялна група", "Ценова група", "VIP клиенти"]
tags: [entity, customers, groups, loyalty, pricing, plan-gated]
plan_gates: ["customer_groups"]
created: 2026-05-23
updated: 2026-06-10
source_count: 8
---

# Customer Group

## Identity

A **Customer Group** is a labeled bucket of [[customer|Customers]] used to differentiate how those customers experience the store — what they see, what they pay, and how they're allowed to check out. The merchant defines groups on [[customers-custom-groups]] (e.g., *"VIP"*, *"Wholesale"*, *"Loyalty Gold"*, *"B2B"*, *"Newsletter only"*) and assigns each customer to exactly one group. Once assigned, the group drives three classes of behavior: **pricing** (discounts can target specific groups, so the merchant can give *"15% off for VIP customers"*); **checkout restrictions** (a [[apps-cart-rules|Cart Rule]] with a customer-group condition can show / hide payment and shipping methods per group, so wholesale customers see invoice-on-delivery while retail customers see only card payments); and **segmentation** (the merchant builds segments of group-X members to target with marketing).

Every customer belongs to **exactly one group** at any moment, including guests — the platform reserves a special "**Guests**" group ID into which every guest checkout falls. Newly registered customers default to a system "**Default**" group (a different ID from the guest group). Merchants then move customers between groups manually (per-customer edit on [[customers-details]]) or in bulk (bulk-action on [[customers]]).

The group's structural simplicity is intentional — it is a **label** the merchant uses to organise customers, with the actual differentiation logic living in the connected entities ([[discount|Discounts]], [[apps-cart-rules|Cart Rules]], segments). The Customer Group feature is **plan-gated**: the merchant's plan caps how many custom groups they can create via the `customer_groups` plan-feature key.

## Aliases

- **Customer Group** / **Custom Group** — the canonical merchant-facing term in CloudCart admin UI.
- **Loyalty Group** / **Customer Tier** — merchant phrasing emphasising rewards / hierarchy.
- **Pricing Tier** — phrasing when the group's purpose is differentiated pricing (B2B / wholesale stores).
- **B2B Group** / **Wholesale Group** — common merchant labels for the wholesale-pricing customer bucket.
- **VIP клиенти** / **Лоялна група** / **Клиентска група** / **Ценова група** — Bulgarian variants merchants use interchangeably.

## Key Attributes

This entity is deliberately thin — the only stored fields are `id` and `name`. Full attribute detail (validation rules, system flags, the no-timestamps quirk, indirect pricing / payment / shipping modifiers) lives on [[customer-group-attributes]]. In summary:

- **Name** — required, max 100 chars, case-insensitive unique per store; *"Default"* is a reserved name.
- **Customers count** — auto-computed; drives the **Has customers: Yes / No** filter.
- **System / Guest flag** — platform-controlled; the Default + Guests groups cannot be deleted or standard-edited.
- **Pricing / Payment / Shipping modifiers** — not stored on the group; achieved indirectly via [[discount|Discounts]] (which carry a `customer_groups` filter) and [[apps-cart-rules|Cart Rules]] (a customer-group condition that gates payment / shipping methods). Payment providers and shipping methods do NOT themselves carry a customer-group field.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[customer-group-attributes]] — the `id` + `name` data shape; name validation strings; the no-`created_at`/`updated_at` quirk; how pricing / payment / shipping differentiation is achieved indirectly rather than stored on the group.
- [[customer-group-system-groups]] — the two reserved system groups (Default + Guests); the one-way guest trap; the case-insensitive *"Default"* reserved-name rule; why "Guests" is NOT reserved by name.
- [[customer-group-pricing-checkout]] — how the group gates differentiated pricing (via discounts), payment-method visibility, and shipping-method visibility; why group changes don't re-price historical orders.
- [[customer-group-lifecycle-deletion]] — created / active / empty / deleted states; the deletion-blocking rules (members + discount references); the dangling-reference risk from DiscountCodePro + Product Selections; empty-group cleanup.
- [[customer-group-segmentation]] — group as the durable segmentation pivot for marketing campaigns; bulk **Set group** on the customer list; the `customer.updated` webhook (no dedicated group-changed event).
- [[customer-group-api]] — JSON-API v2 read / create / update / delete; the side-effects that mirror the admin UI; the plan-cap quirk where both system groups consume slots.

## Where it appears

- [[customers-custom-groups]] — the group list + Add / Edit modal + bulk delete. The home for group taxonomy maintenance.
- [[customer]] — every customer carries a `group_id`. The customer's detail page surfaces the assigned group and lets the merchant change it.
- [[customers]] — the customer list filters by group (column + filter dropdown); the bulk **Set group** action is here.
- [[apps-cart-rules]] — a Cart Rule with a customer-group condition shows / hides payment and shipping methods (and applies fees / gifts) per group at checkout — this is how payment / shipping are group-gated, NOT a field on the provider itself.
- [[marketing-discounts]] (and its variants: [[marketing-discounts-fixed]], [[marketing-discounts-percent]], etc.) — discounts include a customer-group filter to target specific groups.
- [[marketing-segments]] — segment-builder conditions include *Customer group = X*.
- [[reports-customers]] — analytics filter by group for cohort comparison.

## Related

- [[b2b-wholesale]] — B2B & wholesale concept hub.
### Related entities

- [[customer]] — every customer has exactly one group; this is the primary relationship.
- [[discount]] — discounts target groups via `customer_group_ids`.
- [[cart-rule]] — a customer-group condition on a Cart Rule shows / hides payment + shipping methods per group (the actual group→checkout gating mechanism).
- [[segment]] — segments can be built around group membership.
- [[customers-custom-fields]] — sibling customer-metadata mechanism (free-form per-customer fields) — independent of group membership.

### Cross-cutting concepts

- [[customer-group-targeting]] — the concept that ties together everything a group can drive (pricing via discounts, payment/shipping gating via Cart Rules, segmentation).
- [[plan-gates]] — the `customer_groups` count cap.
- [[notification-delivery]] — group membership influences which campaigns reach which subscribers when the campaign's segment is group-defined.
- [[checkout-flow]] — group membership at checkout time determines which payment / shipping options are presented.

## Open Questions

- ⏸️ Whether the "Guests" group can be renamed by the merchant in any UI surface (currently appears to be platform-controlled).
- ⏸️ Whether DiscountCodePro and Product-Selection references should also block group deletion (currently the delete validator only checks standard Discount references).
