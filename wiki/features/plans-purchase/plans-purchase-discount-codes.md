---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase → Pay now → Discount code"
route_name: admin.checkout (Discount card)
route_path: /admin/api/core/cart/discount
aliases: ["Plan discount code", "Plan promo code", "Promo code seeding", "Discount card", "Plan coupon", "Промо код за план", "Купон при плащане на план", "Кодиран отстъпка за абонамент"]
tags: [plans, purchase, discount, promo-code, marketing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans-purchase]]. See the hub for the other aspects (billing cycle, recommended add-ons, plan detail view, checkout panel, business rules, subscription outcomes).

# Plans purchase — discount codes

## Purpose

The plan-purchase flow supports promotional **discount codes** in two ways: (1) seeded into the session via a CloudCart-marketing landing URL before the merchant ever opens the PlanPanel, and (2) entered explicitly on the **Discount card** in the Checkout side-panel. The PlanPanel itself does NOT expose a code input — the merchant either arrives with a session-seeded code, or enters one on the Checkout panel's discount field.

## Where to find it

- **Session-seeded path** — a CloudCart marketing landing URL (set by the marketing team) seeds the code into the merchant's session. When the merchant then opens `/admin/plan/{mapping}/purchase`, the cart is built with the seeded code already applied.
- **Checkout-panel field** — the **Discount code** card inside the Checkout side-panel ([[plans-purchase-checkout-panel]]), visible only when `cart.id` is set AND `cart.hide_discount` is false.

Backend endpoint: `POST /admin/api/core/cart/discount` (server-side coupon application).

## What the merchant can do here

- Apply a promo code on the Checkout panel via the **Apply** button.
- Remove a previously-applied code via the **Remove** button (replaces *Apply* once a code is on the cart).
- See the discount reflected immediately in the *Totals* card.
- Read inline validation errors when the code is invalid / expired / not applicable.

## Settings & fields

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Discount code input** | Free-text input for the coupon string | Empty | Visible only when `cart.id` is set AND `cart.hide_discount` is false. |
| **Apply button** | POSTs the code to the cart-discount endpoint | — | On success → input flips read-only + **Remove** replaces *Apply*. |
| **Remove button** | Removes the applied code from the cart | — | Restores the *Apply* button + clears the input. |
| **Inline validation message** | Per-error message returned from the endpoint | — | Common cases: invalid code, expired code, not applicable to cart items. |
| **Discount line in Totals** | Negative line item showing the coupon-applied discount amount | — | Only renders when `discount_total_without_vat > 0`. |
| **`'cart.hide_discount'` flag** | Cart-level toggle that hides the entire Discount card | false | Used for carts where coupon use is disallowed (LTA carts, internal-only items, etc. — *(verify)*). |

## Business rules

### The PlanPanel has no code field

The plan-purchase PlanPanel does **NOT** expose an "enter coupon code" field. The merchant either:

1. Visits a promotional landing URL first (set by CloudCart marketing) that seeds the code into their session. When they then go through the purchase flow, the cart picks up the seeded code automatically.
2. Enters the code on the Discount card in the Checkout side-panel below.

If a merchant has a code but no landing URL, they should contact CloudCart support / their account manager for the right entry URL.

### Session-seeded codes flow through cart reset

When the bulk-cart promo endpoint clears the cart on PlanPanel submit and re-seeds it with the plan + add-ons (see [[plans-purchase-business-rules]]), it **also re-applies** any active promo code from the session. So the cart-reset rule preserves the session-seeded discount — the merchant doesn't have to re-enter it.

### Endpoint behaviour

`POST /admin/api/core/cart/discount` with the code:

- **Success** — server applies the coupon, recomputes cart totals, returns the updated cart. The Discount card flips to read-only + **Remove** state. The *Totals* card recomputes (Discount line + reduced Total).
- **Failure** — endpoint returns an error message which is surfaced inline below the input (e.g. "Invalid code", "Code has expired", "Code not applicable to cart items"). The cart is unchanged.

### "Price for next billing cycle" hint when promo applies only to first cycle

Some codes apply only to the first billing cycle. When that's the case, the *Order overview* card renders a small *"Price for next billing cycle"* hint under the affected cart-item line, showing the regular renewal amount. The merchant sees what they'll pay now vs. what they'll pay on renewal. See [[plans-purchase-checkout-panel]] for the Order-overview card structure.

### Discount card visibility flag

The Discount card on the Checkout panel is **hidden entirely** when `cart.hide_discount` is true. This is used for carts where coupon use is disallowed — typically LTA bundle carts and any cart flagged at creation as non-discountable. *(verify)*

### Remove + re-apply is non-destructive

Removing a code clears the discount line and restores the original total. The merchant can re-apply a different (or the same) code. The cart's other contents (plan + add-ons) are unaffected.

### Discount badges on cart items

When a billing-cycle discount AND/OR a coupon discount applies to a cart item, the *Order overview* card renders them as `cc-tag-status--enabled` badges on that item's row (one badge per discount source). The badges sit between the original price and the `Total:` line.

## Related

- [[plans-purchase]] — hub.
- [[plans-purchase-checkout-panel]] — the Checkout panel hosting the Discount card.
- [[plans-purchase-business-rules]] — cart-reset rule that preserves session-seeded codes.
- [[marketing-discounts]] — the storefront coupon / discount surface (note: storefront discounts and plan-purchase coupons are separate code namespaces — *(verify)*).
- [[plans-purchase-billing-cycle]] — the variant whose price the discount is applied to.

## Open questions

- *(verify)* Whether `cart.hide_discount` is set only on LTA-bundle carts or on other cart shapes too.
- *(verify)* Whether plan-purchase discount codes share a namespace with storefront coupons or live in a separate marketing catalog.
