---
type: feature
nav_path: "Payment Providers → PlatiPosle"
route_name: apps.plati_posle.settings
route_path: /admin/payment-providers/plati_posle
aliases: ["PlatiPosle", "Plati Posle", "Plati Posle Credissimo", "Plati Posle.bg", "Pay Later Credissimo", "Платипосле", "Credissimo", "Кредисимо"]
tags: [paymentproviders, payment-providers, plati-posle, credissimo, bnpl, installments, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 2
---
# PlatiPosle

## Purpose

**PlatiPosle** (Bulgarian for "Pay Later" — `platiposle.bg`) is Credissimo's online installment-loan payment method for Bulgarian merchants. The merchant signs a partner contract with Credissimo, gets an **API key** + **UUID** pair, enters them in this section of the CloudCart admin panel, and **PlatiPosle** becomes selectable on the storefront checkout. Customers pick a number of installments, redirect to PlatiPosle's hosted application page to fill the credit application, and on Credissimo's approval the merchant gets paid in full while the customer pays Credissimo back over the agreed months.

PlatiPosle uses **a single set of credentials** (no test-mode toggle — the integration is always live, `mode` forced to `live` on save). The minimum order amount is configurable (default 100 BGN). Refunds are NOT API-driven from CloudCart — they're handled out-of-band with Credissimo. This is a single-tab provider (Settings only): installment schemes are fetched live at checkout, and status updates arrive via a callback webhook CloudCart processes server-side.

## Where to find it

Sidebar → **Payment Providers** → click **PlatiPosle**. The route is `/admin/payment-providers/plati_posle` (route name `apps.plati_posle.settings`).

## What the merchant can do here

- See the overview card with the PlatiPosle logo + description + install/active toggle.
- Install / Uninstall the payment method through the standard buttons.
- Activate / deactivate via the header switch.
- Enter credentials:
  - **API Key** issued by PlatiPosle support.
  - **UUID** issued by PlatiPosle support (partner identifier).
  - **Minimum amount** below which PlatiPosle is hidden on storefront.
- Standard payment-provider fields:
  - Logo / Title / Description.
  - Discount.

## Settings & fields

### Credentials

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **API Key** | Credissimo-issued API key, sent in the `api-key` HTTP header on every PlatiPosle API call. | Empty | Required (server message: `"API Key is required"`). Must be at least 10 characters (`"API Key must be at least 10 characters"`). Multi-line text input. Placeholder: "Enter your API key from PlatiPosle". HelpBlock: "API key provided by PlatiPosle support". |
| **UUID** | Partner identifier issued by Credissimo for the merchant. Sent as `uuid` in the query string of every API call. | Empty | Required (server message: `"UUID is required"`). Must match UUID format (`"UUID format is invalid"`). Multi-line text input. Placeholder: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. |
| **Minimum amount** | Order total below which PlatiPosle is hidden on the storefront. | 100 BGN | Required (`"Minimum price is required"`). Numeric, ≥ 0 (`"Minimum price must be at least 0"`). Number input, step 0.01. Unit: the store's configured currency sign. HelpBlock: "Minimum order value required for PlatiPosle payment option (default: 100 BGN)". |

All three credential fields sit in a single card and are always visible — no conditional UI and no mode/test/live pill (the header status bar shows only the Active toggle).

### Standard payment-provider controls

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo / Title / Description** | Customer-facing label on checkout. | Provider defaults | Standard. |
| **Discount** | Optional checkout discount when customer picks PlatiPosle. | None | Standard. |

## Business rules

### How PlatiPosle works for the merchant

1. **Installment options at checkout** — when the customer reaches checkout, CloudCart asks Credissimo for the installment periods that apply to the cart total. Each option shows: name, monthly payment, GLP (yearly interest rate), GPR (APR), total amount due.
2. **Customer picks a plan** — selects the number of installments in the storefront module.
3. **Order registered with Credissimo** — CloudCart sends the customer's name, email, phone, the chosen installment count, shipping cost, the basket items, and a callback URL.
4. **Redirect to PlatiPosle** — the customer is sent to Credissimo's hosted application page to complete the credit form (identity, employment, etc.). The redirect URL renders responsively, so no separate mobile/desktop flag is needed.
5. **Status callbacks via webhook** — Credissimo posts status updates to the store's `payments.webhook` endpoint. CloudCart re-fetches the order's current status (using the stored `provider_reference_id`) and maps the provider statuses to CloudCart payment statuses:
   - `signed`, `paid` → COMPLETED.
   - `unfinished_contract`, `processing`, `waiting` → PENDING.
   - `cancelled`, `disapproved`, `discarded`, `denied` → CANCELED.
   - other → FAILED.
6. **On transition to COMPLETED**, CloudCart automatically sends the invoice via the standard invoicing flow used for any completed payment, and uploads it to Credissimo.

### Saved configuration

The saved settings hold `api_key`, `uuid`, `min_price`, and `mode`. `mode` is always forced to `live` on save — there is NO test-mode toggle exposed to the merchant, and Credissimo's PlatiPosle integration uses a single production environment.

### Connectivity validated on every save

On save, CloudCart immediately tests the new credentials by requesting installment periods for a 100 BGN order. If Credissimo returns an error, the form fails with the message attached to the **API Key** field — the merchant cannot save unusable credentials.

### Refund handling

PlatiPosle refunds are NOT exposed via the CloudCart admin — there is no refund call in the PlatiPosle integration. The merchant coordinates refunds with Credissimo via their portal.

### Initial / down payment

PlatiPosle's pricing API returns periods that may include built-in installment splits — the merchant doesn't configure a down-payment percentage in CloudCart. The customer's `installmentCount` (from the storefront module) is what's sent to Credissimo; the bank decides the resulting first-payment-at-checkout amount on their hosted page.

### Plan-gating

Not plan-gated by CloudCart subscription tier.

### Country + currency

BGN only, Bulgaria only. PlatiPosle is Credissimo's Bulgarian product; not used in other markets.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-dsk-bnpl]] — DSK Bank's BNPL (different bank, similar redirect-then-callback architecture).
- [[payment-providers-fibank-bnpl]] — Fibank's BNPL (different bank).
- [[payment-providers-klear]] — Klear Lending (another Bulgarian consumer-loan provider).
- [[payment-providers-iute]] — Iute Credit (multi-country consumer-loan).

## Open questions

- ⏸️ Supported installment count range (e.g., 2-24 months) is decided by Credissimo per merchant contract. The storefront module surfaces whatever Credissimo returns from the periods API; CloudCart does not enforce a min/max range.
