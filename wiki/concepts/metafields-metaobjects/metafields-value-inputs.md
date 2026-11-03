---
type: concept
nav_path: "Settings → Metaobjects → Add definition → Type; Metafields card; entry form"
aliases: ["Metafield type picker", "Choice list", "Email metafield", "Image metafield", "Video metafield", "One or List", "Add item", "True or false switch", "Measurement unit select", "Rich text editor metafield", "Reference picker", "Mixed reference", "Избор на тип метаполе", "Списък с избори", "Въвеждане на стойност на метаполе"]
tags: [metafields, metaobjects, custom-data, types, admin, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

# Metafield value inputs and the type picker

> Part of [[metafields-metaobjects]]. The types and their rules are in [[metafields-types]]; the stored strings in [[metafields-value-formats]].

## Definition

This page describes how a type looks on screen: how it is chosen when a definition or a metaobject field is made, and which input fills in its value on the **Metafields** card and on an entry's page. Every rule on a value is checked when it is saved, and the refusal shows on the field.

## Scope

### The type picker

*Add definition* (Settings → Metaobjects) and a metaobject's field rows share one picker, with these groups:

| Group | Holds |
|---|---|
| Recommended | Single line text, Multi-line text, Integer, Image, Metaobject |
| Text | Multi-line text, Rich text, Single line text, Choice list, Email |
| Media | File, Image, Video |
| Reference | Category, Customer, Metaobject, Page, Product, Product variant |
| Number | ID, Money, Decimal, Integer, Rating, Measurement |
| Link | Link, URL |
| Date and time | Date, Date and time |
| Other | True or false, Color |
| Advanced | JSON, Mixed reference |

*Measurement*, *Metaobject* and *Mixed reference* open a second level: the measurement's kind, or the metaobject definition. *Mixed reference* takes several definitions and closes with *Done*.

A **One / List** choice switches the form: *"One: a single value. List: several values, in order."* In List mode the picker offers the types that have a list form.

The type names map to technical names in [[metafields-types]]. *Category* is `collection_reference`, *Color* is `color`, *True or false* is `boolean`.

### Presets

Four rows are a type with validations already set:

| Row | Type | Preset |
|---|---|---|
| **Choice list** | Single line text | `choices` |
| **Email** | Single line text | a `regex` for an address |
| **Image** | File | `file_type_options`: Image |
| **Video** | File | `file_type_options`: Video |

### The inputs

| Type | Input |
|---|---|
| Single line text, ID | A text box |
| Single line text with choices | A select, searchable above 8 choices |
| Multi-line text | A text area |
| Integer, decimal | Typed as text, so a minus and a decimal stay as written |
| Money | The amount, beside the store's sign. An amount stored in another currency shows its code instead ([[metafields-types]]). |
| Rating | The value, with its scale beside it |
| Date | A date picker |
| Date and time | A date and time picker, in the store's time zone |
| URL | A text box for the full address |
| Link | Two boxes: *Link text* and the address |
| Color | A colour picker |
| JSON | A code box |
| File | The file with its picture or icon and name, *Change* and *Remove*, or a button that opens the file manager ([[metafields-permissions]]) |

### True or false

A **switch**. Without a value it shows off and stores nothing until it is touched. *Clear* beside it removes a stored value. A required one on a new entry starts as false.

### Measurement

A number and a unit select, with short names in the admin's language (`kg`, `°C`, `mo`). A new value starts in the store's `unit_system`:

| Store | Starting units |
|---|---|
| Imperial | Pounds, inches, US fluid ounces, square feet, Fahrenheit |
| Metric, and anything else | Kilograms, centimeters, liters, square meters, Celsius |
| Both | Kilocalories, watts, volts, mAh, gigabytes, seconds |

A value keeps the unit it was saved in.

### Rich text

The admin's text editor, limited to what the tree holds: paragraphs, headings 1–6, numbered and bulleted lists, links, bold and italic. A paste keeps those elements, and nested lists flatten. A link without a scheme gets `https://`.

### Lists

Rows are dragged to reorder and removed one by one. *Add item* stops at `list.max` or at the type's limit. A choice list is one multi-select of its choices rather than rows. An item its choices no longer hold stays offered until it is removed.

### Reference fields

| Type | Picker |
|---|---|
| Product, Category, Customer, Page | The admin's own searches for each |
| Metaobject | The definition's entries, by display name |
| Mixed reference | Entries, one allowed definition at a time, chosen by name |
| Product variant | A product and variant window. Without the products' permission the field says *"Picking a variant needs the Products permission."* |

A list adds each record once.

## Contrasts

- **Input vs stored value**: the input shows the admin's short unit or date format. The stored string is the one in [[metafields-value-formats]], and the APIs read and write that.
- **Picker's groups vs the type table**: the same types, arranged differently. [[metafields-types]] arranges them by what a value is, with their validations.

## Where it applies

- The **Metafields** card in the product editor (`/admin/products/edit/:id`), the category window (`/admin/products/categories`) and on the customer page (`/admin/customers/details/:id`) ([[metafields-definitions]]).
- An entry's page ([[metaobject-entries-admin]]).
- Validation bounds on a definition's *Validations* card.

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: the types and their validations.
- [[metafields-value-formats]]: the strings the inputs build.
- [[settings-files]]: the file manager behind a file field.

## Open Questions

- None known.
