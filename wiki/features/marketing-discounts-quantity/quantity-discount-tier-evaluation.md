---
type: feature
nav_path: "Marketing → Discounts → Quantity → Tier evaluation"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/quantity
aliases: ["Quantity tier matching", "Quantity discount tier algorithm", "Buy more pay less tier evaluation", "≥ quantity wins"]
tags: [marketing, discounts, quantity, cart, evaluation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, stacking, uniqueness constraint, plan gating, storefront display).

# Quantity discount — tier evaluation at cart-time

## Purpose

This aspect documents **how the platform picks a tier** when a customer's cart contains a product with a Quantity discount. It covers the "≥ quantity wins" matching rule, the 12-tier cap, the `0`-is-empty validator edge case, the per-line (not per-product-cumulative) semantics for variant lines of the same product, and why the admin order-edit screen does not re-evaluate tiers.

## Where to find it

Tier evaluation is **server-side at cart-time**; there is no admin screen that surfaces it directly. The merchant configures tiers on the form documented in [[quantity-discount-form]] at `/admin/marketing-new/discounts/create/quantity` (or `/admin/marketing-new/discounts/edit/{id}`). The cart-side ladder render is documented in [[quantity-discount-storefront-display]].

## What the merchant can do here

The merchant doesn't interact with the evaluator directly — but understanding the matching rule lets them design tier ladders that behave as intended:

- Choose tier thresholds knowing the customer can hit them per-line, not cumulatively across variants of the same product.
- Avoid the `0` trap on either tier field.
- Avoid the smallest-tier-is-N pattern when they really wanted "1+ qty discounted" (instead, use the Fixed-discount type below the lowest tier as a fallback — see [[quantity-discount-stacking]]).

## Settings & fields (used at cart-time)

The cart-time evaluator reads these stored values:

| Field | Source | What it drives |
|-------|--------|----------------|
| `conditions[].quantity` | parent Discount's `quantity_discounts` rows | The tier's minimum cart-line quantity threshold (integer pieces). |
| `conditions[].discount_value` | same | The per-piece replacement price at this tier (integer cents). |
| `customer_groups[]` | parent Discount | Cart customer's `group_id` must match (or list empty) for any tier in the ladder to apply. Guests use the store's default guest-group ID. |
| `date_start` / `date_end` | parent Discount | Cart-engine compares against the **store's local time** at evaluation. |
| `active` | parent Discount | Inactive discounts are skipped entirely. |

## Business rules

### "≥ quantity wins" — sort DESC, pick the first ≤ cart-line quantity

At cart-time, the platform reads tiers ordered by `quantity` DESC (largest threshold first) and picks the **first tier whose `quantity` is ≤ the cart-line's current quantity**. Worked examples with ladder `2 → 9 EUR`, `5 → 8 EUR`, `10 → 6 EUR`:

- Customer adds 4 pcs → tier "2" wins (4 ≥ 2, 4 < 5) → unit price = 9 EUR, line = 36 EUR.
- Customer adds 1 more (5 pcs) → tier "5" wins → unit price = 8 EUR, line = 40 EUR.
- Customer removes 4 pcs (1 pc) → below smallest tier (2) → no tier matches → catalog price (or per-variant Fixed discount if any — see [[quantity-discount-stacking]]).

### Below the smallest tier — no implicit "tier 0" row

The discount **does not "kick in" below the smallest tier's quantity**. If the smallest tier is 3, a cart with 2 pieces gets the catalog price — there's no implicit "tier 1 = catalog price" row. The Quantity ladder is opt-in at the threshold, not a replacement for catalog pricing across all quantities.

### 12 tiers is a UI cap; storage will hold whatever is submitted

The form caps the tier list at **12 entries** — after the 12th, the **+ Add new condition** link is hidden. The merchant can save with fewer (even just one tier). Removing the last tier auto-inserts a fresh empty one (so the form always shows at least one editable row).

The 12-tier cap is enforced by the form, not by a plan-feature limit and not by a stored constraint. An integration writing through the API could in principle submit more, but no admin merchant-facing path allows it.

### `0` is rejected as empty

Every tier row must have BOTH a `quantity` AND a `discount_value` filled in. A row with one empty field rejects the save with *"All conditions must be fulfilled"* (BG: *"Всички условия трябва да се попълнят"*), plus per-field errors *"Quantity is required"* / *"Discount value is required"* — see [[quantity-discount-form]].

**Important edge: `0` is treated as empty.** The save validator treats both `quantity = 0` (e.g., "free starting from 0 units") and `discount_value = 0` (e.g., "free at this tier") as missing, so the row **fails with the empty-fields error**.

To express "free at quantity N", use a small positive value like `0.01` (stored as 1 cent). The number input allows a minimum of `0`, but submitting exactly 0 still fails the save — a subtle inconsistency between the input's minimum and the actual save check.

### Customer-group filter at cart-time

Before applying any tier, the platform checks the parent Discount's `customer_groups`. If that list is non-empty, the customer's `group_id` must match one of them — otherwise the **entire tier ladder is skipped** (catalog price applies). Guests use the store's default guest-group ID; if that ID is not in the allow-list, no tier applies to them.

The filter is per-discount, not per-tier — the same allow-list gates the whole ladder. There is no way to say "Tier 1 applies to everyone, Tier 2 applies only to VIPs". Group-segmented ladders would need separate Quantity discounts per group, which collides with the one-Quantity-discount-per-product rule (see [[quantity-discount-uniqueness-constraint]]), so the pattern isn't supported on a single product.

### One discount, many cart lines — per-line evaluation

The discount targets a `product_id` (not a variant). If a cart contains two lines of the same product but different variants (e.g., size S and size M of the same shirt), the platform evaluates each line's quantity independently against the tier ladder.

The customer needs to hit the tier on the **line** — not the cumulative product total across variants. `5 size-S + 5 size-M` does NOT count as 10 toward a "buy 10" tier; each line counts on its own.

### Cart-side application is storefront-only — admin order-edit does not re-evaluate

Tier evaluation runs only on the storefront cart flow, not in the admin panel. When the merchant views or edits an existing order in the admin order-edit screen, the Quantity tier is **not re-evaluated**; the order's saved tier price persists. Adjusting the quantity there does NOT bump the line into a different tier — the saved unit price is what shows. See also [[quantity-discount-storefront-display]], which notes the same behaviour from the storefront-display angle.

### Date range — store timezone at evaluation, UTC at auto-disable

Cart-engine checks `date_start` / `date_end` against the **store's local time** when evaluating a cart line. This is independent of the daily auto-disable sweep (which runs in UTC — see the [[marketing-discounts-quantity]] hub for the timing gap). Net effect: the customer's cart stops applying tiers at the expected local time, but the discount listing keeps showing `active = yes` for up to ~27 hours after end-of-day in Europe/Sofia.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-form]] — where the tier rows are entered and validated.
- [[quantity-discount-stacking]] — what happens when the matched tier also has a Fixed / promo-code / bundle override at the same line.
- [[quantity-discount-storefront-display]] — how the tier ladder shows on the product page.
- [[marketing-discounts-fixed]] — the per-variant Fixed discount that takes over when no tier matches.
- [[customers-custom-groups]] — `customer_groups[]` allow-list source.

## Open questions

None.
