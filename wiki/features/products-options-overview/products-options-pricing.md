---
type: feature
nav_path: "Products → Options → Add / Edit → price impact"
route_name: apps.product_options.edit
route_path: /admin/products/options/:type/:id?
aliases: ["Product option pricing", "Option price impact", "Option price calculation", "Цена на опция"]
tags: [apps, products, options, pricing, customisation]
plan_gates: ["product_options"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[products-options-overview]]. See the hub for the other aspects (types, assignment, order handling).

# Product Options — price impact

## Purpose

Controls **how much an option adds to (or subtracts from) the line total** when the customer selects it. The price-impact controls appear in the General settings card of the Add / Edit option form, and which ones show depends on the [[products-options-types|Field type]]. Options can be informational (no price impact), add a flat amount, add a percentage, or (length / square) scale the product's price by a size the customer enters.

## Where to find it

Sidebar → Products → **Product options** (*Продуктови опции*) → **+ Create new option** (or edit) → **General settings** card → the price-impact controls below the Field type.

## What the merchant can do here

- Set a flat amount, a percentage, or a per-measure price for the option.
- Choose whether the price applies once per line or per unit of quantity.
- For length / square, set the unit the price is for, the unit the customer enters in, a minimum charged size, and whether less than one price unit may be ordered.

## Settings & fields

The form shows a different subset of controls per type:

| Field | Type / options | Shown for |
|-------|----------------|-----------|
| **Calculate the price for each** (`per_item`) | Toggle | radio, select, checkbox, image, text, textarea, file. Auto-set to 1 on save for length / weight / square. |
| **Type of the value** | Dropdown — % or currency-symbol (fixed) | radio, select, checkbox, image (per-value amounts). |
| **Apply over** | Dropdown — Regular price / Discounted price | Shown only when Type of the value = %. |
| **Type of the value** (inline amount + type pair) | Amount input + amount-type dropdown | text, textarea, file (single global price for the option). |
| **The price is determined base on:** | Length-unit dropdown (Meter / Centimetre / Millimetre / Kilometer) — the unit the product's price is for | length, square. |
| **Option unit** | Length-unit dropdown (same options) — the unit the customer enters | length, square. |
| **Round to size** | Numeric (min 0, step 0.001) — sets `min_square`, the minimum charged size | length, square. |
| **Allow the purchase of a value less than the price of the product** | Toggle — sets `allow_negative` | length / square ONLY when the two unit selects differ. |
| **Per-value Amount** | Numeric per row in the Values editor | radio, select, checkbox, image. |

## Business rules

### Price-impact mechanics (verified)

Each option — and each value within select / radio / checkbox — carries:

- **amount** — the numeric price impact.
- **amount_type** — flat / percent / per-quantity.
- **per_item** — when true, the price impact is multiplied by line quantity. Auto-set to 1 for length / weight / square (you pay per metre of cable × number of cables).
- **allow_negative** — measure types only: lets the customer order less than one price unit (see below).
- **apply_over_price_type** — whether the option price applies over the base price or replaces it (configurable on the form via **Apply over**).
- **product_symbol / value_symbol** — measure types only: the unit the price is for and the unit the customer enters.
- **min_square** — measure types only: the **Round to size** minimum.

### Measure pricing formula

A length or square option has **no amount field**. The product's own price (the chosen variant's price, as on its product page) is the price for one unit of **The price is determined base on:**, and the cart converts the entered size into that unit:

- **Length**: unit price × entered length in price units. Price per Meter, option unit Centimetre, 150 entered → price × 1.5. Price and option unit the same → price × entered value.
- **Square**: the customer enters length and width in the option unit; the area is taken in the price unit squared (cm entered, priced per m → m²), and unit price × area.
- **Round to size**: a smaller size is charged as this minimum — for length, in the option unit; for square, as an area in the price unit (e.g. m²).
- **Field limits**: the number field counts in whole option units, starts at one price unit (100 when Meter / Centimetre), and by default cannot go lower. **Allow the purchase of a value less than the price of the product** (shown only when the two units differ) lowers that to 1 option unit (e.g. 50 cm of a per-metre product). Whether a decimal typed into the field is accepted is not confirmed (verify).
- The scaled price replaces the unit price of that cart line and is multiplied by the line quantity. A discount on the product is scaled the same way, and so is the variant's weight for shipping. Other options' fees are added on top as usual.
- Whether the product page updates the price live while the customer types is not confirmed (verify).

### Price impact at cart calculation

Options with a price impact modify the line total. The platform respects flat additions (e.g. +5 BGN for gift wrap), per-quantity additions (+5 BGN PER unit of the product), and multiplicative / percentage impacts (rarer, but supported). Percentage impacts honour **Apply over** to decide whether they apply to the regular or the discounted price.

### Per-value validation

A per-value amount must be a number; a negative amount is accepted. A per-value thumbnail, if uploaded, must be jpg / jpeg / png / bmp / webp.

## Related

- [[products-options-overview]] — hub.
- [[products-options-types]] — which controls appear per type.
- [[products-options-order-handling]] — how the chosen value reaches the order line.
- [[product-option]] — the underlying option entity.

## Open questions

None.
