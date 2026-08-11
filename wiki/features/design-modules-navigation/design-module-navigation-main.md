---
type: feature
nav_path: "Design → Modules → Navigation → Main navigation"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Main navigation module", "navigationMain", "navigation.main", "Header menu module", "Main menu module", "Главна навигация", "Главно меню"]
tags: [design, modules, navigation, header, menu]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Main navigation (`navigationMain`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Main navigation** module renders the storefront's primary header menu — the link tree the customer uses to reach categories, brands, blog, pages, and other sections. It is the most important navigation surface on the storefront.

The module itself only RENDERS the tree; the actual link content (categories, articles, custom URLs, mega-menu panels, snippets, etc.) is edited in [[design-navigation]] under the **Main menu** tab. The module does NOT have a card on the Modules screen — switching menu layouts (mega-menu vs dropdown vs sidemenu) is done via the **Header settings** module (`headerConfiguration`) on the Modules screen, not here.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Header — exact position depends on the active theme's header template |
| Menu content editor | Sidebar → **Design** → **Navigation** → **Main menu** tab (see [[design-navigation]]) |
| Layout / type picker | Sidebar → **Design** → **Modules** → **Layout** tab → **Header settings** card (`headerConfiguration`) |
| Modules screen card | None — the module itself has no editable form |

The underlying module mapping is `navigation.main`; the instance name is `navigationMain`.

## What the merchant can do here

Because this module has no Modules-screen card, the merchant configures it indirectly:

- **Edit the menu items** in [[design-navigation]] — add / remove / reorder up to four levels of links (12 link types: Product, Product Category, Vendor, Blog, Article, Page, Section, External URL, Snippet, Mega-menu, Banner, Heading).
- **Pick the menu layout** in **Header settings** (`headerConfiguration`) — choose between mega-menu, sidemenu, dropdown, mega-menu two, or top-bar (see *Theme-specific notes* below).
- **Pick the mobile menu layout** in **Header settings** — `sidemenu` (off-canvas drawer) or `dropdown` (accordion).

The merchant cannot:

- Edit individual link captions, URLs, or icons from the Modules screen — that all lives in [[design-navigation]].
- Disable the entire main menu — every theme renders the header navigation slot. To "hide" it, the merchant deletes all links from the `main` tree (the slot then renders empty).
- Move the main menu to the footer — slot placement is fixed by the active theme's header template.

## Settings & fields

The `navigation.main` module itself has NO merchant-editable settings. The settings table for this module is therefore empty.

For completeness, the related settings the merchant adjusts in OTHER screens to control how this module renders:

| Setting | Where to edit | Effect |
|---------|---------------|--------|
| Menu items (the link tree) | [[design-navigation]] → **Main menu** tab | Source of every link the module renders |
| Menu layout type | **Modules** → **Header settings** → `menu` field | Mega-menu / sidemenu / dropdown / mega-menu two / top-bar |
| Mobile menu type | **Modules** → **Header settings** → `menu_mobile` field | `sidemenu` or `dropdown` |
| Header template | **Modules** → **Header settings** → `header` field | Picks which theme header file to use; changes where the menu slot lives |
| Sticky / transparent / search-icon toggles | **Modules** → **Header settings** | Affect surrounding chrome, not the menu items themselves |

### Theme-specific notes

The list of available menu LAYOUTS is theme-shipped. Common variants:

| Layout key | Visual |
|------------|--------|
| `mega-menu` | Multi-column dropdown panels with category / sub-category trees |
| `mega-menu-two` | Richer mega-menu variant; forces sidemenu on mobile |
| `sidemenu` | Left-rail collapsible vertical tree |
| `dropdown` | Classic hover-dropdown horizontal bar |
| `top-bar` | Single horizontal row above the header |

Different themes ship different subsets — e.g., Echappe ships mega-menu + sidemenu + dropdown; Themex adds mega-menu-two; Knowledge-tmarket exposes a custom top-bar variant. The exact options appear as an image-preview select inside **Header settings**.

## Business rules

### The menu CONTENT lives in the navigation editor, not the module

`navigationMain` consumes the `main` group from the navigation editor in [[design-navigation]]. The module's only job is to render whatever links currently exist in that group. There is no caching at the module level — the navigation editor invalidates the navigation cache directly when the merchant saves.

### Layout is theme-driven

Whether the menu appears as a mega-menu, sidemenu, or dropdown is set in **Header settings**, not in the navigation editor or this module. Two different themes can render the SAME `main` tree as a mega-menu and a sidemenu just by picking a different header template.

### The module is universal but the layouts are theme-specific

Every theme ships a `navigationMain` instance and a header that renders it — the merchant always has a main-menu slot. But which menu layouts are available depends on the theme; switching themes can change the picker options in **Header settings**.

### Empty `main` tree → empty header

If the merchant deletes all links from the `main` tree, the header renders with no menu items. The theme still renders the wrapper (logo, search, cart icons) but the menu slot is empty.

### No plan-gating

`navigation.main` is not in the `paid_widgets` allowlist — available on every plan.

## Related

- [[design-modules-navigation]] — hub.
- [[design-navigation]] — edit the `main` tree content (the source of links).
- [[design-module-navigation-footer]] — sibling; renders the `footer` tree.
- [[design-module-navigation-links]] — flat secondary link list (distinct from the menu trees).
- [[design-themes]] — switching themes changes which header / menu layouts are available.
- [[design-modules]] — parent module catalogue.

## Open questions

- 📡 **Per-language navigation links.** With `multylang` installed, the `main` tree supports per-language captions via the language switcher in [[design-navigation]]. GraphQL-resolvable: query whether the `multylang` app is installed.
- ⏸️ **Default theme variant per-merchant.** Different themes ship different default menu layouts; verify with the theme designer if a specific store needs a non-default header layout out-of-the-box.
