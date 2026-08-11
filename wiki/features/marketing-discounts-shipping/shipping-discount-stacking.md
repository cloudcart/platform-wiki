---
type: feature
nav_path: "Marketing → Discounts → Shipping → Stacking"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Free shipping stacking", "Shipping discount code_apply", "Shipping discount selection", "One shipping discount per cart", "Free shipping coupon stacking"]
tags: [marketing, discounts, shipping, stacking, code_apply, selection]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, force-save, other zero-paths, plan gates / API, examples).

# Shipping discount — stacking with other discounts

## Purpose

This page documents **how a Free-shipping discount interacts with other discounts on the same cart** — the `code_apply` flag for code-based variants, the one-shipping-discount-per-cart cap, the no-code vs code pool separation, and the first-match-wins selection (replacing older incorrect "sorted by `order_over DESC`" phrasing).

Tickets that land here: *"my Free-shipping coupon got rejected when the customer has a Fixed-discount item"*, *"which of my two Free-shipping promos wins on a 100 EUR cart"*.

## Where to find it

The `code_apply` toggle and code fields live on the Create / Edit form when the merchant picks the **Discount with code** type-picker card. See [[marketing-discounts-shipping]] for the entry-surface flow.

## What the merchant can do here

- Set the **promo code** for a code-based shipping discount.
- Toggle **`code_apply`** — let the code stack on carts with per-product discounts.
- (Cannot) stack two no-code Free-shipping discounts on the same cart — only one fires.
- (Cannot) make a code-based and a no-code Free-shipping discount compete — they live in separate pools.

## Settings & fields

### Code-based shipping discount (additional fields)

When the merchant creates a code-type discount and sets the inner type to `shipping`, the following fields appear:

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Promo code** | `code` | The literal string the customer types at checkout. | Required, max 20, regex `/^[a-z0-9\#\.]+$/i`, unique across `discounts.code`. |
| **Barcode mode** | `code_format` | When set to `ean13` / `ean8`, the code is treated as a barcode. | Enum. |
| **Barcode prefix** | `barcode_prefix` | Treat `code` as a prefix; the scanner appends the rest. | 1 / 0; only when `code_format` is set. |
| **Apply discount even if the cart contains products with a discount** | `code_apply` | Allow code to stack on top of carts that already have per-product discounts. | 1 / 0. |

Note: `apply_regular_price` does NOT apply to shipping codes — it's only relevant when the discount has a price component (flat / percent).

## Business rules

### `code_apply` blocks free-shipping-on-discounted-cart (both targets)

When a customer enters a free-shipping promo code and `code_apply = 0` (default), the code is **rejected at checkout** if ANY cart line already has a per-product discount applied (Fixed, Quantity tier, Percent code on a specific line). Rationale: the merchant designed the code for "regular-priced" carts; stacking on discounted items can lead to unintended cumulative discounts.

**This block applies to BOTH targets** — `all` AND `order_over`. The previously documented carve-out ("order_over shipping codes always apply if the cart meets the threshold") was incorrect — the validator checks `code_apply` identically. To stack onto a discounted cart, turn ON **"Apply discount even if the cart contains products with a discount"** (`code_apply = 1`) regardless of target.

For non-code (Global) shipping discounts, stacking is allowed by default (no `code_apply` check) — they auto-apply whenever conditions are met.

### One shipping discount per cart at checkout — selection rules

The cart's discount-applicator picks at most **ONE** shipping-type discount per cart at totals time. Multiple shipping discounts in the store do not stack; the engine selects one and silently ignores the rest. Selection rules:

1. If the customer entered a **code-based** free-shipping coupon AND it validated, the code-based discount wins. (Code-based shipping is processed through the discount-code pipeline, separate from the no-code shipping pool.)
2. If no code-based shipping coupon is active, the engine looks up no-code (Global / `order_over`) shipping discounts and returns the **FIRST match in unspecified order** — see *"first-match-wins iteration"* below.
3. Cross-Sell injection (synthetic free-shipping from a cart-row that triggered a free-shipping cross-sell) bypasses both the lookup pool and the code-validation, applying directly to the cart — see [[shipping-discount-other-zero-paths]].
4. `force_save = 1` short-circuits the condition re-check on existing orders — see [[shipping-discount-force-save]].

Practical merchant guidance: design shipping campaigns so they target disjoint scopes (one for domestic via region, one for international via a different region) — overlapping no-code shipping discounts produce undefined "which one wins" outcomes.

### Code-based shipping discounts are NOT part of the "shipping discounts" pool

When the cart looks up active shipping discounts to apply at totals time, the query scope **explicitly excludes code-based shipping discounts** (`code IS NULL` is part of the scope). Code-based shipping discounts are processed via the **code-input path** only — when the customer enters the code at checkout, the platform handles it via the regular discount-code application flow, not via the auto-applied shipping discount loop.

Consequence: a code-based "Free shipping with code WELCOME" coexists peacefully with a Global "Free shipping over 50 EUR" — they don't interact through the shipping-discount selector. A cart that meets both conditions still gets only ONE Free-shipping line on its totals — whichever pipeline produced it.

### Shipping discount selection — first-match-wins iteration (NOT sorted)

When multiple no-code Free-shipping discounts qualify, the cart-engine **iterates them in unspecified order and returns the FIRST match** whose `order_over` threshold is satisfied (or whose `force_save = 1` forces the keep). There is **no `order_over DESC` sort** — ordering is whatever the database returns (typically primary-key ascending, not guaranteed).

Older wiki phrasing claimed "sorted by `order_over DESC` (highest threshold wins)" — incorrect. Practical implication: a merchant with overlapping no-code Free-shipping discounts (e.g., "over 25 EUR" AND "over 50 EUR") will see **undefined behaviour** on a 100 EUR cart — either could fire.

For predictable behaviour: keep **only one active Free-shipping discount with `order_over`** at a time. For multi-tier free shipping, use a Cart Rule (tier ladders, see [[apps-cart-rules]]) or [[settings-shipping]] per-method *"Free shipping threshold"* (courier-method-specific, runs at quote time, independent of the discount engine).

Only ONE shipping discount applies at totals time regardless of how many qualify — the customer always sees a single "Free shipping" line.

### Code-based shipping uses inclusive `>=` on `order_over`

Worth restating in the stacking context: a code-based **Free-shipping** coupon uses an **inclusive `>=` comparison** at the code-validation step (unlike Flat / Percent codes which use strict `>`). A cart subtotal exactly equal to the threshold qualifies. See [[shipping-discount-eligibility]] for the full rule + example.

### Stacking matrix — quick summary

| Cart state | No-code Free-shipping | Code-based Free-shipping |
|---|---|---|
| Cart has no per-product discounts | applies | applies |
| Cart has per-product discount + `code_apply = 0` | applies (no check) | **rejected** |
| Cart has per-product discount + `code_apply = 1` | applies | applies |
| Another shipping discount already applied | ignored (first-match-wins picked one) | wins over the no-code (code path runs first) |
| Cross-Sell free-shipping injected | both can coexist; only one shipping-line on totals (see [[shipping-discount-other-zero-paths]]) | same |

## Related

- [[marketing-discounts-shipping]] — hub.
- [[shipping-discount-eligibility]] — the inclusive `>=` rule + `order_over` threshold details.
- [[shipping-discount-other-zero-paths]] — Cross-Sell injection + Cart Rule + OrderModification mechanisms that coexist with the discount selector.
- [[discount-stacking]] — cross-discount stacking matrix for all discount types.
- [[apps-cart-rules]] — partial-shipping discounts + multi-tier shipping ladders.
- [[settings-shipping]] — per-method *"Free shipping threshold"* runs at quote time, independent of the discount engine.

## Open questions

None.
