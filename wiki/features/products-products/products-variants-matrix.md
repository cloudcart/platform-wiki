---
type: feature
nav_path: "Products → Products → Variants matrix"
route_name: ""
route_path: "/admin/products/edit/:id (modal)"
aliases: ["Variants matrix", "Manage variants", "Edit Variant options", "Product type settings", "Simple Product", "Product with variants", "Add unit price", "Variant manage modal", "Per-variant grid", "Variant detail panel", "Edit Variant side-panel", "Inventory card", "Not for parcel lockers", "Variant bulk actions", "Манаджирай варианти"]
tags: [catalog, products, variants, inventory, matrix, modal]
plan_gates: ["multi_variants"]
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, bulk actions, known issues).

# Products — Variants matrix

## Purpose

The Variants matrix is the per-SKU editing surface inside the [[products-editor|product editor]] — a wide side window titled **Edit Variant options** where the merchant sets price, discount, SKU, barcode, min-order quantity, quantity and weight for **every** variant of a multi-variant product, the only place these are editable per-variant in bulk from one screen. Three adjacent surfaces are documented here too: the **Product type settings** card that holds it, the **Edit Variant** side panel (opens on a row's name; per-variant pricing and inventory + checkout-link action) and the **Inventory** card on the editor (Track-inventory, Requires-shipping and advanced inventory settings).

## Where to find it

- From the [[products-editor]] → **Product type settings** → **Manage variants** button (only after the merchant has picked variant parameters + values). Clicking a value in the **Product variants** summary opens the window filtered to that value.
- The Inventory card appears inline in the same card.

## What the merchant can do here

### Product type settings card

The card opens with a two-choice toggle:

- **Simple Product** — **Pricing**: **Price**, and **On Sale** with **Discount** (amount or percent) + **Sale price**. Going back to it from a product with variants asks *"Set Product to Simple"*: *"This will remove the variants from you product and set it as a simple product."*
- **Product with variants** — rows of **Variant name** + **Variant values**. Pick from the list or type a new name to create one; **Add value** adds a row, up to 3. **Save** turns them into the **Product variants** summary with a pen icon to edit, and **Manage variants** opens the window below.

With the Grocery store app, the **Pricing** block on physical products also has **Add unit price** (marked **Extended**), which adds the price type (**Price per measurement unit** / **Price per package**), measurement unit, **Minimum order qty** and **Visualization**.

### Edit Variant options — header

- Free-text **Search** field — filters the matrix by value / SKU / barcode / price.
- **Filter tag chips** — every unique value appears as a clickable chip; clicking adds it as a filter; chips combine.
- **Modify columns** — show / hide columns (**Price** and **Discount** always stay).

### Per-row editable columns

- **Variant** (the header shows the parameter names, e.g. *Color / Size*) — variant value (read-only) + thumbnail (click opens the variant image modal); clicking the name opens the **Edit Variant** side panel.
- **Price** — currency input.
- **Discount** — amount or percent; the sale price is worked out from it. A discount above the price shows *"Sale price must be greater than or equal to 0"* and clears the discount.
- **SKU** / **Barcode** — text.
- **Min. Order qty** — numeric.
- **Quantity** — numeric. Column header carries a **Track-inventory** toggle; when OFF the column is disabled.
- **Weight** — numeric (min 0.01). Column header carries a **Requires-shipping** toggle; when OFF the column is disabled.

### Bulk actions (apply to all selected variants)

The **Tools** button holds them. Each opens a popup with the matching input: **Modify price**, **Modify SKU**, **Modify barcode**, **Modify min quantity**, **Modify weight** (only when Requires shipping is ON), **Modify quantity** (only when Track inventory is ON). **Modify images** assigns one image set to several variants at once. **Delete** removes the selected rows straight away, with *"Selected variants have been removed"* — deleting all resets the matrix to a single default row. On a phone the same actions unfold as a list under **Tools**. All of this stays in the form until the product is saved.

### Edit Variant side panel

Clicking a variant's name opens the **Edit Variant** side panel:

- Thumbnail + display name (click thumbnail to open the variant image picker).
- **Checkout link** action — copies the variant's checkout-link URL to clipboard (with tooltip *"You need to save you changes first to generate the chechout link"* if the variant has no ID yet).
- **Pricing**: **Price**, **On Sale** with **Discount** (amount or percent) + **Sale price**, and **Add unit price** with the Grocery store app.
- **Inventory**: **SKU**, **Barcode**, **Track inventory** → **Total quantity**, **Requires shipping** → **Weight**, **Minimum order qty**.

### Inventory card on the editor

The **Inventory** card closes the **Product type settings** card, and also the digital product's **Product setup** card. Multi-variant products show only the advanced settings here, and set the rest per variant in the matrix.

**Top-level toggles:** **Product has SKU/Barcode** → SKU + Barcode inputs. **Track inventory** → **Product quantity** input (min 0). **Requires shipping** (hidden for digital `type_digital=page`) → **Product weight** input (min 0.01).

**Advanced inventory settings (**Show settings** / **Hide settings**):** **Minimum order qty** → numeric input (simple products without a unit price). **Continue selling when out ot stock**. **Notify me when quantity is below** (only when tracking is ON) → **Product quantity** threshold input. **Custom statuses** → two pickers, *"Product status in stock"* + *"Product status out of stock"* (the out-of-stock one is disabled, with the tooltip *"Enable Track Inventory or disable Continue Selling option"*, when `continue_selling = 1` or tracking is off); a *"Create new status"* link opens the [[products-statuses]] create modal inline. **Dimensions** → **Length** / **Width** / **Height** inputs in millimetres, and **Not for parcel lockers** (*"Delivery to a parcel locker is not offered at checkout when this product is in the cart"*, [[shipping-provider-mech-locker-fit]]), both on non-page product types only. Turning **Track inventory** off also clears **Continue selling** and the threshold.

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

For a product with variants, the **Qty** column on [[products-list-view]] shows the **sum across variants**; editing quantity on the parent (without selecting a variant) is disabled — the merchant sets it per variant, and tracking applies per-variant. For products WITHOUT variants, quantity is set on the product via the Inventory card; tracking drives stock decrement at checkout (per [[settings-cart]] → `order_status_for_quantity_decrease`).

### Variant deletion edge case

Deleting ALL variants resets the matrix to a single default row; on save the product becomes simple (no-variant) (verify).

### `multi_variants` plan gate

`multi_variants` is the plan feature for multi-variant products; on the Admin GraphQL API, creating a variant needs it. See [[inventory-variant-model]] for downstream consequences.

## Related

- [[products-products]] — hub.
- [[products-editor]] — where the **Product type settings** card + Inventory card live.
- [[products-variants-options]] — parameter / option screen (rename / merge / values).
- [[products-statuses]] — picked in the Custom statuses block.
- [[products-digital]] — the digital product's **Product setup** card.
- [[shipping-provider-mech-locker-fit]] — **Not for parcel lockers**.
- [[inventory-tracking]] — cross-cutting inventory model; the Inventory card is one surface.
- [[inventory-variant-model]] — variant-as-unit-of-stock rule + the three master switches.
- [[inventory-oversell]] — what **Continue selling** does.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `product_threshold` (drive when the tracking toggles take effect).
- [[variant]] / [[variants-model]] — entity + structural model.

## Open questions

None.
