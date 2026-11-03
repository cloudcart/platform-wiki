---
type: concept
nav_path: "Concept → Multi-currency → Taxes & analytics"
aliases: ["Multi-currency taxes", "Percentage VAT currency-agnostic", "Flat tax re-entry", "Mixed-currency analytics", "COD cap BGN", "Cache flush on currency change"]
tags: [finance, currency, taxes, analytics, cod, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[multi-currency]]. See the hub for the other aspects (store currency model, price storage, order snapshot, FX rates, BGN → EUR transition, payment providers).

# Multi-currency — taxes & analytics

## Definition

Tax and analytics behave **asymmetrically** under a currency change:

- **Percentage VAT** rates (e.g., 20%) are **currency-agnostic** — they apply to whichever currency the underlying price is stored in. A 20% rate on a 100 EUR product gives 20 EUR VAT; the same rate on a 100 USD product gives 20 USD VAT. A currency change requires NO tax-rate edit.
- **Flat tax amounts** (where the merchant configured a fixed money amount as a tax line, not a percentage) DO need to change with the currency. The BGN → EUR Convert action handles this automatically; non-Bulgarian merchants must re-enter manually.

The platform's analytics dashboards report revenue in the **order's** frozen currency. For a store run in mixed currencies (e.g., BGN before Convert, EUR after), the analytics layer does NOT consolidate them — the merchant sees two separate revenue streams.

A few platform behaviours depend on the **literal store-currency string** rather than on amounts in general — most notably the Bulgarian-courier cash-on-delivery cap (`BG_MAX_COD = 10000`), which the code applies **only when `site('currency') == 'BGN'`. A store on EUR — the new Bulgarian norm after the euro switch — gets NO platform COD cap** (the "unlimited" sentinel; only the carrier's own server-side limit applies), because the cap condition still keys on the legacy `BGN` string. Also currency-string-dependent: the storefront / search-engine cache invalidation triggered by every currency change.

## Scope

Covered:

- Percentage VAT vs. flat tax amounts under a currency change.
- Mixed-currency analytics behaviour and consolidation options.
- COD amount caps tied to specific currency strings.
- Cache and search-index regeneration on currency change.

Not covered here:

- The Convert action's full field catalogue (including flat taxes) — see [[multi-currency-bgn-eur-transition]].
- Frozen order currency — see [[multi-currency-order-snapshot]].
- Refund-currency rules per provider — see [[multi-currency-payment-providers]].
- The store currency setting itself — see [[multi-currency-store-currency-model]].

## Contrasts

- **Percentage VAT vs. flat tax amounts** — percentage rates don't care about currency; flat amounts do. A currency change requires NO percentage VAT edits, but every flat tax must be re-entered (or swept by the BGN → EUR Convert for Bulgarian merchants).
- **Order-currency analytics vs. consolidated analytics** — CloudCart's dashboards report per the order's frozen `currency`. Mixed-currency stores see split revenue streams; consolidation requires manual export or an accounting-app integration.
- **Currency-agnostic platform behaviour vs. currency-string-dependent behaviour** — most platform logic doesn't care which currency. Specific exceptions (BGN COD cap, BGN → EUR Convert eligibility) check the currency string.

## Where it applies

### Percentage VAT — currency-agnostic

Percentage VAT rates configured in [[settings-taxes]] apply to whichever currency the underlying price is stored in. The same `20%` rate that gave 20 BGN VAT on a 100 BGN product before a currency change gives 20 EUR VAT on a 100 EUR product after. No edit is needed; the rate is a pure ratio.

This is one of the reasons the BGN → EUR Convert can sweep monetary fields cleanly: percentage taxes don't need touching, only the underlying prices do. See [[tax-computation]] for the full mechanics of tax rules.

### Flat tax amounts — re-entry required

If the merchant configured a flat money amount as a tax line (rather than a percentage), the amount IS currency-bound. A 5 BGN flat tax has to become a 2.56 EUR flat tax after a real currency change. The Convert action on [[apps-bgn2eur]] handles this for Bulgarian merchants automatically — see [[multi-currency-bgn-eur-transition]].

For non-Bulgarian merchants changing currency, flat taxes are NOT auto-converted and must be manually re-entered in [[settings-taxes]]. Missing this step is a common bug source: the merchant sees correct percentage tax but wrong flat tax after the change.

### Mixed-currency analytics

Analytics dashboards ([[analytics-pipeline]], [[analytics-total-orders]], [[analytics-full]], [[analytics-more-details]], [[analytics-customer-value]]) report revenue in the order's frozen `currency` — see [[multi-currency-order-snapshot]]. For a store that's run in mixed currencies, the analytics layer presents two separate streams.

Consolidation options for the merchant:

1. **Export the order history (CSV)** and consolidate in a spreadsheet at a chosen rate.
2. **Use an accounting-app integration** ([[apps-szamlazz]], FGO, Smart Bill) that may consolidate at the accounting layer.

CloudCart itself does NOT generate a "convert all historical orders to EUR" report. The mixed-currency display is a permanent visual feature of any mid-life-changed store's analytics.

### COD amount cap is currency-specific

Bulgarian couriers (Econt, Speedy) enforce a **10 000 BGN cap** on cash-on-delivery amounts when the store is in BGN. The cap is checked against the BGN currency string specifically. For non-BGN stores (including a Bulgarian store post-Convert in EUR), the platform does NOT enforce a cap — the courier's own server-side limits apply (which may differ from the BGN cap by their own rules).

This is one of the few places where platform behaviour depends on the specific currency string rather than on amounts. See [[apps-econt]] and [[apps-dpdbulgaria-speedy|Speedy]] for the cap details. Support tickets about "the COD limit changed unexpectedly" after a currency change usually trace back to this rule.

### Cache and search-index regeneration on currency change

Both changing the currency in [[settings-general]] AND running the BGN → EUR Convert action flush the storefront cache and regenerate the storefront's JavaScript data file. The merchant does not need to manually clear caches; the next storefront request shows the new currency immediately.

The search-engine index (the search engine / the search index / etc.) is regenerated during the BGN → EUR Convert flow because Convert rewrites prices. A simple currency-setting change in [[settings-general]] does not rebuild the search index (most engines don't carry price data), but any search-result page that displays prices renders them with the new currency on next request.

### Practical guidance after a real currency change

After a real currency change (whether by Convert or by manual catalog re-import):

- **No edits needed** for percentage VAT.
- **Re-check flat taxes** — Convert sweeps them; manual currency change does NOT.
- **Re-check per-provider configured currency code** — see [[multi-currency-payment-providers]].
- **Expect mixed-currency analytics forever** — historical orders are frozen; see [[multi-currency-order-snapshot]].
- **Expect COD-cap behaviour to flip** — a BGN store moving to EUR loses the in-platform BGN cap; courier-side limits take over.

## Related

- [[multi-currency]] — hub.
- [[multi-currency-order-snapshot]] — order-currency snapshot driving the mixed-currency analytics behaviour.
- [[multi-currency-bgn-eur-transition]] — Convert action that sweeps flat taxes.
- [[multi-currency-payment-providers]] — per-provider configuration to recheck.
- [[tax-computation]] — full mechanics of tax rules.
- [[settings-taxes]] — where tax rates and flat taxes are configured.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] — 10 000 BGN COD cap details.
- [[analytics-pipeline]] / [[analytics-total-orders]] / [[analytics-full]] — analytics dashboards reading order-frozen currency.

## Open Questions

None.
