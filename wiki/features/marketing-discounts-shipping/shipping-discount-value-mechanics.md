---
type: feature
nav_path: "Marketing → Discounts → Shipping → Value mechanics"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Free shipping value mechanics", "Shipping discount totals lines", "Free shipping cart totals", "Shipping discount carrier quote", "Free shipping COD"]
tags: [marketing, discounts, shipping, totals, cart, value-type]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, stacking, force-save, other zero-paths, plan gates / API, examples).

# Shipping discount — value mechanics

## Purpose

This page explains **how** a Free-shipping discount changes the cart totals — the "what does the customer actually see" mechanics. Unlike Flat / Percent discounts, shipping is **binary**: there is no "how much off" number, and the saved amount equals whatever the carrier quoted at the moment of redemption.

The merchant cares because the carrier quote varies per zone, weight, shipping provider, and per-product surcharges — so the **merchant's real cost** of a Free-shipping promo varies cart-to-cart and is only knowable at checkout time.

## Where to find it

The value-type behaviour is determined by setting **Discount type → Free shipping** on the Create / Edit form at `/admin/marketing-new/discounts/create/global` (or `create/code` for the coupon variant). See [[marketing-discounts-shipping]] for the entry-surface flow.

## What the merchant can do here

- Set `type = shipping` from the Discount type select.
- (Cannot) set a numeric `type_value` — the value-type IS the binary "remove shipping line".
- Name the discount via `name`; the value rendered on the customer's cart-totals row is `name` only (no parenthetical suffix).

## Settings & fields

### Type field

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount type** | `type` | Set to `shipping` (Free shipping). | One of `flat` / `percent` / `shipping`. |
| **Discount value** | `type_value` | **Hidden / empty for shipping.** | Must be empty when type=shipping; rejected: *"Type value must be empty"*. |

When the merchant changes Discount type → Free shipping:

1. The Discount value (`type_value`) field hides — shipping has no numeric value.
2. The Discount target dropdown drops product / category / vendor / selection options — only `all` and `order_over` remain.
3. The form forces `settings` to `all` if the merchant was previously on a product-specific target.

## Business rules

### Free shipping = "remove the shipping line" — not a discount amount

A shipping discount **does not produce a `type_value`**. At cart totals time, the platform reads the cart's shipping quote (the price quoted by the chosen shipping provider) and renders a NEGATIVE totals line of exactly that amount alongside the shipping line — effectively zeroing it out:

- Shipping line: + (whatever the courier quoted).
- Free-shipping discount line: − (same amount).
- Net shipping in the order: zero.

The actual saved amount is therefore **the shipping quote at the moment of checkout** — it can vary by zone, weight, shipping provider, even per-product surcharges. The customer always pays zero shipping when the discount applies; the merchant absorbs whatever the courier charges.

### Cart-totals application at checkout

When the platform builds the cart's totals at checkout time:

1. It computes the cart subtotal (line-items + taxes-before-shipping).
2. It computes the shipping provider's quote (the chosen carrier + region + weight + insurance).
3. It looks up active shipping discounts:
   - Match active scope (status + dates + uses) — see [[shipping-discount-eligibility]].
   - Match customer group + region + `only_customer`.
   - For target `order_over`: subtotal ≥ `order_over`.
   - For target `all`: no additional check.
4. If a code is in the cart and it's a shipping-typed code, the platform also runs the `code_apply` stacking rule — see [[shipping-discount-stacking]].
5. If a match wins, the platform adds two paired totals lines: the shipping quote (positive) and a free-shipping discount line of the same magnitude (negative). The net is zero.
6. Order totals recompute with shipping effectively zeroed out.

### Auto-apply via shipping provider integrations — variable saved amount

Some shipping providers (e.g., couriers with delivery-hour add-ons) integrate with the platform's shipping totals. The free-shipping discount runs **on top of the provider's quote** — whatever amount the provider quotes is what the discount zeroes out. This means:

- Insurance add-ons quoted by the provider are NOT separately discounted by free-shipping (they remain billed unless the provider folds them into the main quote).
- "Pay to sender" providers (cash-on-delivery markup) — the markup is part of the shipping quote and IS removed by the free-shipping discount.
- The actual saved amount is variable per order — surface it on order-detail rows for transparency.

### Free shipping applies to whatever the carrier quotes — including COD surcharges

The free-shipping discount zeroes out the shipping quote at the cart-totals level. This means:

- The carrier's base rate is removed.
- "Cash on delivery" surcharges (when folded into the carrier's quote) are removed.
- Insurance add-ons quoted as SEPARATE line items may NOT be removed (they're not part of the shipping quote).
- The carrier's per-product surcharges (oversized items, fragile handling) are removed if part of the main quote.

Merchants who want to discount only the base rate (not insurance) need to use [[apps-cart-rules|Cart Rules]] instead — Discounts can't distinguish quote sub-components.

### Discount-line description on shipping totals is always null

When a Free shipping discount appears in the cart-totals breakdown, the description field (typically used by Percent discounts to surface the percentage) is **always null** for shipping. The customer sees the discount line labeled with the discount's `name` only — no parenthetical "(-N%)" or "(-N EUR)" suffix.

If the merchant wants the customer to see a specific phrase next to the free-shipping line on the cart summary, they should encode it in the discount's `name` field directly.

### Customer-facing display

The cart and checkout pages show the free shipping as TWO lines: the shipping carrier line (positive amount) and the discount line (negative amount of the same value). Some storefront themes collapse this into a single "Free shipping" label with the original amount struck-through — but the underlying totals math is always the paired pos+neg structure.

The discount's `name` field is rendered as the discount line's label, so merchants should name shipping discounts customer-facingly (e.g., "Free delivery over 50 EUR", "Black Friday free shipping") rather than internal codes.

### Save validation — type-specific rules

The backend validator enforces, for `type = shipping`:

- `type_value` must be empty — else: *"Type value must be empty"*.
- `force_save` is required — see [[shipping-discount-force-save]].
- `products` and `product_categories` arrays are rejected — *"Type is not valid for products or product category targets"* (see [[shipping-discount-eligibility]] for the full target-restriction story).
- `type` must be one of `flat`, `percent`, `shipping`, `fixed`, `quantity` — else: *"Type must be one of: flat, percent, shipping, quantity"*.
- All common discount rules apply (name length, code uniqueness for code-based shipping, etc.).

### Shipping at zero already — silent no-op

If the cart's shipping quote is already 0 (e.g., pickup, digital-only carts, or [[shipping]] provider configured with a zero rate for the region), the free-shipping discount silently does NOT render an additional discount line. There is nothing to discount; the cart already shows "Shipping: 0" and stays that way.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[shipping]] — store's shipping providers; the free-shipping discount zeroes out the provider's quote.
- [[apps-cart-rules]] — for partial-shipping discounts (e.g., "10% off shipping") or insurance-aware promos.

## Open questions

None.
