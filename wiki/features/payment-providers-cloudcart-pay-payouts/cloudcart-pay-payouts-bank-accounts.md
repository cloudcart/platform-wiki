---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Payouts → Bank accounts"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["CloudCart Pay bank accounts", "Add bank account payouts", "Default payout account", "Set as default payout account for its currency", "Change payout IBAN", "Добавяне на банкова сметка", "Банкови сметки CloudCart Pay", "Смяна на IBAN за изплащания"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, bank-account, iban]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-payouts]]. See the hub for the other aspects (payout status, schedule and limits).

# Payouts — bank accounts

## Purpose

The bank-account half of the Payouts tab: the **Bank Accounts** table of IBAN accounts the connected account can be paid out to, and the **Add Bank Account** form for adding another one without re-running the onboarding — including making it the default payout account for its currency.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Payouts** tab → **Bank Accounts** (Банкови сметки). The **Add Bank Account** button (Добавяне на банкова сметка) is at the right of the section title and turns into **Cancel** while the form is open.

## What the merchant can do here

- **See the bank accounts on file** and which one is the default for each currency.
- **Add a bank account** (IBAN only).
- **Make the new account the default** for its currency.
- **Cancel** to close the form without adding anything.

Existing accounts cannot be edited or deleted here — see [[cloudcart-pay-payouts-schedule-limits]].

## Settings & fields

### Bank Accounts table

| Column | What it shows |
|---|---|
| **Holder** (Титуляр) | Account holder name. |
| **Type** | Company or individual. |
| **Account** | The number as returned, normally masked: "•••• 1234". |
| **Country** | Country code where the account is held. |
| **Currency** | Payout currency. |
| **Bank** | Bank name when the account reports one; "-" otherwise. |
| **Default** | A **Default** badge on the default account for its currency. |

### Add Bank Account form

| Field | Required | Notes |
|---|---|---|
| **Account Holder Name** (Име на титуляря на сметката) | Yes | As registered with the bank; should match the company or the representative. Up to 255 characters. |
| **Holder Type** (Тип титуляр) | Yes | **Company** or **Individual**; starts at Company. |
| **Country** (Държава) | Yes | 30 European countries. |
| **Currency** (Валута) | Yes | EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON; starts at EUR. |
| **IBAN** | Yes | Up to 34 characters; spaces are removed. |
| **BIC / SWIFT** | No | 8 or 11 characters. |
| **Set as default payout account for its currency** (Задаване като сметка по подразбиране за изплащания за съответната валута) | No | Help: *"The first account added for a currency is the default automatically."* |

**Add Bank Account** stays disabled until **Account Holder Name** and **IBAN** are filled.

## Business rules

### Same rules as onboarding step 6

The form submits the bank account to the connected account exactly as onboarding step 6 does ([[ccpay-onboarding-bank-account]]):

- spaces in the IBAN are removed, so an IBAN pasted in groups is fine;
- a blank **BIC / SWIFT** is left out and never causes the IBAN to be refused;
- a refusal about the IBAN or the BIC appears under that field; other refusals appear above the button.

After a successful add, the form closes and the list reloads with the new account.

### Default account per currency

- The **first** account added for a currency becomes that currency's default automatically.
- Ticking **Set as default payout account for its currency** makes the new account the default, in place of the previous one.
- There is no "make default" action on existing rows, so changing the default for a currency means adding the new account with the box ticked.

### Read live

The table is read live from the connected account each time; nothing about bank accounts is stored in the store. After the store links another account, the table shows that account's bank accounts.

### Currencies

The form offers 11 currencies, the same as the **Supported Settlement Currencies** list. Onboarding step 6 additionally offers BGN — see [[cloudcart-pay-payouts-schedule-limits]].

## Related

- [[payment-providers-cloudcart-pay-payouts]] — hub.
- [[ccpay-onboarding-bank-account]] — onboarding step 6, the same form.
- [[cloudcart-pay-payouts-capability-status]] — whether payouts are enabled.
- [[cloudcart-pay-payouts-schedule-limits]] — what this tab does not do.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding.

## Open questions

- What happens to payouts in a currency that has no bank account in that currency.
