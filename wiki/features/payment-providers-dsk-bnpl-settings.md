---
type: feature
nav_path: "Payment Providers → DSK BNPL → Settings"
route_name: apps.dsk_bnpl.settings
route_path: /admin/payment-providers/dsk_bnpl/settings
aliases: ["DSK BNPL Settings", "DSK BNPL configuration", "Настройки DSK BNPL", "ДСК БНПЛ настройки"]
tags: [paymentproviders, payment-providers, dsk-bnpl, bnpl, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Settings

## Purpose

The Settings tab is where the merchant enters the three pieces of information needed to connect their CloudCart store to DSK Bank's BNPL API: the **Store Unique ID** issued by DSK, the **public-key PEM file** issued by DSK (used to encrypt every API request), and a **minimum order value** below which the DSK BNPL method is hidden from checkout. Saving these settings triggers an immediate API call to DSK's `getCalculationForAllSchemes` endpoint with a dummy 200 BGN price — if DSK rejects the credentials, the form refuses to save and shows the error against the Store Unique ID field.

The merchant gets the Store Unique ID and the PEM file from DSK Bank as part of the DSK Pay merchant onboarding. They are NOT created in CloudCart and cannot be regenerated from this screen.

## Where to find it

Sidebar → **Payment Providers** → **DSK BNPL** → **Settings** tab.

The route is `/admin/payment-providers/dsk_bnpl/settings`. The page renders `SettingsFormPayments` with the `dsk_bnpl` provider key and a single settings box titled **DSK Bank BNPL settings**.

## What the merchant can do here

- Enter the **Store Unique ID** issued by DSK Bank.
- Upload the **Public key** PEM file issued by DSK Bank.
- Set the **Minimum order value** below which DSK BNPL is hidden on storefront checkout.
- Edit the standard payment-provider fields (Logo, Title, Description) via the shared `SettingsFormPayments` controls.
- Save — the form blocks the save if the Store Unique ID can't successfully fetch a calculation from DSK.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Store Unique ID** | Unique merchant identifier issued by DSK Bank (`unicid` in every API request). Required for the integration to work at all. | Empty | Required (server message: `Store Unique ID is required.`). **Multi-line text input** (the codebase explicitly uses `multiLine: true` — accommodates long IDs DSK sometimes issues on multiple lines). Placeholder: *"This Store Unique ID is provided from DSK Bank"*. Field width: `inputSize: 12` (full width). The form validates the value by calling DSK's `getCalculationForAllSchemes` API on save — if DSK returns an error, the save fails with that error attached to the field. |
| **Public key** | PEM-encoded RSA public key issued by DSK Bank. CloudCart uses this to encrypt every API request before sending (chunked, base64-encoded). | Empty | Required on first save (server message: `Public key is required.`). File upload field (`type: "file"`), accepts `.pem`. Help block: *"Choose the public key pem file provided by DSK Bank"*. CloudCart validates the file with `openssl_pkey_get_public` and stores the file contents in the configuration. On edit, the merchant only re-uploads if the key changes — leaving the file field empty keeps the previously saved key. |
| **Minimum order value** | Order total below which DSK BNPL is hidden from checkout (in BGN). | Empty | Required (server message: `Minimum price is required`). Number input. **This minimum is in addition to** the global `min_price` / `max_price` controls every payment provider has — both must pass for DSK BNPL to show. The Promotions sub-tab also enforces this minimum when rendering the per-product installment table. |
| **Logo / Title / Description** | Customer-facing label and image on the checkout. | Provider defaults | Standard fields from `SettingsFormPayments`. |

## Business rules

### Saved configuration shape

The merchant's saved configuration ends up as a JSON blob on the payment-provider configuration row with these keys:

```json
{
  "store_unique_id": "...",
  "public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n",
  "min_price": "100",
  "promo_html": "..." // managed on the Promotions tab, not here
}
```

The `promo_html` key is editable from the Promotions tab and stored alongside the credentials but is not displayed on this Settings tab.

### How CloudCart encrypts each call to DSK

Every API call (`getCalculationForAllSchemes`, `sendDskPayWithPeriod`, `getDskPayStatus`) is RSA-encrypted with the merchant's saved public key before transit. The JSON payload is split into chunks of `(key_bit_length / 8) - 11` bytes, each chunk is encrypted with the public key, the binary result is concatenated and base64-encoded, and the resulting string is sent as `data.data` in the POST body. Endpoint: `https://merchantsonline.dskbank.bg/api/index.php`.

If the merchant uploads an invalid PEM file, the platform's public-key load fails and the merchant sees "Invalid public key file" attached to the public_key field.

### Credentials are validated against DSK on every save

On save, the platform constructs the API client with the new values and immediately calls DSK's calculation API with a dummy 200 BGN order. If DSK rejects the call (bad credentials, network error, malformed key) the error message bubbles back to the form. This means: **the merchant cannot save unusable credentials.** The form refuses to save until DSK's API accepts the configuration.

### Min order value: two layers

There are TWO minimum-order-value controls in play for DSK BNPL:

- **Minimum order value** (this tab) — DSK BNPL-specific. Used by the storefront when deciding whether to render the BNPL module on a product page and by the pricing-table endpoint to raise the localized error: `"Minimum order amount {X} exceeds product price {Y}"`.
- **Min/Max amount** (overview tab, shared with all providers) — global per-provider amount range.

Both must pass; the merchant typically sets just one of them (typically this BNPL-specific `min_price`) and leaves the global range empty.

### Test vs live mode

DSK BNPL has NO test mode toggle in CloudCart. There is only ONE endpoint (`merchantsonline.dskbank.bg`) and one set of credentials. To test the integration, the merchant uses test credentials issued by DSK Bank in their pre-production environment — the credentials themselves determine which DSK environment is hit, not a switch in the admin panel.

### Plan-gating

Not plan-gated. Every CloudCart plan can save these settings.

### What's NOT configured here (and why)

- **Number of installments / monthly payment / interest rate / APR** — set by DSK Bank per-cart via their pricing API; not configured in CloudCart.
- **Eligible product categories** — set by DSK Bank on their side using the DSK promotion ID system. Map products via the [[payment-providers-dsk-bnpl-promotions|Promotions tab]].
- **Customer age / residence / employment requirements** — checked by DSK Bank during the credit-application step on their hosted page. Not configurable from CloudCart.
- **Refund-side flow** — DSK BNPL refunds are not exposed in CloudCart's admin; the merchant initiates refunds through DSK Bank directly.

## Related

- [[payment-providers-dsk-bnpl]] — parent hub for DSK BNPL.
- [[payment-providers-dsk-bnpl-promotions]] — per-product DSK promotion-ID mappings + the `promo_html` rich-text snippet.
- [[payment-providers]] — top-level Payment Providers area.
- [[payment-providers-fibank-bnpl-settings]] — near-identical Settings shape for the Fibank BNPL provider (same Store Unique ID + min-price pattern, but Fibank ships its public key bundled with CloudCart rather than asking the merchant to upload it).

## Open questions

- ⏸️ RSA key rotation workflow on DSK's side (frequency, who initiates it, key delivery channel) is a bank-side process not encoded in CloudCart. If DSK rotates the merchant's key pair, the merchant re-uploads the new PEM here.
