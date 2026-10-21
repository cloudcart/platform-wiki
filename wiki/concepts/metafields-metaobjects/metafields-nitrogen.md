---
type: concept
nav_path: "Concept → Metafields and metaobjects → On a Nitrogen storefront"
aliases: ["Metafields on Nitrogen", "Metafields Storefront API", "metafield(namespace key)", "metafields(identifiers)", "metaobject(handle)", "metaobjects(type)", "HasMetafieldsIdentifier", "MetaobjectHandleInput", "Metafields on classic theme", "MetafieldRichText", "parseMetafield", "Render rich text metafield", "Parse metafield value", "@cloudcart/nitrogen-react", "Метаполета в Nitrogen", "Метаполета в темата"]
tags: [metafields, metaobjects, custom-data, nitrogen, headless, storefront-api, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-21
source_count: 5
---

# Metafields and metaobjects on a Nitrogen storefront

> Part of [[metafields-metaobjects]]. See the hub for definitions, types, limits and permissions.

## Definition

At the time of writing, metafields and metaobjects are **mainly for headless stores built with Nitrogen**. The store's own themes do not display them. A Nitrogen storefront reads them through the **Storefront API** (`/api/sf`, [[headless-storefront-api]]) and decides itself where and how each value appears.

## Scope

### Nitrogen version

The Storefront API schema that Nitrogen ships (`@cloudcart/nitrogen`) has metafields and metaobjects from **2.2.0**. Codegen (`@cloudcart/nitrogen-codegen`) and the development explorer at `/graphiql` use that schema. On an earlier version, a query for `metafield`, `metafields` or `metaobject` fails codegen validation, although the API answers it. The TypeScript types of parsed values and of the rich-text tree (`ParsedMetafield`, `MetafieldMeasurement`, `RichTextRoot` …) come from `@cloudcart/nitrogen-react` 2.2.0.

### Reading metafields

`Product`, `Collection` (a category) and `Customer` have:

- `metafield(namespace:, key:)`: one value, or null.
- `metafields(identifiers: [{namespace, key}, …])`: up to **250** at once, answered in the same order, null where there is none.

```graphql
product(handle: "linen-shirt") {
  care: metafield(namespace: "custom", key: "care_instructions") { key type value }
  chart: metafield(namespace: "custom", key: "size_chart") {
    reference { ... on Metaobject { handle field(key: "table") { value } } }
  }
}
```

- **The namespace is required.** Without it nothing is found, since there is no app-reserved default. Definitions made in the admin are in `custom`.
- A **`Metafield`** returns:
  - `namespace`, `key`, `type`, `value`, `list` and `description`;
  - `createdAt` and `updatedAt`, the API's UTC `DateTime`, read with Nitrogen's `parseDateTime` rather than `new Date`;
  - `parentResource`, plus `reference` (single references) or `references` (lists, paginated, in the stored order).
- **`value` is always a string**, in the formats of [[metafields-value-formats]]. Lists and object types (rating, money, measurement, link, rich text, JSON) arrive as JSON text. `parseMetafield` turns each into a value, and `<MetafieldRichText>` renders rich text (next section).
- A **customer's** metafields come only to that customer, signed in, and only for `READ` definitions ([[metafields-permissions]], [[headless-customer-accounts]]).

### Turning values into display: `parseMetafield` and `<MetafieldRichText>`

`@cloudcart/nitrogen-react` has two helpers for metafield and metaobject-field values. `parseMetafield` exists in earlier versions for numbers, `boolean`, `json` and dates only. From **2.2.0** it reads every type, and `<MetafieldRichText>` is new.

**`parseMetafield({key, type, value})`** returns `{type, value}`, with `value` as its type names:

- `number_integer` and `number_decimal`: a number; `boolean`: `true` / `false`; `date` and `date_time`: a `Date` (a `date` at midnight UTC); `json`: the parsed JSON.
- `rating`: `{value, scaleMin, scaleMax}`.
- `money`: `{amount, currencyCode}`, the shape `<Money>` and `moneyWithFormat` take.
- A measurement (`weight`, `dimension`, `volume` …): `{value, unit}`, the unit as entered (`kilograms`).
- `link`: `{text, url}`.
- `rich_text_field`: the tree ([[metafields-types]]), ready for `<MetafieldRichText>`.
- Every `list.` type: an array of its items, each parsed as above.
- Text, colours, URLs and references (a global ID) stay strings. A value not in its type's format, or a type it does not know, comes back as the string.

So the query asks for `key` and `type` as well as `value`.

**`<MetafieldRichText data={…} />`** renders a `rich_text_field` value as React elements, not an HTML string. `data` is the `value` string or the tree `parseMetafield` gave.

- Paragraphs become `<p>`, headings `<h1>`–`<h6>`, lists `<ol>` / `<ul>` with `<li>`, bold `<strong>`, italic `<em>`, links `<a>` with the `title`.
- `headingStart` (2–6) moves the value's highest heading down to that level, and the rest with it, never past `h6`. Under a page's own `h2`, `headingStart={3}` turns a merchant's level-1 heading into `h3`. Without it, headings keep their stored level.
- `as` picks the wrapper: `div` (default), `section` or `article`.
- It carries no styles. Each element has a `cc-metafield-rich-text-*` class (`root`, `paragraph`, `heading`, `list`, `item`, `link`, `bold`, `italic`), and `classNames` adds the theme's own per part. `className` styles the wrapper.
- A link renders only for an `http`, `https`, `mailto`, `sms` or `tel` address; otherwise its text shows without a link. A value that is not such a tree (invalid JSON, HTML) renders nothing.

```tsx
<MetafieldRichText data={product.care?.value} headingStart={3} />
const weight = parseMetafield(product.weight).value; // {value: 1.2, unit: "kilograms"}
```

`<RichText>` from the same package is for HTML the API returns (descriptions, pages, articles), not for metafields.

### Reading metaobjects

- `metaobject(handle: {type: "designer", handle: "ana-petrova"})`, or `metaobject(id:)`: one entry, or null.
- `metaobjects(type: "faq", first: 20, after:, sortKey: "id" | "updated_at", reverse:, query:)`: a type's entries, page by page.
- `query` filters by fields that have the admin filter on: `fields.topic:delivery`, `fields.starts_at:>=2026-11-01`, `-fields.archived:true` ([[metafields-capabilities]]).
- An entry gives `id`, `handle`, `type`, `updatedAt`, `field(key:)` and `fields`. Only filled fields appear. Each field gives `key`, `type`, `value`, `reference` and `references`.
- Only entries of `PUBLIC_READ` definitions are returned, and only **Active** ones when the definition has the active/draft status.

### What references resolve to

`Product`, `ProductVariant`, `Collection`, `Page`, `Metaobject`, and files as `MediaImage`, `Video` (the uploaded file itself, as its only source) or `GenericFile` (URL, MIME type, size). A file reference reads as:

```graphql
reference {
  ... on MediaImage { alt image { url altText width height } }
  ... on Video { sources { url mimeType format } }
  ... on GenericFile { url mimeType originalFileSize }
}
```

Nitrogen's `<Image data={…}>` takes the `MediaImage`'s `image`, and `url(transform:)` resizes it through the store's image CDN. A referenced record the storefront does not show is left out. A customer reference never resolves. Entries referencing entries can be followed level by level in one query.

## Contrasts

- **Owners**: products, categories and customers, plus metaobject entries. Variants and pages are reached through references.
- **Languages**: a store serves one language, and each field holds one value. A multi-language business runs sister sites ([[apps-multilang]]), each defining and filling its own metafields; the Multilang sync does not copy them. One Nitrogen storefront serving two languages from one store keeps one field per language (`title_bg`, `title_en`). See [[metafields-use-case-multilanguage]].
- **Entry pages**: the Nitrogen storefront builds routes from `type` + `handle` and sets each entry page's SEO itself.
- **Listing filters**: product-listing filters on the Storefront API work by category properties ([[products-property]]). A metafield shapes a listing through a smart collection.
- **Entry order**: entries sort by `id` or `updated_at`. The storefront filters with `query`, then orders by any field itself.
- **Customer values** are read-only from the storefront: `READ_WRITE` reads as `READ`.
- **Namespaces**: any valid namespace except those beginning `app--`, which are reserved. Every definition is the store's own.

**Classic themes**: no CloudCart theme reads metafields or metaobjects yet. On a classic-theme store they can already be filled in, searched through the Admin GraphQL API, and drive smart collections. The storefront shows only what those collections produce.

## Where it applies

- The Nitrogen storefront's own code: product, category and account pages, plus any content route built from metaobject types ([[metafields-use-cases]]).
- Storefront tokens of every Nitrogen storefront of the store ([[nitrogen-storefront-overview]]): all of them see the same `PUBLIC_READ` data.

## Related

- [[metafields-metaobjects]]: hub.
- [[headless-storefront]]: Nitrogen and headless storefronts.
- [[headless-storefront-api]]: endpoint, tokens and scopes.
- [[headless-legacy-vs-nitrogen]]: other things that differ between classic themes and Nitrogen.
- [[metafields-use-cases]]: what to build with these queries.

## Open Questions

- None known.
