---
type: storefront-page
route_name: compare
route_path: /compare
themes_using: [all]
tags: [storefront, compare, products]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Product compare (storefront)

## Purpose

Side-by-side comparison of products the customer has added to the compare tray. Shows product image, name, vendor, price, key attribute groups (the "compare-on" attributes the merchant configured), and a per-product CTA back to the product page.

## URL & route

- **Route name:** `compare`
- **Path:** `/compare`
- **Method:** `GET`.
- **Controller:** the request handler.
- Lives inside the `compare` route group: the platform code.

## How it loads

1. the request handler resolves the active compare tray (cookie/session-held list of product IDs) and loads each product with its compare attributes.
2. `templates/compare/compare.tpl` renders the layout shell (breadcrumb + section title `sf.global.compare.products`).
3. the theme templates (the theme templates, shared across themes) renders a `<table>` with one column per product. Rows include:
   - Product card row (image, ribbon labels, name, price).
   - Vendor row.
   - One row per `compare_group` (the attribute groups the merchant flagged "compare-on") — value is `$compares->get($product->id)->get($group)->implode(', ')`.
   - Actions row — "Details" button linking to the product URL.
4. The wrapper table carries `js-compare-boxes-holder`; each column is tagged `js-compare-box-item js-compare-box-item-{$product->id}` so the storefront JS can hot-remove a column.

## What the customer sees

- Breadcrumb: **Home › Compare products**.
- `<h1>` "Compare products".
- A horizontally-scrollable table with up to N products (typical limit 3-4 — verify the actual cap and where it's configured).
- Per-column controls:
  - Remove `x` link (`.js-remove-compare-box`) with `data-id="{$product->id}"`.
  - Ribbon labels (NEW / SALE / FEATURED / discount-amount badge) reused from the product list partials.
  - Price (with old/new when on sale).
  - Vendor name.
  - One row per comparable attribute group.
  - "Details" CTA linking to the product page.
- Empty tray: the table renders with the labels column only; some themes inject an explicit "No products in compare yet" notice (verify).

## Storefront behaviour

- The compare tray is held in cookies/session — anonymous and logged-in customers both have a tray.
- "Add to compare" is a checkbox rendered on product cards via the theme templates:
  _(platform implementation detail omitted)_

- The `product-compare` data-module hijacks the checkbox change event, posts to the compare endpoint, and updates the header tray counter.
- The page hot-removes a column when the customer clicks the `x` — the controller does NOT need a full reload.
- "Add to cart" itself is NOT in the compare row — the per-column CTA links back to the product page where variant pickers live.

## JavaScript behaviour

- `js-compare-boxes-holder` — wrapper table; targeted by the compare client script.
- `js-compare-box-item` / `js-compare-box-item-{$product->id}` — per-column tags for in-place removal.
- `js-remove-compare-box` with `data-id` — click handler for the column remove control.
- `js-product-compare-check-{$product->id}` with `data-module="product-compare"` — the add/remove checkbox on product cards.
- `data-uicontrol="uniform"` — instructs the storefront's checkbox-skin library to style the input.

## Customisations available to the merchant

- **Which attributes show as rows** — controlled by marking attribute groups as "comparable" in the catalog attributes admin (verify exact UI path — typically **products-attributes** or the attribute group settings).
- **Hide the compare feature on listings** — `listing_show_compare` flag in `$list_widget_settings` controls whether the compare checkbox appears on product cards.
- **Compare tray cap** — typical 3-4 products (verify the setting key / hard-coded limit).
- **Vendor row** — only renders when products have a vendor assigned.
- The empty-state copy / illustration is theme-specific.

## Theme variations

- All themes share the theme templates — the table is the same shape.
- `compare.tpl` is identical across most themes (breadcrumb + heading + the shared table); themes differ in CSS for the table (sticky labels column, alternating row colours, horizontal scroll indicators).
- Themes that hide the feature entirely (rare) omit the compare include in the theme templates and never link to `/compare`.

## Known issues / by-design vs bug

- The compare tray is COOKIE-scoped, not customer-scoped — clearing cookies wipes the tray even for logged-in customers (verify whether logged-in trays sync to the customer record).
- The "Add to compare" checkbox uses a uniform-skin overlay; if the storefront's uniform JS fails to load, clicks may pass to the underlying checkbox which still works but looks unstyled.
- Exceeding the cap silently drops new additions on some themes; others show a toast — verify the storefront framework behaviour.
- Compare attribute values are joined with `, ` — long arrays produce a wide row that can break mobile layout.

## Related

- [[wishlist]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm the maximum number of products that can be in the compare tray (and whether the limit is configurable).
- Confirm where in admin the merchant marks an attribute group as "comparable".
- Confirm whether logged-in customers' compare trays persist to the customer record (like wishlists) or stay cookie-only.
- Confirm the exact endpoint the `product-compare` data-module posts to on add/remove.
