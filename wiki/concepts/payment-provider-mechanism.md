---
type: concept
nav_path: "Concept → Payment provider mechanism"
route_name: ""
route_path: ""
aliases: ["Payment provider mechanism", "Payment provider pattern", "How payment providers work", "Payment gateway integration", "Common payment provider pattern", "Payment integration model", "Payment provider lifecycle", "Платежни доставчици", "Шаблон на платежни доставчици", "Как работят платежните методи"]
tags: [payments, payment-providers, integrations, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Payment provider mechanism

## Definition

The **payment provider mechanism** is the common pattern CloudCart uses across all 72+ payment-provider integrations on the platform — Stripe, PayPal, iCard, Borica Way4, Mokka, Klarna, MyPos, Paynetics, DSK BNPL, FiBank, Iute, CloudCart Pay, Cash on Delivery, bank transfer, and every other gateway in [[settings-payment-providers]]. Despite the wildly different protocols (card networks, BNPL underwriting, instant bank transfers, voucher schemes, COD), every provider plugs into CloudCart through the same five-stage lifecycle: **configure credentials → activate at checkout → take the customer through the provider → confirm payment status → refund / capture / sync as needed**. The merchant configures each gateway in [[settings-payment-providers]] with provider-specific fields (merchant ID, terminal ID, API keys, certificates, etc.), the platform stores both live and test credentials side-by-side, and the customer sees the gateway at checkout as a payment method row.

This concept page describes the **shared mechanism** — what every payment provider has in common — so the 72+ per-provider feature pages (e.g., [[payment-providers-stripe]], [[payment-providers-icard]], [[payment-providers-borica-way4]], [[payment-providers-mokka]]) don't have to repeat the boilerplate. When a merchant asks the AI Assistant "how do I configure a payment provider?", "what statuses are possible?", "how does a refund work?", or "why am I not seeing this provider at checkout?", the answer derives from this pattern; provider-specific quirks live on each provider's page.

## Sub-pages (in this cluster)

This concept is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[payment-provider-configuration]] — credentials model (live + test, `<field>` / `test_<field>` convention); the 6-step activation flow; save-time validation; toggle-OFF vs uninstall; runtime self-deactivation on persistently bad credentials.
- [[payment-provider-integration-patterns]] — the three customer-interaction patterns: **redirect-based** (hosted gateway page, dominant), **embedded / SDK-based** (form inside checkout via SDK, e.g., Stripe / CloudCart Pay), **API-only / manual** (no gateway call — COD, bank transfer, voucher).
- [[payment-provider-tokenization-3ds]] — card data never reaches CloudCart; what's stored (token + masked metadata); Save Customer Card requires a signed-in account; 3DS enforcement matrix (mandatory on BG bank gateways, issuer-driven globally, N/A for offline + BNPL).
- [[payment-provider-refunds]] — the three refund styles: in-CloudCart Refund button (Stripe, Borica Way4, CloudCart Pay), merchant-portal refund + manual mark (iCard, Mokka, most BNPL), no refund support (COD, bank transfer, voucher); partial-refund gateway support vs current UI.
- [[payment-provider-confirmation]] — webhook-based (callback URL `/return/provider/<key>`, signature validation, `EGW_MERCH_BACKREF` for Borica) vs pull-based (Stripe today); the Sync recovery button on [[orders-details]]; status mapping from gateway codes to the canonical 13-value [[payment-status]] enum.
- [[payment-provider-checkout-visibility]] — the full visibility filter stack (Active + `min_price` / `max_price` + currency + country + shipping-method allowed-payments + plan gates); currency support per provider class; the `authorize_payment` plan gate; what the customer's row looks like.

## Scope

What this concept covers (across the 6 sub-pages):

- The configuration model with live + test credentials and the activation flow.
- The three integration patterns (redirect, embedded, manual).
- Tokenization and 3DS enforcement.
- Refund mechanism — three styles.
- Webhook vs sync confirmation + status mapping.
- Plan-feature gating and checkout-visibility filters.

What it does NOT cover:

- The exact credential fields, validation messages, signing algorithms, or refund API of each individual provider — those live on the 72+ per-provider feature pages.
- The order's overall status lifecycle independent of the payment record — see [[order-status-workflow]].
- The complete payment-status enum and its 13 values — see [[payment-status]].
- The cart-to-order transition that triggers the payment in the first place — see [[checkout-flow]].
- Cash-on-delivery sync from couriers (a special manual-payment flow) — see [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]].

## Contrasts

- **Payment provider mechanism vs payment status** — this concept describes the *mechanism* through which a gateway interacts with CloudCart; [[payment-status]] is the enum that records *where the money is*. Every provider's flow ends with a payment-status flip.
- **Payment provider vs shipping provider** — both are third-party integrations the merchant configures with credentials and activates at checkout. They differ in what they're paid for (money in vs parcel out) and where they appear in the customer flow (payment after cart, shipping during cart). See [[shipping-provider-mechanism]].
- **Online provider vs offline / manual provider** — see [[payment-provider-integration-patterns]] for the three-pattern taxonomy and what distinguishes Pattern 3 (no refund button, no live confirmation).
- **Provider-level activation vs provider-method visibility at checkout** — see [[payment-provider-checkout-visibility]] for the full filter chain.

## Where it applies

The payment-provider mechanism spans the merchant's configuration hub, the customer's checkout, the order-side payment actions, and downstream side-effects. Each sub-page documents its own application surface. Cross-cutting surfaces:

- **Configuration**: [[settings-payment-providers]] (central hub) and per-provider settings pages — see [[payment-providers]] (navigation hub).
- **Customer-side**: [[checkout-flow]] (cart-to-order transition; the customer picks a payment method), [[cart]] / [[order]] (the entities that carry the payment record).
- **Order-side actions**: [[orders-details]] (per-order edit hub; payment row shows the current [[payment-status]] and exposes action buttons), [[orders-payment-mark-paid]], [[orders-payment-capture]], [[orders-payment-refund]], [[orders-payment-manual]].
- **Status / data**: [[payment-status]] (the canonical enum), [[payment-provider]] (the entity storing per-provider configuration rows), [[order-status-workflow]] (order's overall status, partly driven by payment-status transitions).
- **Plan / billing**: [[plan-gates]] (`authorize_payment` feature; some advanced providers plan-gated), [[settings-statuses]] (Payment tab — merchant can rename status labels, underlying enum unchanged).

## Related

- [[settings-payment-providers]] — the merchant's payment-methods hub; central point for installing, activating, and configuring providers.
- [[payment-providers]] — the navigation hub listing every provider page.
- [[payment-status]] — the canonical enum every provider's response codes map into.
- [[payment-provider]] — the entity carrying per-provider configuration rows.
- [[checkout-flow]] — the cart-to-order transition where the customer picks a payment method.
- [[orders-details]] — per-order edit hub; payment action buttons (Refund, Capture, Sync, Mark Paid) live here.
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]] — payment-side action pages.
- [[plan-gates]] — the `authorize_payment` plan-feature that gates manual-capture mode.
- [[settings-statuses]] — Payment tab; merchant can rename status labels (underlying enum unchanged).
- [[notification-delivery]] — admin alerts fire when a provider self-deactivates on persistent credential failures.
- [[multi-currency]] — currency conversions and the BGN → EUR transition that rewrites provider currency codes.
- [[shipping-provider-mechanism]] — sister concept for shipping integrations.
- [[order-processing-pipeline]] — when the payment-gateway webhook flips a payment status, this chain of side-effects fires downstream.
- Top providers — per-provider configuration pages: [[payment-providers-cloudcart-pay]], [[payment-providers-stripe]], [[payment-providers-paypal]], [[payment-providers-icard]], [[payment-providers-borica-way4]], [[payment-providers-mokka]], [[payment-providers-dsk-bnpl]], [[payment-providers-fibank-bnpl]], [[payment-providers-iute]], [[payment-providers-klear]], [[payment-providers-tbi-bank]], [[payment-providers-fusion-pay]], [[payment-providers-cardlink]], [[payment-providers-cod]], [[payment-providers-authorize]], [[payment-providers-mollie]], [[payment-providers-braintree]], [[payment-providers-payu]], [[payment-providers-paysera]], [[payment-providers-everypay]], [[payment-providers-euplatesc]], [[payment-providers-mobilpay]], [[payment-providers-monri]], [[payment-providers-cib-bank]].

## Open Questions

- ⏸️ Per-provider behaviour details (partial-refund amount-input UI, exact `held` semantics, webhook signature scheme, plan-gating tier) vary across the 30+ payment integrations CloudCart ships. The per-provider admin screens ([[apps]] → individual payment-provider pages) document each integration's specifics; this concept page describes the shared mechanism only. Merchants integrating a specific provider should consult that provider's dedicated page for behaviour particulars.

All other previously-flagged questions resolved or distributed to sub-pages.
