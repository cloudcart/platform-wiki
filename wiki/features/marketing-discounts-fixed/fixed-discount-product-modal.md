---
type: feature
nav_path: "Marketing → Discounts → Products → Per-product modal"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Fixed discount product modal", "Common price vs Multiple price", "Add product to Fixed discount"]
tags: [marketing, discounts, fixed, modal, ui]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (validation rules, row writes, plan gates, API access, storefront display).

# Fixed discount — per-product modal & list view

## Purpose

This aspect covers the **interactive surface** of the Fixed-discount products page: the list of attached products and the per-product price modal that opens to add or edit a product's fixed prices. It also covers the minimal parent-discount create form for Fixed type.

For what gets written when the modal saves, see [[fixed-discount-row-writes]]; for what's rejected, see [[fixed-discount-validation-rules]].

## Where to find it

From [[marketing-discounts]] → click "Products" on any Fixed-type row. The list of attached products is the page body; the **+ Add product** button (or a row click) opens the modal.

Route: `/admin/marketing-new/discounts/products/:id` (route name `discounts-products`).

## What the merchant can do here

### From the list view

- See every attached product in a grid. Columns:
  - **Product Name** — name with thumbnail; **+ Add product** opens the price-edit modal.
  - **Price** — the product's price (catalog → fixed). Sortable.
  - **Active** — inline toggle; persists immediately via the discount-products status endpoint. Inactive products keep the discount row but the storefront skips it.
  - (actions) — a row **remove** action detaches the product from the discount.
- Bulk **Set status active** / **Set status unactive** and bulk-delete via the table action bar.
- Filter by **Active** (Yes / No), sort, and paginate using the standard grid.

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

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Price type** | `price_type` | `single` or `multiple` — controls which validation set applies. |
| **Prices array** | `prices[]` | One entry per variant: `variant_id`, `price` (catalog price, for validation), and `fixed_price` / `msrp_price`. |

### Per-product edit modal — `single` price mode

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Fixed price (single)** | `fixed_price` | The new price applied to **every variant** of the product. | Required, numeric, `maximum_single:prices.*.price` — must be ≤ the cheapest variant's price. |
| **MSRP (single)** | `msrp_price` | The struck-through "was" price (MSRP mode only — legacy form). | Numeric, min 0, `msrp_price:fixed_price` — must be > `fixed_price`. |

### Per-product edit modal — `multiple` (per-variant) price mode

For each variant:

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Fixed price (per variant)** | `prices.*.fixed_price` | The new price for this specific variant. | Required, numeric, `maximum:prices.*.price` — must be ≤ this variant's catalog price. |
| **MSRP (per variant)** | `prices.*.msrp_price` | The struck-through "was" price for this variant (MSRP mode only — legacy form). | Numeric, min 0, `msrp_price:prices.*.fixed_price` — must be > the variant's fixed price. |

> The modern modal shows only **Price in store** (read-only) and a **New price** input per variant — there is no MSRP field. Stores on the modern UI cannot set a separate MSRP "was" price here. See [[fixed-discount-validation-rules]] for the legacy MSRP-mode details.

### Fixed-discount create form (parent discount settings)

The parent Fixed discount is created via the standard create form with `type=fixed`. Minimal field set:

- **General settings** — status + name only (no discount-type select, no value field; per-product prices are entered later in this products sub-page).
- **Customer groups** — shared block.
- **Color settings** — background + text color for the on-storefront label.
- **Discount amount in label** — As percent / As fixed amount radio (no "Don't change" option in the modern UI).
- **Date range** — start + end + No expiration, plus timer-in-listing / timer-in-details switches.

No Discount-target block (Fixed discounts target products via the per-product attachment table, not the `settings` field), no Discount-limits block, no Regions block. The MSRP flag, `apply_regular_price`, and similar advanced fields live on the parent record but are managed via the legacy edit form for stores still on the old UI.

### What the merchant CANNOT do here

- **Set a fixed price higher than the variant's catalog price** — *"The discount price can not be higher than the price of the item"*; the per-variant validator `maximum:prices.*.price` rejects with the cap value.
- **Set an MSRP lower than the fixed price** — *"The discount.action.msrp must be at least <fixed_price + 1>"*.
- **Add a product already covered by another Fixed discount** — the parent save validates uniqueness across active Fixed discounts (verify).
- **Attach products from incompatible parent / child categories** — *"Parent and Child product categories, can not be included"*.
- **Mass-import per-variant prices** — one product at a time here; for bulk price import, use the Products listing's price-import feature.

See [[fixed-discount-validation-rules]] for the full validation set, including the cross-discount uniqueness story.

## Business rules (modal-scoped)

### Pricing-mode auto-detection on Edit

On Edit, the modal pre-fetches existing per-variant prices and groups them by `(discount_price, msrp_price)` pair. If all variants share the same pair, the form starts in `single` (Common price) mode; otherwise `multiple` (Multiple price). The merchant can switch modes mid-edit; switching `multiple` → `single` collapses to the first variant's price.

### State reset on close

Closing via X, backdrop, or Esc resets all internal state (selected product, fetched variants, chosen mode, entered prices). Re-opening starts fresh — no draft persistence.

### Active toggle is inline + immediate

The Active column's switch is not part of the modal — it persists immediately via a separate status endpoint. Toggling triggers the same product-updated + search-engine-sync effects as a save, and counts against the 10-minute activation cooldown — see [[fixed-discount-plan-gates]].

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-validation-rules]] — what gets rejected on save (and the equality-edge-case quirks).
- [[fixed-discount-row-writes]] — what actually lands in `product_to_discount` after the modal saves.
- [[fixed-discount-api-access]] — the endpoint table this modal calls.
- [[marketing-discounts-products]] — shared per-product price assignment page (same component).
- [[marketing-discounts]] — parent feature; the Fixed discount type lives there.

## Open questions

- The legacy "Parent and Child product categories, can not be included" rejection — verify whether the modern modal surfaces this same error or filters categories pre-submit (verify).
