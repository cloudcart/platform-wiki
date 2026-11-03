---
type: concept
nav_path: "Settings → Metaobjects"
route_name: metafields.settings
route_path: /admin/settings/metafields, /admin/settings/metafields/:ownerType/unstructured, /admin/settings/metafields/:ownerType/new, /admin/settings/metafields/:ownerType/:definitionId, /admin/settings/metafields/metaobjects/new, /admin/settings/metafields/metaobjects/:definitionId
aliases: ["Metafields", "Metaobjects", "Metafields and metaobjects", "Custom data", "Metafield", "Metaobject", "Metafield definitions", "Metaobject definitions", "Metaobject entries", "custom namespace", "Метаполета", "Метаобекти", "Мета полета", "Мета обекти", "Допълнителни полета към продукт", "Собствени обекти"]
tags: [metafields, metaobjects, custom-data, nitrogen, headless, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-11-03
source_count: 13
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
- [[metafields-value-formats]]: the exact string each type stores and accepts: lists, references as global IDs, measurement units, the rich-text tree.
- [[metaobjects-definitions]]: metaobject definitions, their fields, the display name, entries with handles, active/draft status, references and deleting.
- [[metaobject-entries-admin]]: the entries list in the admin: columns, sorting, search, bulk delete, and the *Used in* card on an entry's page.
- [[metafields-value-inputs]]: how each type is entered on screen: the type picker's groups and presets, switches, units, lists, reference pickers.
- [[metafields-capabilities]]: the *Filtering*, *Smart collections* and *Unique values* switches.
- [[metafields-search-syntax]]: the search query language: terms, AND/OR/NOT, how each type matches, which fields each list takes, warnings.
- [[metafields-limits]]: every number: definitions, fields, entries, value sizes, list sizes, calls.
- [[metafields-permissions]]: staff permissions, token scopes, what the storefront and a signed-in customer may read.
- [[metafields-nitrogen]]: how a Nitrogen storefront reads them, what it can rely on, and the `parseMetafield` and `<MetafieldRichText>` helpers.
- [[metafields-admin-api]]: writing values and entries through the Admin GraphQL API: `metafieldsSet`, `compareDigest`, `metaobjectUpsert`, partial vs full updates.
- [[metafields-webhooks]]: the values that product, customer, category and order webhooks carry.

What to build with them:

- [[metafields-use-cases]]: catalogue of data-model patterns (size charts, specifications, ingredients, compatibility, designers, FAQs, banners, B2B customer data and more), each adapted to what CloudCart offers.

## Contrasts

- **Metafields vs category properties** ([[products-property]]). Properties are the platform's shared product characteristics (colour, material, size …), with values reused across products. They are shown on classic themes and used as storefront filters. On the Storefront API the product-list filter `productMetafield` filters by a property, despite its name. Metafields are free typed fields, not storefront filters. Anything shoppers should filter a listing by stays a property.
- **Customer metafields vs customer custom fields** ([[customers-custom-fields]]). Custom fields are asked of the shopper at checkout and the shopper may change them. Customer metafields are set by the store, staff or an integration. The shopper can at most read their own.
- **Metaobjects vs CMS pages** ([[page]]). A page is one free-form document. A metaobject is structured content in repeating entries, which a Nitrogen storefront lays out itself. A metafield may also reference a page (`page_reference`).

## Where it applies

- **Settings → Metaobjects** (`/admin/settings/metafields`). Lists the three owner kinds with their number of metafield definitions, and the metaobject definitions with their entries. *Add definition* is here.
- **Product editor** (`/admin/products/edit/:id`), **category window** (Products → Categories, `/admin/products/categories`) and **customer page** (`/admin/customers/details/:id`): a **Metafields** card shows the pinned definitions in order, then *Show all* for the rest. In the product editor it sits below the Categories card and saves with the page's save bar, in the category window it saves with the window's save, and on the customer page, above the customer's tags, it has **a save bar of its own** ([[metafields-definitions]]).
- **Settings → Metaobjects → a definition → entries**: the entries of a metaobject, where they are added, edited and deleted ([[metaobject-entries-admin]]).
- **Smart collections** ([[products-smart-collections]]): a product metafield can be a condition, see [[metafields-capabilities]].
- **Settings → Files** ([[settings-files-delete-protection]]): a file that only metafields use can be deleted, and the metafields lose it.
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
