---
type: concept
nav_path: "Concept → Variants model"
route_name: (none)
route_path: (none)
aliases: ["Variants model", "Parameter Option Variant", "Variant hierarchy", "Variant taxonomy", "Variant data model", "Parameter vs Option vs Variant", "SKU model", "Product variants explained", "Параметри и варианти", "Опции и варианти"]
tags: [catalog, products, variants, parameters, options, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 11
---

# Variants model

## Definition

The CloudCart catalogue separates a "product with variations" into **three distinct concepts**. Merchants who treat them as one — saying "I added 30 variants" when they actually added 6 Parameter Options across 2 Parameters that produce 15 SKUs — quickly confuse themselves and the support team.

1. **[[variants-parameter|Parameter]]** — a **store-wide attribute definition** naming one customisation dimension ("Colour", "Size", "Material"). A singleton in the catalogue — one Colour Parameter is reused by every product that uses colour. Managed on [[products-variants-options]]. Carries a name, a display type, an Active flag, sort order, and the `variants.listing` premium toggle. See [[variants-parameter]] for the 6 display types and locked-after-creation rule.

2. **[[variants-option|Option]]** — a **value** belonging to one Parameter ("Red", "Blue" under Colour; "S", "M", "L" under Size). Options have NO SKU, NO stock, NO price — they are pure catalogue dictionary entries. See [[variants-option]].

3. **[[variant|Variant]]** — a **specific combination of Options on a specific product**, carrying the sellable data: SKU code, barcode, `quantity` (stock), `price` (overrides product base price), `weight`, `delivery_price`, `minimum` order quantity, unit-of-measure fields. Generated on the product editor's Variants section ([[products-products]]).

Said in one line: **Parameters define the dimensions, Options define the values, Variants are the actual sellable SKUs that combine specific Options for a specific product.**

**Two hard caps bound a product's matrix** — see [[variants-matrix-generation]]:

- **3 Parameters per product** — the Variant record has only `v1` / `v2` / `v3` slots; no v4 exists.
- **500 Variants per product** — at product-save validation; error reads *"max allowed 500 exceeded"*.

The ability to create multi-Variant products is plan-gated by the `multi_variants` feature key — on plans without it, the "Multi variant" product type is hidden from the Add product flow. See [[plan-gates]].

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[variants-parameter]] — the store-wide attribute definition; 6 display types; **locked-after-creation** rule; deletion guard; cascade rename; Active-flag soft hide.
- [[variants-option]] — the values within a Parameter; cascade rename to every Variant label; the irreversible **Merge values** action; why Options carry no SKU / stock / price.
- [[variants-matrix-generation]] — how 3 Parameters × N Options expand into per-product Variant rows; the v1 / v2 / v3 slots; 3-Parameter cap and 500-Variant cap; `default_variant_id` auto-computation; `price_from` / `price_to` denormalisation; product-save validation list.
- [[variants-pricing]] — per-Variant `price` overriding base price; `discount_price` strikethrough field; `delivery_price` per-Variant shipping; unit-of-measure auto-fills; the cascade re-index on every price save.
- [[variants-inventory-link]] — pointer page linking the Variant entity to [[inventory-tracking]]; the per-product master switches (`tracking`, `continue_selling`, `threshold`); the order-line `tracked` flag captured at order time.
- [[variants-image-mapping]] — the 3-layer image fallback chain (Product / Option / Variant); the Variant `image` + `images` relationships; auto-cleanup of `ImageVariant` records on Variant delete.
- [[variants-known-issues]] — by-design constraints vs bugs; merchant-facing workarounds; corrections to earlier wiki claims (Variants DO have their own images; `minimum` auto-corrects to 1; `continue_selling` requires `tracking = yes`).

## Scope

What this cluster covers (across the 7 sub-pages): the three-layer hierarchy (Parameter / Option / Variant); the 6 Parameter display types and locked-after-creation rule; the hard caps (3 Parameters per product, 500 Variants per product, 50,000,000 Variant `quantity`, 1,000,000,000 minor units `price` / `discount_price`); cascade renames; irreversible Option Merge; deletion guards on in-use Parameters / Options; per-Variant sellable attributes; the 3-layer image model; and the `variants.listing` premium. Each sub-page below owns one slice.

What it does NOT cover:

- Per-product Variant matrix UI mechanics (rendering, drag-reorder) — see [[products-products]].
- Property mechanics — see [[products-property]] for the category-scoped Property model.
- Product Options app mechanics — see [[products-options-overview]] for the customer-input customisation Options layer.
- Inventory algorithms (when stock decrements, restock on cancel, oversell, bundles, multi-warehouse, low-stock alerts, debugging) — see [[inventory-tracking]] and aspects.
- Storefront variant-picker UX patterns (which picker shows first, dependency between pickers) — storefront-theme behaviours.

## Contrasts

- **Variants vs Properties** — Variants create separate SKUs with separate stock — **purchase-determining** ("pick a size"). [[products-property|Properties]] are category-scoped descriptive specs — they don't split SKUs, don't gate Add-to-cart, and serve mostly as category-page filters. Variants are store-wide; Properties are category-scoped. *Rule of thumb:* per-SKU dimensions → Variant Parameter; descriptive-only dimensions → Property.
- **Variants vs Product Options** — Variants are pre-defined SKU variations configured upfront. [[products-options-overview|Product Options]] are customer-input fields at the cart line (engraving text, gift wrap, date picker) — no SKU split, no per-Option stock. A T-shirt can have Size + Colour as Variants AND "Add custom name embroidery" as a Product Option.
- **Variants list (catalogue-wide) vs Variants matrix (per-product)** — [[products-variants-options]] manages Parameters + Options catalogue-wide; the Variants section on each product's editor ([[products-products]]) generates the per-product Variant rows and sets sellable attributes. Two screens, two purposes; both surface the word "Variants" which causes confusion. See [[variants-matrix-generation]].
- **Inventory tracking vs Variants model** — [[inventory-tracking]] covers `quantity` behaviour (decrement, oversell, restock); this cluster covers the structural Parameter / Option / Variant hierarchy. The Variant entity is shared. See [[variants-inventory-link]].

## Where it applies

The Variants model touches catalogue management, per-product editing, bulk imports, pricing/discounts, and the storefront.

- **Catalogue-wide:** [[products-variants-options]] (Parameters + Options dictionary).
- **Per-product:** [[products-products]] (editor with per-product Variants matrix); [[products-inventory]] (aggregated per-Variant stock).
- **Bulk operations:** [[apps-csv-import]], [[apps-xml-import]], [[apps-xml-sync]] — all auto-create Parameters / Options / Variants from feeds.
- **Discount / pricing:** [[marketing-discounts]] (per-Variant targeting), [[marketing-discounts-quantity]] (quantity-tier discounts on per-Variant stock).
- **Storefront:** product detail page renders Parameter pickers in the chosen display type; category page shows one card per product by default, one card per Variant with `variants.listing` ON.
- **Plan-gating:** [[plan-gates]] — `multi_variants` (gates the "Multi variant" product type) and `variants.listing` (gates "Show variants as separate products in listing").

## Related

- [[product]] — Product entity that owns Variants.
- [[variant]] — Variant entity.
- [[products-variants-options]] — the Variants management screen (catalogue-wide Parameters + Options).
- [[products-property]] — Category-scoped Properties (NOT Variants — descriptive, no SKU split).
- [[products-options-overview]] — Per-product Product Options app (NOT Variants — no stock split).
- [[product-option]] — Product-Option entity (the customisation Options layer).
- [[category-property]] — Category-Property entity (the Properties layer).
- [[products-products]] — Product editor where per-product Variants matrices live.
- [[products-inventory]] — Inventory tracks per-Variant `quantity`.
- [[apps-csv-import]] — Bulk-create Variants from CSV.
- [[apps-xml-import]] / [[apps-xml-sync]] — Bulk-create Variants from XML feeds.
- [[marketing-discounts]] — Per-Variant discount targeting.
- [[marketing-discounts-quantity]] — Quantity-tier discounts per Variant.
- [[inventory-tracking]] — Stock tracking; per-Variant quantities.
- [[plan-gates]] — `multi_variants` and `variants.listing` plan gates.
- [[checkout-flow]] — Customer's Variant choice becomes an order line item referencing the chosen Variant.
- [[settings-hooks]] — `product.updated` webhook fires on every Variant save.

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages.
