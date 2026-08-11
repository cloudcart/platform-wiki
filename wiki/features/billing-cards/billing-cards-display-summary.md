---
type: feature
nav_path: "Profile → Billing → Payment method → Display summary"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["Card summary", "Masked card", "Read-only card display", "Card brand", "Last 4", "Card metadata", "Card logo"]
tags: [billing, payment-method, display, masked-card, metadata]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-cards]]. See the hub for the other aspects (Stripe flow, Braintree flow, 3DS + security, HTTPS prereqs, replacement, renewal).

# Payment cards — display summary & stored metadata

## Purpose

Wherever the merchant sees their saved card in the CloudCart admin, the display is always the same **read-only masked summary** — never the full card number, never editable. This aspect documents the exact summary format, every place in the admin it's shown, the fields stored locally for it, and the data CloudCart receives from each gateway.

The merchant can use this summary to confirm which card is on file before letting a charge run (e.g. before launching a paid Service purchase) and to verify they replaced the correct card after editing.

## Where to find it

The masked summary appears in every billing-touchpoint surface in the admin:

- **Invoicing details sidebar** on [[billing-invoicing]] — next to the invoicing block; pencil icon opens the replacement panel.
- **Subscriptions list header** on [[subscriptions]] — shows which card pays for these renewals.
- **Services purchase confirmation** on [[services]] — shows which card the merchant is about to charge.
- **Checkout panel** ([[plans-purchase]]) — collapses to the summary after the merchant saves the card via the inline `FormStripe.vue` / `FormPayments.vue` editor.
- **Billing landing area** (Profile dropdown → Billing) — top-level summary block.

A pencil icon next to the summary always opens the relevant card-replace panel — see [[billing-cards-replacement-and-deletion]].

## What the merchant can do here

- **Read** which card is on file by brand + last 4 + expiry.
- **Click the pencil icon** to open the card-replacement panel — see [[billing-cards]] for the panel entry points.

What the merchant **cannot** do here:

- View the full card number, CVV, cardholder name, or full expiry beyond month/year.
- Edit any of the displayed fields — the entire summary is read-only.
- Copy the gateway token — it is not surfaced anywhere in the UI, only stored on the server for renewal charges.

## Settings & fields

The standard summary format is:

```
<cardType (UPPERCASED)> <maskedNumber> Exp. <expirationDate>
```

Concrete example: `VISA **** 1234 Exp. 05/27`.

Fields rendered in the summary:

| Field | Source | What the merchant sees |
|-------|--------|------------------------|
| `cardType` | Gateway response (Visa / Mastercard / Amex / Maestro / etc.) | UPPERCASED brand name |
| `maskedNumber` | Gateway response | `**** **** **** 1234` (last 4 visible) |
| `expirationDate` | Gateway response | `MM/YY` (month / year only) |

The card brand may also render as a small **logo icon** next to or in place of the brand name, depending on the surface. The logo URL is provided by the gateway response and stored locally.

## Business rules

### Only masked metadata is stored locally

After successful tokenisation (see [[billing-cards-stripe-flow]] / [[billing-cards-braintree-flow]]), CloudCart receives and stores the masked summary returned by the gateway — never the full card data. The fields stored locally are:

- **Card brand** (`Visa`, `Mastercard`, `Amex`, `Maestro`, etc.).
- **Masked number** (`**** **** **** 1234`).
- **Expiry month** and **expiry year**.
- **Country of issuance** — used for VAT calculation on the CloudCart invoice the merchant receives, see [[billing-invoicing]].
- **Logo URL** — the gateway-provided URL for the brand icon.
- **Raw gateway token** — the only data needed to charge the card on the next renewal. Never surfaced in the UI.

The token is what subsequent renewal charges use. Cards are charged via the same gateway's transactions API — see [[billing-cards-renewal-charging]].

### Card summary is always read-only

There is no edit control next to the summary anywhere in the admin. To change anything — including the cardholder name (the brand or last 4 won't change, so the merchant typically doesn't see a need to re-save) — the merchant must replace the card entirely. See [[billing-cards-replacement-and-deletion]] for the replacement-only paradigm and [[billing-cards-3ds-and-security]] for why edits aren't permitted.

### Single card displayed everywhere

Because CloudCart's billing model is **one card per merchant** (see [[billing-cards-replacement-and-deletion]]), every surface that shows the card shows the **same** card — the gateway customer's default payment method. There is no per-subscription card display, no card-picker, no "this subscription was charged on a different card" indicator.

### Country of issuance drives VAT on CloudCart invoices

The country of issuance returned by the gateway is one of the inputs the platform uses when computing VAT for the CloudCart-side invoice the merchant receives — see [[billing-invoicing]]. The merchant's invoicing country (from the [[billing-invoicing]] form) is the primary driver, but the card-issuance country can be cross-referenced for risk-check purposes.

### Logo URL is gateway-provided, not stored locally

The brand-logo icon URL is taken straight from the gateway response. If the gateway changes the URL, the local copy may go stale until the next card replacement refreshes the metadata. This is rare in practice — gateway-provided logo URLs are stable for years.

### After save, the inline Checkout panel collapses to the summary

In Checkout's inline `FormStripe.vue` / `FormPayments.vue` editor (see [[billing-cards-stripe-flow]] / [[billing-cards-braintree-flow]]), after the merchant saves the card, the inline form collapses back to the same read-only summary (brand + last 4 + expiry) so the parent Checkout panel can submit Pay-now without the merchant having to re-enter or re-confirm card details.

### Summary string is consistent across surfaces

The format `VISA **** 1234 Exp. 05/27` is rendered identically across Smarty, the application framework, and Vue surfaces. The merchant sees the same summary on [[billing-invoicing]], [[subscriptions]], [[services]], the [[plans-purchase]] Checkout, and the Billing landing area — minimising confusion when the merchant verifies "is this the right card?".

## Related

- [[billing-cards]] — hub.
- [[billing-cards-stripe-flow]] — Stripe-side metadata source.
- [[billing-cards-braintree-flow]] — Braintree-side metadata source.
- [[billing-cards-replacement-and-deletion]] — why the summary is the only mutation surface (via the pencil → replacement panel).
- [[billing-invoicing]] — country-of-issuance is cross-referenced for VAT on the CloudCart invoice.
- [[subscriptions]] — header bar that shows the card paying for renewals.
- [[services]] — purchase confirmation that shows the card about to be charged.
- [[plans-purchase]] — Checkout panel summary.

## Open questions

None.
