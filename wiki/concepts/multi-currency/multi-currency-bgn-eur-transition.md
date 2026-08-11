---
type: concept
nav_path: "Concept → Multi-currency → BGN → EUR transition"
aliases: ["BGN to EUR transition", "BGN → EUR Convert action", "Dual-currency display app", "Fixed 1.95583 rate", "Bulgaria currency transition", "Преход BGN към EUR"]
tags: [finance, currency, bgn, eur, bulgaria, transition, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-currency]]. See the hub for the other aspects (store currency model, price storage, order snapshot, FX rates, payment providers, taxes & analytics).

# Multi-currency — BGN → EUR transition

## Definition

Bulgaria's national-bank-set fixed rate `1 EUR = 1.95583 BGN` drives a Bulgaria-specific app — [[apps-bgn2eur]] — used by all Bulgarian stores during the 2026 currency transition. The app does two things: it **dual-displays prices** in BGN and EUR side-by-side at the fixed rate, and it provides a one-time **Convert** action that mathematically rewrites every monetary field in the store at the fixed rate and flips the site currency from BGN to EUR.

The Convert action is the **only** safe way to perform a real currency change in CloudCart. Once run, the store is in EUR and **cannot be reverted** — the operation is sticky.

For non-Bulgarian merchants, the equivalent operation has **no built-in tool**. The closest path is: export the catalog, recompute prices in a spreadsheet, re-import via the XML/CSV sync apps, then change the currency setting. This is slow and risky — most non-Bulgarian merchants stick with the currency they launched in.

## Scope

Covered:

- The dual-display rendering at the fixed `1.95583` rate.
- The customer-facing banner placement options.
- The full catalogue of monetary fields rewritten by the Convert action.
- What the Convert action explicitly does NOT touch (orders, percentage taxes, multilang sister prices).
- Sticky / non-reversible nature of the Convert.
- Post-Convert side effects (storefront cache, search index, maintenance mode).

Not covered here:

- The store-wide currency setting itself — see [[multi-currency-store-currency-model]].
- Numeric storage without currency tag — see [[multi-currency-price-storage]].
- Why historical orders keep their original currency — see [[multi-currency-order-snapshot]].
- Fixer.io rates for non-fixed currency pairs — see [[multi-currency-fx-rates]].
- Provider-side currency configuration flipped by Convert — see [[multi-currency-payment-providers]].

## Contrasts

- **Dual-display vs. true conversion** — dual-display is a **presentational overlay**: both BGN and EUR are rendered, but the underlying price is still stored in ONE currency. The Convert action is the actual conversion: every numeric value is rewritten.
- **Convert vs. naive currency change** — the Convert action divides every price by 1.95583. A naive currency change in [[settings-general]] (without Convert) is a label flip — see [[multi-currency-price-storage]].
- **First-party dual-display vs. third-party switcher** — [[apps-bgn2eur]] is the only first-party dual-display path. True multi-currency switchers (USD / EUR / GBP per customer choice) are custom theme development — see [[multi-currency-store-currency-model]].
- **Bulgarian Convert vs. non-Bulgarian currency change** — Bulgaria gets a built-in atomic tool because the rate is fixed by law. Other currency changes have no platform tool because there is no canonical rate.

## Where it applies

### The dual-display app

[[apps-bgn2eur]] renders prices in BOTH BGN and EUR side-by-side in a configurable display mode:

- **Storefront** — both currencies render on product pages, category pages, cart, and checkout.
- **Admin panel** — both currencies render in the admin order detail page, the product editor, and other admin price surfaces.
- **Both** — the most common configuration during the transition window.

A customer-facing banner with the default message *"1 EUR = 1.95583 BGN"* (editable) renders at three configurable positions: checkout, cart, footer. See [[apps-bgn2eur-settings]] for the display-mode and message-position toggles.

The dual-display does NOT let the customer pick a currency — both are always shown. This is the only first-party dual-currency rendering shipped by CloudCart.

### The one-time Convert action

The Convert action mathematically rewrites every monetary field in the store at the fixed `1 EUR = 1.95583 BGN` rate (divides each BGN price by 1.95583 to produce the EUR price), then flips the site currency from BGN to EUR. The action:

- Puts the store into **maintenance mode** for the duration of the conversion.
- Sweeps every monetary field listed below in a single atomic operation.
- Flips the `currency` setting from `BGN` to `EUR`.
- Exits maintenance mode on completion.
- **Cannot be reverted** — once run, the store is in EUR permanently.

### Fields rewritten by Convert

- **Product variants** — `price` and `delivery_price` on every Variant.
- **Products** — `price_from` / `price_to` recomputed from variants.
- **Discounts** — flat-amount discounts, fixed-price discounts, shipping discounts.
- **Discount codes** — code-level price targets.
- **Code-Pro** — per-code targets across the Code Pro module.
- **Quantity discounts** — step prices on each tier.
- **Cart Rules** — action prices and trigger-condition price thresholds.
- **Smart collections** — price-range conditions on filter rules.
- **Bundles** — bundle prices.
- **Cross-sells** — action prices and target product prices.
- **Form fields** — add-on prices configured on customer-facing forms.
- **Shipping rates** — every numeric rate on every shipping method.
- **Flat taxes** — flat money amounts configured as tax lines (percentage taxes are unchanged — see [[multi-currency-taxes-analytics]]).
- **Payment-provider fees** — and the provider's configured currency code (BGN → EUR per provider) — see [[multi-currency-payment-providers]].

### What Convert does NOT touch

- **Orders** — `orders.currency` and `price_total` remain in BGN for any order placed before the Convert. See [[multi-currency-order-snapshot]].
- **Percentage taxes** — a `20%` VAT line continues to apply to the new currency directly; no edit needed. See [[multi-currency-taxes-analytics]].
- **Multilang sister sites** — Convert affects only the master store. Sister sites carrying their own currency setting and `price_change` multiplier are not swept; the merchant must run Convert per sister or manage them separately.
- **Customer wallets / store credit** balances tied to historical BGN values (verify) — confirm before assuming Convert touches loyalty / credit balances.

### Post-Convert side effects

- **Storefront cache** is flushed; the next storefront request renders EUR prices.
- **Storefront JavaScript data file** is regenerated.
- **Search-engine index** (the search engine / the search index / etc.) is regenerated where it carries price data; pages that display prices render EUR on the next request.
- **`product.updated` webhook** fires on every affected product as part of the sweep — see [[settings-hooks]]. Receivers must be idempotent.
- **Maintenance mode** is exited once the conversion completes.

### Non-Bulgarian merchants and currency change

For merchants on any other currency change (e.g., a Romanian store moving from RON to EUR), there is no equivalent built-in tool. The closest path:

1. Export the catalog (products, variants, discounts, shipping rates).
2. Recompute prices in a spreadsheet at the merchant's chosen rate.
3. Re-import via the XML/CSV sync apps.
4. Manually re-enter flat taxes and payment-provider fees.
5. Change the currency in [[settings-general]].

This is slow and risky. Most non-Bulgarian merchants stick with the currency they launched in.

## Related

- [[multi-currency]] — hub.
- [[multi-currency-store-currency-model]] — why a naive currency change is a label flip and Convert is needed.
- [[multi-currency-price-storage]] — the storage model that makes a single atomic Convert possible.
- [[multi-currency-order-snapshot]] — Convert does not touch order tables.
- [[multi-currency-taxes-analytics]] — percentage VAT is untouched; flat taxes ARE swept.
- [[multi-currency-payment-providers]] — Convert flips provider-configured currency codes.
- [[apps-bgn2eur]] — the dual-display app and Convert action.
- [[apps-bgn2eur-settings]] — display-mode and message-position toggles.
- [[settings-general]] — `currency` setting flipped by Convert.

## Open Questions

- ⏸️ Confirm whether customer wallets / store-credit balances are swept by the Convert action or left at their BGN numeric value. (verify)
