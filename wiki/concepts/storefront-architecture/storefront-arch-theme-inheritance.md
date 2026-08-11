---
type: concept
nav_path: "Concept → Storefront architecture → Theme inheritance"
aliases: ["Theme inheritance", "Storefront theme inheritance", "themes/_global", "Global template fallback", "Per-file template override", "Theme template fallback"]
tags: [storefront, smarty, themes, inheritance, templates, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, the search index read-side, JS bundles, Smarty plugins, CSS assets, caching).

# Storefront — theme inheritance

## Definition

When the storefront renders a Smarty template, the view finder looks for the file under the merchant's active theme first, then falls back to a shared library under the theme templates if the theme hasn't overridden it. The override is **per-file**: a theme that wants to customise only the cart drawer overrides `cart/cart.tpl` and leaves `cart/include/compact.tpl` to fall through to `_global`.

The shared the theme templates directory is a fully-stocked default theme — every Smarty page the storefront can render has a `_global` version. A new theme is, in practice, a directory that selectively redresses parts of this default (typically home, header, footer, product listings) and inherits the rest (cart, checkout, customer area, payments).

This is why **checkout looks consistent across themes** — most themes do NOT override `checkout/*.tpl`, so the multi-step checkout flow has the same structure on every store, with only theme-driven colour and typography differences.

## Scope

Covered:

- The per-file lookup order: `themes/<theme>/templates/<file>` → `themes/_global/templates/<file>`.
- What lives under the theme templates (the full shared library).
- The parallel the theme templates tree of non-template fragments.
- The anatomy of a new theme directory.
- The `Template` registration row in `cc_gate.templates` (verified — 71 active rows).

Not covered here:

- The per-theme JS bundle composition — see [[storefront-arch-js-bundles]].
- The per-theme CSS bundle + Theme Editor variable substitution — see [[storefront-arch-css-assets]].
- The per-merchant override layer (Theme Editor variables, Custom CSS/JS) — see [[theme-customization-layers]].
- The Themes catalogue and install flow — see [[design-themes]].

## Contrasts

- **Per-file override vs per-directory override** — override is at file granularity. A theme overriding `cart/cart.tpl` does not have to override `cart/include/compact.tpl`. The fall-through pattern keeps cart-and-checkout behaviour platform-controlled by default.
- **Theme override vs per-merchant override** — the **theme** is the file-system layer (merchants don't edit `.tpl` files). The **per-merchant override** is the [[theme-customization-layers]] stack — Theme Editor variables, Custom CSS/JS — which leave the theme files untouched.
- **the theme templates vs the theme templates** — `templates/` holds Smarty `.tpl` files that participate in the inheritance lookup. `global-theme/` is a parallel tree of non-template fragments (crossSell, upSell, dependancies, discounts, exceptions, metatags, product, stores) that themes can include but that are NOT part of the per-file override lookup.

## Where it applies

Every Smarty render on the storefront goes through this lookup:

- Catalogue: home, category, product detail, product list, search, tag, vendor, selection, showcase, bundles.
- Cart and checkout: every step.
- Customer area: account, orders, addresses, wishlist, auth.
- Static: page-builder pages, blog, contacts.
- Embedded surfaces: `/embed/product/{id}`, `/embed/checkout`, `/checkout-link/{variant_id?}`, `/restore-abandoned/...`, `/tracking/{hash}`.
- Modules and partials emitted on any of the above.

## How it works

### The view-finder lookup order

When a Smarty `{include file=".../foo.tpl"}` or a controller-driven the platform code is evaluated, the view finder searches in this order:

1. the theme's own override — the merchant's active theme.
2. the theme templates — the shared fallback library.

The first match wins. Override is per-file, not per-directory: a theme that wants to customise only the cart drawer overrides `cart/cart.tpl` and leaves `cart/include/compact.tpl` to fall through to `_global`.

### What lives in the theme templates

The shared fallback library (every theme inherits from this):

- **Cart** — `cart/cart.tpl` (cart full page) + `cart/include/` (`compact.tpl`, `panel.tpl`, `full.tpl`, `bundle-details.tpl`, `cartItemPrice.tpl`, `total-formatted.tpl`, `email-unconfirmed.tpl`).
- **Checkout** — `checkout/express.tpl` (express checkout) + `checkout/steps/` (`authorize.tpl`, `shipping-address.tpl`, `shipping.tpl`, `billing-address.tpl`, `payment.tpl`, plus per-step subdirectories `edit/`, `empty/`) + `checkout/layout/` (`header.tpl`, `footer.tpl`) + `checkout/return/order/` (post-payment screens) + `checkout/include/` (logo, terms, GDPR, discount display, summary).
- **Customer** — `customer/account.tpl` + `customer/auth.tpl` + `customer/address/` (`form.tpl`, `_form.tpl`, `list.tpl`).
- **Product** — `product/categories.tpl` + `product/options/` + `product/discounts/` + `product/filter/` + `product/embed/` + `product/bundle/` + `product/custom_filter/` + `product/quantity-select/` + `product/rating/`.
- **Payments** — `payments/` (`fusion_pay.tpl`, `iute.tpl`, `klear.tpl`) — payment-provider partials.
- **Draft order** — `draft_order/` (`draft_order.tpl` + steps + include) — admin-created draft order checkout.
- **Form components, geo zone, other, upsell** — `form-components/`, `geo_zone/`, `other/`, `up_cross_sell_preview.tpl`.

And under the theme templates (a parallel tree of non-template fragments): `crossSell/`, `upSell/`, `dependancies/`, `discounts/`, `exceptions/`, `metatags/`, `product/`, `stores/`.

### Anatomy of a new theme

A new theme is a `themes/<slug>/` directory with:

- `templates/layout/header.tpl` + `templates/layout/footer.tpl` + per-page entry templates.
- `templates/headers/`, `templates/footers/`, `templates/products/`, `templates/blog/`, `templates/home/`, `templates/cart/` (optional override), `templates/modules/`, `templates/error.tpl`.
- `assets/scripts/global.js` (source for the theme's JS bundle — see [[storefront-arch-js-bundles]]).
- `assets/styles/theme.css` (the Theme-Editor token file — see [[storefront-arch-css-assets]]).
- `grunt/` + `gruntfile.js` + `package.json` + the theme templates (the per-theme build pipeline).
- A `Template` registration row in `cc_gate.templates` with `mapping=<slug>`, `in_dev=0`, `price=<int|null>` (verified — 71 active rows at the time of writing).

The minimum overrides for a workable new theme are the home page + header + footer + product detail + product card. Everything else can fall through to `_global` and still work.

### Why most themes don't override checkout

A theme overriding `checkout/*.tpl` is opting out of platform-controlled checkout behaviour — including form-submit hooks, payment-method rendering, GDPR consent display, discount-code input, summary totals. Themes usually leave checkout to `_global` so:

- Cross-theme behaviour is consistent (a customer sees the same checkout structure on every CloudCart store).
- Platform engineering can patch checkout in one place and every theme benefits.
- Cart-and-checkout regressions caused by theme customisation are rare.

A theme that overrides checkout must carry the override forward on every platform update — see [[storefront-known-issues]] for cases where this has caused regressions.

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-request-lifecycle]] — the request step that invokes the view finder.
- [[storefront-arch-js-bundles]] — per-theme JS bundle that pairs with the templates.
- [[storefront-arch-css-assets]] — per-theme CSS bundle + `theme.css` token file.
- [[theme-customization-layers]] — the 3-layer per-merchant customisation stack.
- [[design-themes]] — Themes catalogue, install, switch.
- [[storefront-themes-catalog]] — sibling concept: the catalogue of themes available.
- [[storefront-known-issues]] — sibling concept: cross-theme storefront issues.
- [[checkout-flow]] — checkout state machine that `checkout/*.tpl` renders.

## Open Questions

- **Whether platform engineering keeps a "minimum required overrides" checklist** for new themes, or whether the contract is truly "whatever `_global` emits" — verify.
- **Whether any storefront route bypasses the view-finder lookup** and reads templates directly from a fixed path — verify.
