---
type: feature
nav_path: "Payment Providers → myPOS → Setup & Configuration Pack"
route_name: apps.mypos.overview
route_path: /admin/payment-providers/mypos
aliases: ["myPOS Configuration Pack", "myPOS setup", "myPOS credentials", "myPOS Store ID", "myPOS Wallet number", "myPOS Key Index", "myPOS test pack", "Конфигурационен пакет myPOS"]
tags: [paymentproviders, payment-providers, mypos, setup, credentials, config-pack]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-mypos]]. See the hub for related aspects (payment lifecycle, save card, refund & sync).

# myPOS — Setup & Configuration Pack

## Purpose

This aspect covers how a merchant turns on myPOS: where the screen lives, the full settings layout, and the **Configuration Pack** onboarding mechanism that replaces per-field credential entry. myPOS is **friction-light onboarding** compared to traditional bank gateways — no e-commerce contract with a Bulgarian bank is required; sign-up is online through myPOS's web portal. The CloudCart side is equally light: the merchant logs into myPOS, generates a **Configuration Pack** (a base64-encoded blob containing the Store ID, Wallet number, Key Index, and the merchant's RSA private key + myPOS's public certificate), pastes it into CloudCart, and the integration is live.

## Where to find it

Sidebar → **Payment Providers** → click **myPOS**.

Route: `/admin/payment-providers/mypos`. Route name: `apps.mypos.overview`. The page renders the standard `AppOverview`. There are no sub-tabs — wallet management, payouts, and transactions are in myPOS's own merchant portal at `www.mypos.eu`.

## What the merchant can do here

- **Install / Uninstall** the payment method via the standard overview buttons.
- **Activate / Deactivate** using the header switch.
- **Switch between Test and Live** environments using the radio.
- **Paste the test Configuration Pack** — base64-encoded blob from myPOS's developer docs. The platform ships a working test pack pre-populated for trial accounts.
- **Paste the live Configuration Pack** — base64-encoded blob from the merchant's myPOS portal at `www.mypos.eu → menu eCommerce → Online stores`. Once saved, the platform validates and decodes the pack into store credentials.
- **Configure standard payment-method options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override on storefront checkout. | Provider default | Standard. |
| **Title / Description** | Customer-facing payment method label. | Provider default | Standard. |
| **Mode** radio | Test or Live. | Test | Switching to Live requires a valid live Configuration Pack. |
| **Amount from / to** | Order total range where myPOS appears at checkout. | Empty (any amount) | Standard. |
| **Discount** | Optional fixed / percent discount when buyer picks myPOS. | None | Standard. |
| **Test Save customer card** switch | Enables CardToken-based tokenisation in test environment. | `no` | `yes` / `no`. Independent of the live switch. See [[mypos-save-card]]. |
| **Test Configuration Pack** | Base64-encoded blob with test store credentials. Pre-populated from [myPOS developer docs](https://developers.mypos.eu/en/doc/online_payments/v1_4/226-test-data). | (pre-populated test data) | Required. Validated by `base64_decode` + `json_decode`; must contain non-empty `sid` (store ID) and a valid PKCS-readable `pk` (private key). Errors: *"Invalid Configuration Pack"* / *"Invalid Configuration Pack: Invalid Private key"*. |
| **Live Save customer card** switch | Enables tokenisation in live environment. | `no` | Independent of the test switch. The configuration field stored is plain `save_card` (vs `test_save_card` for test). See [[mypos-save-card]]. |
| **Live Configuration Pack** | Base64-encoded blob from myPOS portal (`www.mypos.eu` → eCommerce → Online stores → generate package). | Empty | Required when Live. Same validation. Help block: *"Get your configuration pack at www.mypos.eu > menu eCommerce > Online stores."* |
| **JSON view of decoded credentials** (read-only display) | Shows the decoded fields (Store ID, Wallet number, Key Index, Public Certificate fingerprint) after upload — for the merchant to confirm the right pack was uploaded. | Auto-populated | Hidden until pack is uploaded. |

## Business rules

### Configuration Pack — what it contains and how it's validated

The merchant uploads a **Configuration Pack** (base64-encoded JSON) issued from the myPOS portal. On save, the platform `base64_decode` + `json_decode`s it and extracts: `sid` (Store ID), `wn` (Wallet number), `keyindex`, `pk` (merchant's RSA private key), and the embedded myPOS public certificate.

Validation: `sid` must be non-empty and `pk` must be PKCS-readable. Bad pack → *"Invalid Configuration Pack"*; bad private key → *"Invalid Configuration Pack: Invalid Private key"*.

Test and live packs are stored separately. The platform ships a working test pack pre-populated for trial accounts.

### IPC protocol version + key rotation

The platform pins to IPC version `1.4` (current myPOS Online Payments protocol). The `keyindex` from the Configuration Pack tells myPOS which of its rotating public keys to use when the platform verifies myPOS's responses — this lets myPOS rotate its signing keys without breaking older merchants.

### Test mode — uses myPOS's pre-shared test pack

The platform ships a working test Configuration Pack pre-populated in the field (per the help block: *"Test Mode Configuration Package is pre-populated. You can simply save the settings and press to test myPOS."*). This is myPOS's standard developer test data, available at their docs. Merchants can run end-to-end test transactions without their own myPOS account.

### Plan-tier gating

The provider has no plan gate. Any plan that allows payment providers can install myPOS. myPOS is one of the most accessible card gateways for small Bulgarian merchants because no bank contract is needed — sign-up is online through myPOS's portal.

### UI mechanics — settings card pattern

The Settings page is composed of **four cards** that render conditionally on the **Mode** radio:

1. **Save customer card (Test)** — `editMethod: inline` (toggle directly on card). Visible only when **Mode = Test**. Card has the **test-border colour** (`border-color-test`). Locked from editing while Mode = Live.
2. **Mypos test environment** — `editMethod: slide` (clicking the row opens a slide-down editor). Visible only when **Mode = Test**. Two fields stacked: **Test Configuration Pack** (multi-line textarea, pre-populated, required) and a read-only JSON view (`JsonView` component) showing the decoded test certificate (`test_certInfo` — Issuer, Subject, Valid From/To, Fingerprint, Serial).
3. **Save Customer (Live)** — `editMethod: inline`. Visible only when **Mode = Live**. Card has the **live-border colour** (`border-color-live`). Locked while Mode = Test. (The configuration key stored is `save_card` vs `test_save_card` — independent flags.)
4. **Mypos live environment** — `editMethod: slide`. Visible only when **Mode = Live**. Two fields: **Live Configuration Pack** (multi-line, required, help block points at `www.mypos.eu > menu eCommerce > Online stores`) plus a JSON view of the decoded live certificate (`certInfo`).

The platform watches `settings.configuration.mode` and toggles `isVisible` + `lockEditMethod` reactively — switching modes immediately swaps which cards show without a page reload.

The standard payment-method **`rows`** at the top (above the four cards) are `['logo', 'mode', 'amount', 'discount']` — Description and Authorization rows are intentionally absent because myPOS doesn't expose a customer-facing description override or a two-phase capture flow (see [[mypos-refund-sync]] for the auto-capture-only rule).

## Related

- [[payment-providers-mypos]] — hub.
- [[payment-providers]] — parent payment-providers hub.
- [[settings-payment-providers]] — global payment-providers list where myPOS is installed / uninstalled.
- [[payment-provider]] — entity definition.

## Open questions

_None._
