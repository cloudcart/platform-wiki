---
type: feature
nav_path: "Design → Navigation → Item fields"
route_name: admin.navigation.edit
route_path: /admin/storefront/navigation/{group}/edit/{navigation_id}
aliases: ["Navigation item fields", "Menu item fields", "Add menu item", "Edit menu item", "Navigation validation", "Полета на меню елемент"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Navigation — item fields & validation

> Part of [[design-navigation]]. See the hub for the other aspects (item types, tree editing, menu groups, link resolution, side-effects).

## Purpose

This page documents the **Add / Edit menu item** side panel — the shared fields every menu item carries (label, parent, new-tab switch, icon, snippet text) and the complete validation-message table the form enforces. The per-type picker field (Product autocomplete, Category tree-select, etc.) is on [[design-navigation-item-types]].

## Where to find it

Sidebar → **Design** → **Navigation**. Click **Add more** on a tree, pick a type, and the Add panel opens; or click the inline edit pencil on any node to open the Edit panel (`/admin/storefront/navigation/{group}/edit/{navigation_id}`).

## What the merchant can do here

In the **Add / Edit item** side panel the merchant sets:

- **Menu item name** (or **Menu group name** for `group` type) — the visible storefront label.
- **Menu parent** — optional select of any existing item in the same menu tree (creates a sub-menu under that item). Leave empty for a top-level item.
- A **type-specific picker** that depends on the chosen type — see [[design-navigation-item-types]].
- **Open link in a new window** switch — when on, the link opens in a new browser tab. Not shown for `group`, `mailchimp`, `snippet` types.
- **Icon** select — only if the active theme has `functions.navigations.icon.status` enabled; see [[design-navigation-side-effects]] for the theme-gating.
- **Snippet code** textarea (`snippet` type only) — raw HTML / JS up to 12,000 characters.

## What the merchant cannot do here

- Save an item with no name, or with a name longer than 200 characters.
- Reuse a name already taken by a sibling under the same parent (*"Name is taken"*).
- Save an external `url` item with a malformed address.
- Select an icon on a theme that does not advertise icon support — the field is hidden entirely.

## Settings & fields

### Per-item fields

| Field | What it does | Default | Notes |
|-------|--------------|---------|-------|
| `name` | The label shown in the storefront menu | — | Help text *"This is the name of the menu item that your users will see."* |
| `parent_id` | Parent item — creates a sub-menu under that parent | None (top-level) | Help text *"Choose a parent if you wish this menu item to be a sub-menu."* |
| `blank` | Opens the link in a new browser tab | Off | Hidden for `group`, `mailchimp`, `snippet` types |
| `class` (icon) | Font Awesome icon class shown on the left of the name | None | Theme-gated — only shown when the active theme advertises `functions.navigations.icon.status` |
| `widget_text` | HTML / JS snippet rendered in place of the menu item | — | `snippet` type only |

### Validation messages

| Field | Validation | Error message |
|-------|------------|---------------|
| `name` | Required, max 200 chars, unique within the same parent | *"Name is required"* / *"Name is taken"* / *"Maximum symbols for name are 200"* |
| `link_type` | Required, must be one of the 12 allowed types | *"Link type is required"* / *"Invalid link type"* |
| `url` | Required if type is `url`, must validate as a URL | *"URL is invalid format"* (`core.validate.err.url_invalid_format`) |
| `link_id` | Required for the 7 typed pickers (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`) | *"<type> link does not exist"* (with type name interpolated) |
| `parent_id` | Must exist in the same group; total depth (parent chain + child chain) cannot exceed 4 | *"Parent no longer exists"* / *"Maximum depth is 4"* |
| `route` | Required if type is `section`, must be a known theme route | *"Invalid link section"* |
| `widget_text` | Required if type is `snippet`, max 12,000 chars | *"Invalid link section"* (reused message) |

## Business rules

### Names must be unique within the same parent

Two menu items cannot share the same name if they sit under the same parent (or are both at the top level). The check is per-parent, so the merchant CAN have a "Home" item at the top level and another "Home" inside a different parent group. The error message is *"Name is taken"*. Re-parenting a node re-checks this constraint against its new siblings — see [[design-navigation-tree-editing]].

### New-tab switch is hidden for non-link types

The **Open link in a new window** switch only applies to types that produce a real URL, so it is hidden for `group`, `mailchimp`, and `snippet`.

### Icon field is theme-gated

The **Icon** picker appears only when the active theme advertises `functions.navigations.icon.status = true`. The full gating mechanics (catalogue, theme-config flag) are on [[design-navigation-side-effects]].

## Related

- [[design-navigation]] — hub.
- [[design-themes]] — theme choice controls whether the icon field appears.

## Open questions

None.
