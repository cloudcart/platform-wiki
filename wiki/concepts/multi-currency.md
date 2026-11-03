---
type: concept
aliases: ["Multi-currency", "Multi-currency pricing", "Store currency", "Currency handling", "FX rates", "Exchange rates", "Валута на магазина", "Множество валути"]
tags: [finance, currency, store-currency, fx, bgn-eur, concepts]
created: 2026-05-21
updated: 2026-06-10
source_count: 3
---

# Multi-currency pricing

## Definition

CloudCart stores are **single-currency by design**: every store has one **base currency** chosen in [[settings-general]] → *Currency and units*, and all prices for products, variants, discounts, shipping rates, taxes, payment fees, bundles, cross-sells, form fields, and quantity discounts are stored in that one currency. There is **no** per-product or per-variant currency override, and **no** built-in customer-facing currency picker on the storefront.

When the merchant needs the storefront to display two currencies side-by-side — the dominant case being Bulgaria's 2026 BGN → EUR transition — they install [[apps-bgn2eur]], which adds a second rendering of every price at a **fixed conversion rate**. This is the only first-party multi-currency display path on the platform.

Multi-currency comes up implicitly in **shipping-courier API calls** (the platform converts to the courier's billing currency at request time using internally-synced FX rates) and **internal CloudCart billing** (the merchant's subscription is billed in a fixed currency independent of the store currency). FX rates for these internal conversions come from **Fixer.io** synced every 12 hours and are NOT exposed to the merchant.

The only Bulgaria-specific path through a real currency change is the **one-way Convert** action on [[apps-bgn2eur]], which mathematically rewrites every monetary field at the fixed `1 EUR = 1.95583 BGN` rate. Non-Bulgarian merchants have no equivalent built-in tool.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[multi-currency-store-currency-model]] — where the merchant picks the store currency, what changes / does NOT change on edit, the missing in-app warning for existing orders, why there is no customer-facing currency switcher.
- [[multi-currency-price-storage]] — how monetary fields are stored without a currency tag, the derived `currency_code` accessor, why a naive currency change is a label-flip not a re-price.
- [[multi-currency-order-snapshot]] — order `currency` frozen at creation, refunds and invoices in the original currency, mixed-currency order history after a Convert.
- [[multi-currency-fx-rates]] — Fixer.io 12-hour sync, internal-only uses (courier APIs, plan billing, platform analytics), why merchants don't see a "today's FX rate" module.
- [[multi-currency-bgn-eur-transition]] — Bulgaria's fixed-rate dual-display app, the full field catalogue rewritten by the Convert action, what orders / sister sites are NOT touched.
- [[multi-currency-payment-providers]] — currency-specific providers (BGN-only vs multi-currency), the absence of admin-side validation, how the Convert action flips provider configured currency.
- [[multi-currency-taxes-analytics]] — percentage VAT is currency-agnostic, flat taxes need re-entry, mixed-currency analytics not consolidated, COD caps that depend on the BG store currency.

## Why it matters to the merchant

Multi-currency is one of the few platform topics where the **wrong mental model** silently corrupts pricing. Six high-impact consequences:

- **Changing the currency setting does NOT re-price products.** A `19.99` EUR product becomes a `19.99` USD product — almost never what the merchant intends. (The one currency change that *is* re-priced is the fixed-rate BGN → EUR Convert, line below.) See [[multi-currency-store-currency-model]] + [[multi-currency-price-storage]].
- **The BGN → EUR Convert action is the only safe path** through a real currency change, and only for Bulgarian merchants. It is sticky — once run, no revert. See [[multi-currency-bgn-eur-transition]].
- **Orders freeze the currency they were placed in.** Historical orders are never re-priced; analytics shows mixed-currency revenue streams after a Convert. See [[multi-currency-order-snapshot]] + [[multi-currency-taxes-analytics]].
- **Payment providers are currency-specific**, and CloudCart does NOT validate the pairing on save. A single-currency provider (e.g. a USD-only gateway) enabled on an EUR store fails at the gateway, not in the admin. See [[multi-currency-payment-providers]].
- **No customer-facing currency switcher** ships with the platform. Per-market pricing is approximated through [[apps-multilang]] sister sites, not through a runtime switcher. See [[multi-currency-store-currency-model]].
- **FX rates are NOT merchant-editable.** They sync from Fixer.io every 12 hours and only serve internal conversions (shipping APIs, plan billing). See [[multi-currency-fx-rates]].

## Scope

What this concept covers (across the 7 sub-pages):

- The single-store-currency model and where the store currency is defined.
- How monetary fields are stored and rendered.
- The per-order currency snapshot.
- FX-rate sourcing and where the platform uses currency conversion internally.
- The fixed-rate BGN ↔ EUR transition path.
- Currency-specific payment-provider pairing.
- Tax computation, analytics, and COD-cap behaviour under mixed currencies.

What it does NOT cover:

- A customer-facing currency switcher module on the storefront — CloudCart does not ship one. Custom JS overlays using a third-party FX API are theme work and out of scope.
- Per-product or per-variant currency override fields — they do not exist.
- A merchant-editable FX rate table (other than the fixed BGN ↔ EUR rate, which is hardcoded by Bulgarian law).
- Cross-sister currency reconciliation — when a merchant runs an EUR sister and a UK sister in GBP via [[apps-multilang]], Multilang transforms copied prices at sync-time using a merchant-defined multiplier (not a market FX rate). See [[apps-multilang]].
- Daily settlement / accounting reconciliation across currencies — that's accounting-app territory ([[apps-szamlazz]], FGO, Smart Bill).
- Refunds in a different currency than the order's original currency — the platform does not support cross-currency refunds out of the box.

## Contrasts

- **Multi-currency vs. multi-language** — storefront language ([[multi-language]]) is per-locale and per-customer; currency is per-store and per-order. Changing the store currency does NOT retranslate or re-price existing orders.
- **Multi-currency vs. dual-currency display** — the BGN → EUR app is a **presentational overlay** at a fixed rate, not a market-rate converter. Underlying prices stay in ONE currency. See [[multi-currency-bgn-eur-transition]].
- **Store currency vs. CloudCart subscription billing** — the merchant's plan is billed in a fixed billing currency (typically EUR) regardless of storefront currency. See [[plans]] and [[multi-currency-fx-rates]].
- **Order currency vs. shipping-quote currency** — the order `currency` is frozen; the courier may need amounts in a different currency for its API, converted at request-build time. See [[multi-currency-fx-rates]].
- **Currency change vs. price re-entry** — the platform does NOT re-price products on a currency-setting edit. The correct path for a real currency change is the BGN → EUR Convert action. See [[multi-currency-store-currency-model]] + [[multi-currency-bgn-eur-transition]].
- **Per-market pricing via Multilang sisters vs runtime switcher** — CloudCart approximates per-market pricing through sister sites with their own currency setting and `price_change` multiplier, NOT through a runtime customer-facing switcher.

## Where it applies

- [[settings-general]] — where the merchant picks the store currency.
- [[apps-bgn2eur]] — Bulgarian BGN → EUR dual-display app and the one-time Convert action.
- [[apps-bgn2eur-settings]] — settings sub-page for dual-display mode and message position.
- [[order]] / [[orders-details]] — order currency snapshotted from the site currency at creation.
- [[product]] / [[products-variants-options]] — product and variant prices stored in the store's base currency.
- [[settings-payment-providers]] — payment providers are currency-specific; matching the store currency is the merchant's responsibility.
- [[settings-taxes]] / [[tax-computation]] — percentage VAT applies to any currency; flat tax amounts must be re-entered on a real currency change.
- [[shipping-calculation]] — courier API requests convert amounts at request-build time.
- [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-econt]] / [[apps-cargus]] — couriers requiring currency conversion for their API.
- [[plans]] — CloudCart subscription billed in a fixed currency, independent of store currency.
- [[multi-language]] — sister concept; language and currency are independent settings.

## Related

- [[settings-general]]
- [[apps-bgn2eur]]
- [[apps-bgn2eur-settings]]
- [[order]]
- [[product]]
- [[tax-computation]]
- [[shipping-calculation]]
- [[multi-language]]
- [[apps-multilang]]
- [[apps-dpdbulgaria-speedy|Speedy]]
- [[apps-econt]]
- [[settings-payment-providers]]
- [[plans]]

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages.
