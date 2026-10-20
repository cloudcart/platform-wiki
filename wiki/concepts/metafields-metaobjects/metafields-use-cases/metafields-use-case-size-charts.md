---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Size charts"
aliases: ["Size chart metaobject", "Size guide", "Fit guide", "Structured size chart", "Fit hint", "Таблица с размери", "Размерна таблица", "Как да избера размер"]
tags: [metafields, metaobjects, use-case, fashion, size-chart]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: size charts and fit guides

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

A fashion or footwear store has a few dozen size tables (women's tops, men's trousers, children's shoes …) and thousands of products that share them. The platform already has a **Size Chart** app ([[apps-size-chart]]). It attaches a chart, a CMS page, to products by category or brand, and the Storefront API returns it as `Product.sizeChart`. Metaobjects add what that app does not hold:
- the chart as **data** (rows and columns) rather than a page;
- a chart chosen **per product**;
- **fit hints** per product.

## Scope

### When the Size Chart app is enough

One chart per category or per brand, shown as a page, on classic themes and on Nitrogen (`sizeChart { name pageHandle }`, then `page(handle:)`). Nothing else is needed.

### When a metaobject adds something

- The Nitrogen storefront should **draw** the table itself: responsive, with a cm/in switch, highlighting the recommended size.
- Some products need a **different** chart than their category's.
- Each product carries a **fit** note, such as "runs small".

### The data model

**Metaobject definition `size_chart`**:

| Field | Type | Notes |
|---|---|---|
| `name` | single-line text, required | Display name: *Women's tops — EU*. |
| `table` | `json` | e.g. `{"columns": ["Size","Chest","Waist"], "rows": [["S","86–90","68–72"], …]}`. |
| `how_to_measure` | rich text | Short instructions with headings and lists. |
| `diagram` | file (Image) | A measuring illustration. |
| `unit` | single-line text, `choices`: `cm`, `in` | The table's unit. |

**Metafields**:

| Owner | `namespace.key` | Type | Purpose |
|---|---|---|---|
| Category | `custom.size_chart` | `metaobject_reference` → `size_chart` | The default for the category. |
| Product | `custom.size_chart` | `metaobject_reference` → `size_chart` | An override for one product. |
| Product | `custom.fit` | single-line text, `choices`: *Runs small, True to size, Runs large* | A fit hint. |
| Product | `custom.fit_score` | `rating`, scale 1–5 | Optional "fit meter" (3 = true to size). |

### On the Nitrogen storefront

The product page reads `custom.size_chart`, `custom.fit` and `custom.fit_score` in one `metafields(identifiers:)` call. It follows the reference to the chart's fields. Without a product chart it reads the category's `custom.size_chart`. Without either it falls back to the app's `sizeChart` page. All the definitions stay `PUBLIC_READ`.

## Contrasts

- **Size Chart app vs metaobject**: the app is ready-made and shown on classic themes too. Its chart is a page, chosen by category or brand. The metaobject is structured data, chosen per product or category, and shown only where a Nitrogen storefront draws it.
- **Product tabs vs metaobject**: a product's own content tabs (`Product.tabs`, title + HTML) can hold a chart as free text, but per product. A shared chart then means repeating it.
- **Size options vs size chart**: the sizes the shopper buys are variant options with stock ([[products-variants-options]]). The chart only explains them.
- **`json` table vs fixed fields**: `json` takes any grid without a fixed shape, but cannot be filtered. Filtering a size chart is rarely needed.

## Where it applies

- Clothing, footwear, gloves, helmets, rings, bicycle frames.
- Limits: a `json` value up to 128 KB, far more than a size table needs. Up to 128 metaobject definitions per store ([[metafields-limits]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[apps-size-chart]]: the platform's Size Chart app.
- [[metaobjects-definitions]]: definitions, fields, entries.
- [[products-variants-options]]: the sizes the shopper actually picks.

## Open Questions

- None known.
