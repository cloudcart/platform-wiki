---
type: storefront-page
route_name: site.account.wishlist
route_path: /wishlist (verify)
themes_using: [all]
tags: [storefront, wishlist, favorites, customer-account]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Wishlist (storefront)

## Purpose

The customer's saved-for-later product list. Each saved item shows the same product card as in a category listing, plus a heart icon that becomes "active" on the source listing page. Visible from the main account area and reachable via the heart icons in the header / product cards.

## URL & route

- **Page route:** `site.account.wishlist` → renders `templates/wishlist.tpl` which includes `wishlist/list.tpl` (path on most themes — verify the exact public URL; the user-facing wishlist lives under the customer account section).
- **Add / remove (toggle) action:** `GET /wishlist/action/{id}` — route name `add-to-wishlist`. Toggles product `{id}` in the active wishlist (add if absent, remove if present).
- **Header dropdown:** `GET /wishlist/menu` — route name `wishlist.menu`. Returns the compact panel HTML for the header heart-icon dropdown.
- **Compact account view (AJAX):** `GET /wishlist/compact` — route name `site.account.wishlist.compact`, `IsAjax` middleware.

## How it loads

1. The wishlist page route calls the wishlist controller (verify exact class — `Site\the platform code` / the request handler).
2. `templates/wishlist.tpl` is a one-line shim that includes `wishlist/list.tpl`.
3. `wishlist/list.tpl`:
   - Sets SEO via `$module->setSeo("wishlist")`.
   - Renders the breadcrumb, the section title `sf.global.act.wishlists`, and the product grid using the theme templates with image size `600x600` and responsive `image_srcset`.
   - Adds pagination via the theme templates.
4. Anonymous customers also have a wishlist — held in cookie/session (`uuid_generate` middleware ensures a visitor ID exists). Logged-in customers' wishlists persist to the customer record so they survive cross-device.

## What the customer sees

- Breadcrumb: **Home › Wishlists**.
- Section title (`<h1>` "Wishlists").
- Grid of product cards. Each card uses the same template as category listings, which means:
  - Image (`600x600` thumb), name, price (sale & old price when applicable), labels (new / sale / featured).
  - The "favourite" heart on each card is rendered in active state (`_product-add-to-favorite active`) because the product is already in the list.
  - "Add to cart" button when the product is purchasable.
- Pagination bar.
- Empty state: the `js-empty-on-ajax` flag means after the last item is removed the container collapses to an empty message (the empty-state copy is in the products list template — verify).

## Storefront behaviour

- **Toggling from a product card** — the heart icon `_product-add-to-favorite` has `data-id="{$product->id}"` and `data-module="product-wishlist"`. The storefront's `product-wishlist` data-module posts to `add-to-wishlist` and flips the `active` class plus the label text (`sf.global.add.to.favorites` ↔ `sf.global.remove.from.favorites`).
- **Header dropdown** — the heart icon in the site header fetches `wishlist.menu` and displays a compact list.
- **Anonymous → logged-in merge** — when an anonymous visitor adds items and later logs in, the cookie-held wishlist is merged into the customer record (verify the exact merge timing).
- **Removal from the wishlist page** — clicking the active heart on a product card calls `add-to-wishlist/{id}` again; the controller toggles → product disappears from the grid (AJAX, no full reload, via `js-empty-on-ajax`).

## JavaScript behaviour

- `js-wishlist` — wrapper on the wishlist page's products container; flags the page as a wishlist context.
- `js-empty-on-ajax` — instructs the storefront framework to collapse the container to an empty-state when the last child is removed.
- `js-products-container` — generic products grid wrapper that the storefront JS targets for AJAX updates.
- `_product-add-to-favorite` with `data-module="product-wishlist"` — heart-icon toggle on every product card (in listings, on the product page, and on the wishlist itself).
- `js-wishlist-compact` with `data-module="wishlist-compact"` and `data-ajax-box="{route('site.account.wishlist.compact')}"` — the header dropdown panel.

## Customisations available to the merchant

- **Theme editor / product list module settings** — `listing_show_wishlist` flag in `$list_widget_settings` controls whether the heart icon appears on category / search / wishlist listings.
- **Heart icon styling** — pure CSS per theme.
- **Header dropdown** — included or omitted per theme (look for `wishlist/compact` partial in the header).
- The merchant cannot delete a customer's wishlist from admin (verify); they can only remove products globally.

## Theme variations

- Themes that bundle a compact header dropdown render the theme templates; minimal themes skip it.
- The wishlist page itself reuses the same product list partial as category pages, so visual differences come from each theme's product-card styling.
- A few themes show wishlist counts in a badge over the heart icon (verify which themes).

## Known issues / by-design vs bug

- Anonymous wishlists live in cookies — clearing cookies wipes the list. Customers should be encouraged to log in for persistence.
- `add-to-wishlist/{id}` is a TOGGLE, not an idempotent "add" — clients that call it twice end up with the product removed again.
- Removing the last item triggers `js-empty-on-ajax` to show the empty state without a full reload; if a theme's empty-state copy is missing the container looks visually empty.

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[compare]]

## Open questions

- Confirm the public URL of the wishlist page (`/wishlist` vs `/account/wishlist`) on the latest builds — the routes file shows the AJAX/menu endpoints but the canonical page lives under the customer-account routes.
- Confirm the merge behaviour when an anonymous wishlist is adopted by a customer at login.
- Confirm whether `listing_show_wishlist` is a per-module setting (Theme Editor) or a global storefront flag.
- Confirm the empty-state copy and selector used by `js-empty-on-ajax`.
