---
type: feature
nav_path: "Payment Providers → NewPay"
route_name: apps.newpay.settings
route_path: /admin/payment-providers/newpay
aliases: ["NewPay", "Newpay", "newpay.bg", "Плати с NewPay", "Нюпей", "NewPay BNPL"]
tags: [paymentproviders, payment-providers, newpay, bnpl, bulgaria, online]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# NewPay

## Purpose

A configuration screen for **NewPay.bg** — a Bulgarian alternative-payment provider (typically positioned as a BNPL-like / installment-style payment option). The merchant enters two API credentials (API Key + API Secret), picks Test or Live mode, and NewPay starts appearing as a checkout option for Bulgarian customers.

At checkout, the customer is redirected to a NewPay-hosted payment page where the actual payment plan and authorization happen. After completion, NewPay calls back to CloudCart's webhook to confirm the order's final status.

The integration sends the full cart product list, customer details, and a logo to NewPay so its payment page can show a branded order summary.

## Where to find it

Payment Providers → **NewPay**. Provider key: `newpay`. Route name `apps.newpay.settings`, path `/admin/payment-providers/newpay/settings`.

## What the merchant can do here

- **Toggle Test / Live mode** — Test points to `sandbox.newpay.bg`, Live points to `newpay.bg`.
- **Enter the NewPay credentials**: API Key and API Secret. Both required.
- **See the read-only Webhook URL** that NewPay calls back to with payment outcomes.
- **Customer-facing title** override.
- **Logo override**.
- **Per-provider discount / fee** ([[discount]]).
- **From / To availability window**.
- **Active toggle**.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** switch | Test → `sandbox.newpay.bg/api/v1`. Live → `newpay.bg/api/v1`. | test after install | Stored as `configuration.mode` = `'live'` or `'test'`. Help text: *"Use test mode to test your connection. Live mode is for the actual payment processing. Use live mode when you have verified your credentials."* / BG: *"Използвай тестовата Среда, за да пробваш връзката. Реалната Среда е за обработване на плащания. Използвай реалната Среда, когато верифицираш данните си за достъп."* |
| **API Key** | NewPay-issued API key — the merchant identifier used to authenticate API calls. | required | Stored as `configuration.api_key`. Source label: *"API Key"*. Placeholder: *"API key"*. Help text: *"Enter your NewPay API Key"* / BG: *"Въведете API ключ за достъп до NewPay"*. Validation error: "API Key is required". |
| **API Secret** | NewPay-issued shared secret — used along with API Key to generate the authentication token and verify webhook checksums. | required | Stored as `configuration.api_secret`. Source label: *"API Secret"*. Placeholder: *"API secret"*. Help text: *"Enter your NewPay API Secret"* / BG: *"Въведете API тайна за достъп до NewPay"*. Validation error: "API Secret is required". |
| **Webhook URL** (read-only) | The URL NewPay calls back to confirm payment outcome. | `<cc_payments-domain>/webhook/newpay` | Auto-generated. Card label: *"Webhook URL"*. |

## Business rules

### Checkout flow — token-authenticated, redirect

1. Customer chooses NewPay at checkout → submits.
2. The integration builds a full purchase payload that includes the customer (first name, a single hardcoded space as middle name — NewPay's API requires the field, last name, phone, email), the cart product list with images and URLs, the shipping line item (as a synthetic product), and success / fail return URLs. The phone falls back to the alternative phone if no payment-address phone is set.
3. The client first authenticates against NewPay's `/authentication/get-token` endpoint with the API Key + API Secret to obtain a Bearer token.
4. The token is used to POST to `/purchase`, which returns a `payload.redirectUrl`.
5. CloudCart records NewPay's payment ID as the provider reference, saves the request payload against the payment, and responds to the storefront with a redirect action to the NewPay URL.
6. Customer is redirected to NewPay's payment page.
7. After payment, NewPay redirects back to `site.payment.return` and the payment is marked `pending` (final outcome is webhook-driven).
8. **NewPay POSTs the IPN to `<cc_payments>/webhook/newpay`** with a checksum-hashed `X-API-TOKEN` header.

### Product-list and shipping shown on the NewPay page

Unlike most other providers (which send only the total amount), NewPay receives the entire product list with images:

- Each cart product → a line item with name, price, URL, image, and quantity.
- The shipping cost → a synthetic line item using the provider name + service name as label, the shipping amount, the primary store URL, and the store logo.

This means **the customer sees an itemized order summary on the NewPay-hosted page** — useful for purchases involving multiple items where the customer wants to confirm what they're financing.

### Discount handling on the line items

The integration handles store-wide "order-over" discounts by spreading the discount proportionally across the products:

- If the discount type is `percent`, each product's price is reduced by `price * (discount% / 100) / 100`.
- If the discount type is `flat`, each product's price is reduced proportionally based on its share of the subtotal: `price * (discount / subtotal)`.

This ensures the sum of line-item prices matches the cart total NewPay receives, even with promotional discounts applied.

### Webhook checksum verification

On the incoming IPN, the platform validates the `X-API-TOKEN` header against a SHA-256 hash of API Key + API Secret + `purchaseId`. If the checksum doesn't match, the webhook returns HTTP 401 with `{ status: 'error', message: 'Invalid API-TOKEN' }`. This protects against unauthenticated webhook spoofing.

### Status mapping

| NewPay status | CloudCart payment status |
|---|---|
| `finalised` | `completed` |
| `cancelled` | `cancelled` |
| (anything else) | `unknown` (kept as-is) |

### Cart currency

NewPay's API expects amounts as decimal numbers (rounded to 2 places). The integration sends `order_price / 100` (cents → currency units). No currency-conversion logic exists in the integration — the cart currency is sent through as-is in the line items. Verify with NewPay which currencies their account supports (BGN is the primary market; EUR likely on request).

### Order-ID

The internal CloudCart payment row ID is sent as the `purchaseId`. The customer-facing order ID is NOT passed to NewPay separately — the merchant must cross-reference via CloudCart's order list.

### Test endpoint

Sandbox: `https://sandbox.newpay.bg/api/v1`
Production: `https://newpay.bg/api/v1`

### Shipped-notification API

The NewPay client supports a "shipped" notification that POSTs to `/shipped` on NewPay — meant to tell NewPay the merchant has dispatched the order (relevant for BNPL providers that release funds after shipment confirmation). **This call exists in the client but is not wired up to any CloudCart event today.** A future enhancement could trigger it on order-status change to `shipped`.

### Refund

Not implemented in this integration. Refunds must be coordinated through NewPay's merchant dashboard, then marked Refunded in CloudCart manually.

### Permission

Requires `store.payment_providers`.

### Cache + side effects

Saving settings is a synchronous update on the payment-provider configuration row. No queued jobs at save time. The payment-flow side effects (purchase request, webhook receive) happen on per-customer-transaction events.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — install/uninstall.
- [[settings-general]] — `operation_country` filter (NewPay typically BG-restricted).
- [[discount]] — per-provider fee/discount; on-cart discounts are also spread across line items sent to NewPay.
- [[orders-payment-refund]] — manual Refund.
- [[checkout-flow]] — redirect flow.
- [[payment-providers]] — the `payments` row gets `provider=newpay`.

## Open questions

- ⏸️ Whether NewPay requires shipment confirmation for fund release is a NewPay contract detail. The NewPay shipped-notification API client exists in the integration but is not wired to any CloudCart event — today the merchant notifies NewPay outside CloudCart if required.
- ⏸️ Which currencies a particular NewPay merchant account can settle in is a NewPay contract question. CloudCart sends whatever currency the cart is in; BGN is the primary market.
