---
type: entity
nav_path: "Entity → Product → Key attributes"
aliases: ["Product attributes", "Product fields", "Product validation", "Product record fields"]
tags: [entity, catalog, products, attributes, validation]
plan_gates: ["products", "bundles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product]]. See the hub for the other aspects (lifecycle, business rules, relationships, side effects, API).

# Product — Key attributes

## Identity

The full per-field schema for the [[product|Product]] record — every attribute the merchant configures or sees on the product editor, with purpose, allowed values, defaults, and validation. Remember: SKU, barcode, price, quantity, weight, and dimensions live on the [[variant|Variant]], NEVER on the Product — see [[product-entity-business-rules]].

## Aliases

- **Product attributes** / **Product fields** — the per-record field definitions.
- **Validation constraints** — create / edit rules enforced at save time.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| `name` | Merchant-facing product name | Primary identifier — list, edit header, storefront title, search. Capped at **191 characters**; save fails above that. |
| `url_handle` | URL slug | Storefront path `/product/<slug>`. Prefix is HARDCODED — cannot change `/product/` to `/p/`. Renaming generates a 301 redirect. |
| `type` | `simple` / `multiple` / `digital` / `bundle` / `physically` | `simple` = single SKU, no variants. `multiple` = has variant parameters (≥1 of p1/p2/p3). `digital` = downloadable file or membership page. `bundle` = grouped, priced from children. `physically` is a **filter alias**, not a stored type — see [[product-entity-business-rules]]. |
| `active` | yes / no | Master publish flag. When `no`, the product is a **Draft** — invisible to customers (storefront URL returns 404). |
| `draft` | yes / no | Work-in-progress marker. Set with `active=no` when setup is incomplete. |
| `is_hidden` | 0 / 1 | When `1`, **Hidden** — published BUT excluded from category listings, search, and filters; reachable only via direct URL. See [[product-entity-business-rules]] for Hidden vs Draft. |
| `featured` | yes / no | Surfaces on featured-products modules. Optional auto-expiry via `featured_from` interval. |
| `new` | yes / no | The "New" badge. Optional auto-expiry via `new_from`. |
| `publish_date` | datetime, store timezone | When future, treated as not-yet-published (excluded until `publish_date <= now`). |
| `active_to` | datetime, store timezone | Expiry date. When set, storefront excludes the product after `active_to < now`. |
| `tracking` | yes / no | Stock-tracking master switch. When `no`, variants are always in-stock regardless of `quantity`. See [[inventory-variant-model]]. |
| `continue_selling` | yes / no | Allow-oversell flag. When `yes`, buyable after `quantity` reaches 0. Requires `tracking = yes`. |
| `category_id` | FK → [[category]] | Primary category. Required for `active=yes` — cannot publish without one. |
| `vendor_id` | FK → [[vendor]] | At most one vendor / brand per product. |
| `image_id` | FK to primary image | First in the `images` collection drives the storefront thumbnail. |
| `status_id` | FK → [[product-status]] (in-stock) | Custom in-stock status text on storefront (e.g., "Ships tomorrow"). |
| `out_of_stock_id` | FK → [[product-status]] (out-of-stock) | Custom out-of-stock status text + button label (e.g., "Notify me"). |
| `p1`, `p2`, `p3` + `p1_id`, `p2_id`, `p3_id` | Up to 3 variant parameter references | Variant parameters (e.g., Color, Size, Material). Hard cap of **3** per product. See [[products-variants-options]]. |
| `default_variant_id` | FK → [[variant]] | Variant pre-selected on the storefront product page. |
| `price_from`, `price_to` | Computed price range | Min/max across variants. Storefront shows `price_from` for single-variant, `from X to Y` for multi-variant. |
| `price_percent` | Computed discount % | Driven by per-variant discounts. |
| `price_type` | Display mode | Storefront strike-through MSRP layout vs flat price. |
| `individual_price` | yes / no | Bundle-specific. `yes` = bundle price is SUM of children's current prices; `no` = bundle has its own fixed price. |
| `description` | Long-form HTML body | Rich-text — HTML, images (lifted into [[file-asset]] storage on save), Cloudio-AI content. Capped at **250,000 characters**; save fails above that. |
| `short_description` | Short summary HTML | Storefront product-card caption. |
| `description_title` | Section heading on storefront | Optional override of the "Description" section title. |
| `seo_title`, `seo_description` | SEO meta | Used in `<title>` and `<meta name="description">`. Empty falls back to `name` + truncated `description`. |
| `seo_generated_through_spinner` | 0 / 1 | Marks SEO fields from the SEO Spinner app (counts against its plan cap). Frees on soft-delete. |
| `tags` | Product-tag pivot (see [[products-tags]]) | Free-form tags for filtering / search / segmentation. Max **191 characters/tag**, max **100 tags/product**. |
| `digital`, `type_digital` | yes / no, file / page | Whether digital and the delivery mode (downloadable file vs membership page). |
| `shipping` | yes / no | Whether the product needs shipping (no = digital / service). |
| `sale` | yes / no | Legacy "on sale" flag, inactive in save logic. Modern sales use [[discount|Discount]] records only. Merchant never sets or sees it today. |
| `minimum` | Minimum order quantity | Floor below which the storefront blocks add-to-cart. |
| `threshold` | Low-stock alert threshold | When `quantity` drops to / below this, the [[settings-cart]] `product_threshold` admin notification fires. Requires `tracking = yes`; else save fails with *"Cannot have threshold if not tracked"*. |
| `unit_id` | FK to measurement unit | Sold-by unit (piece, kg, m², etc.). Affects price/quantity formatting. |
| `per_row` | Storefront layout | Forces a products-per-row count on the category page. |
| `sort_order` | Manual sort number | Lower = earlier; tie-break is insertion ID. Assign distinct values for deterministic order. |
| `app_import`, `imported`, `xml_import_id`, `xml_import_product_id`, `xml_import_name` | Import provenance | Which importer / sync app created the product. Drives "Imported with" filter on [[products-products]]. |
| `views` | Hit counter | Public product-page views. Read-only. |
| `date_added`, `date_modified` | Timestamps | `date_added` = creation; `date_modified` = last save. |
| `deleted_at` | Soft-delete timestamp | When set, the product awaits hard-purge by the temporary-delete cleanup window (10 days). See [[product-entity-lifecycle]]. |

## Validation caps (server-enforced)

Caps not in the table above: variants — max **500 per product** at save (fails with *"Maximum 500 variants exceeded"*; enforced on admin, API, and CSV-import). A 4th variant parameter injected via API is silently ignored. The `name`, `description`, tag, parameter-count, and `tracking`-required caps appear inline in Notes.

## FK cleanup behaviour

If a referenced record (`default_variant_id`, `image_id`, `category_id`, `vendor_id`, `status_id`, `out_of_stock_id`) is removed, the reference is **silently nulled** — the product survives, falling back to the first variant / next image. No blocking. (verify)

## Temporary-product marker

An auto-created product (e.g., from a cart line before the merchant fills it in) carries an internal `temporary` timestamp. The list shows a clock-icon tooltip *"Temporary product. Created on `<date>`. This product is auto deleted on `<delete_date>`"*, where `delete_date = created_at + 10 days`. Auto-purge runs then unless the merchant edits / publishes first — see [[product-entity-lifecycle]].

## Where it appears

- [[products-products]] — core list + edit screen.
- [[products-editor]] — per-product edit page surfacing these fields.
- [[products-variants-matrix]] — where `p1` / `p2` / `p3` render as the variant matrix.
- [[products-tags]] — tag-pivot management.
- [[products-statuses]] — custom statuses referenced via `status_id` / `out_of_stock_id`.

## Related

- [[digital-products]] — the digital / downloadable product type that uses these flags.
- [[product]] — hub.
- [[variant]] — sellable unit; SKU / barcode / price / quantity live here.
- [[category]] / [[vendor]] / [[product-status]] / [[file-asset]] — referenced via FKs.
- [[products-variants-options]] — parameter / option model behind `p1` / `p2` / `p3`.
- [[product-entity-lifecycle]] — transitions reading `active`, `draft`, `is_hidden`, `publish_date`, `active_to`, `deleted_at`.
- [[product-entity-business-rules]] — Hidden vs Draft, publish-window, bundle-pricing, `physically` filter alias.
- [[product-entity-side-effects-and-api]] — what fires when these fields save.
- [[plan-gates]] — `products` / `bundles` count caps.

## Open Questions

- Confirm the nulling behaviour for every FK listed above against current migrations (verify).
