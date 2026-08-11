---
type: concept
nav_path: "Concept → Multi-currency → FX rates"
aliases: ["FX rates", "Exchange rates", "Fixer.io sync", "currency_sync job", "Internal currency conversion", "12-hour FX sync", "Курсове на валути"]
tags: [finance, currency, fx, fixer, background-jobs, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[multi-currency]]. See the hub for the other aspects (store currency model, price storage, order snapshot, BGN → EUR transition, payment providers, taxes & analytics).

# Multi-currency — FX rates

## Definition

CloudCart syncs current FX rates from **Fixer.io** via a background job that runs **every 12 hours** (interval 43 200 s, single-flighted on the `cc-system7` queue). The synced rates live in an internal `currencies` table and are **not** exposed in the admin panel for editing. Merchants do not see a "today's FX rate" module anywhere in the platform.

The platform uses these synced rates for **internal conversions only**:

- **Shipping-courier API requests** — when a courier's billing currency differs from the order's currency, the platform converts at request-build time (e.g. a RON store shipping via a courier that bills in EUR has its COD / insurance / parcel amounts converted to EUR).
- **CloudCart-side platform analytics** — visible to CloudCart staff, not the merchant, for per-store revenue consolidation in a common reporting currency.
- **Plan billing** — the merchant's CloudCart subscription is billed in a fixed currency (typically EUR) regardless of the storefront currency.

The **one fixed rate** exposed anywhere in the merchant-facing platform is `1 EUR = 1.95583 BGN`, hardcoded in [[apps-bgn2eur]] per Bulgarian central-bank law. That rate is independent of the Fixer.io feed.

## Scope

Covered:

- The Fixer.io sync mechanism: every 12 hours, single-flighted on the `cc-system7` queue.
- Where the platform uses the synced rates internally.
- Why merchants don't see a "today's rate" module and can't edit the rates.
- The hardcoded `1 EUR = 1.95583 BGN` rate exception (Bulgarian law).

Not covered here:

- The store currency setting itself — see [[multi-currency-store-currency-model]].
- The BGN → EUR fixed-rate Convert action — see [[multi-currency-bgn-eur-transition]].
- Order currency freezing — see [[multi-currency-order-snapshot]].
- Per-provider supported currencies — see [[multi-currency-payment-providers]].

## Contrasts

- **Fixer.io market rates vs. fixed BGN ↔ EUR rate** — Fixer.io feeds a market rate for every currency pair, refreshed every 12 hours. The BGN ↔ EUR rate used by [[apps-bgn2eur]] is the **fixed** `1 EUR = 1.95583 BGN` rate set by Bulgarian central-bank law and is independent of the Fixer.io feed.
- **Internal-only FX vs. merchant-editable FX** — synced rates are NOT exposed in any admin screen. Merchants cannot override them, see them, or be notified of large swings.
- **Live FX at request-build time vs. snapshotted FX** — courier API requests convert at the moment of the request using the latest synced rate. Order totals are never converted; the order's `currency` is frozen — see [[multi-currency-order-snapshot]].
- **Plan billing currency vs. store currency** — the merchant's CloudCart subscription is billed in a fixed currency (typically EUR or USD per region). A Romanian store in RON still pays its CloudCart subscription per the billing setup, not in RON.

## Where it applies

### The 12-hour sync

The `currency_sync` background job pulls rates from Fixer.io into the internal `currencies` table. The job:

- Runs every 12 hours (interval `43200` seconds).
- Is single-flighted on the `cc-system7` queue (one instance at a time, no overlap).
- Is invisible to the merchant — no UI surface, no log entry in any merchant-facing screen.

If Fixer.io is unavailable, the previous synced values continue to be used. There is no merchant-facing alert when the sync fails.

### Where the synced rates are read

**Shipping-courier API requests**

When a courier expects amounts in its billing currency and the store currency differs, the platform converts at request-build time. Examples:

- **[[apps-dpdbulgaria-speedy|DPD Bulgaria (Speedy)]]** — its quote and label-creation endpoints bill in **EUR** (the Bulgarian base currency). A store whose currency differs — e.g. a Romanian store in RON — has the COD amount, insurance value, and parcel subtotal converted to EUR using the latest synced rate before the request is sent.
- **[[apps-econt]]** — same pattern; the Bulgarian couriers bill in **EUR**.
- **[[apps-cargus]]** — Romanian courier; expects RON. Stores in other currencies convert at request build.

The conversion only affects the request payload sent to the courier. The order's stored `currency` and `price_total` remain in the store currency frozen at order creation — see [[multi-currency-order-snapshot]]. The courier's tracking and billing on their side use the converted-to-billing-currency amounts.

**CloudCart-side platform analytics**

CloudCart's internal analytics aggregate per-store revenue into a common reporting currency (typically EUR). The merchant does not see this layer; it is internal to CloudCart's operations. The conversion uses the same synced `currencies` table.

**Plan billing**

The merchant's [[plans|CloudCart subscription plan]] is billed in a fixed billing currency regardless of the storefront's currency. When the store charges customers in RON but the subscription is billed in EUR, CloudCart's billing layer converts at the time of charge using the synced rate. The merchant sees the invoice for the subscription in the billing currency — not in the store currency.

### Why merchants don't see the rate

The Fixer.io feed is a CloudCart operational concern, not a merchant-facing setting. Three reasons:

1. The platform does not let merchants edit prices via FX (no automatic re-pricing path other than the BGN → EUR Convert). Showing the rate would imply such a feature exists.
2. The rate is used only for internal pipelines (couriers, plan billing, internal analytics) — none of which the merchant configures.
3. The one rate the merchant DOES care about — `1 EUR = 1.95583 BGN` — is fixed by law and exposed in [[apps-bgn2eur]] only.

### The fixed BGN ↔ EUR rate exception

The BGN ↔ EUR rate is set by Bulgarian central-bank law and is independent of the Fixer.io feed. [[apps-bgn2eur]] uses `1 EUR = 1.95583 BGN` for all dual-display rendering and for the one-time Convert action. The Fixer.io sync never overwrites this rate, and the merchant cannot edit it.

## Related

- [[multi-currency]] — hub.
- [[multi-currency-bgn-eur-transition]] — the fixed-rate Convert action; uses the hardcoded rate, not the Fixer.io feed.
- [[multi-currency-order-snapshot]] — order `currency` is frozen; courier API conversion does not propagate back.
- [[shipping-calculation]] — courier API requests convert amounts at request-build time.
- [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-econt]] / [[apps-cargus]] — couriers requiring currency conversion for their API.
- [[plans]] — CloudCart subscription billed in a fixed currency.

## Open Questions

None.
