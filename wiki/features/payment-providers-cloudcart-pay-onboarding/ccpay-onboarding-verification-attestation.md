---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Verification & Attestation"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["Paypercut service agreement", "TOS acceptance", "Submit account for review", "Identity verification session", "Verification unavailable fallback", "Attestation"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, verification, tos, attestation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, KYB fields, documents, bank, status, connect/disconnect).

# Onboarding — Verification & Attestation

## Purpose

Step 5 of the onboarding wizard handles three distinct sub-flows: (a) acceptance of the Paypercut service agreement documents (rendered dynamically from the compliance task bundle), (b) submission of the account for review (`details_submitted=true` with server-stamped TOS evidence), and (c) optional creation of an identity verification session for the representative person. This step is where the merchant moves the account from "data collected" to "in review on Paypercut's side".

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab → **Verification** (step 5).

## What the merchant can do here

- Tick acceptance checkboxes for each Paypercut-served agreement document (mandatory documents are starred).
- Click **Accept & Submit** to post an `attestation` recording acceptance.
- Tick the "I confirm the information is accurate" checkbox and click **Submit account for review** to set `details_submitted=true`.
- Click **Start Identity Verification** to create a verification session for the representative; copy the resulting link to share with them.
- See the **Verification unavailable** graceful fallback notice when Paypercut errors AND the account is already operational.

## Settings & fields

| Control | What it does | Notes |
|---------|--------------|-------|
| **Agreement document checkboxes** | One per Paypercut-served agreement document; mandatory documents are starred. **Accept & Submit** posts an `attestation` recording acceptance. | Renders dynamically from the compliance task bundle returned by Paypercut (`agreement_bundle` on each compliance task). |
| **"I confirm the information is accurate" checkbox + Submit account for review button** | Sets `details_submitted=true` on the Paypercut account and records the TOS acceptance evidence: ISO 8601 date, request IP, user agent (capped at 1024 chars), `service_agreement=full`. | Shown only when `details_submitted` is in `currently_due`. |
| **Start Identity Verification button** | Creates a verification session for the representative; returns a URL to share with them. | Disabled until the account is submitted (`details_submitted` not currently due). |
| **Verification link copy / open** | Once a session exists, the link is shown with a Copy button and an Open Verification Link CTA. | The link is one-shot per session — re-creating creates a new session. |
| **"Verification unavailable" notice** | Shown when Paypercut returns a 500 / api_error AND the account is already operational. Lets the merchant continue and complete verification later. | Defensive UX — Paypercut occasionally errors here even on healthy accounts. |

### Backend endpoints

- `POST /admin/cloudcart-pay/attestations` → Paypercut `POST /v1/accounts/{id}/attestations`.
- `PUT /admin/cloudcart-pay/account/submit` → Paypercut `PUT /v1/accounts/{id}` with `details_submitted=true`.
- `POST /admin/cloudcart-pay/verification-session` → Paypercut `POST /v1/identity_verification_sessions`.

## Business rules

### Acceptance evidence is server-stamped

When the merchant submits the account for review, the `tos_acceptance` block sent to Paypercut is **stamped server-side** with:

- `date = now`
- `ip = request IP`
- `user_agent = request user agent (≤ 1024 chars)`
- `service_agreement = "full"`

The merchant cannot spoof acceptance from the browser side — the values are computed on the controller, not posted by the form.

### Agreement documents come from the compliance task bundle

The agreement checkboxes are NOT a static list. The wizard reads the compliance task bundle returned by Paypercut (`GET /v1/accounts/{id}/compliance-status`) and renders one checkbox per attached `agreement_bundle` document. Mandatory documents are starred. Tasks without an `agreement_bundle` (i.e., other compliance tasks) are surfaced read-only on step 7 instead — see [[ccpay-onboarding-status-capabilities]].

### Identity verification gating

Paypercut cannot create a verification session until `details_submitted=true` on the account. The wizard hard-blocks the *Start Identity Verification* button while `requirements.currently_due` still contains `details_submitted`. If the merchant somehow bypasses the gate and Paypercut returns a 500 / api_error, the controller intercepts and replaces the error with the verbatim message:

> *"Identity verification is not available yet. Please make sure all required business and representative details have been submitted, then try again."*

### "Verification unavailable" graceful fallback

If `POST /admin/cloudcart-pay/verification-session` fails AND the account has no remaining `currently_due` requirements (i.e., the account is already operational), the Vue layer **suppresses the error** and shows the verbatim message:

> *"Identity verification is temporarily unavailable from the payment provider. Your account details have been submitted and the account is active — you can continue now and the representative can complete identity verification later from this step."*

This prevents an isolated provider-side outage from trapping merchants on a step they've otherwise completed.

### Verification link is one-shot per session

Re-clicking *Start Identity Verification* creates a new session — the previous link becomes stale. The merchant should share the link only once per session to the representative; if the link expires or is lost, a new session can be created without affecting the rest of the account state.

### Step 5 completion criterion

Step 5 is marked complete when `details_submitted === true` on the live Paypercut account — see [[ccpay-onboarding-wizard-flow]]. Acceptance of agreement documents on its own does not flip step 5 to complete; the *Submit account for review* action is what writes `details_submitted=true`.

### KYB review SLA is not exposed in CloudCart

Turnaround from *Submit account for review* until the `card_payments` capability flips to `active` is on Paypercut's side and not surfaced in CloudCart. The merchant sees the live state of the capability on step 7 (see [[ccpay-onboarding-status-capabilities]]). For an SLA estimate, refer to Paypercut's onboarding documentation or support. (verify)

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — step completion mechanics + resume.
- [[ccpay-onboarding-account-business-fields]] — step 3 representative whose identity is being verified.
- [[ccpay-onboarding-documents-upload]] — step 4 documents accompanying verification.
- [[ccpay-onboarding-status-capabilities]] — step 7 where compliance tasks without an agreement bundle are surfaced.
- [[payment-providers-cloudcart-pay]] — activation gate that depends on `card_payments` capability becoming active.

## Open questions

- ⏸️ KYB review SLA on the Paypercut / CloudCart Pay side — not surfaced in CloudCart. `(verify)` against Paypercut's onboarding documentation.
