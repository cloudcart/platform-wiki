---
type: feature
nav_path: "Products → Options → Add / Edit → price impact"
route_name: apps.product_options.edit.new
route_path: /admin/products/options-new/:type/:id?
aliases: ["Product option pricing", "Option price impact", "Option price calculation", "Цена на опция"]
tags: [apps, products, options, pricing, customisation]
plan_gates: ["product_options"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-options-overview]]. See the hub for the other aspects (types, assignment, order handling).

# Product Options — price impact

## Purpose

Controls **how much an option adds to (or subtracts from) the line total** when the customer selects it. The price-impact controls appear in the General settings card of the Add / Edit option form, and which ones show depends on the [[products-options-types|Field type]]. Options can be informational (no price impact), add a flat amount, scale by a percentage, or charge per measured unit.

## Where to find it

Sidebar → Products → **Options** → **+ Create new option** (or edit) → **General settings** card → the price-impact controls below the Field type.

## What the merchant can do here

- Set a flat amount, a percentage, or a per-measure price for the option.
- Choose whether the price applies once per line or per unit of quantity.
- For length / square, set the unit, a rounding step, and whether to allow ordering below the base price.

## Settings & fields

The form shows a different subset of controls per type:

| Field | Type / options | Shown for |
|-------|----------------|-----------|
| **Calculate the price for each** (`per_item`) | Toggle | radio, select, checkbox, image, text, textarea, file. Auto-set to 1 on save for length / weight / square. |
| **Type of the value** | Dropdown — % or currency-symbol (fixed) | radio, select, checkbox, image (per-value amounts). |
| **Apply over** | Dropdown — Regular price / Discounted price | Shown only when Type of the value = %. |
| **Type of the value** (inline amount + type pair) | Amount input + amount-type dropdown | text, textarea, file (single global price for the option). |
| **The price is determined based on** | Length-unit dropdown (Meter / Centimetre / Millimetre / Kilometer) | length, square. |
| **Option unit** | Length-unit dropdown (same options) | length, square. |
| **Round to size** | Numeric (min 0, step 0.001) — sets `min_square` | length, square. |
| **Allow the purchase of a value less than the price of the product** | Toggle — sets `allow_negative` | length / square ONLY when the two unit selects differ. |
| **Per-value Amount** | Numeric per row in the Values editor | radio, select, checkbox, image. |

## Business rules

### Price-impact mechanics (verified)

Each option — and each value within select / radio / checkbox — carries:

- **amount** — the numeric price impact.
- **amount_type** — flat / percent / per-quantity.
- **per_item** — when true, the price impact is multiplied by line quantity. Auto-set to 1 for length / weight / square (you pay per metre of cable × number of cables).
- **allow_negative** — permits negative amount values (rare; for option-driven discounts).
- **apply_over_price_type** — whether the option price applies over the base price or replaces it (configurable on the form via **Apply over**).
- **product_symbol / value_symbol** — UI labels next to the amount (e.g. "BGN", "EUR", "%", "kg").
- **min_square** — minimum value for length / square / weight options, so a customer can't order 0 metres.

### Measure pricing formula

For length / weight / square, the line price impact is computed as `option_amount × measured_value × line_quantity`. The merchant sets the option unit and a rounding step (**Round to size** → `min_square`); the **Allow the purchase of a value less than the price of the product** toggle (only when the two unit selects differ) sets `allow_negative`.

### Price impact at cart calculation

Options with a price impact modify the line total. The platform respects flat additions (e.g. +5 BGN for gift wrap), per-quantity additions (+5 BGN PER unit of the product), and multiplicative / percentage impacts (rarer, but supported). Percentage impacts honour **Apply over** to decide whether they apply to the regular or the discounted price.

### Per-value validation

A per-value amount must be numeric (positive, or negative when `allow_negative` is on). A per-value thumbnail, if uploaded, must be jpg / jpeg / png / bmp / webp.

## Related

- [[products-options-overview]] — hub.
- [[products-options-types]] — which controls appear per type.
- [[products-options-order-handling]] — how the chosen value reaches the order line.
- [[product-option]] — the underlying option entity.

## Open questions

None.
