---
type: concept
nav_path: "Concept → Variants model → Image mapping"
aliases: ["Variant images", "Per-Variant gallery", "Variant image binding", "ImageVariant", "Option swatch vs Variant image", "Снимки на вариант", "Образец на изображение", "Image swatch override", "Image sample icon replaced", "Управление на разновидности images", "swatch shows product photo not icon"]
tags: [catalog, variants, images, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-16
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Parameter, Option, matrix generation, pricing, inventory link, known issues).

# Variants model — Image mapping

## Definition

CloudCart's variant image model has **three** distinct image layers that the storefront resolves in a fallback chain:

1. **Product-level image set** — the gallery uploaded on the product editor's Images section; applies to the whole product (every Variant) when no more-specific image exists.
2. **Option-level dictionary image** — the catalogue-wide swatch / image attached to an [[variants-option|Option]] (e.g., the Red colour swatch). One image used everywhere the Option appears across the catalogue.
3. **Per-Variant gallery** — images uploaded directly on a Variant row (stored as `ImageVariant` records linked by `parent_id` to the Variant). The Variant has two relationships:
   - `image` — the single primary image for the Variant; renders on storefront thumbnails when the Variant is selected.
   - `images` — the full gallery of images attached to that specific Variant.

Resolution chain on the storefront when the customer picks a Variant: the variant-image mapping resolves to the **Variant's `images`** if present, otherwise falls back to the product-level image set. The Option-level swatch is used in the Parameter picker (e.g., the Colour-swatch tile that the customer clicks), NOT as the main product image.

> **Earlier wiki incorrectly claimed "Variants don't have their own images."** This is verified false — Variants DO have their own gallery via the `image` + `images` relationships. The current page reflects the verified backend behaviour.

## Scope

Covered here:

- The 3-layer image model (Product / Option / Variant) and the fallback chain.
- The two Variant image relationships (`image` primary + `images` gallery).
- Auto-cleanup of `ImageVariant` records on Variant delete.
- Where the merchant uploads each image type.
- Storefront resolution when the customer picks a Variant.
- Which image an **Image-sample** swatch tile shows, and why it differs between the product page (per-Variant image wins) and catalogue surfaces (filters/listings keep the global icon).

Not covered here:

- Option swatch upload mechanics (Image sample / Colour sample / 2D schema types) — see [[variants-option]].
- Per-Variant SKU + price + quantity — see [[variants-matrix-generation]] + [[variants-pricing]] + [[variants-inventory-link]].
- Storefront variant-picker UX patterns (which picker shows first, dependency between pickers) — those are storefront-theme behaviours, not catalog-data behaviours.
- Image hosting / CDN / resizing — out of scope.

## Contrasts

- **Option image vs Variant image** — an Option image (typically a Colour swatch or fabric tile) is a **catalogue-level dictionary image** — one image used everywhere the Option appears. A Variant image is **product-specific** — the "Red T-shirt in this product's photoshoot" photo set, attached directly to the Variant record. Both can coexist: the Colour Option has a swatch (renders in the picker tile), and the "Red, M" Variant has its own gallery (renders when the customer picks Red + M).
- **Variant `image` vs Variant `images`** — `image` is the single primary image (the thumbnail); `images` is the full gallery (the carousel). The product editor's Variants section lets the merchant upload both per Variant row.
- **Product-level image vs Variant-level image** — product-level images apply to every Variant by default; Variant-level images override for that specific Variant. A T-shirt with 5 Colours can have just the 5 colour swatches at the Option level + 5 product-level photos of one default colour; OR it can have a full per-Variant gallery for each colour. Both patterns are common.

## Where it applies

Per-Variant images surface on:

- The Variants section of the product editor on [[products-products]] — each Variant row has an upload area for the per-Variant gallery.
- The storefront product detail page — when the customer picks a Variant, the main product image switches to the Variant's primary `image` if present (otherwise stays on the product-level image).
- The storefront category card — `default_variant_id`'s primary image renders if present (see [[variants-pricing]] for default Variant computation).
- The [[variant|Variant]] entity — exposes the `image` and `images` relationships.

### The 3-layer fallback chain

Storefront resolution when rendering an image for a specific Variant:

1. **Variant-level primary `image`** → if set, use it.
2. Otherwise → use the **product-level image set**.

The **Option-level swatch** is rendered separately in the Parameter picker tile (e.g., the Red colour-swatch the customer clicks). It is NOT used as a fallback for the main product image — the swatch is only the picker's visual cue.

This fallback chain means the merchant has multiple valid patterns:

- **Minimal effort**: upload only product-level images; let every Variant share them. Best for products where colour differences aren't visually meaningful (e.g., size-only variations).
- **Swatch-only**: upload product-level images + Option-level swatches (Colour, Material). The customer sees the swatch in the picker but the main image stays the same.
- **Full per-Variant**: upload a dedicated gallery per Variant. Each Variant's customer sees a uniquely styled photoshoot.

### Variant deletion auto-cleanup

When a Variant is deleted, the cascade removes the linked `ImageVariant` records — the per-Variant gallery is cleaned up automatically. The product-level image set is untouched; the Option-level swatch is untouched (it lives on the [[variants-option|Option]], shared across many products).

The cascade is driven by the Variant's `deleting` boot callback — when the Variant is removed (manually by the merchant, or as a side-effect of deleting the parent product), the linked `ImageVariant` rows are removed too.

### What the merchant sees in the admin

The product editor's Variants section presents per-Variant rows. For each Variant row, the merchant can:

- Upload a primary `image` — typically the thumbnail.
- Upload additional images into the gallery (`images`).
- Reorder the gallery via drag-and-drop.

The catalogue-wide Option-level swatches are managed separately on the per-Parameter Values sub-page of [[products-variants-options]] — see [[variants-option]].

The product-level image set is uploaded on the main Images section of the product editor — outside the Variants section, applies to every Variant.

### How the storefront variant-picker uses these images

Clicking a picker tile selects the Option; if that completes a full Variant (all required Parameters chosen), the main product image switches to the **Variant-level** primary `image` if present, otherwise stays on the product-level image. The swatch the customer clicks and the main product photo that updates after the click can therefore be different images — the swatch identifies the choice, the main photo shows the styled product.

**Which image the swatch tile itself shows depends on the Parameter type and the context** — and for the **Image sample** (`image`) type this differs between the product page and catalogue-level surfaces:

- **Colour sample (`color`)** — the tile always shows the Option's hex colour (the catalogue dictionary value). It is **never** overridden per product.
- **Image sample (`image`), on the product detail page** — the tile resolves its image in this priority order:
  1. the **per-Variant gallery image** — the product-gallery image linked to that value in **Управление на разновидности** ([[products-products]] → Variants) — used **first** whenever the Variant has its own image;
  2. otherwise the **Option-level swatch icon** — the icon uploaded once for that value, catalogue-wide;
  3. otherwise a no-image placeholder.

  So when a merchant links a product-gallery image to an Image-sample value in Управление на разновидности, that gallery image **replaces the uploaded value icon in the product page's picker tile** — by design, because the per-product Variant image has priority over the catalogue-wide icon.
- **Image sample (`image`), on catalogue-level surfaces** — the **category-page variant filter** and the picker's internal value→image map both use the **Option-level swatch icon only**, never the per-product Variant image. This is why the *same* value can show the linked product photo in the product-page picker yet still show the originally uploaded icon in a category filter.

This product-page-vs-catalogue split is intentional: per-product Variant images win where the customer is looking at one product, while the shared icon stays consistent across the catalogue (filters, listings) where no single product is in scope.

## Related

- [[variants-model]] — hub.
- [[variants-option]] — Option-level swatch / image (catalogue dictionary).
- [[variants-matrix-generation]] — per-product Variant rows where per-Variant images are uploaded.
- [[variants-known-issues]] — earlier wiki claim "Variants don't have images" was incorrect.
- [[variant]] — Variant entity exposing the `image` + `images` relationships.
- [[product]] — Product entity with its own image set (the fallback layer).
- [[products-products]] — product editor; the Variants section is where per-Variant uploads happen.
- [[products-variants-options]] — catalogue-wide Option swatch management.

## Open Questions

None.
