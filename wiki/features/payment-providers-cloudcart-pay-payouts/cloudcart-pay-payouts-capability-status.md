---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Payouts → Payout status"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["Payouts enabled status", "Payouts Disabled CloudCart Pay", "Payout Status card", "Default settlement currency", "No bank accounts configured", "Изплащанията са изключени", "Статус на изплащането"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, capability, status]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-payouts]]. See the hub for the other aspects (bank accounts, schedule and limits).

# Payouts — payout status

## Purpose

The **Payout Status** card at the top of the Payouts tab: one badge that says whether payouts are enabled on the connected account, and the account's default currency. It is the merchant's quick answer to "can CloudCart Pay pay me out yet?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Payouts** tab → **Payout Status** (Статус на изплащането), at the top.

## What the merchant can do here

- **Read the payouts badge**: **Enabled** or **Disabled**.
- **Read the default currency** of the account, when it has one.
- **Refresh** the card and the bank accounts below it.

## Settings & fields

| Element | What it shows |
|---|---|
| **Payouts** badge | Green **Enabled** when payouts are active on the account; amber **Disabled** otherwise. |
| **Default Currency** (Валута по подразбиране) | The account's default currency, e.g. EUR — shown when set. |
| **Refresh** (Обнови) | Reads the account again. |

## Business rules

### When the badge reads Enabled

The badge reads **Enabled** when the account reports payouts as enabled **or** its payouts capability is active. The account can take some time to report payouts as fully enabled after the capability has been granted; counting the capability keeps the badge accurate in the meantime. The **Payouts** card on the onboarding **Status** step uses the same rule, so the two screens always show the same answer ([[ccpay-onboarding-status-capabilities]]).

When it reads **Disabled**, the onboarding **Status** step shows what is still needed — often a document, the identity verification or the bank account. Approval of a new account takes from a few hours to 2 business days after submission, longer for a complicated company structure (operator statement; see [[ccpay-onboarding-review-alerts]]). A change in the payouts status also arrives as an admin notification and an email.

### "No bank accounts configured."

When the account has no bank account, the **Bank Accounts** section shows *"No bank accounts configured."* (Няма конфигурирани банкови сметки.). A bank account is needed for payouts; it is added in onboarding step 6 or here with **Add Bank Account** ([[cloudcart-pay-payouts-bank-accounts]]).

### No account

Without a connected account the card shows *"Please complete the onboarding process first."* (Моля, първо завършете процеса на регистрация.) — the same as the Transactions tab.

### Live reading

The card is read live from the connected account each time the tab opens or **Refresh** is clicked; nothing is stored in the store.

### Staff access

Available only to staff whose role allows the store's payment methods settings ([[settings-staff]]).

## Related

- [[payment-providers-cloudcart-pay-payouts]] — hub.
- [[ccpay-onboarding-status-capabilities]] — the Payments and Payouts cards in onboarding.
- [[ccpay-onboarding-review-alerts]] — approval time and alerts.
- [[cloudcart-pay-payouts-bank-accounts]] — bank accounts.
- [[payment-providers-cloudcart-pay-transactions]] — same "complete onboarding first" state.

## Open questions

(none)
