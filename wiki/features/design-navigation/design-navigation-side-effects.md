---
type: feature
nav_path: "Design → Navigation → Side-effects"
route_name: admin.navigation.list
route_path: /admin/storefront/navigation/{group?}
aliases: ["Navigation side-effects", "Menu cache invalidation", "boarding_menus", "Navigation icon support", "Navigation permission", "Странични ефекти на навигацията"]
tags: [design, navigation, menus]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Navigation — save-time side-effects

> Part of [[design-navigation]]. See the hub for the other aspects (item types, item fields, tree editing, menu groups, link resolution).

## Purpose

Every save / edit / delete / reorder on the Navigation screen triggers a set of side-effects that the merchant does not see directly but that explain behaviour they DO observe — the storefront menu updating within seconds, the onboarding checklist ticking off, and the theme-gated icon picker appearing or disappearing. This page collects those side-effects plus the access requirement for the screen.

## Where to find it

These behaviours fire automatically on any change under Sidebar → **Design** → **Navigation**. There is no dedicated screen for them; the merchant observes their effects on the storefront and on the [[dashboard]] checklist.

## What the merchant can do here

- Rely on the storefront menu reflecting any change within seconds, with no manual cache-clear step.
- Complete the "set up your menus" onboarding step simply by adding or editing one menu item.
- Attach a Font Awesome icon to a menu item — but only on themes that advertise icon support.

## What the merchant cannot do here

- Manually clear the menu cache — there is no cache-clear button; regeneration is automatic.
- Re-tick or un-tick the onboarding flag directly — it is a side-effect of saving a menu item.
- Show the icon picker on a theme that does not advertise `functions.navigations.icon.status` — the field is hidden.
- Access the screen without the storefront-design permission in their staff role.

## Settings & fields

This aspect surfaces no merchant-editable fields. The only user-visible control governed here is the **Icon** picker on the item form, whose appearance is gated by the active theme's `functions.navigations.icon.status` flag (the field itself is documented on [[design-navigation-item-fields]]).

## Business rules

### Cache invalidation on every save

Every save / delete / reorder regenerates the merchant's site cache key, which forces the storefront to rebuild the cached menu HTML on the next request. There is no manual cache-clear button — the storefront picks up changes within seconds.

### Onboarding flag side-effect

Successfully adding or editing a menu item sets the merchant-level setting `boarding_menus = 1` — this marks the "set up your menus" onboarding step as complete on the merchant's [[dashboard]] checklist.

### Icon support is theme-gated

The **Icon** picker only appears in the form when the active theme advertises `functions.navigations.icon.status = true` in its theme config. Themes that don't advertise this (e.g., a theme using only text menus) hide the field entirely. The icon catalogue is the platform's bundled Font Awesome library (Pro / Regular). Theme choice is set on [[design-themes]].

### Permission

Access to the Navigation screen requires the storefront-design permission within the merchant's staff role (verify the exact key in [[settings-staff]]).

## Related

- [[design-navigation]] — hub.
- [[design-themes]] — theme config flag governs the icon picker.
- [[settings-staff]] — staff role permission required to access the screen.
- [[dashboard]] — onboarding checklist that the `boarding_menus` flag ticks off.

## Open questions

- 📡 **Multi-language menus.** With `multylang` installed, each menu item carries per-language `name` translations via the language switcher. GraphQL-resolvable: query whether the `multylang` app is installed on this merchant's store.
