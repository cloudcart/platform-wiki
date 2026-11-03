---
type: concept
nav_path: "Concept → Order processing pipeline → Recalculation & freeze"
aliases: ["Order recalculation", "Order totals recalculation", "recalculate_locked", "Order freeze model", "What recalculates on order edit", "Frozen vs live order totals", "Payment method change recalculation", "COD fee on payment change", "payer side", "is_seller_payer_shipping", "Преизчисляване на поръчка", "Заключване на преизчислението", "Смяна на метод на плащане преизчисление"]
tags: [orders, lifecycle, recalculation, totals, payment, shipping, freeze, concepts]
plan_gates: []
created: 2026-06-13
updated: 2026-06-13
source_count: 6
---

> Part of [[order-processing-pipeline]]. See the hub for the other aspects (placement, status transitions, payment sync, fulfillment, manual edits, edge cases).

# Order pipeline — Recalculation & freeze model

## Definition

When the merchant edits an **already-placed** order, the platform re-derives the order's lines, discounts, fees, shipping quote, **payer side**, and totals from the order's current state — **unless recalculation is locked**. This page answers the recurring question *"I changed X on the order — why did (or didn't) the total / fee / shipping change?"*

The part that surprises merchants most: **changing the payment method is NOT an inert provider swap** — it re-derives a whole bundle of payment-inherited conditions (the fee, a per-provider discount, payment-tied free shipping, the payer side, payment-targeted Cart Rules, and cash-on-delivery mode). The tax *rate*, by contrast, is snapshotted at placement and never re-derived — see [[tax-order-snapshot]].

## Scope

Covered:

- The recalculation lock (`recalculate_locked`) and what it freezes.
- Which edits trigger a recalculation.
- The full set of conditions the **payment method** carries into the order total.
- What stays frozen (the snapshot discipline).

Not covered here:

- The per-edit side-effect matrix (history rows / stock / emails / webhooks) — see [[order-pipeline-stage-5-edit]].
- Discount math — see [[discount-stacking]]; tax math — see [[tax-computation]]; shipping-rate arithmetic — see [[shipping-calc-cascade]].
- Where the per-provider fee / discount / seller-payer flag are configured — see [[settings-payment-providers]].

## Contrasts

- **Recalculated vs frozen-snapshot** — lines, discounts, fees, shipping (when unlocked) and the payer side are re-derived on edit; the **tax rate** is a frozen snapshot ([[tax-order-snapshot]]) and never moves.
- **Payment-method change vs shipping-method change** — a shipping change re-quotes only shipping; a **payment** change re-derives a whole bundle (fee + per-provider discount + payment-free-shipping + payer side + payment Cart Rules) AND re-quotes shipping.
- **Locked vs unlocked** — an unpaid order recalculates freely; a paid order is frozen by default (shipping price kept), overridable via the `recalculate_locked` meta.

## Where it applies

### The recalculation lock (`recalculate_locked`)

- **Default:** locked once the order's payment status is `completed` (paid); unlocked before that. An unpaid order recalculates freely; a paid order is frozen by default.
- **Override:** the merchant can flip the `recalculate_locked` order meta from [[orders-details]] to force-lock an unpaid order or force-unlock a paid one.
- **What it gates:** **only the shipping-price re-quote.** When locked, the courier integrations keep the order's **stored shipping / courier amount** (`provider_amount`, the figure that goes on the waybill) instead of asking the carrier for a fresh quote. Everything else still re-derives — line/discount edits recompute the totals, and a payment-method change still re-derives the payment-linked fee, the per-provider discount, and the payer side **regardless of the lock**; only the shipping price stays frozen. One exception: manually **changing the payer side** force-re-quotes shipping even on a locked order, because who-pays-shipping changes the collected amount.
- **Auditable + toggleable:** flipping the lock writes a `lock_order` entry to the order History, so the change is visible on [[orders-history]].

### When a recalculation runs (triggers)

| Edit on [[orders-details]] | What is re-derived |
|---|---|
| Add / edit / remove a product line | line totals + order total (synchronous) — see [[order-pipeline-stage-5-edit]] |
| Add / remove a discount | order total |
| Change shipping method / address (`admin.orders.shipping.change`) | re-quotes shipping for the new method/address — subject to the lock |
| **Change payment method (`admin.orders.payment.change`)** | re-derives every payment-inherited condition below + re-quotes shipping (subject to the lock) + recomputes totals |
| Status change to `paid` / `completed` | engages the lock by default + forces the payer side to **sender** |

### What the payment method carries into the recalculation

Switching the payment method re-derives **all** of these from the *new* provider:

1. **Payment-linked fee (COD surcharge).** Fees tied to the *old* provider are removed; fees configured for the *new* provider (matched to the order's geo-zone) are re-added. So a COD surcharge re-appears **only if** a COD fee is configured for that zone + payment. See [[shipping-provider-mech-cod]] / [[tax-fees-vs-vat]].
2. **Per-provider automatic discount.** A provider can carry its **own discount** — `flat`, `percent`, or `shipping` with a value — applied as an order discount in the `payment` group (type `payment-{type}-{provider}`). It applies only for those three types; `flat`/`percent` need a value ≥ 0; a `flat` discount is **skipped** when its value exceeds the order total.
3. **Payment-tied free shipping.** A method can carry free shipping (an order discount of type `payment-shipping-{provider}`); when present it both affects the shipping line and forces the payer side to **sender**.
4. **Payer side — who pays shipping.** Driven by the provider's `is_seller_payer_shipping` flag. The side is forced to **sender (seller pays)** when *any* hold: the provider is seller-payer, the order is `paid`/`completed`, the order has free shipping, or the method uses a fixed-price shipping model (`fixed_price` / `fixed_weight` / `calculator_fixed` / `price_and_weight`). The side sets the **cash collected at the door** and the **waybill payer side** — see [[shipping-provider-mech-waybill]].
5. **Payment-targeted Cart Rules / discounts.** A [[apps-cart-rules|Cart Rule]] or discount conditioned on the payment method activates or deactivates when the provider changes.
6. **Cash-on-delivery mode.** `provider == cod` flips the order into COD mode — the COD amount on the waybill and eligibility for the automatic COD paid-sync ([[orders-sync-cod]]).

### What does NOT recalculate (frozen)

- **The tax rate** — snapshotted at placement; later tax-setting changes don't move historical orders ([[tax-order-snapshot]]).
- **Shipping price on a paid order** — frozen by the lock until force-unlocked.
- This snapshot discipline keeps historical orders accurate after the merchant later edits rates, fees, or shipping config.

### Why the visible effect of a payment-method change varies

What actually moves when the merchant switches the payment method depends on what the *new* provider carries: whether a COD fee is configured for the zone, whether the provider has its own discount or payment-tied free shipping, its `is_seller_payer_shipping` flag, and whether the order is already paid (locked). When the new provider carries none of these, the change is limited to the provider name and a reset payment status — the totals look unchanged even though the recalculation did run.

## Related

- [[order-processing-pipeline]] — hub.
- [[order-pipeline-stage-5-edit]] — the per-edit side-effect matrix (line / discount / shipping / note / archive).
- [[order-pipeline-stage-2-status]] — status change engages the lock + forces the payer side.
- [[tax-order-snapshot]] — the frozen-at-placement tax snapshot.
- [[tax-fees-vs-vat]] — how payment-linked fees stack (the COD surcharge).
- [[shipping-provider-mech-cod]] — COD fee + per-provider COD toggle + COD-only checkout filter.
- [[shipping-provider-mech-waybill]] — the payer side on the waybill.
- [[shipping-calc-cascade]] — how a shipping quote is produced when re-quoted.
- [[discount-stacking]] — how the payment discount stacks with other discounts.
- [[order-totals-pipeline]] — the stage order that places the payment discount in the before-shipping stage (before shipping & VAT).
- [[orders-details]] — the edit surface + the `recalculate_locked` control.
- [[settings-payment-providers]] — where the per-provider fee / discount / seller-payer flag are configured.

## Open Questions

- The **stage** the payment discount lands in is settled — the before-shipping discount stage, before shipping & VAT (see [[order-totals-pipeline]]). Its exact priority *among the other discounts in that stage* follows [[discount-stacking-evaluation-order]]; the payment group's precise position in that chain is not yet pinned down. (verify)
