---
type: concept
nav_path: "Settings → Metaobjects"
route_name: metafields.settings
route_path: /admin/settings/metafields
aliases: ["Metafields", "Metaobjects", "Metafields and metaobjects", "Custom data", "Metafield", "Metaobject", "Metafield definitions", "Metaobject definitions", "Metaobject entries", "custom namespace", "Метаполета", "Метаобекти", "Мета полета", "Мета обекти", "Допълнителни полета към продукт", "Собствени обекти"]
tags: [metafields, metaobjects, custom-data, nitrogen, headless, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 12
---

# Metafields and metaobjects

## Definition

**Metafields** are extra, typed fields a store adds to its own **products**, **categories** and **customers**: a product's care instructions, a category's hero image, a customer's loyalty tier. **Metaobjects** are record types the store invents itself, such as *Size chart*, *Designer*, *FAQ* or *Ingredient*. Each has its own fields, and its **entries** can be attached to products, categories and customers through reference metafields.

Both work in two layers:

- a **definition**, the schema: name, `namespace.key`, type, validations and who may read it;
- **values**, filled in per product, category or customer, or per entry.

Types have fixed technical names (`single_line_text_field`, `list.product_reference`, `metaobject_reference` …), used the same way in the admin, the Admin GraphQL API and the Storefront API.

> **For now, metafields and metaobjects are mainly for headless stores built with Nitrogen.** The store's own themes do not show them. A Nitrogen storefront ([[headless-storefront]]) reads them through the Storefront API and decides itself how to show them. On a classic theme they are data the storefront does not yet use.

## Scope

How it works:

- [[metafields-definitions]]: metafield definitions on products, categories and customers. Namespace and key, pinning, what can change later, values without a definition, deleting.
- [[metafields-types]]: every value type, its list form and the validations it takes, including measurements, references, files and rich text.
- [[metaobjects-definitions]]: metaobject definitions, their fields, the display name, entries with handles, active/draft status, references and deleting.
- [[metafields-capabilities]]: the admin filter, the smart-collection condition and unique values.
- [[metafields-limits]]: every number: definitions, fields, entries, value sizes, list sizes, calls.
- [[metafields-permissions]]: staff permissions, token scopes, what the storefront and a signed-in customer may read.
- [[metafields-nitrogen]]: how a Nitrogen storefront reads them, and what it can rely on.

What to build with them:

- [[metafields-use-cases]]: catalogue of data-model patterns (size charts, specifications, ingredients, compatibility, designers, FAQs, banners, B2B customer data and more), each adapted to what CloudCart offers.

## Contrasts

- **Metafields vs category properties** ([[products-property]]). Properties are the platform's shared product characteristics (colour, material, size …), with values reused across products. They are shown on classic themes and used as storefront filters. On the Storefront API the product-list filter `productMetafield` filters by a property, despite its name. Metafields are free typed fields, not storefront filters. Anything shoppers should filter a listing by stays a property.
- **Customer metafields vs customer custom fields** ([[customers-custom-fields]]). Custom fields are asked of the shopper at checkout and the shopper may change them. Customer metafields are set by the store, staff or an integration. The shopper can at most read their own.
- **Metaobjects vs CMS pages** ([[page]]). A page is one free-form document. A metaobject is structured content in repeating entries, which a Nitrogen storefront lays out itself. A metafield may also reference a page (`page_reference`).

## Where it applies

- **Settings → Metaobjects** (`/admin/settings/metafields`). Lists the three owner kinds with their number of metafield definitions, and the metaobject definitions with their entries. *Add definition* is here.
- **Product, category and customer pages**: a **Metafields** card shows the pinned definitions in order, then *Show all* for the rest. It is saved together with the page.
- **Settings → Metaobjects → a definition → entries**: the entries of a metaobject, where they are added, edited and deleted.
- **Smart collections** ([[products-smart-collections]]): a product metafield can be a condition, see [[metafields-capabilities]].
- **Admin GraphQL API** (`metafieldsSet`, `metafieldDefinitionCreate`, `metaobjectUpsert` …) for integrations, with personal access tokens ([[settings-pat-tokens]]).
- **Storefront API** (`/api/sf`) for Nitrogen storefronts ([[headless-storefront-api]]).

## Related

- [[headless-storefront]]: Nitrogen, the main consumer of this data.
- [[headless-storefront-api]]: the API a Nitrogen storefront reads them through.
- [[products-property]]: category properties, the filterable alternative.
- [[customers-custom-fields]]: fields the shopper fills in at checkout.
- [[products-smart-collections]]: collections built from metafield conditions.
- [[settings-files]]: the file manager that file fields pick from.
- [[settings-pat-tokens]]: tokens and scopes for the Admin GraphQL API.
- [[settings-staff]]: staff permissions that gate definitions, values and entries.

## Open Questions

- None known.
