---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Compatibility and fitment"
aliases: ["Compatibility metaobject", "Fitment", "Compatible with", "Fits model", "Printer cartridge compatibility", "Lens mount", "Vehicle fitment", "Съвместимост", "Подходящ за модел", "Съвместими модели"]
tags: [metafields, metaobjects, use-case, compatibility, spare-parts, electronics]
plan_gates: []
created: 2026-10-20
updated: 2026-10-21
source_count: 3
---

# Use case: compatibility and fitment

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Accessories, consumables and spare parts are useless if they do not fit. The shopper asks *"does this cartridge fit my printer?"* or *"which straps fit my watch?"*. When fit depends only on **brand → model**, the platform already has an app for it ([[product-compatibility]]). When it depends on more, use a **metaobject per compatible thing**: years, a generation, a mount or connector standard, a note per fit. Products **reference** the entries they fit.

## Scope

### When the Brand-Model app is enough

**Brand-Model** ([[brand-model]]) keeps a brand → model catalogue, assigns products to models, and gives a brand-then-model filter on category pages. On the Storefront API, the product-list filter `brandModel` filters by it. For phone cases, screen protectors and chargers by phone model, nothing more is needed, and the filter works on both classic and Nitrogen storefronts.

### When a metaobject is the better fit

- Compatibility is not brand → model: a lens **mount**, a bicycle axle **standard**, a vacuum bag **type**, a coffee capsule **system**.
- Each fit needs details: model **years**, engine or **generation** codes, a **note** ("needs adapter"), a cartridge's **page yield** on that printer.
- The compatible devices deserve their own pages: *"Everything for the Canon PIXMA G3510"*.

### The data model

**Metaobject definition `device`** (or `printer`, `vehicle`, `mount`):

| Field | Type | Notes |
|---|---|---|
| `name` | single-line text, required | Display name: *Canon PIXMA G3510*. |
| `maker` | single-line text | **Admin filter** on. |
| `series` | single-line text | **Admin filter** on: *PIXMA G*. |
| `year_from`, `year_to` | `number_integer` | **Admin filter** on, for range searches. |
| `image` | file (Image) | |
| `notes` | multi-line text | |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.compatible_with` | `list.metaobject_reference` → `device` | Up to 1,024 entries per product. |
| `custom.primary_device` | `metaobject_reference` → `device` | Optional; **smart-collection condition** on, for a per-device collection. |
| `custom.fit_note` | multi-line text | What applies to all fits of this product. |

Details that vary **per pairing**, such as the yield of a cartridge on one printer, go in a small `fitment` metaobject with `device` (reference), `page_yield` (integer) and `note`. The product then lists `fitment` entries instead of devices.

### On the Nitrogen storefront

- **"Find parts for your device"**: a picker built from `metaobjects(type: "device", query: "fields.maker:Canon")`, narrowed by `series` and `year_from` / `year_to` (`fields.year_to:>=2022`).
- **Device page** `/devices/{handle}`: the entry by handle, with a product grid from a smart collection per device (condition: `custom.primary_device` equals the entry). For many devices, a script creates these collections.
- **Product page**: "Fits:" with the referenced devices, each linking to its device page. A "Check your model" box searches only within this product's list.

## Contrasts

- **Brand-Model app vs metaobjects**: the app gives a ready storefront listing **filter** and works on classic themes. Metaobjects give richer, non-brand-shaped compatibility, but no listing filter, since storefront filters do not use metafields. Shoppers reach products through device pages and smart collections instead. A store can combine both: brand → model in the app, technical detail in metaobjects.
- **List vs single reference**: a list of devices cannot be a smart-collection condition. The single `primary_device` can, which is why both exist.
- **Compatibility vs related products** ([[metafields-use-case-related-products]]): related products point product to product. Compatibility points a product to the *thing it fits*, which may not be sold in the store at all.

## Where it applies

- Printer ink and toner, vacuum and appliance spare parts, camera lenses and accessories, bicycle parts, car and motorbike accessories, watch straps, coffee machines and capsules, tool batteries.
- A store with thousands of devices fills entries by import: `metaobjectUpsert` by handle ([[metafields-admin-api]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[product-compatibility]]: selling by fit with the Brand-Model app.
- [[brand-model]]: the platform's brand → model compatibility app.
- [[metafields-capabilities]]: filtering entries by fields, conditions on a reference.
- [[metafields-use-case-related-products]]: product-to-product relationships.

## Open Questions

- None known.
