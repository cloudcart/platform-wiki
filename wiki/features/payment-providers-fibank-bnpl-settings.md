---
type: feature
nav_path: "Payment Providers → Fibank BNPL → Settings"
route_name: apps.fibank_bnpl.settings
route_path: /admin/payment-providers/fibank_bnpl/settings
aliases: ["Fibank BNPL Settings", "Fibank BNPL configuration", "Fibank E-Credit settings", "Настройки Fibank BNPL", "Фибанк БНПЛ настройки"]
tags: [paymentproviders, payment-providers, fibank-bnpl, bnpl, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Settings

## Purpose

The Settings tab for Fibank BNPL captures just two things: the **Store Unique ID** issued by Fibank under the merchant's E-Credit contract, and a **minimum order value** below which the Fibank BNPL method is hidden from checkout. Unlike the [[payment-providers-dsk-bnpl-settings|equivalent DSK BNPL screen]] there is NO public-key file upload — Fibank's public key is bundled with CloudCart's code and used automatically. The merchant just types in the Store Unique ID and a minimum-order amount, hits save, and CloudCart validates the credentials by calling Fibank's calculation API with a dummy 200 BGN order.

## Where to find it

Sidebar → **Payment Providers** → **Fibank BNPL** → **Settings** tab.

The route is `/admin/payment-providers/fibank_bnpl/settings`. The page renders the shared payment-provider settings shell with the `fibank_bnpl` provider key and a single settings box titled **Fibank BNPL settings**.

## What the merchant can do here

- Enter the **Store Unique ID** issued by Fibank.
- Set the **Minimum order value** below which Fibank BNPL is hidden on the storefront checkout.
- Edit the standard payment-provider fields (Logo, Title, Description) via the shared payment-provider settings controls.
- Save — the form blocks the save if the Store Unique ID can't successfully fetch a calculation from Fibank.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Store Unique ID** | Unique merchant identifier issued by Fibank (sent as `unicid` in every API request). | Empty | Required (server message: `Store Unique ID is required.`). **Multi-line text input** (`multiLine: true`). Placeholder: *"This Store Unique ID is provided from Fibank"*. Field width: full (`inputSize: 12`). On save, the form calls Fibank's calculation API with a dummy 200 BGN order to verify the credential. If Fibank returns an error, the save fails with that error attached to the field. **No public-key file field** (unlike DSK BNPL Settings) — Fibank's public key is shipped with CloudCart's code. |
| **Minimum order value** | Order total below which Fibank BNPL is hidden from checkout (in BGN). | Empty | Required (server message: `Minimum price is required`). Number input. **In addition to** the global `min_price` / `max_price` controls every payment provider has — both must pass for Fibank BNPL to show on checkout. |
| **Logo / Title / Description** | Customer-facing label and image on the checkout. | Provider defaults | Standard payment-provider settings fields. |

## Business rules

### Saved configuration shape

```json
{
  "store_unique_id": "...",
  "min_price": "100"
}
```

Note the absence of any `public_key` field — Fibank's key is bundled with CloudCart and loaded automatically when the API client is constructed.

### How CloudCart encrypts each call to Fibank

Every API call (`getCalculationForAllSchemes`, `sendFibankPayWithPeriod`, `getFibankPayStatus`) is RSA-encrypted with Fibank's bundled public key before transit. The JSON payload is split into chunks of `(key_bit_length / 8) - 11` bytes, each chunk is encrypted with the public key, the binary result is concatenated and base64-encoded, and the resulting string is sent as `data.data` in the POST body. Endpoint: `https://e-credit.fibank.bg/api/index.php`.

The merchant cannot rotate or replace this key from the settings screen. Key rotation is handled by a CloudCart code update.

### Credentials are validated against Fibank on every save

On save, the platform constructs the API client with the new value and immediately calls Fibank's calculation API with a dummy 200 BGN order. If Fibank rejects the call (bad Store Unique ID, network error, etc.) the error message bubbles back to the form. The merchant cannot save unusable credentials.

### Min order value: two layers

There are TWO minimum-order-value controls for Fibank BNPL:

- **Minimum order value** (this tab) — Fibank BNPL-specific. Used by the storefront when deciding whether to render the BNPL module on a product page.
- **Min/Max amount** (overview tab, shared with all providers) — global per-provider amount range.

Both must pass.

### Test vs live mode

Fibank BNPL has NO test mode toggle in CloudCart. There is only ONE endpoint (`e-credit.fibank.bg`) and one set of credentials. To test, the merchant uses test credentials issued by Fibank.

### Plan-gating

Not plan-gated. Every CloudCart plan can save these settings (assuming the merchant has a Fibank contract).

### What's NOT configured here (and why)

- **Number of installments / monthly payment / interest rate / APR** — set by Fibank per-cart via their pricing API; not configured in CloudCart.
- **Eligible product categories** — set by Fibank on their side per merchant-uploaded category. Map specific products via the [[payment-providers-fibank-bnpl-promotions|Promotions tab]].
- **Customer age / residence / employment requirements** — checked by Fibank during the credit-application step on their hosted page.
- **Refund-side flow** — Fibank BNPL refunds are not exposed in CloudCart's admin; the merchant initiates refunds through Fibank directly.

## Related

- [[payment-providers-fibank-bnpl]] — parent hub for Fibank BNPL.
- [[payment-providers-fibank-bnpl-promotions]] — per-product Fibank promotion-ID mappings.
- [[payment-providers-dsk-bnpl-settings]] — DSK BNPL equivalent settings (similar but adds public-key file upload).
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

- ⏸️ Fibank BNPL RSA public key rotation cadence — Fibank-side process not encoded in CloudCart. Key bundled with platform code; rotation requires a CloudCart release. Merchants should watch CloudCart release notes after a Fibank security advisory.
