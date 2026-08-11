---
type: entity
nav_path: "Entity → Cart → Recovery markers"
aliases: ["Cart recovery markers", "Recovery channel", "Restore-link token", "Cart source", "Recovered order attribution", "Guest cart recovery", "Send restore link quota", "Възстановяване на количка"]
tags: [entity, orders, cart, recovery, marketing, consent]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[cart]]. See the hub for the other aspects (data model, lifecycle, stock & pricing, merge).

# Cart — Recovery markers

## Identity

This page covers the Cart entity **from the recovery angle** — the per-cart fields and rules that drive [[abandoned-cart-recovery|abandoned-cart recovery]]: how a cart becomes eligible, which channel reaches it, the restore-link token that lets a customer resume, the two-layer consent gate the send must clear, and how a recovered order is attributed back. The end-to-end recovery pipeline (eligibility checks, timing, channel orchestration) lives on [[abandoned-cart-recovery]]; this page is the entity-side reference for the cart's recovery state.

## Aliases

- **Recovery channel** (`source`) — `email` or `messenger`.
- **Restore-link token** — the unique URL token embedded in the recovery message.
- **`date_sent`** — timestamp the automated recovery email was sent.
- **`abandoned_message_sent`** — boolean marker that the recovery flow already attempted this cart.
- **Recovered order** — an Order produced from a restore-link checkout (`abandoned = 1`, `restore_source` set).

## Key Attributes

### Recovery-state fields on the cart

| Field | What it stores | Notes |
|-------|----------------|-------|
| **`date_sent`** | Timestamp the recovery email was sent | NULL until the automated recovery flow sends the restore-link email; set once and used to prevent duplicate automated reminders. The bulk **Send restore link** on [[orders-abandoned]] does NOT respect this — it can re-send. |
| **`abandoned_message_sent`** | Boolean | Marker that the recovery flow already attempted to reach this cart. |
| **Recovery channel** (`source`) | `email` or `messenger` | Set when the recovery email is sent — drives `restore_source` on the resulting recovered Order. |
| **Restore-link token** | Unique URL token | Embedded in the recovery message URL so any recipient with the link can restore the cart into a fresh checkout session. |

### Guest carts have no customer profile but can still be recovered

A guest cart whose customer typed an email at the checkout email step (without registering) IS recoverable — provided the email belongs to a [[subscriber|Subscriber]] with Email-channel marketing consent. The platform identifies the cart by email and sends the restore-link email. See [[abandoned-cart-recovery]] for the seven eligibility checks.

### The recovery email respects the two-layer consent

For the automated recovery email to actually send, BOTH gates must pass:

1. The cart's owning customer has `marketing = yes` at customer level.
2. The matched [[subscriber|Subscriber]] (by email) has Email-channel `marketing` consent.

Either gate failing suppresses the send. See [[notification-delivery]] and [[subscriber-vs-customer]].

### Recovered orders are auditable

When a customer completes checkout via a restore link, the resulting Order carries:

- `abandoned = 1` — flag indicating the order originated from cart recovery.
- `restore_source` — `email` or `messenger`, identifying the channel that brought the customer back.

The **Recovered source** filter on [[orders]] surfaces these; the per-order audit log shows the banner *"Order was recovered through `<source>`"* (see [[orders-history]]).

### Bulk "Send restore link" consumes the same plan quota as the auto-reminder

The bulk **Send restore link** action on [[orders-abandoned]] consumes the SAME `abandoned_notification` plan quota as the automated reminder — each per-cart click increments the quota counter and is blocked with a *"feature limit warning"* when the quota is exhausted. The merchant should plan bulk recovery sends against the same monthly budget.

## Where it appears

- [[orders-abandoned]] — per-cart and bulk **Send restore link** actions; reads `date_sent` / `abandoned_message_sent`.
- [[abandoned-cart-recovery]] — the end-to-end recovery pipeline and the seven eligibility checks.
- [[orders]] — the **Recovered source** filter surfaces recovered orders (`restore_source`).
- [[orders-history]] — the per-order recovery banner.
- [[analytics-abandoned-carts]] — recovery-rate metrics.
- [[settings-cart]] — abandoned threshold that triggers the recovery flow.

## Related

- [[cart]] — hub.
- [[subscriber]] — the per-channel consent gate matched by email.
- [[customer]] — the customer-level `marketing = yes` gate.
- [[order]] — the recovered Order carrying `abandoned` + `restore_source`.
- [[abandoned-cart-recovery]] — the full recovery pipeline.
- [[notification-delivery]] — the two-layer consent gate mechanics.
- [[subscriber-vs-customer]] — why both consent layers exist.

## Open Questions

- ⏸️ The precise behavior when a guest cart's email matches an existing registered Customer record — is the cart auto-linked to the registered Customer at checkout, or kept as a guest cart?
