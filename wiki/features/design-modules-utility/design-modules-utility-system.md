---
type: feature
nav_path: "Design → Modules → Utility → System modules"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["System modules", "Vendors module", "Payment providers module", "Leasing module", "Authorize module", "Utilities module", "Page module", "Wishlist module", "Wishlist menu module", "Category properties module", "Модул вендори", "Системни модули"]
tags: [design, modules, storefront-customisation, system]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Utility modules — System

> Part of [[design-modules-utility]]. See the hub for the catalogue, editable modules, page-builder blocks, and storage / cache mechanics.

## Purpose

The system modules render automatically on the storefront and have **no merchant settings**. They do not appear as cards on the Modules screen. Trying to open their settings URL returns HTTP 404. The merchant configures the data behind them on a different admin surface — usually the relevant feature area (vendor catalogue, payment providers, customers admin, etc.).

This page catalogues each system module and points to the admin surface that actually controls it.

## Where to find it

Sidebar → **Design** → **Modules** — **none of the modules on this page appear there.** Instead the merchant manages each through the relevant feature surface listed below.

## What the merchant can do here

For every system module:

- They CANNOT open a settings panel on the Modules screen.
- They CAN influence what the module renders by editing the source data in the named admin surface.
- They CAN turn the module off only if the theme exposes a slot toggle in another module (e.g., `listing_show_wishlist` in `filters`) or if the underlying feature is uninstalled.

## Settings & fields

None of these modules has a settings panel — each is managed on its owning feature surface (see [[design-modules-utility-storage]] for why their URLs 404).

### `vendors` (`product.vendors`)

Renders the storefront's vendor / brand list page at `/vendors` (or the theme's equivalent route): each brand with a logo + name, click-through to that vendor's product listing. Vendor records (name, logo, description, URL slug, banner) are managed in the Vendors admin (Catalog → Vendors). If the list is empty, check vendors exist and are marked Active.

---

### `providers` (`payment.providers`)

Renders the row of payment-method icons in the footer / checkout (Visa, Mastercard, PayPal, etc.), pulled from the active configurations in [[settings-payment-providers]] (each provider has its own settings screen — see [[payment-providers]]). Enabling a new provider makes its icon appear automatically; no module configuration needed.

---

### `leasing` (`store.leasing`)

Renders credit / leasing badges + price calculators on product pages and checkout, reading from the active CREDIT-type payment providers (TBI Bank, Mokka, Klear, BNL, BNPL providers — see [[payment-providers]]). The calculator is inline on product pages and a "Leasing terms" link on checkout; customers can click through to the provider's pricing table. Each credit provider offers monthly installments above a configurable price threshold, configured per provider — e.g., [[payment-providers-tbi-bank]], [[payment-providers-mokka]], [[payment-providers-klear]], [[payment-providers-dsk-bnpl]], [[payment-providers-fibank-bnpl]], [[payment-providers-iute]]. If badges aren't showing, verify at least one credit provider is active AND the product's price exceeds that provider's minimum threshold.

---

### `authorize` (`user.authorize`)

Renders the login / register / forgotten-password / reset-password forms at the `/login`, `/register`, `/forgotten-password`, `/reset-password` routes — all customer authentication on the storefront. Account behaviour is controlled in the Customers admin: customer groups via [[customers-custom-groups]], registration custom fields (which are required, etc.) via [[customers-custom-fields]], and admin auth via [[settings-staff]]. If guests can buy without registering, `/login` is optional in the customer flow — the module still exists but the customer is not forced through it.

---

### `utilities` (`base.utilities`)

A largely invisible container / helper module: homepage rendering, "go back to home" redirects, customer-group lookups, and the homepage SEO title/description fallback supplied to other modules. Homepage SEO is set in [[settings-general]] (Store name + Default SEO title fields); customer group rules are in [[customers-custom-groups]]. System plumbing the merchant rarely needs to touch — if the homepage SEO title looks wrong, check [[settings-general]].

---

### `page` (`extra.page`)

Renders static merchant-created pages at `/page/{slug}` (About Us, FAQ, Privacy Policy, Delivery Info, etc.), pulling content by URL slug from [[marketing-landing-pages]] (Static page type) — the source of truth for page body, SEO metadata, and slug. If a page 404s, check it's published (not draft) and the slug matches the URL.

---

### `wishlist` (`wishlist.listing`)

Renders the logged-in-only saved-favourites listing page at `/site/account/wishlist`, where customers see every product they've saved. The wishlist is per-customer state; merchants can't edit it. The heart icon on product cards — controlled by `listing_show_wishlist` in the `filters` module ([[design-modules-utility-editable]]) — adds products. To hide the heart icon globally, turn `listing_show_wishlist` OFF in `filters` AND `show_wishlist` OFF in the productsDetails module ([[design-modules-products]]).

---

### `wishlistMenu` (`wishlist.menu`)

Renders the WISHLIST dropdown / count badge in the header — a heart icon with a counter of saved products, showing the latest N favourites (`limit` defaults to 10, set in theme config). Logged-out customers see an empty / hidden menu; the badge updates client-side as favourites change. To hide entirely, the theme must remove the slot — there's no admin toggle.

---

### `categoryProperties` (`product.categoryProperties`)

Adds category-property facets to product-listing pages — extra filter-sidebar checkboxes for category-specific properties (e.g., "Material: Cotton/Polyester/Wool", "Memory: 16GB/32GB/64GB"). Properties are defined per category in [[products-categories]] (Properties tab). The toggle `enable_category_properties` lives in the `filters` module ([[design-modules-utility-editable]]): ON renders the facets, OFF hides them. The count shown is capped by `category_properties_limit` (default 3) — set higher to show more.

## Business rules

### Why system modules have no editor card

System modules are injected as bare stubs that the platform never recognises as editable, so they never appear as cards on the Modules screen and force-opening their settings URL returns a clean 404. See [[design-modules-utility-storage]] for the full gating mechanics.

### One source of truth per module

The merchant configures system modules on the OWNING feature surface — never on the Modules screen. The mapping is:

| Module | Source of truth |
|--------|-----------------|
| `vendors` | Vendors admin (Catalog → Vendors) |
| `providers` / `leasing` | [[payment-providers]] + provider-specific settings screens |
| `authorize` | [[customers-custom-fields]], [[customers-custom-groups]], [[settings-staff]] |
| `utilities` | [[settings-general]] (store SEO + identity) |
| `page` | [[marketing-landing-pages]] (Static pages) |
| `wishlist` / `wishlistMenu` | Per-customer state; behaviour gated by `filters` module |
| `categoryProperties` | [[products-categories]] + `enable_category_properties` in `filters` module |

### Feature dependencies, not plan gates

System modules are not plan-gated at the module level; they depend on optional features:

- `leasing` requires at least one credit-type payment provider to be active.
- `categoryProperties` requires the active theme to advertise category-property support (most modern themes do).
- `wishlist` / `wishlistMenu` require the customer to be logged in to see content; the header icons may always render but lead to a login page otherwise.

If the underlying feature is not installed / configured, the module either self-hides or shows a placeholder pointing to the install URL.

### Theme exposes a different subset

Each theme decides which system-module slots it renders: a theme without a header slot won't render `wishlistMenu`, one without a vendor sidebar won't render the `vendors` link. The slot list is fixed by the theme — there's no admin toggle for system modules.

## Related

- [[design-modules-utility]] — hub.
- [[design-modules-utility-catalogue]] — full module list.
- [[design-modules-utility-editable]] — `filters` + `categoryProperties` interaction.
- [[design-modules-utility-storage]] — why opening a system module URL 404s.
- [[payment-providers]] — drives `providers` + `leasing`.
- [[settings-payment-providers]] — payment-provider configuration.
- [[settings-general]] — store SEO drives `utilities`.
- [[customers-custom-fields]] — drives `authorize`.
- [[customers-custom-groups]] — drives `authorize` + `utilities` behaviour.
- [[settings-staff]] — staff permissions.
- [[products-categories]] — category properties drive `categoryProperties`.
- [[products-favorite-products]] — wishlist context.
- [[marketing-landing-pages]] — static pages drive `page` module.

## Open questions

None — system modules have no merchant-editable surface area.
