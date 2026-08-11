---
type: feature
nav_path: "Payment Providers → Borica Way4"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica", "Borica Way4", "Borica 3DS", "ПОС терминал Borica", "Виртуален ПОС Borica", "BoricaWay4", "Plashtane s karta - Borica", "Card payments - Borica"]
tags: [paymentproviders, payment-providers, borica-way4, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 3
---

# Borica Way4

## Purpose

**Borica Way4** is the main Bulgarian bank-card gateway on CloudCart — the merchant accepts Visa / Mastercard / Maestro / JCB / Diners / Amex payments through a 3-D Secure redirect to Borica's "Way4" hosted payment page, then receives settlement to whichever Bulgarian bank issued the merchant's e-commerce contract (most BG banks — UniCredit, ProCredit, Postbank, Allianz, etc. — process card e-commerce through Borica's national switch). The integration uses asymmetric RSA signatures: each merchant has their own **terminal ID** plus a **private key + public certificate** pair issued by Borica.

This is the gold-standard card gateway for Bulgarian merchants — the most-deployed, most feature-complete card integration on the platform: **Save customer card** (tokenisation through `MERCH_TOKEN_ID`), **Authorize + Capture** flow (delayed / manual capture), **partial refund** (protocol-allowed; no admin UI input), **Google Pay** and **Apple Pay** wallets through Borica's MPay surface, **BGN or EUR currency**, and synchronous + IPN status reconciliation. The merchant generates a Certificate Signing Request (CSR) from CloudCart, sends it to Borica, gets back a signed certificate, uploads it, and the integration is live.

This hub catalogues the six aspect pages this feature splits into. The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

Sidebar → **Payment Providers** → click **Borica Way4** (or "Pay with card" — the storefront-facing label). Route: `/admin/payment-providers/borica_way4`.

The page renders the standard payment-provider overview used by all payment providers. From there the merchant lands on the **Settings** tab — there are no sub-tabs (no Onboarding, Transactions, Payouts surfaces, unlike CloudCart Pay) because Borica settlement and reporting is done through the merchant's own bank, not through CloudCart.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages:

- [[borica-way4-setup-csr]] — the Terminal ID + CSR + certificate-upload onboarding flow; the bundled `V1800001` shared test terminal; the live-mode certificate gate.
- [[borica-way4-settings-fields]] — full settings layout fields (Mode, MID, `EGW_SECURITY` `MAC_GENERAL` vs `MAC_ADVANCED`, Currency BGN / EUR, Logo / Title / Description, Amount range, Discount, EGW_MERCH_BACKREF return URL, EGW_TERM_GROUP).
- [[borica-way4-payment-lifecycle]] — purchase request, mandatory MPI_OW_APGW 3-D Secure, redirect, return + IPN (`<cc_payments_domain>/return/provider/borica_way4`), `P_SIGN` verification, Borica response-code (`RC`) → payment-status mapping.
- [[borica-way4-authorize-capture]] — two-phase Authorize + Capture flow; `TRTYPE` 12 / 21 / 22; the 7-day Borica capture window; `authorize_payment` plan-feature gate.
- [[borica-way4-save-card-wallets]] — Save Customer Card tokenisation (`MERCH_TRAN_STATE=S` + `MERCH_TOKEN_ID`); Google Pay / Apple Pay (MPay) flow with `MPAY=G|A|N`; how the EGW_TERM_GROUP value flips with Save Customer Card.
- [[borica-way4-refund-sync]] — refund (`TRTYPE=24` reversal); 5-minute platform-wide sync polling; `-24` "transaction not found" auto-cancel; HTTP retry behaviour.

## Settings & fields

This hub does not expose any fields directly. Field-level documentation lives per aspect:

- **Terminal ID + CSR + certificate-upload fields** → [[borica-way4-setup-csr]].
- **Mode, MID, EGW_SECURITY, Currency, Logo / Title / Description, Amount range, Discount, Authorization mode, EGW_MERCH_BACKREF, EGW_TERM_GROUP** → [[borica-way4-settings-fields]].
- **Save Customer Card + Google Pay / Apple Pay toggles** → [[borica-way4-save-card-wallets]].

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page. The high-level actions, with their aspect:

- **Install / Uninstall / Activate / Deactivate** the payment method — standard payment-provider overview controls; the live-activation gate is on [[borica-way4-setup-csr]].
- **Enter Terminal ID, generate CSR, upload signed certificates** — see [[borica-way4-setup-csr]].
- **Configure MID, signing algorithm, currency, storefront labels, amount range, discount** — see [[borica-way4-settings-fields]].
- **Pick Auto vs Manual capture** (and later Capture / Cancel an authorization) — see [[borica-way4-authorize-capture]].
- **Enable Save Customer Card and/or Google Pay / Apple Pay** — see [[borica-way4-save-card-wallets]].
- **Refund a payment, or re-sync a stranded Pending payment** — see [[borica-way4-refund-sync]].

## Business rules (cross-cutting)

The cross-cutting rules that apply to the integration as a whole — each spelled out on the relevant aspect:

- **3-D Secure is mandatory** — every Borica Way4 purchase routes through MPI_OW_APGW; the merchant cannot disable 3DS. See [[borica-way4-payment-lifecycle]].
- **Cannot activate live without valid certificates** (unless using the bundled `V1800001` test terminal). See [[borica-way4-setup-csr]].
- **Per-merchant key material** — every store has its own RSA private key + Borica-signed certificate; nothing is shared across stores. See [[borica-way4-setup-csr]].
- **Each terminal is provisioned for one currency** (BGN or EUR) — orders in a different currency are converted on the fly. See [[borica-way4-settings-fields]].
- **Plan gate**: the **Authorize + Capture** option requires the `authorize_payment` plan feature. Save card and wallets are not separately gated. See [[plan-gates]] and [[borica-way4-authorize-capture]].
- **Sync cadence**: a 5-minute platform-wide reconciliation job settles any stranded Pending payment within at most 5 minutes. See [[borica-way4-refund-sync]].
- **Save card + Authorize coexistence**: if both are configured the runtime picks the authorize branch; the merchant should pick one. See [[borica-way4-save-card-wallets]].

## Why it matters to the merchant

- **Gold-standard BG card gateway.** Most-deployed card integration on the platform. If a Bulgarian merchant accepts cards, they almost certainly use Borica Way4.
- **Per-merchant cryptography** is the operational surface. Every store onboards individually through its own CSR + Borica-signed certificate pair — there is no shared infrastructure failure mode but also no "just turn it on" path. See [[borica-way4-setup-csr]].
- **The bundled test terminal `V1800001` is a real shortcut**, not a stub. Merchants on trial can do realistic checkout end-to-end without signing a contract.
- **Stranded Pending payments self-heal in under 5 minutes** without merchant intervention thanks to the periodic sync. See [[borica-way4-refund-sync]].
- **No money-flow visibility in CloudCart.** Settlement and reporting are done through the merchant's own bank — unlike CloudCart Pay there is no Onboarding / Transactions / Payouts tab. Borica is configuration + reconciliation only, settlement is bank-side.

## Scope

Covered (across the 6 sub-pages):

- Terminal ID, CSR, certificate-upload onboarding + the V1800001 trial path.
- Full settings layout: MID, security algorithm, currency, storefront labels.
- Payment lifecycle: purchase, 3DS, redirect, return + IPN, signature verification, status mapping.
- Authorize + Capture two-phase flow with TRTYPE 12 / 21 / 22.
- Save Customer Card tokenisation and Google Pay / Apple Pay (MPay).
- Refund (TRTYPE 24) and the 5-minute sync reconciliation loop.

Not covered here:

- Settlement money-flow / bank statements — these are bank-side; CloudCart does not surface them.
- Storefront variant of the checkout button rendering — see [[checkout-flow]].
- The order details Refund / Capture buttons themselves — see [[orders-payment-refund]] and [[orders-payment-capture]].
- The customer's *Cards on file* panel — see [[customers-details-payments]].

## Related

- [[payment-providers]] — parent payment-providers hub.
- [[settings-payment-providers]] — global payment-providers list where Borica Way4 is installed / uninstalled.
- [[orders-payment-refund]] — initiates a refund through Borica from the order details page (see [[borica-way4-refund-sync]]).
- [[orders-payment-capture]] — manual capture of an authorized Borica payment (see [[borica-way4-authorize-capture]]).
- [[orders-payment-manual]] — manual payment entry (offline / outside Borica).
- [[customers-details-payments]] — saved-card management for individual customers (see [[borica-way4-save-card-wallets]]).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Authorized / Completed / Canceled / Refunded / Failed mapping.
- [[plan-gates]] — concept page on the `authorize_payment` feature gating.
- [[checkout-flow]] — storefront checkout, where Borica surfaces as a card payment option.

## Open questions

(none — uncertain claims are now flagged with `(verify)` on the aspect pages where they belong.)
