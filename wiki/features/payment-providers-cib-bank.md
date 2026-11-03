---
type: feature
nav_path: "Payment Providers → CIB Bank"
route_name: apps.cib_bank.settings
route_path: /admin/payment-providers/cib_bank
aliases: ["CIB Bank", "CIB", "Central-European International Bank", "Hungarian card gateway", "Hungarian card payments", "CIB eki", "CIB market.saki"]
tags: [paymentproviders, payment-providers, cib-bank, hungary, card, huf, save-card, des-encryption]
plan_gates: []
created: 2026-05-22
updated: 2026-06-24
source_count: 4
---
# CIB Bank

## Purpose

**CIB Bank** is the Hungarian arm of Intesa Sanpaolo and one of the main card-acquiring banks in Hungary. CloudCart integrates the bank's "market.saki" ecommerce hosted-payment gateway so merchants selling to Hungarian customers can accept Visa / Mastercard charges. The customer is redirected from the storefront checkout to CIB's hosted page (`eki.cib.hu` for live, `ekit.cib.hu` for test), enters card details there, completes 3D Secure if required, and is bounced back to the store after authorisation.

The security model is **DES-encryption-based**: CIB issues a `.des` key file (two DES keys + an initialisation vector) that the integration uses to encrypt every outgoing request and decrypt every incoming response. CIB also supports CloudCart's **save-card** mechanism — returning, signed-in customers can pay with a tokenised card on subsequent orders. The settlement currency is **Hungarian Forint (HUF)**.

This page is the **hub** for the CIB Bank cluster. The detail lives in three aspect pages — drill into the one matching the question rather than reading all three.

## Sub-pages (in this cluster)

- [[cib-bank-settings]] — the admin config surface: install / uninstall, Test vs Live mode, per-environment Merchant ID (POS ID), the `.des` file upload, label / amount-range / discount, the settings-UI layout + validation, and the DES-file in-memory lifecycle.
- [[cib-bank-payment-flow]] — the runtime charge: hosted redirect, two-step return (inquiry → complete-purchase), the CIB-response → CloudCart-status mapping, the reconciliation status-sync, 3DSv2 → Pending, and the double-query-string return URL quirk.
- [[cib-bank-save-card-refunds]] — save-card via stored OCID token (signed-in only), the refund flow with automatic `refund` → `retransfer` fallback, the saved-card UI on the customer profile, and the forced HUF currency conversion.

## Where to find it

Sidebar → **Payment Providers** → click **CIB Bank**.

The route is `/admin/payment-providers/cib_bank`. The internal provider key is `cib_bank`. The settings panel is rendered by the shared `SettingsFormPayments` Vue component. Install / uninstall happens from the global list on [[settings-payment-providers]].

## What the merchant can do here

- **Install / Uninstall** + **Toggle Active** the CIB Bank method (header).
- **Configure Test / Live mode**, the per-environment Merchant ID and `.des` key file, label, amount range and discount — see [[cib-bank-settings]].
- **Accept card payments** through the hosted-redirect flow — see [[cib-bank-payment-flow]].
- **Enable Save customer card** + **refund completed CIB payments** — see [[cib-bank-save-card-refunds]].

## Settings & fields

The full field table, defaults, and validation live on [[cib-bank-settings]]. In brief, the merchant configures: `configuration.mode` (Test / Live), `configuration.merchant_id_test` / `configuration.merchant_id_live` (POS IDs), `configuration.des_file_test` / `configuration.des_file_live` (hex-encoded `.des` files), `configuration.save_card` (see [[cib-bank-save-card-refunds]]), `configuration.payment_description` (custom customer-facing description), `configuration.show_footer` (yes/no — show the footer trust block, default yes), plus the standard label, amount-range, and discount rows.

`configurationDefault.cib_bank = { mode: 'test', save_card: 'no', discount_type: 'flat' }`.

## Business rules

Each rule is documented in full on its aspect page:

- **Forced HUF currency** — the gateway settles in HUF only; other-currency orders are converted before redirect. See [[cib-bank-save-card-refunds]].
- **Hosted redirect + two-step return** (inquiry → complete-purchase) + **status mapping** + **status sync** + **3DSv2 → Pending** + the **double-query-string return URL** quirk. See [[cib-bank-payment-flow]].
- **Save customer card** via stored OCID token (signed-in customers only); **refunds** with automatic `refund` → `retransfer` fallback on error code `01`. See [[cib-bank-save-card-refunds]].
- **DES file lifecycle** — hex-decoded to binary in memory per request, three components, never written to disk. See [[cib-bank-settings]].
- **Plan-tier gating** — none; CIB Bank has no `plan_gates` declaration.
- **Storefront footer trust block (bank-mandated).** When CIB Bank is active, the storefront footer automatically shows a trust block — the **CIB logo** (links to cib.hu) plus the accepted **Visa / Mastercard / Maestro** card logos, and a **disclosure line** naming the merchant's registered office: it is built from the store's `country` setting + `company_name` (falling back to `site_name`), is omitted entirely when no `country` is set, and uses Hungarian-specific wording when the store country is Hungary. It appears/disappears purely with the provider's active state (render-time, no persisted markup), is bilingual (Hungarian / English), and the logos are inlined SVGs (no asset deploy needed). The whole block is shown **by default**; a merchant can hide it by setting **`show_footer` = `no`**. Required by CIB's developer guidelines.
- **Custom payment description.** The merchant can set a free-text **`payment_description`** (in the settings configuration) that is shown to the customer for the CIB Bank method — overriding the default method description.
- **Failed transactions are closed (MSGT32).** On the payment result the integration sends CIB's closing message only for **terminal** outcomes: a successful auth (`RC=00`) is closed; any other error code is **closed and then failed**. **Pending** (`RC=PR`) and **timeout** (`RC=TO`) are NOT closed — a timeout is auto-reversed by the bank (the order fails), and a pending result keeps polling.
- **Customer result emails (bank-mandated).** A result email is sent to the customer once per terminal transaction (idempotent via a `result_email_sent` flag): a successful payment includes the transaction id (TRID), auth number (ANUM), amount, currency and response codes (RC/RT); a failed one includes TRID + RC/RT. The email body is in Hungarian.

## Related

- [[cib-bank-settings]] — settings, DES file, validation, UI layout.
- [[cib-bank-payment-flow]] — redirect, return, status mapping, sync.
- [[cib-bank-save-card-refunds]] — save-card, refunds, HUF currency.
- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where CIB Bank is installed / uninstalled.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Pending / Failed / Refunded mapping.
- [[checkout-flow]] — concept page on the storefront checkout.
- [[notification-delivery]] — admin alerts for payment-provider issues.

## Open questions

(none)
