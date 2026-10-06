---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Wizard flow"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay onboarding wizard", "7-step onboarding", "Onboarding step indicator", "Resume onboarding", "Deep-link step", "Set up your CloudCart Connect account", "Стъпки на регистрацията CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, wizard]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (fields, people, documents, verification, bank, status, review and alerts, connect/disconnect).

# Onboarding — wizard flow

## Purpose

How the onboarding wizard itself behaves: the first screen, the seven-step indicator, moving between steps, resuming after the browser was closed, opening a step directly, and when a step counts as done. The fields of each step are on the step pages.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab. A step can be opened directly by adding `?step=1` … `?step=7` to `/admin/payment-providers/cloudcart_pay/onboarding`.

## What the merchant can do here

- **Start** a new account or **link** an existing one from the first screen.
- **Move between steps** with the step indicator and the **Back** / **Continue** buttons.
- **Come back later** and land on the first step that is not done yet.
- **Open the Status step at any time.**

## Settings & fields

### First screen (no account yet)

Title **Set up your CloudCart Connect account** (Настройте своя CloudCart Connect акаунт), text *"Create a connected business account to accept payments and receive payouts through CloudCart Pay, or link an existing CloudCart account."* Two buttons: **Start Onboarding** (Започване на регистрацията) and **Connect Existing Account** (Свързване със съществуващ акаунт) — see [[ccpay-onboarding-connect-disconnect]].

### Step indicator

Seven steps: **Profile, Business, Representative, Documents, Verification, Bank, Status** (Профил, Бизнес, Представител, Документи, Верификация, Банка, Статус).

| What the merchant sees | Meaning |
|---|---|
| Check mark | The step is done. |
| Highlighted step | The step on screen. |
| **Status** step in red | The account still has something outstanding: requirements, documents being verified, rejected items or an unfinished compliance task. |

A step can be clicked when it is done, when it is not beyond the current step, or when every earlier step is done. **Status** can always be opened.

## Business rules

### The steps in order

| # | Step | Done when |
|---|---|---|
| 1 | Profile | The account exists. |
| 2 | Business | The account has a legal company name and a trading name. |
| 3 | Representative | At least one person is on the account. |
| 4 | Documents | At least one document is uploaded. |
| 5 | Verification | The account has been submitted for review. |
| 6 | Bank | A payout bank account is on the account. |
| 7 | Status | The account is submitted and nothing is outstanding. |

Done states are worked out from the live account each time the tab opens, together with the steps this store has already completed. A store that links an existing account therefore sees the steps that account already covers marked as done, without entering anything again.

### Submitting happens in the Documents step

The account is submitted for review with the button in step 4 (**Submit account for review**). Because step 5 counts as done from that moment, reopening the wizard may land on **Bank** or **Status**. Any agreements still to accept then appear on the **Status** step as a compliance task whose **Resolve** button leads back to step 5 — see [[ccpay-onboarding-verification-attestation]].

### Resuming

On opening, the wizard lands on the first of steps 1–6 that is not done; when all are done, on **Status**. A `?step=` in the address takes precedence. Nothing typed into an unsaved form is kept.

### Live data, no local copy

Business details, people, documents and bank accounts are read from the connected account each time; the store keeps only the link to the account and its onboarding progress. Changes made from another store that shares the account appear here on the next load.

### After approval

The tab stays the account's dashboard: the **Status** step shows the capabilities and anything the compliance team asks for, and step 1 holds **Disconnect**. See [[ccpay-onboarding-status-capabilities]].

### Staff access

The Onboarding tab and its actions are available only to staff whose role allows the store's payment methods settings — see [[settings-staff]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-connect-disconnect]] — the first screen's two paths.
- [[ccpay-onboarding-documents-upload]] — where the account is submitted.
- [[ccpay-onboarding-status-capabilities]] — the Status step.
- [[payment-providers-cloudcart-pay]] — CloudCart Pay hub.
- [[settings-staff]] — staff permissions.

## Open questions

(none)
