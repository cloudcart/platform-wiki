---
type: entity
aliases: ["Payment status", "Payment state", "Money status", "Статус на плащане", "Платежен статус"]
tags: [orders, payments, settings, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Payment Status

## Identity

A **Payment Status** is the enum value on an [[order|order's]] payment record that tells the merchant *where the money is*. It is the canonical "is this paid?" signal — distinct from the order's overall **order status** ([[order-status]]). An Order can be `completed` while its Payment Status is `refunded` (the merchant refunded the customer after marking the order completed), and an Order can be `pending` while its Payment Status is `authorized` (pre-auth hold, money locked but not yet captured). Whenever a [[payment-provider]] callback fires, an admin clicks **Mark as paid** / **Refund** / **Capture** / **Cancel authorization**, or a sync pulls the latest provider state — the Payment Status flips, and the order's UI re-renders the buttons that are visible based on it.

The same enum is reused in **two related-but-distinct layers**: at the platform-wide payment-gateway level ([[payment-provider|Payment]] gateway record — what the gateway saw) and at the per-order payment-record level (the order's payment row — what the platform attached to this specific order). The two normally stay in sync — when they diverge (e.g., gateway sees `completed` but order's record is `pending`), the merchant can re-sync via the **Sync** action on the payment row.

This entity is documented across a hub (this page) + 4 aspect sub-pages. The Assistant should drill into the aspect that matches the question rather than read the whole cluster.

## Aliases

- "Payment status" — the canonical merchant-facing term used in the order details, payment-providers settings, and reports.
- "Payment state" — alternative used in some integration docs.
- "Money status" — informal merchant language ("is the money in yet?").
- Bulgarian: "Статус на плащане" / "Платежен статус".
- In the platform schema this is the `status` column on the order's payment record and on the gateway-side payment row.

## Sub-pages (in this cluster)

- [[payment-status-values]] — the 13 platform-defined enum values verbatim, what each means and when it's set; the 9-vs-13 code-constant distinction; the `NEGATIVE_STATUS` counterparts; the per-payment metadata (provider, amount, references).
- [[payment-status-lifecycle]] — the three lifecycle shapes (direct charge / authorize-then-capture / manual-offline); the universal refund path; the **Sync** recovery action; the initial state on order creation.
- [[payment-status-vs-order-status]] — why payment status is independent of order status; what credit-note and archive eligibility gate on (order status, not payment); the side-effects fired when a payment saves as `completed`; why renaming a status doesn't change behaviour.
- [[payment-status-provider-mappings]] — how each [[payment-provider]] translates its native codes into this enum; button-visibility rules (Refund only on `completed`); the `disputed` / `chargebacked` manual-reconciliation rules; `cancelled` vs `voided` semantics; multi-currency and multiple-payment-record handling.

## Key Attributes

The payment-status enum has **13 platform-defined values**. They are NOT extensible — the merchant cannot add custom payment statuses (unlike order statuses). What the merchant CAN do via [[settings-statuses]] is rename the merchant-facing label (translation override) — the underlying enum key stays the same so all business logic continues to work. The verbatim enum values are:

`initiated`, `requested`, `pending`, `authorized`, `held`, `completed`, `failed`, `refunded`, `voided`, `cancelled`, `timeouted`, `chargebacked`, `disputed`.

The full per-value meaning table, the per-payment metadata attributes (provider, amount, references, hash), and the constant-vs-mapping distinction live on [[payment-status-values]]. The transition shapes are on [[payment-status-lifecycle]]. The independence-from-order-status rules are on [[payment-status-vs-order-status]]. The provider translation tables are on [[payment-status-provider-mappings]].

## Where it appears

- [[settings-statuses]] — the **Payment** tab shows all 13 statuses; the merchant can rename their merchant-facing labels (translation override). They CANNOT add new payment statuses or delete built-in ones.
- [[orders]] — the orders list shows a payment-status filter and column.
- [[orders-details]] — the payment action row displays the current status as a coloured badge; the buttons shown (Mark paid, Refund, Capture, Cancel authorization, Sync, Manual) depend on it — see [[payment-status-provider-mappings]].
- [[orders-payment-mark-paid]] — flips status to `completed` manually.
- [[orders-payment-capture]] — flips status from `authorized` → `completed` (Capture) or → `voided` (Cancel authorization).
- [[orders-payment-refund]] — flips status to `refunded` (full refund) when the gateway acknowledges.
- [[orders-payment-manual]] — manual-mode payment confirmation.
- [[orders-credit]] — credit-note eligibility checks the order's overall status; see [[payment-status-vs-order-status]].
- All **[[payment-provider|payment-provider]]** wiki pages (`payment-providers-*`) document their **status mapping** — see [[payment-status-provider-mappings]].
- [[analytics-full]] — analytics dashboards aggregating orders by payment provider; count `completed` separately from `failed` / `cancelled`.

## Related

- [[order-status]] — the OTHER status enum on every order; lifecycle is separate.
- [[shipping-status]] — fulfillment status; also separate.
- [[order]] — order entity; carries one-to-many payment records.
- [[payment-provider]] — the gateway integration that translates native gateway codes to this enum.
- [[settings-statuses]] — Payment tab; merchant can rename labels.
- [[settings-payment-providers]] — install / configure gateways that drive this status.
- [[orders-payment-mark-paid]] — flip to `completed` manually.
- [[orders-payment-capture]] — `authorized` → `completed` (Capture) or → `voided` (Cancel auth).
- [[orders-payment-refund]] — `completed` → `refunded`.
- [[orders-payment-manual]] — manual confirmation flow.
- [[orders-credit]] — credit-note flow (gated by ORDER status, not payment status).
- [[orders-archive]] — archive gating (also ORDER status).
- [[checkout-flow]] — the storefront flow that produces the first payment status.
- [[order-status-workflow]] — concept page on how the two status enums interact at status-change time.
- [[settings-hooks]] — `order.updated` webhook fires on payment-status change.
- [[analytics-full]] — analytics dashboards aggregating payments by provider + status.
- [[plan-gates]] — some payment providers are plan-gated.

## Open Questions

No outstanding questions — all items resolved or distributed to the sub-pages.
