---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Payouts"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["CloudCart Pay payouts", "Bank accounts CloudCart Pay", "Settlement bank account", "External account", "Изплащане", "Банкови сметки CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, bank-account]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---
# Payouts

## Purpose

The **Payouts** tab is where the merchant manages the bank accounts that CloudCart Pay settles money into, and checks whether settlements are actually enabled on the connected account. It is the merchant's everyday answer to "are my payouts working, and where is the money going?".

The page does three jobs: it shows a single capability pill ("are settlements enabled?"), it lists the bank accounts on file, and it lets the merchant add a new bank account inline without re-running the onboarding wizard. Everything is read **live** from the payment provider (Paypercut) — nothing about bank accounts is stored in CloudCart's own database.

This page does NOT show **individual payout events** (the actual money transfers), does NOT let the merchant change the payout schedule, and does NOT yet allow deleting or editing existing accounts. Those scope boundaries — plus the BGN settlement nuance — are documented in [[cloudcart-pay-payouts-schedule-limits]].

This is a hub page. The Payouts tab spans three well-scoped aspects; drill into the one that matches the question rather than reading all three.

## Sub-pages (in this cluster)

- [[cloudcart-pay-payouts-capability-status]] — the "Enabled / Disabled" payouts pill (why it is conservative vs the capability flag), the default settlement currency, the "No account" and "No bank accounts configured" empty states, and the page permission.
- [[cloudcart-pay-payouts-bank-accounts]] — the bank-accounts table columns, the inline **Add Bank Account** form (fields, IBAN whitespace stripping, empty-BIC omission), and the default-for-currency rule.
- [[cloudcart-pay-payouts-schedule-limits]] — the platform-managed SEPA settlement schedule, failed-payout handling, the BGN store-vs-payout-currency discrepancy, and the list of features this page does not yet expose.

## Where to find it

Payment Providers → CloudCart Pay → **Payouts** tab. The route is `/admin/payment-providers/cloudcart_pay/payouts`.

## What the merchant can do here

- **See the payouts capability status** — a green "Enabled" or yellow "Disabled" pill. See [[cloudcart-pay-payouts-capability-status]].
- **See the default settlement currency** of the connected account (e.g., EUR for an EU merchant).
- **See the list of bank accounts on file** with holder, type, masked account, country, currency, bank name, and a "Default" badge. See [[cloudcart-pay-payouts-bank-accounts]].
- **Refresh** the list at any time.
- **Add a new bank account** inline (IBAN-only) and optionally mark it default for its currency. See [[cloudcart-pay-payouts-bank-accounts]].
- **See the supported settlement currencies** in a read-only pill row: `EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON`.

## Settings & fields

The detailed field tables live on the aspect pages:

- **Payout Status card** (capability pill, default currency, Refresh button) — see [[cloudcart-pay-payouts-capability-status]].
- **Bank Accounts table** + **Add Bank Account form** (holder name, holder type, country, currency, IBAN, optional BIC, default-for-currency checkbox) — see [[cloudcart-pay-payouts-bank-accounts]].
- **Supported Settlement Currencies block** — a read-only row of currency pills: `EUR, USD, DKK, SEK, NOK, GBP, CHF, CZK, HUF, PLN, RON`. (The onboarding wizard's step 6 picker additionally includes `BGN` — see [[cloudcart-pay-payouts-schedule-limits]] for the store-vs-payout-currency distinction.)

## Business rules

- **The page reads live from the connected account** — `GET /admin/cloudcart-pay/payouts` fetches the account with its external accounts expanded inline. Nothing is mirrored to CloudCart's database; disconnecting/reconnecting immediately changes what this page shows. See [[cloudcart-pay-payouts-bank-accounts]].
- **The capability pill is conservative** — it shows green only when `payouts_enabled === true`, not when the looser `capabilities.payouts` flag is active. See [[cloudcart-pay-payouts-capability-status]].
- **Adding a bank account uses the same endpoint as onboarding step 6** — identical validation; IBAN whitespace is stripped and empty BIC is omitted. See [[cloudcart-pay-payouts-bank-accounts]] and [[ccpay-onboarding-bank-account]].
- **The payout schedule is platform-managed** — no cadence picker, no manual-payout trigger; SEPA settlement timing is governed by Paypercut. See [[cloudcart-pay-payouts-schedule-limits]].
- **The page is permission-gated** under `hasApiPermission:settings,store.payment_providers`. See [[cloudcart-pay-payouts-capability-status]].

## Related

- [[payment-providers-cloudcart-pay]] — parent overview.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding wizard; step 6 adds the first bank account.
- [[ccpay-onboarding-bank-account]] — onboarding step 6 bank-account form (same endpoint as the inline form here).
- [[payment-providers-cloudcart-pay-transactions]] — the charges that aggregate into each payout.
- [[payment-providers-cloudcart-pay-settings]] — the parent settings tab.
- [[settings-payment-providers]] — global payment-providers list.
- [[payment-provider]] — entity definition.
- [[multi-currency]] — how store currencies interact with payout settlement currencies.

## Open questions

_None._
