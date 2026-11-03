---
type: concept
nav_path: "Concept → Variants model → Option"
aliases: ["Variant Option", "Parameter Option", "Option value", "Option entity", "Merge options", "Option swatch", "Опция", "Стойност на параметър"]
tags: [catalog, variants, parameters, options, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Parameter, matrix generation, pricing, inventory link, image mapping, known issues).

# Variants model — Option

## Definition

An **Option** is a **value** belonging to exactly one [[variants-parameter|Parameter]]. "Red", "Blue", "Green" are Options of the Colour Parameter. "S", "M", "L", "XL" are Options of the Size Parameter. Options are catalogue-level dictionary entries — store-wide, reusable across every product that attaches the parent Parameter.

Options have **NO SKU, NO stock, NO price**. They carry only the data needed to render the storefront picker (name, image/colour, sort order). The sellable data (SKU, quantity, price, weight) lives on the per-product [[variant|Variant]] rows that reference the Option — see [[variants-matrix-generation]].

Options are managed from the per-Parameter Values sub-page of [[products-variants-options]] (drill into the Values count column on the Parameters list).

## Scope

Covered here:

- Option fields (name, image / colour / 2D coords, sort order, Active / `visible`).
- The **Merge values** action — irreversible consolidation.
- Cascade renames — Option name changes propagate to every Variant's `v1` / `v2` / `v3` denormalised label catalogue-wide.
- The deletion guard — analogous to Parameter deletion.
- Why Options carry no SKU / no stock / no price.

Not covered here:

- The parent Parameter — see [[variants-parameter]].
- How Options combine into per-product Variant rows — see [[variants-matrix-generation]].
- Per-Variant per-Option image binding — see [[variants-image-mapping]].
- Per-Variant pricing — see [[variants-pricing]].

## Contrasts

- **Option vs Variant** — an Option is a catalogue-level value ("Red"); a [[variant|Variant]] is a product-specific combination ("Red T-shirt size M") carrying the SKU + quantity + price. Multiple Variants across multiple products can reference the same Option.
- **Option Active OFF vs deletion** — Active OFF (`visible = no`) hides the Option from storefront pickers but preserves it on every Variant that already uses it. Deletion is blocked while any Variant references the Option.
- **Option image vs Variant image** — an Option image (e.g., a colour swatch) is a catalogue-level dictionary image — one swatch used everywhere the Option appears. A Variant can also have its own gallery attached directly to the Variant record — that's a different image set. See [[variants-image-mapping]].

## Where it applies

Options surface on:

- The per-Parameter Values sub-page of [[products-variants-options]] — list view with name, image/colour preview, sort order, Active toggle, Merge / Delete actions.
- The storefront product detail page — Options render inside their Parameter's picker (dropdown entries, radio buttons, swatch tiles, image tiles, 2D-schema overlays, alphanumeric size labels).
- The product editor on [[products-products]] — when generating the Variants matrix, the merchant picks which Options of each attached Parameter to include for this specific product. The matrix expands by the cartesian product of selected Options across the attached Parameters (see [[variants-matrix-generation]]).

### Merchant-controlled fields

| Field | Behaviour |
|-------|-----------|
| **Name** | "Red", "Blue", "S", "M", "L", … Renames propagate to every Variant's denormalised `v1` / `v2` / `v3` text label catalogue-wide. |
| **Image** | Upload (Image sample type only). Stored under `parameter/images`. |
| **Colour** | Hex code (Colour sample type only). Shown as a swatch on the storefront. |
| **Width / Height** | Pixel dimensions for the swatch (2D schema and image-type only). Controls the rendered size. |
| **Settings** | JSON blob — type-specific extras (image cropping coordinates, 2D-overlay positioning, etc.). |
| **Sort order** | integer. Drag-reorder on the Values sub-page; controls the order on storefront pickers. |
| **Active** (`visible`) | yes / no. When `no`, the Option is hidden from storefront pickers but Variants that already reference it keep their data. |

The Option field set depends on the parent [[variants-parameter|Parameter]]'s display type — a Select-type Parameter shows only name; a Colour sample type shows name + hex code; an Image sample type shows name + image upload + width/height; a 2D schema type shows the overlay editor. The merchant cannot upload an image to a Select-type Option — the form simply doesn't expose that field. The **full per-type form + validation table** is on [[products-variants-types]] (also documents the storefront DOM each type renders on [[product-detail]]).

### Cascade rename — Option name propagates to every Variant

When the merchant renames an Option (e.g., "Red" → "Crimson"), the platform updates the denormalised `v1`, `v2`, `v3` text labels on every Variant that uses this Option — across every product in the catalogue. The customer-facing label and the admin Variants matrix both reflect the new name on the next page load. The rename is atomic on save; no re-sync needed.

### Merge values — irreversible consolidation

The **Merge values** action on the per-Parameter Values sub-page consolidates two or more Options into a single survivor. Every Variant previously tagged with the merged Options is reassigned to the survivor. The merged Options cease to exist.

**Merge is irreversible.** Re-creating "Dark red" and "Burgundy" as new Options after a merge does NOT re-tag the Variants — those Variants stay on "Red". The merchant has to manually edit every previously-affected product to redistribute the Variants.

Typical use: cleaning up a sloppy colour palette ("Red", "Dark red", "Burgundy", "Wine red" sitting on different products that should be one) — merge once, accept the loss of fine-grained distinction.

### Deletion guard

An Option cannot be deleted while any Variant references it. The error message is analogous to the Parameter deletion guard (see [[variants-parameter]]). To delete, the merchant first detaches every Variant or deletes the affected products.

### Why Options carry no SKU / stock / price

Options describe what's possible, not what's sold. The sellable attributes (SKU, barcode, quantity, price, weight, delivery price, minimum order quantity, unit-of-measure fields) live on the per-product [[variant|Variant]] row that combines specific Options for a specific product. A single Option ("Red") can be referenced by hundreds of Variants across hundreds of products, each with its own SKU and stock count.

This separation lets one Colour palette serve the entire catalogue — adding a "Yellow" Option once on the Colour Parameter's Values sub-page makes Yellow available on every product using Colour. The merchant still has to visit each product to add the Yellow Variant row to sell it; a globally-available Option doesn't create per-product Variants automatically.

### Per-product, never-reused Options — not supported

The merchant cannot create a per-product Option that exists only on one product — Options are always catalogue-level. A "special edition only on this hoodie" colour still has to be added to the global Colour Parameter; to keep it off other products' pickers, simply don't add a Variant row using it on those products.

## Related

- [[variants-model]] — hub.
- [[variants-parameter]] — the parent dimension that contains Options.
- [[products-variants-types]] — 6 type catalogue: which Value fields appear in admin AND how each renders on the storefront detail page.
- [[variants-matrix-generation]] — how Options combine into per-product Variant rows.
- [[variants-image-mapping]] — per-Variant gallery vs Option-level swatch.
- [[products-variants-options]] — the catalogue-wide management screen.
- [[product-detail]] — storefront page where the Options render inside the picker.
- [[products-products]] — the product editor that picks which Options to include in a product's matrix.

## Open Questions

None.
