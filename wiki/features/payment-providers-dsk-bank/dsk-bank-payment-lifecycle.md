---
type: feature
nav_path: "Payment Providers → DSK Bank → Payment lifecycle"
route_name: apps.dsk_bank.overview
route_path: /admin/payment-providers/dsk_bank
aliases: ["DSK Bank payment lifecycle", "DSK 3DS", "DSK return URL", "DSK order status mapping", "DSK orderNumber", "DSK getOrderStatusExtended", "DSK webhook URL"]
tags: [paymentproviders, payment-providers, dsk-bank, card-gateway, payment-lifecycle, bulgaria]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-dsk-bank]]. See the hub for related aspects (settings, authorize/capture, refund/currency).

# DSK Bank — Payment lifecycle

## Purpose

This aspect documents the end-to-end **payment flow** for a DSK Bank charge: how the platform registers the order with DSK, redirects the customer to the hosted 3-D Secure page, reads the return, periodically syncs to reconcile missed callbacks, and maps DSK's status integer onto the platform [[payment-status]]. 3DS is mandatory on every charge.

## Where to find it

This is runtime behaviour, not a settings screen. The merchant configures the provider on [[dsk-bank-settings-fields]] and gives DSK a return URL (below); the lifecycle then runs automatically whenever a customer pays. Per-order outcomes appear on the order details payment panel — see [[orders-details]].

## What the merchant can do here

- **Give DSK the correct return URL** to set on their terminal (see Business rules below).
- **See the resolved payment status** on the order details page once the customer returns or the periodic sync reconciles the payment.
- **Read provider-side failures** from the order's payment audit log when a charge fails.

## Settings & fields

This aspect exposes no settings fields of its own — credentials and currency are configured on [[dsk-bank-settings-fields]]. The only merchant-supplied value relevant here is the **return URL** the merchant enters in DSK's own merchant portal (not in CloudCart):

```
<cc_payments_domain>/return/provider/dsk_bank
```

## Business rules

### 3-D Secure is mandatory

Every DSK Bank charge runs through the bank's 3DS flow on `epg.dskbank.bg` (live) or `epgtest.dskbank.bg` (test). The merchant cannot disable 3DS — it is the bank's policy. The customer is bounced to DSK's hosted page, completes the 3DS challenge if their issuer demands it, and returns to the platform's `payments.return` URL.

### Order ID format

The platform sends `orderNumber = <internal_order_id>-<site_id>` (e.g., `123456-789` for order 123456 on site 789). This makes the reference unique across multiple CloudCart sites on the same DSK account. The customer-facing description sent to DSK reads `Order #<order_id> | <hostname>` using whichever Order ID display the merchant configured (sequential ID or `increment_hash`).

### Return / webhook URL

The return URL the merchant tells DSK to set on their terminal:

```
<cc_payments_domain>/return/provider/dsk_bank
```

DSK's hosted page POSTs back with `orderId=<order-reference>` after the customer completes payment. `returnUrl` and `failUrl` are both set to the same URL — the platform reads `orderStatus` to decide success vs failure. The platform also syncs payments periodically by polling DSK's order-status endpoint so missed return-URL callbacks are eventually reconciled.

### Status code mapping

DSK returns an `OrderStatus` integer in the order-status response:

| DSK orderStatus | Mapped platform [[payment-status]] |
|-----------------|-----------------------------------|
| `0` / `5` | `Pending` (customer hasn't completed payment yet) |
| `1` | `Authorized` (Two-Step pre-auth held — see [[dsk-bank-authorize-capture]]) |
| `2` | `Completed` |
| `3` | `Canceled` |
| `4` | `Refunded` (see [[dsk-bank-refund-currency]]) |
| anything else | `Failed` |

### Error handling — payment-flow errors land in the payment log, not exceptions

If DSK returns a provider-side failure (e.g., "Access denied" because the credentials are wrong, or a soft decline like "insufficient funds"), the platform marks the payment as `Failed`, logs the error to the order's payment audit log, and surfaces it to the merchant — but it does NOT raise a global exception. This keeps DSK provider hiccups from polluting the platform's exception logs. The merchant can see the error from the order's payment details panel.

## How it works (verified against backend)

Built on the `omnipay-dsk-bank` driver.

### Payment lifecycle

1. **Purchase** calls DSK's `registerOrder` (or `registerPreAuth` for manual capture — see [[dsk-bank-authorize-capture]]) with `orderNumber = <internal_order_id>-<site_id>` (ensures uniqueness across multi-site DSK accounts), `amount` in minor units, `currency`, `returnUrl`, `failUrl` (both set to the same `<cc_payments_domain>/return/provider/dsk_bank`), and description `Order #<order_id> | <hostname>`. DSK responds with `orderId` (DSK-side reference) and `formUrl`.
2. **Redirect**: the customer is sent to `formUrl` (DSK's Way4-based hosted page).
3. **3DS** happens on `epg.dskbank.bg`. Mandatory.
4. **Return**: DSK POSTs back with `orderId=<dsk-side-reference>`. The platform reads `orderStatus` via `getOrderStatusExtended` and updates the platform's status (see *Status code mapping*).
5. **Sync**: a periodic sync polls `getOrderStatusExtended` to reconcile missed returns.

## Related

- [[payment-providers-dsk-bank]] — hub.
- [[dsk-bank-settings-fields]] — credentials + currency the lifecycle uses.
- [[dsk-bank-authorize-capture]] — the Two-Step (pre-auth) variant of the purchase request.
- [[dsk-bank-refund-currency]] — refund flow that flips `orderStatus 4` → `Refunded`.
- [[payment-status]] — the platform statuses this maps onto.
- [[orders-details]] — where the resolved status and payment log appear.
- [[checkout-flow]] — storefront checkout that triggers the purchase.

## Open questions

- None.
