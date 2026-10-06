---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Payouts"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["CloudCart Pay payouts", "Bank accounts CloudCart Pay", "Settlement bank account", "Payout status CloudCart Pay", "Изплащания CloudCart Pay", "Банкови сметки CloudCart Pay", "Статус на изплащането"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, bank-account]
plan_gates: []
created: 2026-05-21
updated: 2026-10-06
source_count: 2
---
# CloudCart Pay — Payouts

## Purpose

The **Payouts** tab (Изплащания) answers "are my payouts working, and where does the money go?". It shows whether payouts are enabled on the connected account and its default currency, lists the bank accounts on file, and lets the merchant add another bank account without going back through the onboarding. Everything is read live from the connected account; nothing about bank accounts is stored in the store.

The tab does **not** list individual payouts, does not let the merchant change the payout schedule, and does not edit or delete bank accounts — see [[cloudcart-pay-payouts-schedule-limits]].

## Sub-pages (in this cluster)

- [[cloudcart-pay-payouts-capability-status]] — the **Payout Status** card: **Enabled** / **Disabled**, the default currency, the empty states.
- [[cloudcart-pay-payouts-bank-accounts]] — the **Bank Accounts** table and the **Add Bank Account** form, including the default account per currency.
- [[cloudcart-pay-payouts-schedule-limits]] — what the tab does not do, settlement currencies, open points about timing.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Payouts** tab. Address: `/admin/payment-providers/cloudcart_pay/payouts`.

## What the merchant can do here

- **See whether payouts are enabled** and the default currency — [[cloudcart-pay-payouts-capability-status]].
- **See the bank accounts on file** with holder, type, masked number, country, currency, bank and a **Default** badge — [[cloudcart-pay-payouts-bank-accounts]].
- **Add a bank account** (IBAN) and make it the default for its currency.
- **See the supported settlement currencies.**
- **Refresh** the status.

## Settings & fields

- **Payout Status** (Статус на изплащането): **Payouts** — **Enabled** / **Disabled**; **Default Currency** (Валута по подразбиране); **Refresh**.
- **Bank Accounts** (Банкови сметки): table, and **Add Bank Account** (Добавяне на банкова сметка) / **Cancel**.
- **Add Bank Account** form: Account Holder Name, Holder Type, Country, Currency, IBAN, BIC / SWIFT, **Set as default payout account for its currency**.
- **Supported Settlement Currencies** (Поддържани валути за разплащане): EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON.

## Business rules

- **Payouts read Enabled** when payouts are active on the account — the same rule as the **Payouts** card on the onboarding **Status** step, so the two always agree. See [[cloudcart-pay-payouts-capability-status]].
- **Adding an account works like onboarding step 6**: spaces in the IBAN are removed, a blank BIC is left out, and a refusal appears under the IBAN or BIC field. See [[cloudcart-pay-payouts-bank-accounts]].
- **Live data.** Each load reads the connected account; after linking another account the tab shows that account's bank accounts.
- **Payout timing is not set here.** There is no schedule, no manual payout and no payout history on this tab ([[cloudcart-pay-payouts-schedule-limits]]).
- **Deductions.** Chargebacks and related costs can be deducted from the money being paid out under the agreement ([[cloudcart-pay-merchant-terms]]).
- **No account.** Without a connected account the tab shows *"Please complete the onboarding process first."*
- **Staff access** needs the permission for the store's payment methods settings ([[settings-staff]]).

## Related

- [[payment-providers-cloudcart-pay]] — CloudCart Pay hub.
- [[ccpay-onboarding-bank-account]] — the first bank account, added in onboarding step 6.
- [[ccpay-onboarding-status-capabilities]] — the same Payouts status in onboarding.
- [[payment-providers-cloudcart-pay-transactions]] — the payments behind the payouts.
- [[cloudcart-pay-transactions-totals]] — totals and net per period.
- [[cloudcart-pay-merchant-terms]] — deductions from payouts.
- [[multi-currency]] — store currencies.

## Open questions

- How often and how long after a payment the money is paid out (not shown in CloudCart).
