---
type: feature
nav_path: "Payment Providers → Mollie"
route_name: apps.mollie.settings
route_path: /admin/payment-providers/mollie
aliases: ["Mollie", "Mollie payments", "Mollie EU"]
tags: [paymentproviders, payment-providers, mollie, international, eu, card-gateway, ideal]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Mollie

## Purpose

Mollie is a European payment service provider (PSP). A single integration exposes the methods the merchant has enabled in their Mollie dashboard — iDEAL, Bancontact, SEPA Direct Debit, cards (Visa/Mastercard/Maestro/Amex), Apple Pay, Klarna BNPL, PayPal, Sofort, Giropay, KBC, ING, Belfius, Trustly, EPS, and more. The customer picks one at Mollie's hosted checkout page. Mollie is the recommended option for **EU-focused stores** wanting native-method coverage across the Netherlands, Belgium, Germany, France, Austria, and surrounding markets.

## Where to find it

Payment Providers → **Mollie**. URL `/admin/payment-providers/mollie`, route name `apps.mollie.settings`. Permission: `hasApiPermission:settings,store.payment_providers`.

## What the merchant can do here

- Toggle the provider **Active** (header status bar with mode pill + Enable/Disable button).
- Switch **Test mode** / **Live mode** (radio card; border colour follows mode).
- Enter the **Profile ID**, **Test API key** (`test_...`), and **Live API key** (`live_...`).
- Set the storefront name + logo, accepted-amount range, and an optional discount when paying with Mollie (common option group).

## Settings & fields

All three Mollie-specific fields live in one **Mollie setup** card (key `configuration`, slide edit). The Test/Live key rows show or hide based on the mode toggle (`dependField: configuration.mode`); Profile ID is always visible. Default `configuration = { discount_type: 'flat', mode: 'test' }`.

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | ON = sandbox, OFF = live. Active mode picks which key is read at runtime. | Test mode ON | Stored as `configuration.mode = "test"` or `"live"`. |
| **Profile ID** (`configuration.profile_id`) | Mollie Profile ID — record of which Mollie website/sub-account the key belongs to. | empty | Required. Message: "Profile id is required". See Business rules — not sent at runtime. |
| **Test API key** (`configuration.test_api_key`) | Sandbox key (`test_...`). | empty | Required (unconditional). Message: "Test API key is required". |
| **Live API key** (`configuration.live_api_key`) | Production key (`live_...`). | empty | Required (unconditional). Message: "Live API key is required". |
| **Storefront name** | Display name on storefront. | "Mollie" | Common option. |
| **Logo** | Provider logo. | Mollie default | Common option (`PaymentLogoSection`). |
| **Amount from / Amount to** | Order-amount range when Mollie is offered. | empty / empty | Common gate. |
| **Discount when paying with Mollie** | Flat / percent / shipping-free discount. | none | Common option. |

**Backend requires BOTH keys regardless of mode.** The validator rules are plain `required` (not `required_if:mode,...`) for `test_api_key` AND `live_api_key`. The form hides the opposite mode's key row, so a merchant who fills only the test key in Test mode is still rejected with "Live API key is required". To save, supply **both** keys. (Messages come from the validator's `attributes` labels; `messages` is empty, so the application framework's default "required" wording is used with these labels.)

## Business rules

### Customer flow at checkout

1. Customer picks Mollie; CloudCart creates a `Payment` row.
2. CloudCart calls Mollie's `payments` API with: amount in **EUR** (see currency rule), description `"Order #{order_id}"` (using the increment hash when `order_id_display` is `increment_hash`), locale (if supported), return/cancel/notify URLs, and metadata `{order_id}`.
3. Mollie returns a payment with `id` (`tr_...`) + `checkoutUrl`. CloudCart stores `tr_id` as `provider_reference_id`; status → `requested`.
4. Customer is redirected to Mollie's hosted checkout, picks a method, and completes it.
5. Mollie redirects to the `site.payment.return` route → status moves to `pending` (Mollie may not yet know the bank-side outcome).
6. Mollie sends an **IPN webhook**; CloudCart fetches the final status and updates `Payment.status`.

### Currency — EUR-only

The integration **always sends EUR to Mollie**, converting from the store's currency first (iDEAL, Bancontact, and SEPA are EUR-only by design). Non-EUR stores: the customer sees EUR amounts at Mollie checkout, and Mollie's exchange rate may differ slightly from CloudCart's at-checkout rate.

### Webhook → status sync

The webhook URL is `route('payments.webhook', 'mollie')` — typically `https://<cc-payments-domain>/webhook/mollie`. **It must be publicly reachable** (no `localhost`, IP-whitelisting, or basic auth); the `cc-payments` host is publicly resolvable. If a custom-deployed store's firewall blocks Mollie's IPs, webhooks fail and payments stick in `pending` indefinitely. The handler does **not** parse the POST body — it re-fetches the payment from Mollie via authenticated API call, so a spoofed notification cannot change status. Outside webhooks, the platform can also poll on demand (e.g. when the merchant opens the order) — same fetch path, same mapping.

Mollie status → CloudCart [[payment-status]]:

- `paid`, `authorized` → **Completed**
- `pending` → **Pending**
- `failed`, `expired` → **Failed**
- `canceled` → **Cancelled**
- Refunded / partially refunded → **Refunded**
- Any other value (including `open`) → **Requested**

### Other behaviour

- **Profile ID is not sent at runtime.** The active Profile is inferred by Mollie from the API key; the field is only a settings-form record. An unset Profile ID does not break payments — the validator is the only constraint.
- **Available methods are managed in the Mollie dashboard**, not CloudCart. There are no per-method code paths; Mollie's hosted page shows whatever is enabled and applicable to the customer's country/currency.
- **3D Secure** is handled by Mollie automatically for cards; non-card methods use their own authentication.
- **Refunds** supported via the payment record's Refund button (calls Mollie's refund API with the saved `tr_id`). Full-amount only — partial refunds are not surfaced in the UI. Processed asynchronously (hours/days to reach the bank).
- **Capture** is automatic; no manual-capture control. Funds settle into the merchant's Mollie balance.
- **Recurring / SEPA mandates and saved cards / tokenization are not implemented** — this integration is one-off purchase only.
- **Locales** passed when supported: `en_US, nl_NL, nl_BE, fr_FR, fr_BE, de_DE, de_AT, de_CH, es_ES, ca_ES, pt_PT, it_IT, nb_NO, sv_SE, fi_FI, da_DK, is_IS, hu_HU, pl_PL, lv_LV, lt_LT` (otherwise Mollie's default).
- **No plan gate** — available on every plan.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-stripe]] — alternative international card gateway.
- [[payment-providers-paypal]] — wallet alternative.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.
- [[payment-status]] — status enum the Mollie statuses map onto.

## Open questions

(none)
