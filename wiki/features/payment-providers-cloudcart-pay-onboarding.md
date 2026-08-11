---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay onboarding", "Connect account", "Connected account", "KYB", "CloudCart Connect", "Identity verification", "Регистрация CloudCart Pay", "Свържи акаунт"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, kyb]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Onboarding

## Purpose

A **7-step KYB (Know-Your-Business) wizard** that creates the merchant's connected sub-account on the CloudCart Pay platform — the prerequisite for activating the CloudCart Pay payment method on the storefront. The wizard collects the legal entity details, a representative person, identity / business documents, an IBAN bank account for payouts, and the merchant's acceptance of the Paypercut Service Agreement, then submits the account for review. Until this flow is completed (or the merchant links an existing CloudCart Pay account via *Connect Existing Account*), the storefront cannot accept card payments through CloudCart Pay — activation is server-side blocked, see [[payment-providers-cloudcart-pay]].

The wizard mirrors the live state of the connected account on every reload (it reads back from the Paypercut Accounts, Persons and Files APIs), so a merchant who closes the browser mid-onboarding picks up exactly where they left off without losing data. Once approved, the merchant's account on this tab becomes the long-lived **account dashboard** — the same screen shows verification status, capability flags, outstanding compliance tasks, and the *Disconnect* action.

This hub catalogues the 7 aspect pages this concept splits into. Drill into the aspect that matches the question rather than reading every page.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab.

The route is `/admin/payment-providers/cloudcart_pay/onboarding`. The wizard supports a `?step=<1-7>` query parameter for deep-linking to a specific step. The page is rendered by `Onboarding.vue`.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages:

- [[ccpay-onboarding-wizard-flow]] — the 7-step structure, step indicator, resume-on-reload, `?step=N` deep-linking, live-state step-completion derivation, the `cleanupObsoleteConfig` rule, and the `store.payment_providers` permission gate.
- [[ccpay-onboarding-account-business-fields]] — every field on steps 1 (Account), 2 (Business / Legal entity / Registered address / Customer support), and 3 (Representative — Identity / Contact / Home address); MCC `<optgroup>`, `company_structure` enum, edit-in-place rep replacement.
- [[ccpay-onboarding-documents-upload]] — step 4 identity + business-registration uploads; `pdf/png/jpg/jpeg` ≤ 10 MB; `purpose=identity_document`; attachment to `verification.document.front` / `documents.proof_of_registration.files`; the inline file-view proxy.
- [[ccpay-onboarding-verification-attestation]] — step 5 agreement attestations, `details_submitted=true` with server-stamped TOS evidence, identity-verification sessions, the *"Verification unavailable"* graceful fallback.
- [[ccpay-onboarding-bank-account]] — step 6 payout IBAN; `numbers.scheme=iban`; the 12 settlement currencies; whitespace-strip on IBAN; empty-BIC omission; *Replace bank account*.
- [[ccpay-onboarding-status-capabilities]] — step 7 read-only dashboard; `payments_enabled` / `payouts_enabled`; capability pill colours; `currently_due` vs `pending_verification`; compliance tasks with / without `agreement_bundle`.
- [[ccpay-onboarding-connect-disconnect]] — *Connect Existing Account* (`POST /admin/cloudcart-pay/account/connect`, HTTP 409 when already linked), *Disconnect* cascade (auto-deactivates the payment method), country / business-type lock rationale, "change country" workflow.

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page. The 7 high-level actions, with their aspect page:

- **Start a new connected account / link an existing one** — see [[ccpay-onboarding-connect-disconnect]].
- **Walk through / resume the 7-step wizard** — see [[ccpay-onboarding-wizard-flow]].
- **Enter KYB fields** (country, business, representative) — see [[ccpay-onboarding-account-business-fields]].
- **Upload identity / business-registration documents** — see [[ccpay-onboarding-documents-upload]].
- **Accept the Paypercut service agreement, submit for review, start identity verification** — see [[ccpay-onboarding-verification-attestation]].
- **Add the payout IBAN** — see [[ccpay-onboarding-bank-account]].
- **Read the live status dashboard + refresh capabilities** — see [[ccpay-onboarding-status-capabilities]].

## Settings & fields

This hub does not expose any fields directly. Field-level documentation per step:

- Steps 1 / 2 / 3 (KYB) → [[ccpay-onboarding-account-business-fields]].
- Step 4 (documents) → [[ccpay-onboarding-documents-upload]].
- Step 5 (verification + attestation) → [[ccpay-onboarding-verification-attestation]].
- Step 6 (bank) → [[ccpay-onboarding-bank-account]].
- Step 7 (status, read-only) → [[ccpay-onboarding-status-capabilities]].
- Connect / Disconnect form → [[ccpay-onboarding-connect-disconnect]].

## Business rules

The cross-cutting rules that apply to the screen as a whole are spelled out per aspect:

- **Live-state derivation of step completion + no local cache** — see [[ccpay-onboarding-wizard-flow]].
- **Country / business-type locked after account creation** — see [[ccpay-onboarding-connect-disconnect]].
- **TOS evidence stamped server-side** — see [[ccpay-onboarding-verification-attestation]].
- **Disconnect cascades into `active=no` on the storefront payment method** — see [[ccpay-onboarding-connect-disconnect]] and [[payment-providers-cloudcart-pay]].
- **Permission gate** `store.payment_providers` — see [[ccpay-onboarding-wizard-flow]] + [[settings-staff]].
- **All API calls scoped via `Paypercut-Account` header** — see [[payment-providers-cloudcart-pay]] for the platform-wide auth model.

## Why it matters to the merchant

- **Server-side activation gate.** The storefront *Active* switch on CloudCart Pay refuses to flip ON until onboarding is complete AND `card_payments` is `active` on the connected account — see [[payment-providers-cloudcart-pay]].
- **No local cache — every field is live from Paypercut.** The May 2026 refactor removed every locally-cached copy of the account data. The merchant can edit details from another CloudCart store or from a Paypercut admin tool and the wizard will reflect the change on next load. See [[ccpay-onboarding-wizard-flow]].
- **Country + business type are immutable after creation.** To "change country" the merchant must disconnect and re-onboard — see [[ccpay-onboarding-connect-disconnect]].
- **Disconnect ≠ delete.** Disconnect only clears this store's local link; the Paypercut account survives and can be re-linked from this or another CloudCart store via *Connect Existing Account*.

## Scope

Covered (across the 7 sub-pages):

- The 7-step wizard structure + step indicator + resume.
- Every KYB field on steps 1, 2, 3 with validation.
- Document upload constraints + the file-view proxy.
- Service-agreement attestation, TOS server-stamping, identity verification.
- Bank account / payout IBAN, settlement currencies.
- Read-only status dashboard with capabilities + requirements + compliance tasks.
- Connect / Disconnect mechanics + immutable country / business-type.

Not covered here:

- The storefront-facing checkout JS (embedded vs hosted) — see [[payment-providers-cloudcart-pay]].
- The *Save customer card* toggle — see [[payment-providers-cloudcart-pay-settings]].
- The Paypercut transaction ledger — see [[payment-providers-cloudcart-pay-transactions]].
- The payouts capability lifecycle — see [[payment-providers-cloudcart-pay-payouts]].
- The `store.payment_providers` staff permission detail — see [[settings-staff]].

## Related

- [[payment-providers-cloudcart-pay]] — parent overview with the activation gate.
- [[payment-providers-cloudcart-pay-settings]] — the *Save customer card* switch and the connected-account chip mirror this tab's state.
- [[payment-providers-cloudcart-pay-transactions]] — visible only when this onboarding is complete and `card_payments` is active.
- [[payment-providers-cloudcart-pay-payouts]] — uses the bank account added in step 6 (see [[ccpay-onboarding-bank-account]]).
- [[settings-payment-providers]] — global payment-providers list.
- [[payment-provider]] — entity definition.
- [[notification-delivery]] — where onboarding error / auto-deactivation notices surface.
- [[settings-staff]] — `store.payment_providers` permission required to open this page.
- [[checkout-flow]] — what becomes available on the storefront once onboarding finishes.

## Open questions

- ⏸️ KYB review SLA on the Paypercut / CloudCart Pay side — turnaround from *Submit account for review* until the capability flips to `active` is not surfaced in CloudCart; refer to Paypercut's onboarding documentation or support. See [[ccpay-onboarding-verification-attestation]]. `(verify)`
