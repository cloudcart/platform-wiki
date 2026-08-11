---
type: feature
nav_path: "Marketing → Discounts → Quantity → Storefront display"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/quantity
aliases: ["Quantity discount product page", "Quantity tier ladder", "Volume discount storefront", "Quantity discount radio selectors", "Quantity discount unit price label"]
tags: [marketing, discounts, quantity, storefront, product-page]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, stacking, uniqueness constraint, plan gating).

# Quantity discount — storefront display on the product page

## Purpose

This aspect documents what the customer sees on the **storefront product detail page** when a Quantity discount is active on that product: the tier-ladder layout, the per-row text label format ("N qty" / "From A to B qty" / "over N qty"), the radio-button selector when tier quantities are consecutive, and the read-only ladder when they have gaps. It also covers the admin order-edit screen, where the tier is NOT re-evaluated (the saved unit price persists).

## Where to find it

Rendering happens on the **storefront product detail page** for any product that has at least one tier configured. It is automatic — there is no admin toggle for "show / hide tier ladder". The merchant configures tiers at `/admin/marketing-new/discounts/create/quantity` (see [[quantity-discount-form]]); the storefront picks them up from the product automatically. The admin-side counterpart is [[orders-details]], where the merchant viewing an existing order sees the saved per-line tier price.

## What the merchant can do here

The merchant cannot directly control storefront rendering of the tier ladder — but understanding the rules helps them design tier ladders that present clearly:

- **Use tight consecutive tier quantities** (e.g. 2, 3, 4, 5) to get the radio-button picker UX.
- **Use sparse tier quantities** (e.g. 5, 10, 50) to get the read-only ladder (which signals "step up by N at a time, not one piece").
- **Combine with a per-variant Fixed discount** to provide a fallback price below the smallest tier — see [[quantity-discount-stacking]].

## Settings & fields

No merchant-tunable storefront fields. The tier ladder renders automatically from the Quantity discount; the mode (radio vs read-only) is derived from the tier-quantity pattern. The values that drive the render:

| Field | What it drives at render-time |
|-------|-------------------------------|
| `conditions[].quantity` | Sorted ASCENDING on the product page; deltas between consecutive values pick the row-label format and decide radio vs read-only ladder. |
| `conditions[].discount_value` | The "unit price: <amount>" shown on each ladder row, in the store's currency. |
| `customer_groups[]` | Filters the ladder out entirely for non-matching customers (catalog price shows). |

## Business rules

### Product-page tier ladder

On the product detail page, the storefront renders the tier ladder **above the add-to-cart button**. For each tier (sorted **ascending** by `quantity`), it shows two columns:

- **Description** — one of three formats, depending on the delta between this tier's quantity and the next:
  - *"N qty"* — when consecutive tiers differ by exactly 1.
  - *"From A to B qty"* — when there's a gap between this tier's quantity and the next.
  - *"over N qty"* — for the largest tier (the open-ended top row).
- **Unit price** — formatted as *"unit price: <amount>"* in the store's currency.

The customer reads the ladder top-to-bottom as a price schedule that gets cheaper per unit at each higher quantity.

### Radio buttons vs read-only ladder

The ladder's interactivity depends on the tier quantity pattern:

- **Tight / consecutive ladders** — when all tier deltas are tight (consecutive `quantity` values, e.g. tiers at 2, 3, 4, 5), the storefront renders **radio-button selectors** next to each row so the customer can click a tier to auto-fill the quantity input.
- **Sparse / gap ladders** — when deltas are non-consecutive (e.g. tiers at 5, 10, 50), the tier list shows as a **read-only ladder** — the customer reads it as reference but must manually adjust the quantity input to reach the next tier.

The merchant doesn't pick the rendering mode — it's automatic from the tier-quantity pattern.

### No storefront timer, no sticker overlay

Quantity discounts deliberately omit:

- **No storefront countdown timer** — see [[quantity-discount-form]] for the absence of timer fields on the form.
- **No banner / label / sticker overlay** — there's no visual fields box. The storefront renders the tier list itself; there's no separate badge that says "On Sale" or "Volume offer".

If a merchant wants a sticker / promo-banner aesthetic on a quantity-tiered product, they typically combine the Quantity discount with a separate visual treatment via theme customization or a separate marketing campaign.

### Cart-line display

On the cart and checkout, the per-line price shows the **applied tier's `discount_value`** as the unit price. The customer sees:

- Unit price = tier value (NOT the catalog price).
- Line total = tier value × cart-line quantity.
- The "saving versus catalog" computed dynamically per-line at cart-time (the saved amount is the delta between catalog and tier price; see [[discounts-storefront-display]] for the cross-cutting per-line saving display).

The catalog price is NOT shown crossed-out next to the tier price on the cart line unless the theme implements it independently; the platform doesn't surface the strike-through automatically for Quantity tier replacements.

### Admin order-edit display — saved tier price persists

Quantity tier evaluation does NOT run in the admin order-edit screen (see [[quantity-discount-tier-evaluation]] for the cart-time matching angle). Net effect on display:

- The merchant sees the existing order's saved per-line tier price.
- Adjusting a line's quantity in the admin does NOT re-evaluate to a different tier — the saved unit price stays.
- If the merchant deletes a Quantity discount on a product, past orders still show their original tier price (the delete only affects the parent discount, not the historical order records — see [[quantity-discount-uniqueness-constraint]]).

This is intentional: it preserves order history and prevents retroactive price changes on already-placed orders.

### Variant-picker integration

The tier ladder is rendered for the parent product, but the cart-line evaluation happens per variant line (see [[quantity-discount-tier-evaluation]] for the per-line / per-variant rule). The customer picking different variants of the same product sees the same tier ladder above the add-to-cart button, and each variant they add becomes a separate cart line that's evaluated against the ladder independently.

The customer can't "combine 3 size-S + 2 size-M = 5 toward a buy-5 tier" — each line evaluates on its own. Storefront display does not warn the customer of this; they may be surprised at checkout that the cumulative-quantity logic doesn't apply.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-tier-evaluation]] — cart-time matching that determines which tier the storefront line displays.
- [[quantity-discount-form]] — confirms there are no timer / sticker / banner fields on the form.
- [[quantity-discount-stacking]] — what happens visually when a tier line also has a promo code applied.
- [[quantity-discount-uniqueness-constraint]] — the delete-cascade rule that preserves past-order display.
- [[discounts-storefront-display]] — cross-cutting storefront rendering rules for all discount types.
- [[products-products]] — the product the tier ladder renders on.

## Open questions

- The exact theme template names that render the tier ladder per storefront theme (varies across CloudCart's themes). `(verify)`

