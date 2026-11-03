---
type: entity
aliases: ["Payment status lifecycle", "Payment transitions", "Payment status flow", "Authorize then capture", "Жизнен цикъл на плащане", "Преходи на платежен статус"]
tags: [orders, payments, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[payment-status]]. See the hub for the other aspects (values, vs order status, provider mappings).

# Payment Status — the lifecycle

## Identity

This page describes **how a payment moves between statuses** over its life. The lifecycle has **three common shapes**, depending on the provider's payment model, plus a universal refund path and a **Sync** recovery action. The individual status meanings live on [[payment-status-values]]; this page is about the transitions between them.

## Aliases

- "Payment lifecycle" / "Payment status flow" — the sequence of transitions.
- "Authorize-then-capture" — the pre-auth shape.
- Bulgarian: "Жизнен цикъл на плащане" / "Преходи на платежен статус".

## Key Attributes

### Shape 1 — direct charge (most common: card-on-file, redirect-then-capture)

```
initiated → requested → pending → completed
                                    ↘ failed
                                    ↘ cancelled
                                    ↘ timeouted
```

- The platform creates a payment record (`initiated`), redirects the customer to the gateway (`requested`), waits during the gateway's processing (`pending`), and lands on `completed` (money captured) or one of the negatives.
- From `completed`, the merchant can later issue a refund → `refunded`.
- Months later, the customer's bank could chargeback the charge → `chargebacked`, or open a dispute → `disputed`.

### Shape 2 — authorize-then-capture (pre-auth, e.g., Klarna, some Stripe flows)

```
initiated → requested → authorized → completed (merchant clicked Capture)
                                       ↘ voided (merchant clicked Cancel authorization)
                                       ↘ timeouted (auth expired without capture)
```

- The gateway authorises (`authorized`) — funds are reserved but not taken. The merchant has a finite window to capture.
- Capture → `completed` (see [[orders-payment-capture]]). Cancel → `voided`.
- Refund follows the same later path.

### Shape 3 — manual / offline payment (COD, bank transfer)

```
pending → completed (merchant clicks "Mark as paid")
        ↘ cancelled (order cancelled before payment received)
```

- The platform creates the order with payment `pending`. No gateway round-trip.
- When the cash / bank transfer is received, the merchant manually flips to `completed` via [[orders-payment-mark-paid]].

### Refund path (universal)

From `completed` → the merchant clicks **Refund** (see [[orders-payment-refund]]):

- The gateway is called with the refund request.
- On gateway success → status flips to `refunded`.
- On gateway failure → status stays `completed` and the merchant sees the gateway error.

### Sync as the recovery path

For any in-flight payment (`pending`, `requested`, `authorized`), the **Sync** action queries the gateway for the latest status and updates the platform record. This is critical for providers without webhook callbacks (Stripe uses pull-based sync per [[payment-providers-stripe]]) and as a recovery tool when the gateway's webhook was lost. Sync is also the fix when the gateway-side and order-side records diverge — see the two-layer note on the [[payment-status]] hub.

### Initial state on order creation

When a new order is created with an online-payment provider, the payment record is created with status `initiated`. When the gateway accepts the redirect request, it flips to `requested`. The customer's gateway interaction drives subsequent transitions. For manual / offline payment orders, the initial state is `pending`.

## Where it appears

- [[checkout-flow]] — produces the first payment status (`initiated` / `pending`).
- [[orders-details]] — the payment row shows the current status; the buttons that drive transitions render conditionally — see [[payment-status-provider-mappings]].
- [[orders-payment-mark-paid]] — drives Shape 3 to `completed`.
- [[orders-payment-capture]] — drives Shape 2 `authorized` → `completed` / `voided`.
- [[orders-payment-refund]] — the universal refund path → `refunded`.
- [[orders-payment-manual]] — manual confirmation flow.

## Related

- [[payment-status]] — hub.
- [[payment-status-values]] — what each status in these flows means.
- [[payment-status-provider-mappings]] — which gateway response codes map onto each transition.
- [[checkout-flow]] — produces the initial payment status.
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]] — the actions that drive transitions.
- [[payment-providers-stripe]] — pull-based Sync example.
- [[order-status-workflow]] — how payment transitions interact with order-status transitions.

## Open Questions

No outstanding questions.
