---
type: concept
nav_path: "Concept → Payment provider mechanism → Integration patterns"
aliases: ["Payment provider integration patterns", "Redirect-based payment provider", "Embedded payment provider", "SDK-based payment provider", "API-only payment provider", "Manual payment provider", "Шаблони за интеграция на платежни доставчици"]
tags: [payments, payment-providers, integrations, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-provider-mechanism]]. See the hub for the other aspects (configuration, tokenization & 3DS, refunds, confirmation, checkout visibility).

# Payment provider — integration patterns

## Definition

CloudCart's 72+ payment providers fall into one of **three integration patterns**, depending on how the customer's payment interaction is routed: **redirect-based** (customer leaves CloudCart to a hosted gateway page), **embedded / SDK-based** (the payment form renders inside the checkout via the gateway's SDK), and **API-only / manual** (no live gateway call — offline confirmation by the merchant). The merchant configures every provider the same way ([[payment-provider-configuration]]); the customer's UX differs.

## Scope

Covered:

- Pattern 1 — Redirect-based: how it works, customer experience, why it's the dominant pattern, the long list of providers using it.
- Pattern 2 — Embedded / SDK-based: how it works, what makes the experience seamless, examples.
- Pattern 3 — API-only / manual: how it works, no-gateway-call providers, no refund button.
- Why all three patterns end with the same final [[payment-status]] flip.

Not covered here:

- The credential and activation flow common to all patterns — see [[payment-provider-configuration]].
- How status is confirmed post-payment (webhook vs sync) — see [[payment-provider-confirmation]].
- Tokenization (saved cards) which is orthogonal — see [[payment-provider-tokenization-3ds]].
- Refund mechanics — see [[payment-provider-refunds]].

## Contrasts

- **Redirect vs embedded** — redirect-based providers move the customer off CloudCart to the gateway's hosted page (visible domain switch). Embedded providers render the payment form inside the checkout via an SDK — no domain switch, seamless feel. Both keep card data off CloudCart's servers.
- **Online provider vs offline / manual provider** — patterns 1 and 2 talk to a gateway in real time and end with an automatic status update. Pattern 3 records `pending` and waits for the merchant to confirm off-platform (cash received, bank transfer arrived, voucher confirmed).
- **Pattern 3 has no refund button** — refunds happen off-platform (cash refunded in person, bank transfer reversed, voucher restored manually), then marked refunded via [[orders-payment-refund]]. See [[payment-provider-refunds]] for the full taxonomy.

## Where it applies

### Pattern 1 — Redirect-based (most common)

The customer clicks a payment method at checkout, the platform creates a payment record (`initiated` status), calls the gateway's API to create a payment session, and **redirects the customer to the gateway's hosted payment page** (a different domain — `gate.icards.eu`, `borica.bg`, `checkout.stripe.com`, etc.). The customer enters card details ON THE GATEWAY'S DOMAIN — so CloudCart never sees the card number and doesn't carry PCI-DSS scope for cardholder data.

After the customer completes payment (and 3DS if required), the gateway redirects them back to a CloudCart return URL with the result. The platform either reads the result from the redirect parameters or calls the gateway's status-fetch API (Sync) to confirm the final status — see [[payment-provider-confirmation]].

**Examples** (the majority of CloudCart's portfolio): iCard, Borica Way4, MyPos, Mokka, DSK BNPL, FiBank BNPL, Iute, Cardlink, ePay, EasyPay, BNP, MyFin, Authorize.Net, Mollie, PayU, EveryPay, Settle, EuPlatesc, MobilPay, Monri, NestPay, Paysera, Skrill, Sofort, Revolut, FusionPay, Klear, Plati Posle, TBI Bank, Catalyst Pay, Instamojo, CIB Bank, BTEPos, Smart UCF, UCF, IBank, BWT.

This is the **dominant pattern** because it requires no PCI-DSS compliance from the merchant or CloudCart; the gateway handles all card-data security.

### Pattern 2 — Embedded (SDK-based)

The payment form is rendered INSIDE the CloudCart checkout via the gateway's SDK (typically a JavaScript library or iframe module). The card form lives on CloudCart's page so the customer doesn't see a domain switch — the experience feels seamless. But the SDK routes the card data directly to the gateway's vault (the platform NEVER receives the card number); only the resulting payment token comes back.

**Examples**:

- **Stripe** ([[payment-providers-stripe]]) — uses Stripe Checkout Sessions (a hosted redirect for first-time card, then off-session charges for saved cards). Note: while Stripe Checkout itself is technically a redirect, CloudCart's saved-card flow is server-to-server (off-session PaymentIntent), making subsequent purchases effectively embedded.
- **CloudCart Pay** ([[payment-providers-cloudcart-pay]]) — CloudCart's own gateway with native embedded card form + saved cards.
- Some BNPL providers when configured for inline application forms instead of redirect.

The merchant configures these the same way as redirect providers; the customer just sees a different UX.

### Pattern 3 — API-only / manual

No live gateway interaction. The customer picks the method, the platform records the order with payment status `pending`, and the merchant marks it paid manually after the off-platform event (cash received, bank transfer arrived, voucher confirmed).

**Examples**:

- **Cash on Delivery** ([[payment-providers-cod]]) — the courier collects cash from the customer at delivery; the courier's COD-sync sub-flow (see [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]]) automatically marks the order paid when the courier reports the COD collected, OR the merchant flips it manually via [[orders-payment-mark-paid]].
- **Bank transfer** — customer transfers funds to the merchant's account; merchant marks paid via [[orders-payment-mark-paid]] after the bank confirms.
- **Voucher / gift card / store credit** — internal credit redemption with no gateway call.

These methods have no refund button (see [[payment-provider-refunds]]).

## Related

- [[payment-provider-mechanism]] — hub.
- [[payment-provider-configuration]] — sibling aspect; the merchant configures all three patterns the same way.
- [[payment-provider-confirmation]] — what happens AFTER the customer pays (webhook vs sync) — orthogonal to the pattern.
- [[payment-provider-refunds]] — refund availability by pattern (patterns 1/2 typically have a refund button; pattern 3 never does).
- [[checkout-flow]] — the cart-to-order transition where the customer picks a payment method.
- [[payment-providers-stripe]] / [[payment-providers-cloudcart-pay]] — embedded examples.
- [[payment-providers-cod]] — Pattern 3 example.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] — courier COD-sync sub-flow that closes Pattern 3 automatically for delivery cash.

## Open Questions

None.
