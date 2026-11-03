---
type: concept
nav_path: "Concept → Inventory tracking → Multi-warehouse"
aliases: ["Inventory multi-warehouse", "Multiple warehouses", "Per-warehouse stock", "Store locations", "Dropshipping stock sync", "ERP stock sync", "Multi-warehouse not native"]
tags: [catalog, inventory, stock, multi-warehouse, apps, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, decrement timing, restock, oversell, bundle stock, in-stock badge, debugging playbook).

# Inventory — multi-warehouse (via apps)

## Definition

CloudCart's **native inventory model is single-warehouse** — one `quantity` per Variant, with no concept of "5 in Sofia warehouse + 3 in Plovdiv warehouse = 8 total". Merchants running multiple physical warehouses install a **multi-warehouse app**, dropshipping integration, or ERP connector that:

- Owns the per-warehouse stock **externally** (the app's own DB tables, or the ERP / dropshipper's source-of-truth).
- Periodically pushes the **aggregate** (sum across warehouses) into CloudCart's per-Variant `quantity`.
- Handles fulfilment routing on the warehouse-side based on order-shipping address + warehouse rules.

The storefront does NOT show "available in Sofia 5, Plovdiv 3" — the customer just sees "In stock" or "Out of stock" based on the aggregated `quantity`. The merchant's warehouse-side dashboard lives **inside the app**, not in the CloudCart admin.

There are **two distinct app patterns** here:

- **Aggregate-sync** (ERP / dropshipping / headless) — the app owns per-warehouse stock externally and pushes the *sum* into one `quantity`; every customer sees the same number. Most of this page covers this pattern.
- **Geo-zone routing** (the built-in [[apps-store-locations]] app, working alongside the [[apps-stores]] Local-Pickup app) — availability is **switched by the customer's location**: a Sofia customer sees the Sofia warehouse's stock, a Plovdiv customer sees Plovdiv's. The routing key is the customer's [[settings-geo-zones|geo zone]] (resolved from their address, stored in a cookie) — see [[geo-targeting]]. This is the pattern for *"different stock per customer location"*.

## Scope

Covered:

- Why native CloudCart is single-warehouse and what that means in practice.
- The three common multi-warehouse patterns (dropshipping, ERP connectors, headless fulfilment).
- What the storefront does and doesn't show.
- What the merchant gives up by leaving CloudCart's native model.

Not covered here:

- The per-Variant tracking model — see [[inventory-variant-model]].
- Specific multi-warehouse app pages — see [[apps-store-locations]], [[apps-microbg]], [[apps-microinvest]], [[apps-fgo]], [[apps-smart-bill]], [[apps-emag-sync]] for the integrations themselves.
- Order routing logic — owned by the app, not CloudCart.

## Contrasts

- **Native single-warehouse vs multi-warehouse apps** — native CloudCart has one `quantity` per Variant — no location breakdown. Multi-warehouse merchants install a separate app or ERP connector that owns per-warehouse stock externally and syncs the aggregate into the per-Variant `quantity`.
- **CloudCart-side `quantity` (aggregate) vs app-side per-warehouse counts** — what the merchant sees in [[products-inventory]] is the **sum** the app last synced. The per-warehouse breakdown lives in the app's own admin. Editing the CloudCart-side `quantity` manually is usually a bad idea — the next app-sync will overwrite it with the latest aggregate.
- **CloudCart's order-decrement vs app's fulfilment routing** — when a CloudCart order moves to a decrementing status, CloudCart decrements the aggregate `quantity`. The app then routes the fulfilment to the right warehouse separately, based on its own logic. These two flows can diverge if the app's sync is delayed.

## Where it applies

Common patterns for multi-warehouse operations:

### Dropshipping integrations

The supplier's stock is the source of truth. CloudCart pulls aggregate availability via XML / API sync (typically via [[apps-xml-sync]] or a custom app). Stock counts move only in one direction: supplier → CloudCart. The merchant doesn't manage the warehouse-side at all.

Risks: aggregate availability can drift between sync runs (typically every few minutes to hourly). Orders placed against the cached count can fail at the supplier's side if the supplier sells out between syncs.

### ERP connectors (Szamlazz, FGO, SmartBill, Profics, Micro.bg, custom)

The ERP holds per-warehouse stock. An integration job (per the specific app — see [[apps-microbg]] for the canonical 3-minute pattern) syncs the aggregate into CloudCart's per-Variant `quantity`. The ERP handles the per-warehouse routing on fulfilment.

The merchant has TWO admin panels in this scenario: CloudCart's admin (storefront, orders, customers) + the ERP's admin (warehouse stock, invoicing, accounting). Routine warehouse operations happen in the ERP.

### Multi-warehouse apps (geo-zone routing)

The built-in **[[apps-store-locations]]** app adds per-location stock tracking inside CloudCart itself (rather than in an external ERP) and — unlike the aggregate-sync pattern — **switches the catalog availability by the customer's [[settings-geo-zones|geo zone]]**: each zone maps to one or more warehouses, and a customer in that zone sees the stock (and shipping) of the warehouse serving it. It works **in symbiosis with [[apps-stores]]** (Local Pickup), which defines the physical shop/warehouse records and provides the per-store quantity editor; Store Locations adds the geo-routing on top. When [[apps-store-locations]] is installed, the order-event side of [[order-processing-pipeline]] Stage 2 (storefront search index sync + `product.updated` webhook) is **skipped** — that app handles its own per-location stock sync. See [[apps-store-locations]] for the full routing rules.

### Headless fulfilment

The merchant runs CloudCart as the storefront-only layer and exposes orders via webhooks to an external warehouse-management system. CloudCart is the order-of-record; the WMS picks orders up and routes them. The aggregate `quantity` is push-updated back to CloudCart from the WMS.

This is the most flexible pattern but requires custom integration work — there's no off-the-shelf "headless WMS" connector documented; the merchant builds against the platform's [[settings-hooks|webhooks]] + [[json-api-v2|JSON-API v2]].

### What CloudCart does NOT support natively

- **Per-customer-zone warehouse selection** — showing different stock to Sofia vs Plovdiv customers based on geo-routing is **not native**, but the built-in [[apps-store-locations]] app adds exactly this (see the geo-zone routing pattern above).
- **Per-warehouse pricing** — a Variant has one price; per-location pricing requires the app to handle it externally (some apps do, by writing the per-zone effective price into CloudCart's `price`).
- **Warehouse-side reservations during cart** — CloudCart's native model doesn't reserve stock during the cart stage; reservation happens at the order-status transition per [[inventory-decrement-timing]]. Multi-warehouse apps that need true cart-stage reservations implement them externally.

## Related

- [[inventory-tracking]] — hub.
- [[inventory-variant-model]] — the per-Variant `quantity` field that aggregate syncs write into.
- [[inventory-decrement-timing]] — order-status-driven decrement on the aggregate.
- [[inventory-debugging-playbook]] — multi-warehouse syncs are a frequent suspect in "stock changed unexpectedly" tickets.
- [[apps-store-locations]] — built-in multi-location app (geo-zone availability routing).
- [[apps-stores]] — Local Pickup app that pairs with Store Locations (defines the shops + per-store quantity editor).
- [[settings-geo-zones]] — the zones that map to warehouses for geo-routing.
- [[geo-targeting]] — how the customer's zone is resolved from their address.
- [[apps-microbg]] — Bulgarian cloud accounting + warehouse, 3-min sync pattern.
- [[apps-microinvest]] — Microinvest Delta on-prem ERP (different product from Micro.bg).
- [[apps-fgo]] / [[apps-smart-bill]] / [[apps-szamlazz]] — invoicing / ERP integrations with optional stock sync.
- [[apps-emag-sync]] — eMag marketplace stock sync.
- [[apps-xml-sync]] — generic supplier-feed stock sync.
- [[settings-hooks]] — webhooks the merchant subscribes for headless fulfilment.
- [[json-api-v2]] — API surface for headless integrations.
- [[order-processing-pipeline]] — Stage 2 sync skip when `apps-store-locations` is installed.

## Open Questions

None.
