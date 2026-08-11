---
type: concept
nav_path: "Concept → Multi-currency → Order currency snapshot"
aliases: ["Order currency snapshot", "Frozen order currency", "Order currency at creation", "Refund currency", "Mixed-currency history", "Замразена валута на поръчка"]
tags: [finance, currency, orders, refunds, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[multi-currency]]. See the hub for the other aspects (store currency model, price storage, FX rates, BGN → EUR transition, payment providers, taxes & analytics).

# Multi-currency — order currency snapshot

## Definition

When an order is created, the platform captures the store's current currency into the order's `currency` field. From that moment, the order's currency is **frozen**. Subsequent edits to the store currency setting do NOT propagate to past orders. The order detail page, the invoice, the refund flow, the order-level totals, and the order's exported records all use the snapshot — not the live `site('currency')`.

This is what produces a **mixed-currency order history** for any store that goes through a real currency change. After a Bulgarian merchant runs the BGN → EUR Convert action, the order list shows BGN orders before the cutover and EUR orders after, with no automatic recomputation of historical totals.

The platform does NOT support **cross-currency refunds** out of the box. A refund on an order placed in BGN is processed in BGN; a refund on an order in EUR is in EUR. The payment provider's own refund-currency rules (Stripe, Borica, Adyen, etc.) gate this further — most providers require the refund to be in the same currency as the original capture.

## Scope

Covered:

- Where and when the order currency snapshot is taken.
- Every order-level surface that reads the snapshot (detail page, invoice, refund, exports).
- Mixed-currency order history after a real currency change.
- Refund currency rules and the payment-provider gate.

Not covered here:

- The store-wide currency setting itself — see [[multi-currency-store-currency-model]].
- The price-storage model behind the numeric snapshot — see [[multi-currency-price-storage]].
- The Convert action and which tables it does / does NOT touch — see [[multi-currency-bgn-eur-transition]].
- Mixed-currency analytics consolidation — see [[multi-currency-taxes-analytics]].
- Per-provider refund currency support — see [[multi-currency-payment-providers]].

## Contrasts

- **Order `currency` vs. site `currency`** — `orders.currency` is per-order and frozen at creation; `site('currency')` is store-wide and mutable. The two can diverge for any historical order after a currency change.
- **Order `currency` vs. payment-provider settled currency** — the order is in its frozen currency; the provider may have settled the actual payment in a different currency (e.g., the bank's processing currency). The platform stores the order's nominal currency; the provider's settlement is its own concern. See [[multi-currency-payment-providers]].
- **Refund in original currency vs. cross-currency refund** — CloudCart only supports refunds in the order's frozen currency. Cross-currency refunds (e.g., a RON-priced order originally captured in EUR) are not a platform feature; they depend entirely on the provider's API.

## Where it applies

### Snapshot at creation

When an order is created (storefront submit, admin manual creation, JSON-API v2 creation), the platform sets `orders.currency = site('currency')` at that moment. The numeric totals on the order (`price_total`, `price_subtotal`, etc.) are likewise captured against the implicit unit of the current site currency — see [[multi-currency-price-storage]] for why none of those fields carries its own tag.

From that point on, the order's totals and the order's `currency` are paired and immutable.

### Surfaces that read the snapshot

- **Order detail page** ([[orders-details]]) — displays totals in the order's `currency`, not the current site currency. Look at an old BGN order on an EUR store and you see BGN totals.
- **Invoices** generated from the order — use the order's `currency`.
- **Order-list export** ([[orders]]) — currency column reflects the per-order snapshot, allowing the merchant to filter or sort by currency.
- **`price_total_formatted` accessor** — formats with the order's `currency` symbol and locale separator.
- **Refund and partial-refund flows** — read the order's `currency` for the refund amount.
- **Order edits** ([[orders-details]]) — adding line items, changing quantities, applying additional discounts on a historical order — all stay in the order's original currency.

The Convert action on [[apps-bgn2eur]] explicitly does NOT touch order tables. After Convert, a BGN-placed order keeps BGN totals forever.

### Mixed-currency order history

For any store that goes through a real currency change, the order history splits at the cutover:

- Orders placed BEFORE the change carry the old currency.
- Orders placed AFTER the change carry the new currency.

The order list does NOT auto-recompute historical totals into the new currency. Analytics dashboards ([[analytics-pipeline]], [[analytics-total-orders]]) report revenue per the order's snapshot, producing two separate revenue streams visible in the merchant admin. Consolidation requires manual export — see [[multi-currency-taxes-analytics]].

### Refund-currency rules

The platform does not support cross-currency refunds. A refund on a BGN order is processed in BGN; on a EUR order, in EUR. Beyond the platform itself, the payment provider gates the refund:

- **Stripe** — refunds must be in the original capture currency.
- **Borica** — refunds in the original capture currency.
- **Adyen** — same constraint by default; multi-currency-capable accounts may differ.
- **iCard, ePay, Paynetics, Wallet** — refunds in the original capture currency.
- **PayPal** — broader currency support, but each merchant's PayPal account configuration determines what works.

The merchant should always confirm refund-currency support with the provider before assuming a cross-currency refund will work. The CloudCart admin does NOT validate this before initiating the refund — the request will simply fail at the gateway if the provider rejects it.

### Historical orders after the BGN → EUR Convert

A Bulgarian merchant running the Convert action on [[apps-bgn2eur]] ends with:

- All prospective monetary fields (products, variants, discounts, shipping, payment fees, etc.) rewritten to EUR at 1 / 1.95583.
- All historical orders **untouched** — they remain in BGN.
- New orders captured in EUR.

Support tickets about "why does my old order show BGN totals after the EUR cutover" map directly to this frozen-snapshot rule. The merchant cannot retroactively convert old orders without exporting and processing them externally.

## Related

- [[multi-currency]] — hub.
- [[multi-currency-price-storage]] — why the numeric totals on a historical order are static.
- [[multi-currency-bgn-eur-transition]] — Convert action; explicitly does NOT touch order tables.
- [[multi-currency-payment-providers]] — provider-side refund-currency rules.
- [[multi-currency-taxes-analytics]] — mixed-currency revenue streams in analytics.
- [[order]] — Order entity carrying the frozen `currency` field.
- [[orders-details]] — order detail page that reads the snapshot.
- [[orders-payment-refund]] — refund flow that uses the order's `currency`.

## Open Questions

None.
