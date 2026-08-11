---
type: feature
nav_path: "Payment Providers → myPOS → Payment lifecycle & 3DS"
route_name: apps.mypos.overview
route_path: /admin/payment-providers/mypos
aliases: ["myPOS Virtual Checkout", "myPOS 3DS", "myPOS IPN", "myPOS webhook", "myPOS return URL", "myPOS status mapping", "myPOS IPCPurchaseNotify", "myPOS OrderID", "myPOS purchase flow"]
tags: [paymentproviders, payment-providers, mypos, lifecycle, 3ds, ipn, status-codes]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-mypos]]. See the hub for related aspects (setup & config pack, save card, refund & sync).

# myPOS — Payment lifecycle & 3DS

## Purpose

This aspect documents what happens on the wire from "customer picks myPOS" to "order shows Completed in the admin". The flow is: purchase request → redirect to myPOS's hosted **Virtual Checkout** page → mandatory 3-D Secure → return + IPN webhook to CloudCart → signature verification → status mapping. The customer is redirected to myPOS's hosted Virtual Checkout page, enters their Visa / Mastercard / Maestro / VPay / JCB card, completes 3-D Secure, and the funds settle to the merchant's **myPOS wallet** (the merchant can then withdraw to their bank account or use the funds via myPOS's debit card).

## Where to find it

This aspect is invisible to the merchant — it's the runtime behaviour behind every order paid through myPOS. The merchant sees the result on the order in [[orders-details]]. The per-payment webhook / return URLs are dynamic and need no merchant configuration (see *Webhook / IPN URLs* below).

## What the merchant can do here

- **Inspect a payment's lifecycle** on the order details page — the myPOS response and mapped status are stored on the payment row.
- **Re-sync a stranded Pending payment** — see [[mypos-refund-sync]] for the periodic reconciliation mechanism.
- **Confirm no portal-side URL setup is needed** — both return and notify URLs are sent dynamically on every transaction (see below).

## Settings & fields

This aspect does not expose its own fields — the lifecycle is the runtime behaviour determined by the credentials on [[mypos-setup-config-pack]] (Configuration Pack, Mode). The save-card branch is documented on [[mypos-save-card]]; refunds and reconciliation on [[mypos-refund-sync]].

## Business rules

### 3-D Secure is mandatory

Every myPOS Virtual Checkout charge runs through 3DS on myPOS's hosted page (`www.mypos.com/vmp/checkout` for live, `www.mypos.com/vmp/checkout-test` for test). The merchant cannot disable 3DS — it's myPOS policy.

### Payment lifecycle (verified against backend)

1. **Purchase** builds an HTML auto-submit form via myPOS's IPC SDK (version 1.4) targeting `https://www.mypos.com/vmp/checkout` (live) or `/vmp/checkout-test` (test). Payload includes the SID, wallet number, OrderID, amount, currency, customer details, return + notify URLs, and an RSA signature with the merchant's private key.
2. **3DS challenge** happens on myPOS's hosted page.
3. **Return**: the customer returns to `<storefront_domain>/payment/return/<payment_id>`.
4. **IPN webhook**: myPOS POSTs to `<storefront_domain>/payment/webhook/<payment_id>` with `IPCmethod=IPCPurchaseNotify` (success) or `IPCPurchaseError` (failure). The platform verifies the signature against myPOS's public certificate from the pack, updates status, and **returns `OK` to acknowledge**.

### Webhook / IPN URLs (no merchant configuration needed)

The platform exposes per-payment URLs sent on every transaction, so there is nothing to configure inside myPOS's portal beyond the wallet:

```
URL OK / URL Cancel (return): <storefront_domain>/payment/return/<payment_id>
URL Notify (webhook / IPN): <storefront_domain>/payment/webhook/<payment_id>
```

myPOS calls the webhook with `IPCmethod=IPCPurchaseNotify` (success) or `IPCPurchaseError` (failure) and the platform reconciles the status. After processing, the platform returns `OK` to myPOS's webhook to acknowledge.

### Card networks supported

Visa, Visa Electron, VPay, Mastercard, Maestro, JCB. The platform's save-card helper maps each network to a brand label for display: VISA → "Visa", VPAY / Visa Electron → "Visa", Mastercard → "MasterCard", Maestro → "Maestro", JCB → "JCB". (Amex is typically not enabled on myPOS wallets — confirm with the merchant's contract.)

### Currency support (multi-currency)

myPOS wallets are typically provisioned for **BGN, EUR, USD, GBP** — whichever currencies the merchant has opted into during myPOS sign-up. The platform sends the storefront order's currency directly to myPOS on each transaction — no currency forcing or conversion at platform level. If the customer's currency isn't supported by the wallet, myPOS rejects the transaction at their side.

### Status code mapping

myPOS's `IPCmethod` and `PaymentStatus` map to the platform's [[payment-status]]:

| myPOS response | Mapped status |
|---------------|---------------|
| Webhook `IPCPurchaseNotify` (success) | `Completed` |
| Webhook `IPCPurchaseOK` (success) | `Completed` |
| Return URL `IPCPurchaseOK` | `Completed` |
| Sync `PaymentStatus = 1` | `Completed` |
| Sync `PaymentStatus = 2` | `Pending` |
| Sync any other status | `Canceled` |
| Webhook or return any other method | `Canceled` |

### Order ID format

The platform sends `OrderID = <internal order_id>` or the merchant's chosen Order ID display setting:

- **Live mode**: uses the configured `setting('order_id_display')` (sequential ID or `increment_hash`).
- **Test mode**: forces `increment_hash` for safety (test payments never expose real sequential order IDs to myPOS's test environment).

The customer-facing cart description sent to myPOS reads `Order #<order_id> | <hostname>`.

### Address handling

The platform sends the customer's full billing address to myPOS:

- First name, Last name, Phone (E.164 normalised)
- Street, City, ZIP
- Country (ISO 3166 alpha-3 code derived from the platform's alpha-2 — falls back to `BGR` if unknown)
- Email

This is required by myPOS's anti-fraud and 3DS data-quality rules. Digital orders without a billing address skip the address fields but still send email.

## Related

- [[payment-providers-mypos]] — hub.
- [[payment-status]] — Completed / Pending / Canceled / Refunded mapping for myPOS charges.
- [[orders-details]] — where the merchant sees the payment lifecycle result.
- [[checkout-flow]] — storefront checkout, where myPOS surfaces as a card payment option.

## Open questions

_None._
