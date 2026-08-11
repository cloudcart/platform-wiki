---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Wizard flow"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay onboarding wizard", "7-step KYB wizard", "Onboarding step indicator", "Resume onboarding", "Deep-link step"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, wizard]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (KYB fields, documents, verification, bank, status, connect/disconnect).

# Onboarding — wizard flow

## Purpose

The onboarding screen is structured as a **7-step KYB (Know-Your-Business) wizard** that walks the merchant from "I have no CloudCart Pay account" to "my account is submitted for review". This aspect documents how the wizard itself behaves: the step structure, navigation between steps, resume-after-reload, deep-linking, and how each step's "complete" state is derived.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab.

Route: `/admin/payment-providers/cloudcart_pay/onboarding`. The wizard supports a `?step=<1-7>` query parameter for deep-linking to a specific step.

## What the merchant can do here

- Walk through the 7 wizard steps sequentially.
- Jump to any already-completed step via the step indicators at the top of the page.
- Resume on the last incomplete step on every reload — `determineCurrentStep` walks the saved progress list and lands on the first unfinished step.
- Edit previously-entered data by clicking a completed step in the stepper. Some fields (country, business type) are locked — see [[ccpay-onboarding-connect-disconnect]].
- Deep-link directly into a step with `?step=N`.

## The 7 steps

| # | Step | Aspect page | What it does |
|---|------|------------|--------------|
| 1 | **Account** | [[ccpay-onboarding-account-business-fields]] | Pick country, business type (`company` / `non_profit`), email; creates the connected account. |
| 2 | **Business** | [[ccpay-onboarding-account-business-fields]] | Public business profile, legal entity (KYB), registered address. |
| 3 | **Representative** | [[ccpay-onboarding-account-business-fields]] | A real person who controls the entity — identity, contact, home address. |
| 4 | **Documents** | [[ccpay-onboarding-documents-upload]] | Identity document + business registration document. |
| 5 | **Verification** | [[ccpay-onboarding-verification-attestation]] | Accept Paypercut agreements, submit account for review, optionally start identity verification. |
| 6 | **Bank** | [[ccpay-onboarding-bank-account]] | Add the payout IBAN. |
| 7 | **Status** | [[ccpay-onboarding-status-capabilities]] | Read-only status dashboard: capabilities, requirements, compliance tasks. |

## Settings & fields

The wizard itself exposes only step-indicator controls; the per-step fields live on the aspect pages linked above. The step-indicator panel renders one chip per step, marks completed steps with a check, the active step highlighted, and any step the merchant can revisit clickable.

## Business rules

### Onboarding progress is reconstructed live from the API

Step completion is **not** stored only as a local counter — the platform calculates which steps are satisfied **from the live Paypercut account state** on every load, then unions that with the local `onboarding_completed_steps` counter. Concretely:

- **Step 1** complete: an account ID exists.
- **Step 2** complete: `company.name` AND `business_profile.name` are set.
- **Step 3** complete: ≥1 person exists with `relationship.representative=true` (or any person — first one wins).
- **Step 4** complete: the Files API (`GET /v1/files`) returns ≥1 uploaded file.
- **Step 5** complete: `details_submitted === true`.
- **Step 6** complete: the account has ≥1 external account with an `id`, `last4`, or `holder_name`.
- **Step 7** complete: `details_submitted === true` AND `requirements.currently_due` is empty.

This means a merchant who links an **existing** account via the *Connect Existing Account* flow sees the correct already-completed steps without re-entering anything — see [[ccpay-onboarding-connect-disconnect]] for the connect/disconnect mechanics.

### Live state, no local cache

The May 2026 refactor removed every locally-cached copy of the account / persons / bank / documents data. Field values rendered in the wizard come straight from the Paypercut API: `GET /v1/accounts/{id}` (with `expand=external_accounts`), `GET /v1/accounts/{id}/persons`, and `GET /v1/files`. Stale legacy keys (`tax_id`, `bank_iban`, `doc_identity`, etc.) are explicitly stripped on every account load via `cleanupObsoleteConfig`. Only the connected account ID and the local "completed steps" counter are persisted by CloudCart itself; everything else is the platform's source of truth.

### Approved account = long-lived dashboard

Once approved, the merchant's account on this tab becomes the long-lived "account dashboard" — the same screen shows verification status, capability flags, outstanding compliance tasks (see [[ccpay-onboarding-status-capabilities]]), and the *Disconnect* action (see [[ccpay-onboarding-connect-disconnect]]).

### Permission

The page is under `hasApiPermission:settings,store.payment_providers`. A staff member without that grant cannot reach the page or its API endpoints — see [[settings-staff]].

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[payment-providers-cloudcart-pay]] — parent provider overview with the activation gate.
- [[settings-staff]] — `store.payment_providers` permission required to open this page.

## Open questions

(none)
