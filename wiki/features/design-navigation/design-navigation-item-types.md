---
type: feature
nav_path: "Design → Navigation → Item types"
route_name: design.navigation
route_path: /admin/design/navigation
aliases: ["Navigation item types", "Menu item types", "Choose item type", "Link types", "Видове меню елементи"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---
# Navigation — item types

> Part of [[design-navigation]]. See the hub for the other aspects (item fields, tree editing, menu groups, link resolution, side-effects).

## Purpose

When the merchant clicks **Add link** on a menu's tab, a dialog headed "What should this menu item link to?" opens with one card per link type. The chosen type determines which picker field the **Add link** form surfaces and how the menu item resolves to a storefront URL. This page catalogues the 12 item types and their pickers.

## Where to find it

Sidebar → **Design** → **Navigation** → **Add link** (on the open menu's tab). The picker and the add form that follows it open on the same screen (`/admin/design/navigation`); neither has an address of its own.

## What the merchant can do here

In the "What should this menu item link to?" dialog the merchant picks one of the cards below; each opens a slightly different **Add link** form whose picker field is listed in *Settings & fields*.

| Type | Card label | Use case |
|------|------------|----------|
| `url` | **Web link** | Link to an external website — *"Add link to an external web site"*. |
| `product` | **Link to a specific product** | The menu item redirects to one product detail page. |
| `category` | **Link to a specific category** | The menu item redirects to one product category. |
| `vendor` | **Link to specific vendor** | The menu item redirects to one Brand (vendor) page. |
| `blog` | **Link to a specific article category** | The menu item redirects to one blog category. |
| `article` | **Link to a specific article** | The menu item redirects to one blog article. |
| `page` | **Link to a specific static page** | The menu item redirects to one landing / static page (see [[marketing-landing-pages]]). |
| `section` | **Link to a specific store section** | The menu item redirects to a built-in storefront page (cart, account, contacts, etc.) or one an app adds, such as the withdrawal page. |
| `selection` | **Link to a specific Smart Collection** | The menu item redirects to one Smart Collection page. |
| `group` | **Group menu** | A header-only menu item that just groups child items into a dropdown — no link itself. |
| `mailchimp` | **Subscription for Newsletter** | The menu item opens the Newsletter (Mailchimp) signup pop-up. |
| `snippet` | **Integrate a snippet code** | The menu item is raw HTML / JS injected into the menu (any custom markup the merchant pastes). |

## What the merchant cannot do here

- Pick a type outside the 12-item whitelist — the server rejects with *"Invalid link type"*.
- Hide the `mailchimp` card — the dialog lists all 12 cards on every store, whether or not the Newsletter / Mailchimp integration is active. The integration itself is managed under [[apps-mailchimp]].

## Settings & fields

Each type surfaces exactly one picker field on the add-form. How that field then resolves to a storefront URL is on [[design-navigation-link-resolution]]; the shared fields (`name`, `parent_id`, `blank`, icon) are on [[design-navigation-item-fields]].

| Type | Picker field |
|------|--------------|
| `url` | **External link address** text input: a full address with `https://`; a bare path such as `/withdrawal` is rejected. |
| `product` | **Select product** autocomplete (searches by name). |
| `category` | **Select category** search-select. |
| `vendor` | **Select vendor** autocomplete. |
| `blog` | **Select blog** autocomplete. |
| `article` | **Select article** autocomplete. |
| `page` | **Select page** dropdown of all pages. |
| `section` | **Theme section** dropdown of store sections (see the rule below). |
| `selection` | **Select product selection** dropdown of all Smart Collections. |
| `group` | No picker — only a **Group name** (header / parent-only item). |
| `mailchimp` | No picker. |
| `snippet` | **HTML snippet** textarea (raw HTML / JS, up to 12,000 characters). |

The 7 typed pickers (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`) save a `link_id` + `link_type` pair. The `url`, `section`, and `snippet` types save their own column value — see [[design-navigation-link-resolution]].

## Business rules

### Type whitelist — exactly 12 strings

The server accepts only `product`, `category`, `vendor`, `page`, `section`, `url`, `group`, `blog`, `article`, `selection`, `mailchimp`, `snippet`. Any other value returns *"Invalid link type"*.

### `group` type — header-only, no link

A **Group menu** item has no URL of its own; it exists purely to nest child items into a dropdown. Selecting it shows only a **Group name** field.

### `mailchimp` type — wires to the Newsletter pop-up

Selecting **Subscription for Newsletter** sets the item's internal module to `mailchimp`. On the storefront, clicking the item opens the Newsletter signup pop-up — the same pop-up driven by the `mailchimp.newsletter` module. The signup is managed under [[apps-mailchimp]].

### `snippet` type — raw HTML / JS up to 12,000 chars

Selecting **Integrate a snippet code** sets the item's internal module to `snippet` and surfaces a single **HTML snippet** textarea (up to 12,000 characters), rendered in place of the menu link on the storefront. There is no sanitisation — the merchant is trusted to write safe markup.

### `section` type — which store sections are listed

The **Theme section** list is the same on every theme: home, cart, contacts, blog, brands, categories and bundles; unless the store's customer access is guests only (verify), also the account pages (profile, files, orders, payments, addresses, wishlist), login and register; plus pages apps add — **Withdraw from contract** (`/withdrawal`, „Отказ от договора“ in a Bulgarian admin) from [[apps-aftercare]] and the gift card page from [[apps-gift-card]]. App entries are listed on every store, installed or not; the link leads to a 404 page while the app is not active. A section not on the list is rejected with *"Invalid link section"*. See [[design-navigation-link-resolution]] for how the route name persists.

## Related

- [[design-navigation]] — hub.
- [[marketing-landing-pages]] — landing pages selectable as `page` link type.
- [[marketing-blog-articles]] — blog articles selectable as `article` link type.
- [[products]] — products selectable as `product` link type.
- [[products-vendors]] — vendors selectable as `vendor` link type.
- [[products-smart-collections]] — collections selectable as `selection` link type.
- [[apps-mailchimp]] — Newsletter Mailchimp app; powers the `mailchimp` link-type pop-up.
- [[aftercare-settings-setup]] — adding the withdrawal page to a menu.

## Open questions

- 📡 **`mailchimp` item without the integration.** The card is always offered; what the storefront item does when the Mailchimp integration is not set up is unverified. GraphQL-resolvable: query whether the Mailchimp integration is installed and configured on this merchant's store.
