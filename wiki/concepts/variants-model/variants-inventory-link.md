---
type: concept
nav_path: "Concept → Variants model → Inventory link"
aliases: ["Variant inventory link", "Per-Variant quantity", "Variant stock pointer", "Tracking master switch", "Запас на вариант"]
tags: [catalog, variants, inventory, stock, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Parameter, Option, matrix generation, pricing, image mapping, known issues).

# Variants model — Inventory link

## Definition

Each [[variant|Variant]] carries its **own** `quantity` integer — independent of every other Variant of the same product. Selling out of "Red Large T-shirt" does NOT block "Red Medium T-shirt". The Variant is CloudCart's **unit of stock tracking**; there is no per-Product `quantity` column — even a "simple" product with no merchant-defined Parameters has exactly one backing Variant that holds the stock.

The three master switches that control how that `quantity` is interpreted — `tracking`, `continue_selling`, `threshold` — sit on the **parent Product**, not per-Variant. So a product either tracks all its Variants or none; there is no "track Red but not Blue" on the same product.

**This is the pointer page.** The full inventory model — when stock decrements, restock on cancel / refund, oversell clamping at 0, bundle stock, multi-warehouse via apps, low-stock alerts, the debugging playbook — lives on [[inventory-tracking]] and its aspect pages. The Variants-model cluster only documents the *link* between the Variant entity and the inventory system.

## Scope

Covered here (briefly, with pointers):

- The Variant-as-unit-of-stock rule and where `quantity` is edited.
- The three product-level master switches and their interaction with Variants.
- The `tracked` flag captured on order-line records at order time.
- Pointers into the full inventory model for everything else.

NOT covered here — see the linked aspect:

- When stock decrements (`paid` vs `pending` decrement setting) — see [[inventory-decrement-timing]].
- Automatic stock return on cancel / refund / void — see [[inventory-restock]].
- The oversell flag + clamp-at-0 rule — see [[inventory-oversell]].
- Bundle stock derivation — see [[inventory-bundle-stock]].
- Multi-warehouse via apps — see [[inventory-multi-warehouse]].
- In-stock badge + low-stock email gating — see [[inventory-in-stock-badge]].
- "Stock changed and we didn't change it" investigation — see [[inventory-debugging-playbook]].
- The three master switches in depth + `quantity = NULL` semantics — see [[inventory-variant-model]].

## Contrasts

- **Variants model vs Inventory tracking** — this cluster ([[variants-model]]) covers the *structural* Parameter / Option / Variant hierarchy. [[inventory-tracking]] covers the *behavioural* stock model — when `quantity` changes, who can buy at 0, etc. The Variant entity is the shared object; the two clusters slice it from different angles.
- **Per-Variant `quantity` vs per-Product `tracking`** — `quantity` lives on the [[variant|Variant]] (per-SKU); `tracking` lives on the [[product|Product]] (master switch). The merchant cannot have "track Red but not Blue" — it's all-or-nothing per product.
- **`quantity = 0` vs `quantity = NULL`** — `0` is "out of stock, blocked unless `continue_selling = yes`". `NULL` is "unlimited" — every storefront and admin check treats it as in-stock; [[products-missing-product]] renders it as `∞`. See [[inventory-variant-model]].

## Where it applies

Per-Variant `quantity` is edited from three places:

- The Variants section of the product editor on [[products-products]] — one row per Variant in the matrix, with `quantity` editable inline.
- [[products-inventory]] (Products → Inventory) — bulk Update Quantities with **Set** mode (replace) and **Add** mode (delta).
- Bulk imports via [[apps-csv-import]] (CSV) and [[apps-xml-sync]] (XML feeds) — both write `variant.quantity` rows.

The three master switches (`tracking`, `continue_selling`, per-product `threshold`) live on the product Edit page on [[products-products]]. The Inventory list also exposes the per-row `continue_selling` toggle for quick changes without opening the full product editor. See [[inventory-variant-model]] for the validation rules around these switches (e.g., `continue_selling = yes` requires `tracking = yes`; `threshold` cannot be set when `tracking = no`; `threshold = 0` is rejected).

### Per-order-line `tracked` flag

Each OrderProduct line has its own `tracked` flag (Yes / No) captured **at order time** that records whether the decrement actually happened on that specific line. A single order with 5 lines can have line-level mixing — some lines were decrementing (`tracked = yes`, the product had `tracking = yes` at order time), others were untracked products (`tracked = no`).

On cancellation / refund, only the `tracked = yes` lines get re-credited — `tracked = no` lines have nothing to return. See [[inventory-restock]] for the full restock catalogue.

This is why **switching a product's `tracking` flag mid-life is safe**: an order placed when the product was tracked correctly re-credits on cancel (the line's `tracked = yes` is captured at order time and persisted). An order placed when the product was untracked correctly doesn't try to re-credit. The flag on the order line is independent of the current product setting.

### Cascade re-index / cache invalidation on stock save

Every Variant `quantity` save fires the same side-effect chain documented in [[variants-pricing]] — the search re-index for the parent product id, `ProductUpdated` event firing the `product.updated` webhook on [[settings-hooks]], and product-cache clear. See [[storefront-architecture]] for why the storefront can lag after a stock change (the search index sync is queued).

Bulk updates de-duplicate by parent-product id — touching 50 Variants on the same product fires the events once for that product, not 50 times.

### `multi_variants` plan gate

The "Multi variant" product type is hidden from the Add product flow on plans without the `multi_variants` feature key. Merchants on those plans can only sell single-Variant products (each product has exactly one backing Variant). See [[plan-gates]].

## Related

- [[variants-model]] — hub.
- [[inventory-tracking]] — the full inventory model (hub).
- [[inventory-variant-model]] — the three master switches in depth.
- [[inventory-decrement-timing]] — when stock decrements.
- [[inventory-restock]] — automatic stock return on cancel / refund.
- [[inventory-oversell]] — `continue_selling` + clamp-at-0.
- [[inventory-bundle-stock]] — bundle stock derivation.
- [[inventory-multi-warehouse]] — multi-warehouse via apps.
- [[inventory-in-stock-badge]] — storefront badge + low-stock alerts.
- [[inventory-debugging-playbook]] — "stock changed and we didn't change it" investigation.
- [[variant]] — Variant entity carrying `quantity`, `sku`, `barcode`.
- [[product]] — Product entity carrying `tracking`, `continue_selling`, `threshold`.
- [[products-products]] — product editor with per-Variant matrix + master switches.
- [[products-inventory]] — per-Variant stock-management screen.
- [[plan-gates]] — `multi_variants` plan gate.

## Open Questions

None.
