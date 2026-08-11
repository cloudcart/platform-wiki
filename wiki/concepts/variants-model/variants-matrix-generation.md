---
type: concept
nav_path: "Concept → Variants model → Matrix generation"
aliases: ["Variant matrix", "Variants matrix", "Variant generation", "3-Parameter cap", "500-variant cap", "v1 v2 v3 slots", "Default variant", "Матрица на варианти", "Генериране на варианти"]
tags: [catalog, variants, parameters, options, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Parameter, Option, pricing, inventory link, known issues).

# Variants model — Matrix generation

## Definition

**Matrix generation** is the per-product step where the merchant attaches catalogue-level [[variants-parameter|Parameters]] to a product, picks which [[variants-option|Options]] of each Parameter it carries, and the platform expands the cartesian product into per-Variant rows. Each row is one [[variant|Variant]] — a specific combination of Options that becomes its own sellable SKU with its own stock and (optionally) price.

The matrix lives on the Variants section of each product's editor on [[products-products]] — NOT on the catalogue-wide [[products-variants-options]] screen, which only defines what Parameters and Options exist. The editor decides which combinations actually sell.

Two hard caps bound the matrix size: **3 Parameters per product** (`v1` / `v2` / `v3` slots — no `v4`) and **500 Variants per product** (total rows after expansion; rejected on save with *"max allowed 500 exceeded"*).

## Scope

Covered here: the 3-Parameter cap (`v1` / `v2` / `v3` slots); the 500-Variant cap and other product-save validation limits; cartesian-product expansion math; `default_variant_id` auto-computation (lowest price, ties by ID); `price_from` / `price_to` denormalisation on the parent Product; Variants having no `created_at` / `updated_at`; the `multi_variants` plan gate hiding the "Multi variant" product type; duplicate combination / duplicate Parameter rejection on save; the `minimum` floor auto-correction; unit-of-measure auto-fills.

Not covered here: the Parameter definition — see [[variants-parameter]]; Option values within a Parameter — see [[variants-option]]; per-Variant price, base-price override + discounts — see [[variants-pricing]]; per-Variant `quantity` semantics + tracking — see [[variants-inventory-link]] + [[inventory-tracking]]; per-Variant image gallery — see [[variants-image-mapping]].

## Contrasts

- **Catalogue-wide Variants screen vs per-product Variants matrix** — [[products-variants-options]] manages Parameters + Options catalogue-wide; the matrix on [[products-products]] generates the per-product Variant rows. Both surface the word "Variants", which causes confusion (see [[variants-model]]).
- **0 vs 1 vs 3 Parameters** — a "simple" product (no merchant-defined Parameters) still has exactly **one** backing Variant carrying `quantity` / `sku` / `barcode` / `price` / `weight`; products with 1, 2, or 3 Parameters expand to N rows. There is no zero-Variant product.
- **3-Parameter cap vs 500-Variant cap** — different ceilings, different scaling patterns. 3 Parameters × 3 Options = 27 Variants (under 500); 3 Parameters × 8 Options = 512 (rejected by the 500 cap). 4 Parameters is impossible regardless of Option counts.

## Where it applies

The matrix expansion shows up on:

- The Variants section of the product editor on [[products-products]] — picker to attach 1, 2, or 3 Parameters; per-Parameter Option-include checklist; then the generated matrix grid, one row per combination.
- [[products-inventory]] — aggregates per-Variant `quantity` across all products' matrices, with bulk Set / Add update modes.
- Bulk import: [[apps-csv-import]] (CSV bulk-creates Parameters + Options + Variants); [[apps-xml-import]] / [[apps-xml-sync]] (XML feeds carry per-product Parameter / Option data and auto-create Variants).
- [[products-variants-options]] — does NOT generate per-product matrices; only manages catalogue dictionary entries.

### The 3-Parameter cap (v1 / v2 / v3 slots)

A product can attach 0, 1, 2, or 3 Parameters (the `v1` / `v2` / `v3` dimension slots). Selecting a 4th in the product editor's Parameter picker is rejected — there is no `v4`. This permanent ceiling is the most-asked "why can't I add more variants" question in support tickets.

The merchant must pick the 3 most-important dimensions to vary on. Others go to [[products-property|Properties]] (descriptive, no SKU split), get baked into the product name, or become separate products. Apparel typically uses 2 (Size + Colour); electronics 1 (Storage / Power / Memory); furniture 1 (Colour / Material). [[variants-option|Option]] renames propagate to the matrix automatically.

### Cartesian expansion — worst-case matrix sizes

The matrix expands by the cartesian product of the selected [[variants-option|Options]] across attached Parameters:

| Chosen | Variant rows |
|--------|---------------|
| 1 Parameter × 10 Options | 10 |
| 2 Parameters (Size 4 × Colour 5) | 20 |
| 3 Parameters (Size 4 × Colour 5 × Material 3) | 60 |
| 3 Parameters (Size 10 × Colour 10 × Material 10) | 1,000 — **rejected by the 500-Variant cap** |

### Hard limits enforced at product-save validation

| Limit | Value | Error message |
|-------|-------|---------------|
| Max Variants per product | 500 | "max allowed 500 exceeded" |
| Max Variant `quantity` | 50,000,000 | "quantity max 50000000" |
| Parameter name length | 1–191 chars | "parameter must be between 1 and 191 characters long" |
| Per-Variant `price` | ≤ 1,000,000,000 (minor units) | (generic validation message) |
| Per-Variant `discount_price` | ≤ 1,000,000,000 (minor units) | (generic validation message) |
| Per-Variant `weight` | 0.01 – 10,000,000 | (generic validation message) |
| Duplicate Parameter names on the same product | rejected | "duplicate parameters" |
| Duplicate Variant combinations on the same product | rejected | "variants must be unique" |

"5 sizes × 10 colours × 10 materials = 500 Variants" is the absolute ceiling for one product. 5×10×11 (550) is rejected — drop Options or split the product.

### `default_variant_id` — lowest price, ties by ID

`default_variant_id` on the parent Product is **not** manually selectable in the admin UI. It's the Variant with the lowest `price` (ties broken by Variant ID — oldest wins), recomputed on every price save, including bulk updates from [[products-inventory]]. Lowering one Variant's price below all siblings promotes it to the default Variant shown on the storefront category card; raising the cheapest can demote it. See [[variants-pricing]].

### `price_from` / `price_to` denormalisation

On every Variant price save the parent Product's `price_from` (min Variant price) and `price_to` (max Variant price) are recomputed. These are the "from / to" range the storefront shows on the category card before the customer picks a Variant. See [[variants-pricing]].

### Variants have no `created_at` / `updated_at`

A Variant has no `created_at` / `updated_at`. The merchant cannot see "when was this Variant added" directly — the parent Product's timestamps and the per-Variant audit / diff log are the only sources. See [[variants-known-issues]].

### `multi_variants` plan gate — hides the "Multi variant" product type

Creating multi-Variant products is plan-gated by the `multi_variants` feature key. On plans without it, the "Multi variant" product type is hidden from the Add product flow entirely — those merchants can only sell single-Variant products. See [[plan-gates]].

### `minimum` order quantity floor — auto-corrected to 1

Every Variant carries a `minimum` field (minimum order quantity per cart line). Setting `minimum = 0` or empty on save is auto-corrected to **1** — the effective floor is 1 unit per Variant. If a Variant's `quantity` is below its `minimum`, the storefront greys out Add-to-cart even though the count is positive; the Inventory screen still shows the in-stock quantity, but the purchase is blocked.

### Unit-of-measure auto-fills

When a Variant has `unit_id` set but no `base_unit_id`, `unit_id` is auto-copied into `base_unit_id` on save. When `unit_id == base_unit_id` and no `base_unit_value` is set, `base_unit_value` is auto-filled to `1`. Both happen silently on every save, so a merchant who configures only the unit still gets a valid record (typically used for "5 BGN per 100 g" per-unit pricing display).

## Related

- [[variants-model]] — hub (Parameter, Option, pricing, inventory link, known issues).
- [[products-products]] — product editor that hosts the matrix.
- [[products-variants-options]] — the catalogue-wide Parameters / Options dictionary.
- [[products-inventory]] — per-Variant stock-management screen.
- [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] — bulk-create Parameters + Options + Variants.
- [[inventory-tracking]] — per-Variant `quantity` model.
- [[plan-gates]] — `multi_variants` feature key.

## Open Questions

None.
