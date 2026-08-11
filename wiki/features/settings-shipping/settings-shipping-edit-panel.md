---
type: feature
nav_path: "Settings → Shipping → Edit panel"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping method edit panel", "Shipping rate config", "Rate rows", "Insurance shipping", "Allowed payment methods shipping", "Geo zone shipping", "Postal money order shipping", "Rate bracket auto-fill"]
tags: [settings, shipping, edit-panel, rate-rows, geo-zones, payments]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-shipping]]. See the hub for the other aspects (list & Add modal, Custom rate types, rate matching, lifecycle, API & permissions).

# Shipping — per-method edit panel

## Purpose

When the merchant clicks a Custom rate card (from the Add modal — see [[settings-shipping-list-and-add]]) or clicks an existing Custom method's row name from the list, a wide slide-in panel opens for **rate-config**. This aspect documents the panel's layout, every field (with verbatim setting keys), the rate-bracket auto-fill quirk, and the marketplace / N18 Audit conditional sections.

For integration-backed methods (Speedy, Econt, DHL, GLS, etc.), clicking the row name opens the integration's own app settings page instead — the Custom edit panel below applies only to the four Custom `type` keys (see [[settings-shipping-custom-rates]]).

## Where to find it

Settings → Shipping → click a Custom rate card from the Add modal, OR click an existing Custom method's row name.

The panel title reads *"Create new shipping method"* (Add) or the method's name (Edit). The header has **Cancel** and **Save** buttons fixed at the top.

## What the merchant can do here

### Layout — top-to-bottom

| Block | Field | Notes |
|-------|-------|-------|
| **Top row** | **Provider name** (`provider[name]`) | Required. Helper: *"This is what your customer will see at checkout"*. |
| | **Description** (`provider[description]`) | Free text, 3-row textarea. Tooltip: *"This is what your customer will see at checkout"*. Hidden for marketplace type. |
| **Insurance + Logo row** | **Insurance** (`has_insurance` switch + `provider[insurance]` percent) | Switch ON enables a 0–100 percent input with the **%** suffix. Helper: *"may increase the shipping rate"*. Hidden for marketplace. |
| | **Logo** (image upload) | PNG/JPG drop-zone. |
| **Postal money order** (when [[apps-n18-audit]] / N18 Audit installed) | **Use postal money order** switch | Optional Bulgarian-postal toggle. Only appears when the N18 Audit app is installed. |
| **Regions** | **The whole world** switch (`provider[target] = restofworld`) | When ON, hides the Geo zone dropdown below. Helper: *"This shipping method will be available everywhere"*. |
| | **Geo zone** dropdown (`provider[geo_zone_id]`) | When the world switch is OFF, the dropdown lists all defined [[settings-geo-zones]] for the merchant to pick exactly one. |
| **Allowed payment methods** | **Allow all payment methods** switch (`payments_all`) | When ON (default), the multi-select below is disabled (greyed out) and the method works with every payment provider. |
| | **Payment providers** multi-select (`payments_providers[]`) | When the switch is OFF, lists every active payment provider's storefront name; the merchant picks one or more. |
| **Rate rows** (Price / Weight / Price-and-weight types only) | **Order rate** brackets | Per row: **from** (price OR weight) → **to** (or `∞` blank for no upper bound) → **amount**. Amount is in store currency. Tooltip on the header: *"Both boundaries are inclusive — when an order value sits on a boundary, the cheaper rate is chosen"*. **+ Add row** at the bottom auto-fills the new row's `from` with the previous row's `to`, preventing gaps. Trash icon on each row except the first deletes it. |
| **Different price for categories** | Switch (`provider[use_price_category]`) | When ON, a second rate-row block appears below labelled *"Category rates"* with its own `+ Add row` and its own brackets, applied only to products in the selected categories. |
| **Marketplace (Local Pickup)** | **Marketplaces** multi-select (`provider[marketplaces]`) | Only on `type = marketplace`. Lists every physical store ([[apps-stores]]) that has an address. The customer picks one of these as the pickup point at checkout. |

Saving submits the form via `ajaxForm` — validation errors render inline next to the offending input; successful save closes the panel and refreshes the list.

### Rate bracket auto-fill quirk

When the merchant clicks **+ Add row** for a new bracket, the JS reads the previous row's `from`/`to`, then sets:

- the new row's `from = previous.to`
- and `to = from + (to - from)` (preserves the previous bracket's width).

Special cases:

- If the previous row's `to` is empty (open upper bound), the click is a **no-op** (focus jumps to the empty `to` field).
- If `to <= from`, the click is also a **no-op**.

This auto-stitching keeps brackets contiguous without the merchant having to type the next `from` value manually.

### Free shipping via rate rows

A rate row with `amount = 0` effectively makes that bracket free shipping. See [[settings-shipping-custom-rates]] for the "Free over X" pattern recipe and [[settings-shipping-rate-matching]] for how the cheapest-on-overlap rule resolves edges.

## Settings & fields

The exhaustive field map for the edit panel:

| Setting key | Verbatim | Where rendered | What it does |
|-------------|----------|---------------|--------------|
| `provider[name]` | Provider name | Top row | Customer-facing label at checkout. Required. |
| `provider[description]` | Description | Top row | Short blurb at checkout. Hidden on marketplace. |
| `has_insurance` | Insurance switch | Insurance row | Toggles the percent input. |
| `provider[insurance]` | Insurance percent | Insurance row | 0–100, with `%` suffix. Hidden on marketplace. |
| `provider[target] = restofworld` | The whole world | Regions block | When ON, hides the Geo zone dropdown. |
| `provider[geo_zone_id]` | Geo zone | Regions block | One zone from [[settings-geo-zones]]. |
| `payments_all` | Allow all payment methods | Payments block | Switch — when ON the multi-select is disabled. |
| `payments_providers[]` | Payment providers | Payments block | Multi-select when `payments_all` is OFF. |
| `provider[use_price_category]` | Different price for categories | Rate rows block | Reveals the second "Category rates" block. |
| `provider[marketplaces]` | Marketplaces | Marketplace block | Multi-select of [[apps-stores]] locations on `type = marketplace`. |
| _(N18)_ Use postal money order | Postal money order | Conditional | Only when [[apps-n18-audit]] is installed. |

## Business rules

- **One geographic scope per row** — either `provider[target] = restofworld` or a single `geo_zone_id`. The "The whole world" switch hides the dropdown; toggling back OFF re-shows it. (verify whether `target` enum has values beyond `restofworld` / `regions`.)
- **Allowed payment methods restricts checkout pairings** — when `payments_all = no` and the merchant picks a subset, the method only appears at checkout if the customer's chosen payment provider is in that subset. This is one of the four storefront-visibility gates (see [[settings-shipping-rate-matching]]).
- **Rate-row brackets are contiguous by design** — the auto-fill quirk pre-populates `from` from the previous row's `to`. Gaps are still possible if the merchant manually edits the `from` value, but the default click behaviour prevents them.
- **Category rates ride alongside the default rate set** — when `provider[use_price_category] = yes` and a cart contains products from a category for which a category-specific rate set exists, the category rate applies to those products' contribution; the rest use the default rate set.
- **`Description` and `Insurance` are hidden for marketplace methods** — the storefront pickup-flow UX doesn't render a description blurb or a percentage insurance, so the merchant doesn't see those fields when `type = marketplace`.
- **Postal money order toggle requires N18 Audit** — the field surfaces only on stores with the [[apps-n18-audit]] (Bulgarian fiscalisation) app installed.

## Related

- [[settings-shipping]] — hub.
- [[settings-shipping-list-and-add]] — where the edit panel opens from.
- [[settings-shipping-custom-rates]] — the four Custom `type` keys that drive which fields appear here.
- [[settings-shipping-rate-matching]] — how the rate rows resolve at checkout (both ends inclusive, cheapest wins).
- [[settings-geo-zones]] — populates the **Geo zone** dropdown.
- [[settings-payment-providers]] — populates the **Payment providers** multi-select.
- [[apps-stores]] — populates the **Marketplaces** multi-select for `type = marketplace`.
- [[apps-n18-audit]] — adds the **Postal money order** switch.

## Open questions

_None._
