---
type: feature
nav_path: "Design → Modules → Navigation → User controls"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["User controls module", "userControls", "user.controls", "Account icons module", "Login icon module", "Customer account module", "Модул потребителски икони"]
tags: [design, modules, navigation, header, user, account]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — User controls (`userControls`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **User controls** module renders the customer's account / login / logout icons in the header. The exact icons shown depend on the customer's authentication state:

- **Guest customer** (not logged in) → **Login** icon.
- **Logged-in customer** → **My Account** icon + **Logout** icon.

The module has no merchant-editable settings — content is fully driven by the auth state plus the active theme's translation strings. It's a SYSTEM module, injected by the module helper even when the active theme doesn't declare it in its `theme.json`.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Header — usually top-right, near the search icon and cart icon |
| Admin edit card | None — the module has no card on the Modules screen |
| Auth / customer-account settings | [[settings-cart]] (customer-access permissions, guest checkout) |
| Login / registration routes | `site.auth.login`, `site.auth.logout`, `site.account` |

The underlying module mapping is `user.controls`; the instance name is `userControls`. The module is in the platform's hard-coded `system_widgets` list.

## What the merchant can do here

Because this module has no Modules-screen card, the merchant configures it indirectly:

- **Disable guest customer-access entirely** in [[settings-cart]] — when `customer_access = guest`, the login icon is suppressed and the account routes return 404 / not-allowed errors.
- **Pick a header template** in **Header settings** (`headerConfiguration`) that hides or repositions the user-controls slot.
- **Customise the icon set** via theme CSS — the icons render with hard-coded FontAwesome classes (`fa fa-user`, `fa fa-sign-in`, `fa fa-sign-out`); merchants who want different glyphs ask CloudCart for theme customisation.

What the merchant CANNOT do:

- Hide the login icon for guests but keep the account icons for logged-in customers — they share the same module slot.
- Replace the link target — clicking "My Account" always goes to `site.account` route, clicking "Login" always goes to `site.auth.login`, clicking "Logout" always goes to `site.auth.logout`.
- Add a "Register" icon next to "Login" — the theme template only renders Login; merchants who want a separate Register link use [[design-module-navigation-links]] with an `external` link to `/auth/register`.
- Add a wishlist or cart icon to this slot — those are separate modules, rendered nearby by the theme.

## Settings & fields

The `user.controls` module has NO merchant-editable settings (no restrictions array, no defaults array). It reads its rendering data at request time from:

| Read from | Value | Notes |
|-----------|-------|-------|
| the platform code | `guest` or `customer` | Suppresses the icon list when customer access is `guest`-mode disabled |
| the platform code | bool | Determines whether to render Login vs My Account + Logout |
| Translation keys | `sf.global.act.my_account`, `sf.global.act.logout`, `sf.global.act.login` | Icon labels (per-language via `multylang`) |

There are no form fields, no Save button, no Reset button — the module is purely auth-driven.

### Theme-specific notes

- **`knowledge-freedom` theme uses light FontAwesome icons** (`fal fa-user` / `fal fa-sign-in` / `fal fa-sign-out`) instead of the solid set (`fa fa-...`). The template branches on `site('template') == 'knowledge-freedom'` for this. Other themes use the solid icons.
- **Mobile placement varies.** Some themes group the user controls into a hamburger / mobile drawer; others always render them inline in the header. Theme-controlled.
- **Login as an AJAX panel.** The Login link in most themes is rendered with `data-ajax-panel="true"` — clicking opens the login form in a slide-in side panel instead of navigating away. Merchants on themes with this attribute get a smoother login UX.

## Business rules

### Auth-state determines content — no merchant override

The module always renders Login (guest) or My Account + Logout (logged-in). The merchant cannot override the conditional or force one icon to show regardless of auth state.

### `customer_access = guest` mode hides the icon list

When the merchant disables customer accounts in [[settings-cart]] (the platform code returns `false`), the module hides the icon list entirely — there's no Login icon, no Account icon. The store still works for guest purchases.

### System module — always available

`userControls` is in the hard-coded `system_widgets` list and is injected by the module helper. Even themes that don't declare it in `theme.json` get it. The merchant never has to enable the slot.

### No save / reset surface

Because there's no Modules-screen card, there's no Save / Reset / Cancel pipeline. The only "configuration" surface is [[settings-cart]] (guest mode toggle) and theme CSS (icon styling).

### Login redirects via `intended` session

When a guest tries to access a logged-in-only route, the platform stores the original URL in `session('intended')`. After login, the customer is redirected to that URL. The Login icon does NOT directly support deep-linking — it just opens the login form / panel.

### Logout invalidates customer session

Clicking Logout fires the `site.auth.logout` route which clears the customer's auth guard and redirects to the homepage.

### Cache invalidation

Because the module is auth-state-driven, it's rendered fresh per request and NOT cached. The storefront cache key system bypasses this module — there's no cached output to invalidate.

### No plan-gating

`user.controls` is not in the `paid_widgets` allowlist — available on every plan.

### Per-language labels via multylang

When `multylang` is installed, the icon labels (Login / My Account / Logout) translate per the customer's selected language. The translation keys are platform-level and not per-store editable.

## Related

- [[design-modules-navigation]] — hub.
- [[settings-cart]] — customer-access permissions (guest checkout toggle).
- [[design-module-navigation-links]] — alternative for adding a Register link or custom account-shortcut links.
- [[settings-general]] — store name (used as `alt` fallback in some themes).
- [[design-modules]] — parent module catalogue.

## Open questions

- ⏸️ **Per-theme AJAX panel.** Confirm which themes render the Login link as an inline AJAX panel vs a full-page navigation. UX-relevant for support troubleshooting "why is my login slow".
- 📡 **Wishlist icon adjacency.** Themes that support wishlist render its icon next to `userControls`. GraphQL-resolvable: query whether the wishlist app is enabled and which themes co-render it.
- ⏸️ **Knowledge-freedom font variant.** Verify whether the light-FontAwesome treatment in `knowledge-freedom` is intentional or a remnant of a theme migration.
