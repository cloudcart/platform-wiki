---
type: concept
nav_path: "Concept → Digital & downloadable products"
route_name: (none)
route_path: (none)
aliases: ["Digital products", "Downloadable products", "Virtual products", "Sell files", "Sell downloads", "Digital goods", "Дигитални продукти", "Сваляеми продукти", "Продажба на файлове", "E-book selling"]
tags: [digital, downloadable, products, product-type, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-08-06
source_count: 1
---
# Digital & downloadable products

## Definition

A **digital product** is a non-physical item — a downloadable file (e-book, software, audio, design asset) or access to a page / content — sold instead of a shipped good. A product is flagged **Digital** at creation; the platform then skips shipping for it and delivers the file or page access after purchase. Internally each product carries a `digital` flag, and a digital product has a `type_digital` of either **file** or **page**.

## Scope

- **Product type at creation** — choose **Digital** (vs simple / multiple / bundle) when adding a product — see [[products-digital]] for the full create flow and the Files section.
- **Two delivery modes** (`type_digital`):
  - **file** — the customer downloads an attached file after purchase.
  - **page** — the customer is granted access to a page / content; this mode is the [[apps-membership]] integration ("Landing pages").
- **No shipping** — a digital product carries no weight and generates no courier waybill; a digital-only cart skips the shipping step at [[checkout-flow]].
- **Auto-fulfilled on paid** — a digital-only order needs no waybill and no manual step: it is fulfilled automatically the moment it reaches `paid`, so (with `order_complete = 1`) it auto-promotes to `completed` without a shipping step. See [[order-pipeline-stage-4-fulfillment]].
- **Delivery after purchase** — the file is served through a signed, order-scoped download link (the headless storefront exposes a signed `/api/sf/downloads/{id}` endpoint — see [[headless-storefront-api]]).
- The `digital` / `type_digital` flags live on the product record — see [[product-entity-attributes]].

## Contrasts

- **Digital vs physical.** Physical = shipped, has weight / stock / waybill; digital = delivered electronically, no shipping step.
- **file vs page mode.** `file` = a downloadable asset; `page` = gated content / access (closer to a membership).
- **Type vs variants.** "Digital" is a product *type*, orthogonal to whether the product has [[products-variants-options|variants]] or belongs to a bundle.

## Where it applies

- Product editor — the Digital type selection ([[products-editor]]).
- Checkout — a digital-only order skips shipping ([[checkout-flow]]).
- Order delivery — signed download link per order ([[headless-storefront-api]]).

## Related

- [[products-digital]] — the feature page: create flow, Files section, file vs page mode.
- [[apps-membership]] — the app behind the page (Landing pages) mode + membership tiers.
- [[products-editor]] — the product editor that hosts the Files section.
- [[product-entity-attributes]] — the `digital` / `type_digital` fields.
- [[checkout-flow]] — how a digital-only order skips shipping.
- [[headless-storefront-api]] — the signed download endpoint.

## Open Questions

- Exact file-upload limits, accepted types, and download caps / expiry for the Downloadable-files mode (verify) — see [[products-digital]].
- Whether digital products track stock and/or enforce download limits / expiry (verify).
- (Resolved) The "membership" option is **not** a distinct type — it creates a digital product with `type_digital = page` via the [[apps-membership]] app; see [[products-digital]].
