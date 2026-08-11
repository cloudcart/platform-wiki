---
type: storefront-page
route_name: cart.list
route_path: /cart/{cart_key}
themes_using: [all]
tags: [storefront, cart, drawer, compact, rendering]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[storefront-cart]]. See the hub for the other aspects (cart actions / mutations, merchant customisation + known issues).

# Cart — surfaces & rendering

## Purpose

Documents the **three render surfaces** the cart controller serves and what the customer sees on each, plus the per-line markup shared between them and how themes vary. All three render from the same `Cart` model instance and stay in sync via AJAX reloads — see [[storefront-cart-actions]] for the reload pipeline that keeps them consistent.

## URL & route

The render (GET) routes for the three surfaces:

- **Cart full page** — `cart.list` — `/cart/{cart_key}` (`cart_key` is a 32+-char alphanumeric key — guests get a fresh one per browser; logged-in customers re-use their own).
- **Cart bare entry** — `cart.site` — `/cart` (redirects to `/cart/{cart_key}` with a freshly-issued key when the customer has no cart yet).
- **Cart drawer** — `cart.panel` — `/cart/panel/{cart_key?}` (AJAX-only, returns the panel HTML); the edit variant is `cart.panel.edit` — `/cart/panel-update/{cart_key}`.
- **Cart compact (header)** — `cart.compact` — `/cart/compact` (AJAX-only, returns the header HTML).
- **Cart-summary fragments** — `cart.summary` (`/cart/summary`), `cart.total-formatted` (`/cart/total-formatted`).

**Render-route middlewares**: `uuid_generate`, `subscriber_uuid`. (POST-mutation middlewares are on [[storefront-cart-actions]].)

## How it loads

1. The bare `/cart` route immediately redirects to `/cart/{freshKey}` so the customer's browser holds a stable URL.
2. The cart instance resolves the current cart — for guests by the `_cart_key` cookie, for logged-in customers by their account. If both exist they are merged (see [[cart-vs-order-lifecycle]]).
3. If the customer arrived from a **shared cart link** (the `{key}` in the URL differs from the resolved instance key), the controller merges that cart and redirects to the resolved cart's canonical URL.
4. The Smarty template `cart.full` renders — under `flair`, this is the theme templates, which captures the cart HTML and (in non-AJAX mode) wraps it in the layout + breadcrumb. In AJAX mode it returns the fragment only.
5. **The three AJAX wrappers** (the canonical refresh selectors the storefront AJAX pipeline uses to repopulate cart HTML after any mutation):
   - Full-page wrapper: `data-ajax-box="{route('cart.list', $cc_cart_key)}" data-module="cart" data-effect="populate"`.
   - Drawer wrapper: `js-cc-cart-panel data-ajax-box="{route('cart.panel', $cc_cart_key)}" data-module="cart" data-effect="replace"`.
   - Compact wrapper: `_cart-compact data-ajax-box="{route('cart.compact')}" data-module="cart-compact"`.

## What the customer sees

### Cart full page

- Breadcrumb: Home → "Cart".
- Header bar: page title "Shopping cart" + "Clear cart" link (`js-cart-clear`).
- Left column (col-md-8): cart product list.
- Right column (col-md-4, `_cart-sidebar js-checkout-sidebar`):
  - **Cart totals** — subtotal, applied discounts, applied cart-rule modifications, free-shipping-amount-left message, total.
  - **Submit button** — the theme templates ("Continue to checkout" or equivalent).
  - **Optional text module** (`checkoutText` — Theme Editor) below the summary.
- **Empty state** — `sf.module.cart.nfy.cart_is_empty` notice + nothing else.

### Each cart line (from the theme templates and `panel.tpl`)

- Product image (300x300 thumb, linked to product page).
- Product name (clickable to product page).
- Parameters (variant attributes — size, color, etc.).
- Product **options** (configured option values; can be file uploads — clickable to download).
- Per-line **discount display**, **discount-code display**, **discount modifications** (from `_global/templates/checkout/include/discount_display.tpl` etc.).
- Weight (when set).
- **Bundle sub-products** (when the line is a bundle and the sub-product has `setting('visible_cart')` on).
- **Quantity stepper** — input with `data-uicontrol="spinner"` (or `spinnerMask` in the drawer); cap is `product_quantity` when stock-tracked + `continue_selling=no`. Out-of-stock-but-still-in-cart lines show a glyph + the `sf.module.cart.product.nfy.out_of_stock` tooltip.
- **Line total** — uses the most-discounted price path: `getTotalPriceWithOptionsAfterDiscountsWithModification` when discounts apply, falling back through `…AfterGlobalDiscountWithModification` / `…WithModification` / `…WithOptions`.
- **Remove icon** (`js-cart-product-remove`) — clicks AJAX-delete the line.
- The whole line has `id="variant-{$product->variant_id}"` and the panel adds `data-key="{$product->key}"` so the JS can target specific lines.

### Cart drawer (panel)

- Right-side slide-over (the `data-ajax-panel` mechanism in [[storefront-architecture]]).
- "Clear cart" link at the top.
- Same line format as above (with `cc-cart-product-` class prefix instead of `_cart-product-`).
- Footer: totals + "Continue to checkout" button.
- Includes a `summary_disable` hidden input that suppresses the right-column sidebar when re-loaded inside the panel.

### Cart compact (header bubble)

- Cart icon + bubble count (`bubble_count` — sum of quantities).
- Subtotal label.
- When clicked: if `compact_cart_panel` setting is on → opens the cart drawer (`/cart/panel/...`); otherwise → navigates to `/cart/{key}` (full page). See [[storefront-cart-customisation]] for the settings.
- Hovering exposes a dropdown of current cart items (`_cart-compact-dropdown` containing the theme templates).
- The compact element is **completely hidden** when `setting('show_cart')` is `no` OR when the plan doesn't include `checkout`.
- Empty cart → renders just the icon with the label "Shopping cart" (no bubble, no dropdown).

## Storefront behaviour

Surface-level behaviour only: each surface is a fragment reloaded from its own `data-ajax-box` URL after any cart mutation, so updating one surface updates all three in a single round-trip. The mutations themselves (add / update / remove / clear / discount-code / checkout) live on [[storefront-cart-actions]].

## JavaScript behaviour

Surface-targeting hooks (the full hook + event inventory is on [[storefront-cart-actions]]):

- `[data-ajax-box="{url}"]` — selector + URL pair the storefront AJAX pipeline uses to repopulate a fragment.
- `[data-module="cart"]` — every full-cart-page wrapper.
- `[data-module="cart-compact"]` — every header-bubble wrapper.
- `[data-effect="populate"]` vs `[data-effect="replace"]` — whether to populate inside the wrapper or replace the wrapper.
- `[data-ajax-panel="true"]` — opens a route inside a side panel instead of navigating.
- `.js-cc-cart-panel` — the drawer wrapper; reloaded after each mutation.
- `.js-checkout-sidebar` — the page-cart's right-side summary (sticky-scroll handler).
- `[data-uicontrol="spinner"]`, `[data-uicontrol="spinnerMask"]` — quantity-stepper modules; `[data-spinner-max="{n}"]` carries the stock cap.

## Customisations available to the merchant

The surfaces respond to several settings (full detail on [[storefront-cart-customisation]]):

- `show_cart` — global kill-switch for the header cart bubble; when `no`, no cart UI shows anywhere.
- `compact_cart_panel` — clicking the header bubble opens the drawer instead of navigating to `/cart`.
- `action_after_add_to_cart` — whether Add-to-cart opens the drawer, redirects to `/cart`, or stays silent.
- Theme Editor → Cart module → "Checkout text" (`checkoutText`) — free-form HTML below the totals summary.

## Theme variations

- Most themes redefine `cart/full.tpl` and `cart/compact.tpl` (in their own the theme's own override folder). All themes reuse `_global/templates/cart/include/full.tpl` and `_global/templates/cart/include/panel.tpl` for the actual line markup unless they explicitly override those too.
- Themes vary on:
  - Whether the header cart bubble has a hover-dropdown (compact preview) or only a click-to-open behaviour.
  - Where the "Continue to checkout" CTA sits (sticky bottom, in the sidebar, or below each line).
  - Whether the discount-code field is on the cart page or only on the checkout page.
  - Whether the empty-state shows recommended products / "popular" carousel.
- The `_global/templates/cart/cart.tpl` file itself is empty (0 lines) — the cart entry-point is the per-theme `full.tpl`.

## Known issues / by-design vs bug

- **The cart drawer and the cart page can show different `summary` states** — the drawer's `summary_disable` hidden input suppresses the side summary when the drawer is reloaded inside itself; this is intentional to avoid double-rendering the totals block in the slide-over. By design.
- **Compact bubble hidden on catalogue-only sites** — `show_cart=no` (or a plan without `checkout`) hides the bubble everywhere; this is the merchant's global kill-switch for the cart UI. By design. See [[storefront-cart-customisation]].

## Related

- [[storefront-cart]] — hub.
- [[storefront-architecture]] — request lifecycle, AJAX-pipeline, `data-ajax-box` / `data-module` conventions, the slide-over panel mechanism.
- [[product-detail]] — where Add-to-cart originates.
- [[cart-vs-order-lifecycle]] — Cart entity lifecycle + guest-merge semantics.
- [[settings-cart]] — `show_cart`, `compact_cart_panel`, `action_after_add_to_cart`.

## Open questions

None.
