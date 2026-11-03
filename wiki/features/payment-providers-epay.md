---
type: feature
nav_path: "Payment Providers → ePay"
route_name: apps.epay.settings
route_path: /admin/payment-providers/epay
aliases: ["ePay", "ePay.bg", "EPay", "Epay", "ePay e-wallet", "ePay карта", "Епей"]
tags: [paymentproviders, payment-providers, epay, wallet, bulgaria, online]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# ePay

## Purpose

A configuration screen for the **ePay.bg** e-wallet payment gateway — one of Bulgaria's oldest online payment providers, popular for both registered ePay account holders (e-wallet transfers) and customers who pay by debit card through the ePay-branded card-acceptance flow. The merchant enters two credentials (KIN + secret), picks Test or Live, and ePay starts appearing as a checkout option for Bulgarian customers.

ePay processes payments in **BGN** (Bulgarian lev). At checkout, the customer is redirected to the ePay-hosted payment page, completes the payment (either by logging into their ePay account or by entering card details), then returns to the store. ePay confirms the outcome asynchronously via an IPN (instant payment notification) webhook.

## Where to find it

Payment Providers → **ePay**. Provider key: `epay`. Route name `apps.epay.settings`, path `/admin/payment-providers/epay/settings`. Available after installing from [[settings-payment-providers]] → "Add payment method".

## What the merchant can do here

- **Toggle Test / Live mode** — Test mode points the gateway at `demo.epay.bg`; Live mode hits the production endpoint.
- **Enter the ePay credentials**: KIN (customer number) and Secret. Both required.
- **See the read-only Webhook URL** that must be entered in the merchant's ePay dashboard so ePay can POST the IPN to CloudCart.
- **Customer-facing title** override (the label shown at checkout — e.g., rename "ePay" → "Плати с ePay").
- **Logo override**.
- **Set a per-provider discount / fee** (see [[discount]]).
- **From / To availability window**.
- **Active toggle** (master switch).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** switch (`mode`) | When OFF (test): payments go to `demo.epay.bg`. When ON (live): payments go to `www.epay.bg`. | `test` after install | Help text: *"Use test mode to test your connection. Live mode is for the actual payment processing. Use live mode when you have verified your credentials."* |
| **KIN** (`kin`) | ePay customer number — the merchant's identifier in the ePay system. | required | Label: *"This is your ePay client number (KIN)"*. Placeholder: *"Enter kin"*. |
| **Secret** (`secret`) | ePay shared secret — used to sign payment requests and verify the IPN response. | required | Label: *"This is your ePay secret."*. Placeholder: *"Enter secret"*. Treat as confidential. |
| **Webhook URL** (read-only) | The URL the merchant must paste into the ePay merchant dashboard. ePay POSTs the payment outcome (PAID / DENIED / EXPIRED) to this URL. | `<payments-domain>/webhook/epay` | Auto-generated. Card label: *"Webhook URL"*. |

### Validation errors

| Trigger | Message |
|---------|---------|
| KIN missing | "EPay: KIN is required." |
| Secret missing | "EPay: secret is required." |

(In the Vue panel: the translation map shows these exact strings, plus their Bulgarian counterparts.)

## Business rules

### Currency: BGN only

ePay charges in **BGN**. The platform does NOT auto-convert non-BGN cart amounts — the cart amount is passed as-is to ePay, sent in BGN with two decimals. **In practice, stores that operate in EUR / USD / RON cannot use ePay as a working checkout option.**

### Checkout flow — redirect

1. Customer chooses ePay at checkout → submits. The payment request uses the CloudCart payment ID as the transaction ID, with a `returnUrl` (`site.payment.return`) and `cancelUrl` (`site.payment.cancel`).
2. ePay returns a redirect URL; the customer's browser redirects to ePay.
3. Customer completes payment on ePay (account login OR card-payment form).
4. ePay redirects back to `site.payment.return`. At this point the payment is marked `pending` (not `completed` yet — final confirmation comes via the webhook).
5. **In parallel**, ePay POSTs an IPN to `<payments-domain>/webhook/epay`. The platform verifies the signature using the merchant's secret, sets the payment status (PAID → `completed`, DENIED → `failed`, EXPIRED → `timeouted`), and replies with the `notify_text` ePay expects to confirm the IPN was accepted.

### IPN signature verification — the `encoded` field

ePay sends the IPN as a base64-encoded blob signed with the merchant's `secret`. The decoded body looks like:

```
INVOICE=<payment_id>:STATUS=<PAID|DENIED|EXPIRED>(:PAY_TIME=<ts>:STAN=<n>:BCODE=<code>)?
```

The `INVOICE` value IS the CloudCart payment ID, and the matched payment must belong to the `epay` provider. Anything that doesn't parse or match returns a Bad Request error.

### Test mode endpoint

When `mode = test`, the redirect goes to `demo.epay.bg` (use ePay's published demo credentials and demo cards); when `mode = live`, it goes to `www.epay.bg`. **There is no separate Test KIN / Live KIN field** — both modes use the same KIN + Secret fields; only the endpoint changes with the `mode` toggle. The merchant rotates their entered credentials between demo and production values.

### `enable_iframe` configuration flag

An `enable_iframe` (boolean) flag exists but is NOT exposed as a toggle in the settings UI. When set, the gateway switches from a full-page redirect to an embedded iframe — but the admin panel doesn't let the merchant configure this today.

### Order-ID format

The integration sends CloudCart's internal payment ID (an integer) as the ePay transaction ID — NOT the merchant-facing order ID. The customer's ePay receipt and any ePay support ticket reference this internal payment ID. The order's customer-facing increment hash (e.g., `2024-11-0042`) is NOT visible on the ePay side.

### Refund

API-driven refunds are not supported for ePay. To refund an ePay payment, the merchant logs into their ePay dashboard and initiates the refund from there. Then mark the order's payment row as Refunded in CloudCart manually.

### No periodic status sync

Unlike ePay One Touch, this integration does NOT poll the gateway for transaction status. Payment status is driven entirely by the IPN. If the IPN never arrives (rare but possible — ePay outage, merchant's webhook URL is wrong), the payment stays in `pending` indefinitely.

### Country restriction — Bulgaria only

ePay is country-restricted to BG (`operation_country = BG`). Merchants whose store country is RO / GR / MK / etc. won't see ePay in the Add-payment-method modal. Combined with the BGN-only rule above, ePay is effectively a Bulgaria-only checkout option.

### Payment logging

Every purchase request (site → ePay) and every IPN (ePay → site) is recorded in the order's payment log with the request and response bodies — useful for support troubleshooting.

### Permission

Configuring ePay requires the `store.payment_providers` permission section.

### Saving

Saving the settings updates the provider configuration immediately. No queued background jobs.

## Related

- [[payment-providers]] — parent hub; the payment record gets `provider=epay` and advances `requested → pending → completed`.
- [[payment-providers-epay-one-touch]] — ePay's one-click "saved card" variant (separate provider in the platform).
- [[payment-providers-epay-worldwide]] — Borica-acquired international card processor branded under ePay (separate provider).
- [[settings-payment-providers]] — install/uninstall, master Active toggle.
- [[discount]] — per-provider fee/discount.
- [[orders-payment-refund]] — manual Refund flow after ePay-side refund.
- [[checkout-flow]] — how the redirect happens.
- [[settings-general]] — store-country filter; ePay is available only for BG-country stores.

## Open questions

(none)
