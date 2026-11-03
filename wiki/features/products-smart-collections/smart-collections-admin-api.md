---
type: feature
nav_path: "Products → Smart Collections → Admin GraphQL API"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart collections API", "Smart collections GraphQL", "createSmartCollection", "updateSmartCollection", "smartCollectionsBulkDelete", "regenerateSmartCollection", "smartCollections", "smartCollectionByHandle", "searchSmartCollections", "smartCollectionCacheHealth", "SmartCollectionRowInput", "Колекции през API", "Динамични колекции през API"]
tags: [products, collections, selections, admin-graphql, api, metafields]
plan_gates: ["product_collections"]
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, editor, rule builder, rule types, evaluation, storefront side-effects, rules and limits).

# Smart Collections — Admin GraphQL API

## Purpose

An integration or a script can read, create, change and delete the store's smart collections through the Admin GraphQL API at `<store-host>/api/gql` ([[admin-graphql-api]]), instead of the editor. A collection saved this way is the same record the editor opens, and it is filled by the same background step ([[smart-collections-evaluation]]).

## Where to find it

There is no screen of its own. Collections made through the API appear at Sidebar → Products → **Smart Collections**.

## What the merchant can do here

| Operation | What it does |
|---|---|
| `smartCollections(name, executing, first, page)` | Lists collections, up to 100 a page. `name` is a partial match. `executing` is true while one is being filled. |
| `smartCollection(id)` | One collection. |
| `smartCollectionByHandle(urlHandle)` | One collection by its URL handle. |
| `searchSmartCollections(query)` | Searches by name: 10 a page by default, up to 50. |
| `smartCollectionCacheHealth(includeHealthy, recentRegenSeconds, stuckSeconds)` | Compares each collection's stored product count with a live count. Verdicts are `OK`, `STALE_CACHE`, `DRIFT_AFTER_RECENT_REGEN` and `STUCK_EXECUTING`. It lists the problem collections unless `includeHealthy` is true. |
| `createSmartCollection(input)` | Creates a collection. |
| `updateSmartCollection(id, input)` | Changes a collection. |
| `smartCollectionsBulkDelete(ids)` | Deletes collections in the background, and returns a job that `bulkOperationStatus(jobId)` follows. |
| `regenerateSmartCollection(id)` | Fills a collection again, and answers `success`, `message` and `collection`. |

## Settings & fields

### Input

| Field | Rule |
|---|---|
| `name` | Required on create, up to 191 characters. |
| `description` | Up to 250,000 characters. |
| `url_handle`, `seo_title`, `seo_description`, `canonical` | Optional. Answers name them `urlHandle`, `seoTitle`, `seoDescription`, `canonical`. |
| `rows` | **1 to 10 rows**, required on create. On update, the rows given **replace** the old ones. |

### A row

`{value_type, record_type, operation, records, value, sub_value}`, or for a metafield `{value_type, metafield_definition_id, operation, value}`.

| `value_type` | `operation` | Takes |
|---|---|---|
| `product`, `category`, `discount`, `vendor`, `tag`, `category_property_option`, `selection` | `in`, `not_in` | `record_type` and `records` |
| `price` | `between`, `not_between`, `gt`, `gte`, `equal`, `not_equal`, `lte`, `lt` | `value`; `sub_value` for a range |
| `digital`, `sale`, `new`, `featured` | `is`, `is_not` | `value` |
| `metafield` | by the definition's type, below | `metafield_definition_id` and `value` |

`eq` and `not_eq` are read only, on rows stored earlier.

### A metafield row

The definition is a product definition with its **Smart collections** switch on and its values prepared ([[metafields-capabilities]]).

| Definition type | Operations | Value |
|---|---|---|
| `boolean` | `equal` | `true` or `false` |
| `single_line_text_field` | `equal` | The exact text, case-sensitive |
| `metaobject_reference` | `equal` | The entry's `gid://cloudcart/Metaobject/<id>` |
| `number_integer`, `number_decimal`, `rating` | `equal`, `gt`, `lt` | A number; a rating's value |

A value is at most 191 characters. It is checked against the type, not against the definition's validations.

```graphql
mutation {
  createSmartCollection(input: {
    name: "Cotton"
    rows: [{value_type: metafield, metafield_definition_id: 12, operation: equal, value: "Cotton"}]
  }) { id name products executing }
}
```

## Business rules

### Access

Every operation needs the staff permission **Products** or **Products → Smart Collections**; otherwise the answer is `ACCESS_DENIED`. A browser sign-in acts as the admin who signed in, with that admin's permissions. A token acts as the store owner ([[settings-pat-tokens]]).

### A refused row writes nothing

The whole save is refused, with every refusal of every row at once, in `errors[].extensions.validation`. The keys are `input.rows.<n>.metafield_definition_id`, `.operation` or `.value`. The messages are those of the editor ([[smart-collections-rule-builder]]). An operation the kind does not take answers *"Field is invalid. Allowed value must be: …"*, naming the ones it takes.

### Other failures

A failed save or regeneration answers `Failed to create smart collection: …`, `Failed to update smart collection: …` or `Failed to trigger regeneration: …`. The ending is the platform's own message when it has one, otherwise *"Unexpected error. Please try again later"*.

### Prices

`equal` and `not_equal` are accepted on a price row, but the background step that fills the collection reads only `between`, `not_between`, `gt`, `gte`, `lt` and `lte`, so the collection does not fill. For one exact price, use a `gte` and an `lte` row: rows combine with AND ([[smart-collections-rules-and-limits]]). The price rules are in [[smart-collections-rule-types]].

### Filling is in the background

A save answers before the products are filled. `executing` stays true and `products` keeps its old count until that step finishes.

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-rule-types]] — the rule catalogue these rows follow.
- [[smart-collections-rule-builder]] — the same rows in the editor.
- [[smart-collections-evaluation]] — how a collection is filled.
- [[metafields-capabilities]] — the switch a metafield row depends on.
- [[metafields-permissions]] — permissions on metafield conditions.
- [[headless-product-listing-order]] — reading smart collections on the Storefront API.

## Open questions

None.
