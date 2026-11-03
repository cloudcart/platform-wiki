---
type: feature
nav_path: "Payment Providers → CIB Bank → Settings"
route_name: apps.cib_bank.settings
route_path: /admin/payment-providers/cib_bank
aliases: ["CIB Bank settings", "CIB Bank configuration", "CIB DES file", "CIB Merchant ID", "CIB POS ID", "CIB Bank install"]
tags: [paymentproviders, payment-providers, cib-bank, hungary, card, des-encryption, settings]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# CIB Bank — settings & DES file

> Part of [[payment-providers-cib-bank]]. See the hub for the other aspects (payment flow, save-card & refunds).

## Purpose

This page covers the **admin configuration surface** for the [[payment-providers-cib-bank|CIB Bank]] payment method: where the merchant installs it, the per-environment Merchant ID + `.des` key file, the customer-facing label, the amount range and discount, and the DES-file lifecycle. The payment behaviour itself (redirect, status mapping) is on [[cib-bank-payment-flow]]; save-card and refunds are on [[cib-bank-save-card-refunds]].

The security model is **DES-encryption-based**: CIB Bank issues a `.des` key file containing three components (two DES keys and an initialisation vector) that the integration uses to encrypt every outgoing request and decrypt every incoming response. The merchant pastes the file content (hex-encoded) into the settings here.

## Where to find it

Sidebar → **Payment Providers** → click **CIB Bank**.

The route is `/admin/payment-providers/cib_bank`. The internal provider key is `cib_bank`. The settings panel is rendered by the shared `SettingsFormPayments` Vue component. CIB Bank is installed / uninstalled from the global list on [[settings-payment-providers]].

## What the merchant can do here

- **Install / Uninstall** the CIB Bank payment method.
- **Toggle Active** on / off in the header.
- **Switch between Test and Live mode** — each mode points to a different CIB endpoint and uses its own Merchant ID (POS ID) + DES file.
- **Enter the Test Merchant ID** and upload the **Test DES key file** (`.des`).
- **Enter the Live Merchant ID** and upload the **Live DES key file**.
- **Enable Save customer card** — see [[cib-bank-save-card-refunds]].
- **Override the customer-facing label** — logo, title, description on storefront checkout.
- **Set an amount range** (min / max) and an optional **discount** for the method.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Switches between CIB's test environment (`ekit.cib.hu`) and production (`eki.cib.hu`). | `test` | When the field is empty, the integration treats it as Test. |
| **Test Merchant ID** (`configuration.merchant_id_test`) | POS ID issued by CIB for the sandbox. | Empty | `required_if:configuration.mode,test`. Error: "Merchant ID is required" |
| **Test DES file** (`configuration.des_file_test`) | Hex-encoded contents of the `.des` key file CIB issues for the sandbox — parsed into key1, key2, IV. | Empty | Required when mode = test. Validated by the file-upload component. |
| **Live Merchant ID** (`configuration.merchant_id_live`) | POS ID issued by CIB for live processing. | Empty | `required_if:configuration.mode,live`. Error: "Merchant ID is required" |
| **Live DES file** (`configuration.des_file_live`) | Hex-encoded `.des` file for live mode. | Empty | Required when mode = live. Validated by the file-upload component. |
| **Save customer card** (`configuration.save_card`) | When `yes` and the customer is signed in, the next payment can be charged against a stored CIB token. | `no` | See [[cib-bank-save-card-refunds]]. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when customer picks CIB Bank. | None | `discount_type: 'flat'` default. |

`configurationDefault.cib_bank = { mode: 'test', save_card: 'no', discount_type: 'flat' }`.

## Business rules

### Settings UI layout (verified 2026-05-27)

Layout of route `apps.cib_bank.settings`:

1. **Header + Tabs + Logo** (`:no-description="true"` — no TinyMCE description slide-out for CIB Bank) + **Environment mode radio**.
2. **SettingsBox — CIB Bank-specific** (three cards):
   - **Live environment** (key `live`, edit method `panel`, **`isVisible: mode === 'live'`**, lock when `mode === 'test'`, border-color-live). Two fields:
     - `configuration.merchant_id_live` — required string. Label "POS ID for Live environment". Placeholder "This POS ID is provided from CIB Bank". Full-width (`inputSize: 12`).
     - `configuration.des_file_live` — file upload. Label "Live keys.des file". Help: "Choose the.des file provided by CIB Bank for Live Environment".
   - **Test environment** (key `test`, edit method `panel`, **`isVisible: mode === 'test'`**, lock when `mode === 'live'`, border-color-test). Two fields:
     - `configuration.merchant_id_test` — required string. Label "POS ID for Test environment".
     - `configuration.des_file_test` — file upload. Label "Test keys.des file".
   - **Save customer card settings** (key `save_card_settings`, edit method `inline`, `hideTitle: true`, always visible). One switch:
     - `configuration.save_card` — switch (`trueValue: 'yes'`, `falseValue: 'no'`).
3. **Common rows** — Amount from/to + Discounts.
4. **SubmitChanges** sticky bar.

### Conditional UI behaviour

- Only one environment's card is visible at a time (`isVisible` toggles on `mode`).
- The Save-card switch is global — one setting applies to both environments.

### DES file lifecycle

The `.des` file CIB issues contains a binary payload with three concatenated components: two DES keys (Key1, Key2, used for triple-DES encryption of payment data) and an initialisation vector (IV). The merchant pastes the **hex-encoded** file contents into the settings; on every config load, the integration decodes the hex back to binary, splits it into the three components, and feeds them to the gateway client. The file is **never written to disk** — it's reconstructed in memory per request. This avoids the kind of temp-file management [[payment-providers-mobilpay|MobilPay]] needs for its certificate pair.

The integration assumes **exactly three** concatenated components. There is no provision for tenants whose key bundle has a different layout — if CIB issues a different shape, the integration will reject it.

### Plan-tier gating

None — CIB Bank has no `plan_gates` declaration.

## Related

- [[payment-providers-cib-bank]] — hub.
- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where CIB Bank is installed / uninstalled.
- [[payment-provider]] — entity definition.
- [[payment-providers-mobilpay]] — contrast: certificate-file (temp-file) gateway.

## Open questions

(none)
