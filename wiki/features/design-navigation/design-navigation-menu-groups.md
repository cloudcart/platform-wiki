---
type: feature
nav_path: "Design → Navigation → Menu groups"
route_name: admin.navigation.list
route_path: /admin/storefront/navigation/{group?}
aliases: ["Navigation menu groups", "Main menu", "Footer menu", "Menu group keys", "Главно меню", "Меню във футъра"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Navigation — menu groups (main + footer)

> Part of [[design-navigation]]. See the hub for the other aspects (item types, item fields, tree editing, link resolution, side-effects).

## Purpose

The Navigation screen surfaces exactly two menu trees: the **Main menu** (group `main`, rendered in the store header) and the **Footer menu** (group `footer`, rendered at the bottom of every page). This page explains the two-group model, why a third group key is rejected, and how these two trees differ from the `navigation.links` storefront modules.

## Where to find it

Sidebar → **Design** → **Navigation**. The two trees sit side-by-side on `/admin/storefront/navigation`. The `{group}` URL parameter (`main` or `footer`) selects which tree's data is fetched — see [[design-navigation-link-resolution]] for the dual full-HTML / AJAX request handling on this route.

## What the merchant can do here

- Build the **Main menu** tree (left) — *"The content here will be visible in the main menu of your store."*
- Build the **Footer menu** tree (right) — *"The content here will be visible in the footer of your store."*
- Add the first item to an empty tree via the **Add your first menu item** link.

## What the merchant cannot do here

- Create a third menu group from this screen. Addressing any group key other than `main` or `footer` from the URL returns a 404.
- Manage top-bar links, footer-column links, or page-menu pages here — those are `navigation.links` module instances configured on [[design-modules-navigation]], not menu groups.

## Settings & fields

### Menu group keys

| Group key | Storefront placement | Description |
|-----------|----------------------|-------------|
| `main` | Top header menu (or the theme's primary navigation) | *"Add menu items to the store's main navigation."* |
| `footer` | Bottom of every storefront page | *"Add menu items to the store footer section."* |

The exact rendering of the `main` group depends on the active theme's primary-navigation layout — see [[design-themes]].

## Business rules

### Two menu groups only — `main` and `footer`

The Navigation screen surfaces exactly two menu trees: **Main menu** (group `main`) and **Footer menu** (group `footer`). Any attempt to address a different group key from the URL returns a 404.

### Additional menu surfaces come from modules, not groups

Other storefront menu surfaces — top-bar links, footer-column links, page-menu pages — are powered by `navigation.links` module instances configured under [[design-modules-navigation]]. They are NOT additional groups on this screen. A merchant looking for "a third menu" should be directed to the Modules screen, not here.

### The active theme governs visibility of each group

Whether a theme renders the `footer` group at all, and how the `main` group is laid out, is theme-dependent. Switching themes via [[design-themes]] can change where (and whether) each menu group appears, even though the underlying menu items are unchanged.

## Related

- [[design-navigation]] — hub.
- [[design-modules-navigation]] — `navigation.links` module instances (top-bar, footer-column, page-menu); distinct from the `main` / `footer` groups here.
- [[design-themes]] — theme choice controls how / whether each group renders.

## Open questions

None.
