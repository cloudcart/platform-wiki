---
type: concept
nav_path: "Concept → Shipping calculation → Discounts and Cart Rules"
aliases: ["Free shipping discount vs rate row", "Cart Rules shipping override", "Percentage off shipping", "Force shipping method", "order_over free shipping", "Безплатна доставка отстъпка", "Правила за поръчка доставка"]
tags: [shipping, discounts, cart-rules, free-shipping, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, carrier integrations, the checkout cascade, COD surcharge, persistence).

# Shipping — Discounts and Cart Rules

## Definition

After the [[shipping-calc-cascade|8-step cascade]] decides which methods are available and the customer picks one, two layers can still modify the shipping line — this is **Step 9** of the calculation:

- **Free-Shipping discounts** (the Free-Shipping type from [[marketing-discounts-shipping]]) can ONLY zero out the shipping line: they add a NEGATIVE totals line equal to the carrier's quote, netting zero. No percentage or partial reductions.
- **[[apps-cart-rules|Cart Rules]]** have one shipping action, Free shipping, which also zeroes the whole line. Their amount and percent actions reduce the goods, not the shipping line.

The two layers run in order: **Discounts FIRST, Cart Rules SECOND.** A Cart Rule's free shipping applies only if no discount took the row.

A third, simpler pattern involves neither layer: a **`$0` rate row** on a custom method ([[shipping-calc-rate-models]]) makes the SHIPPING METHOD itself free for the bracket. Simplest when the merchant just wants "free shipping above 100 EUR".

## Scope

Covered: Free-shipping discount mechanics (`target = order_over`, customer-group / region / `only_customer` restrictions, dates / max-uses / code-stacking); the one-free-shipping-row-per-cart cap and its order (no-code or Cross-Sell → code → payment method → Cart Rule); discount applied AFTER the carrier quotes; the Cart Rule free-shipping action; and the setup patterns for a free-shipping threshold.

Not covered: other discount types and percentage / flat-amount logic (see [[marketing-discounts-shipping]]); the Cart Rules app's general conditions / actions / scoping / stacking (see [[apps-cart-rules]]); cascade Steps 1–8 that pick the method this layer modifies (see [[shipping-calc-cascade]]); how the modified line is saved (see [[shipping-calc-persistence]]).

## Contrasts

- **`$0` rate row vs. Free-Shipping discount** — a `$0` row makes THIS METHOD free for the bracket (order shows `shipping = 0`). A discount adds a negative offset to the carrier's quote (order shows `carrier quote = X, discount line = -X, net = 0`). The discount path is more flexible (threshold via `order_over`, customer-group restrictions, promo codes with a region) but the customer must qualify.
- **Discounts vs. Cart Rules** — Discounts are merchant-facing and visible in [[marketing-discounts-shipping]]. Cart Rules are an app, with their own conditions on cart contents and customer history. Both zero the whole line.
- **Discount BEFORE Cart Rule** — when a free-shipping discount took the row, a Cart Rule's free shipping adds no second row.
- **One free-shipping row per cart** — many eligible free-shipping discounts can exist, but only one row shows; the order is no-code or Cross-Sell → code → payment method → Cart Rule.

## Where it applies

### Free-Shipping discount mechanics

A discount of type **Free Shipping** ([[marketing-discounts-shipping]]) applies when ALL pass:

- **Active** — within its date range, under max-uses, not paused.
- Cart matches the **target**: `target = all` (no minimum) or `target = order_over` (only when the total before shipping, after whole-order discounts, is at or above the threshold).
- Cart matches any **customer-group** and **region** restrictions set, and the customer is one of the **specific customers** if any are picked.
- **Code-stacking rules** satisfied (customer entered the code, or the discount is auto-apply).

When all gates pass, the platform adds a NEGATIVE totals line equal to the carrier's quoted shipping. The order detail shows the carrier's positive quote AND the discount's negative offset side-by-side. The discount runs AFTER the carrier quotes, so the saved amount IS the carrier's quote — no pre-discount lookup.

**One free-shipping row per cart maximum.** The first that applies takes it: no-code discount or Cross-Sell → code (customer entered a code) → payment method → Cart Rule.

### No partial shipping discount

Discounts can only zero out shipping, and so can [[apps-cart-rules|Cart Rules]]. There is no percentage or partial shipping reduction, no forced shipping method, no COD surcharge action in Cart Rules, and no Cart Rule condition on the delivery method.

### Run-order: Discounts FIRST, Cart Rules SECOND

Cascade Steps 1–8 produce a method and quote. Then one row takes it: a no-code discount or Cross-Sell, else a code, else a payment-method free shipping, else a Cart Rule's.

### Patterns for "free shipping above a threshold"

- **Option A — `$0` rate row** (custom method, no discount). A Custom **Based on price** method, e.g. `0–50 → 5.00`, `50–100 → 3.00`, `100–blank → 0.00`. Carts of 100+ get free shipping; `amount = 0` renders as "Free". Simplest for the merchant.
- **Option B — Free-Shipping discount with `order_over`** (`target = order_over`, `order_over = 100`). Customer keeps a normal paid method, the discount zeros it once the total before shipping reaches 100. Lets the same threshold work uniformly across multiple methods.
- **Option C — Cart Rule with a cart-amount condition** — the Free shipping action zeroes the line when the condition is met. Most flexible (customer-group / category / cart-content conditions) but needs the app and is least discoverable.
- **Option D — the shipping method's own *Free shipping threshold*** on [[settings-shipping]]. Set per method, runs at quote time.

### Free shipping is NEVER global

There is no store-wide "Free shipping above 100 EUR" master setting on [[settings-shipping]] or [[settings-cart]]. Each shipping method has its own Free shipping threshold; every other free-shipping configuration is one of the patterns above.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-cascade]] — Steps 1–8 that produce the method this layer modifies.
- [[shipping-calc-rate-models]] — `$0` rate row pattern.
- [[shipping-calc-cod-surcharge]] — COD surcharge.
- [[shipping-calc-persistence]] — how the modified line is saved.
- [[marketing-discounts-shipping]] — Free-Shipping discount type.
- [[apps-cart-rules]] — Cart Rules app and its Free shipping action.
- [[settings-cart]] — checkout defaults.

## Open Questions

None.
