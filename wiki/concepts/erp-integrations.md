---
type: concept
nav_path: "Apps → ERP & accounting integrations"
route_name: (none)
route_path: (none)
aliases: ["ERP integrations", "ERP", "Accounting integrations", "ERP sync", "ЕРП интеграции", "Складов софтуер", "Счетоводен софтуер", "Sync with ERP", "Accounting software", "Inventory software"]
tags: [erp, integrations, apps, sync, accounting, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---
# ERP & accounting integrations

## Definition

**ERP integrations** connect the store to an external **ERP / accounting / inventory-management system**, so the merchant's product catalogue, stock levels, prices, and orders stay in sync between CloudCart and the system that runs their back office. Each integration is installed as a separate app from the [[apps]] App Store; there is **no single "ERP" admin screen** — CloudCart groups these as a dedicated ERP app category, and this page is the directory of the supported systems plus the shared sync model behind them.

## Scope

A typical ERP integration synchronises some or all of:

- **Catalogue / categories** — products and their categories pushed or pulled between the two systems.
- **Inventory** — stock quantities kept in step (the ERP is usually the source of truth — see [[inventory-tracking]]).
- **Prices** — price lists maintained in the ERP flow into the store.
- **Orders** — placed orders are exported into the ERP for invoicing / accounting / dispatch.

Direction, frequency, and which of these are covered differ per system — see each app page. Install and configuration always happen through [[apps]].

## Contrasts

- **ERP vs storefront catalogue** — the ERP is usually the source of truth for stock and prices; CloudCart reflects them rather than the reverse (unless a specific app says otherwise).
- **ERP vs [[fulfillment-and-warehouse]]** — ERP/accounting apps sync *data* (catalogue, stock, orders, invoices); fulfillment apps move *physical goods*.
- **ERP vs one-off import** — ERP integrations sync continuously; an [[apps-csv-import]] / XML feed is a manual snapshot, not a live link.

## Supported systems (directory)

- [[apps-microinvest]] — Microinvest (BG accounting / warehouse software).
- [[apps-microbg]] — Microinvest-family integration (BG).
- [[apps-colibri]] — Colibri ERP.
- [[apps-selmatic]] — SelMatic ERP.
- [[apps-gensoft]] — Gensoft.
- [[apps-it4profit]] — It4Profit.
- [[apps-polycomp]] — Polycomp.
- [[apps-versus-erp]] — Versus ERP.
- [[apps-barsy]] — Barsy (POS / retail).
- [[apps-posmaster]] — PosMaster (POS + retail ERP).
- [[apps-rkeeper]] — r_keeper (restaurant / hospitality POS).
- [[apps-universum]] — Universum.
- [[apps-zeron]] — Zeron.
- [[apps-vali-computers]] — Vali Computers.
- [[apps-also]] — ALSO distribution feed.
- [[apps-finaleinventory]] — Finale Inventory (inventory management).

## Where it applies

- Stock behaviour once an ERP owns inventory — see [[inventory-tracking]].
- Product / price data flowing into the catalogue — see [[products]].
- Order export for invoicing — see [[orders]].

## Related

- [[apps]] — the App Store (install any of the above; ERP category).
- [[external-record-mapping]] — the shared ID↔ID table (`ExternalMetaData`) every ERP uses to match incoming external items to CloudCart records, plus the internal read queries.
- [[fulfillment-and-warehouse]] — sibling integration category for picking / packing / 3PL.
- [[inventory-tracking]] — how stock is tracked once an external system feeds it.

## Open Questions

- Per-system sync direction + frequency matrix (verify against each app page).
- Whether [[apps-also]] is best classed as ERP or as a product feed (verify).
