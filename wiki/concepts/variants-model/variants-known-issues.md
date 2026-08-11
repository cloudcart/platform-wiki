---
type: concept
nav_path: "Concept → Variants model → Known issues"
aliases: ["Variants known issues", "Variants by-design quirks", "Variants gotchas", "Locked display type", "Irreversible merge", "Известни проблеми с варианти"]
tags: [catalog, variants, parameters, options, concepts, known-issues]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Parameter, Option, matrix generation, pricing, inventory link, image mapping).

# Variants model — Known issues

## Definition

This page catalogues the **by-design** quirks of the Variants model that surface as merchant support tickets — plus past wiki misconceptions now corrected against verified backend behaviour. None are bugs; they follow from the data model and product decisions. Documenting them helps support route tickets ("by design" vs "let me investigate") and helps merchants plan around the constraints up front.

## Scope

Covered here:

- By-design constraints that drive tickets (3-Parameter cap, 500-Variant cap, locked display type, irreversible merge, no timestamps, no per-Variant default picker, deletion guards, per-product tracking, catalogue-level Options).
- Wiki-record corrections — claims previously documented incorrectly, now verified.
- The merchant workaround for each constraint.

Not covered: open backend bugs (none at this revision); storefront-theme variant-picker UX; inventory-side known issues — see [[inventory-tracking]].

## Contrasts

- **By-design vs bug** — every item here is intentional, even when it surprises merchants. It becomes a bug only if backend behaviour diverges from documented intent.
- **Constraint vs feature** — the caps (3-Parameter, 500-Variant) protect against catalogue explosion and storefront performance; locked display type and irreversible merge reflect schema decisions that are expensive to reverse.

## Where it applies

The constraints below surface on the product editor on [[products-products]] (most caps fire at save validation), the catalogue-wide [[products-variants-options]] screen (Parameter deletion, Option merge), and bulk imports via [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] (validation rejects oversized matrices at import).

### By-design constraint 1 — Hard cap of 3 Parameters per product

A product can attach 0, 1, 2, or 3 Parameters; picking a 4th is rejected.

**Workaround:** keep the 3 most-important SKU-splitting dimensions, then either move the 4th to a [[products-property|Property]] (descriptive, no SKU split, supports category-page filtering), bake it into the product name ("Red Leather Loafer — Wide"), or split into separate products ("Regular Fit" vs "Wide Fit").

Most-asked "why can't I add more variants" ticket. See [[variants-matrix-generation]].

### By-design constraint 2 — Hard cap of 500 Variants per product

The combinations of selected [[variants-option|Options]] across the 3 Parameters cannot exceed 500. Error: *"max allowed 500 exceeded"*.

**Workaround:** reduce per-Parameter Option counts (drop sizes that don't sell), or split into separate products by one dimension instead of using it as a Parameter.

See [[variants-matrix-generation]] for the full validation list (`quantity` max 50,000,000; per-Variant `price` max 1,000,000,000 minor units).

### By-design constraint 3 — Parameter display type locked after creation

Once a [[variants-parameter|Parameter]] is created with a display type (Select / Radio / Image / Colour / 2D / Numeric alpha), the type cannot be changed. To switch (e.g., Select → Colour swatches):

1. Create a new Parameter with the desired type.
2. Re-add every Option with the new type's required fields (hex codes for Colour, uploads for Image).
3. For each product on the old Parameter: detach it, attach the new one, re-set the Option on every Variant row.
4. Delete the old Parameter once no product uses it.

For 50 products this is a multi-hour migration — pick the type carefully up front. See [[variants-parameter]].

### By-design constraint 4 — Merge values is irreversible

Consolidating [[variants-option|Options]] ("Red", "Dark red", "Burgundy" → "Red") reassigns every Variant tagged with the merged Options to the survivor; the merged Options cease to exist.

Once committed, re-creating them as new Options does **not** auto-re-tag the Variants — they stay on "Red". The merchant must manually redistribute them across every affected product. There is no undo. See [[variants-option]].

### By-design constraint 5 — Variants have no created/updated timestamps

A Variant has no `created_at` / `updated_at` field, so the merchant cannot see "when was this Variant added" from the Variant alone. The parent product's timestamps and the audit log are the only sources.

**Workaround:** every Variant save records its changed fields into the audit log (new Variants record their initial state). Support can read that history — there is no merchant-facing per-Variant history UI.

### By-design constraint 6 — Merchant cannot pick the default Variant manually

The default Variant shown on the storefront category card (and in the price box before the customer picks) is auto-computed as the Variant with the lowest `price`, ties broken by oldest / first-created, recomputed on every price save.

**Workaround:** to force a specific Variant as default, price it lower than all siblings. There is no UI to manually pin a different Variant. See [[variants-pricing]].

### By-design constraint 7 — Deletion guard on in-use Parameters / Options

A [[variants-parameter|Parameter]] cannot be deleted while any product references it (*"This parameter is used by products. Remove the products first."*). An [[variants-option|Option]] cannot be deleted while any Variant references it. Bulk-delete with mixed used / unused entries deletes only the unused; used entries surface in the error.

**Workaround:** detach the Parameter / Option from every product or Variant first, or delete the affected products. The guard prevents accidental data loss.

### By-design constraint 8 — `tracking` master switch is per-Product, not per-Variant

Although stock lives on the Variant, the `tracking` switch sits on the parent Product. A product with 12 Variants either tracks all 12 (each `quantity` honoured) or none (storefront treats every Variant as in-stock). The merchant cannot have "track Red but not Blue" on one product.

**Workaround:** for per-Variant tracking control, split into separate products. See [[variants-inventory-link]] + [[inventory-variant-model]].

### By-design constraint 9 — Per-product, never-reused Options not supported

[[variants-option|Options]] are always catalogue-level. The merchant cannot create a "special edition only on this hoodie" colour that exists on just one product — it has to be added to the global Colour Parameter. To keep it off other products' pickers, don't add a Variant row using it there.

### Wiki-record correction 1 — Variants DO have their own images

Earlier wiki claim: *"Variants don't have their own images."* Verified false. A Variant has both a single primary image (the storefront thumbnail when selected) and a full gallery, deleted with the Variant. See [[variants-image-mapping]] for the 3-layer image model (Product / Option / Variant fallback chain).

### Wiki-record correction 2 — `minimum` defaults to 1, not 0

Earlier wiki claim: *"`minimum` can be set to 0 to disable the order-quantity floor."* Verified false. Setting `minimum` to 0 or empty on save is auto-corrected to **1**; there is no zero-minimum state — the floor is 1 unit per Variant. If a Variant's `quantity` is below its `minimum`, the storefront greys out Add-to-cart even when the count is positive. See [[variants-matrix-generation]].

### Wiki-record correction 3 — `continue_selling` requires `tracking = yes`

Saving `continue_selling = yes` while `tracking = no` is rejected (`cannot_continue_selling_untracked_product`). The per-product `threshold` likewise cannot be set when `tracking = no` (`cannot_have_threshold_if_not_tracked`), and `threshold = 0` is rejected (`threshold_invalid_value`).

To disable low-stock alerts, the merchant leaves the threshold blank (falls back to store-wide). See [[inventory-variant-model]].

## Related

- [[variants-model]] — hub.
- [[variants-parameter]] — locked display type, deletion guard.
- [[variants-option]] — irreversible merge, deletion guard, no per-product Options.
- [[variants-matrix-generation]] — 3-Parameter cap, 500-Variant cap, no `created_at` / `updated_at`.
- [[variants-pricing]] — `default_variant_id` not manually picked.
- [[variants-inventory-link]] — `tracking` is per-product, not per-Variant.
- [[variants-image-mapping]] — Variants DO have their own images (correction).
- [[inventory-tracking]] — inventory model with related constraints.
- [[products-property]] — alternative for descriptive non-SKU-splitting dimensions.

## Open Questions

None.
