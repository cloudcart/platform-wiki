---
type: feature
nav_path: "Apps → Local Pickup → Settings"
route_name: apps.stores.settings
route_path: /admin/apps/stores/settings
aliases: ["Stores Settings", "Local Pickup Settings"]
tags: [apps, administration, stores, local-pickup, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Local Pickup → Settings

## Purpose

The **Settings** route for [[apps-stores]] (Local Pickup) — currently REDIRECTS to the legacy `/admin/stores` URL via the `RedirectOldApp` Vue wrapper. The actual management UI is Smarty-based at `/admin/stores`. See [[apps-stores]] for the full feature set.

## Where to find it

Sidebar → Apps → Local Pickup → **Settings**. Route: `/admin/apps/stores/settings`. Redirects to `/admin/stores`.

## What the merchant can do here

The redirect lands the merchant on the legacy `/admin/stores` management page where they:
- Add new physical store locations.
- Edit existing locations (Title / URL / Address / Email / Phone / Work time per [[apps-stores]]).
- Configure SEO per store.
- Manage per-store product inventory.
- View / edit the Local Pickup shipping method + Pay on place payment method (auto-installed by [[apps-stores]]).

### What the merchant CANNOT do here
- Stay in the modern Vue UI — Settings auto-redirects to legacy.

## Settings & fields

Settings are handled by the legacy `/admin/stores` page. See [[apps-stores]] for the comprehensive list of per-store fields.

## Business rules

### Modern Vue placeholder

The modern Vue at `/admin/apps/stores/settings` is a redirect wrapper — actual functionality has not been migrated to modern Vue yet. The merchant works in the legacy UI.

### Modern URL routes to legacy via wrapper

The route exists in modern Vue but its component is a `RedirectOldApp` wrapper — it doesn't render any UI; it just redirects to the legacy `/admin/stores` URL where the Smarty-based stores management lives. So opening the settings URL from modern admin causes a full page navigation, not a Vue-internal route change.

### Settings UI is the per-store add/edit form, not a global settings panel

Unlike other app Settings pages, this page does NOT host a global settings form (translate toggles, AI keys, etc.). All "settings" for Local Pickup are per-store records (title, address, work time, products) plus one global setting: the *"Sum the quantities in the product"* checkbox documented on [[apps-stores]]. There's no other store-wide config.

### Permission
Standard apps permission scope.

## Related

- [[apps-stores]] — Local Pickup hub.
- [[apps-store-locations]] — distinct concept (multi-warehouse inventory).
- [[shipping]] — Local Pickup appears as shipping method.
- [[settings-payment-providers]] — Pay on place appears as payment method.

## Open questions

No outstanding questions.
