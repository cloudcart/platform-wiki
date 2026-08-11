---
type: feature
nav_path: "Payment Providers → TBI Bank"
route_name: apps.tbi_bank.settings
route_path: /admin/payment-providers/tbi_bank
aliases: ["TBI Bank", "TbiBank", "TBI Bank card gateway", "TBI Bank ecomadm", "ТБИ Банк", "ТБИ Банк карти"]
tags: [paymentproviders, payment-providers, tbi-bank, card-payment, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# TBI Bank

## Purpose

**TBI Bank** is CloudCart's integration with TBI Bank's online card-acceptance gateway (their hosted-payment-page product running on the `ecomadm.tbibank.bg` URL — a Sberbank-style gateway that TBI Bank operates). This is **NOT the TBI installment-loan product** — for that the merchant uses [[payment-providers-fusion-pay|Fusion Pay]] (modern) or [[payment-providers-tbi|TBI]] (legacy). The TBI Bank provider is the standard card-payment-gateway integration: customer enters card details on TBI's hosted page, TBI authorises the card, money settles to the merchant's TBI Bank merchant account.

The integration uses **HTTP Basic-auth-style username + password credentials** per environment (test + live). Currencies are **BGN (975)** and **EUR (978)**. Refunds CAN be initiated through the CloudCart admin against the order's reference ID.

## Where to find it

Sidebar → **Payment Providers** → click **TBI Bank**.

The route is `/admin/payment-providers/tbi_bank`. The page renders the standard payment-provider settings shell with the `tbi_bank` provider key. There are no sub-tabs — Settings is the only screen.

## What the merchant can do here

- See the overview card with the TBI Bank logo + description + install/active toggle.
- Install / Uninstall the payment method through the standard buttons.
- Activate / deactivate via the header switch.
- Configure credentials:
  - **Test mode switch**: live vs test.
  - **Username** + **Password** for the active mode.
- Standard payment-provider fields:
  - Logo / Title / Description.
  - Min / Max order amount.
  - Discount.

## Settings & fields

### Credentials

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode switch** | Switches between test and live credentials. | test | Both sets are saved at once; switching only changes which is used. |
| **Username** (live or `_test`) | Merchant username issued by TBI Bank for the gateway. Sent in HTTP form-encoded request bodies as `userName`. | Empty | Required in the active mode. Server message: `"Live username is required."` / `"Test username is required."`. |
| **Password** (live or `_test`) | Merchant password issued by TBI Bank for the gateway. Sent as `password`. | Empty | Required in the active mode. Server message: `"Live Password is required."` / `"Test Password is required."`. |

### Standard payment-provider controls

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo / Title / Description** | Customer-facing label on checkout. | Provider defaults | Standard. |
| **Min / Max amount** | Order-total range for showing TBI Bank on checkout. | None | Standard. |
| **Discount** | Optional checkout discount when customer picks TBI Bank. | None | Standard. |

## Business rules

### How TBI Bank works for the merchant

TBI Bank is a standard hosted-card-gateway integration:

1. **Storefront** — customer adds products to cart, picks TBI Bank at checkout.
2. **Register call** — CloudCart calls TBI's `payment/rest/register.do` with the merchant credentials, order number, amount, currency, return URL, callback URL, and customer description. TBI returns an `orderId` (TBI-side reference) and a `formUrl` (TBI's hosted card page URL).
3. **Redirect to TBI** — CloudCart redirects the customer to `formUrl` to enter card details.
4. **Customer enters card / 3DS** — entire card-data step is on TBI's hosted page.
5. **Customer returns to CloudCart** — TBI redirects back to the return URL with the order's reference attached. TBI also pushes a callback to the dynamic callback URL.
6. **Status sync** — CloudCart calls `payment/rest/getOrderStatusExtended.do` with the reference ID to fetch the order status. CloudCart maps TBI's `orderStatus`:
   - `0` → REQUESTED.
   - `1`, `2` → COMPLETED.
   - `4` → REFUNDED.
   - other → FAILED.

### Currency codes

TBI Bank uses ISO 4217 numeric currency codes in the request:

- BGN → `975`
- EUR → `978`

CloudCart picks one of these based on the order's currency. Other currencies are not supported.

### Endpoints

- **Test**: `https://ecomadmuat.tbibank.bg/`
- **Live**: `https://ecomadm.tbibank.bg/`

POST to `payment/rest/register.do` (registration), `payment/rest/getOrderStatusExtended.do` (status sync), `payment/rest/refund.do` (refund). All form-encoded.

### Refund flow

Unlike most BNPL providers, **TBI Bank refunds ARE API-driven from CloudCart**. CloudCart issues a refund call against the reference ID stored at purchase time. The amount and reference are sent form-encoded; on success TBI returns `orderStatus = 4` which CloudCart maps to Refunded.

### NOT an installment-loan product

The TBI Bank provider only accepts plain card payments. It does NOT split payments over months and does NOT apply for a loan on the customer's behalf. For TBI's installment-loan product, the merchant installs [[payment-providers-fusion-pay|Fusion Pay]] (modern) or [[payment-providers-tbi|TBI]] (legacy) — both completely separate from this provider.

### Plan-gating

Not plan-gated by CloudCart subscription tier.

### Country + currency

Bulgaria-focused. BGN + EUR.

## Deep audit: settings UI surfaces (verified 2026-05-27)

Layout of route `apps.tbi_bank.settings`:

1. **Header + Tabs + Logo/Description + Environment mode radio**.
2. **SettingsBox — TBI Bank-specific** (two cards — exactly one visible based on mode):
   - **TBI Bank settings (Live)** (key `live`, edit method `slide`, **`isVisible: mode === 'live'`**, lock when `mode === 'test'`). Two required string fields:
     - `configuration.live_username` — required string. Label "Username".
     - `configuration.live_password` — required string. Label "Password".
   - **TBI Bank settings (Test)** (key `test`, edit method `slide`, **`isVisible: mode === 'test'`**, lock when `mode === 'live'`). Two required string fields:
     - `configuration.test_username` — required string.
     - `configuration.test_password` — required string.
3. **Common rows** — Amount from/to + Discounts.
4. **SubmitChanges** sticky bar.

### Per-field validation (`TbiBank/ConfigurationValidator.php`)

| Field | Rule | Message |
|---|---|---|
| `configuration.test_username` | `required_if:configuration.mode,==,test` | "Test username is required." |
| `configuration.test_password` | `required_if:configuration.mode,==,test` | "Test Password is required." |
| `configuration.live_username` | `required_if:configuration.mode,==,live` | "Live username is required." |
| `configuration.live_password` | `required_if:configuration.mode,==,live` | "Live Password is required." |

`configurationDefault.tbi_bank = { mode: 'test', discount_type: 'flat' }`.

### Conditional UI behaviour

- Only one mode's card is rendered at a time (`isVisible` toggles entirely).

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-fusion-pay]] — TBI Bank's installment-loan product (not this card gateway).
- [[payment-providers-tbi]] — legacy TBI installment provider (calculator-only).
- [[payment-providers-borica-way4]] — Borica Way4 card-payment gateway with a similar register/sync API shape.
- [[payment-providers-mypos]] — myPOS card-payment gateway with a similar hosted-form flow.

## Open questions

- ⏸️ 3DS step-up behaviour depends on TBI Bank's hosted-page configuration. The underlying gateway protocol handles 3DS automatically on its own hosted page when the card requires it; CloudCart does not flag or branch on 3DS, nor surface a separate Pending state for 3DS step-up.
