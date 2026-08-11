---
type: feature
nav_path: "Payment Providers → UBB"
route_name: apps.ubb.overview
route_path: /admin/payment-providers/ubb
aliases: ["UBB", "United Bulgarian Bank", "Обединена Българска Банка", "ОББ", "Виртуален ПОС ОББ", "Плащане с карта - ОББ", "UbbService"]
tags: [paymentproviders, payment-providers, ubb, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# UBB

## Purpose

**UBB** (United Bulgarian Bank / Обединена Българска Банка / ОББ) is the bank-card gateway for merchants with an e-commerce contract through **ОББ** (part of KBC Group). The customer is redirected to UBB's hosted Cardgate-style payment page (the *Universal Plug-in* / *CGN* protocol), enters their Visa / Mastercard / Maestro card, and on a successful 3DS challenge the money settles to the merchant's UBB business account.

Setup uses a single proprietary **encrypted resource bundle** — UBB issues each merchant a binary `.cgn` (Cardgate) file holding the terminal credentials and signing keys. The merchant uploads it as-is; no usernames, passwords, or separate certificate. Storefront default label: *"United Bulgarian Bank"* / *"Обединена Българска Банка"*.

Supported: redirect to UBB's hosted page, status callback on `responseurl`, mandatory 3DS. Not supported: saved cards, Authorize + Capture (single-message capture only), native partial refunds.

## Where to find it

Sidebar → **Payment Providers** → click **UBB**.

Route: `/admin/payment-providers/ubb`. Route name: `apps.ubb.overview`. Standard payment-provider overview, no sub-tabs.

## What the merchant can do here

- **Install / Uninstall** the payment method via the standard overview buttons.
- **Activate / Deactivate** using the header switch.
- **Upload the UBB-issued resource file** (`.cgn` Cardgate bundle). The platform reads the terminal alias from the bundle and stores it for confirmation.
- **Pick an action** — `1` (default / Sale) is the standard payment action.
- **Configure standard payment-method options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount.

UBB has no dedicated settings panel — it uses the platform's default settings form, which surfaces the file upload, the action selector, and the standard form rows.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override on storefront checkout. | Provider default | Standard. |
| **Title / Description** | Customer-facing label. Storefront default reads "United Bulgarian Bank" (en) / "Обединена Българска Банка" (bg). | "United Bulgarian Bank" | Standard. |
| **Amount from / to** | Order total range where UBB appears at checkout. | Empty (any amount) | Standard. |
| **Discount** | Optional fixed / percent discount when buyer picks UBB. | None | Standard. |
| **Resource file** | UBB-issued binary `.cgn` Cardgate bundle. | Empty | Required. MIME must be `application/octet-stream`. The terminal alias is read from the bundle — if none can be extracted, save fails with *"Invalid resource file"*. If missing on first save: *"Resource file is required"*. |
| **Resource name (read-only)** | The terminal alias the bundle was issued for. | Auto-populated | Confirms the right bundle was uploaded. |
| **Action** | UBB Cardgate operation code. `1` = Sale (the default). | `1` | Other action codes exist in the protocol but Sale is what e-commerce uses. |

## Business rules

### 3-D Secure is mandatory

Every UBB charge runs through 3DS on UBB's hosted page. The merchant cannot disable 3DS — it's the bank's policy. The customer is redirected to UBB's payment page (URL is read from UBB's response `PAYMENTPAGE` field), completes the 3DS challenge, and is bounced back to the platform's webhook URL.

### Card networks supported

Visa, Mastercard, Maestro. Amex / JCB / Diners are typically not enabled on UBB Cardgate terminals.

### Currency support

UBB Cardgate terminals are provisioned at the bank for a specific currency — typically **BGN** for Bulgarian merchants. The platform does NOT send an explicit currency code on each transaction, so the terminal's own configuration determines acceptance. There is no per-environment currency dropdown on this page. EUR acceptance is possible at the bank level for merchants with the right contract. The merchant should align store currency with the terminal's currency. The amount is sent divided by 100 (input in stotinki/cents).

### Webhook / response URL

The merchant configures the UBB terminal to call:

```
<cc_payments_domain>/webhook/ubb
```

This is sent as both `responseurl` and `errorurl` on every UBB request. UBB calls it with `paymentid=<UBB transaction id>` plus response codes. The platform reads `result` to determine status:

| UBB `result` | Mapped platform [[payment-status]] |
|--------------|-----------------------------------|
| `CAPTURED`, `APPROVED` | `Completed` |
| `CANCELED`, `NOT CAPTURED`, `NOT APPROVED` | `Canceled` |
| anything else (no `result` field) | `Pending` / `Failed` |

After processing, the platform returns `REDIRECT=<payment-return-url>`; UBB then redirects the customer's browser there.

### Order ID / tracking ID

The platform sends `trackid` — a short unique reference generated per payment. UBB stores it as the merchant's reference and includes it in callbacks. The callback `paymentid` is UBB's internal transaction reference.

### Redirect-to-payment-page flow

UBB's hosted payment page URL comes back in the `PAYMENTPAGE` field of UBB's create-payment response. The platform then shows a redirect page that auto-submits the customer to UBB's page.

### Encrypted resource bundle (`.cgn`)

UBB's IT team generates the per-merchant binary bundle (it embeds the terminal alias, signing key, and encryption keys). The merchant gets it via email or UBB's portal and uploads it as-is — the platform never asks for separate merchant ID, terminal ID, or secret. This makes UBB easier to set up than Borica (no CSR), but **harder to debug**: neither the merchant nor CloudCart support can inspect the bundle's contents. If a transaction is rejected with a generic error, the merchant must contact UBB support directly.

### No Authorize + Capture, no saved cards, no wallets

The integration is **single-message capture only** — no pre-authorize / delayed-capture, no saved-card tokenisation, no Google Pay / Apple Pay. If the merchant needs these, see [[payment-providers-borica-way4]] or [[payment-providers-cloudcart-pay]].

### Refund support

There is no working refund from CloudCart's admin yet. Refunding a UBB payment must be done from UBB's own merchant portal. The merchant can still mark the order as refunded via [[orders-payment-refund]], but the financial reversal happens at UBB.

### iframe option (legacy)

The configuration stores an `enable_iframe` boolean — historically the UBB payment page could be embedded in an iframe instead of a full redirect. This flag is not exposed in the UI today.

### Plan-tier gating

The provider has no plan gate. Any plan that allows payment providers can install UBB.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[orders-payment-refund]] — initiates a manual refund flag on the order (financial reversal happens in UBB's portal).
- [[orders-payment-manual]] — manual payment entry (offline / outside UBB).
- [[payment-providers-borica-way4]] — multi-bank alternative if the merchant wants saved cards / Authorize + Capture / wallets / partial refunds.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway if the merchant doesn't have a UBB e-commerce contract.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Canceled / Pending mapping for UBB charges.
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

- ⏸️ Whether a EUR UBB terminal accepts a CloudCart store's request is a UBB-side terminal-config question. The integration sends amount only (no explicit currency code in the create-payment call), so the terminal's own currency configuration determines acceptance.
