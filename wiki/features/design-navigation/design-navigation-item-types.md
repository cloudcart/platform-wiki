---
type: feature
nav_path: "Design → Navigation → Item types"
route_name: admin.navigation.create.select
route_path: /admin/storefront/navigation/{group}/create-select
aliases: ["Navigation item types", "Menu item types", "Choose item type", "Link types", "Видове меню елементи"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Navigation — item types

> Part of [[design-navigation]]. See the hub for the other aspects (item fields, tree editing, menu groups, link resolution, side-effects).

## Purpose

When the merchant clicks **Add more** on either menu tree, the **Choose item type** side panel opens with one card per link type. The chosen type determines which picker field the Add form surfaces and how the menu item resolves to a storefront URL. This page catalogues the 12 item types and their pickers.

## Where to find it

Sidebar → **Design** → **Navigation** → **Add more** (on the Main or Footer tree). The picker is served at `/admin/storefront/navigation/{group}/create-select`; selecting a card routes to `/admin/storefront/navigation/{group}/create/{type}`.

## What the merchant can do here

In the **Choose item type** side panel the merchant picks one of the cards below; each opens a slightly different add-form whose picker field is listed in *Settings & fields*.

| Type | Card label | Use case |
|------|------------|----------|
| `url` | **Web link** | Link to an external website — *"Add link to an external web site"*. |
| `product` | **Link to a specific product** | The menu item redirects to one product detail page. |
| `category` | **Link to a specific category** | The menu item redirects to one product category. |
| `vendor` | **Link to specific vendor** | The menu item redirects to one Brand (vendor) page. |
| `blog` | **Link to a specific article category** | The menu item redirects to one blog category. |
| `article` | **Link to a specific article** | The menu item redirects to one blog article. |
| `page` | **Link to a specific static page** | The menu item redirects to one landing / static page (see [[marketing-landing-pages]]). |
| `section` | **Link to a specific store section** | The menu item redirects to a built-in storefront route (cart, profile, search, etc. — anything theme-defined). |
| `selection` | **Link to a specific Smart Collection** | The menu item redirects to one Smart Collection page. |
| `group` | **Group menu** | A header-only menu item that just groups child items into a dropdown — no link itself. |
| `mailchimp` | **Subscription for Newsletter** | The menu item opens the Newsletter (Mailchimp) signup pop-up. |
| `snippet` | **Integrate a snippet code** | The menu item is raw HTML / JS injected into the menu (any custom markup the merchant pastes). |

## What the merchant cannot do here

- Pick a type outside the 12-item whitelist — the server rejects with *"Invalid link type"*.
- See the `mailchimp` card on stores without the Newsletter / Mailchimp integration active — that card simply isn't rendered (verify). The integration itself is managed under [[apps-mailchimp]].

## Settings & fields

Each type surfaces exactly one picker field on the add-form. How that field then resolves to a storefront URL is on [[design-navigation-link-resolution]]; the shared fields (`name`, `parent_id`, `blank`, icon) are on [[design-navigation-item-fields]].

| Type | Picker field |
|------|--------------|
| `url` | **External address** text input (must validate as a URL). |
| `product` | **Product** autocomplete (searches by name). |
| `category` | **Product category** tree-select. |
| `vendor` | **Brand** autocomplete. |
| `blog` | **Article category** autocomplete. |
| `article` | **Article** autocomplete. |
| `page` | **Static page** dropdown of all pages. |
| `section` | **Store section** dropdown of theme-defined routes. |
| `selection` | **Collection** dropdown of all Smart Collections. |
| `group` | No picker — only a name (header / parent-only item). |
| `mailchimp` | No picker. |
| `snippet` | **Snippet code** textarea (raw HTML / JS, up to 12,000 characters). |

The 7 typed pickers (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`) save a `link_id` + `link_type` pair. The `url`, `section`, and `snippet` types save their own column value — see [[design-navigation-link-resolution]].

## Business rules

### Type whitelist — exactly 12 strings

The server accepts only `product`, `category`, `vendor`, `page`, `section`, `url`, `group`, `blog`, `article`, `selection`, `mailchimp`, `snippet`. Any other value returns *"Invalid link type"*.

### `group` type — header-only, no link

A **Group menu** item has no URL of its own; it exists purely to nest child items into a dropdown. Selecting it shows only a name field.

### `mailchimp` type — wires to the Newsletter pop-up

Selecting **Subscription for Newsletter** sets the item's internal module to `mailchimp`. On the storefront, clicking the item opens the Newsletter signup pop-up — the same pop-up driven by the `mailchimp.newsletter` module. The signup is managed under [[apps-mailchimp]].

### `snippet` type — raw HTML / JS up to 12,000 chars

Selecting **Integrate a snippet code** sets the item's internal module to `snippet` and surfaces a single textarea (up to 12,000 characters), rendered in place of the menu link on the storefront. There is no sanitisation — the merchant is trusted to write safe markup.

### `section` type — themes define which sections exist

The selectable storefront sections are theme-specific; each theme registers its own routed sections (Cart, Checkout, Account, Search, Wishlist, etc.). Selecting a section that no longer exists (e.g., after switching themes) returns *"Invalid link section"* on save. See [[design-navigation-link-resolution]] for how the route name persists.

## Related

- [[design-navigation]] — hub.
- [[marketing-landing-pages]] — landing pages selectable as `page` link type.
- [[marketing-blog-articles]] — blog articles selectable as `article` link type.
- [[products]] — products selectable as `product` link type.
- [[products-vendors]] — vendors selectable as `vendor` link type.
- [[products-smart-collections]] — collections selectable as `selection` link type.
- [[apps-mailchimp]] — Newsletter Mailchimp app; powers the `mailchimp` link-type pop-up.

## Open questions

- 📡 **`mailchimp` card visibility.** Whether the card renders unconditionally or is hidden on stores without the Mailchimp integration is unverified across themes. GraphQL-resolvable: query whether the Mailchimp integration is installed and configured on this merchant's store.
