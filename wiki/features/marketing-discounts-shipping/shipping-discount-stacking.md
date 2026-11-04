---
type: feature
nav_path: "Marketing → Discounts → Shipping → Stacking"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Free shipping stacking", "Shipping discount code_apply", "Shipping discount selection", "One shipping discount per cart", "Free shipping coupon stacking"]
tags: [marketing, discounts, shipping, stacking, code_apply, selection]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, force-save, other zero-paths, plan gates / API, examples).

# Shipping discount — stacking with other discounts

## Purpose

This page documents **how a Free-shipping discount interacts with other discounts on the same cart** — the `code_apply` flag for code-based variants, the one-shipping-discount-per-cart cap, the no-code vs code pool separation, and the selection among several no-code discounts.

Tickets that land here: *"my Free-shipping coupon got rejected when the customer has a Fixed-discount item"*, *"which of my two Free-shipping promos wins on a 100 EUR cart"*.

## Where to find it

The `code_apply` toggle and code fields live on the Create / Edit form when the merchant picks the **Discount with promo code** type-picker card. See [[marketing-discounts-shipping]] for the entry-surface flow.

## What the merchant can do here

- Set the **promo code** for a code-based shipping discount.
- Toggle **`code_apply`** — let the code stack on carts with per-product discounts.
- (Cannot) stack two no-code Free-shipping discounts on the same cart — one line shows, whichever qualified first.
- (Cannot) show both a code-based and a no-code Free-shipping row — a qualifying no-code discount takes the row.

## Settings & fields

### Code-based shipping discount (additional fields)

When the merchant creates a code-type discount and sets the inner type to `shipping`, the following fields appear:

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Promo code** | `code` | The literal string the customer types at checkout. | Required, max 20, regex `/^[a-z0-9\#\.]+$/i`, unique across `discounts.code`. |
| **Barcode mode** | `code_format` | When set to `ean13` / `ean8`, the code is treated as a barcode. | Enum. |
| **Barcode prefix** | `barcode_prefix` | Treat `code` as a prefix; the scanner appends the rest. | 1 / 0; only when `code_format` is set. |
| **The discount is applied even when the cart contains discounted products.** | `code_apply` | Allow code to stack on top of carts that already have per-product discounts. | 1 / 0. |

Note: `apply_regular_price` does NOT apply to shipping codes — it's only relevant when the discount has a price component (flat / percent).

## Business rules

### `code_apply` blocks free-shipping-on-discounted-cart (both targets)

When a customer enters a free-shipping promo code and `code_apply = 0` (default), the code is **refused at entry** if ANY cart line already holds a product discount. With a minimum the message is *"This discount code can not be applied because you already have a discounted products at your cart"*; with target `all` it is *"Invalid discount code"*. The check runs only at entry: a discounted product added afterwards does not remove the free shipping.

**This block applies to BOTH targets** — `all` AND `order_over`. To accept the code on a discounted cart, turn ON **"The discount is applied even when the cart contains discounted products."** (`code_apply = 1`) regardless of target.

For non-code (Global) shipping discounts, stacking is allowed by default (no `code_apply` check) — they auto-apply whenever conditions are met.

### One shipping discount per cart at checkout — selection rules

The cart's discount-applicator picks at most **ONE** shipping-type discount per cart at totals time. Multiple shipping discounts in the store do not stack. The customer sees one row, but every qualifying no-code discount is recorded on the order and each one's `uses` goes up. Selection order:

1. The engine looks up no-code (Global / `order_over`) shipping discounts and returns the **first one that qualifies**; a discount that does not qualify no longer ends the search — see *"Every discount is tried"* below. Cross-Sell injection (synthetic free-shipping from a cart-row that triggered a free-shipping cross-sell) takes the place of this pool — see [[shipping-discount-other-zero-paths]].
2. Only if none applies, a **code-based** free-shipping coupon in the cart takes the row. (Code-based shipping is processed through the discount-code pipeline, separate from the no-code shipping pool.) A valid code still shows no row of its own when a no-code discount qualifies.
3. Only if no code applies, a payment-method free shipping takes the row, then a Cart Rule's.
4. `force_save = 1` short-circuits the condition re-check on existing orders — see [[shipping-discount-force-save]].

Overlapping no-code shipping discounts give free shipping either way; only the name on the line can differ. Design campaigns with disjoint customer groups or dates when the name matters.

### Code-based shipping discounts are NOT part of the "shipping discounts" pool

When the cart looks up active shipping discounts to apply at totals time, the lookup **explicitly excludes code-based shipping discounts**. Code-based shipping discounts are processed via the **code-input path** only — when the customer enters the code at checkout, the platform handles it via the regular discount-code application flow, not via the auto-applied shipping discount loop.

Consequence: a code-based "Free shipping with code WELCOME" coexists peacefully with a Global "Free shipping over 50 EUR" — they don't interact through the shipping-discount selector. A cart that meets both conditions gets only ONE Free-shipping line on its totals: the no-code discount's, because it runs first.

### Every discount is tried; the amount left uses the closest

The cart-engine goes through all no-code Free-shipping discounts and returns the **first that qualifies** (its `order_over` threshold is satisfied, or `force_save = 1` forces the keep). One that does not qualify no longer ends the search: a store with "over 60 EUR" and "any order" discounts gives free shipping on any order.

There is **no threshold sort**, so which discount's name shows on a cart that meets several is unspecified. The cart gets free shipping either way. The **"left to free shipping"** amount is measured against the closest threshold across all of them.

For different thresholds per delivery method, use the [[settings-shipping]] per-method *"Free shipping threshold"* (courier-method-specific, runs at quote time, independent of the discount engine). [[apps-cart-rules|Cart Rules]] have no condition on the delivery method.

Only ONE shipping discount applies at totals time regardless of how many qualify — the customer always sees a single "Free shipping" line.

### A code's minimum: strictly above at entry

At the code box the products subtotal must be strictly above a free-shipping code's minimum. Once accepted, shipping stays free while the total before shipping is at or above it. See [[shipping-discount-eligibility]] for the full rule + example.

### Stacking matrix — quick summary

| Cart state | No-code Free-shipping | Code-based Free-shipping |
|---|---|---|
| Cart has no per-product discounts | applies | applies |
| Cart has per-product discount + `code_apply = 0` | applies (no check) | **rejected** |
| Cart has per-product discount + `code_apply = 1` | applies | applies |
| A no-code and a code-based discount both qualify | the first no-code that qualifies takes the row | accepted, but no row of its own |
| Cross-Sell free-shipping injected | replaced by the Cross-Sell row (see [[shipping-discount-other-zero-paths]]) | no row of its own |

## Related

- [[marketing-discounts-shipping]] — hub.
- [[shipping-discount-eligibility]] — the minimum-amount rules + `order_over` threshold details.
- [[shipping-discount-other-zero-paths]] — Cross-Sell injection, Cart Rule and order modification, the other ways the line reaches zero.
- [[discount-stacking]] — cross-discount stacking matrix for all discount types.
- [[apps-cart-rules]] — Cart Rule free shipping.
- [[settings-shipping]] — per-method *"Free shipping threshold"* runs at quote time, independent of the discount engine.

## Open questions

None.
