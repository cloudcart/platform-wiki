---
type: concept
nav_path: "Concept → Inventory tracking"
aliases: ["Inventory tracking", "Stock tracking", "Quantity tracking", "Stock management", "Per-variant stock", "Inventory model", "Oversell handling", "Out-of-stock handling", "Restock detection", "Наличности", "Складова наличност", "Управление на склад", "Проследяване на наличности", "Свободна наличност"]
tags: [catalog, inventory, stock, variants, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 13
---

# Inventory tracking

## Definition

**Inventory tracking** is the platform-wide system that decides — for every sellable SKU in the store — how many units exist, when the count goes down, when it goes back up, whether the storefront still lets the customer buy at zero stock, and which screens / notifications surface stock changes to the merchant. The unit of tracking is the **[[variant|Variant]]**, not the [[product|Product]] — every SKU has its own `quantity` integer.

> **Important: stock does NOT go negative on the order-decrement path.** When a Variant's stock would drop below 0 on a decrement, the platform clamps it to **0** (regardless of the `continue_selling` flag). The merchant tracks "how many units we owe customers" via the count of outstanding orders against a 0-stock Variant — the Variant `quantity` itself never goes negative. This is the most-misstated rule about CloudCart inventory. See [[inventory-oversell]] for the full clamping mechanics.

CloudCart's native inventory tracking is **single-warehouse** — one `quantity` per SKU, with no notion of per-location sub-totals; multi-warehouse fulfilment lives in apps (see [[inventory-multi-warehouse]]). The most-asked operational question is **when** stock drops — set store-wide by `order_status_for_quantity_decrease` on [[settings-cart]] (`paid` default vs `pending`); cancelled / refunded orders return stock automatically, tracked per-line so the platform never double-credits (see [[inventory-decrement-timing]] + [[inventory-restock]]).

**Stock movements ARE auditable** — every Variant `quantity` change (auto-decrements, manual edits, imports, ERP syncs, JSON-API v2 writes) is recorded in the parent product's [[products-change-log|Change log]] with timestamp + explicit Initiator. For "the stock changed and we didn't change it" tickets, the Change log is the **first place to look** — see [[inventory-debugging-playbook]].

## Sub-pages (in this cluster)

This concept is split into 8 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[inventory-variant-model]] — the Variant-as-unit-of-stock rule; the three master switches (`tracking`, `continue_selling`, `threshold`); per-product validation; `multi_variants` plan gate; `quantity = NULL` semantics.
- [[inventory-decrement-timing]] — the `order_status_for_quantity_decrease` setting (`paid` vs `pending`); merchant guidance per payment mix; the deterministic decrement matrix per (status × fulfillment × setting).
- [[inventory-restock]] — automatic stock return on cancel / refund / void / chargeback; the per-line decrement-tracking flag that prevents double-counting; symmetric re-decrement on re-mark-paid.
- [[inventory-oversell]] — the `continue_selling` flag; backorders / pre-orders / replenishable goods; clamping at 0 (Variant `quantity` never goes negative); how to track "owed" units via outstanding paid orders.
- [[inventory-bundle-stock]] — bundle products derive stock from minimum-available across child Variants; child `continue_selling = no` wins over bundle's flag; auto-deactivation when a child deactivates.
- [[inventory-multi-warehouse]] — native single-warehouse; multi-warehouse via [[apps-store-locations]] / [[apps-microbg]] / dropshipping / ERP connectors; what CloudCart does and doesn't support.
- [[inventory-in-stock-badge]] — storefront in-stock / out-of-stock badge logic; `minimum` order quantity blocking sellability at positive stock; low-stock + out-of-stock email alerts and their three-switch gating.
- [[inventory-debugging-playbook]] — the 6-step "stock changed and we didn't change it" support investigation workflow + Initiator decoding table.

## Why it matters to the merchant

Inventory tracking is one of the few systems where a wrong default silently leaks money — either as **oversells** (sold goods the merchant doesn't have) or as **lost sales** (storefront shows out-of-stock while units sit on a shelf). The per-Variant model means stock is never shared across colours / sizes (selling out of "Red Large" does not block "Red Medium" — see [[inventory-variant-model]]); the decrement-timing setting decides whether unpaid orders block stock (see [[inventory-decrement-timing]]); and oversell is opt-in per product, with "how many we owe" read from outstanding paid orders rather than a negative count (see [[inventory-oversell]]). Two insight pages turn stock-state into restock priority: [[products-missing-product]] (back-in-stock subscribers) and [[products-favorite-products]] (wishlist counts).

## Scope

What this concept covers (across the 8 sub-pages):

- The per-Variant tracking model + 3 master switches.
- Stock-decrement timing + the symmetric restock flow.
- Oversell + clamping rules.
- Bundle stock derivation.
- Multi-warehouse via apps.
- In-stock badge + low-stock alert mechanics.
- The debugging playbook for unexpected stock changes.

What it does NOT cover:

- The per-Variant matrix UI on the product editor (rendering, drag-reorder) — that's on [[products-products]].
- Storefront variant-picker UX patterns — those are theme behaviours.
- Reservation / hold semantics during checkout (cart-stage stock reservations are not part of the native model; stock decrement happens on the order, not the cart — see [[cart-vs-order-lifecycle]]).
- Refund money-movement audit (the financial side) — see [[orders-credit]].

## Contrasts

- **Per-Variant tracking vs per-Product tracking** — stock on the Variant; switches on the Product. See [[inventory-variant-model]].
- **Native single-warehouse vs multi-warehouse apps** — see [[inventory-multi-warehouse]].
- **`paid` decrement vs `pending` decrement** — see [[inventory-decrement-timing]].
- **`tracking` vs `continue_selling`** — see [[inventory-variant-model]] + [[inventory-oversell]].
- **Bundle stock vs Component stock** — see [[inventory-bundle-stock]].
- **Decrement IN vs re-credit OUT** — see [[inventory-decrement-timing]] + [[inventory-restock]].
- **Inventory tracking vs Variants model** — this concept covers `quantity` + oversell behaviour. [[variants-model]] covers the structural Parameter / Option / Variant hierarchy.

## Where it applies

The inventory-tracking system spans the catalog, orders flow, insight pages, and downstream notification / webhook surfaces. Each sub-page documents its own application surface. The cross-cutting side-effects are:

- **Every stock save queues a search re-index** of the affected product on the `searchable-import4` queue. Storefront catalog + filter pages read from the search index, not the live database, so the storefront reflects the change only after that queue processes the product. See [[storefront-architecture]] + [[background-queue-inventory]].
- **Storefront cache invalidation** — product-detail, category, and variant-picker fragments are flushed.
- **`product.updated` webhook fires** on every stock change — chatty; receivers must be idempotent. See [[settings-hooks]].

## Related

- [[product]] — Product entity; carries the master switches.
- [[variant]] — Variant entity; carries the per-SKU `quantity`.
- [[variants-model]] — structural Parameter / Option / Variant model.
- [[products-inventory]] — per-Variant stock-management screen.
- [[products-products]] — product editor with per-Variant matrix.
- [[products-change-log]] — Change log modal; the audit trail for stock changes.
- [[products-missing-product]] — back-in-stock subscribers.
- [[products-favorite-products]] — wishlist counts.
- [[products-statuses]] — custom in-stock / out-of-stock labels.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `product_threshold`.
- [[settings-admin-notifications]] — low-stock + out-of-stock email gating.
- [[settings-general]] — `site_email` as default recipient.
- [[settings-hooks]] — `product.updated` webhook fires on stock changes.
- [[order]] / [[orders-details]] / [[orders-status-change]] — status transitions drive decrement / restock.
- [[cart-vs-order-lifecycle]] — cart-stage vs order-stage stock semantics.
- [[order-processing-pipeline]] — the full status-transition pipeline.
- [[storefront-architecture]] — search-index read-side (why the storefront can lag after a stock change).
- [[background-queue-inventory]] — `searchable-import4` queue + the search-index sync chain.
- [[apps-csv-import]] / [[apps-xml-sync]] — bulk imports that bypass the low-stock alert.
- [[apps-store-locations]] / [[apps-microbg]] / [[apps-microinvest]] — multi-warehouse / ERP sync apps.

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages.
