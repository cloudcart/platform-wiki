---
type: feature
nav_path: "Sidebar → Services → Billing cycles & VAT"
route_name: admin.services.list
route_path: /admin/services
aliases: ["Services billing cycles", "Service billing period", "Services VAT", "Service currency", "Recurring services"]
tags: [services, billing, subscriptions, vat, currency]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[services]]. See the hub for related aspects (catalog, purchase flow, routes, catalog controls, known gaps).

# Services — billing cycles, currency display, and VAT

## Purpose

This page covers **how often a service is charged** (`billing_cycle`), **what currency the merchant sees vs. what currency the invoice uses**, and **how VAT is added at invoice time** (per the merchant's billing country). These three rules are easy to confuse because the catalog row shows ONE figure but the merchant's card is charged a DIFFERENT figure (different currency and / or with VAT added).

## Where to find it

Billing-cycle labels and the without-VAT price appear on:

- The catalog rows on [[services-catalog]] (`/admin/services`) — price + `/ <billing_period>` suffix.
- The purchase confirmation step on [[services-purchase-flow]] (`/admin/services/purchase`) — same without-VAT figure.

The actual VAT-inclusive figure appears only on the invoice PDF emailed after Pay Now succeeds.

## What the merchant can do here

Nothing directly — billing cycle and currency are properties of the catalog row, set by CloudCart's commercial team (see [[services-catalog-controls]]). The merchant's only action is choosing whether to tick a service whose billing cycle matches their intent (one-off vs recurring).

## Settings & fields

### Billing periods (`billing_cycle` integer)

| `billing_cycle` | Displayed label | Behaviour |
|-----------------|-----------------|-----------|
| `null` | `once` | Paid for once, no recurring charge. Typical for migration jobs, one-off design work, hosting setup. Does NOT become a recurring [[subscriptions]] row. |
| `1` | `month` | Charged once at purchase, then renewed monthly on the same calendar day until cancelled. Joins [[subscriptions]]. |
| `12` | `year` | Charged once at purchase, then annually. Joins [[subscriptions]]. |
| `24` | `2years` | Charged once at purchase, then every 2 years. Joins [[subscriptions]]. |
| Other values | "every N months" (generic) | Rendered as a generic interval text `(verify)`. |

A merchant ticking a recurring service is starting a **new subscription on top of their existing ones**. The new subscription appears alongside the merchant's plan and other recurring items on [[subscriptions]], with its own next-billing date, renewal amount, and Cancel control.

### Source-currency vs displayed-currency

Each catalog row has a base `currency` (typically `EUR` in CloudCart's current setup) and a `price` (integer, in source-currency cents). The catalog and purchase-confirmation pages display the figure **converted to the merchant's currency** for browsing convenience, using CloudCart's internal currency-conversion table.

**However:**

- The invoice CloudCart issues uses the **service's source currency** for the amount.
- VAT is then added per the merchant's billing-country VAT rate from [[billing-invoicing]].

If a merchant's currency does not match the service's currency, the figure on the catalog page is a **guide**; the figure on the actual invoice / card charge may differ by the exchange-rate margin. The page does not show a disclaimer about this — see [[services-known-gaps]].

## Business rules

### Recurring services join `[[subscriptions]]`; one-offs don't

A service with `billing_cycle = 1` / `12` / `24` becomes a recurring `SiteSubscription` after Pay Now — it appears in [[subscriptions]] with its next-billing date and a Cancel control. The merchant can cancel future renewals there.

A service with `billing_cycle = null` (one-off) creates a single `SiteSubscription` record at Pay Now time (mode = `create`), but does NOT recur. The invoice is issued, the card is charged once, and the service is considered "delivered" once paid. There is NO in-app Cancel UI for a one-off after Pay Now — refunds / cancellations require CloudCart support (see [[services-known-gaps]]).

### VAT is computed and added at INVOICE time, NOT shown on catalog

Both the catalog and the purchase confirmation display the figure **WITHOUT VAT**. The catalog footer says *"All prices are without VAT"* (`payment.no_vat`). VAT is computed and added at INVOICE time downstream based on the merchant's billing country saved in [[billing-invoicing]]:

| Merchant billing country | VAT applied on invoice |
|--------------------------|------------------------|
| **Bulgaria** | Local VAT (20 %) is added. |
| **EU with VIES-valid VAT ID (B2B)** | Reverse-charge; NO VAT added (the merchant's own VAT return handles it). |
| **EU without VAT ID (B2C)** | Local VAT of the merchant's country is added (per EU place-of-supply rules). |
| **Outside EU** | NO VAT added. |

The actual figure charged to the card is the final invoice total (with VAT applied per the above rule). The merchant should always look at the resulting invoice email — that is the authoritative VAT-inclusive amount.

### One-off vs recurring — same Pay Now button

The same Pay Now button at the end of [[services-purchase-flow]] works for both one-off and recurring services. For a one-off, it charges the card once. For a recurring service, it charges immediately AND configures automatic renewals; future charges happen on the same calendar day each billing cycle.

### Recurring service cancellation goes through `[[subscriptions]]`

Recurring services are cancelled by the merchant via [[subscriptions]] — picking the service row and clicking Cancel stops future billings. The most recent charge is NOT refunded by that action — it would require contacting support. See [[services-known-gaps]] for the refund / cancellation gap inventory.

### One-off cancellation before delivery — support-only

There is NO in-app cancel action for one-off services once Pay Now has succeeded. The merchant must contact CloudCart support to cancel a one-off service before delivery. Only recurring services can be self-service-cancelled (via [[subscriptions]]).

## How it works (verified against backend)

### Invoice generation

When Pay Now succeeds, the invoice is generated using the merchant's [[billing-invoicing]] fields + the service's source-currency `price` + VAT per the merchant's billing-country rule above. The PDF is emailed to the invoicing email on file. The invoice appears in the merchant's invoice history.

### Subscription join

The `SiteSubscription` record created at Pay Now time carries the `billing_cycle` from the service row. Recurring billing is then driven by the renewal job that processes due `SiteSubscription` rows on each cycle (`(verify)` — same machinery as the plan renewal).

## Related

- [[services]] — hub.
- [[services-catalog]] — where billing-cycle labels appear in the row UI.
- [[services-purchase-flow]] — Pay Now flow that triggers VAT computation + subscription creation.
- [[services-routes]] — which routes create which `SiteSubscription`.
- [[services-known-gaps]] — silent FX gap; no refund self-service; no one-off cancel.
- [[subscriptions]] — where recurring services land after purchase.
- [[billing-invoicing]] — country / VAT ID source of truth for VAT rules.
- [[billing-cards]] — what is charged the final VAT-inclusive amount.
- [[plans]] — separate subscription surface (same `SiteSubscription` table).

## Open questions

- Confirm "every N months" rendering for `billing_cycle` values other than `1` / `12` / `24` `(verify)`.
- Confirm the exact renewal job that processes due service `SiteSubscription` rows `(verify)`.
