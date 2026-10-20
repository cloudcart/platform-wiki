---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Ingredients and materials"
aliases: ["Ingredients metaobject", "Materials metaobject", "Allergens", "INCI list", "Nutrition facts", "Fabric composition", "Съставки", "Алергени", "Материали", "Хранителна информация"]
tags: [metafields, metaobjects, use-case, cosmetics, food, materials]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: ingredients, materials, allergens and nutrition

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Cosmetics, food, supplements and textiles describe products by what they are made of. The same ingredient (hyaluronic acid, oat flour, merino wool) appears in many products, and each deserves one explanation, one image and one set of flags (allergen, vegan, organic). An **`ingredient` metaobject** holds that once. Each product lists its ingredients **in order** as references. Nutrition values, which are specific to the product, are **product metafields**.

## Scope

### The data model

**Metaobject definition `ingredient`** (or `material` for textiles):

| Field | Type | Notes |
|---|---|---|
| `name` | single-line text, required | Display name: *Hyaluronic acid*. |
| `inci_name` | single-line text | The official cosmetic name, where it applies. |
| `description` | rich text | What it does, where it comes from. |
| `image` | file (Image) | |
| `is_allergen` | boolean | **Admin filter** on. |
| `is_vegan`, `is_organic` | boolean | **Admin filter** on. |
| `origin` | single-line text | Country or source. |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.ingredients` | `list.metaobject_reference` → `ingredient` | **In label order**; a list holds up to 1,024 references. |
| `custom.composition` | multi-line text | The label text exactly as printed, for compliance. |
| `custom.energy` | `energy` (kilojoules / kilocalories) | Per 100 g. |
| `custom.fat`, `custom.carbohydrates`, `custom.protein`, `custom.salt` | `weight` (grams) | Per 100 g. |
| `custom.net_quantity` | `weight` or `volume` | 250 g, 50 ml. |
| `custom.vegan` | boolean | **Smart-collection condition** on. |

For textiles, `material` entries (*Cotton*, *Elastane*) with a `care` rich-text field, and on the product a `json` composition such as `{"cotton": 95, "elastane": 5}`, or two parallel lists.

### On the Nitrogen storefront

- **Product page**: the ingredient list in label order. Each name opens its entry's description and image, and allergen entries are marked from `is_allergen`.
- **Ingredient glossary**: `metaobjects(type: "ingredient")` lists every entry. An A–Z glossary page needs no extra data; each entry's page is found by its handle, `/ingredients/hyaluronic-acid`.
- **Allergen list**: `metaobjects(type: "ingredient", query: "fields.is_allergen:true")`, possible because the field has the admin filter on ([[metafields-capabilities]]).
- **Nutrition table**: the nutrition metafields read in one call and shown per 100 g.

### Collections from the data

A **"Vegan"** smart collection with the condition `custom.vegan` = true fills itself ([[products-smart-collections]]). It also works on classic themes, as a normal collection. A condition can test a **single** `metaobject_reference`, such as `custom.key_ingredient` = *Shea butter*, but not a **list**. So `custom.ingredients` cannot drive a collection. A key ingredient gets its own single reference or a boolean flag.

## Contrasts

- **Ingredients as entries vs as text**: text is fastest to enter but cannot be explained, filtered or reused. Entries cost one-time setup and pay back when the same ingredient appears in many products.
- **Allergen flags vs category properties**: if shoppers should **filter listings** by "gluten free", that is a category property ([[products-property]]), since storefront listing filters do not use metafields. The metaobject is for explaining and grouping.
- **Nutrition per product vs per variant**: the values sit on the product. Flavours with different nutrition values are separate products or keep a `json` map per variant on the product.

## Where it applies

- Cosmetics and skincare, food and drink, supplements, pet food, candles, textiles and furniture finishes.
- Keep `is_allergen` and similar fields `PUBLIC_READ`. Supplier codes for an ingredient go in a separate metaobject field on a definition the storefront cannot read, or on the product with storefront access `NONE`.
- No translations: a bilingual store keeps `name_bg` / `name_en` and `description_bg` / `description_en` fields on the entry ([[metafields-nitrogen]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[metaobjects-definitions]]: entries, handles, the list order.
- [[metafields-capabilities]]: filtering entries; smart-collection conditions.
- [[food-restaurant-grocery]]: the food-business setup these labels sit in.

## Open Questions

- None known.
