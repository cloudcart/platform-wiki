---
type: entity
nav_path: "Entity → Product Option → Pricing"
aliases: ["Product Option pricing", "Option price modifier", "Option surcharge", "Option amount type", "Option per-value modifier", "Option allow negative", "Option price impact"]
tags: [catalog, products, options, pricing, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product-option]]. See the hub for the other aspects (attributes, order-line storage, scoping + edge cases).

# Product Option — Pricing

## Identity

How a Product Option modifies the line total at cart-calculation time. Most Options are informational (no price impact), but the merchant can attach a surcharge — flat or percentage, once-per-line or per-quantity, before or after discount, and optionally negative (a credit). This aspect documents the full price-modifier model and the calculation rules. The non-pricing fields (Name, input type, Required, Storefront name) are in [[product-option-entity-attributes]].

## Aliases

- **Price impact** / **Option surcharge** — the merchant-facing term for the modifier.
- **Amount type** (`amount_type`) — flat vs percent aggregation rule.
- **Per-value modifier** — per-choice surcharge on Select / Radio / Checkbox.
- **Allow negative** (`allow_negative`) — turning a surcharge into a credit.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Price impact** | Optional — None / Add (flat) / Per-quantity / Multiplicative | When set, the Option modifies the line total at cart-calculation time. *Add* surcharges the line by a flat amount (e.g., +5 BGN for gift wrap). *Per-quantity* multiplies the surcharge by the line quantity (e.g., +5 BGN PER engraved unit). *Multiplicative* scales the line price by a factor (rare). *None* makes the Option informational only. |
| **Amount type** (`amount_type`) | The aggregation rule applied when the Option carries a price modifier | One of: `flat` (fixed surcharge added once per cart line) or `percent` (percentage of the parent product's price). The `per_item = 1` flag flips the surcharge to a per-quantity multiplier when ON. |
| **Per-value price modifier** | Per-row amount (Select / Radio / Checkbox types only) | Each discrete value can carry its own surcharge — e.g., "Standard font: +0", "Italic font: +2 BGN", "Calligraphy font: +5 BGN". |
| **Apply over price type** (`apply_over_price_type`) | Whether the surcharge applies before or after discounts | Picks whether the Option modifier sees the discounted price or the original price as its base when computing percentage surcharges. Affects margin on discounted lines. |
| **Allow negative** (`allow_negative`) | Whether the Option's amount can be a discount (negative surcharge) | When ON, the merchant can configure a NEGATIVE per-value modifier, e.g., "Skip warranty: -10 BGN". Treated as a per-line credit at cart calculation. |
| **Min square** (`min_square`) | Floor value for the Square measurement type | Visible only on Square-type Options. The customer cannot enter a smaller area than this floor (prevents nuisance tiny orders). |

## Calculation rules

### Per-value price modifiers stack additively on Checkbox

Per-value price modifiers on Select / Radio apply to the single picked value. On a **Checkbox**-type Option, modifiers **sum additively** when the customer ticks multiple boxes — checking 2 or 3 boxes adds the surcharge from each. There is no alternative aggregation rule. (The Checkbox multi-pick behaviour itself is documented in [[product-option-entity-attributes]].)

### Option price tax uses the parent product's tax class

Option price modifiers participate in tax computation using the **parent product's tax class** — there is no per-Option tax-class override. Surcharges follow whatever tax rate applies to the product.

### Measurement types auto-force `per_item = 1`

When the merchant saves an Option of type `length`, `weight`, or `square`, the platform silently sets `per_item = 1` regardless of the merchant's choice — measurement Options are always treated as per-unit charges (you can't say "1 BGN flat for any length", only "1 BGN per cm"). The merchant cannot override this.

### Surcharges flow into the line total seen by discounts

Line-level [[discount|discounts]] apply to the line total *including* any Option price modifiers, so the merchant should account for surcharges when planning promotions. The `apply_over_price_type` flag governs the inverse direction — whether a percentage Option surcharge is computed over the pre- or post-discount price.

## Where it appears

- [[products-options-overview]] — where the merchant sets the price impact, amount type, per-value modifiers, and the negative / min-square flags.
- [[apps-product-options-settings-new]] — app-level configuration that can set defaults for the Options system.
- [[cart]] — the surcharge is applied to the line total at cart-calculation time.
- [[order]] — the resulting line total (including the surcharge) is snapshotted onto the order — see [[product-option-entity-order-storage]].

## Related

- [[product-option]] — hub.
- [[product-option-entity-attributes]] — the non-pricing fields + the Checkbox multi-pick mechanics referenced above.
- [[product-option-entity-order-storage]] — how the computed surcharge + picked value snapshot onto the order line.
- [[discount]] — line-level discounts apply to the line total including Option surcharges.
- [[product]] — the parent product whose tax class and price the surcharge uses as its base.

## Open Questions

None.
