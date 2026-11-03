---
type: concept
nav_path: "Concept → Metafields and metaobjects → Writing through the Admin GraphQL API"
aliases: ["metafieldsSet", "metafieldsDelete", "compareDigest", "INVALID_COMPARE_DIGEST", "metaobjectCreate", "metaobjectUpdate", "metaobjectUpsert", "batchMetaobjectDelete", "bulkOperationCancel", "metafieldDefinitionTypes", "requiredValidations", "validationJob", "MetafieldOwnerType", "ownerId", "Write metafields API", "Import metafields", "Sync metaobjects", "Metafields integration", "Запис на метаполета през API", "Импорт на метаобекти"]
tags: [metafields, metaobjects, custom-data, admin-graphql, api, integrations, concepts]
plan_gates: []
created: 2026-10-21
updated: 2026-11-03
source_count: 3
---

# Writing metafields and metaobjects through the Admin GraphQL API

> Part of [[metafields-metaobjects]]. Value formats are in [[metafields-value-formats]]; definitions in [[metafields-definitions]].

## Definition

Integrations, imports and syncs write metafield values and metaobject entries through the **Admin GraphQL API** at `<store-host>/api/gql`, with a personal access token ([[settings-pat-tokens]]). Every value is a string in its type's format ([[metafields-value-formats]]). The same checks apply as in the admin: a value outside its type or validations is refused.

## Scope

### Plain ids and global IDs

- **Owners and entries are named by their plain id**, as everywhere in the Admin GraphQL API: `ownerId: "123"`, `metaobjectUpdate(id: "45")`. A global ID there is not found.
- **Values that reference a record carry its global ID**: `gid://cloudcart/Product/123`.

### Setting metafield values: `metafieldsSet`

```graphql
mutation {
  metafieldsSet(metafields: [
    {ownerType: PRODUCT, ownerId: "123", namespace: "custom", key: "care", value: "Wash at 30 °C"},
    {ownerType: PRODUCT, ownerId: "123", namespace: "specs", key: "weight",
     value: "{\"value\": 1.2, \"unit\": \"kilograms\"}"}
  ]) {
    metafields { namespace key type value compareDigest }
    userErrors { field elementIndex code message }
  }
}
```

- `ownerType` is `PRODUCT`, `CATEGORY` or `CUSTOMER`.
- `namespace` is required: there is no default namespace. Values of admin-made definitions are in `custom`.
- `type` is needed only for a value **without a definition** (an unstructured value), which is then checked against that type alone. With a definition, the value takes the definition's type and validations; a different `type` sent with it is refused (`INVALID_TYPE`).
- Up to **25** values per call, **all or none**. One refused value fails the call; `userErrors` names it by `elementIndex`. Codes include `INVALID_VALUE`, `INVALID_TYPE`, `BLANK` and `LESS_THAN_OR_EQUAL_TO`.
- **Safe updates**: read a metafield's `compareDigest` and send it back with the new value. The write happens only if nobody changed the value in between; otherwise `INVALID_COMPARE_DIGEST`. `compareDigest: null` means the metafield must not exist yet; if it does, the same code answers *"The metafield exists already."*
- A blank value is refused. **`metafieldsDelete`** removes values: up to 250 identifiers (`ownerType`, `ownerId`, `namespace`, `key`) per call, all or none.
- Permissions: products and categories need the **Products** permission and the `products` scope; customers the **Customers** permission and the `customers` scope ([[metafields-permissions]]).

### Metaobject entries

| Mutation | What it does |
|---|---|
| `metaobjectCreate(metaobject: {type, handle, fields, capabilities})` | Creates an entry. Without `handle`, one is made from the display name. |
| `metaobjectUpdate(id:, metaobject: {fields})` | Changes **only the fields listed**. |
| `metaobjectUpdate(id:, metaobject: {values})` | **Replaces all fields**: keys left out are cleared. |
| `metaobjectUpsert(handle: {type, handle}, metaobject: {fields})` | Creates the entry when the handle is new; otherwise changes only the fields listed. |
| `metaobjectUpsert(handle: {type, handle}, values: {...})` | Creates, or **replaces all fields** of an existing entry. |
| `metaobjectDelete(id:)` | Deletes one entry and the references to it. |
| `batchMetaobjectDelete(where: {ids} or {type})` | Deletes up to 250 entries, or every entry of a type, as a background job; `bulkOperationStatus(jobId)` reports its progress. |

- `fields` is a list of `{key, value}`. `values` is one JSON object by key, each value a string. A call takes one or the other, not both.
- A **blank value** clears that field.
- `capabilities: {publishable: {status: ACTIVE}}` or `DRAFT` sets the status, only for a definition with active/draft status ([[metaobjects-definitions]]).
- Changing an entry's `handle` does not keep the old one: a storefront route by the old handle stops finding it.
- All need the **Metaobjects** permission, and with a token the `metaobjects` scope ([[metafields-permissions]]).

```graphql
mutation {
  metaobjectUpsert(
    handle: {type: "designer", handle: "ana-petrova"}
    metaobject: {fields: [
      {key: "name", value: "Ana Petrova"},
      {key: "country", value: "Bulgaria"}
    ]}
  ) {
    metaobject { id handle }
    userErrors { field elementKey code message }
  }
}
```

### Asking which types exist: `metafieldDefinitionTypes`

Lists every type, `list.` forms included, each with `category`, `name`, `supportedValidations {name type}` and `requiredValidations`. Reading it first avoids a refused create. `requiredValidations` names `metaobject_definition_id` for a metaobject reference, `metaobject_definition_ids` for a mixed reference, and `scale_min` and `scale_max` for a rating. Staff need any of Settings, Settings → Metafields and metaobjects, Products, Products → Products, Products → Categories, Customers or Metaobjects.

### Background jobs

- `metafieldDefinitionUpdate` returns `validationJob` when it revalidates values, otherwise null. `bulkOperationStatus(jobId)` follows it, as it does `batchMetaobjectDelete`.
- `bulkOperationCancel(jobId)` stops a batch deletion before its next chunk; entries already deleted stay deleted. A validation runs to its end.
- `skippedIds` lists the ids that name no entry.
- **Access follows the area**: a batch deletion belongs to entries, a validation to definitions. The status needs the area's read, a cancel its write; otherwise `ACCESS_DENIED`.

### Query cost and search

A query nesting lists sets `first` to what it shows: a cost over 1,000 is refused before it runs ([[metafields-limits]]). The `query:` arguments use one language ([[metafields-search-syntax]]).

## Contrasts

- **`fields` vs `values`**: `fields` is a partial update, `values` a full replacement. A sync that sends only changed fields uses `fields`. A sync that mirrors a source record whole uses `values`.
- **Upsert vs create**: `metaobjectUpsert` by handle needs no lookup of ids, so a repeated import does not duplicate entries.
- **API vs admin namespaces**: the admin always writes in `custom`; the API may use any valid namespace, except `app--…` ([[metafields-definitions]]).

## Where it applies

- ERP, PIM and supplier syncs ([[metafields-use-case-integration-data]]), and large imports of entries such as designers, devices or ingredients.
- Definitions are created through the same API (`metafieldDefinitionCreate`, `metaobjectDefinitionCreate`), see [[metafields-definitions]] and [[metaobjects-definitions]].
- Limits per call and per store are in [[metafields-limits]].
- Smart collections with metafield conditions have their own operations ([[smart-collections-admin-api]]).

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-value-formats]]: the string each type takes.
- [[metafields-permissions]]: permissions and token scopes.
- [[settings-pat-tokens]]: personal access tokens.

## Open Questions

- None known.
