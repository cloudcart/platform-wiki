---
type: feature
nav_path: "Settings → Shipping → Custom rate types"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Custom shipping rates", "Price based shipping", "Weight based shipping", "Price and weight shipping", "Local Pickup", "Marketplace shipping", "Different price for categories", "Free shipping threshold"]
tags: [settings, shipping, custom-rates, free-shipping, categories]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-shipping]]. See the hub for the other aspects (list & Add modal, edit panel, rate matching, lifecycle, API & permissions).

# Shipping — Custom rate types

## Purpose

When the merchant clicks **+ Add shipping method** and picks the **Custom** section, they choose one of four Custom rate **types**. The type drives which fields appear on the per-method edit panel (see [[settings-shipping-edit-panel]]) and is **permanent** — once chosen at creation, it cannot be changed.

This aspect catalogues the four type cards, their `type` keys, the type-is-permanent rule, the free-shipping pattern, the category-rate split, and the country-default recommendation logic.

## Where to find it

Settings → Shipping → **+ Add shipping method** → **Custom** section. See [[settings-shipping-list-and-add]] for the modal layout.

## What the merchant can do here

### The four Custom type cards

| Card | `type` key | Helper | What rates depend on |
|------|-----------|--------|---------------------|
| **Based on price** | `price` | *"This shipping method rates will depend on order subtotal"* | Order subtotal. |
| **Based on weight** | `weight` | *"Rates will depend of order total weight"* | Total cart weight. |
| **Based on price and weight** | `price_and_weight` | *"Rates will depend of order total price and weight"* | Both dimensions, nested. |
| **Local Pickup** | `marketplace` | *"Customers select a physical store to pickup their orders"* | No price/weight rates — the customer picks one of the merchant's [[apps-stores|Stores]] locations at checkout. |

Each card has its own icon. Clicking a card opens the per-type rate-config wide slide-in (see [[settings-shipping-edit-panel]]).

### Free-shipping pattern

There is **no global "Free shipping over X" master setting** on this page or in [[settings-cart]]. Free shipping is configured **per shipping method** by adding a rate row whose `amount = 0` and whose `from / to` brackets cover the desired order range.

The merchant's recipe:

1. Create a Custom shipping method (**Based on price**) — e.g., "Free over 100 BGN".
2. Add a single rate row: `from = 100`, `to = (blank)`, `amount = 0`.
3. Save.

At checkout, when the customer's subtotal crosses 100 BGN, this method becomes available with a 0 BGN shipping fee.

**Alternative pattern** — a method with multiple brackets where the highest bracket has `amount = 0`:

- `0-50 BGN: 5 BGN shipping`
- `50-100 BGN: 3 BGN shipping`
- `100+ BGN: free` (`amount = 0`)

The bracket-matching engine resolves overlaps by picking the cheapest matching rate — see [[settings-shipping-rate-matching]].

### Different price for categories

The per-method edit panel exposes a **Different price for categories** switch (`provider[use_price_category]`). When ON, a second rate-row block appears below labelled *"Category rates"* with its own `+ Add row` and its own brackets. The category rates apply only to products in the selected categories; the rest of the cart uses the default rate set. The merchant configures both sets through the same edit panel. See [[settings-shipping-edit-panel]] for the field detail.

### Country-default recommendations

Certain shipping methods are tagged as **Recommended** based on the store's [[settings-general]] operation country. The "Browse shipping integrations" section also filters its app list by that country. The merchant cannot override either from the list; to access integrations for other countries, they would need to change the operation country in [[settings-general]] (which has cascade effects on language / currency / etc.).

## Settings & fields

| Field | Where it lives | What it does |
|-------|---------------|--------------|
| `type` (`price` / `weight` / `price_and_weight` / `marketplace`) | Created at Add time; not editable afterwards. | Drives which rate-bracket fields appear on the edit panel. |
| `provider[use_price_category]` | Edit panel — *"Different price for categories"* switch. | Enables the second rate-row block scoped to specific product categories. |

## Business rules

### Type is permanent

The Add modal explicitly warns: *"Choose the shipping method type. You cannot change this after a type has been chosen."* To switch types, the merchant must delete the method (subject to the orders-attached delete protection — see [[settings-shipping-lifecycle]]) and recreate it.

### Local Pickup requires the Stores app

The **Local Pickup** card appears only when the [[apps-stores]] (Stores) app is installed AND no marketplace provider already exists. Without the Stores app, the card is hidden. Local Pickup depends on the merchant's physical store locations being defined first. See [[settings-shipping-list-and-add]] for the card visibility logic.

### Free shipping is a `$0` rate, not a separate setting

The merchant cannot toggle a single "Enable free shipping" boolean — it is always expressed through a rate row. This keeps free-shipping eligibility consistent with the rest of the bracket matcher (zone matching, allowed-payments gating, bracket inclusivity, cheapest-wins on overlap — see [[settings-shipping-rate-matching]]).

### Integration-backed methods bypass the Custom rate config

For integration-backed providers (Speedy, Econt, DHL, GLS, etc.), the shipping rates come from the integration's own pricing rules / live API. The merchant cannot edit individual rate rows for an integration-backed method directly from the Shipping list — they configure the carrier through the app's own settings page. The Custom rate-row UI applies only to the four `type` keys above.

## Related

- [[settings-shipping]] — hub.
- [[settings-shipping-list-and-add]] — where the four type cards live in the Add modal.
- [[settings-shipping-edit-panel]] — per-method rate-config side panel (where rate rows and **Different price for categories** are configured).
- [[settings-shipping-rate-matching]] — how the bracket matcher resolves overlapping rates (cheapest wins).
- [[apps-stores]] — required for the `marketplace` (Local Pickup) type.
- [[settings-general]] — operation country drives **Recommended** badges and the integrations filter.
- [[settings-cart]] — there is NO global free-shipping threshold here either.

## Open questions

_None._
