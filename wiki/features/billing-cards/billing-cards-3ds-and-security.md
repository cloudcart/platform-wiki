---
type: feature
nav_path: "Profile → Billing → Payment method → 3D Secure & PCI"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["3D Secure", "3DS", "PSD2 SCA", "PCI-DSS scope", "Tokenisation", "Authentication required", "3D Secure validation error"]
tags: [billing, payment-method, 3d-secure, psd2, sca, pci-dss, security]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[billing-cards]]. See the hub for the other aspects (Stripe flow, Braintree flow, HTTPS prereqs, replacement, renewal, display summary).

# Payment cards — 3D Secure & security

## Purpose

This aspect catalogues the security rules that apply to **both** billing-side gateways on the **Payment method** panel: how card data is kept out of CloudCart's PCI scope, the mandatory 3D Secure check at card registration, and the off-session "Authentication required" failure mode that surfaces during renewals.

These rules are **enforced by both gateways and cannot be bypassed from the merchant UI**. The merchant can only retry on a different card or wait for issuer-side fixes.

## Where to find it

- The 3DS pre-authorisation notice is shown above the gateway module on every `/admin/billing/card` panel — Stripe variant (see [[billing-cards-stripe-flow]]), Braintree variant (see [[billing-cards-braintree-flow]]).
- The 3DS challenge UI (OTP / mobile-banking confirmation) is shown by the gateway / the merchant's bank, never by CloudCart.
- 3DS-failure errors surface inline in the panel; "Authentication required" failures from off-session charges surface in [[details-billing]] as transaction-log rows.

## What the merchant can do here

- Complete the 3DS challenge presented by their bank during card registration (OTP entry, mobile-banking confirmation, biometric).
- Retry on a different card if the issuer does not support 3DS 2.x.
- Re-save the same card when an off-session renewal fails with "Authentication required" — re-saving triggers a fresh 3DS handshake at registration, which the next renewal can then re-use.

What the merchant **cannot** do here: skip 3DS at registration, save a card whose `liabilityShifted` is not true on Braintree, or pre-authorise a future off-session renewal that the issuer will challenge (the failure happens at charge time).

## Settings & fields

There are no editable settings on this screen — the 3DS flow is end-to-end controlled by the issuer + the gateway.

Verbatim pre-authorisation notice shown above the module:

> *"In connection with PSD2 SCA regulatory requirements, we will validate your card with 3D Secure validation for the amount of 1 `<currency>`, which will not be debited from the card. After successful validation, the selected card will be charged automatically for all your subscriptions."*

The validation amount (`1 <currency>`) is an authorisation hold, not a real charge. Braintree uses a real `$1`-equivalent hold; Stripe uses its intent-confirmation flow with `off_session` usage type and does not run a separate verification amount in the same way. Both achieve the same outcome: the card is validated as live before being saved.

Verbatim Braintree-side rejection message when 3DS does not liability-shift:

> *"3D Secure validation error"*

## Business rules

### Card data never touches CloudCart — tokenisation only

The card details (PAN, CVV, expiry) are entered directly into the gateway's module (Stripe Payment Element or Braintree Drop-in UI), which runs in the merchant's browser, posts the card data straight to the gateway, and returns a **token / nonce** to CloudCart. CloudCart stores only this token plus the masked card metadata — see [[billing-cards-display-summary]].

**The store is not in PCI-DSS scope for cardholder data.** This is a deliberate architecture decision: by keeping card data out of CloudCart servers, the merchant inherits the gateway's PCI-DSS attestation rather than having to maintain their own.

### 3D Secure is mandatory at card registration

Both gateways enforce 3DS as part of the save flow:

- **Stripe** — the SetupIntent runs through Stripe's normal 3DS flow; some issuers may show an OTP / mobile-banking challenge before the card is saved. The card is not added to the customer's saved methods unless the SetupIntent succeeds — see [[billing-cards-stripe-flow]].
- **Braintree** — the integration rejects a nonce that was not 3D-Secured. If the issuer's `threeDSecureInfo.liabilityShifted` flag is not true, the save throws *"3D Secure validation error"* and no card is stored — see [[billing-cards-braintree-flow]].

This means a merchant cannot save a card whose issuer does not support 3D Secure 2.x — both gateways enforce this. The merchant must retry on a card whose issuer supports 3DS, or contact their bank.

### Off-session renewal failure mode: "Authentication required"

Renewal charges run with `off_session: true` and `confirm: true` (on Stripe; Braintree has an equivalent flow) — meaning the gateway charges the saved default payment method automatically without merchant intervention. But if 3DS is required by the issuer (re-authentication, e.g. for high-value transactions or after a long gap), the off-session charge **fails** rather than challenging the merchant in real-time.

The failure surfaces in [[details-billing]] as a transaction row with response *"Authentication required"*. The merchant must clear this by **re-saving the card** so a fresh 3DS handshake runs at registration — the next off-session renewal can then re-use the freshly authenticated payment method.

### The 3DS challenge UI is the gateway's / bank's, not CloudCart's

When 3DS triggers (at registration or during an interactive Pay-now), the merchant sees the issuer's bank-controlled challenge modal — typically OTP input or mobile-banking confirmation. CloudCart does **not** render this UI. After success (`liabilityShifted: true` on Braintree, `succeeded` SetupIntent status on Stripe), the original cart submits with the verified nonce / payment method. After failure, the merchant sees an inline error and the charge is not retried.

### Tokens are gateway-specific and non-portable

If CloudCart migrates a merchant between gateways (e.g. Braintree to Stripe), the merchant **MUST re-enter their card** after migration because tokens are gateway-specific and don't transfer. There is no in-product migration prompt — this is a support-driven flow; CloudCart support coordinates the timing and notifies the merchant out-of-band when re-entry is required.

### Card data is one-way — no edit, no name change

The merchant cannot edit the cardholder name, address, or any other property of the saved card from the admin. To change anything, they must replace the card entirely. Card metadata stored locally (brand, last 4, expiry, country of issuance) is derived from the gateway response and never editable by the merchant — see [[billing-cards-display-summary]].

## Related

- [[billing-cards]] — hub.
- [[billing-cards-stripe-flow]] — Stripe-side 3DS via SetupIntent.
- [[billing-cards-braintree-flow]] — Braintree-side 3DS + `liabilityShifted`.
- [[billing-cards-renewal-charging]] — where "Authentication required" surfaces.
- [[billing-cards-replacement-and-deletion]] — why re-saving the card is the only fix.
- [[details-billing]] — transaction log where 3DS failures appear.

## Open questions

None.
