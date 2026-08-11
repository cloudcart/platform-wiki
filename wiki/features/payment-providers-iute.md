---
type: feature
nav_path: "Payment Providers → Iute"
route_name: apps.iute.overview
route_path: /admin/payment-providers/iute
aliases: ["Iute", "Iute Credit", "IuteCredit", "Iute installment", "Iute BNPL", "Iute Pay", "Иуте", "Иуте кредит"]
tags: [paymentproviders, payment-providers, iute, bnpl, installments, bulgaria, albania, moldova, north-macedonia, bosnia-herzegovina]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Iute

## Purpose

**Iute** (full name *Iute Credit*) is a multi-country consumer-loan provider operating in Bulgaria, Albania, Bosnia and Herzegovina, North Macedonia, and Moldova. The merchant signs a contract with Iute, gets two API keys per environment (`api_key` for storefront calls + `admin_api_key` for catalog management), picks the country, and Iute becomes selectable on the storefront. The customer-facing flow uses Iute's own JavaScript module (`iutepay.js`) injected into the storefront — the customer goes through Iute's fast-checkout entirely inside an embedded modal, and CloudCart receives a `checkoutSessionId` to confirm the order.

Iute's pricing model is **catalog-driven on Iute's side** — the merchant uploads a mapping of CloudCart SKU → Iute's "loan product" ID via the [[payment-providers-iute-schemes|Schemes tab]] (Iute calls these "product mappings"). Each Iute loan product defines its own months / rate / monthly payment. The mapping list lives entirely on Iute's servers; CloudCart reads it via the admin API on the Schemes tab.

## Where to find it

Sidebar → **Payment Providers** → click **Iute**.

The route is `/admin/payment-providers/iute`. The hub page renders the standard payment-provider overview, with three tabs at the top: **Overview**, **Settings**, **Schemes**.

## What the merchant can do here

- **Read the overview card** — logo, description, and the standard install / activate / deactivate buttons.
- **Install / Uninstall the payment method** through the overview's standard buttons.
- **Activate the payment method** once both API keys are saved AND validated by Iute on save.
- **Switch between the three tabs**:
  - [[payment-providers-iute-settings]] — country selector, test/live mode, two API keys per environment, promo-button switch.
  - [[payment-providers-iute-schemes]] — map CloudCart products to Iute loan-product IDs (per Iute's catalog).

## Settings & fields

This is a hub page — the actual fields live on the two sub-tabs. The overview itself only exposes the standard payment-provider controls:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Creates the `PaymentProviderConfiguration` for `iute`. | Not installed | One-click. |
| **Active** switch | Turns Iute ON / OFF for storefront checkout. | OFF | Server refuses activation unless API keys are saved AND Iute validates them via `validateApiKey` + `validateAdminApiKey`. |
| **Test mode switch** | Switches between test (`_test`) and live credentials. | test | Both sets saved at once. |
| **Min / Max amount** | Order-total range in which Iute shows on checkout. | Empty | Standard. |
| **Logo / Title / Description** | Customer-facing label on checkout. | Provider defaults | Standard. |
| **Discount** | Optional discount when customer picks Iute. | None | Standard. |

## Business rules

### How Iute works for the merchant

1. **Catalog setup** — the merchant uploads Iute SKU mappings via the Schemes tab. Iute uses these to decide what loan terms to offer for each product.
2. **Customer browses** — on the product page, if the merchant has the **promo button** enabled, Iute's `iutepay.js` module renders a "Pay with Iute" promo button + monthly price preview inline. The module calls Iute directly for the price preview (no CloudCart calculation API).
3. **Customer adds to cart and checks out** — picks Iute at checkout. CloudCart embeds Iute's `iutepay.js` module in the storefront checkout. Iute's modal takes over.
4. **Customer completes Iute's flow** — identity, employment data, etc., all inside Iute's modal. On success, the modal calls back into CloudCart with a `checkoutSessionId`.
5. **CloudCart finalises** — the platform receives the session ID, calls Iute's order-status endpoint to fetch the loan status, and updates the payment accordingly.
6. **Status confirmations via webhook** — Iute pushes status changes to CloudCart at `payments.webhook` with signed headers (`x-iute-timestamp` + `x-iute-signature`). The signature is verified with Iute's public key.

### Multi-country base URL pattern

Iute's API base URL depends on the merchant's chosen country AND mode:

```
Live: https://ecom.iutecredit.{bg|al|ba|mk|md}
Test: https://ecom-stage.iutecredit.{bg|al|ba|mk|md}
```

The `country` config picks the country TLD; `mode` picks the `-stage` suffix. Each merchant operates in exactly one country (no multi-country single-store support).

### Webhook signature verification

Iute pushes status callbacks signed with their public key. CloudCart checks the `x-iute-timestamp` + `x-iute-signature` headers against Iute's loaded public key — requests without valid signatures are rejected and CloudCart returns HTTP 400. This protects against forged callbacks impersonating Iute.

### Two API keys per environment

Iute uses two different keys for different scopes:

- **api_key** — for storefront calculation calls (calculating monthly price for a basket; sent via `x-iute-api-key` header).
- **admin_api_key** — for catalog management (listing loan products, managing product mappings, fetching order status; sent via `x-iute-admin-key` header).

Both must be valid for activation. On save, the platform validates:

- API key — POSTs a dummy calculation request to `/api/v1/eshop/client/eshop-product/-/calculation` with a 250-amount sample.
- Admin API key — GETs `/api/v1/eshop/management/loan-product`.

If either fails, the merchant sees the error `"Invalid api key"` or `"Invalid admin api key"` on the respective field.

### Promo button on product page

When the **promo button** is enabled (Settings tab), CloudCart injects Iute's `iutepay.js` on every product page and renders:

```html
<div id="iute-trigger" class="iute-as-low-as"
     data-id="{$product_id}" data-amount="{$price}"
     data-page-type="product" data-sku="{$product_id}"
     data-learnmore-show="false"></div>
```

This shows "from {monthly} per month" or "learn more" with Iute's branded styling. Customers can also click the button to start the fast-checkout flow directly from the product page (skipping the cart).

### Refund handling

Refunds are NOT exposed in CloudCart's admin for Iute — the merchant handles refunds via Iute's portal.

### Plan-gating

Not gated by CloudCart subscription tier.

### Country + currency

Country dropdown lists: Bulgaria (BG), Albania (AL), Bosnia and Herzegovina (BA), Macedonia (MK — the picker label reads just "Macedonia", though the country is officially North Macedonia), Moldova (MD). The currency is the country's national currency — Iute returns prices in that currency from its calculation API. No multi-currency support per merchant.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-iute-settings]] — country, mode, API keys, promo-button switch.
- [[payment-providers-iute-schemes]] — per-product Iute loan-product mappings.
- [[payment-providers-klear]] — Klear lending, another EU consumer-loan provider with similar API-driven architecture.
- [[payment-providers-fusion-pay]] — TBI Bank installment, similar module-injection pattern.

## Open questions

- ⏸️ Iute public-key rotation cadence — Iute-side process, not documented in CloudCart. The integration always fetches Iute's current key live for webhook-signature verification, so rotation is transparent; the cadence itself is set by Iute.
