---
type: feature
nav_path: "Payment Providers → Sofort"
route_name: apps.sofort.settings
route_path: /admin/payment-providers/sofort
aliases: ["Sofort", "Sofortüberweisung", "Sofort bank transfer", "SOFORT Klarna"]
tags: [paymentproviders, payment-providers, sofort, international, eu, bank-transfer, deprecated]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Sofort

## Purpose

Sofort (formerly Sofortüberweisung, now part of Klarna's Pay Now product) is a German-originated **online bank-transfer** payment method, widely used in Germany, Austria, Belgium, Italy, the Netherlands, Poland, Spain, Switzerland, and the United Kingdom. The customer logs into their own online banking through the Sofort hosted page (Sofort never stores the credentials), and Sofort initiates the transfer on the customer's behalf. The merchant sees a confirmed payment with high authenticity (the customer's bank actually initiated the SEPA transfer), and Sofort/Klarna passes the funds to the merchant's account.

**Deprecation note**: Sofort is a **deprecated** payment provider on CloudCart (alongside Instamojo) — hidden from the active-providers list and not installable from scratch. Stores with a long-standing Sofort configuration may still process payments, but new activations are not encouraged. Merchants wanting bank-transfer flows should use [[payment-providers-mollie|Mollie]] (which routes Sofort under its hood) or a direct Klarna integration. See [Deprecated status](#deprecated-status).

## Where to find it

Payment Providers → **Sofort** (not visible by default — deprecated).

URL: `/admin/payment-providers/sofort`. Route name: `apps.sofort.settings`.

Because Sofort is on the deprecated list, it's filtered out of the active-providers query, so a new merchant cannot reach a save form even via direct URL (the route resolves but the provider isn't in the install picker that drives the page). "Un-deprecating" it for a specific store requires a CloudCart support intervention, not an admin click.

## What the merchant can do here

(Applies to merchants with a pre-existing Sofort configuration.)

- Toggle the provider **Active**.
- Enter the **Customer Number** (Sofort/Klarna account customer ID).
- Enter the **API Key** (the secret key from the Sofort/Klarna dashboard).
- Enter the **Project ID** (Sofort project identifier from the Klarna dashboard).
- Pick the **Currency** — Sofort supports a limited set of currencies (see list below).
- View the **Webhook URL** to register with Klarna's dashboard for status notifications.
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with Sofort.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Customer Number** | The merchant's Sofort/Klarna customer number — used as the Sofort API username. | empty | Required. |
| **API Key** | The Sofort API secret key (acts as the API password). | empty | Required. |
| **Project ID** | The numeric Sofort project ID identifying which project / configuration this is. | empty | Required. |
| **Currency** | Charging currency. | empty (must pick) | Dropdown of supported currencies: CHF, CZK, EUR, GBP, HUF, PLN. EUR is most common. |
| **Webhook URL** | (Read-only display) The URL the merchant must register in Klarna's dashboard for status notifications. | Auto-generated: `https://<cc-payments-domain>/webhook/sofort` | Not editable. The merchant copies this into Klarna's dashboard. |
| **Storefront name** | Display name on storefront. | "Sofort" | Common option. |
| **Logo** | Provider logo. | Sofort default | Common option. |
| **Amount from / Amount to** | Order-amount range when Sofort is available. | empty / empty | Common gate. |
| **Discount when paying with Sofort** | Flat / percent / shipping-free discount. | none | Common option. |

### Supported currencies

Limited list: **CHF (Swiss Franc), CZK (Czech Koruna), EUR (Euro), GBP (British Pound), HUF (Hungarian Forint), PLN (Polish Złoty)**.

### UI vs. validation mismatch

The current Sofort settings screen only renders **API Key** + **API Secret** inputs (plus the read-only webhook URL, logo, description, amount-range, and discount controls). The other fields above — **Customer Number**, **Project ID**, **Currency** — are remnants of the original form: backend validation still requires `customer_number` and `project_id`, so a save from the current UI fails validation. This mismatch is another indicator of the integration's deprecated state.

## Business rules

### Customer flow at checkout

1. Customer picks Sofort at checkout; a payment is created and Sofort is called with the amount in the configured currency, a transaction reference, the return/success/abort/notification URLs, and the project ID. Payment status → `requested`.
2. Customer is redirected to Sofort's hosted page, selects their country and bank, logs into their online banking, and confirms the transfer.
3. Sofort returns the customer to the store, then POSTs a status notification to the webhook URL when the transfer is confirmed (or failed). The matching payment is updated.

### Notification format — XML, not JSON

Unlike most modern providers, Sofort sends status notifications as **XML** documents (a legacy of its pre-REST API design). On the incoming webhook the raw request body is parsed as XML and the `<transaction>` element's reference is used to look up the matching payment:

```
POST /webhook/sofort
Content-Type: application/xml
Body:
  <?xml version="1.0"?>
  <status_notification>
    <transaction>123456789-...-AAA</transaction>
    <time>2026-05-22T...</time>
    ...
  </status_notification>
```

If the XML is malformed or the transaction reference isn't found, the platform returns a Bad Request. Most modern providers use JSON with HMAC signatures; Sofort/Klarna kept XML for backwards compatibility, part of why the integration is being deprecated.

### Currency

The configured currency is sent fixed to Sofort. Most stores use EUR. A store selling in a non-supported currency must convert prices manually or pick a supported currency at the Sofort level (which means showing customers two currencies).

### Capture mode

Auto. Bank transfers are inherently auto-captured — once the customer's bank confirms the transfer, the money is on its way. No manual capture.

### Refunds

Refunds are **manual** at the Klarna side — the merchant initiates them through Klarna's merchant portal, not through CloudCart, and uses that portal for partial refunds and refund-status tracking. The integration's refund call relies on the bundled Omnipay-Sofort adapter; since Klarna migrated Sofort onto a newer API, the legacy call may 404 or return a deprecated-API error against current accounts. Treat Sofort refunds as Klarna-portal-only in practice.

### Recurring / subscriptions

Not supported. Sofort is a one-off bank-transfer mechanism; the customer must re-authorize each transfer.

### 3D Secure

Not applicable — bank-transfer auth uses the customer's banking credentials (two-factor at the bank's side), not card 3DS.

### Plan-gating & permission

No plan-feature gate. Requires the standard payment-providers permission (`store.payment_providers`).

### Deprecated status

**Sofort is on CloudCart's deprecated-providers list** and the active-providers query skips it. A store with a stored configuration row continues to render the settings page and process payments, but deprecated providers don't appear in the install picker, so new stores cannot get to a save form. The recommended migration path for existing Sofort merchants is [[payment-providers-mollie|Mollie]] — it exposes Sofort as one of its payment methods, preserving the customer experience while giving the merchant a maintained integration. Klarna's newer Klarna Payments product is also viable but not yet shipped as a separate CloudCart integration.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-mollie]] — modern alternative that supports Sofort under the hood as one of many payment methods.
- [[orders-payment-refund]] — refund concept (Sofort refunds are typically done at Klarna's portal, not here).
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
