---
type: feature
nav_path: "Apps → Grocery Store → Settings"
route_name: apps.grocery_store.settings
route_path: /admin/apps/grocery_store/settings
aliases: ["Grocery Store Settings", "Grocery layout settings", "Grocery store config"]
tags: [apps, administration, grocery, storefront-mode, settings]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 1
---
# Grocery Store → Settings

## Purpose

The **Settings** tab is where the merchant configures the **grocery-store layout behaviour** on the storefront. Different from regular e-commerce, grocery storefronts are optimised for:
- Many items per cart (10-30+ items).
- Per-unit price display (price per kg / per liter / per piece).
- Inline +/− quantity controls on category listings.
- Substitution preferences when items are out of stock.
- Recurring orders for staples.

For the full Grocery Store feature set, see [[apps-grocery-store-overview-new]].

## Where to find it

Sidebar → Apps → Grocery Store → **Settings tab**. Route: `/admin/apps/grocery_store/settings`.

## What the merchant can do here

### Layout settings

Configurable per the platform's grocery defaults (from `Bgn2EurManager`-style configuration — verify):

| Setting | Notes |
|---|---|
| **Categories per row** | Grid density on category browsing pages (3 / 4 / 6). |
| **Show unit price** | Display price per unit (kg / liter / piece) alongside package price. |
| **Inline quantity controls** | Show +/− buttons inline on listing cards. |
| **Real-time cart update** | AJAX cart update on quantity change (vs page reload). |

### Substitution rules

| Setting | Notes |
|---|---|
| **Allow substitutions** | Whether out-of-stock items can be substituted at fulfillment. |
| **Customer chooses substitution** | When ON, customer picks accepted substitutes at checkout. When OFF, merchant decides. |

### Recurring orders

| Setting | Notes |
|---|---|
| **Enable recurring orders** | Customer can set up auto-renewing baskets. |
| **Default frequency** | Weekly / fortnightly / monthly. |

### Delivery time slots

| Setting | Notes |
|---|---|
| **Use Shipping Hours** | Whether to require time-slot selection at checkout (per [[apps-shipping-hours]]). |
| **Default slot duration** | 1-hour / 2-hour / 4-hour windows. |

### What the merchant CANNOT do here
- Disable the grocery layout per category — the layout is store-wide.
- Mix grocery + non-grocery layouts (use multi-store for that).
- Set per-category substitution rules — substitution is store-wide.

## Settings & fields

Per [[apps-grocery-store-overview-new]] Manager: `getDefaults` returns the default configuration. Settings persist as a JSON object on the app instance.

## Business rules

### Layout = storefront-wide switch

Activating Grocery Store changes the storefront template store-wide. To revert, the merchant uninstalls. Cannot be enabled per-category.

### Unit price requires weight / unit data

For unit-price display to work, products must have weight (per [[settings-boxes]]) + unit-of-measure data populated. Without these, the storefront falls back to package price only.

### Permission
Standard apps permission scope.

## Related

- [[apps-grocery-store-overview-new]] — hub page.
- [[apps-grocery-store-overview-new]] — modern Vue overview (if separate).
- [[apps-shipping-hours]] — delivery time slots integration.
- [[products-products]] — products with weight + unit data.
- [[orders-subscriptions]] — recurring orders.

## How it works (verified against backend)

### "Settings" here = the unit-of-measure table

The Grocery Store app does not have a traditional settings page with toggles for layout, substitutions, recurring orders, or time slots. The settings surface is a **unit-of-measure manager**: the merchant adds, edits and deletes units (kg, g, m, cm, liter, ml, pieces, bunches, etc.) and assigns those units to their products.

For the complete list of capabilities (the unit tree, the storefront short-name fallback, the `action_after_add_to_cart` change on install, etc.), see [[apps-grocery-store-overview-new]].

### `getDefaults` returns metric or imperial tree

`getDefaults` reads the merchant's `unit_system` site setting:

- `metric` (default for most CloudCart stores) — returns the kg / g / mg, m / cm / mm, l / ml hierarchy.
- anything else (typically `imperial`) — returns pound / ounce, yard / foot / inch, gallon / quart / pint / fluid ounce hierarchy.

These defaults are seeded once during install (only if no units exist yet); the merchant is free to add custom units or delete unused defaults afterwards.

### Per-category, per-mobile, multi-store: not configurable here

The unit list is **store-wide**. There is no per-category override (every category can use any unit). There is no separate mobile vs desktop unit setting. There is no per-storefront separation when running multiple stores via [[apps-stores]] — each CloudCart store has its own units, but the same units table applies to every category and every theme on that store.

### Per-unit fields

For each unit, the merchant configures:

- **Name** — internal full name (e.g., "Kilogram"). Required, max 191 characters. Validation: *"Name is required"* / *"Name max 191"*.
- **Short name** — abbreviation shown on the storefront (e.g., "kg"). Required, max 191 characters.
- **Parent unit** — optional. Picking a parent makes this unit a sub-unit (e.g., gram is a sub-unit of kilogram).
- **Steps per parent** — required only when a parent is set. Numeric, non-zero, up to 3 decimals (e.g., 1000 grams in 1 kilogram; 16 ounces in 1 pound). Validation messages exist for each rule (numeric / not-in-zero / regex / required-with).
- **Decimals** — integer 0 to 3. Controls how the storefront formats fractional unit values (e.g., 0.250 kg for produce sold to 3 decimals).

### POS integration

The Grocery Store app does not register a POS hook. Integrations such as [[apps-microinvest]] / [[apps-posmaster]] each define their own product mapping. They will use the unit ids and values stored on products / variants when syncing, but there is no settings panel inside this app that controls POS behaviour.

### Cache cleared on save

Saving a unit clears the product cache, so storefront caches refresh immediately on the next request — the merchant does not need to manually clear anything.

## Open questions

