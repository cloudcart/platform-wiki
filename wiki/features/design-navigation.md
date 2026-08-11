---
type: feature
nav_path: "Design → Navigation"
route_name: admin.navigation.list
route_path: /admin/storefront/navigation
aliases: ["Navigation", "Menus", "Storefront menu", "Header menu", "Footer menu", "Навигация", "Меню"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 0
---
# Storefront Navigation

## Purpose

The **Navigation** screen is where the merchant builds the storefront's menus — the **Main menu** rendered in the store header and the **Footer menu** rendered at the bottom of every page. Each menu is a drag-and-drop reorderable tree of items, where every item links to a Product, a Product Category, a Brand (Vendor), a Blog category, a Blog article, a Static page, a Theme section, a Smart Collection, an external URL, a Mailchimp newsletter pop-up, or a custom HTML / JS snippet. Items nest into sub-menus (up to 4 levels deep) for dropdowns.

This page is the **navigation pivot** for the cluster. The screen-level mechanics — the item type catalogue, the add / edit panel fields, the tree-editing behaviour, the two menu groups, how each link type resolves to a storefront URL, and the per-save side-effects — each live on a dedicated aspect page below.

## Where to find it

Sidebar → **Design** → **Navigation**.

The route is `/admin/storefront/navigation`. The page is a single screen with two side-by-side tree editors — **Main menu** on the left, **Footer menu** on the right — each with its own "Add more" button and breadcrumb labelled "Navigation".

Sub-routes:

| Action | Route name | Path |
|--------|------------|------|
| List (both trees) | `admin.navigation.list` | `/admin/storefront/navigation/{group?}` |
| Choose item type | `admin.navigation.create.select` | `/admin/storefront/navigation/{group}/create-select` |
| Add item of a type | `admin.navigation.create` | `/admin/storefront/navigation/{group}/create/{type}` |
| Edit item | `admin.navigation.edit` | `/admin/storefront/navigation/{group}/edit/{navigation_id}` |
| Reorder (drag-and-drop) | `admin.navigation.reorder` | `POST /admin/storefront/navigation/{group}/reorder` |
| Delete item | `admin.navigation.delete` | `/admin/storefront/navigation/{group}/delete/{navigation_id}` |

The `{group}` URL parameter is the menu group key — `main` or `footer`. See [[design-navigation-menu-groups]].

## Sub-pages (in this cluster)

This topic is split into 6 aspect pages. Drill into the one that matches the question rather than reading every page.

- [[design-navigation-item-types]] — the 12 item types (`url`, `product`, `category`, `vendor`, `blog`, `article`, `page`, `section`, `selection`, `group`, `mailchimp`, `snippet`); their picker fields and use cases.
- [[design-navigation-item-fields]] — the Add / Edit side-panel fields (`name`, `parent_id`, `blank`, icon, `widget_text`) and the full validation-message table.
- [[design-navigation-tree-editing]] — drag-and-drop with three drop modes (`before` / `after` / `inside`), 4-level depth limit, per-parent name uniqueness, recursive delete, reorder self-heal.
- [[design-navigation-menu-groups]] — the two-group model (`main` + `footer` only); why a third group 404s; relation to `navigation.links` modules on [[design-modules-navigation]].
- [[design-navigation-link-resolution]] — how each link type resolves to a storefront URL; `url` verbatim vs `section` route-name vs typed `link_id` resolution; active-state computation.
- [[design-navigation-side-effects]] — per-save cache regeneration, the `boarding_menus` onboarding flag, theme-gated icon support, lazy tree loading, permission requirement.

## What the merchant can do here

On the **Navigation** screen the merchant can:

- See two trees side-by-side: **Main menu** ("The content here will be visible in the main menu of your store") and **Footer menu** ("The content here will be visible in the footer of your store"). Empty trees show a "There are no main / footer menu items yet" message with an **Add your first menu item** link.
- Click **Add more** (top-right of each tree) to open the **Choose item type** side panel with the type cards — see [[design-navigation-item-types]].
- Click any node to expand it and reveal child items (sub-menus). Trees auto-open on load.
- Drag any node to a new position to reorder or re-parent it — see [[design-navigation-tree-editing]].
- Click the inline edit pencil to open the **Edit menu item** side panel ([[design-navigation-item-fields]]); click the delete icon to remove the node (and all its children).
- Click **Hire expert** (top-right) to be routed to the in-platform marketplace of paid services for help building menus.

## What the merchant cannot do here

- Add a menu beyond `main` and `footer` from this screen. Any third menu group (e.g., the "Page menu" set of `navigation.links` modules on some themes) is configured from [[design-modules-navigation]], not here — see [[design-navigation-menu-groups]].
- Nest items more than 4 levels deep — the form rejects with *"Maximum depth is 4"*. See [[design-navigation-tree-editing]].
- Reuse the same name twice within the same parent — the form rejects with *"Name is taken"*. See [[design-navigation-item-fields]].

## Settings & fields

The Navigation screen has no page-level settings — every configurable value lives on an individual menu item via the Add / Edit side panel. The full field list, defaults, and validation-message table are on [[design-navigation-item-fields]]. The per-type picker field that each item type surfaces is on [[design-navigation-item-types]]. The two menu group keys (`main`, `footer`) and their storefront placement are on [[design-navigation-menu-groups]].

## Business rules

The cluster's business rules are documented on the aspect that owns each one:

- Exactly **two menu groups** (`main` + `footer`); a third group 404s — [[design-navigation-menu-groups]].
- **Max nesting depth 4**, three drop modes, no-cycle rule, recursive delete — [[design-navigation-tree-editing]].
- **Per-parent name uniqueness** + the full validation table — [[design-navigation-item-fields]].
- **Type whitelist** of 12 link types — [[design-navigation-item-types]].
- **Link persistence** per type (`url` verbatim, `section` route-name, typed `link_id`) + auto-computed active state — [[design-navigation-link-resolution]].
- **Per-save cache regeneration**, the `boarding_menus` onboarding flag, theme-gated icons — [[design-navigation-side-effects]].

## Related

- [[design]] — parent Design pillar.
- [[design-themes]] — theme picker; theme choice controls icon support, supported sections, and whether `navigation.links` module instances exist.
- [[design-modules-navigation]] — sibling; configures `navigation.links` module instances (top-bar links, footer-column links, page-menu pages) — distinct from these two `main` / `footer` menu trees.
- [[marketing-landing-pages]] — landing pages selectable as `page` link type.
- [[marketing-blog-articles]] — blog articles selectable as `article` link type.
- [[products]] — products selectable as `product` link type.
- [[products-vendors]] — vendors selectable as `vendor` link type.
- [[products-smart-collections]] — collections selectable as `selection` link type.
- [[apps-mailchimp]] — Newsletter Mailchimp app; powers the `mailchimp` link-type pop-up.

## Open questions

None at the hub level — see each aspect page for its own open questions.
