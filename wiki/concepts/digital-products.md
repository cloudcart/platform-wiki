---
type: concept
nav_path: "Concept → Digital & downloadable products"
route_name: (none)
route_path: (none)
aliases: ["Digital products", "Downloadable products", "Virtual products", "Sell files", "Sell downloads", "Digital goods", "Дигитални продукти", "Сваляеми продукти", "Продажба на файлове", "E-book selling"]
tags: [digital, downloadable, products, product-type, concepts, hub]
plan_gates: ["digital_products"]
created: 2026-06-11
updated: 2026-11-09
source_count: 2
---
# Digital & downloadable products

## Definition

A **digital product** is a non-physical item — a downloadable file (e-book, software, audio, design asset) or access to a page / content — sold instead of a shipped good. A product is flagged **Digital** at creation; the platform then skips shipping for it and delivers the file or page access after purchase. Internally each product carries a `digital` flag, and a merchant-created digital product has a `type_digital` of either **file** or **page**.

## Scope

- **Product type at creation** — choose **Digital** (vs simple / multiple / bundle) when adding a product — see [[products-digital]] for the full create flow and the Files section.
- **Two delivery modes** (`type_digital`):
  - **file** — the customer downloads an attached file after purchase.
  - **page** — the customer is granted access to a page / content; this mode is the [[apps-membership]] integration ("Landing pages").
- **Two internal values** — `wallet` and `gift_card` mark the hidden products behind [[virtual-wallet]] top-ups and [[apps-gift-card]] purchases. Merchants do not choose them; they show in webhook and order payloads. See [[wallet-gift-instrument-checkout]].
- **Plan, not an app** — the **file** mode is native and needs only the plan feature `digital_products`; there is no separate digital-files app. The **page** mode needs [[apps-membership]].
- **No shipping** — a digital product carries no weight and generates no courier waybill; a digital-only cart skips the shipping step at [[checkout-flow]] unless the store-wide **Ask for shipping address for digital products** is on. The product's own **Requires shipping** switch does not change this.
- **Account required** — a cart holding a digital product never offers guest checkout; see [[checkout-flow-guest-vs-registered]].
- **Auto-fulfilled on paid** — a digital-only order needs no waybill and no manual step: it is fulfilled automatically the moment it reaches `paid`, so (with `order_complete = 1`) it auto-promotes to `completed` without a shipping step. See [[order-pipeline-stage-4-fulfillment]].
- **Delivery after purchase** — on a paid or completed order the email and the thank-you page send the buyer to **My account → Files**, which needs sign-in and shows only their own orders' files; no download cap or expiry. Details on [[products-digital]]. A headless storefront gets a 15-minute signed link (`/api/sf/downloads/{id}` — see [[headless-storefront-api]]).
- The `digital` / `type_digital` flags live on the product record — see [[product-entity-attributes]].

## Contrasts

- **Digital vs physical.** Physical = shipped, has weight / stock / waybill; digital = delivered electronically, no shipping step.
- **file vs page mode.** `file` = a downloadable asset; `page` = gated content / access (closer to a membership).
- **Type vs variants.** "Digital" is a product *type*; a digital product has a single variant and cannot have [[products-variants-options|variants]].
- **Digital file vs attached file.** Any product can carry attached files (a manual, a data sheet) with a **Publish file** switch. A published one downloads at `/download/product/public/…` (`site.download.public`). An unpublished one shows only on the buyer's order page and thank-you page, through a link carrying the order's hash (`site.download.private.hash`); `site.download.private` without the hash works only for a signed-in buyer of that product. These are not a digital product's download.

## Where it applies

- Product editor — the Digital type selection ([[products-editor]]).
- Checkout — a digital-only order skips shipping ([[checkout-flow]]).
- Order delivery — the buyer's **Files** page in their account ([[products-digital]]); a signed link on a headless storefront ([[headless-storefront-api]]).

## Related

- [[products-digital]] — the feature page: create flow, Files section, file vs page mode.
- [[apps-membership]] — the app behind the page (Landing pages) mode + membership tiers.
- [[products-editor]] — the product editor that hosts the Files section.
- [[product-entity-attributes]] — the `digital` / `type_digital` fields.
- [[wallet-gift-instrument-checkout]] — the rules for the two internal digital products.
- [[checkout-flow]] — how a digital-only order skips shipping.
- [[headless-storefront-api]] — the signed download endpoint.

## Open Questions

- (Resolved) File limits, types and download access — see [[products-digital]]: up to 5 files, any file-manager type up to 1024 MB, no download cap or expiry.
- Whether digital products track stock (verify).
- (Resolved) The "membership" option is **not** a distinct type — it creates a digital product with `type_digital = page` via the [[apps-membership]] app; see [[products-digital]].
