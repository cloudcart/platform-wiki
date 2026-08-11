---
type: concept
nav_path: "Concept → Multi-currency → Store currency model"
aliases: ["Store currency model", "Single-currency store", "Currency setting", "Currency dropdown", "No customer-facing currency switcher", "Currency and units", "Валута на магазина — модел"]
tags: [finance, currency, store-currency, settings, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[multi-currency]]. See the hub for the other aspects (price storage, order snapshot, FX rates, BGN → EUR transition, payment providers, taxes & analytics).

# Multi-currency — store currency model

## Definition

A CloudCart store has **exactly one** active currency at any moment, set in [[settings-general]] → *Currency and units* box → **Currency** dropdown. The chosen value lives in the `currency` setting (e.g., `BGN`, `EUR`, `RON`, `USD`) and acts as the implicit unit for every monetary field across products, variants, discounts, shipping rates, taxes, payment fees, bundles, cross-sells, form fields, and quantity discounts. There is no per-product or per-variant override.

The country chosen in [[settings-general]] → *Country of operations* determines the **default suggested** currency on first setup (a Bulgarian store defaults to BGN, a Romanian store to RON, etc.), but the merchant can override the suggestion before saving. The currency dropdown lists every standard ISO 4217 code bundled with the platform.

Customers visiting the storefront see prices in **one** currency. There is no first-party "Switch to EUR / Switch to USD" widget; the only dual-currency rendering shipped by CloudCart is [[apps-bgn2eur]], which always displays BOTH currencies side-by-side (the customer never picks).

## Scope

Covered:

- Where the merchant picks the store currency.
- What changes and what does NOT change when the merchant edits the currency value.
- The unrendered `currencyAlertForExistingOrders` flag — why merchants get no in-app warning before changing currency on a live store.
- Why there is no customer-facing currency switcher.
- How per-market pricing is approximated through [[apps-multilang]] sister sites.

Not covered here:

- The actual storage of monetary values without a currency tag — see [[multi-currency-price-storage]].
- The order's frozen `currency` field — see [[multi-currency-order-snapshot]].
- The BGN → EUR Convert action — see [[multi-currency-bgn-eur-transition]].
- FX rates synced from Fixer.io — see [[multi-currency-fx-rates]].
- Currency-specific payment providers — see [[multi-currency-payment-providers]].

## Contrasts

- **Currency change vs. price re-entry** — saving a new currency in [[settings-general]] is a **label flip**, not a re-price. Numeric values are unchanged. See [[multi-currency-price-storage]] for the implementation reason and [[multi-currency-bgn-eur-transition]] for the only safe re-pricing path.
- **Per-store currency vs. per-customer currency** — every customer of one store sees the same currency at the same moment. Multi-language ([[multi-language]]) is per-customer; currency is not.
- **First-party dual-display vs. third-party switcher** — [[apps-bgn2eur]] renders BOTH BGN and EUR at a fixed rate; it is NOT a customer-pick switcher. True multi-currency switchers are custom theme development.
- **Single store with one currency vs. multiple sister sites with different currencies** — when a merchant wants per-market pricing (e.g., 100 BGN for BG customers vs 60 EUR for DE customers), the standard pattern is [[apps-multilang]] sister sites, each with its own currency and its own pricing transformed via a merchant-defined multiplier.

## Where it applies

### Picking the currency

The merchant edits the currency in [[settings-general]] → *Currency and units* box → **Currency** dropdown. The field is required. The list is the bundled ISO 4217 catalogue. The chosen value is saved into the `currency` setting and the country-of-operations default only matters at first setup.

### What changes on save

Saving a new currency in [[settings-general]]:

1. Updates the `currency` setting.
2. Regenerates the storefront's JavaScript data file (which carries the catalog with formatted prices) — the storefront then renders prices with the new currency code and the platform's number-format conventions for that currency (separator, decimal mark, symbol placement).
3. Flushes the settings cache so every read across the platform sees the new value immediately.

### What does NOT change on save

The actual numeric price values stored against every Product, Variant, Discount, Shipping Rate, Tax, Payment Fee, etc. are untouched. A product priced `19.99` in BGN before the change is still stored as `19.99` after the change — it just renders with the new currency symbol. So switching `BGN` → `EUR` without running the BGN → EUR Convert action makes every price ~1.96× higher in real money (a 19.99 BGN product becomes 19.99 EUR, ≈ 39 BGN equivalent).

### The unrendered warning for existing orders (verify)

The platform internally computes a `currencyAlertForExistingOrders` flag (true when the store has completed orders) intended to warn the merchant — but the [[settings-general]] page does NOT render the warning to the user. (verify) Merchants changing currency post-launch get NO in-app warning that historical orders will look weird. The support workflow should always check whether the store has prior orders before recommending a currency change.

### Why there is no customer-facing currency switcher

Customers visiting the storefront see prices in the single currency from the `currency` setting. There is no "Switch to EUR / Switch to USD" module supplied by CloudCart out of the box. If a merchant wants a true multi-currency switcher (typical pattern: USD / EUR / GBP per customer choice, with rates pulled from a third-party API), that is **custom theme development** — not a standard platform feature.

The only first-party dual-currency rendering is the BGN → EUR app, which always shows BOTH currencies (never letting the customer pick). See [[multi-currency-bgn-eur-transition]].

### Per-market pricing via Multilang sisters

For merchants who want different prices in different markets, the standard CloudCart pattern is [[apps-multilang]] sister sites. Each sister has its own currency setting and its own pricing. Sister-site pricing can be derived from the master via a `price_change` multiplier on the per-sister Multilang settings (e.g., `1.10` adds a 10% markup), with `price_round` controlling rounding. Manual edits on the sister override the transformed price for that product.

This is the closest CloudCart comes to per-market pricing — and it is a build-time copy with a multiplier, not a runtime currency switch.

## Related

- [[multi-currency]] — hub.
- [[settings-general]] — where the merchant picks the currency.
- [[multi-currency-price-storage]] — why a currency change is a label-flip.
- [[multi-currency-bgn-eur-transition]] — the only safe re-pricing path (Bulgaria-specific).
- [[multi-language]] — sister concept; per-customer language is independent of per-store currency.
- [[apps-multilang]] — sister sites pattern for per-market pricing.

## Open Questions

- ⏸️ Confirm in the current Vue admin whether the `currencyAlertForExistingOrders` warning ever surfaces (it is computed but not rendered as of the most recent inspection). (verify)
