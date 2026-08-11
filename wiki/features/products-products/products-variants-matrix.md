---
type: feature
nav_path: "Products → Products → Variants matrix"
route_name: ""
route_path: "/admin/products/products-new/edit/:id (modal)"
aliases: ["Variants matrix", "Variant manage modal", "Per-variant grid", "Variant detail panel", "Edit Variant side-panel", "Inventory card", "Variant bulk actions", "Манаджирай варианти"]
tags: [catalog, products, variants, inventory, matrix, modal]
plan_gates: ["multi_variants"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, bulk actions, known issues).

# Products — Variants matrix

## Purpose

The Variants matrix is the per-SKU editing surface inside the [[products-editor|product editor]] — a full-screen modal where the merchant sets price, discount, SKU, barcode, min-order quantity, quantity and weight for **every** variant of a multi-variant product, the only place these are editable per-variant in bulk from one screen. Two adjacent surfaces are documented here too: the **Variant detail side panel** (opens on a row's name; full per-variant pricing module + checkout-link action) and the **Inventory card** (on the editor for simple / digital products that don't open the matrix; Track-inventory, Requires-shipping and advanced inventory settings).

## Where to find it

- From the [[products-editor]] → Variants section → **Manage variants** button (only after the merchant has picked variant parameters + values).
- The Inventory card appears inline in the same Variants section, for products without a per-variant matrix.

## What the merchant can do here

### Manage modal — header

- Free-text **Search** field — filters the matrix by `v1` / `v2` / `v3` / SKU / barcode / price.
- **Filter tag chips** — every unique value appears as a clickable chip; clicking adds it as a filter; chips combine.
- **Manage columns** — show / hide columns.

### Per-row editable columns

- **Name** — variant value (read-only) + thumbnail (click opens the variant image modal); clicking the name opens the Variant detail side panel.
- **Price** — currency input (step 0.01, min 0).
- **Discount** — discount price + auto-computed Save % (clears the discount if the save would be negative).
- **SKU** / **Barcode** — text.
- **Min. Order qty** — numeric, min 1.
- **Quantity** — numeric (min 0). Column header carries a **Track-inventory** toggle; when OFF the column is disabled.
- **Weight** — numeric (min 0.01, step 0.01). Column header carries a **Requires-shipping** toggle; when OFF the column is disabled.

### Bulk actions (apply to all selected variants)

Each opens a popup with the matching input: **Modify price**, **Modify SKU**, **Modify barcode**, **Modify min quantity**, **Modify weight** (only when Requires shipping is ON), **Modify quantity** (only when Track inventory is ON). **Modify images** assigns one image set to several variants at once. **Delete** asks *"Are you sure you want to delete the selected variants?"* then removes the selected rows — deleting all resets the matrix to a single default row. A mobile **Bulk Actions** sub-modal lists the same actions as tappable rows.

### Variant detail side-panel modal

Clicking a variant's name opens the **Edit Variant** side panel:

- Thumbnail + display name (click thumbnail to open the variant image picker).
- **Checkout link** action — copies the variant's checkout-link URL to clipboard (greyed out with tooltip *"You need to save your changes first to generate the checkout link"* if the variant has no ID yet).
- Full per-variant pricing module (base price, discount price, percent / fixed discount type, price-from / price-to behaviour).

### Inventory card on the editor (simple / digital products)

For simple / digital products the Variants section embeds an **Inventory** card directly (multi-variant products use the matrix instead).

**Top-level toggles:** **Product has SKU/Barcode** → SKU + Barcode inputs. **Track inventory** → **Product quantity** input (min 0). **Requires shipping** (hidden for digital `type_digital=page`) → **Product weight** input (min 0).

**Advanced inventory settings (collapsible):** **Minimum order qty** → numeric input. **Continue selling when out of stock**. **Notify me when quantity is below** (only when tracking is ON) → **Product quantity** threshold input. **Custom statuses** → two pickers, *"Product status in stock"* + *"Product status out of stock"* (the out-of-stock one is disabled, with a tooltip, when `continue_selling = 1` or tracking is off); a *"Create new status"* link opens the [[products-statuses]] create modal inline. **Dimensions** → Width / Depth / Height inputs (non-page product types only).

## Settings & fields

### Data-model caps

- At most **3 variant parameters** per product (e.g. Color + Size + Material) — a hard cap. See [[products-known-issues]].
- At most **500 variants** total; a larger save fails with *"max allowed exceeded"*. The 3 parameters combine freely within the cap — 50 sizes × 10 colors = 500 is fine, 50 × 11 = 550 is rejected.
- A variant's `quantity` is capped at **50,000,000**.

### Validation summary

- Duplicate `(v1, v2, v3)` combinations are rejected — every variant must be unique across the three parameter slots.
- `sku`, `barcode`: max 191 chars each.
- Price: currency amount, up to 10 decimal places. Empty price → base product price applies.
- `quantity`: min 0, max 50 000 000.
- `weight`: min 0.01, max 10 000 000 (enforced only when Requires shipping is ON).

## Business rules

### Variant value rename: future only; Merge also rewrites order history

Renaming a variant value (e.g. Color "Red" → "Crimson") on the per-parameter Values page ([[products-variants-options]]) updates every referencing variant's displayed text (`v1` / `v2` / `v3` columns); the matrix shows it on next load. **Past orders that bought the variant do NOT update** — their order-line keeps the name recorded at purchase. The **Merge values** action differs: it rewrites BOTH future variants AND past order records (historical order-lines are reassigned to the survivor value). **Merge is irreversible.**

### Variant parameter rename cascades to all products

Renaming a variant parameter (e.g. "Color" → "Colour") on the Variants list page updates the `p1` / `p2` / `p3` text on every product using it — no per-product re-save.

### "Show as separate product in listing" toggle is throttled to 24 h

Toggling *"Show each variant as a separate product in the listing"* ON/OFF on an existing parameter (paid plan), or changing *"Include the variant name in the product title"*, sets the parameter's `next_update` to now + 24 hours and blocks re-toggling these two settings until then — a guard while the storefront listing rebuilds. Renames and other parameter changes are NOT throttled; only these two listing-mode toggles are.

### Variant quantity vs product quantity

For a product with variants, the **Quantity** column on [[products-list-view]] shows the **sum across variants**; editing quantity on the parent (without selecting a variant) is disabled — the merchant sets it per variant, and tracking applies per-variant. For products WITHOUT variants, quantity is set on the product via the Inventory card; tracking drives stock decrement at checkout (per [[settings-cart]] → `order_status_for_quantity_decrease`).

### Variant deletion edge case

Deleting ALL variants resets the matrix to a single default row; on save the product becomes simple (no-variant).

### `multi_variants` plan gate

Defining more than the default single variant requires the `multi_variants` plan feature. Stores without it see the Variants section but cannot add parameters. See [[inventory-variant-model]] for downstream consequences.

## Related

- [[products-products]] — hub.
- [[products-editor]] — where the Variants section + Inventory card live.
- [[products-variants-options]] — parameter / option screen (rename / merge / values).
- [[products-statuses]] — picked in the Custom statuses block.
- [[inventory-tracking]] — cross-cutting inventory model; the Inventory card is one surface.
- [[inventory-variant-model]] — variant-as-unit-of-stock rule + the three master switches.
- [[inventory-oversell]] — what "Continue selling when out of stock" does.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `product_threshold` (drive when the tracking toggles take effect).
- [[variant]] / [[variants-model]] — entity + structural model.

## Open questions

None.
