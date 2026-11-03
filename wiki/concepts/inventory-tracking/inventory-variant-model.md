---
type: concept
nav_path: "Concept → Inventory tracking → Variant model"
aliases: ["Inventory variant model", "Per-variant stock", "Stock unit of tracking", "Master switches per product", "Tracking + continue_selling + threshold", "Складова единица — Variant"]
tags: [catalog, inventory, stock, variants, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (decrement timing, restock, oversell, bundle stock, multi-warehouse, in-stock badge, debugging playbook).

# Inventory — the Variant model

## Definition

CloudCart's **unit of stock tracking is the [[variant|Variant]], not the [[product|Product]]**. Every SKU has its own `quantity` integer that drives the in-stock / out-of-stock decision independently of every other SKU. Multi-variant products track per-SKU stock; "simple" products with no merchant-defined variant parameters still have exactly **one** backing Variant under the hood that carries the `quantity`, `sku`, `barcode`, `price`, `weight` — there is no `quantity` field directly on the Product record.

Three master switches sit on the **parent Product** (not per-Variant), so they apply to every Variant of the product equally:

| Setting | What it does | Default |
|---------|--------------|---------|
| `tracking` | Master switch. When `no`, the platform **ignores** every Variant's `quantity` for this product — the product is always treated as in-stock regardless of the number. When `yes`, per-Variant `quantity` drives the in-stock / out-of-stock logic. | `yes` |
| `continue_selling` | Allow-oversell flag — see [[inventory-oversell]]. When `yes`, customers can buy a Variant even at `quantity = 0`; the value is clamped to 0 on decrement (never goes negative). When `no`, the storefront blocks Add-to-cart at `quantity = 0`. | `no` |
| `threshold` | Per-product low-stock alert level — overrides the store-wide `product_threshold` setting from [[settings-cart]]. When a Variant's `quantity` drops to or below this, the `product_quantity_low` admin email fires (see [[inventory-in-stock-badge]] for the full alert gating). | (uses store-wide default) |

Typical configurations:

- **Hard-stocked physical goods** that run out: `tracking = yes`, `continue_selling = no`, `threshold = 5`.
- **Replenishable / pre-order goods**: `tracking = yes`, `continue_selling = yes`, `threshold = empty`.
- **Digital products / services** (no physical stock): `tracking = no`. The storefront never shows out-of-stock regardless of what `quantity` says.

## Scope

Covered:

- The Variant-as-unit-of-stock rule and why simple products still have a backing Variant.
- The three master switches (`tracking`, `continue_selling`, `threshold`).
- Validation around `threshold` (rejects `0`, rejects when `tracking = no`).
- Where the merchant edits per-Variant `quantity`.
- The `multi_variants` plan gate.

Not covered here:

- When stock decrements — see [[inventory-decrement-timing]].
- Stock return on cancel / refund — see [[inventory-restock]].
- Oversell semantics — see [[inventory-oversell]].
- Bundle product stock — see [[inventory-bundle-stock]].
- Multi-warehouse — see [[inventory-multi-warehouse]].
- Storefront badge + alert gating — see [[inventory-in-stock-badge]].

## Contrasts

- **Per-Variant tracking vs per-Product tracking** — stock lives on the [[variant|Variant]], not the [[product|Product]]. A multi-variant product has independent stock per Variant SKU; selling out of one Variant doesn't block the others.
- **`tracking` vs `continue_selling`** — `tracking` is the master switch; when OFF, `quantity` is ignored entirely (product always in stock). `continue_selling` is the oversell flag; when ON, customers can buy even at `quantity = 0`. The two operate independently.
- **Per-product `threshold` vs store-wide `product_threshold`** — per-product setting overrides the store-wide default from [[settings-cart]]. Blank per-product field falls back to store-wide.

## Where it applies

The Variant-as-stock-unit rule shows up across the catalogue and import surfaces:

- **Per-Variant quantity is edited from three places**: the product Edit page's Variants section (one row per Variant), [[products-inventory]] (Products → Inventory with bulk Update Quantities + Set/Add modes), and bulk imports via [[apps-csv-import]] / [[apps-xml-sync]] writing `variant.quantity` rows.
- **The three master switches live on the product Edit page** (`tracking`, `continue_selling`) and the Inventory list also has the per-row `continue_selling` toggle.
- **`multi_variants` is a plan gate** — the "Multi variant" product type appears in the Add product flow only on plans that include the `multi_variants` feature. Plans without it allow only simple (single-variant) products.

**Per-product `threshold` opt-out rules** — leaving the per-product threshold field blank falls back to the store-wide `product_threshold` from [[settings-cart]]. Entering `0` is **rejected** with *"threshold has invalid value"* (the `intval` cast treats `0` as missing). The threshold field is also rejected when `tracking = no` is set — *"product cannot have threshold if not tracked"*. To effectively disable low-stock alerts for a product, either turn off the per-product threshold (falls back to store-wide), turn off `mail_product_quantity_low` globally on [[settings-admin-notifications]], or set store-wide `product_threshold` to a very low value.

**`quantity = NULL` means unlimited stock.** A Variant whose `quantity` field is NULL (rather than 0) is treated as **unlimited inventory** by every storefront and admin check. The [[products-missing-product]] page renders NULL as `∞`. NULL appears on Variants that were originally tracked but had `tracking` removed, OR on products imported via feeds without quantity data. Setting `quantity = 0` explicitly is a different state — sellable only if `continue_selling = yes`.

## Related

- [[inventory-tracking]] — hub.
- [[product]] — Product entity; carries `tracking`, `continue_selling`, `threshold`.
- [[variant]] — Variant entity; carries `quantity`, `sku`, `barcode`, `price`, `weight`.
- [[variants-model]] — Parameter / Option / Variant hierarchy that stock tracks against (different concept).
- [[products-inventory]] — the per-Variant stock-management screen.
- [[products-products]] — product editor with per-Variant matrix + master switches.
- [[settings-cart]] — store-wide `product_threshold` default.
- [[plan-gates]] — `multi_variants` plan gate.

## Open Questions

None.
