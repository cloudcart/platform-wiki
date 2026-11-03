---
type: feature
nav_path: "Design → Navigation → Link resolution"
route_name: admin.navigation.list
route_path: /admin/storefront/navigation/{group?}
aliases: ["Navigation link resolution", "Menu URL resolution", "Menu active state", "Section route name", "URL verbatim", "Резолюция на меню връзки"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Navigation — link resolution & active state

> Part of [[design-navigation]]. See the hub for the other aspects (item types, item fields, tree editing, menu groups, side-effects).

## Purpose

This page explains how each menu item resolves to a real storefront URL at render time, the three different persistence strategies (typed `link_id`, verbatim `url`, route-name `section`), and how the highlighted "active" state is computed per request. It complements [[design-navigation-item-types]], which lists the picker per type; this page covers what is stored and how it later resolves.

## Where to find it

This is render-time behaviour on the storefront, configured implicitly when the merchant picks an item type and target under Sidebar → **Design** → **Navigation**. The same admin route `/admin/storefront/navigation/{group?}` also serves both the full-page HTML and the per-tree AJAX data (see *How it works*).

## What the merchant can do here

- Pick a typed target (Product, Category, Brand, Blog category, Article, Static page, Smart Collection) and rely on the storefront to resolve the current slug automatically — even if the slug changes later.
- Pick a **Store section** and rely on it following the theme's current URL for that route.
- Paste an **External address** that is stored and rendered exactly as typed.

## What the merchant cannot do here

- Have an external `url` item auto-update if the destination site later changes its address — verbatim URLs are frozen until the merchant edits and re-saves.
- Configure the active-state highlight manually — it is computed automatically per request.

## Settings & fields

There are no extra fields here beyond the per-type picker on [[design-navigation-item-types]]. The relevant stored values are: `link_type` + `link_id` for the 7 typed pickers, the `url` column for external links, the `route` (route name) for `section` items, and `widget_text` for `snippet` items.

### Storefront URL per type

| Type | Storefront URL |
|------|----------------|
| `url` | The exact URL typed (e.g., `https://google.com`). |
| `product` | `/product/<product-slug>`. |
| `category` | `/category/<category-slug>`. |
| `vendor` | `/brand/<vendor-slug>` (storefront `site.vendor.view`). |
| `blog` | `/blog/category/<blog-slug>`. |
| `article` | `/blog/article/<article-slug>`. |
| `page` | `/page/<page-slug>`. |
| `section` | The route's path (e.g., `/cart`, `/account`, `/search`). |
| `selection` | `/selection/<collection-slug>`. |
| `group` | No URL (header / parent-only item). |
| `mailchimp` | No URL — opens the Newsletter signup pop-up. |
| `snippet` | No URL — the snippet HTML / JS is rendered in place of the menu item. |

## Business rules

### Typed pickers resolve a slug at render time

The 7 typed pickers (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`) save a `link_id` + `link_type` pair, NOT a frozen URL. The storefront resolves the linked entity's current slug on each request, so renaming a product / category / brand automatically updates the menu link with no merchant action.

### `url`-type links are saved verbatim

The `url` type saves the typed URL verbatim into the `url` column. If the merchant later changes the linked external site's address, the menu item is NOT auto-updated — the merchant must edit and re-save.

### `section` type stores the route name, not the path

For `section`-type items, the server stores the storefront route NAME (e.g., `cart.view`), not its current URL path. If the merchant later switches to a theme that defines `cart.view` at a different URL, the menu item automatically follows — the storefront resolves the URL on each request. Selecting a section that no longer exists returns *"Invalid link section"* on save — see [[design-navigation-item-types]].

### Active state is auto-computed per storefront request

The menu item's "active" / highlight state on the storefront is computed at render time: an item is active if the current storefront route matches the item's target route (or any of its children is active). The merchant does not configure this — it just happens.

## How it works (verified against backend)

### Two screen modes — full HTML and AJAX tree fetch

The same `/admin/storefront/navigation/{group?}` URL serves both the initial full-page HTML (no `group` param) and the AJAX tree-data response when `group=main` or `group=footer` is requested via XHR. A non-XHR request without `group` renders the parent shell with both trees; an XHR request without one of those two valid groups returns 404.

### Tree data loads on demand per node

Each tree fetches its root-level nodes on page load, then lazy-loads children when a parent is expanded — the tree element's data URL points to the same list endpoint with `node=<parent_id>` as a query parameter. Each node response includes a `load_on_demand` flag based on its `children_count`, so the UI knows whether to render an expand arrow.

## Related

- [[design-navigation]] — hub.
- [[design-themes]] — theme choice determines which `section` routes exist and their URLs.

## Open questions

None.
