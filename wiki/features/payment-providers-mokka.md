---
type: feature
nav_path: "Payment Providers → Mokka"
route_name: apps.mokka.settings
route_path: /admin/payment-providers/mokka
aliases: ["Mokka", "Mokka BNPL", "Mokka split-payment"]
tags: [paymentproviders, payment-providers, mokka, bnpl, installments, bulgaria, romania]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# Mokka

## Purpose

**Mokka** is a Bulgarian BNPL (Buy Now Pay Later) and consumer-credit provider, popular for splitting larger purchases into 2-12 monthly installments. Originally Bulgarian, Mokka also operates in Romania and Greece. The CloudCart integration adds Mokka as a checkout payment method — the customer picks Mokka, fills in a short application form (ID number, phone, employment basics), gets an instant decision from Mokka's underwriting API, and the merchant receives the full purchase amount upfront from Mokka (Mokka collects from the customer in installments).

Used by merchants selling higher-ticket items (electronics, furniture, appliances) who want to remove the price barrier — customers see "12 × 50 BGN/month" instead of "600 BGN".

## Where to find it

Sidebar → **Settings → Payment methods** → **Mokka** row → **Settings**.

The page's breadcrumb reads "Payment providers → Mokka". The route is `/admin/payment-providers/mokka`.

## What the merchant can do here

- Enter Mokka **store credentials** for live and test environments.
- Toggle the integration between test mode (Mokka sandbox) and live mode.
- Activate / deactivate Mokka at storefront checkout.
- Configure storefront display name + per-method min-order constraints via [[settings-payment-providers]] common fields.

What the merchant **cannot** do here:
- Change the installment plans / interest rates — those are configured on Mokka's side (per the merchant's contract).
- Approve or reject applications — Mokka's underwriting is fully automated and the merchant has no visibility into customer credit decisions.
- Issue refunds from CloudCart — refunds happen in Mokka's merchant portal; CloudCart's order is then manually marked refunded.

## Settings & fields

The integration requires THREE credentials per environment (live + test). The active environment is picked by the **Mode** toggle.

| Field | Required when | What it is |
|-------|---------------|------------|
| **Mode** | always | `live` / test (empty string `""`). |
| **Store ID** (`store_id` / `store_test_id`) | required for the active mode | Mokka merchant store identifier. |
| **Store Key** (`store_key` / `store_test_key`) | required for the active mode | Secret key Mokka issues to sign requests + verify callbacks. |
| **Store Endpoint** (`store_endpoint` / `store_test_endpoint`) | required for the active mode | Mokka's API base URL (production vs sandbox; the URL is country-specific). |

### Validation messages (exact strings)

- *"Store ID is required"* — when `store_id` (or `store_test_id` in test mode) is empty.
- *"Secret key is required"* — when `store_key` / `store_test_key` is empty.
- *"You have not entered an API base url"* — when `store_endpoint` / `store_test_endpoint` is empty.

So Mokka is one of the **simplest BNPL integrations to configure** — just three fields per environment.

## Business rules

### Live and test credentials co-exist on one row

Like other CloudCart payment providers, Mokka stores BOTH live and test credentials simultaneously. Toggling Mode changes which set is used at runtime; the merchant doesn't re-enter credentials when switching.

### Customer-side flow

1. At checkout, the customer picks Mokka and clicks Pay.
2. The platform creates a Mokka order via Mokka's API (sending order amount, customer email, phone, items).
3. The customer is redirected to Mokka's application form (hosted on Mokka).
4. The customer fills in their EGN (Bulgarian personal ID), employment info, and accepts terms.
5. Mokka returns an instant credit decision.
6. On approval → customer returns to CloudCart's success URL; the order is marked paid.
7. On rejection → customer returns to the cancel URL; the merchant sees a rejected order they can either retry with another payment method or cancel.

### Country-specific endpoints

The `store_endpoint` field lets the merchant point at country-specific Mokka APIs:
- Bulgaria — `mokka.bg` API.
- Romania — Mokka's Romanian endpoint.
- Greece — Mokka's Greek endpoint.

The endpoint is provided by Mokka during onboarding and the merchant pastes it as-is.

### Merchant-side payout

Mokka pays the FULL order amount to the merchant within Mokka's payout cycle (typically T+1 to T+3 business days). Mokka then collects from the customer in installments. The merchant carries NO credit risk — Mokka takes the risk in exchange for a per-transaction commission (negotiated in the merchant's contract).

### Refunds are Mokka-side

CloudCart doesn't expose a refund button for Mokka. The merchant issues a refund through Mokka's merchant portal; Mokka reverses the customer's installment plan; the merchant marks the CloudCart order as refunded manually via [[orders-payment-refund]].

### Permission

Standard payment-providers permission scope.

## Related

- [[settings-payment-providers]] — payment methods landing page.
- [[payment-providers]] — payment providers hub.
- [[orders-payment-mark-paid]] — order is marked paid on Mokka's success callback.
- [[orders-payment-refund]] — refunds are mirrored from Mokka portal.
- Other BNPL providers: [[payment-providers-dsk-bnpl]], [[payment-providers-fibank-bnpl]], [[payment-providers-iute]], [[payment-providers-klear]], [[payment-providers-tbi-bank]], [[payment-providers-fusion-pay]], [[payment-providers-plati-posle]].

## How it works

### Signed requests and verified callbacks

The integration signs every outgoing request to Mokka with the merchant's Store Key and verifies Mokka's response signature before accepting it — preventing tampered confirmations.

### Conditional credential validation

Each credential is required ONLY when its corresponding environment is selected. The merchant can save with just live credentials and switch to test later (but then must add test credentials before the integration works in test mode).

### Test mode is the "empty" mode

Test mode is identified internally by an empty mode value, not the literal string "test". When the merchant disables the live flag, the platform treats this as test environment.

### Same 3-field shape as other BNPL providers

The 3-field model (ID + key + endpoint) per environment is shared with several other BNPL integrations — it's the minimum information Mokka needs to identify the merchant and sign / verify each transaction.

## Open questions

- ⏸️ Number of installments available per country (e.g., BG 2-12 months vs Mokka-RO / Mokka-GR ranges) is defined on Mokka's side per merchant contract; CloudCart does not encode the per-country range.

## Verified — amount limits + iframe UX

- **Min / max order amounts**: NOT configured in CloudCart. The Mokka validator only requires per-environment Store ID / Secret Key / API base URL. There is no Mokka-specific amount-range field on the settings tab; the merchant can fall back to the standard provider Amount-from / Amount-to row if they want a CloudCart-side gate. Mokka itself enforces installment-amount limits server-side (typical BG market: 100 - 15 000 BGN), so any cart outside Mokka's contract limit is rejected at request time.
- **Customer application UX**: **iframe embed**, not a full redirect. The integration returns Mokka's `iframe_url` and CloudCart renders it inside an iframe on the checkout page. The customer fills the Mokka application without leaving the storefront.
