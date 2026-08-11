---
type: concept
nav_path: "Concept → Storefront architecture → JS bundles"
aliases: ["Storefront JS bundles", "Per-theme JS", "scripts.min.js", "js hook classes", "cc.* events", "Storefront jQuery", "Theme JS pipeline", "cc.variant.changed", "cc.ajax.reload"]
tags: [storefront, javascript, jquery, themes, events, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, theme inheritance, the search index read-side, Smarty plugins, CSS assets, caching).

# Storefront — JS bundles and conventions

## Definition

Every storefront theme ships **its own compiled JS bundle** at the theme's own override. There is **no shared platform-level storefront JS file** — the cross-theme contract is conventions, not code:

- **`.js-*` hook class names** that the JS binds to (e.g., `.js-add-to-cart`, `.js-quantity-input`, `.js-filter-list`).
- **`cc.*` custom events on `document`** as a cross-component messaging bus (e.g., `cc.variant.changed`, `cc.filters.filters.after`, `cc.ajax.reload`).
- **jQuery 3.x** as the framework of choice — each theme bundles its own copy.

The contract between template and JS is the hook class set: templates expose interactive surfaces by adding `.js-*` classes; the bundle binds behaviour to them on page load. A theme is free to use different class names — but the platform's shared `_global` templates assume the most common patterns, so a theme that doesn't override the cart template inherits the hooks `_global` emits, and the theme's JS must bind to those for the cart to work.

## Scope

Covered:

- How the per-theme bundle is composed (jQuery 3.x + theme code + third-party plugins).
- The `.js-*` hook-class convention + observed examples.
- The `cc.*` custom-event bus + the verified storefront event vocabulary (cart / product / checkout / account / content / generic) and the server-side dispatch mechanism.

Not covered here:

- The CSS bundle and Theme Editor variable substitution — see [[storefront-arch-css-assets]].
- The Smarty plugin catalogue available in `.tpl` files — see [[storefront-arch-smarty-plugins]].
- Theme inheritance for templates — see [[storefront-arch-theme-inheritance]].
- The merchant's Custom CSS/JS injection layer — see [[design-custom-assets]] and [[theme-customization-layers]].

## Contrasts

- **Per-theme JS bundle vs shared platform bundle** — every theme ships its own `js/scripts.min.js`. There is **no shared platform-level storefront JS file**. Two CloudCart stores on different themes ship two different jQuery binaries to the browser cache.
- **Conventions vs contracts** — `.js-*` class names and `cc.*` events are conventions, not hard contracts. A theme is free to deviate, but the shared `_global` templates assume the most common patterns. Anything that needs to behave identically across themes (GA tracking pixels, `cc-analytics` setup) is injected from the platform's global head partial, not from theme JS.
- **Theme JS vs Custom JS** — the theme JS is shipped by the theme author and compiled into the bundle. The merchant's [[design-custom-assets]] Custom JS is rendered verbatim into the page head and runs in the same jQuery world but cannot modify the bundle.

## Where it applies

- Every interactive surface on every storefront page — Add-to-cart, quantity steppers, filters, tabs, carousels, sliders, sticky headers, mobile navigation, AJAX listing reloads, cart drawer, wishlist drawer, search autosuggest.
- Cross-theme integrations and apps that listen for `cc.*` events to react to customer actions.
- The platform's analytics setup script that fires alongside theme JS but is platform-managed, not theme-managed.

## Bundle composition

Each theme's `scripts.min.js` includes:

- **A copy of jQuery 3.x** — bundled per theme, not shared across themes. Each theme version-pins independently (verify whether older themes still ship jQuery 1.x / 2.x).
- **Theme-specific custom code** — the interaction behaviour for that theme (navigation, sidebars, tabs, carousels, sticky header, etc.).
- **Third-party plugins** the theme depends on — typically a cookies helper, a modal, Swiper or a comparable carousel (OwlCarousel on older themes), jQuery UI on a few.

## The `.js-*` hook-class convention

The bundle's public contract with templates is the set of `.js-*` hook class names that the JS binds to. Templates expose interactive surfaces by adding these classes — for example, `<button class="js-add-to-cart" data-variant-id="123">Add</button>` is the contract between template and JS.

**Common `.js-*` hook conventions observed across themes** (the exact names vary per theme — verify against the specific theme):

- **Navigation**: `.js-navigation-hamburger`, `.js-navigation-hamburger-dropdown`, `.js-nav-mobile`, `.js-nav-mobile-backdrop`, `.js-nav-mobile-button`, `.js-categories-menu`, `.js-close-dropdown`.
- **Cart and add-to-cart**: `.js-addtocart-actions`, `.js-cart-add`, `.js-add-to-cart`.
- **Quantity steppers**: `.js-quantity-input`, `.js-quantity-plus`, `.js-quantity-minus`.
- **Product display**: `.js-product-details-container`, `.js-product-details-sidebar`, `.js-product-fixed`, `.js-product-fixed-treshold`, `.js-product-share`, `.js-products-box`.
- **Filters**: `.js-filter-list`, `.js-filter-category-list-toggle`, `.js-filter-category-property-toggle`.
- **Tabs**: `.js-tabs`, `.js-tabs-link`, `.js-tab`, `.js-faq-list-item`, `.js-faq-list-item-title`.
- **Carousels and showcases**: `.js-blog-showcase`, `.js-blog-showcase-next`, `.js-blog-showcase-prev`, `.js-showcase-brands1`, `.js-showcase-brands2`, `.js-showcase-categories`, `.js-showcase-product-{1,3,4}`.
- **Header**: `.js-header-fixed`, `.js-header-bar-inner`, `.js-search-form-wrapper`, `.js-search-button`.
- **Sidebars**: `.js-sidebar`, `.js-sidebar-ajax`, `.js-sidebar-box`, `.js-fixed-sidebar`, `.js-fixed-sidebar-container`, `.js-sidebar-toggler`.
- **Misc**: `.js-to-top`, `.js-collapse-load-more`, `.js-back`, `.js-button-share`, `.js-promo-bar-remove`, `.js-request-status`, `.js-order-details-button`, `.js-nolink`, `.js-form-submit-ajax`, `.js-modal-open`.

These are **conventions, not contracts** — a theme is free to use different class names, but a theme that doesn't override the cart template inherits the hooks `_global` emits, and the theme's JS must bind to those for the cart to work.

## `cc.*` custom events — the cross-component messaging bus

Storefront components coordinate through `cc.*` custom events on `document`. **Most are dispatched server-side**: a storefront AJAX response carries an `events` array (built in the `Site\*` controllers — cart, account, checkout, etc.) that the storefront JS replays as `$(document).trigger(<event>, [payload])`. A few are fired directly in theme JS (the variant picker, filters, the cart spinner). So the authoritative source is the backend `'events' => [...]` arrays plus the `_global` theme triggers — **not** purely an emergent per-theme convention. (This is why reading a `.tpl` template alone misses most events — they arrive in the AJAX response.)

The verified storefront vocabulary, by area:

- **Cart** — `cc.cart.product.addToCart` (+ the `.disable-panel` namespaced variant cross-sell / up-sell use to add **without** opening the drawer), `cc.cart.product.updated`, `cc.cart.product.removed`, `cc.cart.product.deleted`, `cc.cart.updated`, `cc.cart.open.checkout`, `cc.cart.compact.spinner` (drawer loading spinner), `cc.item_added_to_cart`, `cc.addToCart.product.added`.
- **Product** — `cc.product.details.init`, `cc.variant.changed` (variant pick → price / gallery / stock badge), `cc.countdown.ended` (countdown discount), `cc.discount_accepted`.
- **Checkout** — `cc.checkout.step`, `cc.checkout.user.{shipping,billing}.address.{added,edited}`, `cc.shipping_provider_changed`, `cc.place.change` / `cc.place.city-selected` (delivery-place / office picker), plus order-state signals `cc.status_{completed,pending,processed,refunded,requested,chargebacked}`, `cc.order_payment_sync_success`, `cc.order_payment_refund_success`.
- **Account / customer** — `cc.user.sign.in` / `cc.guest.sign.in`, `cc.customer.update`, `cc.user.details.updated`, `cc.details_changed`, `cc.password_changed` / `cc.password_is_reset`, `cc.address_added` / `.edited` / `.removed`, `cc.default_address_changed`, `cc.user.address.{removed,setDefault}`, `cc.user.confirmationSent`, `cc.email_confirmation_link_sent_to_mail_address`.
- **Content** — `cc.contact.form.sent` / `cc.contact_request_sent`, `cc.submit.review`, `cc.blog.article.comment.posted`, `cc.comment_posted` / `cc.comment_posted_pending_moderation`.
- **Filters & generic UI** — `cc.filters.filters.after`, `cc.category-properties.after` / `.successAjax`, `cc.ajax.success` / `cc.ajax.reload` / `cc.ajax.error` (the storefront AJAX form lifecycle), `cc.overlay.hide`.

A theme reacts by listening on `document`; a module / integration pushes UI changes by triggering one. Themes MAY emit additional theme-specific events beyond this core set.

Anything that MUST behave identically across themes (analytics setup, GDPR consent banner script, the `cc-analytics` payload) is injected from the platform's global head partial, outside the theme bundle.

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-request-lifecycle]] — emits the bundle URL into the page.
- [[storefront-arch-theme-inheritance]] — templates that the JS binds to.
- [[storefront-arch-css-assets]] — paired CSS bundle.
- [[storefront-arch-caching-invalidation]] — bundle URL is cache-busted by `?<last_build>`.
- [[design-custom-assets]] — Custom JS injection that runs alongside the theme bundle.
- [[theme-customization-layers]] — the 3-layer customisation stack including Custom JS.

## Open Questions

- **The exact set of `.js-*` hook class names that every theme MUST implement** is not centrally documented. A theme author building a new theme has to read the `_global` templates plus several reference themes to infer the contract. Worth confirming whether platform engineering has a checklist (verify).
- ✅ Resolved: the core `cc.*` storefront vocabulary is catalogued above, sourced from the `Site\*` controllers' AJAX-response `events` arrays + the `_global` theme triggers (events are mostly **server-dispatched**, not theme-emergent). Individual themes MAY still add their own theme-specific events on top of this core set.
- **Per-theme JS minor-version drift on jQuery** — each theme bundles its own jQuery copy. The platform's policy on which jQuery version themes should ship is not documented. Worth checking whether old themes still ship jQuery 1.x / 2.x (verify).
