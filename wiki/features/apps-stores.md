---
type: feature
nav_path: "Apps → Local Pickup (Stores)"
route_name: apps.stores.overview
route_path: /admin/apps/stores
aliases: ["Stores", "Local Pickup", "Physical stores", "Pickup locations", "no enable disable button", "app has no active toggle"]
tags: [apps, stores, local-pickup, shipping, payment, physical-location]
plan_gates: ["stores"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Local Pickup (Stores)

## Purpose

**Local Pickup** (also titled "Stores" / "CloudCart Local Pickup") — adds **physical store locations** to the merchant's CloudCart store, enabling customers to:

1. See all physical store locations on a public storefront page (with working hours, address, phone, email, Google Map).
2. Pick **Local Pickup** as a shipping method at checkout (skip the courier entirely).
3. Pick **Pay on place** as a payment method (pay cash on pickup at the store).

This is the **hub page** for the Local Pickup cluster. The detail lives in the sub-pages listed below — drill into the one that matches the question rather than reading all of them.

Different from [[apps-store-locations]] (which is multi-warehouse INVENTORY with geo-zone routing). This app is customer-facing pickup-points + a shipping method + a payment method. Both can be installed together — they solve different problems and are not coupled (uninstalling one does not affect the other).

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **store location** — every location has its own active flag (an inactive location drops off the public stores page and the pickup picker), see [[apps-stores-main-locations]].

## Where to find it

Sidebar → Apps → install → **Local Pickup**. The route is `/admin/apps/stores` (Vue overview). The settings sub-route redirects to the legacy URL `/admin/stores` via a `RedirectOldApp` Vue wrapper — the actual management UI is the legacy Smarty flow. See also [[apps-stores-settings]] for the install/overview screen.

## What the merchant can do here

- Add **unlimited** physical store locations (title, URL handle, address, email, phone, working hours) — see [[apps-stores-main-locations]].
- Manage per-store product lists + quantities and the optional "Sum the quantities in the product" toggle — see [[apps-stores-main-stock]].
- Get a **Local Pickup** shipping method and a **Pay on place** payment method auto-installed — see [[apps-stores-main-shipping-payment]].
- Get an auto-generated public stores page listing every active location with a Google Map.

### What the merchant CANNOT do here
- Use Local Pickup without the new shipping + payment methods being auto-installed (the app does this).
- Configure courier-based shipping from this page — this is for pickup at the merchant's own physical locations only.
- Edit the public stores page layout from this app — it's auto-generated.
- Set per-location prices (one price per product across all stores) — see [[apps-stores-main-stock]].

## Settings & fields

The cluster's fields and settings are documented on the aspect pages:

- **Per-store location fields** (Title, URL handle, Store Address, Email, Phone, Work time, active flag, sort order, GPS coordinates) — see [[apps-stores-main-locations]].
- **Per-store products + quantity modal + "Sum the quantities in the product"** — see [[apps-stores-main-stock]].
- **Shipping + payment method records** the app installs — see [[apps-stores-main-shipping-payment]].

## Business rules

The defining cluster-level rules (each detailed on the aspect pages):

- Installing the app **auto-creates** a Local Pickup shipping method, a Pay on place payment method, and a public stores page — see [[apps-stores-main-shipping-payment]].
- Stock is tracked **per store** in addition to the master product quantity; a customer cannot pick Local Pickup for a product that is out of stock at the chosen store — see [[apps-stores-main-stock]].
- There is **no per-store pricing** — one price + one discount per product across all stores — see [[apps-stores-main-stock]].
- Deleting a store cascades to its address row and per-location shipping rates — see [[apps-stores-main-locations]].

### Permission
Standard apps permission scope.

### Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `stores` | Access gate (install URL) | The install URL `/admin/apps/stores/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

### Programmatic access

Physical store locations can be **read** via **JSON-API v2** — see [[api-stores]] for the endpoint and field map. The endpoint is **APP-GATED**: it returns 404 when the Stores (Local Pickup) app is not installed. Per-store stock is exposed through a SEPARATE resource — see [[api-store-quantity]] and [[apps-stores-main-stock]]. See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Sub-pages (in this cluster)

- [[apps-stores-main-locations]] — managing physical store locations: per-store fields, add/edit/delete, working hours, SEO URL handle, GPS / Google Map, active flag, sort order, delete cascade.
- [[apps-stores-main-shipping-payment]] — the auto-installed Local Pickup shipping method + Pay on place payment method, the auto-generated public stores page, and Click-and-Collect combinations.
- [[apps-stores-main-stock]] — per-store products + quantities, the "Sum the quantities in the product" toggle, out-of-stock pickup blocking, no per-store pricing, and the JSON-API per-store stock surface.

## Related

- [[apps]] — App Store hub.
- [[apps-stores-settings]] — the install / overview screen for this app.
- [[apps-store-locations]] — multi-warehouse inventory (different concept).
- [[shipping]] — Local Pickup appears as a shipping method.
- [[settings-payment-providers]] — Pay on place appears as a payment method.
- [[apps-stores-sync]] — multi-store catalog sync (different concept).
- [[products-products]] — products linked to stores.
- [[api-stores]] / [[api-store-quantity]] — JSON-API v2 read surface for stores + per-store stock.

## Open questions

None.
