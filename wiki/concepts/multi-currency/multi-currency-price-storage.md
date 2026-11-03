---
type: concept
nav_path: "Concept → Multi-currency → Price storage"
aliases: ["Price storage", "Currency-less price storage", "currency_code accessor", "Label flip currency change", "Implicit currency unit", "Съхранение на цени"]
tags: [finance, currency, pricing, storage, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[multi-currency]]. See the hub for the other aspects (store currency model, order snapshot, FX rates, BGN → EUR transition, payment providers, taxes & analytics).

# Multi-currency — price storage

## Definition

Every monetary field in the platform stores a **numeric value with no currency tag**. The store's `currency` setting is the **implicit unit**. There is no `currency_code` column on Product, Variant, Discount, Shipping Rate, Tax, or Payment Fee. The Product's `currency_code` accessor is **derived** — it returns the current value of `site('currency')`, not a value stored against the product itself.

The direct consequence: when the merchant sees the price `19.99` on a product, that value can be interpreted as 19.99 BGN OR 19.99 EUR OR 19.99 RON, depending on which currency the store is set to **at the moment of viewing**. The platform does NOT preserve "this price was set when the store was in BGN" — it always reads through the current setting.

This is the implementation reason behind the BGN → EUR **Convert** flow being the merchant's only safe path through a real currency change: the Convert action goes through every monetary field and rewrites it mathematically (price / 1.95583), so a 19.99 BGN product becomes 10.22 EUR — a real conversion, not a label flip. See [[multi-currency-bgn-eur-transition]].

## Scope

Covered:

- How the platform stores monetary values without a currency tag.
- The derived `currency_code` accessor and what it returns.
- Why changing the store currency is a label-flip, not a re-price.
- The financial impact of an unconverted currency change (≈ 1.96× over-pricing for BGN → EUR).

Not covered here:

- The actual currency picker UI — see [[multi-currency-store-currency-model]].
- Per-order frozen currency — see [[multi-currency-order-snapshot]].
- The Convert action's full field catalogue — see [[multi-currency-bgn-eur-transition]].
- FX rates available for internal conversion — see [[multi-currency-fx-rates]].

## Contrasts

- **Stored value vs. rendered value** — the database holds the bare number; the storefront and admin panel render it with the current `currency` symbol and locale-appropriate formatting. The render is dynamic; the stored value is static.
- **Per-product currency tag (does not exist) vs. derived `currency_code` accessor** — the accessor LOOKS like a per-product field but it always returns the site-wide `currency` setting. There is no way for two products on the same store to be priced in different currencies.
- **Label flip vs. mathematical conversion** — saving a different currency in [[settings-general]] does not touch numeric values. The BGN → EUR Convert action actually divides each price by 1.95583. Only one of those two is a real currency change.

## Where it applies

### The fields that store numeric values

Every monetary field below stores a bare number interpreted in the store currency:

- Product `price`, `price_from`, `price_to`.
- Variant `price`, `delivery_price`.
- Discount amounts (flat, percent, shipping, fixed-price, quantity-step prices).
- Discount-code targets, Code-Pro targets.
- Cart Rule action prices and trigger-condition prices.
- Smart-collection price-range conditions.
- Bundle prices.
- Cross-sell action and target prices.
- Form-field prices (add-ons configured by the merchant).
- Shipping rate prices on every shipping method.
- Flat tax amounts (percentage taxes apply to whichever currency the price is in — see [[multi-currency-taxes-analytics]]).
- Payment-provider fees and a separately-configured currency code per provider — see [[multi-currency-payment-providers]].

The fact that none of these carries its own currency tag is what makes the BGN → EUR Convert action a single coherent operation: it can sweep every monetary field in the store and rewrite it under one rule.

### The derived `currency_code` accessor

Asking a Product (in code or via JSON-API v2) for its currency returns the site's current currency, not a value stored against the product. The accessor exists so consumers don't have to look up the site setting separately, but it provides no per-product flexibility.

### What this means for a naive currency change

Switching the [[settings-general]] currency dropdown from `BGN` to `EUR` and saving:

- Every product still has its old numeric price.
- The storefront now renders each price with the EUR symbol.
- A `19.99` BGN product becomes a `19.99` EUR product visually — but EUR is ≈ 1.96× the value of BGN, so the merchant has effectively raised every price by 96%.
- New orders capture the EUR-tagged value as the order's frozen currency.
- Historical orders (placed in BGN) keep their BGN currency snapshot — see [[multi-currency-order-snapshot]].

This is rarely what the merchant intends. For a Bulgarian store moving to EUR, the [[apps-bgn2eur]] Convert action is the only safe path. For any other currency change, the merchant has no in-platform tool; manual export, recompute in a spreadsheet, re-import.

### Per-variant currency overrides do not exist

There is no per-Variant currency override field. The Variant's `price` is interpreted in the store currency, full stop. The BGN → EUR Convert action rewrites every Variant price; nothing else can change a Variant's currency.

If a merchant wants to sell to BOTH a Bulgarian (BGN) and a Romanian (RON) audience from one store at different price points, the standard answer is: they can't, with one CloudCart store. Either run TWO separate CloudCart stores (one in BGN, one in RON), pick the store currency and let customers in the other market deal with their bank's conversion, or use [[apps-multilang]] sister sites — see [[multi-currency-store-currency-model]].

The merchant CAN configure **shipping methods scoped to geo zones** so Bulgarian customers see different shipping rates from Romanian customers (still numeric values in the store currency, just scoped) — but they're still all the same currency.

## Related

- [[multi-currency]] — hub.
- [[multi-currency-store-currency-model]] — the currency-setting UI and what changes / does not change on edit.
- [[multi-currency-bgn-eur-transition]] — the Convert action that performs a real re-price.
- [[multi-currency-order-snapshot]] — why historical orders keep their original numeric values.
- [[product]] — Product entity carrying price fields without currency tag.
- [[variant]] — Variant entity carrying `price` and `delivery_price`.
- [[settings-general]] — where the implicit unit is set.

## Open Questions

None.
