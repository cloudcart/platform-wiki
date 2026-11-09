---
type: feature
nav_path: "Design → Navigation → Item fields"
route_name: design.navigation
route_path: /admin/design/navigation
aliases: ["Navigation item fields", "Menu item fields", "Add menu item", "Edit menu item", "Navigation validation", "Полета на меню елемент"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---
# Navigation — item fields & validation

> Part of [[design-navigation]]. See the hub for the other aspects (item types, tree editing, menu groups, link resolution, side-effects).

## Purpose

This page documents the **Add link** / **Edit link** form (a dialog on the Navigation screen) — the shared fields every menu item carries (label, parent, new-tab switch, icon, snippet text) and the complete validation-message table the form enforces. The per-type picker field (Product autocomplete, Category tree-select, etc.) is on [[design-navigation-item-types]].

## Where to find it

Sidebar → **Design** → **Navigation**. Click **Add link** on a menu's tab, pick a type in the "What should this menu item link to?" dialog, and the **Add link** form opens; or click the pencil on any row to open the **Edit link** form directly. Both open on the same screen (`/admin/design/navigation`), without an address of their own.

## What the merchant can do here

In the **Add link** / **Edit link** form (card **General settings**) the merchant sets:

- **Link name** (or **Group name** for the `group` type) — the visible storefront label.
- **Parent** — optional search-select of the existing items in the same menu (creates a sub-menu under that item); on edit it leaves out the item itself and its sub-items. Leave it at **None (top level)** for a top-level item. Any item can be a parent, a **Web link** included; how a parent that has its own link shows its sub-items is up to the theme.
- A **type-specific picker** that depends on the chosen type — see [[design-navigation-item-types]].
- **Open in new window** switch — when on, the link opens in a new browser tab. Not shown for `group`, `mailchimp`, `snippet` types.
- **Icon** select — only if the active theme has `functions.navigations.icon.status` enabled; see [[design-navigation-side-effects]] for the theme-gating.
- **HTML snippet** textarea (`snippet` type only) — raw HTML / JS up to 12,000 characters.
- **Menu item image** (in an **Image** card) — only on the few stores the platform has enabled for it, and only for link types that produce a URL.

The dialog's buttons are **Save** and **Cancel** (English labels; the Bulgarian ones come from the admin translations). A successful save shows *"Saved successfully"*.

## What the merchant cannot do here

- Save an item with no name, or with a name longer than 200 characters.
- Reuse a name already taken by a sibling under the same parent (*"Name is taken"*).
- Save an external `url` item with a malformed address, or with a bare path such as `/withdrawal`: the address must start with a scheme (`https://`). For a page of the store, use its link type (for example **Link to a specific store section**) or type the full address.
- Select an icon on a theme that does not advertise icon support — the field is hidden entirely.

## Settings & fields

### Per-item fields

| Field | What it does | Default | Notes |
|-------|--------------|---------|-------|
| `name` | The label shown in the storefront menu | — | Label **Link name** (**Group name** for `group`) |
| `parent_id` | Parent item — creates a sub-menu under that parent | None (top-level) | Label **Parent**, empty value **None (top level)** |
| `blank` | Opens the link in a new browser tab | Off | Label **Open in new window**; hidden for `group`, `mailchimp`, `snippet` types |
| `class` (icon) | Font Awesome icon class shown on the left of the name | None | Theme-gated — only shown when the active theme advertises `functions.navigations.icon.status` |
| `widget_text` | HTML / JS snippet rendered in place of the menu item | — | Label **HTML snippet**; `snippet` type only |

### Validation messages

| Field | Validation | Error message |
|-------|------------|---------------|
| `name` | Required, max 200 chars, unique within the same parent | *"Name is required"* / *"Name is taken"* / *"Maximum symbols for name are 200"* |
| `link_type` | Required, must be one of the 12 allowed types | *"Link type is required"* / *"Invalid link type"* |
| `url` | Required if type is `url`, must be a full URL with a scheme | *"URL format is invalid."* / *"URL формат е невалиден."* (`core.validate.err.url_invalid_format`) |
| `link_id` | Required for the 7 typed pickers (`product`, `category`, `vendor`, `blog`, `article`, `page`, `selection`) | *"<type> link does not exist"* (with type name interpolated) |
| `parent_id` | Must exist in the same group; total depth (parent chain + child chain) cannot exceed 4 | *"Parent no longer exists"* / *"Maximum depth is 4"* |
| `route` | Required if type is `section`, must be a known theme route | *"Invalid link section"* |
| `widget_text` | Required if type is `snippet`, max 12,000 chars | *"Invalid link section"* (reused message) |

## Business rules

### Names must be unique within the same parent

Two menu items cannot share the same name if they sit under the same parent (or are both at the top level). The check is per-parent, so the merchant CAN have a "Home" item at the top level and another "Home" inside a different parent group. The error message is *"Name is taken"*. Re-parenting a node re-checks this constraint against its new siblings — see [[design-navigation-tree-editing]].

### New-tab switch is hidden for non-link types

The **Open in new window** switch only applies to types that produce a real URL, so it is hidden for `group`, `mailchimp`, and `snippet`.

### Icon field is theme-gated

The **Icon** picker appears only when the active theme advertises `functions.navigations.icon.status = true`. The full gating mechanics (catalogue, theme-config flag) are on [[design-navigation-side-effects]].

## Related

- [[design-navigation]] — hub.
- [[design-themes]] — theme choice controls whether the icon field appears.

## Open questions

None.
