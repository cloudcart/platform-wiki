---
type: concept
nav_path: "Concept → Payment provider mechanism → Refunds"
aliases: ["Payment provider refunds", "Refund mechanism", "Refund styles", "In-CloudCart refund button", "Merchant-portal refund", "No-refund methods", "Partial refunds", "Възстановяване на плащане"]
tags: [payments, payment-providers, refunds, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-provider-mechanism]]. See the hub for the other aspects (configuration, integration patterns, tokenization & 3DS, confirmation, checkout visibility).

# Payment provider — refunds

## Definition

How a merchant issues a refund depends on **which provider** processed the payment. CloudCart's 72+ integrations sort into **three refund styles**: in-CloudCart refund button (gateway-API call from the platform), merchant-portal refund + manual mark (off-platform action + status flip in CloudCart), and no refund support (off-platform-only — cash, bank transfer, voucher). The end state is the same — [[payment-status]] = `refunded` — but the path differs.

## Scope

Covered:

- The three refund styles, with which providers fall into each.
- Where the Refund button lives in the admin.
- Partial refund availability (gateway-dependent, current UI limitations).
- Why offline / manual methods (Pattern 3) never have a Refund button.

Not covered here:

- The full [[payment-status]] enum and its 13 values — that's its own page.
- The voiding of authorized-but-not-captured holds — see [[orders-payment-capture]] (`authorized` → `voided`).
- The status mapping from gateway response codes — see [[payment-provider-confirmation]].
- The credit-memo / financial-side audit trail (what's owed back to the customer) — see [[orders-credit]].

## Contrasts

- **In-CloudCart refund vs merchant-portal refund** — the first calls the gateway's refund API from CloudCart and flips the status atomically. The second requires the merchant to refund in the gateway's own portal AND then manually mark refunded in CloudCart — two-step, easy to forget the second step.
- **No-refund methods vs no-refund-button** — offline methods (COD, bank transfer, voucher) have no refund path through CloudCart because the refund itself happens off-platform (cash refunded in person, bank transfer reversed, voucher restored manually). The Refund button is absent by design.
- **Full refund (current default) vs partial refund (limited)** — some gateways support partial refunds at the API level, but CloudCart's current admin UI typically issues a full refund of the captured amount. Per-provider partial-refund support is documented on each provider's page.
- **Refund vs void** — refund returns money on a `completed` payment. Void cancels an authorization hold that was never captured (`authorized` → `voided`) — different path; see [[orders-payment-capture]].

## Where it applies

### Refund admin entry point

- [[orders-details]] — per-order edit hub; the payment row exposes the Refund button when the provider supports it. Status: `completed` → `refunded` on success.
- [[orders-payment-refund]] — the action page that fires the refund (full-refund-only in the current UI, with provider-side partial-refund support varying).
- [[orders-credit]] — the financial / credit-memo side of refunds (money movement audit).

### The three refund styles

| Style | How it works | Example providers |
|-------|--------------|-------------------|
| **In-CloudCart refund button** | The merchant clicks Refund on the order's payment row in [[orders-details]]; the platform calls the gateway's refund API; on success the [[payment-status]] flips to `refunded`. | Stripe, Borica Way4, CloudCart Pay, some Cardlink configs |
| **Merchant-portal refund + manual mark** | CloudCart does not expose a refund button. The merchant logs into the gateway's own merchant portal (iCard portal, Mokka portal, etc.) and issues the refund there. After the refund clears at the gateway, the merchant manually marks the CloudCart order as refunded via [[orders-payment-refund]] (which then just flips the status without a gateway call). | iCard, Mokka, most BNPL providers |
| **No refund support** | The method itself has no refund path through CloudCart. For COD / bank transfer / voucher, the merchant arranges the refund off-platform and manually marks the order refunded. | COD ([[payment-providers-cod]]), bank transfer, voucher |

### Partial refunds

**Partial refunds** are technically supported by some gateways:

- **Stripe** ([[payment-providers-stripe]]) — partial-refund supported at the API.
- **Borica Way4** ([[payment-providers-borica-way4]]) — partial via TRTYPE 24.
- **CloudCart Pay** ([[payment-providers-cloudcart-pay]]) — partial-refund supported.

But the current admin UI typically issues a **full refund of the captured amount**. (verify) — partial-refund UI may differ per provider; see each provider's page for the per-provider note on partial-refund availability.

## Related

- [[payment-provider-mechanism]] — hub.
- [[payment-provider-integration-patterns]] — Pattern 3 providers are exactly the ones with no Refund button.
- [[orders-payment-refund]] — the refund action page.
- [[orders-payment-capture]] — sibling action (capture / void authorized funds — not refund).
- [[orders-credit]] — the financial-side audit of money owed back.
- [[payment-status]] — the canonical enum, where `refunded` is the end state.
- [[payment-providers-stripe]] / [[payment-providers-borica-way4]] / [[payment-providers-cloudcart-pay]] — in-CloudCart refund-button providers.
- [[payment-providers-cod]] — no-refund-support example.

## Open Questions

- ⏸️ Partial-refund admin UI varies per provider (verify) — exact UI controls and amount-input semantics documented on individual provider pages.
