---
type: feature
nav_path: "Design → Modules → Products → Related products"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/productsRelated
aliases: ["Related products module", "productsRelated module", "product.related", "Top products module", "Match with module", "Combine module", "Модул свързани продукти", "Свързани продукти"]
tags: [design, modules, products, related]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Related / Top / Match-with (`product.related`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Related products** module (type `product.related`) renders a horizontal row of recommended products on the **product detail page**. The SAME module TYPE is reused for multiple distinct instances per theme — `productsRelated` (Related products / Accessories), `productsRelated2` (Top products), `productsCombine` (Match with), `productsRelatedRow2` (Related products on a theme that ships it). Each instance is a SEPARATE row on the product page with its own settings — the merchant decides which strategy each row uses (category match vs vendor match vs tag match).

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab. The card label varies per instance and per theme (e.g., **"Related Products"**, **"Top products"**, **"Match with"**, **"Accessories"**).

Edit-panel URL: `/admin/storefront/widgets/{instance-name}` (e.g., `/admin/storefront/widgets/productsRelated`).

Renders below the product detail card on the product page; the theme decides the exact slot position.

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
- Cannot use the `match` sort with `type=category` or `type=vendor` — it only ranks tags.
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

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `products` out of 2-10 | Field-level integer-range error |
| `per_row` out of 1-5 | Field-level integer-range error |
| `type` not in enum | Field-level enum error |

## All themes vs theme-specific

| Setting / instance | All themes | Theme-specific notes |
|--------------------|-----------|----------------------|
| Core fields (`enabled`, `title`, `products`, `per_row`, `order_by`, `order_direction`, `type`) | yes | Universal across every theme that ships product detail pages |
| Number of `product.related` instances | varies | a theme that ships it ships `productsRelated` + `productsRelatedRow2` + `productsCombine`; older themes typically ship one `productsRelated` only |

## Business rules

### Strategy dispatch

`type=category` matches by the product's category tree (child-by-path); `type=vendor` matches by `vendor_id`; `type=tag` joins on shared tag IDs. The current product is excluded automatically.

### `match` ordering is tag-only

`order_by=match` is meaningful only when `type=tag` — it ranks candidate products by how many tags they share with the current product (highest first). If the product has no tags, the runtime falls back to its `hidden_tags` set; if that's empty too, the row is empty.

### `rand` mid-flips direction

`order_by=rand` internally flips direction on each request so the row feels fresh on repeat visits.

### Reset propagates across ALL instances of the type

`product.related` uses a SHARED `Configuration` group across all its instances. Resetting `productsRelated` ALSO clears the saved settings on `productsRelated2`, `productsCombine`, and every other `product.related` instance — surprising to merchants expecting per-card behaviour. Editing one instance saves only that instance, but Reset is store-wide for the TYPE.

### Cache invalidation on save / reset

Save and Reset bump the per-site cache key — visible on the next storefront request.

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

- 📡 **Tag-match scoring weight.** The match score is the count of overlapping tags. Whether weighted tags or partial-match thresholds are applied needs verification.
- 📡 **`price` sort field on legacy themes.** Some older theme forms may not expose the `price` option in the dropdown — verify per-theme.
