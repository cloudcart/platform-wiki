---
type: entity
nav_path: "Entity → Payment Provider → Integration styles"
aliases: ["Redirect vs embedded vs manual", "Payment provider patterns", "PCI scope-out", "Card data never reaches CloudCart", "Integration types"]
tags: [entity, payments, payment-providers, integrations, pci, security]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Payment Provider — Integration styles

> Part of [[payment-provider]]. See the hub for related aspects (attributes, credentials + modes, relationships, lifecycle, plan gating, side effects).

## Identity

CloudCart's 72+ Payment Providers all fall into one of **three integration styles**, distinguished by where the customer enters their card data and how the payment result returns to CloudCart. The merchant configures all three the same way through the per-provider settings page; the customer sees different UX at checkout. The constant across all three styles: **CloudCart never stores raw card data**, which keeps it out of PCI-DSS cardholder-data scope.

## Aliases

- **Redirect vs embedded vs manual** — the three patterns merchants commonly ask about.
- **PCI scope-out** / **Card data never reaches CloudCart** — the security guarantee that follows from the integration style choice.
- **Integration types** — when discussing provider onboarding.

## Key Attributes

| Style | How it works | Examples |
|-------|--------------|----------|
| **Redirect-based** (most common) | The customer is redirected to the gateway's hosted payment page (e.g., `gate.icards.eu`, Borica's 3DS page, `checkout.stripe.com`). They enter card details on the gateway's domain. After 3DS and authorization, the gateway redirects back to a CloudCart return URL with the result. | iCard, Borica Way4, MyPos, Mokka, most BNPL providers, EuPlatesc, MobilPay, PayU — the majority of CloudCart's catalogue. |
| **Embedded (SDK-based)** | The payment form is rendered inside CloudCart's checkout via the gateway's SDK. The customer sees no domain switch but the SDK routes card data to the gateway's vault. | Stripe (saved-card off-session flow), CloudCart Pay (native embedded form), some BNPL inline application forms. |
| **API-only / manual** | No live gateway call. The platform records `pending` payment status, and the merchant manually marks the order paid via [[orders-payment-mark-paid]] after receiving cash / bank transfer / voucher. | COD ([[payment-providers-cod]]), bank transfer, voucher / gift card. |

The merchant configures all three the same way; the customer just sees a different UX. The cross-cutting concept page [[payment-provider-integration-patterns]] catalogues the runtime mechanics in more depth.

## Card data never reaches CloudCart

Across all three patterns, the constant is: CloudCart NEVER stores raw card numbers, expiry dates, or CVV codes. The gateway-side vault holds the card; CloudCart stores only:

- A **token** (the gateway's reference to the saved card, e.g., Stripe `pm_...`, Borica `MERCH_TOKEN_ID`).
- **Masked metadata** for display — card brand (Visa / Mastercard / Maestro / Amex / Diners / JCB), last 4 digits, expiry month/year, issuing country.

This is what keeps CloudCart out of PCI-DSS cardholder-data scope. The merchant inherits this scope-out — they do not handle card numbers, and a database leak does not expose customer cards.

## Customer's view at checkout

Customer sees the provider as a row in the payment-method picker with:

- Logo (provider's default or merchant's override).
- Storefront name (merchant's configured label).
- Description (optional short explainer).
- Discount / fee badge (if configured — see [[payment-provider-entity-attributes]]).

The customer picks, clicks Pay, and the integration style (redirect / embedded / manual) takes over. The merchant's configuration looks the same regardless of which style the provider uses.

## How the style choice shapes other behavior

- **Confirmation** — Redirect + Embedded providers usually use webhooks; API-only / manual providers always use manual mark-paid. See [[payment-provider-confirmation]].
- **Refunds** — Redirect + Embedded providers may expose in-CloudCart refund; manual providers cannot. See [[payment-provider-refunds]].
- **Tokenization** — Only Embedded and some Redirect providers can save customer cards. See [[payment-provider-tokenization-3ds]].
- **3DS enforcement** — Redirect-based bank gateways enforce 3DS 2.x mandatorily; global gateways defer to the issuer; offline / manual methods have no 3DS at all.

## Where it appears

- Every per-provider settings page reflects its style implicitly (redirect providers expose the webhook callback URL field; embedded providers expose SDK-specific settings; manual providers have no gateway credentials).
- [[checkout-flow]] — the customer's experience of the style choice.
- [[payment-provider-integration-patterns]] — full cross-cutting concept page.

## Related

- [[payment-provider]] — hub.
- [[payment-provider-integration-patterns]] — the cross-cutting concept covering all three styles.
- [[payment-provider-confirmation]] — webhook vs Sync vs manual confirmation flows.
- [[payment-provider-refunds]] — refund availability per style.
- [[payment-provider-tokenization-3ds]] — saved-card and 3DS rules per style.
- [[payment-providers-cod]] — canonical manual / offline example.
- [[payment-providers-stripe]] — canonical embedded / SDK example.
- [[payment-providers-icard]] — canonical redirect example.
- [[checkout-flow]] — where the style affects customer UX.

## Open Questions

None.
