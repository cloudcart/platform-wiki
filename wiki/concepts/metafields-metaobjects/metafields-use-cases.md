---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases"
aliases: ["Metafields use cases", "Metaobjects use cases", "Metafield examples", "Metaobject examples", "What to build with metafields", "Metafields ideas", "Примери за метаполета", "Примери за метаобекти", "Как да използвам метаполета"]
tags: [metafields, metaobjects, use-case, custom-data, nitrogen, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 8
---

# Metafields and metaobjects: use cases

> Part of [[metafields-metaobjects]]. Each use case is its own page.

## Definition

A catalogue of data-model patterns for metafields and metaobjects. Each is built on **what CloudCart offers today**. Every page names the native feature it builds beside, so nothing is modelled twice.

Every pattern assumes:

- **Owners** are products, categories and customers. Variants and pages are reached through references.
- **Shown on Nitrogen** storefronts. Classic themes do not display metafields yet ([[metafields-nitrogen]]).
- **No translations**, no web page per entry, and no writes from the storefront.
- **Storefront listing filters** stay on category properties. Metafields reach listings through smart collections ([[metafields-capabilities]]).
- **Metaobject entries** can be filtered on the Storefront API by fields with the admin filter on, and sorted only by id or last update.

## Scope

### Product information

- [[metafields-use-case-specifications]]: typed specs with units beside the native dimensions, weight and energy class; comparison tables.
- [[metafields-use-case-size-charts]]: structured charts and fit hints, beside the Size Chart app.
- [[metafields-use-case-ingredients]]: ingredients, materials, allergens and nutrition as reusable entries.
- [[metafields-use-case-documents]]: typed, shared, multilingual documents beside the product's public files.
- [[metafields-use-case-box-contents]]: what's in the box, with links to items sold separately.
- [[metafields-use-case-availability-notes]]: lead times, pre-order and restock dates, delivery notes beside product statuses.

### Merchandising

- [[metafields-use-case-related-products]]: typed relationships (accessories, consumables, successors) beside Linked products.
- [[metafields-use-case-color-swatches]]: colour families across separate products.
- [[metafields-use-case-compatibility]]: compatibility beyond brand → model, beside the Brand-Model app.
- [[metafields-use-case-highlights]]: certification and quality icons; flags that build smart collections.
- [[metafields-use-case-category-content]]: hero, intro, SEO text and featured products on category pages.

### Content

- [[metafields-use-case-page-sections]]: homepage and landing pages composed of section entries.
- [[metafields-use-case-banners]]: scheduled banners, announcements and a singleton settings entry.
- [[metafields-use-case-faq]]: shared questions on products, categories and a help centre.
- [[metafields-use-case-designers]]: designer, author and maker profiles with their product pages.
- [[metafields-use-case-testimonials]]: store testimonials, press mentions, case studies.
- [[metafields-use-case-recipes-guides]]: recipes, lookbooks, routines and guides linked to products.
- [[metafields-use-case-events]]: events and workshops, with dates the storefront filters.

### Customers and operations

- [[metafields-use-case-customer-profile]]: loyalty tier, points, preferences; what the customer sees on their account page.
- [[metafields-use-case-b2b-accounts]]: payment terms, credit limit, account manager, contract on business customers.
- [[metafields-use-case-integration-data]]: ERP, PIM and supplier keys kept off the storefront.
- [[metafields-use-case-multilanguage]]: three patterns for content in several languages.

## Contrasts

### Choosing the tool

| The need | Use |
|---|---|
| One more fact about each product, category or customer | a **metafield** |
| The same content reused by many records, or a new kind of content | a **metaobject**, referenced by metafields |
| A link between records that carries its own data (a quantity, a step) | a **join metaobject** ([[metafields-use-case-recipes-guides]]) |
| Shoppers filter listings by it | a **category property** ([[products-property]]) |
| A self-maintaining product list by a value | a **smart-collection condition** on a product metafield |
| Something the platform already has (dimensions, linked products, labels, size chart, reviews, bundles) | the **native feature** |

### Common needs and their route

| Need | Route |
|---|---|
| A value that differs per variant (a swatch, a spec) | Product-level fields, a `json` map by variant SKU; variant references |
| A gift message or delivery instructions on an order | Customer custom fields at checkout ([[customers-custom-fields]]) |
| Shoppers filter listings by a value | Category properties; smart collections |
| A web page per entry | Nitrogen routes by type and handle |
| Content in several languages | [[metafields-use-case-multilanguage]] |
| Customers edit their own data | Customer custom fields |
| Store-wide settings for the storefront | A singleton metaobject ([[metafields-use-case-banners]]) |
| Segments by a customer value | Customer groups, custom fields |

## Where it applies

- Stores building or running a **Nitrogen** storefront ([[headless-storefront]]).
- Classic-theme stores can already fill values and use them in **smart collections**, ahead of a move to Nitrogen.

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: the types the patterns use.
- [[metafields-limits]]: the numbers to plan within.
- [[metafields-nitrogen]]: reading the data on the storefront.

## Open Questions

- None known.
