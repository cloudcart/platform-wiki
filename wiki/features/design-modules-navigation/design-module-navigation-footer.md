---
type: feature
nav_path: "Design → Modules → Navigation → Footer navigation"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Footer navigation module", "navigationFooter", "navigation.footer", "Footer menu module", "Foot menu module", "Долна навигация", "Долно меню"]
tags: [design, modules, navigation, footer, menu]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Footer navigation (`navigationFooter`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Footer navigation** module renders the FOOTER link tree — typically the "Shop", "Company", "Help", "Customer service" columns the customer sees at the bottom of every storefront page. Same edit mechanics as [[design-module-navigation-main]] but stored as a SEPARATE tree (`footer`).

The module RENDERS the tree; the link content is edited in [[design-navigation]] under the **Footer menu** tab. The footer column layout (single column vs multi-column vs accordion) is picked via the **Foot settings** module (`footerConfiguration`).

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Footer — column placement determined by the active theme's footer template |
| Menu content editor | Sidebar → **Design** → **Navigation** → **Footer menu** tab (see [[design-navigation]]) |
| Layout / type picker | Sidebar → **Design** → **Modules** → **Layout** tab → **Foot settings** card (`footerConfiguration`) |
| Modules screen card | None — the module has no editable form |

The underlying module mapping is `navigation.footer`; the instance name is `navigationFooter`.

## What the merchant can do here

Because the module has no Modules-screen card, the merchant configures it indirectly:

- **Edit the menu items** in [[design-navigation]] (the `footer` tree) — same 4-level nesting and 12 link types as the main tree.
- **Pick the footer template** in **Foot settings** (`footerConfiguration`) — determines the column layout the footer tree renders into.
- **Optionally use sibling flat-link modules** ([[design-module-navigation-links]] instances `footerLinks1` / `footerLinks2` / `footerLinks3`) to fill EXTRA footer columns alongside this tree.

The merchant cannot:

- Edit individual footer-link captions / URLs from this module — they all live in [[design-navigation]].
- Move the footer tree to the header — the slot is fixed by the active theme's footer template.
- Hide the entire footer navigation — to "hide" it, the merchant deletes all links from the `footer` tree, leaving an empty column.

## Settings & fields

The `navigation.footer` module itself has NO merchant-editable settings.

The related settings the merchant adjusts in OTHER screens to control how this module renders:

| Setting | Where to edit | Effect |
|---------|---------------|--------|
| Footer link tree | [[design-navigation]] → **Footer menu** tab | Source of every link rendered |
| Footer template | **Modules** → **Foot settings** → `footer` field | Picks the theme footer file (controls column layout, copyright block placement, etc.) |
| Footer column composition | **Modules** → **Foot settings** | Multi-column setups can route SUB-trees into separate columns |

### Theme-specific notes

Most themes ship a SINGLE column for the `footer` tree plus three independent flat-link columns (`footerLinks1` / `footerLinks2` / `footerLinks3`). When the merchant wants a 4-column footer, the typical pattern is:

- Column 1: `navigationFooter` tree
- Columns 2-4: `footerLinks1`, `footerLinks2`, `footerLinks3` (flat lists edited via [[design-module-navigation-links]])

Some themes (e.g., Echappe, Themex) consume the `footer` tree's TOP-LEVEL items as column headers and the children as the column contents — a sub-tree per column. Other themes (e.g., simpler one-column themes) flatten the whole tree into a single list. The behaviour is theme-controlled, not editable.

## Business rules

### The footer tree is independent of the main tree

`navigationFooter` reads ONLY the `footer` navigation group. Adding a link to the `main` tree does NOT add it to the footer — the merchant must add it to BOTH trees separately if it should appear in both places.

### Empty `footer` tree → empty column

If the merchant deletes all links from the `footer` tree, the footer column renders empty (the theme still renders the column wrapper). The merchant should typically populate the footer tree with at least 3-5 essential links (About, Contact, Shipping, Returns, Terms).

### Multi-column themes use sibling flat-link modules

Themes that ship multi-column footers (construction, motivation-businessindustrial, flair-electronicstore variants) typically use `footerLinks1` / `footerLinks2` / `footerLinks3` ALONGSIDE `navigationFooter`. The merchant edits each one separately. Verify in the active theme's config which slot renders which module.

### No plan-gating

`navigation.footer` is not in the `paid_widgets` allowlist — available on every plan.

## Related

- [[design-modules-navigation]] — hub.
- [[design-navigation]] — edit the `footer` tree content (the source of links).
- [[design-module-navigation-main]] — sibling; renders the `main` tree.
- [[design-module-navigation-links]] — flat sibling-column link modules (`footerLinks1-3`).
- [[design-themes]] — switching themes changes the column layout for the footer.
- [[design-modules]] — parent module catalogue.

## Open questions

- 📡 **Per-language footer links.** With `multylang` installed, the `footer` tree supports per-language captions via the language switcher in [[design-navigation]]. GraphQL-resolvable: query whether the `multylang` app is installed.
- ⏸️ **Footer tree → column mapping.** Confirm per-theme whether the `footer` tree's top-level items become column headers or whether the tree is flattened into a single list.
