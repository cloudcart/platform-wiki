---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Onboarding → Connect / Disconnect"
route_name: apps.cloudcart_pay.onboarding
route_path: /admin/payment-providers/cloudcart_pay/onboarding
aliases: ["Connect existing CloudCart Pay account", "Disconnect CloudCart Pay account", "Re-link connected account", "Country business-type lock", "Change country CloudCart Pay", "Account details could not be loaded", "Свързване със съществуващ акаунт", "Прекъсни връзка CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, onboarding, connect, disconnect, account-link]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-onboarding]]. See the hub for the other aspects (wizard flow, fields, people, documents, verification, bank, status, review and alerts).

# Onboarding — Connect / Disconnect

## Purpose

The two actions that link and unlink a store and its CloudCart Pay account outside the seven steps: **Connect Existing Account** (link this store to an account created earlier, for example from another CloudCart store) and **Disconnect** (clear this store's link without deleting the account). This page also covers the screen shown when a linked account cannot be loaded, and why changing the country means a new account.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Onboarding** tab.

- **Connect Existing Account** (Свързване със съществуващ акаунт) — on the first screen, while the store has no account.
- **Disconnect** (Прекъсни връзка) — in step 1, next to **Connected Account ID**, and on the warning shown when the account cannot be loaded.

## What the merchant can do here

- **Start Onboarding** for a new account, or **Connect Existing Account** by pasting an account ID.
- **Copy** the connected account ID.
- **Disconnect** the store from its account.

## Settings & fields

### Connect Existing Account

| Field | Required | Notes |
|---|---|---|
| Account ID | Yes | Placeholder *"CloudCart account ID (e.g. 01KPZ...)"*. Help: *"Paste an existing CloudCart connected account ID to link this store to it without creating a new account."* Button **Link**. |

### Disconnect

No fields. A confirmation asks: *"Disconnect this account? The account will still exist on CloudCart but this store will stop referencing it and the payment method will be turned off."*

## Business rules

### Connect Existing Account

- Refused when this store already has an account: *"An account is already connected. Disconnect first."*
- The ID is checked against CloudCart Pay first; an unknown ID shows the reason returned and nothing is saved.
- After linking, the wizard opens on the right step: whatever the account already contains (business details, people, documents, bank account, submission) is marked as done.
- Several CloudCart stores can be linked to the same account this way.

### Disconnect

Disconnect:

1. clears this store's link to the account and its onboarding progress;
2. **switches the CloudCart Pay payment method off** — the header switch turns off without a reload;
3. leaves the account itself untouched: it can be linked again from this or another store.

To take card payments again, the store links an account or onboards a new one, and switches the method back on ([[cloudcart-pay-activation-gate]]). Saved cards of the old account are not offered on a different account ([[cloudcart-pay-save-card]]).

### When the account cannot be loaded

If the store is linked but the account's details cannot be read, the tab shows *"This store is linked to a CloudCart Pay account, but its details could not be loaded."* and *"The account may belong to a different environment (test/live), have been removed, or the payment provider may be temporarily unavailable. You can disconnect the link below and connect again."*, with the account ID, **Copy** and **Disconnect**. An account created in the test environment cannot be used in the live one, and vice versa.

### Country and business type are locked

Once the account exists, the **Country** and **Business Type** lists in step 1 are disabled; the screen says *"Account created on CloudCart. Country and business type are locked after creation. Disconnect only clears the local link — the account still exists on CloudCart."* There is no "change country" control. To register under another country or business type:

1. **Disconnect** the current account;
2. click **Start Onboarding** on the first screen;
3. choose the new country and business type in step 1;
4. complete the onboarding again; the new account goes through review like any new account.

The old account stays as it was and is no longer used by this store.

## Related

- [[payment-providers-cloudcart-pay-onboarding]] — hub.
- [[ccpay-onboarding-wizard-flow]] — the first screen and the steps.
- [[ccpay-onboarding-account-business-fields]] — the locked fields in step 1.
- [[cloudcart-pay-account-model]] — one account, several stores.
- [[cloudcart-pay-activation-gate]] — Disconnect switches the method off.
- [[payment-providers-cloudcart-pay-settings]] — the Connected Account card follows the link.

## Open questions

- Whether the payment platform limits how many stores may share one account.
- How an account that is no longer used is closed.
