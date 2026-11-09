---
type: feature
nav_path: "Design → Navigation → Menu groups"
route_name: design.navigation
route_path: /admin/design/navigation
aliases: ["Navigation menu groups", "Main menu", "Footer menu", "Menu group keys", "Главно меню", "Меню във футъра"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---
# Navigation — menu groups (main + footer)

> Part of [[design-navigation]]. See the hub for the other aspects (item types, item fields, tree editing, link resolution, side-effects).

## Purpose

The Navigation screen shows one tab per menu. Every store has the **Main menu** (group `main`, rendered in the store header) and the **Footer menu** (group `footer`, rendered at the bottom of every page); a Liquid-theme store also lists its custom menus. This page explains which menus are listed per theme type, why an unknown group key is rejected, and how these menus differ from the `navigation.links` storefront modules.

## Where to find it

Sidebar → **Design** → **Navigation**, at `/admin/design/navigation`. Each menu has its own tab on this screen. The group key (`main`, `footer`, or a custom menu's key on Liquid themes) selects which menu's tree is fetched — see [[design-navigation-link-resolution]] for how the screen and its tree data load.

## What the merchant can do here

- Build the **Main menu** tree (first tab) — *"This content is shown in the top (main) menu of your store."*
- Build the **Footer menu** tree (second tab) — *"This content is shown in the footer menu of your store."*
- On a Liquid-theme store, build each custom menu on its own tab; the tab shows that menu's own description.
- Add the first item to an empty menu via the **Add the first link** button.

## What the merchant cannot do here

- Create, rename or delete a menu — the screen has no control for it (on Liquid themes, verify where custom menus are created). `main` and `footer` are created automatically when missing and cannot be deleted; requesting a menu key that does not exist returns a 404.
- Manage top-bar links, footer-column links, or page-menu pages here — those are `navigation.links` module instances configured on [[design-modules-navigation]], not menu groups.

## Settings & fields

### Menu group keys

| Group key | Storefront placement | Description |
|-----------|----------------------|-------------|
| `main` | Top header menu (or the theme's primary navigation) | *"This content is shown in the top (main) menu of your store."* |
| `footer` | Bottom of every storefront page | *"This content is shown in the footer menu of your store."* |
| custom key (Liquid themes only) | Wherever the theme places that menu (verify) | The menu's own description |

The exact rendering of the `main` group depends on the active theme's primary-navigation layout — see [[design-themes]].

Each tab shows the menu's stored name. `main` and `footer` get their names when first created, in the admin's language at that moment: in Bulgarian „Главно меню“ / „Долно меню“, in English "Main menu" / "Footer menu" (verify on an older store).

## Business rules

### Which menus are listed depends on the theme type

On a Smarty-theme store the screen lists only the two system menus, **Main menu** (`main`) and **Footer menu** (`footer`). On a Liquid-theme store it lists those two first, then every custom menu. A request for a menu key that does not exist returns a 404.

### Additional menu surfaces come from modules, not groups

On Smarty themes, other storefront menu surfaces — top-bar links, footer-column links, page-menu pages — are powered by `navigation.links` module instances configured under [[design-modules-navigation]]. They are NOT additional groups on this screen. A merchant looking for "a third menu" should be directed to the Modules screen, not here.

### The active theme governs visibility of each group

Whether a theme renders the `footer` group at all, and how the `main` group is laid out, is theme-dependent. Switching themes via [[design-themes]] can change where (and whether) each menu group appears, even though the underlying menu items are unchanged.

## Related

- [[design-navigation]] — hub.
- [[design-modules-navigation]] — `navigation.links` module instances (top-bar, footer-column, page-menu); distinct from the `main` / `footer` groups here.
- [[design-themes]] — theme choice controls how / whether each group renders.

## Open questions

None.
