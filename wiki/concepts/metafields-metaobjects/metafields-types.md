---
type: concept
nav_path: "Settings → Metaobjects → Add definition → Type"
aliases: ["Metafield types", "Metafield type", "single_line_text_field", "multi_line_text_field", "rich_text_field", "number_integer", "number_decimal", "metaobject_reference", "mixed_reference", "product_reference", "variant_reference", "collection_reference", "file_reference", "list types", "Measurement types", "Metafield validations", "Типове метаполета", "Валидации на метаполе"]
tags: [metafields, metaobjects, custom-data, types, validations, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Metafield types and validations

> Part of [[metafields-metaobjects]]. The same types serve metafield definitions ([[metafields-definitions]]) and metaobject fields ([[metaobjects-definitions]]).

## Definition

Every metafield definition and every metaobject field has a **type**. The type decides what a value may hold and which **validations** the definition can add. Most types also have a **list** form, `list.<type>`, holding several values in order: up to 128 items, or 1,024 for lists of metaobject or mixed references. Every list can also set `list.min` and `list.max`, the fewest and most items.

## Scope

| Group | Type | List | Validations | Value |
|---|---|---|---|---|
| Text | `single_line_text_field` | yes | `min`, `max` (length), `regex`, `choices` (a fixed set, up to 128) | text |
| Text | `multi_line_text_field` | no | `min`, `max`, `regex` | text with line breaks |
| Text | `rich_text_field` | no | none | a formatted-text tree (below) |
| Number | `number_integer` | yes | `min`, `max` | whole number |
| Number | `number_decimal` | yes | `min`, `max`, `max_precision` | up to 13 digits and 9 decimals |
| Number | `rating` | yes | `scale_min`, `scale_max` (both required) | `{"value", "scale_min", "scale_max"}` |
| Number | `money` | no | `min`, `max` | `{"amount", "currency_code"}`, in the **store's currency** only |
| Date and time | `date`, `date_time` | yes | `min`, `max` | ISO 8601; a date-time is kept in UTC |
| Link | `url` | yes | `allowed_domains` (up to 128) | `https`, `http`, `mailto`, `sms` or `tel` |
| Link | `link` | yes | `allowed_domains` | `{"text", "url"}` |
| Other | `boolean` | no | none | `true` / `false` |
| Other | `color` | yes | none | `#rrggbb` |
| Other | `id` | no | `regex` | text, **always unique** per definition |
| Advanced | `json` | no | none | any JSON, up to 128 KB |
| Media | `file_reference` | yes | `file_type_options`: `Image` and/or `Video` | a file from the file manager |
| Reference | `product_reference`, `variant_reference`, `collection_reference`, `customer_reference`, `page_reference` | yes | none | a product, variant, category, customer or CMS page |
| Reference | `metaobject_reference` | yes | `metaobject_definition_id` (required) | an entry of one metaobject definition |
| Reference | `mixed_reference` | yes | `metaobject_definition_ids` (required) | an entry of any of several metaobject definitions |
| Measurement | 11 types (below) | yes | `min`, `max` | `{"value", "unit"}` |

### Measurements

| Type | Units |
|---|---|
| `weight` | grams, kilograms, ounces, pounds |
| `dimension` | millimeters, centimeters, meters, inches, feet, yards |
| `volume` | milliliters, centiliters, liters, cubic meters; US and imperial fluid ounces, pints, quarts, gallons |
| `area` | square centimeters, square meters, square inches, square feet, square yards |
| `temperature` | celsius, fahrenheit, kelvin |
| `energy` | joules, kilojoules, calories, kilocalories |
| `power` | milliwatts, watts, kilowatts, horsepower |
| `voltage` | volts |
| `battery_charge_capacity` | milliamp hours |
| `data_storage_capacity` | bytes, kilobytes, megabytes, gigabytes, terabytes |
| `duration` | nanoseconds … seconds, minutes, hours, days, months, years |

A value keeps the unit it was entered in. For filtering and smart-collection conditions it is compared in a common base unit, so `1 kilograms` and `900 grams` compare correctly.

### Rich text

A rich-text value holds only: paragraphs, headings (levels 1–6), ordered and unordered lists, links, and bold and italic text. Anything else is refused, so a value is always something both the admin and a Nitrogen storefront can render. Links follow the `url` rules, so `javascript:` links are impossible.

### Files

A file field picks from the store's file manager ([[settings-files]]), or uploads into it. With `file_type_options` it accepts only images, only videos, or both. On the Storefront API an image comes back as a `MediaImage`, a video as a `Video` and anything else as a `GenericFile`. The `Video` is the uploaded file itself, with no transcoded versions or preview image.

### Value sizes

A value is at most 64 KB; `json` 128 KB; `url` and `id` 2 KB. In a list, each item has that limit. See [[metafields-limits]].

## Contrasts

- **The full list**: the types above are all the types offered. Any other type name is refused. A variant is reached through `variant_reference`. See [[metafields-nitrogen]].
- **`single_line_text_field` with `choices` vs a metaobject reference**: choices are a fixed word list stored as text. A metaobject reference points to an entry that carries its own fields (an image, a colour, a description) and is edited in one place for every product that uses it.
- **`json` vs structured fields**: `json` takes anything and cannot be filtered, used in a smart collection, or checked beyond being valid JSON. Typed fields are validated and, where eligible, filterable ([[metafields-capabilities]]).

## Where it applies

- The **type picker** of *Add definition* (metafields) and of a metaobject's field rows, grouped as above.
- Every value write: the admin's Metafields card, metaobject entries, `metafieldsSet` and the metaobject mutations of the Admin GraphQL API. A value outside its type or validations is refused with the reason.

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-capabilities]]: which types can be filtered, be a smart-collection condition, or be unique.
- [[settings-files]]: the file manager behind `file_reference`.

## Open Questions

- None known.
