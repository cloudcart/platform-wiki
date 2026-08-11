---
type: entity
nav_path: "Entity → Variant → Relationships"
aliases: ["Variant relationships", "Variant references", "Variant FK graph", "What references a Variant"]
tags: [entity, catalog, variants, relationships]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[variant]]. See the hub for the other aspects (attributes, lifecycle, business rules, side effects and API).

# Variant — Relationships

## Identity

The full FK / reference graph for the [[variant|Variant]] record — what a Variant belongs to (required parent + 0–3 Parameter Options + optional image), and what references a Variant (Order line items, Cart line items, `fixed` Discounts, back-in-stock waitlist subscribers, smart-collection rule evaluation, search-engine index entries, imports / exports).

The Variant sits at the centre of the **catalogue ↔ orders ↔ imports** triangle. Most platform-wide side-effect chains that touch inventory or money pass through a Variant ID at some point.

## Aliases

- **Variant references** — the inbound FK graph (what references a Variant).
- **Variant FK graph** — the outbound + inbound relationships combined.

## Key Attributes

### Outbound — what a Variant belongs to

- **Belongs to one** [[product|Product]] — **required**. The Product is the descriptive parent; the Variant is the sellable child. A Variant cannot exist without a Product. The relationship is stored as `product_id` FK on the Variant.
- **References 0–3** [[product-option|Parameter Options]] via `p1` / `p2` / `p3` — exactly as many as the Product's defined parameters. Simple products have 0; multi-variant products have 1–3. Each reference is the canonical identity of which "Red" / "M" / "Cotton" this Variant is. The denormalised label cache (`v1` / `v2` / `v3`) mirrors the Option's name text for fast reads — see [[variant-entity-attributes]].
- **Has 0–1** Variant-specific image — `image_id` FK to a [[file-asset]] record. When set, the storefront switches the gallery to this image when the customer picks this Variant. Falls back to the Product's primary image when empty.
- **References 0–1** [[product-status]] for in-stock status (`status_id`) and 0–1 for out-of-stock (`out_of_stock_id`) — per-Variant overrides of the parent Product's status labels. Optional; both fall back to the Product's values.
- **References one** measurement unit via `unit_id` (and `base_unit_id` for sold-by-measure variants) — see [[variant-entity-attributes]].

### Inbound — what references a Variant

- **[[order|Order]] line items** (`OrderProduct.variant_id`) — the order snapshots which Variant was bought, at what price, in what quantity. The line also snapshots the SKU + denormalised labels so the order remains readable even if the Variant is later deleted (FK is `ON DELETE SET NULL` — see [[variant-entity-business-rules]]).
- **Cart line items** — the customer's in-progress selection points to a specific Variant. When the cart converts to an order, the line snapshot is captured at order-creation time.
- **[[discount|Discount]] of type `fixed`** — `fixed` discounts override the price of a SPECIFIC Variant (not the whole Product). One discount = one Variant override. See [[marketing-discounts-fixed]]. Other discount types (`flat`, `percent`, `shipping`, `quantity`, `countdown`) target the Product or category and apply uniformly across Variants.
- **Back-in-stock waitlist subscribers** — see [[products-missing-product]]. The waitlist is per-Variant; when a sold-out Variant restocks, the waitlist for THAT Variant is notified.
- **Smart-collection rule evaluation** — rules that depend on Variant-level attributes (price, SKU pattern) match per-Variant.
- **Search-engine index entries** — the storefront search index includes per-Variant data so SKU search and per-Variant price filtering work.
- **Imports / exports** — the SKU is the join key in [[apps-csv-import]], [[apps-xml-sync]], and the [[apps-microbg]] / [[apps-microinvest]] ERP connectors. The CSV / XML update path joins to the existing Variant by SKU and updates `quantity`, `price`, etc. in place.
- **`ImageVariant` rows** — pivot table linking Variants to the optional secondary images (beyond the primary `image_id`). Cleaned up on Variant delete by the model's `deleting` hook — see [[variant-entity-business-rules]].
- **External-meta-data rows** — integration extension rows (carrier-specific overrides, ERP barcodes, app-installed fields). Cleaned up on Variant delete.

## Cardinality summary

| From → To | Cardinality | Notes |
|-----------|-------------|-------|
| Variant → Product | many-to-one (required) | Variant cannot exist without a Product. |
| Variant → Parameter Option | many-to-many (0–3) | Stored as `p1` / `p2` / `p3` slots, not a pivot table. |
| Variant → File asset (image) | many-to-one (0–1) | Variant-specific gallery image. |
| Variant → Product status | 2 × many-to-one (0–1 each) | `status_id` (in-stock) + `out_of_stock_id` (out-of-stock). |
| Order line item → Variant | many-to-one (0–1) | `variant_id` set NULL on delete; snapshot retained. |
| Cart line item → Variant | many-to-one | Resolved at cart time; snapshot captured at order-creation. |
| `fixed` Discount → Variant | one-to-one | One discount targets one Variant's price. |
| Back-in-stock subscriber → Variant | many-to-one | Per-Variant waitlist row. |

## Where it appears

- [[products-variants-options]] — Parameter / Option management; the source of `p1` / `p2` / `p3` references.
- [[products-products]] — the Product editor's Variants tab; per-Variant relationships edited here (image, status overrides).
- [[orders-details]] — order line items reference Variants.
- [[orders-ordered-products]] — per-Variant order line item view.
- [[marketing-discounts-fixed]] — `fixed` discount type picks a specific Variant.
- [[products-missing-product]] — per-Variant back-in-stock waitlist subscribers.
- [[customers-details-products]] — customer's purchased-Variant history.

## Related

- [[variant]] — hub.
- [[product]] — required parent.
- [[product-option]] — Parameter Option referenced via `p1` / `p2` / `p3`.
- [[order]] — orders contain Variant line items.
- [[discount]] — `fixed` discount type overrides a specific Variant's price.
- [[product-status]] — custom in-stock / out-of-stock status labels.
- [[file-asset]] — Variant-specific image storage.
- [[variants-image-mapping]] — the 3-layer image fallback chain (Product / Option / Variant).
- [[variants-model]] — Parameter / Option / Variant structural model.

## Open Questions

None.
