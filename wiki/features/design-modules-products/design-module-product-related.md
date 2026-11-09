---
type: feature
nav_path: "Design → Modules → Products → Related products"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/productsRelated
aliases: ["Related products module", "productsRelated module", "product.related", "Top products module", "Match with module", "Combine module", "Модул свързани продукти", "Свързани продукти"]
tags: [design, modules, products, related]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

# Product module — Related / Top / Match-with (`product.related`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Related products** module (type `product.related`) renders a horizontal row of recommended products on the **product detail page**. The SAME module TYPE is reused for multiple distinct instances per theme — `productsRelated` (Related products / Accessories), `productsRelated2` (Top products), `productsCombine` (Match with), `productsRelatedRow2` (Related products on a theme that ships it). Each instance is a SEPARATE row on the product page with its own settings — the merchant decides which strategy each row uses (category match vs vendor match vs tag match).

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab. The card label varies per instance and per theme (e.g., **"Related Products"**, **"Top products"**, **"Match with"**, **"Accessories"**).

Edit-panel URL: `/admin/storefront/widgets/{instance-name}` (e.g., `/admin/storefront/widgets/productsRelated`).

Renders below the product detail card on the product page; the theme decides the exact slot position.

Bulgarian admin: cards **Свързани продукти** (`productsRelated`), **Топ продукти** (`productsRelated2`), **Съчетай с** (`productsCombine`), which a theme may rename; fields **Име на секцията**, **Брой продукти**, **Продукти на ред**, **Вид** (*Филтрирай по категория* / *по производител* / *по таг*), **Подреди по** (*Подреди по ID*, *Подреди по име*, *По брой съвпадения*, *Случаен принцип*, *Цена*) and **Посока на подредба**.

## What the merchant can do here

- Title the row (e.g., "You may also like", "Complete the look").
- Pick a matching strategy: same **category**, same **vendor**, or matching **tag**.
- Pick a sort: id, name, match-score, random, or price.
- Pick a direction (asc / desc) — hidden when sort is `rand` or `match`.
- Set how many products and how many per row.

## What the merchant cannot do here

- Cannot show fewer than 2 products or more than 10 (`int:2,10`).
- Cannot pick more than 5 products per row (`int:1,5`).
- Cannot mix strategies — `type` is single-valued. Need a hybrid? Use two instances.
- Cannot make `match` filter by tags: with category or brand matching it only ranks the same candidates by shared tags.
- Cannot pick a `selection` (Smart Collection) source — that lives on [[design-module-product-showcase]].

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool | `true` | on / off | — | `bool` | Master on/off |
| `title` | string | `""` | any string | 0-100 chars | `char:0,100` | Section title |
| `products` | int | `4` | 2-10 | 2-10 | `int:2,10` | Number of products to fetch |
| `per_row` | int | `4` | 1-5 | 1-5 | `int:1,5` | Products per row |
| `order_by` | enum | `id` | `id`, `name`, `match`, `rand`, `price` | — | `in:id,name,match,rand,price` | Sort field |
| `order_direction` | enum | `desc` | `asc`, `desc` | — | `in:asc,desc` | Sort direction; hidden for `rand`/`match` |
| `type` | enum | `category` | `category`, `vendor`, `tag` | — | `in:category,vendor,tag` | Matching strategy |

### Validation strings

Shared Save / Reset messages ([[design-modules-products]]); out-of-range numbers and unknown values get field-level errors.

## All themes vs theme-specific

| Setting / instance | All themes | Theme-specific notes |
|--------------------|-----------|----------------------|
| Core fields (`enabled`, `title`, `products`, `per_row`, `order_by`, `order_direction`, `type`) | yes | Universal across every theme that ships product detail pages |
| Number of `product.related` instances | varies | a theme that ships it ships `productsRelated` + `productsRelatedRow2` + `productsCombine`; older themes typically ship one `productsRelated` only |

## Business rules

### Strategy dispatch

- **Category** — products in the product's **main category or any of its subcategories**, at every depth.
- **Brand** — products of the same brand.
- **Tag** — products sharing at least one tag; the product's hidden tags are used when it has no visible ones.

A product with no main category, no brand, or no tags at all gets no row for that type. The current product is excluded.

### Which products can appear

The row follows the listing rules: inactive, draft, out-of-window and hidden products never appear; sold-out products are left out when the store hides them, and geo zones apply, on the indexed engine ([[product-visibility]], [[design-module-product-filters]]).

### Sort `id`

`id` is the date added: **descending (the default) = newest first**.

### `match` ordering

`order_by=match` ranks candidates by how many tags (or hidden tags) they share with the current product, highest first, then newest first. There is no minimum: products sharing no tag can still fill the remaining places. A product with no tags, or a store on the basic database engine, gets the newest-first order instead ([[apps-listing-engine]]; verify the store's engine).

### `rand` mid-flips direction

`order_by=rand` internally flips direction on each request so the row feels fresh on repeat visits.

### Reset propagates across ALL instances of the type

`product.related` uses a SHARED `Configuration` group across all its instances. Resetting `productsRelated` ALSO clears the saved settings on `productsRelated2`, `productsCombine`, and every other `product.related` instance — surprising to merchants expecting per-card behaviour. Editing one instance saves only that instance, but Reset is store-wide for the TYPE.

### Empty row hides itself

If the matching strategy yields zero products, the row self-hides on the storefront — no empty "Related products" header is rendered.

## Related

- [[design-modules-products]] — hub.
- [[products-products]] — products that get matched.
- [[products-categories]] — source for `type=category`.
- [[products-vendors]] — source for `type=vendor`.
- [[products-tags]] — source for `type=tag`.
- [[design-module-product-linked]] — sibling row driven by explicit per-product linked-product lists.
- [[design-module-product-showcase]] — for homepage rows (Smart Collection / Featured / etc.).

## How it works (verified against backend)

### Restrictions

`enabled=bool, title=char:0,100, products=int:2,10, per_row=int:1,5, order_by=in:id,name,match,rand,price, order_direction=in:asc,desc, type=in:category,vendor,tag`.

### Defaults

`enabled=true, title="", products=4, per_row=4, order_by=id, order_direction=desc, type=category`.

### Sort dispatch

The runtime maps `order_by` to a listing-driver sort key. `match` sets a `match_tag_ids` option on the driver. `rand` picks `random-asc` or `random-desc` based on a coin flip.

### Shared `Configuration` group

`product.related` declares a `getConfigurationName` shared across instances. Reset deletes the per-instance row AND re-creates the shared group with defaults — so a single Reset wipes settings for every `product.related` instance.

## Open questions

- 📡 **`price` sort field on legacy themes.** Some older theme forms may not expose the `price` option in the dropdown — verify per-theme.
