---
type: feature
nav_path: "Payment Providers → Bank Wire Transfer"
route_name: apps.bwt.settings
route_path: /admin/payment-providers/bwt
aliases: ["Bwt", "BWT", "Bank Wire Transfer", "Bank Transfer", "Wire Transfer", "Bank deposit", "Банков трансфер", "Платежно нареждане"]
tags: [paymentproviders, payment-providers, bwt, offline, bank-transfer, manual-payment, global]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Bank Wire Transfer

## Purpose

**Bank Wire Transfer (BWT)** is CloudCart's **offline-payment method** for accepting bank wire transfers from customers. When the customer picks BWT at checkout, the order is placed in **Requested** status and the customer is shown a merchant-configured **Description** — typically bank account details (IBAN, account holder name, BIC/SWIFT, payment reference instructions). The customer transfers the funds manually, and the merchant marks the payment as Paid from the order page once the transfer arrives.

This is not a gateway — there's no automated checking and no API integration. BWT is **global by design**: any country, any currency, any bank. Its only job is to (1) surface the bank-details description to the customer at checkout and (2) place the order in a clean Requested state so the merchant can fulfil it once funds are verified.

## Where to find it

Sidebar → **Payment Providers** → click **Bank Wire Transfer**. The route is `/admin/payment-providers/bwt`. The internal provider key is `bwt`. Default storefront label: **"Bank Wire Transfer"** (EN) / **"Банков трансфер"** (BG).

## What the merchant can do here

- **Install / Uninstall** the BWT method (see [[settings-payment-providers]]).
- **Toggle Active** on / off in the header.
- **Edit the long Description** (`configuration.description`) — the bank-details text shown to the customer **after** they place an order (order-confirmation page + confirmation email).
- **Edit the Payment-method description** (`configuration.payment_description`) — the brief blurb shown **during** checkout, when the customer is choosing the payment method.
- **Override the customer-facing label** — logo and title on the storefront payment-method picker.
- **Set an amount range** (min / max) and an optional **discount** for the method.
- **Mark a BWT payment as Paid manually** from the order page (see [[orders-payment-mark-paid]]) once the funds arrive.

## Settings & fields

The settings page is the **simplest of all payment providers** — no environment-mode radio, no card-save toggles, no provider-specific options. Sections render top-to-bottom: Header (status bar + Enable/Disable), single Settings tab, then four slide-outs.

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Payment-method description** (`configuration.payment_description`) | TinyMCE editor. Brief text shown to the customer **during** checkout when picking the method. | Empty | Help text: "The description entered above will be visible to your customers every time they choose the payment method when finalizing the order." |
| **Acceptance by order amount** (`configuration.amount_from` / `configuration.amount_to`) | Restrict the method to orders inside this range (currency unit). | Empty | |
| **Discounts** (`configuration.discount_type` / `configuration.discount_amount`) | Discount applied when the customer picks BWT. Type: Fixed / Percent / Free shipping. | `discount_type: flat` (Fixed amount) | |
| **Checkout settings — Description** (`configuration.description`) | TinyMCE editor. The **long bank-details text** shown on the order-confirmation page and email (IBAN, BIC, account holder, payment reference). | Empty | Required. Max 50,000 characters. Errors: "Bank wire transfer: description is required." / "Bank wire transfer: description should be less than 50000 characters long." |
| **Logo / Title** | Standard storefront-label override. | Provider defaults | |

The **Description** is HTML / rich text: the storefront prints the saved HTML verbatim after the customer places the order, so IBANs, BIC, recipient, deadline and notes can be formatted with bold / lists / tables. The 50,000-character cap is enforced server-side.

## Business rules

### Customer flow — instant order placement, no charge

1. Customer reaches checkout, picks BWT, clicks Place Order.
2. The platform immediately sets the payment status to **Requested** and returns no action to the storefront — no redirect, no popup, no iframe.
3. The order-confirmation page renders with the merchant's full **Description** (the bank account details). The confirmation email includes the same text.
4. The merchant waits for the wire to arrive, then opens the order in admin and clicks **Mark as Paid** (see [[orders-payment-mark-paid]]) — flipping the payment status to **Completed**.

There is no automated reconciliation — the merchant's bank doesn't talk to CloudCart, so verification is fully manual. The audit trail is the manual order log only; BWT stores **no `provider_data`** on the payment row (unlike gateway providers, which store the gateway's response).

### Description content best practices

Typical Description content: account holder name (must match the bank transfer form), IBAN (or local account number), BIC / SWIFT (for international transfers), bank name, and a line like *"Please use your order number `<order_id>` as the payment reference"* so the merchant can match the incoming wire to the order. Some merchants add a deadline ("Order will be cancelled if payment is not received within 7 days"), enforced manually via order cancellation.

### Currency, multi-IBAN, refunds, reminders

- **Currency-agnostic** — the integration does nothing about currency. The customer pays in whatever currency the order is in.
- **One BWT instance per store** — per-country / per-currency multiple BWT providers are not supported. Merchants with multiple IBANs (e.g. separate EUR / USD accounts) put all of them inside the single Description, typically in a table labelling which IBAN to use for which currency or country.
- **Refunds** happen offline — the merchant wires funds back and may change the order's payment status manually to reflect it.
- **Auto-reminder emails** for customers who haven't wired within N days are **not implemented**; the merchant follows up or cancels manually. There is no platform-side reminder timer for offline-payment orders.

### Provider classification

BWT is classified as **offline** (`is_offline_payment=true`) but **also as seller-payer-shipping** (`is_seller_payer_shipping=true`) — an explicit carve-out. Even though BWT is offline, the merchant absorbs shipping cost the same way they would for an online card payment. (Compare with Cash on Delivery, where the customer typically pays shipping on top.)

### Plan-tier gating

None — BWT has no gateway-side costs and is available on every plan.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where BWT is installed / uninstalled.
- [[orders-payment-mark-paid]] — the manual flow for marking a BWT payment as received.
- [[orders-payment-manual]] — concept page on manual / offline payments generally.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Requested / Completed mapping for offline flows.
- [[checkout-flow]] — concept page on the storefront checkout (BWT shows description after Place Order).

## Open questions

(none)
