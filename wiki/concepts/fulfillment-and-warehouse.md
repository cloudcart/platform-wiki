---
type: concept
nav_path: "Apps → Fulfillment & warehouse"
route_name: (none)
route_path: (none)
aliases: ["Fulfillment integrations", "Warehouse integrations", "Order fulfillment", "3PL", "Pick and pack", "Dropshipping", "Фулфилмънт", "Изпълнение на поръчки", "Складова логистика", "Warehouse & fulfillment"]
tags: [fulfillment, warehouse, 3pl, logistics, apps, integrations, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-08-06
source_count: 1
---
# Fulfillment & warehouse

## Definition

**Fulfillment & warehouse** integrations cover *how orders get picked, packed, and shipped* — whether from the merchant's **own warehouse**, an **outsourced 3PL**, or a **supplier / dropshipper** who ships on the merchant's behalf. Unlike [[erp-integrations]] (which CloudCart groups as a dedicated app family), this is a **merchant-facing grouping** of otherwise-separate apps that solve the same problem; each is installed from the [[apps]] App Store and there is no single fulfillment screen.

## Scope

The supported models:

- **In-house warehouse** — [[apps-pick-and-pack]] adds a tablet/terminal interface where warehouse staff scan, count, pack, and confirm dispatch (configured in [[apps-pick-and-pack-settings]]).
- **Outsourced 3PL** — [[apps-frisbo]] hands fulfilment to the Frisbo third-party logistics network; orders are routed to Frisbo for storage + shipping (see [[apps-frisbo-orders]], [[apps-frisbo-settings]]).
- **Dropshipping** — [[apps-drop-shipping]] lets suppliers ship products directly to the customer, so the merchant holds no stock.
- **Suppliers** — [[apps-suppliers]] manages supplier catalogues feeding the store (see [[apps-suppliers-overview]]).

For the *physical hand-off to a courier* once a parcel is packed, see [[shipping]] (the courier directory). For stock counts, see [[inventory-tracking]].

## Contrasts

- **In-house vs 3PL** — [[apps-pick-and-pack]] is for merchants running their own warehouse; [[apps-frisbo]] outsources the warehouse entirely.
- **Fulfilment vs shipping** — fulfilment is *picking & packing*; [[shipping]] is *handing the parcel to a courier*. Many stores use one app from each.
- **Fulfilment vs ERP** — [[erp-integrations]] sync catalogue / stock / accounting data; fulfilment apps move the physical goods.

## Where it applies

- Stock decremented as orders are packed / shipped — see [[inventory-tracking]].
- Courier waybills generated at dispatch — see [[shipping]] / [[orders-shipping-waybill]].

### The native fulfillment flag (no app required)

Independently of every app above, each order carries a **`status_fulfillment`** flag (`not_fulfilled` / `fulfilled`) flipped by **generating a waybill** — the **Fulfill products** button on [[orders-details-shipping]], reversed by **Mark as unfulfilled** on the same row — and a **fully-digital order auto-fulfills the moment it reaches `paid`** (no waybill). The pick-and-pack / 3PL / dropship / supplier apps layer ON TOP of this native flag; they don't replace it. The full fulfillment-event chain (add / remove, the stock-decrement moment, partial per-product fulfillments, auto-fulfill) is on [[order-pipeline-stage-4-fulfillment]]; the status semantics are on [[order-status-workflow]].

## Related

- [[apps]] — the App Store (install any of the above).
- [[erp-integrations]] — sibling integration category (back-office sync).
- [[shipping]] — courier integrations (the dispatch step after packing).
- [[inventory-tracking]] — the stock model.
- [[order-pipeline-stage-4-fulfillment]] — the native fulfillment-event chain (add / remove, auto-fulfill on digital, partial fulfillments).
- [[order-status-workflow]] — the `status_fulfillment` flag + its interaction with `status`.

## Open Questions

- Whether [[apps-stores]] / [[apps-store-locations]] (multi-location) belong in this grouping or under store setup (verify).
