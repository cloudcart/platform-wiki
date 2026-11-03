---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Product highlights and certifications"
aliases: ["Product highlights metaobject", "Certification badges", "Eco badge", "Handmade badge", "Feature icons", "USP icons", "Trust icons", "Сертификати", "Иконки с предимства", "Еко продукт", "Ръчна изработка", "Предимства на продукта"]
tags: [metafields, metaobjects, use-case, merchandising, certifications, smart-collections]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: product highlights and certifications

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Shoppers scan a product page for a few key reassurances: *Organic*, *Handmade in Bulgaria*, *CE marked*, *Recyclable packaging*, *Vegan*, *2-year warranty*. Each deserves an icon, a short explanation and sometimes a link to the certifying body. The same few dozen highlights recur across the catalogue. A **`highlight` metaobject** defines each one once. Products **reference** the ones that apply, and a flag per important highlight lets **smart collections** gather the products that carry it.

## Scope

### The data model

**Metaobject definition `highlight`**:

| Field | Type | Notes |
|---|---|---|
| `title` | single-line text, required, `max` 50 | Display name: *Organic*. |
| `icon` | file (Image) | An SVG or PNG icon. |
| `description` | multi-line text, `max` 300 | What it means for this store. |
| `info_url` | `url` | The certifier's page. |
| `kind` | single-line text, `choices`: *Certification, Material, Origin, Service* | **Admin filter** on. |
| `priority` | `number_integer` | Which highlights the storefront shows first. |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.highlights` | `list.metaobject_reference` → `highlight`, `list.max` 6 | The icon row, in the chosen order. |
| `custom.is_organic` | `boolean` | **Smart-collection condition** on. |
| `custom.made_in` | single-line text, `choices` | **Smart-collection condition** on: *Bulgaria*, *EU* … |

The flags exist because a smart-collection condition can test a single value, but not an item of a list. The icon list is for display; the flags build collections.

### On the Nitrogen storefront

- **Product page**: an icon row from `custom.highlights`. Each icon opens its `description`, with a link to `info_url`.
- **Product cards**: the first one or two highlights by `priority`, read with the listing (`metafield` on each product).
- **"What our badges mean"** page: `metaobjects(type: "highlight", query: "fields.kind:Certification")`.
- **Collections**: "Organic" and "Made in Bulgaria" are smart collections built on the flags ([[products-smart-collections]]). They also work as normal collection pages on classic themes.

### Upkeep

Renaming a highlight, changing its icon or fixing its text is one edit to its entry, and every product shows the change. Deleting an entry removes it from every product's list ([[metaobjects-definitions]]).

## Contrasts

- **Highlights vs product labels and banners** ([[products-banners-labels]]): labels (*New*, *Sale* …) and banner images on product cards are a native feature, with their own rules, and are on the Storefront API (`Product.labels`, `Product.banners`). They are promotional markers. Highlights are lasting facts about the product, with an explanation. A store uses labels for campaigns and highlights for certifications and qualities.
- **Highlights vs category properties** ([[products-property]]): if shoppers should *filter listings* by "Organic", a property is needed, since storefront filters use properties. The highlight explains it; the property filters by it.
- **Metaobject vs a `choices` text list**: `list.single_line_text_field` with choices stores only words. The metaobject carries an icon, text and a link, edited once.

## Where it applies

- Food and cosmetics (organic, vegan, cruelty-free), fashion (recycled, fair trade), electronics (CE, warranty), furniture (FSC), handmade and local products.
- Highlights stay `PUBLIC_READ`. Internal audit data about a certificate goes in a separate definition with storefront access `NONE`.

## Related

- [[metafields-use-cases]]: all use cases.
- [[metafields-capabilities]]: smart-collection conditions on boolean and text.
- [[products-banners-labels]]: native card labels and banners.
- [[metafields-use-case-documents]]: certificates as downloadable documents.

## Open Questions

- None known.
