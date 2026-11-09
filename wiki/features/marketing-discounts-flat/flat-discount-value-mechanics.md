---
type: feature
nav_path: "Marketing → Discounts → Flat → Value mechanics"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Flat type_value", "Flat amount in cents", "Flat discount amount cap", "Flat amount validator", "Matched subtotal flat", "Strictly-greater order_over flat", "Per-customer cap flat code", "Flat code rejected at checkout"]
tags: [marketing, discounts, flat, type_value, cents, validation]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, eligibility, stacking, programmatic access).

# Flat discount — value mechanics

## Purpose

This page documents **how the Flat amount is stored, validated, and gated against the matched subtotal at checkout** — the cents storage convention, the absence of a maximum, what happens when the amount exceeds the subtotal, the strictly-greater check on `order_over`, and the per-customer cap that clears the code from the cart.

Tickets that land here: *"my 20 EUR code doesn't apply to a 15 EUR cart"*, *"why does my customer get rejected at exactly 100 EUR when the threshold is 100 EUR"*, *"the code disappeared from the cart after one use"*.

## Where to find it

The **Discount value** field in the General settings block on the create / edit form — see [[flat-discount-form-entry]]. The field accepts a currency amount in EUR; the platform stores it as integer cents on `type_value`.

## What the merchant can do here

- Enter the **Discount value** (the flat amount) in EUR. The value is stored as integer cents on `type_value`.

### What the merchant CANNOT do here

- Apply a Flat code on `all` or a specific target to a cart whose matched subtotal is less than the discount amount.
- Apply an `order_over` Flat discount, with or without a code, to a cart whose subtotal equals (but does not exceed) the threshold.

## Settings & fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount value** | `type_value` | The currency amount; what it comes off depends on the target ([[discount-stacking-amount-by-target]]). Entered in EUR; stored as cents. | Numeric. A blank value is sent as 0 and saves. See *"Amount value"* below. |

## Business rules

### Amount storage — integer cents

The `type_value` is stored as an **integer in cents**. The UI shows the merchant 20.00 EUR; the DB stores 2000. Conversion happens in the format helper when displaying back to the merchant.

Amounts are written in **cents** via the API as well — a 10 EUR flat discount is `type_value = 1000` regardless of source (see [[flat-discount-programmatic-access]]).

### Amount value — no maximum

There is **no maximum amount** on a flat discount. The form takes euros: typing 1000 means 1,000 EUR, stored as `100000`. Raw cents apply only through the API.

When the merchant genuinely wants:

- a percentage off — use [[marketing-discounts-percent]]
- a per-product absolute-price replacement (e.g., "this product now costs 9.99 EUR") — use [[marketing-discounts-fixed]]
- a free-shipping waive — use [[marketing-discounts-shipping]]

### Flat amount larger than the subtotal

The amount is never capped. What happens depends on the discount — see [[discount-stacking-amount-by-target]]:

- **No code, `order_over`** — skipped, and no other `order_over` discount is tried.
- **No code, products** — a product whose lowest price is below the amount gets no discount.
- **Code, `all` or a specific target** — refused at entry if the matching lines add up to less than the amount (below). After that, lines and the total have no lower limit and can go below zero.
- **Code, `order_over`** — only the threshold is checked, not the amount. The total can go below zero.

### Flat code on `all` or a specific target requires matched subtotal ≥ amount

For a **Flat code** on `all` or a specific target, the cart's **matched subtotal** must be **at least** `type_value` (the flat amount). A 20 EUR code on a cart whose matched products sum to 15 EUR is **refused at entry** with *"Invalid discount code"*, with no mention of the amount.

- For target = `all`, the matched subtotal is all lines in the cart.
- For target = `product` / `product_category` / etc., the matched subtotal is the sum of the matching lines only.

### Strictly-greater subtotal check on `order_over` Flat

On `order_over`, with or without a code, the cart subtotal must be **strictly greater than** the threshold. The subtotal is the lines after product discounts, line-level codes and product-level Cart Rule reductions, at the prices as entered: a store whose prices exclude VAT is compared without VAT. A cart **exactly equal** to the threshold does not qualify. To allow "exactly N or more", merchants should set the threshold to **N − 0.01**.

> No-code free shipping is at or above the threshold — see [[marketing-discounts-shipping|Shipping discounts]].

Example: a 10 EUR code with `order_over = 50 EUR` on a 50 EUR cart → **refused** with *"The discount could not be applied because the minimum total price of the products has not been reached."*. On a 50.01 EUR cart → applies. The merchant working around this should set `order_over = 49.99 EUR` to admit the 50 EUR cart.

### Per-customer cap auto-clears the code

When a logged-in customer has redeemed a code-based Flat discount up to the `maxused_user` cap, entering the code shows *"You have used this discount code the maximum number of times"* and **the code is cleared from the cart**. The customer would need a different code.

The cap counts the customer's uses on orders in a counted status (see [[flat-discount-eligibility]]).

### Worked example — distribution + matched-subtotal check

Cart with two matched lines (code, target = `product_category`):

- Line A: 12 EUR.
- Line B: 8 EUR.
- Matched subtotal: 20 EUR.
- Flat amount: 5 EUR.

The engine distributes proportionally:

- Line A share: `5 × (12 / 20) = 3.00 EUR`.
- Line B share: `5 × (8 / 20) = 2.00 EUR`.
- Total: 5.00 EUR — exact, no cent-fix needed.

If the code's amount were 25 EUR instead, it would be **refused at entry** since matched subtotal (20) < `type_value` (25) — see above. The merchant must either lower the code's amount or design the campaign for higher-value carts.

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-targeting]] — what the amount comes off per target.
- [[flat-discount-eligibility]] — `maxused_user` cap + uses counter + counted statuses.
- [[flat-discount-stacking]] — `code_apply` blocks (different reject path: existing discounts on lines, not matched-subtotal).
- [[flat-discount-programmatic-access]] — `type_value` over JSON-API v2 + GraphQL is also in cents.
- [[marketing-discounts-percent]] — sister type; same strictly-greater `order_over` rule.
- [[marketing-discounts-fixed]] — different model (per-variant replacement price).
- [[marketing-discounts-shipping]] — different model (no `type_value`; binary "remove shipping line").

## Open questions

None.
