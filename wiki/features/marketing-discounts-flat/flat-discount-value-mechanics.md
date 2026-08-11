---
type: feature
nav_path: "Marketing → Discounts → Flat → Value mechanics"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Flat type_value", "Flat amount in cents", "Flat discount amount cap", "Flat amount validator", "Matched subtotal flat", "Strictly-greater order_over flat", "Per-customer cap flat code", "Flat code rejected at checkout"]
tags: [marketing, discounts, flat, type_value, cents, validation]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, eligibility, stacking, programmatic access).

# Flat discount — value mechanics

## Purpose

This page documents **how the Flat amount is stored, validated, and gated against the matched subtotal at checkout** — the cents storage convention, the practically-uncapped amount validator nuance, the matched-subtotal-must-cover-the-amount rule, the strictly-greater check on code-based `order_over`, and the per-customer cap that silently removes the code from the cart.

Tickets that land here: *"my 20 EUR code doesn't apply to a 15 EUR cart"*, *"why does my customer get rejected at exactly 100 EUR when the threshold is 100 EUR"*, *"the code disappeared from the cart after one use"*, *"I typed 100,000 in the amount field and it saved as 1,000 EUR".

## Where to find it

The **Discount value** field in the General settings block on the create / edit form — see [[flat-discount-form-entry]]. The field accepts a currency amount in EUR; the platform stores it as integer cents on `type_value`.

## What the merchant can do here

- Enter the **Discount value** (the flat amount) in EUR. The value is stored as integer cents on `type_value`.

### What the merchant CANNOT do here

- Enter a numeric value that exceeds the validator's character limit (decimal points included; see the practical guidance below).
- Apply a Flat code to a cart whose matched subtotal is less than the discount amount.
- Apply a code-based `order_over` Flat discount to a cart whose subtotal equals (but does not exceed) the threshold.

## Settings & fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount value** | `type_value` | The currency amount subtracted from the cart (or matched subtotal). Entered in EUR; stored as cents. | Required when `type = flat`. *"The field 'amount' can not be empty"*. See *"Amount value"* below for the validator nuance. |

## Business rules

### Amount storage — integer cents

The `type_value` is stored as an **integer in cents**. The UI shows the merchant 20.00 EUR; the DB stores 2000. Conversion happens in the format helper when displaying back to the merchant.

Amounts are written in **cents** via the API as well — a 10 EUR flat discount is `type_value = 1000` regardless of source (see [[flat-discount-programmatic-access]]).

### Amount value — practically uncapped (platform stores in cents)

The flat amount field validates through the platform's currency-amount validator. Important nuance: the validator's "max" parameter is the **maximum number of CHARACTERS allowed in the input string** — NOT a numeric value cap. The default 100,000-character ceiling means a merchant can practically enter any reasonable value (decimal points and all) without hitting the limit. There is **no built-in numeric ceiling** on the flat amount.

A merchant attempting to save what they read as "100,000" in the form is saving a value of **100,000 cents = 1,000 EUR** (the platform stores all monetary values in **cents**, so the displayed-vs-stored relationship is always ×100). If the merchant types a number that the form misinterprets (e.g., decimal-separator confusion), the platform will accept and store whatever it parsed. Sanity-check large amounts at save time by reviewing the resulting `type_value` on the listing — it shows the actual saved value.

When the merchant genuinely wants:

- a percentage off — use [[marketing-discounts-percent]]
- a per-product absolute-price replacement (e.g., "this product now costs 9.99 EUR") — use [[marketing-discounts-fixed]]
- a free-shipping waive — use [[marketing-discounts-shipping]]

### Discount capped to matched subtotal

When the cart-engine applies the Flat amount, it **caps the applied amount to the matched subtotal** so the discount never exceeds what's available to discount. A 20 EUR flat on a matched subtotal of 15 EUR never produces a -5 EUR cart line — the platform applies at most 15 EUR.

### Flat code requires matched subtotal ≥ amount

For a **Flat code-based** discount, the customer's cart **matched subtotal** must be **at least** `type_value` (the flat amount). A 20 EUR code on a cart whose matched products sum to 15 EUR is **rejected at code-validation time** — the discount won't be applied because there's not enough to discount. The merchant sees their code fail at checkout with **no clear "less than amount" error**.

- For target = `all`, the matched subtotal is the whole cart.
- For target = `product` / `product_category` / etc., the matched subtotal is the sum of the matching lines only.

This rule is **specific to code-based Flat discounts** — no-code Global / `order_over` Flat discounts cap-to-subtotal silently instead of rejecting (see above).

### Strictly-greater subtotal check on `order_over` Flat code

When a Flat **code** requires `order_over`, the cart subtotal must be **strictly greater than** the threshold. A cart **exactly equal** to the threshold is rejected. To allow "exactly N or more", merchants should set the threshold to **N − 0.01**.

> Contrast with the no-code Global Flat discount and with [[marketing-discounts-shipping|Shipping discounts]], which use inclusive `>=` — the strictly-greater rule is specific to code-based Flat / Percent.

Example: a 10 EUR code with `order_over = 50 EUR` on a 50 EUR cart → **rejected**. On a 50.01 EUR cart → applies. The merchant working around this should set `order_over = 49.99 EUR` to admit the 50 EUR cart.

### Per-customer cap auto-clears the code

When a customer has redeemed a code-based Flat discount up to the `maxused_user` cap, the next checkout where they enter the code **removes the code from the cart entirely** rather than rejecting it with a "limit reached" message. The customer would need a different code — they cannot retry the same one.

The cap counter increments when the customer's order reaches one of the counted statuses (see [[flat-discount-eligibility]]).

### Worked example — distribution + matched-subtotal cap

Cart with two matched lines (target = `product_category`):

- Line A: 12 EUR.
- Line B: 8 EUR.
- Matched subtotal: 20 EUR.
- Flat amount: 5 EUR.

The engine distributes proportionally:

- Line A share: `5 × (12 / 20) = 3.00 EUR`.
- Line B share: `5 × (8 / 20) = 2.00 EUR`.
- Total: 5.00 EUR — exact, no cent-fix needed.

If the merchant had set Flat = 25 EUR instead, the engine would **cap the applied amount to 20 EUR** (the matched subtotal). Both lines go to zero. For a code-based variant, the same scenario instead **rejects at code-validation** since matched subtotal (20) < `type_value` (25) — see *"Flat code requires matched subtotal ≥ amount"* above. The merchant must either lower the code's amount or design the campaign for higher-value carts.

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-targeting]] — what counts as the matched subtotal per target (cart-wide vs lines).
- [[flat-discount-eligibility]] — `maxused_user` cap + uses counter + counted statuses.
- [[flat-discount-stacking]] — `code_apply` blocks (different reject path: existing discounts on lines, not matched-subtotal).
- [[flat-discount-programmatic-access]] — `type_value` over JSON-API v2 + GraphQL is also in cents.
- [[marketing-discounts-percent]] — sister type; same strictly-greater `order_over` rule on codes.
- [[marketing-discounts-fixed]] — different model (per-variant replacement price).
- [[marketing-discounts-shipping]] — different model (no `type_value`; binary "remove shipping line").

## Open questions

None.
