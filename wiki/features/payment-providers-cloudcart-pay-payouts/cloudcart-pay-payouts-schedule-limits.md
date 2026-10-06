---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Payouts → Schedule & limits"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["CloudCart Pay payout schedule", "When will I get paid CloudCart Pay", "Payout history", "Settlement currencies", "Delete bank account CloudCart Pay", "Кога се изплащат парите CloudCart Pay", "Поддържани валути за разплащане"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, schedule, currency]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-payouts]]. See the hub for the other aspects (payout status, bank accounts).

# Payouts — schedule & limits

## Purpose

What the Payouts tab does **not** do or show: no list of payouts, no payout schedule to change, no editing or deleting of bank accounts. It also lists the settlement currencies and the one currency difference with the onboarding. The page exists so support can answer "when will the money arrive?" and "where is my payout list?" without promising controls that are not there.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Payouts** tab. The limits apply to the whole tab; the only related element on screen is **Supported Settlement Currencies** (Поддържани валути за разплащане) at the bottom.

## What the merchant can do here

- **Read the supported settlement currencies** and the account's default currency.
- The merchant **cannot**: see a list of payouts, change how often payouts happen, trigger a payout, set a minimum balance, edit or delete a bank account, or change the default on an existing row.

## Settings & fields

**Supported Settlement Currencies** — a read-only row: **EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON**.

There are no schedule or limit fields.

## Business rules

### No payout list

The tab shows no history of individual payouts (date, amount, status, target account). A payout that fails, for example because of a bank rejection, is not shown here either. For the money taken and refunded per period, the [[cloudcart-pay-transactions-totals|Transactions totals]] give captured, refunded, fees and net.

### No schedule controls

Payout timing is not configured in CloudCart: there is no cadence picker, manual payout or minimum balance. The agreement accepted during onboarding governs payouts and allows chargebacks, fees and penalties to be deducted from the money being paid out ([[cloudcart-pay-merchant-terms]]).

### Existing bank accounts are view-only

Adding is the only change possible. To make another account the default for a currency, add it with **Set as default payout account for its currency** ticked ([[cloudcart-pay-payouts-bank-accounts]]). Removing or editing an account is not available on the tab.

### BGN only in onboarding

Onboarding step 6 offers **BGN** among its currencies ([[ccpay-onboarding-bank-account]]); the Payouts tab's form and the **Supported Settlement Currencies** list do not. Both forms start at EUR.

## Related

- [[payment-providers-cloudcart-pay-payouts]] — hub.
- [[cloudcart-pay-payouts-bank-accounts]] — adding accounts and the default per currency.
- [[ccpay-onboarding-bank-account]] — onboarding step 6.
- [[cloudcart-pay-transactions-totals]] — totals per period.
- [[cloudcart-pay-merchant-terms]] — deductions from payouts.
- [[multi-currency]] — store currencies.

## Open questions

- How often payouts are made and how long after a payment the money arrives.
- Whether, and how, the merchant is told about a failed payout.
- How a bank account is removed or corrected (likely through support).
- Whether payouts in BGN are possible, given that BGN is offered only in onboarding.
