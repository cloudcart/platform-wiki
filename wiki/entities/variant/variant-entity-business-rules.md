---
type: entity
nav_path: "Entity → Variant → Business rules"
aliases: ["Variant business rules", "Variant invariants", "Variant save rules", "Variant SKU uniqueness", "Default variant pointer", "Cascade rename of v1/v2/v3", "Variant cascade cleanup"]
tags: [entity, catalog, variants, business-rules]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[variant]]. See the hub for the other aspects (attributes, lifecycle, relationships, side effects and API).

# Variant — Business rules

## Identity

The catalogue of invariants and save-time rules the [[variant|Variant]] record obeys — SKU uniqueness, the 3-parameter hard cap, the one-default-Variant rule, the cascade rename of denormalised labels (`v1` / `v2` / `v3`), the `minimum` floor, the unit-of-measure auto-defaults, the cascade cleanup on delete, and the historical-order-survives rule. The rules the AI Assistant cites for *"Why did my CSV import skip those rows?"*, *"Why did the back-in-stock email fire?"*, *"What happens to old orders if I delete this colour option?"*.

## Aliases

- **Variant invariants** / **Variant save rules** — the catalogue below.

## Key Attributes

### SKU and barcode live on the Variant; the Variant is THE sellable unit

For every product — even simple, single-variant products — SKU and barcode are stored on the underlying Variant. The "Product SKU" the merchant types on the Edit page is written to the single backing Variant; multi-variant products fill each SKU separately on the Variants tab. Cart line items, order line items, `fixed` [[discount|Discounts]], back-in-stock waitlists, inventory imports, and stock alerts all reference a specific Variant ID.

### Hard caps: 3 Parameter Options per Variant, 500 Variants per Product

A Variant references at most 3 Parameter Options (via `p1` / `p2` / `p3`) because a Product allows at most 3 parameters — there is no merchant setting to lift this. The Variant matrix size = product of option counts (10 colors × 5 sizes × 3 materials = 150 Variants). Total Variants per product is capped at **500** at product-save validation. See [[variants-matrix-generation]].

### One default Variant per Product

Exactly one Variant per Product is the default. The Product's `default_variant_id` column stores the pointer (the flag is NOT on the Variant row); the referenced Variant is pre-selected when the customer lands on the product page. Picking a new default rewrites the Product, not the Variants.

### Denormalised labels (`v1` / `v2` / `v3`) cascade-rename on Option rename

The Variant caches `v1`, `v2`, `v3` text for the up-to-3 parameter options so apps and exports can read Variant data without joining to the Parameter Option table. When the merchant renames a Parameter Option (e.g., "Red" → "Crimson"), the platform sweeps every Variant referencing that option ID and updates the matching `v1` / `v2` / `v3` in-place — **immediate and store-wide**. Historical orders snapshot the value at purchase time, so they keep the old label; live catalog and in-progress carts show the new label.

### Quantity per Variant; Product `quantity` is a SUM; no per-Variant timestamps

The Product-list quantity column shows the SUM of `quantity` across the Product's Variants. Editing quantity at the Product level is disabled for multi-variant products — the merchant must edit each Variant's quantity individually (or via bulk inventory import) — see [[inventory-variant-model]]. Variants do NOT carry their own `created_at` / `updated_at`; change tracking happens at the Product level (the Product's `date_modified` ticks on every Variant save).

### Price range computed from Variant prices; Variant images are optional fallbacks

The Product's `price_from` and `price_to` are min/max `price` across its active Variants — the storefront card shows the flat price if all share one, "from X to Y" if they differ. A Variant may have its own image; if not, the gallery uses the Product's primary image. When the customer picks a Variant with its own image, the gallery swaps. See [[variants-image-mapping]] for the 3-layer fallback chain.

### SKU uniqueness store-wide — admin returns 422, bulk CSV silently skips

SKU uniqueness is validated store-wide on save. The inline-edit save returns a validation error with the SKU field highlighted (*"This SKU is already in use"* or the localized equivalent). The **bulk CSV import path logs the duplicate row and SKIPS** it rather than failing the whole import — intentional, since bulk imports often contain a few duplicates.

### `compare_at_price` and `cost_price` are per-Variant

`compare_at_price` / `msrp` are editable per-Variant on the **Variants tab**; CSV import accepts a per-Variant `compare_at_price` column. Older admin layouts only expose the Product-level field — use the Variants tab. `cost_price` is settable via CSV import (when the column is included) and via the JSON-API v2 / GraphQL API; it surfaces **only** on admin reports (margin analytics, accounting) — never on the storefront. There is no product-catalogue CSV export screen, so `cost_price` cannot be pulled out that way; for a catalogue dump use an [[apps-xml-feed|XML product feed]] or the [[apps-google-sheets|Google Sheets app]].

### Restock-notification trigger; deleting a Parameter Option does NOT block

The back-in-stock email fires when a Variant's stock transitions from `<= 0` to `> 0` — NOT only when the merchant explicitly clears an out-of-stock label. The waitlist is queried, emails dispatched, and rows cleared in one batch ([[products-missing-product]]). Deleting a Parameter Option does NOT block when historical orders reference its Variants. The Variant rows are removed, but order line items' `variant_id` is set to NULL via `ON DELETE SET NULL`. The order line retains its **snapshotted SKU and label text** so the order remains readable ([[variant-entity-lifecycle]]).

### Discount type `fixed` targets a single Variant

The `fixed` discount type ([[marketing-discounts-fixed]]) overrides the price of one specific Variant — picking the Product alone is NOT enough; the merchant must pick which Variant gets the override. Other discount types (`flat`, `percent`, `shipping`, `quantity`, `countdown`) target the Product or category and apply uniformly across Variants.

### Save-time defaults (admin namespace only)

When the Variant is saved from the **admin namespace** (NOT from storefront / API contexts), the `saving` hook normalizes three fields:

- **`minimum` floor of 1** — if `minimum <= 0`, it is reset to `1`. Clamps out-of-bounds CSV imports / API payloads to a safe default.
- **`base_unit_id` defaults to `unit_id`** — copied when the merchant sets `unit_id` but never set `base_unit_id`.
- **`base_unit_value` defaults to `1`** — filled when `unit_id == base_unit_id` and `base_unit_value` is empty. Guarantees the price-per-base-unit calculation always has a non-null value at runtime.

### Cascade cleanup on delete

When a Variant is deleted (typically as part of a Product cascade — see [[product]] — or via the Parameter Option removal flow), the model's `deleting` hook removes two child tables BEFORE the Variant row goes: **Variant images** (every `ImageVariant` row hard-deleted; their image-cache directories wiped through the image trait's boot hook) and **external-meta-data rows** (carrier-specific overrides, ERP barcodes, app-installed fields). Variant-level snapshots already copied onto historical Order line items are NOT touched — they retain SKU + denormalized label text per the *"Deleting a Parameter Option does NOT block"* rule above.

## Where it appears

- [[products-variants-options]] — Parameter / Option management; option rename triggers the `v1` / `v2` / `v3` cascade.
- [[products-products]] — Variants tab; per-Variant `compare_at_price`, default-Variant picker, SKU edits.
- [[products-inventory]] — bulk SKU / quantity edits; uniqueness errors surface here.
- [[apps-csv-import]] — CSV import; silent-skip-duplicates rule applies.
- [[marketing-discounts-fixed]] — `fixed` discount picker; one Variant per discount.

## Related

- [[variant]] — hub.
- [[product]] — parent record; carries `default_variant_id`, `price_from` / `price_to`, the `tracking` / `continue_selling` / `threshold` switches.
- [[product-option]] — Parameter Option; rename / delete cascades through Variants.
- [[order]] — order line items hold snapshots that survive Variant delete.
- [[discount]] — `fixed` discount type targets one Variant.
- [[variants-matrix-generation]] — the 3-parameter / 500-Variant caps.
- [[variants-image-mapping]] — Variant image fallback chain.
- [[variant-entity-side-effects-and-api]] — JSON-API behaviour vs admin behaviour (clamping, uniqueness).

## Open Questions

None.
