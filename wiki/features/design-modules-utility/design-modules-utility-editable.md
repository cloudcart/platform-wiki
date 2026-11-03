---
type: feature
nav_path: "Design → Modules → Utility → Editable modules"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Filters module", "Product catalog settings module", "Social icons module", "Footer text module", "Checkout text module", "Header text module", "Yotpo reviews module legacy", "Модул филтри", "Модул социални мрежи", "Модул долен текст"]
tags: [design, modules, storefront-customisation, editable]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

# Utility modules — Editable

> Part of [[design-modules-utility]]. See the hub for the catalogue, system modules, page-builder blocks, and storage / cache mechanics.

## Purpose

The utility modules that DO have an edit form on the Modules screen — the only ones the merchant configures by clicking a card: `filters`, `social`, the three `extra.text` instances (`footerText` / `checkoutText` / `headerText`), and the legacy `yotpoReviews` toggle.

## Where to find it

Sidebar → **Design** → **Modules** — then:

| Module | Tab |
|--------|-----|
| `filters` | **Products** tab — card labelled "Product Catalog Settings" |
| `social` | **Others** tab |
| `footerText` / `checkoutText` / `headerText` | **Others** tab — three separate cards |
| `yotpoReviews` (legacy) | **Others** tab — only when the Yotpo app is installed |

## What the merchant can do here

Standard actions on every editable module card: **Save module**, **Reset module** (to theme defaults), **Cancel**, and an **Enable / disable** master toggle. Confirmations and success messages are in the Save / Reset / Cancel table below; the save / reset pipeline (validation, cache invalidation, storage) is in [[design-modules-utility-storage]].

## Settings & fields

### `filters` — Product catalog settings (`product.filters`)

The MASTER settings module for EVERY product-listing page — category, search, vendor, smart-collection, and the wishlist. Controls per-page count, products per row, sorting, filter chips, price ranges, and card-display toggles. Shown on the **Products** tab as **"Product Catalog Settings"** (despite the `filters` instance name). Universal.

Selected fields (the form has 40+):

- **Layout / counts.** `per_page` (default, must be one of `per_page_options`); `per_page_options` (e.g. `9`/`18`/`36`/`72` — 2-10 entries, each 2-100); `per_row` (1-5, desktop); `per_row_mobile` (1-2).
- **Sorting.** `order_by` (**date** (id) / **name** / **price** / **sale** / **new** / **featured** / **sort_order**); `order_by_options`; `order_direction` (**asc** / **desc**).
- **Filter chips.** `filters_options` (which appear: **categories**, **sort**, **sort_direction**, **per_page_filter**, **price_ranges**, **vendors**, **new**, **sale**, **variants**, etc.); `filters_sort_numbers` (per-filter order, new themes only).
- **Price filter.** `products_price_ranges` (from / to ranges; when mode is NOT `range_slider`); `price_range_step` (slider step; only when `mode: range_slider`).
- **Card display toggles.** `listing_show_wishlist` / `listing_show_compare` / `listing_show_price` / `listing_show_buy` (wishlist / compare icon, price, Buy button); `show_quick_view`; `hide_sale` / `hide_featured` (SALE / FEATURED badge); `show_short_description`; `second_image_show` (on hover); `manufacturer_logo_show` (brand-logo overlay); `color_product_variants` (multiselect); `variants` (variant pickers).
- **Out-of-stock.** `show_out_of_stock_products` (include); `mark_out_of_stock_products` (badge instead of hiding); `order_latest_out_of_stock` (push to END).
- **Facets.** `show_facet_counts` (count per facet, e.g. "Red (12)"); `enable_category_properties` (needs theme + `categoryProperties` — see [[design-modules-utility-system]]); `category_properties_limit`.
- **Templates (new themes only).** `list_class` (card template — **_list-one** / **_list-two** / **_list-horizontal**); `list_horizontal_size` (height — small / normal / large); `list` (filter position — sidebar, top-bar, etc.). Shown only on themes advertising "new theme settings".

**Tips.**
- "Change products-per-page", "add a Sale filter", "show out-of-stock products" all live here; `filters_options` is the source of truth for which chips appear.
- `mode: range_slider` is set in theme config, NOT the form — in slider mode edit `price_range_step` instead of the price-range list.
- The merchant CAN add `per_page_options` (e.g. `15`, `30`, `60`), but `per_page` must stay one of them.
- Raising `per_row` (3→4) usually needs a matching `list_class` change or cards overflow.
- "Browsable but distinct" out-of-stock = `show_out_of_stock_products` + `mark_out_of_stock_products` + `order_latest_out_of_stock`.

---

### `social` — Social network icons row (`extra.social`)

Renders the row of social-network icons linking to the store's profiles — theme-controlled placement (usually footer); universal. Each network has two fields — `<network>_link` (valid URL) and `<network>_show` (toggle); BOTH must be set for the icon to appear.

Networks, with default URL and default `show`: Facebook (`facebook`, `http://www.facebook.com`, ON); X / Twitter (`x`, `https://x.com/`, ON); Instagram (`instagram`, `https://www.instagram.com`, ON); Pinterest (`pinterest`, `http://www.pinterest.com`, OFF); YouTube (`youtube`, `https://www.youtube.com`, OFF); LinkedIn (`linkedin`, `https://www.linkedin.com`, OFF); TikTok (`tiktok`, `https://www.tiktok.com`, OFF).

**Tips.**
- An empty link with `show` ON falls back to a global per-network default in [[settings-general]] — but cleaner to fill the real profile URL. If ALL networks are off, the row self-hides.
- No built-in slot for WhatsApp / Telegram — add an extra link via [[design-modules-navigation]] `navigationLinks` with a `tel:` or `https://wa.me/...` URL.
- The supported network list is fixed by the platform; removing one (e.g. old "twitter") may need a theme switch.

---

### `footerText`, `checkoutText`, `headerText` — Theme-slot text blocks (`extra.text` instances)

Three INSTANCES of the generic `extra.text` module — same TYPE, different theme slot; the instance name decides the slot:

- `headerText` → header — short marketing tagline / promo near the logo.
- `footerText` → footer — long-form copy: store description, copyright, ABN/VAT number, contact summary; good for legal + SEO copy.
- `checkoutText` → checkout summary — reassurance / shipping-promise text; keep short (e.g. "Secure SSL checkout, 30-day returns").

Fields (identical for all three): `enabled` (toggle, default on — when off the slot is empty); `title` (text, char:0-250, default "Example title" — optional heading); `text` (rich-text editor, char:1-30000, default "Example text" — body; supports inline HTML, links, formatting, embedded images).

Each theme ships its own combination (most have `footerText`, about half `checkoutText`, fewer `headerText`). Switching themes can ADD or REMOVE instances — settings for a removed instance persist but become non-editable.

**Tips.**
- Interchangeable in form but render in different places — don't put footer copy in `headerText`.
- Use the editor's source-view to paste exact HTML; keep copy lean despite the 30 000-char limit.
- With the `multylang` app, per-language bodies use the language switcher inside the editor.

---

### `yotpoReviews` (legacy) — Yotpo reviews enable toggle (`extra.yotpoReviews`)

A gate that turns the Yotpo reviews UI on/off for the active theme. When the Yotpo integration is installed and this module is `enabled` (toggle, default on), the theme renders Yotpo's review block in its slots (usually product pages + homepage). Shown on the **Others** tab only when the Yotpo app is installed. No API keys here — keys live in [[apps-yotpo-settings]]. Only themes with a `yotpoReviews` instance + a slot render Yotpo.

**Tips.**
- For per-page placement use the richer page-builder `yotpo-reviews` block (Reviews type — site-wide vs per-product; Product picker) — see [[design-modules-utility-page-builder]].
- If reviews don't appear despite this module being ON, confirm the Yotpo app is installed AND the App Key + Secret are set in [[apps-yotpo-settings]].
- This gate only affects theme storefront blocks — to fully disable Yotpo, uninstall the app or remove the API keys.

## Business rules

- **`filters` changes apply globally** to every product-listing page — no per-page override. For per-page customisation, use [[marketing-landing-pages]] Dynamic pages.
- **`social` falls back to global URLs when blank.** A blank URL with `show` ON pulls the global URL from [[settings-general]].
- **`extra.text` instances are per-slot, not shared.** Editing `footerText` does not change `checkoutText` / `headerText`; reuse copy by pasting into each.

### Save / Reset / Cancel — standard buttons

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists settings; rebuilds cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

## Related

- [[design-modules-utility]] — hub.
- [[design-modules-utility-catalogue]] — full module list.
- [[design-modules-utility-storage]] — save / reset pipeline + cache invalidation.
- [[settings-general]] — social URL fallbacks; store SEO.
- [[apps-yotpo-settings]] — Yotpo API keys (gates the `yotpoReviews` modules).
- [[marketing-landing-pages]] — Dynamic pages for per-page overrides.

## Open questions

- 📡 **`social` module URL fallbacks.** Pulls from general-settings keys (`facebook_link`, `instagram_link`, `youtube_link`, `x_link`, etc.) — see [[settings-general]]. GraphQL-resolvable: query general settings for configured social URLs.
- 📡 **`extra.text` per-language content.** With `multylang`, the three text instances accept per-language bodies via the language switcher. GraphQL-resolvable: query whether `multylang` is installed.
