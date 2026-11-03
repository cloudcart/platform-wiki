---
type: concept
nav_path: "Concept → Food, restaurant & grocery"
route_name: (none)
route_path: (none)
aliases: ["Food ordering", "Restaurant", "Grocery", "Quick commerce", "Restaurant POS", "Food delivery", "Ресторант", "Хранителни стоки", "Хранителен магазин", "Доставка на храна", "Заведение", "Grocery store"]
tags: [food, restaurant, grocery, pos, delivery, apps, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---
# Food, restaurant & grocery

## Definition

**Food, restaurant & grocery** is running CloudCart for a food business — a restaurant / café taking orders, or a grocery / quick-commerce store — typically by combining a **POS**, an **on-demand delivery** courier, and a **grocery-optimised storefront**. There is no single "food" screen; this page maps the apps that together cover the use case.

## Scope

- **Restaurant / hospitality POS** — [[apps-rkeeper]] (r_keeper) keeps the online menu and orders in step with the in-venue point-of-sale. (For retail POS more broadly, see [[apps-posmaster]] and [[erp-integrations]].)
- **On-demand / hyperlocal delivery** — [[apps-glovo]] hands last-mile delivery to Glovo's courier network.
- **Grocery storefront** — the grocery-store app ([[apps-grocery-store-overview-new]], [[apps-grocery-store-settings]]) tailors the storefront for grocery / quick-commerce (large SKU counts, fast reorder).
- **Multi-location availability** — a grocery chain or dark-store network can show each customer the stock of the store serving their area, via [[apps-store-locations]] (geo-zone routing) paired with [[apps-stores]] — see [[inventory-multi-warehouse]].
- **Variable-weight billing** — for goods sold by weight (deli, meat, fish, produce) the ordered amount rarely matches the picked amount. On card gateways that support it, authorize the ordered amount at checkout, then [[orders-payment-capture|capture the lower actual total]] once staff weigh / pick the goods (often via [[apps-pick-and-pack]]) — avoiding a small refund.

## Contrasts

- **POS-led vs storefront-led.** A restaurant usually treats the POS ([[apps-rkeeper]]) as the source of truth and mirrors the menu online; a grocery store treats the CloudCart catalogue as the source of truth.
- **On-demand vs courier shipping.** [[apps-glovo]] is hyperlocal and immediate; standard couriers in the [[shipping]] directory are parcel / next-day.
- **Menu vs catalogue.** A restaurant menu is small and changes often; a grocery catalogue is large and stock-driven — see [[inventory-tracking]].

## Where it applies

- Menu / catalogue + stock — [[products]] and [[inventory-tracking]].
- Orders flow through the normal [[order-processing-pipeline]].
- Delivery dispatch — [[apps-glovo]] / [[shipping]] / [[fulfillment-and-warehouse]].

## Related

- [[apps-rkeeper]] — restaurant POS integration.
- [[apps-glovo]] — on-demand delivery.
- [[apps-grocery-store-overview-new]] — grocery storefront app.
- [[erp-integrations]] / [[fulfillment-and-warehouse]] / [[shipping]] — POS, fulfilment, and delivery siblings.

## Open Questions

- Whether the grocery-store app gates on a plan-feature (verify).
- Whether [[apps-rkeeper]] syncs menu both ways or POS → store only (verify).
