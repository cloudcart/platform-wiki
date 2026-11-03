---
type: feature
nav_path: "Marketing → Discounts → Quantity → Quantity counting"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/quantity
aliases: ["Quantity counting", "Count the quantity from all cart lines of the product", "quantity_count_all_lines", "Quantity discount per cart line", "Quantity discount across variants", "Sizes do not add up to a tier", "Брой от всички редове в количката", "Количествена отстъпка по варианти", "Отстъпка за количество на ред"]
tags: [marketing, discounts, quantity, cart, variants, personalisation]
plan_gates: ["discount_quantity"]
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, stacking, uniqueness constraint, plan gating, storefront display).

# Quantity discount — counting per cart line or across all lines

## Purpose

A customer can add the same product to the cart on several lines: different variants, or the same variant with different personalisations such as uploaded photos. This aspect documents the per-discount switch that decides whether those lines add up toward a tier. **By default each line counts alone.**

## Where to find it

**Marketing → Discounts → Quantity discount**, on the create form (`/admin/marketing/discounts/create/quantity`) or the edit form (`/admin/marketing/discounts/edit/{id}`), in the box **Quantity counting**. The box's help text reads:

> *"Choose how the quantity for the discount tiers is counted when the product is added to the cart on several lines (different variants or personalisations)."*

## What the merchant can do here

- Leave the switch off, so each cart line reaches a tier with its own quantity.
- Turn it on, so the pieces of the product on all cart lines add up.

## Settings & fields

| Field | Key | Default | What it does |
|---|---|---|---|
| **Count the quantity from all cart lines of the product** | `quantity_count_all_lines` | Off | Per discount. Off: each line counts alone. On: all lines of the product count together. |

Discounts that existed before this setting start with it off. Saving a request that leaves the key out keeps the stored value.

## Business rules

### Off (default): each line counts alone

Each cart line reaches a tier with its own quantity only, whether the lines differ by variant or by personalisation.

With tiers `5 → 8 EUR` and `10 → 6 EUR`:

| Cart | Result |
|---|---|
| 5 size-S + 5 size-M | Each line reaches the "buy 5" tier and pays 8 EUR. Neither reaches "buy 10". |
| 10 size-S + 2 size-M | The size-S line pays 6 EUR. The size-M line reaches no tier and pays its regular price. |
| 5 pieces with photo A + 5 pieces with photo B | Two lines, each at the "buy 5" tier. |

### On: all lines add up

The pieces of the product on all cart lines add up, and each line pays **its own variant's price** at the tier that total reaches. A variant left without a price at that tier pays its price at the highest lower tier it has, or its regular (or Fixed-discount) price.

With the same tiers, 5 size-S + 5 size-M counts as 10, so both lines take the "buy 10" tier.

### Bundle lines stay out

In both modes, pieces added as part of a bundle do not count toward a tier and take no tier price. The bundle prices its own lines.

### Where the same rule applies

- **The cart and checkout** — the prices the customer pays.
- **The Storefront API** — `Product.quantityTierPrice` works out a selection of lines per line when the switch is off and pooled when it is on, so a headless storefront shows what the cart charges ([[headless-catalogue-reads]]).

### Setting it through the API

The Admin GraphQL API has no field for this setting. A discount created there counts per line, and the switch is changed on the admin form.

### What the product page shows

The tier ladder shows the tiers of the selected variant in both modes and says nothing about other lines — see [[quantity-discount-storefront-display]].

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-tier-evaluation]] — how the count is matched to a tier.
- [[quantity-discount-form]] — the form the box sits on.
- [[products-products]] — the target product and its variants.
- [[headless-catalogue-reads]] — the Storefront API price calculation.

## Open questions

- (verify) Whether creating a discount through the Admin GraphQL API is meant to set this switch.
