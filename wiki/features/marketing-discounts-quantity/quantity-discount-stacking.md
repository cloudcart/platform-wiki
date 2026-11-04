---
type: feature
nav_path: "Marketing → Discounts → Quantity → Stacking"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/quantity
aliases: ["Quantity discount stacking", "Quantity vs Fixed discount", "Quantity + promo code", "Quantity discount priority", "code_apply Quantity"]
tags: [marketing, discounts, quantity, stacking, priority, cart]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, uniqueness constraint, plan gating, storefront display).

# Quantity discount — stacking and priority at cart-time

## Purpose

This aspect documents what happens at cart-time when a Quantity-tier line **also** has another discount source — a per-variant Fixed discount, an up-sell / cross-sell / bundle override, or a promo code. It covers which discount source wins per line and whether a promo code can apply on top of a Quantity-tier price.

## Where to find it

Stacking behaviour is cart-side; there is no admin UI screen that toggles it. The relevant inputs sit on different discount surfaces — Quantity tiers on the form at `/admin/marketing/discounts/create/quantity` (see [[quantity-discount-form]]), Fixed discounts on [[marketing-discounts-fixed]], promo codes on [[marketing-discounts-codes]] / [[marketing-discounts-code-pro]], and Cart Rules at [[apps-cart-rules]].

## What the merchant can do here

The merchant cannot configure stacking directly on the Quantity form — `code_apply` is not exposed and there is no priority dial. Practical levers:

- **Choose between Quantity and Fixed** for the same product knowing that at and above the smallest threshold the tier price applies, less the Fixed saving; the Fixed price applies as fallback below it.
- **Configure `code_apply` on a promo code or a Code PRO code** — this decides whether the code applies to a tier-priced line. A Container has no such switch.
- **Avoid up-sell / cross-sell / bundle conflicts** with Quantity tiers on the same products if predictable per-unit pricing matters — those overrides win above Quantity.

## Settings & fields

This aspect has no merchant-tunable fields on the Quantity form itself. The relevant fields live on **other** discount records that the Quantity tier interacts with:

| Field | Lives on | What it does at stacking-time |
|-------|----------|-------------------------------|
| `code_apply` | A promo code or Code PRO code | On: the code also applies to a tier line, on the reduced amount. Off: see the rules below. |
| `code_apply` | The Quantity discount itself | Not shown on the Quantity form (see [[quantity-discount-form]]); on for a discount saved from the admin form. When on, the cart takes the saving of the variant's active Fixed or no-code Flat/Percent discount off the tier price, with or without a code. |
| `discount_value` (per tier) | The Quantity discount's tier rows | The replacement unit price the tier sets. |
| Up-sell / cross-sell / bundle override flags | The up-sell, cross-sell or bundle settings | Take priority over the Quantity tier. |

## Business rules

### Per-line discount-priority resolver

When a cart line has BOTH a per-variant [[marketing-discounts-fixed]] price AND an active Quantity tier, the platform's per-line discount-priority resolver picks **one source** in this order (highest priority first):

1. **Up-sell override** — if the line was added via an up-sell trigger.
2. **Cross-sell override**.
3. **Bundle override** — when the line is part of a cart-bundle.
4. **Quantity tier** (this feature).
5. **The cheapest active row among Fixed and no-code Flat or Percent**.

So if a product has BOTH a Fixed discount AND a Quantity discount, a reached tier sets the line's price. With the Quantity discount's `code_apply` on, which a discount saved from the admin form has, the variant's active Fixed or no-code saving also comes off the tier price, with or without a code: catalog 20 EUR, Fixed 15 EUR, tier 12 EUR means the cart charges 7 EUR while the ladder shows 12 EUR. There is no lower limit on the result. Below the smallest tier's threshold, the Fixed-discount price applies as fallback. This holds the same whether viewed from the product line or from the variant: the Quantity check runs before the variant's Fixed-discount fallback.

### Quantity + promo-code stacking — controlled by the promo code's `code_apply`, not the Quantity discount

Whether a promo code applies on top of a Quantity-tier line is decided by the **external code-based discount's own `code_apply` setting**, on a promo code or a Code PRO code ([[marketing-discounts-code-pro]]). A Container ([[marketing-discounts-codes]]) has no such switch: its default is on, and it is never refused for this.

- **Off, code on all products or a specific target** → accepted; the tier line is skipped and the other lines get the code. If every line is discounted, nothing comes off and no message shows.
- **Off, code with Orders over or free shipping with a threshold** → refused at entry if any line holds a product discount, with *"This discount code can not be applied because you already have a discounted products at your cart"*.
- **Off, free shipping for all, or Code PRO** → refused at entry with *"Invalid discount code"*.
- **On** → the code applies **on top of** the Quantity-tier price, on the reduced amount. For what a code's amount comes off, see [[discount-stacking-amount-by-target]].
- **On, with `apply_regular_price` also on** → the code is worked out on the regular price and compared with the current discounted price. If the code's price is lower, it replaces the tier on the line; otherwise the line keeps the tier and no code. Never both.

The Quantity discount also has its own `code_apply` flag. It is not shown on the Quantity form (see [[quantity-discount-form]] for the omitted-fields list), and a discount saved from the admin form has it on. It does not depend on any code: when on, the cart takes the saving of the variant's active Fixed or no-code Flat/Percent discount off the tier price, as in the example above. Only the Admin GraphQL API can turn it off; with it off the line pays the plain tier price.

### Quantity discounts have no code field, never code-based

Quantity discounts are **always automatic**. There's no code field on the form (see [[quantity-discount-form]]). The tier activates purely from the counted pieces reaching the threshold (per cart line, see [[quantity-discount-line-counting]]) — the customer never types anything to trigger it.

Code-based stacking is therefore always **between** a Quantity discount and a separate code-based discount the merchant created elsewhere, not within the Quantity discount itself.

### Tier is applied at the storefront cart, not in the admin

The tier is evaluated and applied only at the storefront cart; it then persists onto the order. The merchant viewing or editing the order in the admin does NOT see the Quantity tier re-applied — so adjusting an order's quantity in the admin does NOT switch tiers on the saved line. See [[quantity-discount-tier-evaluation]] for the same behaviour from the tier-matching angle.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-tier-evaluation]] — the matched-tier resolution that this aspect's priority resolver picks between.
- [[quantity-discount-form]] — confirms `code_apply` is NOT a merchant-exposed field on the Quantity form.
- [[marketing-discounts-fixed]] — the per-variant Fixed discount whose price a matched tier replaces, and whose saving comes off the tier price.
- [[marketing-discounts-codes]] — Container codes, which apply on top of tier lines.
- [[marketing-discounts-code-pro]] — Code PRO codes, each with its own `code_apply` switch.
- [[apps-cart-rules]] — Cart Rules can compose multi-product promotions Quantity discount cannot express; they reduce a line after its product discount and any line-level code.

## Open questions

None.
