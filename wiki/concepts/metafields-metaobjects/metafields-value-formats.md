---
type: concept
nav_path: "Concept → Metafields and metaobjects → Value formats"
aliases: ["Metafield value format", "Metafield value JSON", "Metaobject field value format", "Rich text tree", "Rich text JSON", "list-item", "listType", "Measurement units", "Metafield units", "gid://cloudcart", "Metafield global ID", "List value JSON array", "Rating value", "Money value", "Формат на стойност на метаполе", "Форматиран текст в метаполе", "Мерни единици на метаполе"]
tags: [metafields, metaobjects, custom-data, types, api, concepts]
plan_gates: []
created: 2026-10-21
updated: 2026-10-21
source_count: 2
---

# Metafield value formats

> Part of [[metafields-metaobjects]]. The types and their validations are in [[metafields-types]].

## Definition

Every metafield and metaobject-field value is **one string**, whatever its type. The Storefront API returns it in `value`, and the Admin GraphQL API takes it in `value` ([[metafields-admin-api]]). This page gives the exact string for each type: what is stored, what a write must send, and what a reader gets back. A write in another form is refused with a message naming the expected form.

## Scope

### Single values

| Type | The string | Notes |
|---|---|---|
| `single_line_text_field`, `id` | `Linen` | No line breaks. |
| `multi_line_text_field` | `Line 1` + line break + `Line 2` | |
| `number_integer` | `42` | Within ±9,007,199,254,740,991. |
| `number_decimal` | `12.5` | Within ±9,999,999,999,999.999999999. |
| `boolean` | `true` or `false` | |
| `color` | `#1a2b3c` | Six hex digits, either case. |
| `date` | `2026-11-01` | Years 1000–9999. |
| `date_time` | `2026-11-01T18:30:00Z` | Stored and returned in UTC. A write may carry an offset (`+02:00`) or a fraction of a second. Without a zone, the Admin GraphQL API reads it as UTC and the admin's own pages in the store's time zone. |
| `url` | `https://example.com/care` | A full address: https, http, mailto, sms or tel, no spaces, and a host for http(s). A path alone (`/sale`) is refused. With `allowed_domains`, the host must be one of them or under one. |
| `link` | `{"text": "Care guide", "url": "https://example.com/care"}` | Exactly these two keys; `url` as for `url`. |
| `rating` | `{"value": "4.5", "scale_min": "1", "scale_max": "5"}` | Numbers as **strings**. The scale must be the definition's. |
| `money` | `{"amount": "19.90", "currency_code": "EUR"}` | The amount as a **string**. The currency must be the store's. |
| A measurement | `{"value": 1.2, "unit": "kilograms"}` | The value as a **number**, up to 15 significant digits and 9 decimals. Units below. |
| `json` | any valid JSON | |
| `rich_text_field` | a JSON tree | Below. |
| A reference | `gid://cloudcart/Product/123` | Below. |

A value is kept as sent, spaces included. A blank value is refused.

### Lists

A `list.` value is a **JSON array** of 1 to 128 items (1,024 for metaobject and mixed references):

- Items of text, number, date, colour, URL and reference types are **strings**: `["1", "2", "3"]` for `list.number_integer`, `["gid://cloudcart/Product/1", "gid://cloudcart/Product/2"]` for `list.product_reference`. `[1, 2, 3]` is refused.
- Items of `link`, `rating` and measurement types are **objects** in the single type's form: `[{"value": 30, "unit": "centimeters"}, {"value": 45, "unit": "centimeters"}]`.
- An empty array is refused. A list is emptied by deleting the value, or on a metaobject entry by sending a blank value.

### References

A reference's value is the record's global ID, `gid://cloudcart/<Type>/<id>`:

| Type | Global ID |
|---|---|
| `product_reference` | `gid://cloudcart/Product/<id>` |
| `variant_reference` | `gid://cloudcart/ProductVariant/<id>` |
| `collection_reference` | `gid://cloudcart/Collection/<id>`, a category |
| `customer_reference` | `gid://cloudcart/Customer/<id>` |
| `page_reference` | `gid://cloudcart/Page/<id>` |
| `metaobject_reference`, `mixed_reference` | `gid://cloudcart/Metaobject/<id>` |
| `file_reference` | `gid://cloudcart/File/<id>` |

- The record must exist. A file must be of a kind the definition allows; an entry must be of the definition(s) the field names.
- On the Storefront API a reader does not need to parse the ID: `reference` and `references` return the record itself ([[metafields-nitrogen]]). Nitrogen's `parseGid` splits an ID when it is needed.

### Measurement units

| Type | Units, as the value names them |
|---|---|
| `weight` | `grams`, `kilograms`, `ounces`, `pounds` |
| `dimension` | `millimeters`, `centimeters`, `meters`, `inches`, `feet`, `yards` |
| `volume` | `milliliters`, `centiliters`, `liters`, `cubic_meters`, `us_fluid_ounces`, `us_pints`, `us_quarts`, `us_gallons`, `imperial_fluid_ounces`, `imperial_pints`, `imperial_quarts`, `imperial_gallons` |
| `area` | `square_centimeters`, `square_meters`, `square_inches`, `square_feet`, `square_yards` |
| `temperature` | `celsius`, `fahrenheit`, `kelvin` |
| `energy` | `joules`, `kilojoules`, `calories`, `kilocalories` |
| `power` | `milliwatts`, `watts`, `kilowatts`, `horsepower` |
| `voltage` | `volts` |
| `battery_charge_capacity` | `milliamp_hours` |
| `data_storage_capacity` | `bytes`, `kilobytes`, `megabytes`, `gigabytes`, `terabytes` |
| `duration` | `nanoseconds`, `microseconds`, `milliseconds`, `seconds`, `minutes`, `hours`, `days`, `months`, `years` |

### Rich text

A rich-text value is a JSON tree. Each part has a `type` and only the properties below:

| Part (`type`) | Properties | Holds (`children`) |
|---|---|---|
| `root` | `children` | `paragraph`, `heading`, `list` |
| `paragraph` | `children` | `text`, `link` |
| `heading` | `level` (1–6), `children` | `text`, `link` |
| `list` | `listType` (`ordered` or `unordered`), `children` | `list-item` |
| `list-item` | `children` | `text`, `link` |
| `link` | `url`, `title` (optional), `children` | `text` |
| `text` | `value`, `bold` and `italic` (optional, `true` / `false`) | none |

- Lists do not nest: a list item holds text and links only.
- An optional property, when present, must have its type: `"title": null` is refused.
- A link's `url` follows the `url` rules, so `javascript:` links are impossible.
- Any other part or property is refused, with an error naming where in the tree it sits.

```json
{"type": "root", "children": [
  {"type": "heading", "level": 2, "children": [{"type": "text", "value": "Care"}]},
  {"type": "paragraph", "children": [
    {"type": "text", "value": "Wash at "},
    {"type": "text", "value": "30 °C", "bold": true},
    {"type": "text", "value": ". See the "},
    {"type": "link", "url": "https://example.com/care", "title": "Care guide",
     "children": [{"type": "text", "value": "care guide"}]}
  ]},
  {"type": "list", "listType": "unordered", "children": [
    {"type": "list-item", "children": [{"type": "text", "value": "Do not tumble dry"}]}
  ]}
]}
```

Because nothing else can be stored, every value displays both in the admin and on a Nitrogen storefront, where `<MetafieldRichText>` renders the tree ([[metafields-nitrogen]]).

## Contrasts

- **Strings vs numbers**: `rating` and `money` carry their numbers as strings, a measurement as a number, and list items of number types as strings. Sending the other form is refused.
- **`value` vs `reference` on the Storefront API**: `value` is the global ID as stored; `reference` / `references` resolve it to the product, entry or file.
- **Stored unit vs compared unit**: a measurement keeps the unit it was written in; filters and smart-collection conditions compare it in a common base unit ([[metafields-types]]).

## Where it applies

- Every write: the admin's Metafields card and entry forms (which build these strings), `metafieldsSet` and the metaobject mutations ([[metafields-admin-api]]).
- Every read: `value` on the Storefront API and the Admin GraphQL API. On Nitrogen, `parseMetafield` turns the string into a value ([[metafields-nitrogen]]).

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: the types and their validations.
- [[metafields-admin-api]]: writing values.
- [[metafields-nitrogen]]: reading them on a Nitrogen storefront.
- [[metafields-limits]]: value sizes.

## Open Questions

- None known.
