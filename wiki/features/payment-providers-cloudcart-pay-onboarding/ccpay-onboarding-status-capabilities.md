---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Status"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["CloudCart Pay status dashboard", "Capabilities pills", "Pending Requirements", "Pending Verification", "Compliance Tasks", "payments_enabled", "payouts_enabled"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, status, capabilities, compliance]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, KYB fields, documents, verification, bank, connect/disconnect).

# Onboarding — Status & capabilities

## Purpose

Step 7 of the onboarding wizard is the **read-only status dashboard** for the connected account. It shows the current state of the payments and payouts capabilities, the full list of capability flags, outstanding requirements the merchant must address, items Paypercut is verifying on its side, and any compliance tasks (some of which are accepted earlier in step 5 — see [[ccpay-onboarding-verification-attestation]]). Once onboarding is approved, this step becomes the long-lived "account dashboard" the merchant returns to.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab → **Status** (step 7).

## What the merchant can do here

- Read the current **Payments** and **Payouts** capability state.
- Read the full capabilities list with coloured pills.
- See pending requirements that need merchant action.
- See pending verifications that are on Paypercut's side (no merchant action).
- See outstanding compliance tasks.
- **Refresh status** to re-fetch capabilities, requirements, and compliance tasks live from Paypercut.
- Copy the connected account ID or the representative's person ID to the clipboard.

## Settings & fields

Backend: `GET /admin/cloudcart-pay/account` → Paypercut `GET /v1/accounts/{id}?expand=external_accounts`; `GET /admin/cloudcart-pay/compliance-status` → Paypercut `GET /v1/accounts/{id}/compliance-status`. Read-only.

| Block | What it shows |
|-------|---------------|
| **Payments** card | "Enabled" or "Disabled" + sub-text ("Capability under review" / "Capability active — provider finalizing"). Active when `payments_enabled === true` OR `capabilities.card_payments === "active"`. |
| **Payouts** card | "Enabled" or "Disabled" + sub-text ("Payouts capability not requested" if the capability isn't on the account). Active when `payouts_enabled === true` OR `capabilities.payouts === "active"`. |
| **Capabilities list** | Every capability on the account with a coloured pill: `active` (green), `inactive` (yellow), `pending` (cyan), `disabled` (red), other (grey). |
| **Pending Requirements** | `requirements.currently_due` entries — the merchant must address each. |
| **Pending Verification** | `requirements.pending_verification` entries — on Paypercut's side, no merchant action. |
| **Compliance Tasks** | Outstanding tasks returned by the risk endpoint. Tasks with an `agreement_bundle` are accepted in step 5; other tasks are surface-only here. |

## Business rules

### Payments enabled — either flag activates

The Payments card flips to "Enabled" when **either** `payments_enabled === true` **or** `capabilities.card_payments === "active"`. The two are usually in sync but the platform sometimes lags one behind the other; the OR keeps the card honest.

### Payouts capability may not be requested at all

If the account was created without requesting `payouts.requested=true` (uncommon — see [[ccpay-onboarding-account-business-fields]] which sets both capabilities by default), the Payouts card shows "Payouts capability not requested" instead of "Disabled". This distinguishes "capability not on the account" from "capability on the account but inactive".

### Capability pill colours

The full capabilities list uses a pill-colour convention:

- `active` → green pill
- `inactive` → yellow pill
- `pending` → cyan pill
- `disabled` → red pill
- any other state → grey pill

The Assistant should map merchant-language questions ("why is my account yellow?") to the underlying capability state by reading this section.

### Pending Requirements vs Pending Verification

These are two different lists from Paypercut's `requirements` block:

- **`requirements.currently_due`** — merchant action needed. Each entry names a field, document, or attestation the merchant must provide. Step 5 (verification submission) clears the `details_submitted` requirement; step 4 (documents) clears document requirements; step 6 (bank) clears external-account requirements.
- **`requirements.pending_verification`** — Paypercut is checking something on its side. No merchant action — the merchant just waits.

### Compliance Tasks — two sub-classes

Compliance tasks from the risk endpoint come in two flavours:

- **Tasks with an `agreement_bundle`** — agreement documents (TOS, processing addendum, etc.) the merchant accepts on step 5. Once accepted, the task disappears from this list. See [[ccpay-onboarding-verification-attestation]].
- **Tasks without an `agreement_bundle`** — surface-only on this step. The merchant sees them as information ("provide additional info to your account manager") but cannot act on them through the wizard. They typically resolve once Paypercut's risk team closes them server-side.

### Step 7 completion criterion

Step 7 is marked complete when `details_submitted === true` AND `requirements.currently_due` is empty — see [[ccpay-onboarding-wizard-flow]]. This is the "fully onboarded" state.

### Refresh status re-fetches live

Clicking *Refresh status* re-runs `GET /admin/cloudcart-pay/account` and `GET /admin/cloudcart-pay/compliance-status` against Paypercut without a page reload. The capability pills, requirements lists, and compliance task list all repopulate from the response. Useful when the merchant expects Paypercut to have moved a flag (e.g., after submitting documents) but the wizard was loaded before the change.

### Status flow drives storefront activation

The Payments capability state on this step is what gates the storefront-facing payment method. The provider page's *Active* switch refuses to flip ON until either `payments_enabled === true` or `capabilities.card_payments === "active"` — see [[payment-providers-cloudcart-pay]] for the activation gate's full criteria.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — step completion mechanics + resume.
- [[ccpay-onboarding-verification-attestation]] — step 5 where compliance tasks with agreement bundles are accepted.
- [[ccpay-onboarding-bank-account]] — step 6 where the `payouts` capability gets its bank account.
- [[payment-providers-cloudcart-pay]] — activation gate that consumes this status.
- [[payment-providers-cloudcart-pay-payouts]] — payouts capability surfaced on a separate sub-tab.

## Open questions

(none)
