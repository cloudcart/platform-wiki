---
type: feature
nav_path: "Design → Navigation"
route_name: design.navigation
route_path: /admin/design/navigation
aliases: ["Navigation", "Menus", "Storefront menu", "Header menu", "Footer menu", "Навигация", "Меню"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-05-23
updated: 2026-11-09
source_count: 1
---
# Storefront Navigation

## Purpose

The **Navigation** screen is where the merchant builds the storefront's menus — the **Main menu** rendered in the store header and the **Footer menu** rendered at the bottom of every page. Each menu is a drag-and-drop reorderable tree of items, where every item links to a Product, a Product Category, a Brand (Vendor), a Blog category, a Blog article, a Static page, a Theme section, a Smart Collection, an external URL, a Mailchimp newsletter pop-up, or a custom HTML / JS snippet. Items nest into sub-menus (up to 4 levels deep) for dropdowns.

This page is the **navigation pivot** for the cluster. The screen-level mechanics — the item type catalogue, the add / edit link form fields, the tree-editing behaviour, the menu groups, how each link type resolves to a storefront URL, and the per-save side-effects — each live on a dedicated aspect page below.

## Where to find it

Sidebar → **Design** → **Navigation**.

The address is `/admin/design/navigation`, so the full link is `https://<store-domain>/admin/design/navigation`. The older address `/admin/storefront/navigation` belonged to the previous version of this screen, which was replaced by the new admin in July 2026: it no longer exists and does not redirect, so a direct link to it lands on a 404 page.

The screen (title **Navigation**, breadcrumb **Design → Navigation**) shows one menu at a time, with a tab per menu: **Main menu** and **Footer menu** on every store, plus any custom menus on a Liquid-theme store. Each tab shows that menu's tree with an **Add link** button.

Adding, editing, reordering and deleting menu items all happen on this one screen; none of these actions has an address of its own. The per-action addresses of the old screen (`/admin/storefront/navigation/{group}/create-select`, `/create/{type}`, `/edit/{id}`, `/reorder`, `/delete/{id}`) were removed with it.

Each menu is identified by its group key — `main`, `footer`, or a custom menu's key on Liquid themes. See [[design-navigation-menu-groups]].

## Sub-pages (in this cluster)

This topic is split into 6 aspect pages. Drill into the one that matches the question rather than reading every page.

- [[design-navigation-item-types]] — the 12 item types (`url`, `product`, `category`, `vendor`, `blog`, `article`, `page`, `section`, `selection`, `group`, `mailchimp`, `snippet`); their picker fields and use cases.
- [[design-navigation-item-fields]] — the **Add link** / **Edit link** form fields (`name`, `parent_id`, `blank`, icon, `widget_text`) and the full validation-message table.
- [[design-navigation-tree-editing]] — drag-and-drop with three drop modes (`before` / `after` / `inside`), 4-level depth limit, per-parent name uniqueness, recursive delete, reorder self-heal.
- [[design-navigation-menu-groups]] — which menus the screen lists per theme type (`main` + `footer`, plus custom menus on Liquid); why an unknown menu key 404s; relation to `navigation.links` modules on [[design-modules-navigation]].
- [[design-navigation-link-resolution]] — how each link type resolves to a storefront URL; `url` verbatim vs `section` route-name vs typed `link_id` resolution; active-state computation.
- [[design-navigation-side-effects]] — per-save cache regeneration, the `boarding_menus` onboarding flag, theme-gated icon support, permission requirement.

## What the merchant can do here

On the **Navigation** screen the merchant can:

- Switch menus with the tabs. **Main menu** reads "This content is shown in the top (main) menu of your store."; **Footer menu** reads "This content is shown in the footer menu of your store." An empty menu shows "No links have been added to this menu yet." with an **Add the first link** button.
- Click **Add link** (top-right of the tree) to open a dialog headed "What should this menu item link to?" with one card per link type — see [[design-navigation-item-types]].
- Click the arrow on a row that has children to collapse or expand its sub-links; every level is expanded on load. Each row shows the item's name, its storefront address (when it has one) and, for a parent, a **Sub-links** count.
- Drag any node to a new position to reorder or re-parent it — see [[design-navigation-tree-editing]].
- Click the pencil on a row to open the **Edit link** form ([[design-navigation-item-fields]]); click the remove icon and confirm **Remove link?** to delete the item and all its children.

## What the merchant cannot do here

- Create, rename or delete a menu — the screen has no control for it. On Smarty themes only `main` and `footer` are listed; extra link sets such as the "Page menu" `navigation.links` modules are configured from [[design-modules-navigation]]. On Liquid themes custom menus appear as extra tabs (verify where they are created) — see [[design-navigation-menu-groups]].
- Nest items more than 4 levels deep — the form rejects with *"Maximum depth is 4"*. See [[design-navigation-tree-editing]].
- Reuse the same name twice within the same parent — the form rejects with *"Name is taken"*. See [[design-navigation-item-fields]].

## Settings & fields

The Navigation screen has no page-level settings — every configurable value lives on an individual menu item via the **Add link** / **Edit link** form. The full field list, defaults, and validation-message table are on [[design-navigation-item-fields]]. The per-type picker field that each item type surfaces is on [[design-navigation-item-types]]. The menu group keys and their storefront placement are on [[design-navigation-menu-groups]].

## Business rules

The cluster's business rules are documented on the aspect that owns each one:

- **Menus per theme type**: `main` + `footer` on Smarty themes, plus custom menus on Liquid themes; an unknown menu key returns 404 — [[design-navigation-menu-groups]].
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
