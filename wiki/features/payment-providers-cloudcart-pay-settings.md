---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Settings"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay settings", "CloudCart Pay configuration", "Save customer card CloudCart Pay", "Настройки CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-05-21
updated: 2026-06-23
source_count: 3
---
# Settings

## Purpose

A small configuration screen for the **CloudCart Pay** payment method. The May 2026 refactor moved all credentials to the platform; the merchant-controlled settings are now the **Save customer card** switch plus a small set of checkout-experience toggles — **Express checkout**, **Digital wallets** (Apple Pay / Google Pay), and **Card form display** (inline vs popup). Everything credential-related that used to live here (test/live API keys, public keys, separate save-card per mode) is now platform-driven: the test-vs-live environment is platform-wide (`CLOUDCART_PAY_MODE` host env), the secret key is the platform's system key, and the merchant's link to it is the **connected account ID** established through onboarding.

The tab therefore exists to (1) expose that single switch alongside the universal payment-method fields (logo, min/max amount, discount), and (2) surface the **connected account ID** (or a "no connected account yet" prompt) so the merchant knows which CloudCart Pay account this store is linked to.

## Where to find it

Payment Providers → CloudCart Pay → **Settings** tab. Route `/admin/payment-providers/cloudcart_pay/settings`; renders inside the `<router-view>` of the shared payment-provider page.

## What the merchant can do here

- **See the connected account ID** in a `<code>` chip at the top, with a **Manage Onboarding** link to the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]] — or a "no connected account yet" banner with a **Start Onboarding** link.
- **Toggle "Save Customer Card"** — whether customers see a "save this card for next time" option during checkout (see Business rules).
- **Toggle "Express checkout"** — shows an Apple Pay / Google Pay express button on **product pages** so a shopper can buy a single product without going through the cart and checkout.
- **Toggle "Digital wallets"** (Apple Pay / Google Pay) — enables/disables each wallet; applies to both the popup checkout and the express button.
- **Pick the "Card form display"** — `inline` (card fields embedded in the checkout page) or `popup` (default — fields open in a popup/modal).
- **Edit the standard payment-method shell** (logo, min/max amount, discount) via the shared settings shell used by every other payment provider.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Connected Account chip** | Read-only Paypercut connected-account ID this store is linked to (e.g., `acct_01HZX…`). | None until onboarding | Live from `connectedAccountState`; falls back to cached `configuration.connected_account_id` on cold reload. |
| **Manage Onboarding** / **Start Onboarding** link | Jumps to the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]]. | n/a | "Manage" when an account is connected; "Start" (info banner) when `connected_account_id` is empty. |
| **Save Customer Card** switch | Enables Paypercut's "save payment method" flow during checkout. | **ON** (new setups) | `configuration.save_card` boolean, persisted as `save_card`. The June-2026 defaults turned save-card (and wallets) **on** for new setups, alongside inline checkout. Legacy `test_save_card` / `live_save_card` still honoured for back-compat but no longer written. |
| **Express checkout** switch | Apple Pay / Google Pay express button on **product pages** (buy a single product without cart/checkout). | OFF | `configuration.express_checkout` boolean. Needs at least one wallet enabled + a completed connected account. |
| **Digital wallets** — Apple Pay / Google Pay | Enable/disable each wallet; applies to popup checkout **and** the express button. | Enabled (absent = enabled) | `configuration.apple_pay` / `configuration.google_pay` booleans. |
| **Card form display** | `inline` (card fields embedded in the checkout page) or `popup` (fields open in a modal after the complete-order button). | **`inline`** | `configuration.display_mode` — `inline` / `popup`. The default flipped from `popup` to **`inline`** in June 2026 (card fields embedded directly in checkout). |
| **Logo / Title / Description** | Standard payment-method appearance overrides. | Provider defaults | Shared shell; same as every provider. |
| **Amount (min / max)** | Order-total range in which CloudCart Pay appears at checkout. | Unset | Standard payment-provider field. |
| **Discount** | Optional discount when CloudCart Pay is selected. | None | Standard payment-provider field. |
| **Active** switch (page header) | ON / OFF for storefront checkout. | OFF | Activation rejected (HTTP 422) if onboarding isn't complete and `card_payments` capability isn't active. See [[payment-providers-cloudcart-pay#activation-gate-payments-must-be-active-on-the-connected-account|the parent page's activation gate]]. |

### Removed / no-longer-shown fields (May 2026 refactor)

Removed during the connected-account refactor. They are no longer editable by the merchant and are stripped from stored configuration on the next page load via the obsolete-keys cleanup (noted here so older support material referencing them can be located):

| Removed field | Why it's gone |
|---------------|---------------|
| `test_secret_key` / `live_secret_key` | Payments use the platform's system secret key; merchant has none of their own. |
| `test_public_key` / `live_public_key` | Never used in production; removed entirely. |
| Mode (test / live) toggle | Mode is platform-wide (`CLOUDCART_PAY_MODE` env), not per-merchant. |
| Separate test/live save-card switches | Consolidated into the single mode-agnostic `save_card`. |
| `tax_id`, `company_structure`, `bank_*`, `doc_*` keys | Onboarding data is now sourced live from the Paypercut API on every load; nothing is cached locally. |

## Business rules

### Save customer card — the only merchant-controlled CloudCart Pay field

This switch only affects **logged-in** storefront customers; the checkout-creation logic skips the save-card flow for guests entirely (regardless of switch state). When ON:

- Every checkout sets `saved_payment_method_options.payment_method_save = "enabled"` on the Paypercut checkout session.
- For logged-in customers the session also sets `payment_intent_data.setup_future_usage = "on_session"`. The platform creates or re-uses a Paypercut customer record (stored against the CloudCart customer) so the saved card can later be charged off-session and offered from the saved-cards picker.
- If the stored Paypercut customer is unknown to the current connected account (e.g., after disconnecting one account and connecting another), the stale reference is silently discarded and a fresh Paypercut customer created — no "No such customer" error.

When OFF, checkout still works but no Paypercut customer record is created; saved cards are neither offered nor retained.

Saved card records use the platform-wide save-card mechanism shared by every save-card-capable provider; the Paypercut customer ID and payment-method ID land on a CloudCart customer-card row visible at [[customers-details-payments]]. After a disconnect/re-connect to a different account, old cards remain as records but become unusable (see [[payment-providers-cloudcart-pay#save-card-flow-single-mode-agnostic-setting]]).

### Express checkout, card-form display, and digital wallets

- **Express checkout** (`express_checkout`) adds Apple Pay / Google Pay buttons on the **product detail page** — the shopper confirms the wallet sheet (address + shipping method) and the order is created without entering the cart or full checkout. It is built on the storefront routes `site.payment.cloudcart_pay.express-shipping` (recalculates shipping for the wallet address) and `site.payment.cloudcart_pay.express-order` (creates the order). It requires the provider active + onboarded **and** at least one wallet enabled.
- **Card form display** (`display_mode`): `popup` (default) opens the card form in a modal after "Complete order"; `inline` embeds the card fields directly on the checkout payment step via a short-lived inline session (`site.payment.cloudcart_pay.inline-session`).
- **Digital wallets** (`apple_pay` / `google_pay`) are each enable/disable, default enabled. They apply to the popup checkout and the express button alike.
- **Managing saved cards** — in inline mode the checkout payment step shows a "Manage saved cards" area where a signed-in customer can pick or remove a previously saved card; the same cards are visible to staff at [[customers-details-payments]].

### No credential validation runs on save

There are no merchant-entered credentials to validate — the secret key is the platform's system key and the connection is the per-merchant `connected_account_id` from onboarding. "Save" never raises a per-field credential error; those failures are caught instead by the activation gate and the runtime auto-deactivation on config load.

### Stripping obsolete keys on save

Every Save merges the new configuration into the existing one, then removes every key in the obsolete-keys list. A one-time cleanup: merchants who installed before the refactor may still carry stale `tax_id`, `bank_iban`, `test_secret_key`, etc.; the first Save (or first Onboarding-tab load) clears them. **Live data is sourced from the Paypercut API on every page load, never from stored configuration.**

### Connected-account chip reactivity

The display reads from a shared Vue reactive (`connectedAccountState`) updated by the Onboarding tab on connect, disconnect, and account-load. So connecting or disconnecting on Onboarding then switching to Settings updates the chip (new ID, or the "Start Onboarding" banner) without a reload. On a cold Settings load it falls back to `settings.configuration.connected_account_id` from the cached configuration.

### Test vs live mode is platform-controlled, not merchant-controlled

CloudCart Pay's Settings page deliberately has no "Mode: Test / Live" toggle and no API-key pairs. The test-vs-live decision is owned by the platform via the host-level `CLOUDCART_PAY_MODE` environment variable (default `test`); the system secret key is also platform-wide (`CLOUDCART_PAY_TEST_SECRET_KEY` or `CLOUDCART_PAY_LIVE_SECRET_KEY`).

Practical consequence: in test mode every charge runs against Paypercut's test environment and the [[payment-providers-cloudcart-pay-transactions|Transactions]] tab only shows test payments (`livemode=false` forced on the query); in live mode only live payments show. No merchant-visible button flips between the two.

The page shows a **read-only mode badge reflecting the REAL platform mode** (`platform_mode` = `live` / `test`, sourced from `CLOUDCART_PAY_MODE`) — previously it could fall back to the never-set per-merchant `mode` and mislead. The badge now always shows the actual environment the store is charging in.

### Disconnect option when the connected account is unreachable

When a `connected_account_id` exists but its details can't be fetched (test/live mismatch, the account was deleted upstream, or the provider is unreachable), Onboarding shows the account ID + a warning + a **Disconnect** button (instead of silently falling back to the "start onboarding" state). This lets the merchant clear a stale/broken link and reconnect.

### Publishable key is auto-fetched on connect

On account create / connect, onboarding auto-fetches and stores the connected account's **publishable key** (`pk_…`). It is the merchant's own key used to initialise the express-checkout / inline SDK on the storefront (rather than a platform key). The merchant never enters it.

### Saving uses the standard payment-provider save endpoint

The form POSTs to `/admin/payment-providers/save/cloudcart_pay` (the shared save route). Configuration preparation casts `save_card` to a strict boolean, preserves existing `connected_account_id` and `onboarding_completed_steps` keys, and strips the obsolete-keys list.

### Plan-tier gating

None — inherits the parent provider's plan posture. See [[payment-providers-cloudcart-pay#plan-tier-gating]].

### Permission

Same middleware as the other payment-provider screens: `hasApiPermission:settings,store.payment_providers`. A staff member without that grant can't reach the page (denied before render).

## Related

- [[payment-providers-cloudcart-pay]] — parent overview with the activation gate, checkout mechanism, and refund flow.
- [[payment-providers-cloudcart-pay-onboarding]] — where the `connected_account_id` is actually created or linked.
- [[payment-providers-cloudcart-pay-transactions]] — see the resulting card payments.
- [[payment-providers-cloudcart-pay-payouts]] — see where the money lands.
- [[settings-payment-providers]] — the global payment-providers list where this provider is installed.
- [[payment-provider]] — entity definition.
- [[customers-details-payments]] — customer-level view of saved cards (populated when *Save Customer Card* is ON).
- [[orders-payment-capture]] — capture flow (CloudCart Pay uses automatic capture).
- [[orders-payment-refund]] — refund flow against a CloudCart Pay payment.

## Open questions

_None._
