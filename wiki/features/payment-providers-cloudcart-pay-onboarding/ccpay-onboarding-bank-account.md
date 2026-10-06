---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Bank account"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay payout IBAN", "Bank account on file", "Replace bank account", "BIC SWIFT CloudCart Pay", "Settlement currency onboarding", "Банкова сметка CloudCart Pay", "Налична банкова сметка", "Замяна на банкова сметка"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, bank, iban, payouts]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, status, review and alerts, connect/disconnect).

# Onboarding — Bank account (step 6)

## Purpose

Step 6 adds the **payout bank account** — the IBAN to which CloudCart Pay pays out the merchant's card takings. Later bank accounts are added and managed on the [[payment-providers-cloudcart-pay-payouts|Payouts tab]].

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab → step 6, **Bank** (Банка); screen title **Bank Account** (Банкова сметка).

## What the merchant can do here

- **Add the payout IBAN** with holder name, holder type, country, currency and an optional BIC / SWIFT.
- **See the bank account already on file**.
- **Replace bank account** to enter a different one, or **Cancel** to keep the current one.

## Settings & fields

### Bank account on file (Налична банкова сметка)

When an account is already saved, the step shows the holder name with a badge such as "EUR · BG" (currency and country), the bank name and the account number ending (•••• 1234), or a **Submitted** badge. Text: *"Bank account is saved with CloudCart. Click Continue to proceed, or "Replace bank account" to enter new details."* Buttons: **Replace bank account** (Замяна на банкова сметка) or **Cancel** (Отказ).

### The form

| Field | Required | Notes / help text |
|---|---|---|
| **Account Holder Name** (Име на титуляря на сметката) | Yes | *"Name exactly as registered with the bank. Must match the legal entity or the representative."* Up to 255 characters. |
| **Holder Type** (Тип титуляр) | Yes | **Company** or **Individual** (Физическо лице). *"Whether the bank account belongs to the legal entity or an individual."* |
| **Country** (Държава) | Yes | *"Country where the bank account is held."* Same 30 countries as step 1. |
| **Currency** (Валута) | Yes | *"Currency in which payouts will be settled to this account."* BGN, DKK, SEK, NOK, GBP, EUR, USD, CHF, CZK, HUF, PLN, RON. Starts at EUR. |
| **IBAN** | Yes | *"International Bank Account Number, no spaces. Up to 34 characters."* |
| **BIC / SWIFT** | No | *"8 or 11-character SWIFT/BIC identifier. Optional if the IBAN is sufficient for routing."* |

Buttons: **Back** (Назад) and **Save & Continue** (Запазване и продължаване), or **Continue** when an account is on file and not being replaced.

## Business rules

### Spaces in the IBAN are fine

Spaces are removed before the IBAN is sent, so an IBAN pasted as "BG80 BNBG 9661 1020 3456 78" is saved as one string. The IBAN can still be at most 34 characters.

### BIC can stay empty

A blank BIC / SWIFT is simply left out; it never causes the IBAN to be refused.

### Errors appear on the field

When the IBAN or the BIC is refused, the reason appears under that field rather than as a general error. Other refusals appear under the form.

### Replace bank account adds a new account

Replacing submits a new bank account to the connected account; the earlier one stays listed on the [[payment-providers-cloudcart-pay-payouts|Payouts tab]]. The first account added for a currency becomes that currency's default payout account; the default can be set when adding an account on the Payouts tab — see [[cloudcart-pay-payouts-bank-accounts]].

### Currencies here and on the Payouts tab

The currency list in this step includes **BGN**; the Payouts tab's form and its **Supported Settlement Currencies** list do not. See [[cloudcart-pay-payouts-schedule-limits]].

### When step 6 counts as done

When the connected account has a bank account. The step cannot be finished without one.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[payment-providers-cloudcart-pay-payouts]] — payouts and later bank accounts.
- [[cloudcart-pay-payouts-bank-accounts]] — the bank accounts table and the default per currency.
- [[cloudcart-pay-payouts-schedule-limits]] — settlement currencies.
- [[ccpay-onboarding-status-capabilities]] — the Payouts status after onboarding.
- [[ccpay-onboarding-wizard-flow]] — when steps count as done.

## Open questions

- Whether an earlier bank account stays in use for payouts after **Replace bank account**, or stops once a new default exists.
- Whether payouts in BGN are possible, given that BGN is offered only in this step.
