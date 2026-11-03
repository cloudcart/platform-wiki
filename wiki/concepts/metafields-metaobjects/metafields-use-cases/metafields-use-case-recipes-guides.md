---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Recipes, lookbooks and shoppable guides"
aliases: ["Recipe metaobject", "Lookbook metaobject", "Shoppable content", "Buying guide", "How-to guide", "Routine builder", "Join metaobject", "Рецепти", "Лукбук", "Ръководство за покупка", "Съдържание с продукти"]
tags: [metafields, metaobjects, use-case, content, recipes, lookbook, shoppable]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: recipes, lookbooks and shoppable guides

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Content that sells is content that links to products. Examples:

- a recipe whose ingredients go to the cart in one click;
- a lookbook outfit with every piece linked;
- a skincare routine of four steps;
- a "how to choose a tent" guide with the recommended models.

A blog article ([[blog-article]]) can mention products in its text, but only as links in HTML. A **metaobject** stores the content in structured form, with **product references** the storefront can price, stock-check and add to the cart.

## Scope

### Recipes, with a join entry for quantities

When a relationship carries data of its own, such as *250 g of this flour*, the link itself becomes an entry: a **join metaobject**.

**Metaobject definition `recipe`**:

| Field | Type | Notes |
|---|---|---|
| `title` | single-line text, required | Display name; the handle is the URL: `/recipes/banitsa`. |
| `hero` | file (Image) | |
| `intro` | multi-line text | |
| `prep_time`, `cook_time` | `duration` (minutes) | |
| `servings` | `number_integer`, `min` 1 | |
| `difficulty` | single-line text, `choices`: *Easy, Medium, Hard* | **Admin filter** on. |
| `diet` | `list.single_line_text_field`, `choices`: *Vegetarian, Vegan, Gluten-free* | **Admin filter** on. |
| `ingredients` | `list.metaobject_reference` → `recipe_ingredient` | In recipe order. |
| `steps` | rich text | Numbered list. |

**Join definition `recipe_ingredient`**:

| Field | Type |
|---|---|
| `label` | single-line text, required: *Flour, type 500* |
| `product` | `product_reference` (optional: not every ingredient is sold) |
| `amount` | single-line text, as printed: *250 g*, *a pinch* |
| `grams` | `weight` (optional): the exact quantity, for scaling servings |

The reverse link is a product metafield, `custom.recipes` as `list.metaobject_reference` → `recipe`: "Used in these recipes". References are not automatic in both directions, so it is kept by hand or by a script.

### Lookbooks and routines

- **`look`**: `title`, `images` (`list.file_reference`, Image), `story` (rich text), `products` (`list.product_reference`), `season` (single-line text with choices, **admin filter** on).
- **`routine`**: `title`, `skin_type` (choices), `steps` (`list.metaobject_reference` → `routine_step`). Each step has `name`, `product` (reference) and `how_to` (multi-line text).
- **`guide`**: `title`, `body` (rich text), `recommended` (`list.product_reference`), `article_url` (`url`) when a long version lives in the blog.

### On the Nitrogen storefront

- **Recipe page** `/recipes/{handle}`: the entry by handle, with its ingredients' references resolved to products in one query (entry → join entry → product). "Add all to cart" adds the sold ingredients.
- **Recipe index**: `metaobjects(type: "recipe", query: "fields.diet:Vegan fields.difficulty:Easy")`.
- **Product page**: "Used in these recipes" from `custom.recipes`.
- **Lookbook**: images with the products of the look; unavailable products drop out of the references automatically.

## Contrasts

- **Blog articles vs entries**: articles are free text with blog categories, served on classic themes and through the Storefront API. Entries are structured and shoppable, but have no classic-theme page. A store can keep the story in the blog and the shoppable part in an entry linked by `article_url`. There is no article reference type.
- **List of products vs join entries**: a plain `list.product_reference` is enough when only "which products" matters. Join entries are needed when each link carries a quantity, a step name or an order of its own. They cost one more level per query.
- **Recipes vs bundles** ([[bundle]]): "Add all to cart" adds separate products at their own prices. A bundle is one product with a set price.

## Where it applies

- Food and grocery, kitchenware, cosmetics routines, fashion lookbooks, outdoor and DIY guides, crafts and hobby kits.

## Related

- [[metafields-use-cases]]: all use cases.
- [[blog-article]]: the native blog.
- [[metafields-use-case-ingredients]]: ingredient entries for product labels.
- [[metaobjects-definitions]]: handles, references between entries.

## Open Questions

- None known.
