---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Technical specifications"
aliases: ["Product specifications metafields", "Spec sheet", "Technical data", "Measurement metafields", "Comparison table", "Технически характеристики", "Спецификации на продукт", "Сравнение на продукти"]
tags: [metafields, use-case, specifications, measurements, electronics]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: technical specifications and comparison tables

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Electronics, tools, appliances and furniture are bought on their numbers. The platform already has some of them natively, on the Storefront API too:

- the product's **length, width and height** (`Product.dimensions`);
- the variant's **weight**;
- the **energy class** (`Product.energyClass`);
- the category **properties** (`Product.properties`).

Everything beyond these, such as power, battery, capacity, run time and noise, would otherwise sit in the description, where it cannot be compared, checked or reused. As **typed product metafields**, each number has a unit and a valid range. A Nitrogen storefront can put them in a specification table and a side-by-side comparison.

## Scope

### The data model

Product metafields in a namespace of their own, e.g. `specs`, to keep them apart from marketing fields. A namespace other than `custom` is made through the Admin GraphQL API; in the admin everything is `custom`.

| `namespace.key` | Type | Validation | Example |
|---|---|---|---|
| `specs.cable_length` | `dimension` | `min` 0 | `{"value": 1.5, "unit": "meters"}` |
| `specs.net_weight` | `weight` | `min` 0 | `{"value": 2.1, "unit": "kilograms"}`: the product itself, where the variant's weight is the shipping weight |
| `specs.power` | `power` | | `{"value": 2000, "unit": "watts"}` |
| `specs.voltage` | `voltage` | | `{"value": 230, "unit": "volts"}` |
| `specs.battery` | `battery_charge_capacity` | | `{"value": 5000, "unit": "milliamp_hours"}` |
| `specs.storage` | `data_storage_capacity` | | `{"value": 256, "unit": "gigabytes"}` |
| `specs.capacity` | `volume` | | `{"value": 9, "unit": "liters"}` |
| `specs.run_time` | `duration` | | `{"value": 45, "unit": "minutes"}` |
| `specs.noise_db` | `number_decimal` | `max_precision` 1 | `42.5` |
| `specs.connectivity` | `list.single_line_text_field`, `choices`: *Wi-Fi, Bluetooth, USB-C …* | | `["Wi-Fi","Bluetooth"]` |
| `specs.warranty_years` | `number_integer` | `min` 0, `max` 10 | `3` |
| `specs.ease_of_use` | `rating`, scale 1–5 | | `{"value": "4", "scale_min": "1", "scale_max": "5"}` |
| `specs.extra` | `json` | | rare, product-specific attributes |

The 11 measurement types keep the unit entered. Filtering and comparison convert to a common unit, so `900 grams` sorts below `1 kilograms` ([[metafields-types]]).

### On the Nitrogen storefront

- **Specification table**: the product page reads the `specs.*` identifiers in one `metafields(identifiers:)` call, up to 250, beside the native `dimensions`, `energyClass` and `properties`. It shows each value in the unit stored, or converted to the visitor's preference.
- **Comparison**: for 2–4 chosen products, the same identifiers per product. Rows where all values are equal can be collapsed.
- **Badges from numbers**: e.g. "Quiet" when `specs.noise_db` < 45, decided on the storefront.

### Making numbers work in the admin

- **Admin filter** on the important definitions lets staff and integrations find products by them, e.g. `metafields.specs.power:>=2000` ([[metafields-capabilities]]).
- **Smart-collection condition** on an integer, decimal or rating definition builds lists such as "Quiet dishwashers" from `specs.noise_db` less than 45. The collection is a normal collection on the storefront.

## Contrasts

- **Native fields first**: dimensions, weight and energy class have their own fields, which shipping and classic themes already use. Copying them into metafields would mean two values to keep in step.
- **Specs as metafields vs category properties** ([[products-property]]): properties are shared option lists (*Colour: red / blue*), shown on classic themes and **filterable in storefront listings**. Metafields hold exact numbers with units and validation, but are **not** storefront listing filters. Something shoppers filter by (screen size range, connectivity) is best kept as a property, or as both. Exact values for the specification table go in metafields.
- **Product-level values**: metafields sit on the product. A spec that differs per variant (a 128 GB vs 256 GB phone) is either a variant option or stored per variant in a `json` map on the product.
- **`json` catch-all vs typed fields**: `json` is quick for rare attributes, but has no units, validation, filter or smart-collection use.

## Where it applies

- Electronics, home appliances, power tools, batteries, storage, lighting, furniture, sports equipment.
- Up to 256 product definitions; 50 pinned on the product page; 50 with the admin filter; 128 as smart-collection conditions ([[metafields-limits]]).
- Usually all `PUBLIC_READ`. Supplier-only data goes in another namespace with storefront access `NONE`.

## Related

- [[metafields-use-cases]]: all use cases.
- [[metafields-types]]: the 11 measurement types and their units.
- [[metafields-capabilities]]: admin filter and smart-collection conditions on numbers.
- [[products-property]]: the filterable alternative.

## Open Questions

- None known.
