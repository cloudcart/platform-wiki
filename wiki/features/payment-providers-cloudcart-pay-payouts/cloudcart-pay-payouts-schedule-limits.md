---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Payouts → Schedule & limits"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["CloudCart Pay payout schedule", "SEPA settlement schedule", "Payout history", "BGN settlement currency", "Payout cadence"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, schedule, sepa, currency]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-payouts]]. See the hub for the other aspects (capability status, bank-accounts table + form).

# Payouts — schedule & limits

## Purpose

This aspect documents what the Payouts tab does **not** control and does **not** yet show: the platform-managed SEPA settlement schedule, failed-payout handling, the BGN store-vs-payout-currency distinction, and the missing per-payout history. It exists so support can answer "when will the money arrive?" and "where is my payout list?" without implying the page offers controls it doesn't have.

## Where to find it

Payment Providers → CloudCart Pay → **Payouts** tab. These are scope boundaries of the whole tab rather than a single on-screen block, so there is nothing extra to click — the absence of controls is the point.

## What the merchant can do here

- **Read** the supported settlement currencies (a pill row) and the default settlement currency.
- The merchant **cannot** change the payout cadence, trigger a manual payout, set a minimum balance, view a per-payout history, or delete / edit an existing bank account from this page.

## Settings & fields

There are no editable schedule or limit fields on this page. The only read-only schedule-relevant element is the **Supported Settlement Currencies** block — a row of pills showing what CloudCart Pay can settle into: **EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON**.

## Business rules

### SEPA settlement schedule — platform-managed

Paypercut handles payout scheduling (typically T+2 to T+5 SEPA transfers from the connected-account balance to the registered IBAN). The merchant **cannot configure schedule** from this page — no cadence picker, no manual-payout trigger, no minimum-balance setting. This is by design — Paypercut's commercial agreement governs the cadence.

### Failed payout retry — not surfaced

There is no per-payout list, so failed payouts (e.g., IBAN issue, bank rejection) are not visible here today. Paypercut handles retries platform-side; merchants are notified via email or in-platform notifications outside this page.

### BGN handling: store vs payout currency

CloudCart's storefront supports BGN-denominated orders (see [[multi-currency]]). The Onboarding wizard's step 6 includes `BGN` in its currency picker so Bulgarian merchants can register their BGN bank account during onboarding — see [[ccpay-onboarding-bank-account]]. The Payouts tab's *Add Bank Account* form, however, lists only the 11 currencies CloudCart Pay actively settles in (`EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON`).

This is a deliberate distinction: Bulgarian merchants typically register a BGN account during onboarding for storage / verification, but settlement happens in EUR for now. Whether BGN settlement reaches the roadmap is an open question. `(verify)`

### What this page does NOT yet show

- **No per-payout event list** — there is no "Payout history" table showing the individual SEPA transfers the platform has sent (date, amount, status, target bank account). Paypercut has the API surface, but it isn't wired into this page yet.
- **No payout-schedule controls** — payout cadence (e.g., daily / weekly, T+2 vs T+5) is platform-managed; the merchant cannot change it from this page.
- **No bank-account delete / set-default actions** — the table is view-only for existing accounts. Adding a new account is the only mutating action; changing the default for a currency is done implicitly by creating a new account with `default_for_currency=true` (see [[cloudcart-pay-payouts-bank-accounts]]). Removing or editing an existing account is not exposed yet.

## Related

- [[payment-providers-cloudcart-pay-payouts]] — hub.
- [[cloudcart-pay-payouts-bank-accounts]] — where the Add Bank Account form and default-for-currency rule live.
- [[ccpay-onboarding-bank-account]] — onboarding step 6, whose picker includes BGN.
- [[multi-currency]] — store-currency vs settlement-currency handling.
- [[payment-providers-cloudcart-pay]] — parent overview.

## Open questions

- ⏸️ Whether BGN settlement (not just BGN account storage) is on the CloudCart Pay roadmap, or whether Bulgarian merchants will continue to settle in EUR indefinitely. `(verify)`
