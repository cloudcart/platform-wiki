---
type: feature
nav_path: "Products → Variants → Option types"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variant types", "Variant display types", "Variant visualisation types", "Option types", "Variant parameter types", "Select option", "Radio button", "Image sample", "Color sample", "Colour sample", "2D schema", "Numeric alpha", "Типове варианти", "Видове разновидности", "Видове параметри", "Визуализация на разновидности", "Радио бутони", "Селект меню", "Цветни мостри", "Снимки на разновидности"]
tags: [products, variants, option-types, validation, storefront-rendering]
plan_gates: ["multi_variants"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Variants — the 6 option types

> Part of [[products-variants-options]]. See the hub for the other aspects.

## Purpose

Canonical reference for the **6 variant parameter types** CloudCart supports. Picking the type does **three things at once**: it decides what the customer sees on the storefront picker, what fields the per-Value form shows, and the validation on those fields (e.g., `numeric_alpha` rejects pure-digit or pure-letter Value names). The full per-type breakdown is in the reference table below.

Type is chosen ONCE when the Parameter is created in the wizard ([[products-variants-wizard]]) and is **locked after creation** — see Business rules. The merchant cannot switch a "Color sample" Parameter to "Radio button" later without recreating it.

## Where to find it

The type radio sits on **Products → Variants → + Add variant → Step 1 → Option type**. The same Type field appears on the Edit modal (but the server rejects changes once Variants reference the Parameter). The chosen type then controls, downstream: the Value-input form on the per-Parameter [[products-variants-values|Values]] sub-page; the picker every product using this Parameter renders on its [[product-detail|storefront detail page]]; and the category-page filter rendering when "Show in listing" is on (see [[plan-gates]] — `variants.listing`).

## What the merchant can do here

- Pick exactly one of 6 types when creating the parameter (Step 1 of [[products-variants-wizard]]).
- Add Values of the chosen type via Step 2 of the wizard or the per-parameter [[products-variants-values|Values]] sub-page — the form fields adapt to the type.
- Nothing else to configure: the type drives the storefront picker automatically. There is no per-product picker setting — every product using this Parameter shows the same picker to the customer.

## Settings & fields

### The 6 types — full reference table

Each row lists the type key (chosen once in Step 1), the per-Value form fields, the storefront picker the customer sees, and the best use case.

| # | Type label (BG / EN) | Type key | Admin Value form fields | Storefront picker | Best use case |
|---|---|---|---|---|---|
| 1 | **Селект меню** / **Select option** | `select` | Name only (max 150 chars) | Dropdown; customer picks one | Many values (10+) — country, language, voltage |
| 2 | **Радио бутони** / **Radio button** | `radio` | Name only (max 150 chars) | Row of radio buttons, all visible; one click | 2–5 options shown all at once |
| 3 | **Снимки** / **Image sample** | `image` | Name + **Image upload per Value** (jpg / jpeg / png / bmp / webp; counts against the store's [[settings-files|storage quota]]). On edit, a **Delete image** link appears | Row of clickable image tiles; Values with no image show just the name | Patterns, fabrics, designs, prints |
| 4 | **Цветни мостри** / **Color sample** | `color` | Name + **Hex colour picker per Value** (default `#FFFFFF`, pattern `#?[a-f0-9]{3,6}`) | Row of clickable colour swatches filled with the Value's hex | Colour pickers (Red / Blue / Black) |
| 5 | **2D схема** / **2D schema** | `2d` | Name + 2D coordinate data (X axis + Y axis) | 2D table — X axis as columns, Y axis as rows; each cell a clickable radio | Clothing measurements, anything 2-axis |
| 6 | **Цифрово-буквена** / **Numeric alpha** | `numeric_alpha` | Name only — **must match `<digits><letters>` pattern** (e.g., `36A`, `40B`, `5XL`). Pure-digit (`36`) or pure-letter (`XL`) rejected at save with *"Размерът трябва да съдържа цифра и буква"* | 2D table identical to `2d`; each cell is one concatenated size (cell X=`A`, Y=`36` submits `36A`) | Sizes with width-and-length axes (`36A`, `36B`, `40A`, `40B`); enables the smart numeric-then-alpha sort |

Both the per-Value form (**+ Add variant value** on the [[products-variants-values|Values]] sub-page) and the storefront picker are driven by the parent Parameter's type — the merchant never configures them separately. The same modal serves Create + Edit, so a `select`-type Parameter simply has no image or colour field. On the storefront, every picker shares the same JS hook `js-parameter-choose` (class `parameter-value-js`), so one script listens to all six shapes; only the clickable shape inside differs.

## Business rules

### Type is locked once products use the Parameter

The Parameter's type cannot be changed after any Variant references it. The Edit modal ([[products-variants-wizard]]) still shows the Type radio, but the change is rejected on save. To switch types, the merchant must delete the Parameter and recreate it — which is blocked while products still use it (see [[variants-parameter]]). In practice: **pick the type carefully on first creation**. Switching from `select` to `color` on a Parameter attached to 50 products is a multi-hour migration (recreate Parameter → re-add Values → re-edit every product → delete the old one).

### Cross-Parameter limits on the same product

Within a single product's Variant matrix (max 3 Parameters per product — see [[variants-matrix-generation]]):

- **At most 1 `numeric_alpha` Parameter per product.** Two on one product (e.g., a shoe with both length and width on alphanumeric axes) fails on save.
- **At most 2 `2d` Parameters per product.** A third is rejected.
- **If `numeric_alpha` is present, at most 1 `2d` Parameter** on the same product.

These limits do **not** restrict store-wide Parameter creation — the merchant can have many numeric-alpha Parameters in their catalogue, but only one can be applied per product. The 3-Parameter-per-product hard cap still applies on top.

### Numeric-alpha smart sort

The strict `<digits><letters>` pattern on `numeric_alpha` Values enables CloudCart's smart sort across mixed sizes — Values sort by the leading numeric part first, then the alpha suffix. So `36A` < `36B` < `40A` < `40B` regardless of insertion order, both in the admin matrix and on the storefront picker.

### Color hex without `#` is accepted

The hex picker emits `#`-prefixed values, but the validation pattern treats the prefix as optional. Three-digit shorthand (`#0F0`) and six-digit (`#FF0000`) are both valid; the swatch renders the value verbatim.

### Image-sample storage quota

Image uploads on Image-sample Value rows count against the store's overall [[settings-files|storage quota]]. A merchant near quota who tries to upload more sees a quota-exceeded error before the Value saves.

### Type ≠ Variant image gallery

A `color` or `image` Parameter type drives the **Option-level swatch** the customer clicks in the picker — a catalogue-level dictionary image shared across every product using this Option. This is separate from the **per-Variant gallery** a merchant uploads on the product editor's Variants section to override the main photo when a Variant is selected. See [[variants-image-mapping]] for the 3-layer image model (Product → Option → Variant fallback chain) — confusing these two layers is a common merchant mistake.

One consequence catches merchants out: for the **`image` type specifically**, on the **product detail page** the picker tile shows the **per-Variant gallery image** when one is linked to that value in Управление на разновидности — it *replaces* the uploaded value icon there (by design; the per-product image has priority). The original icon still shows on catalogue-level surfaces (category-page variant filter, listings). The `color` type is never overridden this way. The full priority order is on [[variants-image-mapping]].

## Related

- [[products-variants-options]] — hub.
- [[products-variants-wizard]] — where the type is chosen (Step 1 radio).
- [[products-variants-values]] — the per-Parameter Values modal that switches fields per type.
- [[products-variants-data-model]] — the 3-Parameters-per-product cap + type-locked-after-use rule.
- [[variants-parameter]] — Parameter concept; the type is one of its attributes.
- [[variants-option]] — Option concept; Value fields adapt to the parent type.
- [[variants-image-mapping]] — 3-layer image chain; Option swatch (type-driven) vs Variant gallery (per-product).
- [[product-detail]] — storefront page where the picker renders.
- [[settings-files]] — Image-sample Value images count against this storage quota.
- [[products-property]] — sister system for descriptive specs; own type taxonomy (not Variant types).

## Open questions

None.
