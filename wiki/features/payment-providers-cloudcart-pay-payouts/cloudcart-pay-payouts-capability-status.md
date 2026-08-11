---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Payouts → Capability status"
route_name: apps.cloudcart_pay.payouts
route_path: /admin/payment-providers/cloudcart_pay/payouts
aliases: ["Payouts enabled status", "Payouts capability pill", "Settlement currency CloudCart Pay", "Payouts disabled", "No bank accounts configured"]
tags: [paymentproviders, payment-providers, cloudcart-pay, payouts, capability, status]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-payouts]]. See the hub for the other aspects (bank-accounts table + form, schedule/limits).

# Payouts — capability status

## Purpose

This is the "is payouts working?" surface of the Payouts tab — the **Payout Status card** at the top. It answers the question merchants most often have after a busy sales day: are my settlements actually enabled, and which currency do they settle in? A single coloured pill plus the default-currency line give the answer at a glance, with a Refresh button to re-read the live state.

## Where to find it

Payment Providers → CloudCart Pay → **Payouts** tab → the **Payout Status** card at the top of the page.

## What the merchant can do here

- **Read the payouts capability** — a green "Enabled" or yellow "Disabled" pill.
- **Read the default settlement currency** of the connected account (e.g., EUR for an EU merchant) when it is set.
- **Refresh** the live status (and the bank-accounts list below) at any time.

## Settings & fields

### Payout Status card

| Block | What it shows |
|-------|---------------|
| **Payouts** pill | Green "Enabled" if `payouts_enabled` is `true` on the connected account; yellow "Disabled" otherwise. |
| **Default Currency** | The connected account's `default_currency` (typically `EUR` for EU merchants) — shown when set. |
| **Refresh** button | Re-fetches `GET /admin/cloudcart-pay/payouts`. |

## Business rules

### The payouts pill is conservative

The payouts pill follows `payouts_enabled === true` on the connected account — **not** the `capabilities.payouts` flag. Paypercut leaves `payouts_enabled` `false` (or `null`) until the platform fully finalises the account, even after the underlying capability flips to `active`. For the **Status step on the Onboarding wizard** ([[ccpay-onboarding-status-capabilities]]) the logic is intentionally looser (it accepts either signal); this Payouts page errs on the side of "treat enabled as a real platform commitment" and only shows green when `payouts_enabled` is truly `true`.

The practical consequence: a merchant can see "Disabled" here while the onboarding Status step still reads as progressing. When that happens, the merchant should check the Onboarding tab's status step for what is still required — often identity verification, additional documents, or a default bank account.

### "No bank accounts configured" state

If the external-accounts list is empty AND not loading, the page shows: *"No bank accounts configured."* The merchant should add one (see [[cloudcart-pay-payouts-bank-accounts]]) before payouts can run, even if the capability is otherwise active.

### "No account" state

If the upstream call returns 404 (no `connected_account_id`), the page shows: *"Please complete the onboarding process first."* — the same fallback as the Transactions tab ([[payment-providers-cloudcart-pay-transactions]]). The merchant has not started or finished onboarding, so there is nothing to read.

### Page is read live from the connected account

`GET /admin/cloudcart-pay/payouts` reads the connected account with its external accounts expanded inline. Nothing about the capability or bank accounts is mirrored to CloudCart's database — every load (and every Refresh click) is a fresh upstream read. Disconnecting and re-connecting, or switching to a different connected account, immediately changes what this card shows.

### Permission

The page is under `hasApiPermission:settings,store.payment_providers`. A staff member without that grant cannot reach the page or its API endpoints.

## Related

- [[payment-providers-cloudcart-pay-payouts]] — hub.
- [[ccpay-onboarding-status-capabilities]] — onboarding step 7, where the `payouts` capability state is shown with the looser accept-either-signal logic.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding wizard; complete it before payouts can be enabled.
- [[payment-providers-cloudcart-pay-transactions]] — same "complete onboarding first" fallback.
- [[payment-providers-cloudcart-pay]] — parent overview.

## Open questions

_None._
