---
type: feature
nav_path: "Apps → Grocery Store"
route_name: apps.grocery_store.overview.new
route_path: /admin/apps/grocery_store-new
aliases: ["Grocery Store Overview (modern)", "Grocery Store new", "Grocery overview new", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, grocery, storefront-mode, overview, modern-vue]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Grocery Store → Overview (modern Vue)

## Purpose

The **modern Vue version** of the Grocery Store overview page — replaces the legacy [[apps-grocery-store-overview-new]] with a refreshed UI in CloudCart's CcDomain pattern (modern Vue + TypeScript). Same conceptual functionality: shows install state + capabilities + quick actions for the Grocery Store app.

For the full Grocery Store feature set, see [[apps-grocery-store-overview-new]] (legacy) — content is equivalent.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → Grocery Store (when the new Vue is in use). Route: `/admin/apps/grocery_store-new`.

The path `grocery_store-new` distinguishes it from the legacy `/admin/apps/grocery_store` route.

## What the merchant can do here

- See the app's metadata + install state.
- Trigger Install / Uninstall.
- Read capability summary.
- Navigate to [[apps-grocery-store-settings]] for configuration.

### What the merchant CANNOT do here
- Configure layout-specific settings — those are in the Settings tab.

## Settings & fields

The modern Vue uses CloudCart's `CcSettingsBox` / `CcCard` design system. The fields exposed are equivalent to the legacy overview but with modern UX patterns (better mobile, accessibility improvements).

## Business rules

### Modern Vue vs legacy

Some merchants may see the legacy [[apps-grocery-store-overview-new]] while others see this modern version — depending on rollout. Eventually the legacy is deprecated.

### Permission
Standard apps permission scope.

## Programmatic access

Units of measure can be **read** via **JSON-API v2** — see [[api-units]] for the endpoint and field map. The endpoint is **APP-GATED**: it returns 404 when the Grocery Store app is not installed (the units table itself only seeds on install).

The API surface is **read-only**: integrations can enumerate the unit tree (root units, sub-units with conversion factors, storefront names) but cannot add, edit, or delete units through the API — those operations live in the admin panel.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

- [[apps-grocery-store-overview-new]] — legacy version (same content).
- [[apps-grocery-store-settings]] — Settings tab.
- [[products-products]] — grocery products with weight / unit data.

## How it works (verified against backend)

### What the app actually adds: units of measure for products

Despite descriptions implying a "grocery storefront layout", this app **does not change the storefront theme**. It does exactly two things on install:

1. Forces the cart-flow setting `action_after_add_to_cart` to `stay_on_page` — so when the customer adds an item, they stay on the listing instead of being navigated to the cart. This is the grocery-style behaviour where the customer adds many items in a row without leaving the page.
2. Seeds a hierarchical **units-of-measure** table with sensible defaults for the merchant's `unit_system` (Bulgarian / European stores get **metric**; US-style stores get **imperial**).

After install, products and variants gain a unit assignment (`unit_id` + `unit_value`) so the merchant can sell a product per-kilogram, per-meter, per-liter, per-ounce, etc., with decimal steps. This is the **whole** feature surface — there are no substitution rules, no recurring orders, no time-slot configuration, no per-category opt-out toggles, no "grocery layout" templates baked in.

### Default unit tree

The defaults shipped per `unit_system`:

**Metric (default for most CloudCart stores)**:

- Mass — Kilogram (3 decimals) → Gram (3 decimals, 1000 per kg) → Milligram (0 decimals, 1000 per g).
- Length — Meter (2 decimals) → Centimeter (1 decimal, 100 per m) → Millimeter (0 decimals, 10 per cm).
- Volume — Liter (2 decimals) → Milliliter (0 decimals, 1000 per l).

**Imperial**:

- Mass — Pound (2 decimals) → Ounce (0 decimals, 16 per lb).
- Length — Yard (2 decimals) → Foot (1 decimal, 3 per yd) → Inch (0 decimals, 12 per ft).
- Volume — Gallon (2 decimals) → Quart (1 decimal, 4 per gal) → Pint (0 decimals, 2 per qt) → Fluid ounce (0 decimals, 16 per pt).

The merchant can add custom units (e.g. "bunch", "dozen", "carton") with a name, short name, parent unit, steps-per-parent and decimal places. Custom units inherit a parent and define how many child units fit into one parent (the `steps` field).

### Steps field validation

When the merchant adds a unit with a parent, the `steps` field becomes required. Validation rules:

- Must be numeric.
- Cannot be zero.
- Up to **3 decimal places** is allowed in the value (regex `^(\d+)(\.([\d]{1,3}))?$`).
- Decimals (rounding precision) on the unit itself is **0 to 3**.

If the unit has no parent it's a top-level unit and `steps` defaults to 1.

### Cannot delete a unit that is in use

`allowDelete` checks whether any product or variant currently references the unit (or any descendant unit). If yes, deletion is blocked. Deleting a top-level unit also deletes its child sub-units.

### Storefront name fallback

Each unit can have an internal **name** (e.g., "Kilogram") and a **short_name** (e.g., "kg"). The storefront displays the short name when present; otherwise the full name. The merchant chooses what shows under the price (e.g., "5.99 BGN / kg").

### Caching

Unit tree and step lookups are cached in memory so per-request reads don't re-hit the database. When the merchant adds / edits / deletes a unit, the product cache is cleared so the storefront picks up the change immediately.

### Why "Grocery Store"

The name reflects the original use case (selling meat / produce by weight, milk / oil by volume, fabric / wire by length). The same units also serve hardware stores, fabric stores, fuel stations or any retailer who needs to sell by measure rather than per piece. The app does not lock the merchant into a "grocery" theme — it simply adds the unit infrastructure that grocery-style merchants need.

### Install hook forces a global setting change
On install, the integration directly writes `action_after_add_to_cart = 'stay_on_page'` to the store's general settings — overwriting whatever the merchant had configured before. Uninstalling the app does NOT restore the previous value; the setting stays at `stay_on_page` until the merchant manually changes it in [[settings-cart]].

So a side-effect of installing Grocery Store is that the merchant's cart behaviour changes globally — even if they only wanted the unit-of-measure functionality. The merchant should be aware before installing.

### Install-time defaults are seeded only when the units table is empty
The platform code call respects existing rows — if the merchant has already configured custom units (e.g., from a previous install), the defaults are NOT re-seeded. So uninstalling and re-installing the app does not double-up the unit tree.

### `unit_system` site setting selects the seeded tree
The seed picks the **metric** tree by default; only stores with `unit_system != 'metric'` get the **imperial** tree. The merchant's `unit_system` value is read once at install time — switching it later does not retroactively swap the unit tree.

### Icon is shared with Domain Redirect
The app's icon (`icon-domain-redirect.png`) is accidentally shared with the Domain Redirect app — a known visual artefact, not a functional issue. The merchant sees identical tile artwork for the two apps in the App Store; the names + descriptions differentiate them.

## Open questions

