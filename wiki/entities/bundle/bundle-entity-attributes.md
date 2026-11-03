---
type: entity
nav_path: "Entity → Bundle → Attributes"
aliases: ["Bundle attributes", "Bundle fields", "Bundle key attributes", "Bundle pivot columns", "Bundle product shape"]
tags: [entity, catalog, products, bundles, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[bundle]]. See the hub for the other aspects (relationships, lifecycle, component overrides, stock + activation, app + storefront).

# Bundle — Attributes

## Identity

The merchant-controlled fields on a Bundle and the per-row pivot columns that link the Bundle to its constituents. A Bundle is technically a [[product|Product]] record with `type = 'bundle'`, so it carries every standard product attribute (name, image, price, SEO, categories, vendors, tags, custom fields) PLUS a `bundles_products` pivot table whose rows hold per-constituent fields.

This aspect documents what the merchant sets on the editor and what each pivot column means. The override columns themselves are documented separately in [[bundle-entity-component-overrides]].

## Aliases

- **Bundle fields** / **Bundle attributes** — the per-Bundle inputs.
- **Bundle pivot columns** — the per-constituent row shape inside a Bundle.
- **Bundle products** — the editor's label for the constituent list.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** | Required text | What the customer sees on the storefront and in the cart. |
| **Image** | Required upload | The main visual for the Bundle (storefront thumbnail + hero image on the Bundle page). |
| **Bundle products** | Required multi-select with per-item quantity | The constituent [[product|Products]] that make up this Bundle. Each row has a `product_id` reference + a `qty` (how many of that product the Bundle includes). |
| **Bundled price** | Set on the Bundle parent Product | The price the customer pays for the whole Bundle. Typically less than the sum of the constituent prices; the storefront can also display the per-component sum + the "savings vs individual" calculation. |
| **Description** | Free-text rich content | Explanatory text shown on the Bundle's storefront page. |
| **SEO settings** | Title, description, URL handle | Standard product-page SEO. The URL handle drives the storefront path. |
| **Is active** | Toggle | Master publish state. When OFF, the Bundle is invisible on the storefront and cannot be added to cart. Auto-flipped OFF by the platform when any constituent is deactivated — see [[bundle-entity-lifecycle]]. |
| **Per-component overrides** | Per row in the Bundle products list | Each constituent row supports rich per-item overrides (optional flag, price override, title override, visibility scopes) — see [[bundle-entity-component-overrides]]. |
| **Component variant pinning** | Pivot column tied to the parent product reference | When a constituent product has multiple Variants, the merchant cannot pin the Bundle to a single Variant from the pivot itself — the pivot stores only the parent `product_id`. The Variant chosen at checkout is the customer's selection in the Bundle's storefront layout (or the product's default Variant when the layout hides Variant pickers per `visible_product_details`). |
| **Component sort order** | `sort_order` per pivot row | Lower = earlier in the displayed component list. Determines the order components appear on the Bundle's storefront page, in the cart line breakdown, and in order details. |
| **Per-component qty enabled** | `individual_qty_enabled` toggle + `qty` value per pivot row | When OFF, the constituent contributes its product-level price untouched to the headline-sum calculation. When ON, the Bundle treats `qty` as the multiplier (e.g., "2 cameras + 1 lens" gives `2 × camera_price + 1 × lens_price`). The headline price of the Bundle itself is independent — `qty` only affects stock decrement and the "savings vs individual" display. |

### Inherited Product attributes

Because the Bundle parent is a standard [[product|Product]] record with `type = 'bundle'`, it carries every regular product field on top of the Bundle-specific component list:

- **Categories** — Bundles can be assigned to one or more [[category|Categories]] like any product. They appear in category navigation pages.
- **Vendors** — optional vendor / brand attribution.
- **Tags** — free-form merchandising tags.
- **Custom fields** — any product custom field the merchant has defined.
- **File-asset gallery** — additional images beyond the main image, shown on the Bundle's storefront page.
- **SEO redirects** — when the URL handle changes, the platform writes a redirect from the old path (same behaviour as regular products).
- **Multi-language translations** — name, description, SEO can be translated per language.

The parent Bundle record does NOT carry a `quantity` column of its own — see [[bundle-entity-stock-and-activation]] for the derived-availability rule.

### Pivot-row shape

The `bundles_products` pivot table linking the Bundle to its constituents carries these columns per row:

- `product_id` — the constituent product reference (parent product, not a Variant).
- `qty` — how many units of this constituent the Bundle includes.
- `sort_order` — display order in the component list.
- `individual_qty_enabled` — whether `qty` is treated as a multiplier in the headline-sum calculation.
- The per-row override fields — `optional`, `individual_price_enabled`, `individual_price`, `discount`, `override_title`, `title`, `override_short_description`, `short_description`, `hide_thumb`, `visible_product_details`, `visible_cart`, `visible_order_details`, `price_visible_*`. All of these are catalogued in [[bundle-entity-component-overrides]].

## Where it appears

- [[bundles-list]] — the master list view where the merchant creates, edits, and deletes Bundles.
- [[apps-bundles-settings-new]] — store-wide defaults that apply when per-Bundle overrides are not set.
- [[products-products]] — Bundles also appear in the master product list because they're Products with `type = 'bundle'`.
- [[orders-ordered-products]] — expands a Bundle order line to show the constituent breakdown using the saved pivot data.

## Related

- [[bundle]] — hub.
- [[bundle-entity-component-overrides]] — the per-row override columns in detail.
- [[bundle-entity-stock-and-activation]] — how `qty` drives derived availability and decrement.
- [[product]] — the parent Product entity whose schema the Bundle inherits.
- [[variant]] — constituents with Variants; pivot stores only `product_id`, so Variant is chosen at checkout.
- [[file-asset]] — image + gallery files referenced by the Bundle.
- [[category]] — Bundles can be categorised like any product.

## Open Questions

None.
