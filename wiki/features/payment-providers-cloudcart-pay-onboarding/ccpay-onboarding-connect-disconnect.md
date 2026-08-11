---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Onboarding → Connect / Disconnect"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["Connect existing CloudCart Pay account", "Disconnect CloudCart Pay account", "Re-link connected account", "Country business-type lock", "Account locked after creation"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, connect, disconnect, account-link]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, KYB fields, documents, verification, bank, status).

# Onboarding — Connect / Disconnect

## Purpose

The onboarding screen exposes two account-link operations outside the 7-step flow itself: **Connect Existing Account** (link this store to a Paypercut connected account already created from another CloudCart store) and **Disconnect** (clear the local link without deleting the account at the platform). Together they explain why country and business type are locked after creation — to "change country" the merchant has to disconnect, create a brand-new account, and re-onboard.

## Where to find it

Payment Providers → CloudCart Pay → **Onboarding** tab.

- *Connect Existing Account* lives on the empty-state screen (visible when no account is on file for this store).
- *Disconnect* lives on step 1 once an account exists.

## What the merchant can do here

- Choose between two onboarding paths on the empty-state screen:
  - **Start Onboarding** — create a new connected account through the wizard.
  - **Connect Existing Account** — paste an existing CloudCart connected-account ID (e.g., `01KPZ...`) to link this store to an account created earlier from another CloudCart store.
- Copy the connected account ID or the representative's person ID to the clipboard.
- Click **Disconnect** on step 1 to clear the local link (the platform account is preserved).

## Settings & fields

### Connect Existing Account form

| Field | Required? | What it does | Notes |
|-------|-----------|--------------|-------|
| **Account ID** | Yes | Existing Paypercut connected-account ID, posted as `account_id`. | Format e.g. `01KPZ...`. The backend verifies the ID exists on Paypercut before saving. |

Backend: `POST /admin/cloudcart-pay/account/connect`.

### Disconnect action

Backend: `DELETE /admin/cloudcart-pay/account/disconnect`. No form fields — the action prompts a confirmation dialog with the verbatim warning text below.

## Business rules

### Country and business type are locked after creation

The step 1 selects become **disabled** the moment an account exists. The Paypercut platform does not let either change after creation — to "change country" the merchant has to disconnect, create a brand-new account, and re-onboard. (Disconnect does not delete the platform account; it only clears the local link — see below.)

### Disconnect clears the local link without deleting the platform account

The **Disconnect** action on step 1 calls `DELETE /admin/cloudcart-pay/account/disconnect`. It:

1. Strips obsolete legacy config keys (`tax_id`, `bank_iban`, `doc_identity`, etc. — same list as `cleanupObsoleteConfig`).
2. Sets `connected_account_id = null` and `onboarding_completed_steps = []`.
3. **Forcibly deactivates the CloudCart Pay payment method** (sets the provider row's `active` flag to `no`).
4. Returns `{disconnected: true}` so the Vue layer can also push `active=no` into the cached app settings (the header toggle flips off without a reload).

The connected account itself **still exists on the CloudCart Pay platform** — only this store's local link is cleared. The same account can later be re-linked through *Connect Existing Account*, or replaced with a brand-new account.

The wizard explicitly warns the merchant on the disconnect confirmation prompt with the verbatim message:

> *"Disconnect this account? The account will still exist on CloudCart but this store will stop referencing it and the payment method will be turned off."*

### Connect Existing Account — refuses if an account is already linked

Pasting an existing connected-account ID in the *Connect Existing Account* form POSTs to `/admin/cloudcart-pay/account/connect`. The backend:

1. **Refuses with HTTP 409** if a connected account is already on file for this store — the merchant must disconnect first. Error message: *"An account is already connected. Disconnect first."*
2. **Verifies the ID exists** on the Paypercut platform via `GET /v1/accounts/{id}`. Returns the provider's error verbatim if the ID is unknown.
3. **Saves the ID** to the provider configuration.
4. **Re-derives the completed-steps list** from the live account state so the wizard lands on the correct step (see [[ccpay-onboarding-wizard-flow]]).

### Multi-store account sharing — allowed by CloudCart, gated by Paypercut

Multiple CloudCart stores can technically link to the same Paypercut connected account — the CloudCart controller only refuses to connect when **the current store** already has an account on file. Whether Paypercut itself rejects duplicate Site IDs on its side is a provider-side rule, not a CloudCart rule. `(verify)` against Paypercut's documentation.

### Cleanup of obsolete config on every account load

`cleanupObsoleteConfig` runs on every account load (not only on disconnect) and strips legacy keys that pre-date the May 2026 refactor: `tax_id`, `bank_iban`, `doc_identity`, `bank_account_holder_name`, etc. Only the connected account ID and the completed-steps counter are persisted by CloudCart itself; everything else is read from Paypercut on demand — see [[ccpay-onboarding-wizard-flow]] for the live-state derivation logic.

### Disconnect cascades into the payment-method `active` flag

Disconnect is the only one-click action on this tab that **forcibly deactivates** the storefront payment method. Once the local link is cleared, the activation prerequisite is gone, so the platform flips the provider row's `active=no` immediately. The merchant must re-onboard (or link an existing account) and re-activate before the storefront sees CloudCart Pay again — see [[payment-providers-cloudcart-pay]] for the activation gate.

### "Change country" workflow

There is no direct "change country" control. To change the country (or business type) of an existing account, the merchant must:

1. Disconnect the current account (this store stops referencing it; the platform account remains).
2. Click *Start Onboarding* on the empty state.
3. Pick the new country / business type in step 1.
4. Re-onboard from scratch.

The old account on the Paypercut platform is now orphaned from this store — the merchant can either re-link it from a different CloudCart store, or close it via Paypercut support. `(verify)` the closure procedure.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — re-derive completed steps from live state after re-link.
- [[ccpay-onboarding-account-business-fields]] — step 1 country / business-type locked once an account exists.
- [[payment-providers-cloudcart-pay]] — activation gate + auto-deactivation on disconnect.
- [[payment-providers-cloudcart-pay-settings]] — connected-account chip mirrors the link state.

## Open questions

- ⏸️ Whether Paypercut rejects duplicate Site IDs when two CloudCart stores try to link to the same connected account. `(verify)`
- ⏸️ Procedure for closing an orphaned Paypercut account after disconnect-then-re-onboard. `(verify)`
