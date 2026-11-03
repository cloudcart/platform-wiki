---
type: concept
nav_path: "Concept → Shipping calculation → Discounts and Cart Rules"
aliases: ["Free shipping discount vs rate row", "Cart Rules shipping override", "Percentage off shipping", "Force shipping method", "order_over free shipping", "Безплатна доставка отстъпка", "Правила за поръчка доставка"]
tags: [shipping, discounts, cart-rules, free-shipping, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, carrier integrations, the checkout cascade, COD surcharge, persistence).

# Shipping — Discounts and Cart Rules

## Definition

After the [[shipping-calc-cascade|8-step cascade]] decides which methods are available and the customer picks one, two layers can still modify the shipping line — this is **Step 9** of the calculation:

- **Free-Shipping discounts** (the Free-Shipping type from [[marketing-discounts-shipping]]) can ONLY zero out the shipping line: they add a NEGATIVE totals line equal to the carrier's quote, netting zero. No percentage or partial reductions.
- **[[apps-cart-rules|Cart Rules]]** can do anything — add a fixed amount, subtract a fixed amount, apply a percentage, force a specific shipping method, add or remove COD surcharges.

The two layers run in order: **Discounts FIRST, Cart Rules SECOND.** A free-shipping discount that already zeroed the line makes the Cart Rule operate on zero, which can turn it into a no-op.

A third, simpler pattern involves neither layer: a **`$0` rate row** on a custom method ([[shipping-calc-rate-models]]) makes the SHIPPING METHOD itself free for the bracket. Simplest when the merchant just wants "free shipping above 100 BGN".

## Scope

Covered: Free-shipping discount mechanics (`target = order_over`, customer-group / region / `only_customer` restrictions, dates / max-uses / code-stacking); the one-shipping-typed-discount-per-cart cap and first-match precedence (code-applied → global → `order_over`); discount applied AFTER the carrier quotes; partial shipping discounts via Cart Rules; the four Cart Rule shipping powers; Cart Rules adding / removing COD surcharges; the Discounts-FIRST, Cart-Rules-SECOND run-order; and the three setup patterns for a free-shipping threshold.

Not covered: other discount types and percentage / flat-amount logic (see [[marketing-discounts-shipping]]); the Cart Rules app's general conditions / actions / scoping / stacking (see [[apps-cart-rules]]); cascade Steps 1–8 that pick the method this layer modifies (see [[shipping-calc-cascade]]); how the modified line is saved (see [[shipping-calc-persistence]]).

## Contrasts

- **`$0` rate row vs. Free-Shipping discount** — a `$0` row makes THIS METHOD free for the bracket (order shows `shipping = 0`). A discount adds a negative offset to the carrier's quote (order shows `carrier quote = X, discount line = -X, net = 0`). The discount path is more flexible (threshold via `order_over`, customer-group / region restrictions, promo codes) but the customer must qualify.
- **Discounts vs. Cart Rules** — Discounts are merchant-facing and visible in [[marketing-discounts-shipping]]. Cart Rules are an app — less discoverable, but support arbitrary modification (percentage, force-method, conditional COD surcharge). The most powerful and the least visible shipping override.
- **Discount BEFORE Cart Rule** — a free-shipping discount that zeroed the line makes the subsequent Cart Rule operate on zero, often a no-op. Don't stack a percentage-off-shipping Cart Rule on top of a free-shipping discount — one wins, not both.
- **One shipping-typed discount per cart** — many eligible free-shipping discounts can exist, but only one applies to a cart; the engine picks the first match in precedence code-applied → global → `order_over`.

## Where it applies

### Free-Shipping discount mechanics

A discount of type **Free Shipping** ([[marketing-discounts-shipping]]) applies when ALL pass:

- **Active** — within its date range, under max-uses, not paused.
- Cart matches the **target**: `target = all` (every cart) or `target = order_over` (only when `cart.subtotal >= order_over_threshold`).
- Cart matches any **customer-group**, **region**, and **`only_customer`** restrictions set.
- **Code-stacking rules** satisfied (customer entered the code, or the discount is auto-apply).

When all gates pass, the platform adds a NEGATIVE totals line equal to the carrier's quoted shipping. The order detail shows the carrier's positive quote AND the discount's negative offset side-by-side. The discount runs AFTER the carrier quotes, so the saved amount IS the carrier's quote — no pre-discount lookup.

**One shipping-typed discount per cart maximum.** First eligible in precedence wins (subsequent matches skipped): code-applied (customer entered a code) → global (auto-apply targeting `all`) → `order_over` (auto-apply threshold).

### Partial shipping discounts via Cart Rules

Discounts can only zero out shipping. For partial reductions ("20 % off shipping for VIPs", "5 BGN off shipping over 50 BGN"), the merchant uses [[apps-cart-rules]], which can:

- **Add** a fixed amount to the shipping line.
- **Subtract** a fixed amount from it.
- **Apply a percentage** to it.
- **Override the shipping method entirely** — force a specific method on qualifying carts, regardless of the customer's pick.
- **Add or remove a COD surcharge** on a method.

Cart Rules are the only way to express "10 % off shipping" or "force this method" — neither Discounts nor the rate-row model can.

### Run-order: Discounts FIRST, Cart Rules SECOND

Cascade Steps 1–8 produce a method and quote → Free-Shipping discount, if eligible, zeroes it → Cart Rules run on the (possibly already-zeroed) quote. This matters in two scenarios:

- **"15 % off shipping" Cart Rule + "Free shipping above 100 BGN" discount** — for carts ≥ 100 BGN the discount zeros the line, so 15 % off zero is still zero; the 15 % is ignored above the threshold. The merchant wants ONLY ONE layer, not both.
- **"Force method = Econt" Cart Rule + free-shipping discount** — the discount zeros the Econt quote; force-method runs on the zeroed quote and still selects Econt. Forcing a method is independent of the line amount, so this combination works.

### Three patterns for "free shipping above a threshold"

- **Option A — `$0` rate row** (custom method, no discount). A Custom **Based on price** method, e.g. `0–50 → 5.00`, `50–100 → 3.00`, `100–blank → 0.00`. Carts of 100+ get free shipping; `amount = 0` renders as "Free". Simplest for the merchant.
- **Option B — Free-Shipping discount with `order_over`** (`target = order_over`, `order_over = 100`). Customer keeps a normal paid method, the discount zeros it once subtotal hits 100. Lets the same threshold work uniformly across multiple methods.
- **Option C — Cart Rule with subtotal condition** — subtracts the full shipping amount when subtotal ≥ 100. Most flexible (customer-group / category / cart-content conditions) but needs the app and is least discoverable. Required for any condition beyond subtotal.

### Free shipping is NEVER global

There is no store-wide "Free shipping above 100 BGN" master setting on [[settings-shipping]] or [[settings-cart]]. Every free-shipping configuration is one of the three patterns above. Merchants asking "where's the free-shipping threshold setting?" — there isn't one.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-cascade]] — Steps 1–8 that produce the method this layer modifies.
- [[shipping-calc-rate-models]] — `$0` rate row pattern.
- [[shipping-calc-cod-surcharge]] — COD surcharge that Cart Rules can add or remove.
- [[shipping-calc-persistence]] — how the modified line is saved.
- [[marketing-discounts-shipping]] — Free-Shipping discount type.
- [[apps-cart-rules]] — Cart Rules app for partial / percentage / force-method overrides.
- [[settings-cart]] — checkout defaults.

## Open Questions

None.
