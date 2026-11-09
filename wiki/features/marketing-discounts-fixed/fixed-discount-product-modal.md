---
type: feature
nav_path: "Marketing → Discounts → Products → Per-product modal"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id, /admin/marketing/discounts/create/fixed
aliases: ["Fixed discount product modal", "Common price vs Multiple price", "Add product to Fixed discount"]
tags: [marketing, discounts, fixed, modal, ui]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (validation rules, row writes, plan gates, API access, storefront display).

# Fixed discount — per-product modal & list view

## Purpose

This aspect covers the **interactive surface** of the Fixed-discount products page: the list of attached products and the per-product price modal that opens to add or edit a product's fixed prices. It also covers the minimal parent-discount create form for Fixed type.

For what gets written when the modal saves, see [[fixed-discount-row-writes]]; for what's rejected, see [[fixed-discount-validation-rules]].

## Where to find it

From [[marketing-discounts]] → click "Products" on any Fixed-type row. The list of attached products is the page body; the **+ Add product** button (or a row click) opens the modal.

Route: `/admin/marketing/discounts/products/:id` (route name `discounts-products`).

## What the merchant can do here

### From the list view

- See every attached product in a grid. Columns:
  - **Product Name** — name with thumbnail; **+ Add product** opens the price-edit modal.
  - **Price** — the product's price (catalog → fixed). Sortable.
  - **Active** — inline toggle; persists immediately via the discount-products status endpoint. Inactive products keep the discount row but the storefront skips it.
  - (actions) — a row **remove** action detaches the product from the discount.
- Bulk **Set status active** / **Set status unactive** and bulk-delete via the table action bar.
- Search by product name in the grid's **Search and Filter** box (a part of the name matches), filter by **Active** (Yes / No), sort by name, price or Active, and paginate.

### The per-product price modal flow

The price modal opens from the products list (**+ Add product** OR row click). It's titled *"Add product"* (new) or *"Edit product"* (existing). Flow:

1. **Product picker step** — only on Add. A single product-search field. On selecting a product, its variants are fetched. On Edit the product is fixed and the header shows its thumbnail + name (no picker).
2. **Pricing mode radio** — only when the product has multiple variants OR its `type` is `multiple`:
   - **Common price** (`single`) — one price applied to all variants.
   - **Multiple price** (`multiple`) — one price per variant.
3. **Pricing table** — three shapes:
   - **No variants** — one row: Price in store (read-only catalog price) + New price (editable currency input).
   - **Multi-variant common-price** — the first variant's row only; its New price applies to all variants on save.
   - **Multi-variant multi-price** — every variant in its own row, with Variant options (e.g., "Red / XL"), Price in store, New price.

The save button persists the prices; backdrop / Esc are disabled while saving. State reset on close and pricing-mode auto-detection on Edit are covered under **Business rules** below.

## Settings & fields

### Common modal fields (always present)

| Field | What it does |
|-------|--------------|
| **Pricing mode** | **Common price** (`single`) or **Multiple price** (`multiple`). Decides how many **New price** inputs show; it is not stored. |
| **Price in store** | Read-only catalog price of the variant. |

The save sends one entry per variant: `product_id`, `variant_id`, `price` (in cents).

### Per-product edit modal — `single` price mode

| Field | What it does | Validation |
|-------|--------------|------------|
| **New price** | The new price applied to **every variant** of the product. | From 0.01 up to and including the cheapest variant's catalog price; a higher one fails the whole save. |

### Per-product edit modal — `multiple` (per-variant) price mode

For each variant:

| Field | What it does | Validation |
|-------|--------------|------------|
| **New price** | The new price for this specific variant. | From 0.01 up to and including this variant's catalog price; a higher or blank one fails the whole save. |

> The modal shows **Price in store** (read-only) and a **New price** input per variant.

### Fixed-discount create form (parent discount settings)

The parent Fixed discount is created via the standard create form with `type=fixed`. Minimal field set:

- **General settings** — status + name only (no discount-type select, no value field; per-product prices are entered later in this products sub-page).
- **Customer groups** — shared block.
- **Color settings** — background + text color for the on-storefront label.
- **Discount amount in label** — As percent / As fixed amount radio (no "Don't change" option in the modern UI).
- **Date range** — start + end + No expiration, plus timer-in-listing / timer-in-details switches.

No Discount-target block (Fixed discounts target products via the per-product attachment table, not the `settings` field), no Discount-limits block, no Regions block.

### What the merchant CANNOT do here

- **Set a fixed price higher than the variant's catalog price** — *"Price must be at least 1 and less than &lt;catalog price&gt;"*; the whole save fails.
- **Mass-import per-variant prices** — one product at a time here; for bulk price import, use the Products listing's price-import feature.

See [[fixed-discount-validation-rules]] for the full validation set, including the cross-discount uniqueness story.

## Business rules (modal-scoped)

### Pricing-mode auto-detection on Edit

On Edit, the modal pre-fetches existing per-variant prices and groups them by `discount_price`. If all variants share the same price, the form starts in `single` (Common price) mode; otherwise `multiple` (Multiple price). The merchant can switch modes mid-edit; switching `multiple` → `single` collapses to the first variant's price.

### State reset on close

Closing via X, backdrop, or Esc resets all internal state (selected product, fetched variants, chosen mode, entered prices). Re-opening starts fresh — no draft persistence.

### Active toggle is inline + immediate

The Active column's switch is not part of the modal — it persists immediately via a separate status endpoint. Toggling triggers the same product-updated + search-engine-sync effects as a save.

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-validation-rules]] — what gets rejected on save (and the equality-edge-case quirks).
- [[fixed-discount-row-writes]] — what actually lands in `product_to_discount` after the modal saves.
- [[fixed-discount-api-access]] — the endpoint table this modal calls.
- [[marketing-discounts-products]] — shared per-product price assignment page (same component).
- [[marketing-discounts]] — parent feature; the Fixed discount type lives there.

## Open questions

No outstanding questions.
