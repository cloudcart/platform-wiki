---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Payouts → Bank accounts"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["CloudCart Pay bank accounts", "Add bank account payouts", "External account IBAN", "Default for currency", "Settlement bank account list"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, bank-account, iban]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-payouts]]. See the hub for the other aspects (capability status, schedule/limits).

# Payouts — bank accounts

## Purpose

This is the bank-account management half of the Payouts tab: the **Bank Accounts table** listing the IBAN accounts on file, and the inline **Add Bank Account** form for registering a new one without re-running the onboarding wizard. Each connected account has one or more **external accounts** (IBAN-based bank accounts) registered for payouts; this surface shows them and lets the merchant add more.

## Where to find it

Payment Providers → CloudCart Pay → **Payouts** tab → the **Bank Accounts** table and the **Add Bank Account** button below the Payout Status card.

## What the merchant can do here

- **See the list of bank accounts on file**, with holder name, type, masked account / last 4, country, currency, bank name, and a "Default" badge on the default-for-currency account.
- **Add a new bank account** through the inline form — IBAN-only (scheme = `iban`).
- **Mark the new account as default for its currency** with a checkbox.
- **Cancel** the form to collapse it without adding anything.

(Editing or deleting an existing account is not exposed yet — see [[cloudcart-pay-payouts-schedule-limits]].)

## Settings & fields

### Bank Accounts table

| Column | What it shows | Notes |
|--------|---------------|-------|
| Holder | `holder_name` (or legacy `account_holder_name`). | |
| Type | `holder_type`: `company` or `individual`. | |
| Account | Full `account_number` if returned (rare — typically masked); otherwise `•••• <last4>`. | Paypercut returns the IBAN masked for security after creation. |
| Country | Two-letter ISO code where the account is held. | |
| Currency | Settlement currency, upper-cased. | |
| Bank | `bank_name` if Paypercut can resolve it from the IBAN; `-` otherwise. | |
| Default | "Default" badge on the row that is `default_for_currency=true`. | |

### Add Bank Account form

Shown after clicking **Add Bank Account** (collapses when **Cancel** is clicked).

| Field | Required? | What it does | Notes |
|-------|-----------|--------------|-------|
| **Account Holder Name** | Yes | Name as registered with the bank. | Max 255. Should match the legal entity or the representative. |
| **Holder Type** | Yes | `company` or `individual`. | |
| **Country** | Yes | Two-letter ISO country code; picked from a 30-country EEA+CH+GB+NO list. | |
| **Currency** | Yes | Settlement currency; default `EUR`. Picked from `EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON`. | |
| **IBAN** | Yes | International Bank Account Number, up to 34 chars. Whitespace is stripped server-side. | |
| **BIC / SWIFT** | No | 8 or 11-character SWIFT/BIC identifier. **Omitted from the API call when blank** — sending an empty BIC makes Paypercut reject the IBAN scheme branch with misleading errors. | |
| **Set as default payout account for its currency** | No | Checkbox. Sets `default_for_currency=true` on the new external account. | Helper text: "The first account added for a currency is the default automatically." |
| **Add Bank Account** button | n/a | Submits the form. Disabled until Holder Name and IBAN are populated. | |

The form maps Paypercut field-level errors (`{ code, message, param: "numbers.iban", ... }`) back to the matching input — for example, an invalid IBAN renders as a red border on the IBAN field with the provider's message, instead of a generic banner.

## Business rules

### Page is read live from the connected account

`GET /admin/cloudcart-pay/payouts` calls `getConnectedAccount($accountId, ['external_accounts'])` on the Paypercut Accounts API with the `expand=external_accounts` query parameter — the bank accounts are returned inline with the account object. The controller flattens Paypercut's nested response (each item is `{ external_account: {...}, default_for_currency: bool }`) into a list of flat objects the UI can render directly.

Nothing about bank accounts is mirrored to CloudCart's database — every load is a fresh upstream read. Disconnecting and re-connecting (or switching to a different connected account) immediately changes what this page shows.

### Adding a bank account uses the same endpoint as onboarding step 6

The inline form POSTs to `/admin/cloudcart-pay/external-accounts` — the same endpoint as the wizard's bank step. Validation rules and field semantics are identical (see [[ccpay-onboarding-bank-account]]). The backend:

1. Validates the payload: `external_account.object=bank_account`, `country` (size 2), `currency` (size 3), `holder_name` (max 255), `holder_type` in `company,individual`, `numbers.scheme=iban`, `numbers.iban` (max 34), optional `numbers.bic` (max 11), optional `default_for_currency` (boolean).
2. **Strips whitespace from the IBAN** before sending (`preg_replace('/\s+/', '', ...)`). A pasted `BG80 BNBG 9661 1020 3456 78` is cleaned to `BG80BNBG96611020345678` before validation runs.
3. **Omits BIC entirely when empty** — sending `bic: ""` or `bic: null` makes Paypercut reject the IBAN branch of the `oneOf` external-account scheme and surface confusing aba / sort_code / eft errors. Leaving BIC blank is therefore safe; the merchant never sees the spurious rejection.
4. Forwards the payload to Paypercut's `POST /v1/accounts/{id}/external_accounts` with the `Paypercut-Account` header.
5. On 4xx, the field-level error (with `param`) is returned to the UI which binds it to the matching input — for example, `param=numbers.iban` renders a red border on the IBAN field.

After success, the page re-fetches itself and displays the new account in the list.

### Default-for-currency rule

When `default_for_currency=true` is sent on a new account creation:

- If no other account exists for that currency yet, the new account becomes the default automatically (this is Paypercut's default behaviour for the first account per currency — the form helper text reflects this).
- If another account already holds the default for that currency, the platform transfers the default flag to the newly created account.

The helper text under the checkbox reads: *"The first account added for a currency is the default automatically."* Because there is no explicit "set default" action on the existing rows, **changing the default for a currency is done implicitly by creating a new account with the checkbox ticked** — see [[cloudcart-pay-payouts-schedule-limits]] for the view-only nature of existing rows.

## Related

- [[payment-providers-cloudcart-pay-payouts]] — hub.
- [[ccpay-onboarding-bank-account]] — onboarding step 6 bank-account form; same endpoint and identical validation.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding wizard adds the first bank account.
- [[payment-providers-cloudcart-pay]] — parent overview and end-to-end currency handling.
- [[multi-currency]] — how store currencies relate to payout settlement currencies.

## Open questions

_None._
