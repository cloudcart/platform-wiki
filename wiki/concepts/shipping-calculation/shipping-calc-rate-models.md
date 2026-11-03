---
type: concept
nav_path: "Concept → Shipping calculation → Rate models"
aliases: ["Shipping rate models", "Based on price", "Based on weight", "Based on price and weight", "Local pickup shipping", "Marketplace shipping", "Rate-row table", "Custom shipping methods", "Тегло и цена", "По цена", "По тегло", "Локално вземане", "Blank upper bound", "Empty to value", "Empty upper weight", "до кг празно", "Празна горна граница", "до безкрайност", "no upper limit", "Shipping method not showing at checkout", "Why is my shipping method missing", "Доставката не се показва"]
tags: [shipping, checkout, rates, custom-methods, marketplace, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (geo gating, carrier integrations, the checkout cascade, COD surcharge, discounts + Cart Rules, persistence).

# Shipping — rate models

## Definition

Every shipping method on [[settings-shipping]] has exactly one **rate model** — the algorithm that converts a cart into a shipping quote. CloudCart supports five:

| `type` | Source of the quote | Editable by merchant |
|--------|---------------------|----------------------|
| `price` | Rate-row table indexed by cart **subtotal** | YES — full table |
| `weight` | Rate-row table indexed by cart **total weight** | YES — full table |
| `price_and_weight` | Rate-row table with BOTH dimensions | YES — full table |
| `marketplace` | Flat pickup fee at a physical store location | YES — pickup fee per location |
| `integration` | Live API call to the carrier's `getQuotes` endpoint | NO — carrier owns the price |

Custom-method models (`price`, `weight`, `price_and_weight`, `marketplace`) live entirely on CloudCart — rate rows in the merchant's database, edited from the method's settings page. Carrier integrations (`integration`) are documented separately on [[shipping-calc-carrier-integrations]].

### Rate-row table semantics

Every custom-method rate row has a `from / to` range and an `amount`:

- **Both bounds are inclusive.** A row matches when `from ≤ value` **and** `value ≤ to`. So a row `from = 50, to = 100` matches `50.00 ≤ subtotal ≤ 100.00` (the engine tests `from ≤ value AND (value ≤ to OR to is blank)`).
- **A blank `to` (upper bound) means NO upper limit — the bracket runs to infinity** ("`from` and above"). This is the normal, intended way to write the top open-ended row. A blank upper bound does **NOT** make the row invalid and does **NOT** hide the method at checkout — quite the opposite, it is what guarantees every heavier/pricier cart is still covered. A single row with `from = 0` (or blank) and a blank `to` therefore matches **every** cart.
- **A blank `from` (lower bound) means start at 0** — no lower limit.
- **On overlap, the cheapest matching row wins.** Because both bounds are inclusive, a boundary value (e.g. exactly `50` against rows `0–50` and `50–100`) matches BOTH rows; the engine then keeps the one with the **lowest `amount`** (category-specific rows are tried first — see the category-rate split below). Overlapping brackets don't error — they resolve to the cheaper rate.
- `amount = 0` renders as **"Free"** at checkout — the customer sees zero, no negative line, no discount paired.
- The method is **dropped** from checkout only when **NO row matches**, and the single way that happens is a cart value **below the lowest `from`** (e.g. subtotal `30` against a table whose lowest `from` is `50`). An open-ended top row (blank `to`) is exactly what prevents the equivalent gap at the high end — so "the upper bound is empty" is **never** the reason a method fails to show.

## Scope

Covered:

- The five rate models and which is editable by the merchant.
- Rate-row table semantics: `from`-inclusive, `to`-exclusive, blank-`to` unbounded, `$0` = free.
- **Based on price** lookup against cart subtotal (line totals + per-product taxes, BEFORE shipping).
- **Based on weight** lookup against cart total weight (sum of `weight × quantity` in the store's [[settings-general]] unit — kg or lb); products with no weight = zero weight, which under-quotes.
- **Based on price and weight** — two-dimensional matching.
- **Local Pickup / Marketplace** — physical store location selection with configured pickup fee.
- **Category-rate split** — Step 4 of the cascade; per-category secondary rate table summed with the default.

Not covered here:

- The live carrier API path (`type = integration`) — see [[shipping-calc-carrier-integrations]].
- How the method becomes available for the cart's address — see [[shipping-calc-geo-gating]].
- The full Step 1–8 cascade — see [[shipping-calc-cascade]].
- COD surcharge mechanics — see [[shipping-calc-cod-surcharge]].
- Free-shipping discounts vs `$0` rate rows — see [[shipping-calc-discounts-rules]].

## Contrasts

- **Custom rate rows vs. carrier-quoted prices** — custom-method rows are fully under merchant control. Carrier-integration prices are opaque and cannot be overridden on the rate level (only via [[apps-cart-rules]] post-quote).
- **`$0` rate row vs. Free-Shipping discount** — `$0` row makes THIS METHOD free for the bracket; discount adds a negative offset to whatever the carrier quoted. See [[shipping-calc-discounts-rules]].
- **`price` vs. `weight` vs. `price_and_weight`** — choose `price` when freight cost correlates with order value (digital + light goods, retail). Choose `weight` when freight cost correlates with mass (bulky goods). Choose `price_and_weight` when the merchant's logistics partner prices by both dimensions (e.g., heavy + cheap items vs. light + expensive items).
- **`marketplace` vs. zero-priced custom method** — marketplace forces the customer to pick a physical [[apps-store-locations|store location]]; a zero-priced custom method has no location step. Use marketplace only when the merchant runs physical pickup points; otherwise a `$0` row on a normal `price` method is simpler.

## Where it applies

### Based on price (`type = price`)

Example table:

| from | to | amount |
|------|-----|--------|
| 0 | 50 | 5.00 |
| 50 | 100 | 3.00 |
| 100 | _(blank)_ | 0.00 |

- Subtotal `30` → 5.00 (only the `0–50` row matches).
- Subtotal `50` → 3.00 (`50` matches BOTH `0–50` and `50–100` — the cheaper `3.00` wins).
- Subtotal `99.99` → 3.00 (only the `50–100` row).
- Subtotal `100` → 0.00 (matches BOTH `50–100` and the open `100+` row — the cheaper `0.00` wins).
- Subtotal `5000` → 0.00 (the open top row has **no upper limit**, so it still matches).

### Based on weight (`type = weight`)

Same logic but the lookup key is cart total weight. Weight unit follows the store unit-system on [[settings-general]] (kg for metric, lb for imperial).

| from | to | amount |
|------|-----|--------|
| 0 | 2 | 4.00 |
| 2 | 5 | 6.00 |
| 5 | _(blank)_ | 10.00 |

A 1.5 kg cart → 4.00; 4.99 kg → 6.00; 10 kg → 10.00; a 500 kg cart → **still 10.00** — the `5 → blank` top row has no upper limit, so heavy carts never fall through.

**Unweighted products are a footgun.** A product with no `weight` set contributes `0` to the cart-weight calculation. A weight-based method against a cart of unweighted products quotes the lowest bracket (often `$0` if `0 ≤ from < 0.0001` matches), regardless of actual freight cost. Merchants on weight-based shipping must fill `weight` on every product.

### Based on price and weight (`type = price_and_weight`)

Rate rows have BOTH `from / to` price brackets AND `from / to` weight brackets. The matching row is the one where the cart's subtotal AND total weight both fall in range. Most complex of the custom models.

### Local Pickup / Marketplace (`type = marketplace`)

The customer does not pay a typical shipping fee — they pick a physical **store location** the merchant has configured via the Stores app ([[apps-store-locations]]). The checkout shipping line reads *"Local pickup from [Store Name]"* and the configured pickup fee (often `0`). Available only when the Stores app is installed and at least one location is defined.

### Category-rate split (Step 4 of the cascade, custom methods only)

Custom methods support a SECOND rate table scoped to specific product categories. When "Different price for categories" is turned ON for the method:

- For each line item whose product belongs to one of the category-specific categories, the platform computes the rate from the **category-specific rate table** for that line's contribution to the subtotal.
- Lines that don't match the category use the default rate table.
- The two contributions are **summed** for the final method quote.

Useful for "heavy furniture costs more to ship than other products" patterns. The split applies only to `price`, `weight`, and `price_and_weight` — `marketplace` and `integration` ignore the category-rate split entirely.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-geo-gating]] — geographic filtering that runs BEFORE rate-row lookup.
- [[shipping-calc-carrier-integrations]] — the `integration` rate model.
- [[shipping-calc-cascade]] — full Step 1–8 sequence with rate-row lookup as Step 3.
- [[shipping-calc-discounts-rules]] — `$0` rate row vs. free-shipping discount.
- [[settings-shipping]] — the method-edit screen with the rate-row table editor.
- [[settings-general]] — store unit-system (kg vs. lb) used by `weight` model.
- [[apps-store-locations]] — store-locations app required by the `marketplace` model.

## Open Questions

- (verify) **Multi-package / split shipments.** CloudCart's rate models treat each cart as a single package — there is no platform-wide multi-package layer that splits a large order into multiple labels at the calculation step. Some carrier integrations (Speedy, Econt) expose multi-package fields on their own per-app forms; behaviour varies per carrier and is documented on each integration's dedicated page rather than here.
