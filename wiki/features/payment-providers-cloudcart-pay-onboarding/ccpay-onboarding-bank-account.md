---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Bank account"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay payout IBAN", "External account", "Bank account on file", "Replace bank account", "BIC SWIFT", "Settlement currency"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, bank, iban, payouts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, KYB fields, documents, verification, status, connect/disconnect).

# Onboarding — Bank account

## Purpose

Step 6 of the onboarding wizard collects the **payout IBAN** — the external bank account where Paypercut will settle the merchant's card receipts via SEPA payout. The bank account is added as a Paypercut `external_account` of type `bank_account` and attached to the connected account.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab → **Bank** (step 6).

## What the merchant can do here

- Add a new payout IBAN with holder name, holder type, country, currency, IBAN, optional BIC / SWIFT.
- See the **Bank account on file** alert when an account is already configured.
- Click **Replace bank account** to dismiss the alert and open the new-IBAN form.
- Click **Cancel** to keep the existing IBAN without changes.

## Settings & fields

Backend: `POST /admin/cloudcart-pay/external-accounts` → Paypercut `POST /v1/accounts/{id}/external_accounts` with `external_account.object=bank_account`, `numbers.scheme=iban`.

| Field | Required? | What it does | Notes |
|-------|-----------|--------------|-------|
| **Account Holder Name** | Yes | Exact name as registered with the bank; must match the legal entity or representative. | Max 255. |
| **Holder Type** | Yes | `company` or `individual`. | |
| **Country** | Yes | 2-letter ISO country where the account is held. | |
| **Currency** | Yes | Settlement currency. Picked from `BGN, DKK, SEK, NOK, GBP, EUR, USD, CHF, CZK, HUF, PLN, RON`. | Determines the supported scheme. |
| **IBAN** | Yes | International Bank Account Number, up to 34 chars. | The backend strips all whitespace before sending. Validation message on failure: *"IBAN must be a valid IBAN."* |
| **BIC / SWIFT** | No | 8 or 11-character SWIFT/BIC identifier. | **Omitted from the API call entirely when blank** (sending an empty BIC makes Paypercut reject the IBAN scheme). |

The full Paypercut payload uses `numbers.scheme=iban`, `numbers.iban`, optional `numbers.bic`, plus `country`, `currency`, `holder_name`, `holder_type`, and optional `default_for_currency`.

Existing bank accounts are shown in a "Bank account on file" alert with a **Replace bank account** button — the merchant can dismiss the new form with **Cancel** to keep the existing IBAN.

## Business rules

### Whitespace is stripped from IBAN server-side

The backend strips all whitespace from the IBAN before sending it to Paypercut. Merchants who paste an IBAN like `BG80 BNBG 9661 1020 3456 78` get a clean `BG80BNBG96611020345678` on the platform. The IBAN's own validation runs against the cleaned value.

### Empty BIC is omitted, not sent as ""

If the BIC / SWIFT field is left blank, the backend omits `numbers.bic` from the API payload entirely. Sending `bic=""` makes Paypercut reject the IBAN scheme with a validation error. This is a quiet correctness fix — the merchant never sees the rejection because the field is properly skipped on serialise.

### Validation message for invalid IBAN

If the IBAN fails Paypercut's structural validation, the merchant sees verbatim: *"IBAN must be a valid IBAN."* No partial diagnostic about which character or country prefix is wrong is shown.

### Replace bank account — adds, doesn't update in place

Clicking *Replace bank account* opens the new-IBAN form; submitting it adds a new `external_account` to the connected account. Paypercut keeps the prior account in history; whether the prior account is automatically marked inactive on the platform side is a provider rule. (verify)

### Settlement currencies are fixed

The 12 settlement currencies in the picker (`BGN, DKK, SEK, NOK, GBP, EUR, USD, CHF, CZK, HUF, PLN, RON`) are the ones the platform supports. If the storefront's order currency is not on this list, the customer's order is rejected at checkout-session creation time on Paypercut's side — see [[payment-providers-cloudcart-pay]] for the currency handling.

### Step 6 completion criterion

Step 6 is marked complete when the connected account has ≥1 external account with an `id`, `last4`, or `holder_name` — see [[ccpay-onboarding-wizard-flow]]. The merchant cannot finish step 6 without successfully adding an IBAN.

### Payouts list lives on a separate sub-tab

This step only **adds** the bank account during onboarding. The standalone Payouts tab — [[payment-providers-cloudcart-pay-payouts]] — surfaces the payouts capability status, additional bank-account management actions, and the running payout schedule once the account is live.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — step completion mechanics.
- [[ccpay-onboarding-status-capabilities]] — step 7 where the `payouts` capability state is shown.
- [[payment-providers-cloudcart-pay-payouts]] — separate sub-tab for payouts lifecycle management.
- [[payment-providers-cloudcart-pay]] — currency handling end-to-end.

## Open questions

- ⏸️ Whether Paypercut automatically marks the prior external_account inactive when a new one is added via *Replace bank account*, or whether both stay active until the merchant explicitly designates a default. `(verify)`
