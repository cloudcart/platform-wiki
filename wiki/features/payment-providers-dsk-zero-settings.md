---
type: feature
nav_path: "Payment Providers → DSK Zero → Settings"
route_name: apps.dsk_zero.settings
route_path: /admin/payment-providers/dsk_zero/settings
aliases: ["DSK Zero Settings", "DSK 0% settings", "Настройки DSK Zero", "ДСК Зеро настройки"]
tags: [paymentproviders, payment-providers, dsk-zero, bnpl, settings, zero-interest]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Settings

## Purpose

The Settings tab for DSK Zero captures just three things: the merchant's **agreement number / merchant ID** (whatever DSK Bank issued for the merchant's zora contract — the field is intentionally generic), the **contact email** DSK Bank uses for the offline order workflow, and a switch that decides whether CloudCart sends an automated email after every DSK Zero order is completed. There's no API key, no public key, no test/live mode — DSK Zero is a curated-list integration with no real-time API to DSK at storefront calculation time. The credentials here are used only as the "to/from" of the operational notification email and as a token DSK can use to reconcile the order on their side.

## Where to find it

Sidebar → **Payment Providers** → **DSK Zero** → **Settings** tab.

The route is `/admin/payment-providers/dsk_zero/settings`. The page renders `SettingsFormPayments` with the `dsk_zero` provider key and a single settings box titled **DSK Bank 0% settings**.

## What the merchant can do here

- Toggle **Send an email after completing an order** — when ON, CloudCart sends an operational email to the configured email address after each DSK Zero order is completed.
- Enter the **Email address** DSK Bank uses for the offline approval workflow.
- Enter the **Agreement or Merchant ID** issued by DSK Bank under the zora program.
- Edit the standard payment-provider fields (Logo, Title, Description) via the shared payment-provider settings controls.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Send an email after completing an order** | Toggles the automated DSK-notification email on every order completion. | OFF | Switch. When ON, the merchant typically also needs to enter the **Email** field below. The system uses this as the loop that informs DSK Bank an order needs processing. |
| **Email address** | Contact email at DSK Bank where order-completion notifications are sent (when the switch above is ON). | Empty | Required (server message: `Email is required.`). Must be a valid email (`Entered email is invalid.`). The default for new integrations is `the provider's support address` — the merchant can override it if DSK has assigned a different inbox to their account. |
| **Agreement or Merchant ID** | Merchant identifier or contract / agreement number issued by DSK Bank under the zora program. Stored as the `id` configuration key. | Empty | Required (server message: `Number of agreement is required.`). Free text. CloudCart does NOT validate this against DSK — it's a passthrough string used in the notification email and stored for the merchant's reference. |
| **Logo / Title / Description** | Customer-facing label and image on the checkout. | Provider defaults | Standard payment-provider settings fields. |

## Business rules

### Saved configuration shape

```json
{
  "send_email_after_checkout": true,
  "email": "the provider's support address",
  "id": "...agreement number..."
}
```

These three keys are the entire DSK Zero credentials surface. There are no public keys, no API tokens, no test-mode flags, no signature secrets.

### No live API to DSK Bank during checkout

Unlike [[payment-providers-dsk-bnpl|DSK BNPL]] (which calls DSK's calculation API live for every customer at checkout), DSK Zero does NOT hit DSK Bank at storefront pricing time. The 0% installment plans the customer sees are calculated entirely locally with a 0% monthly rate. The credentials on this tab are operational tokens only — they're never sent as authentication headers to a DSK API.

### What the merchant DOES NOT set here

- **Number of installments / which months are offered** — set on the [[payment-providers-dsk-zero-schemes|Schemes tab]] per scheme.
- **Eligible products** — set per-scheme on the [[payment-providers-dsk-zero-schemes|Schemes tab]].
- **Interest rate** — hard-coded to 0% (it's literally the product's name).
- **Minimum order value** — not a DSK Zero-specific field; merchants use the standard provider-wide Min/Max amount on the overview tab if they need this.
- **Customer eligibility criteria** — DSK Bank decides during the offline approval workflow.

### Plan-gating

Not plan-gated by CloudCart subscription tier. Gated by the store-level `zora` enrollment — non-zora stores can't see this provider at all (see [[payment-providers-dsk-zero#zora-only-gating|Zora-only gating]] on the parent page).

### Email format

The notification email sent to DSK on order completion is the standard CloudCart site-mail template — the contents typically include the order number, customer name, total amount, picked months, and a link for DSK staff to follow up. The merchant doesn't customise this email body from the settings tab.

## Related

- [[payment-providers-dsk-zero]] — parent hub for DSK Zero.
- [[payment-providers-dsk-zero-schemes]] — the (months, products) scheme list — what the customer actually picks at checkout.
- [[payment-providers-dsk-bnpl-settings]] — the equivalent settings screen for DSK BNPL, which has a much richer credential surface (Store Unique ID, public key, etc.) because it actually hits DSK's API.
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

_None._
