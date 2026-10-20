---
type: concept
nav_path: "Settings → Metaobjects → a metaobject definition → Entries"
route_name: metafields.entries
route_path: /admin/settings/metafields/metaobjects/{definitionId}/entries
aliases: ["Metaobject definition", "Metaobject entries", "Metaobject entry", "Metaobject handle", "Display name field", "Active draft status", "publishable metaobject", "Used in", "metaobjectUpsert", "Дефиниция на метаобект", "Записи на метаобект", "Чернова и активен запис"]
tags: [metaobjects, custom-data, entries, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 5
---

# Metaobject definitions and entries

> Part of [[metafields-metaobjects]]. See the hub for metafields, types, limits and permissions.

## Definition

A **metaobject definition** is a record type the store designs itself: *Size chart*, *Designer*, *FAQ*, *Store event*. It lists its **fields**, each with a key, a name, a type ([[metafields-types]]) and validations. Its **entries** are the actual records, such as *"Size chart — women's tops"* or *"Designer — Ana Petrova"*. An entry is used by pointing to it from a metafield (`metaobject_reference`, `mixed_reference`) or from another metaobject's field. One entry can be used by any number of products, categories or customers and is edited in one place.

## Scope

### The definition

| Attribute | Rule |
|---|---|
| Type | The definition's code, e.g. `size_chart`: 3–255 characters, letters, digits, `-` and `_`. Unique in the store, **never changes**. A type beginning `app--` is reserved for apps. |
| Name, description | Shown to staff; the name up to 255 characters. |
| Fields | Up to **40**. Each has a key (2–64 characters, fixed once made), a name, a description, a type, validations and **required** yes/no. The order can be rearranged. |
| Display name | The single-line text field whose value names each entry in lists and pickers. By default, the first single-line text field. |
| Storefront access | `PUBLIC_READ` (default) or `NONE`. |
| Active/draft status | On by default: each entry is **Active** or **Draft**, and only active ones reach the storefront. Off: every entry counts as active. |
| Admin filter, per field | Any type except JSON and rich text; up to 50 fields per definition. See [[metafields-capabilities]]. |

Staff access is fixed. Whoever holds the entries permission reads and writes entries. There is no per-definition admin access setting ([[metafields-permissions]]).

### Changing fields later

A field can be added, renamed, have its validations or *required* changed, or be removed. Its **key and type stay**. Changed rules are checked against existing entries in the background. An entry that no longer passes keeps its value and shows the error until it is edited. Removing a field deletes its values in the background.

### Entries

- **Handle**: each entry has a handle, unique within its definition: letters, digits and `-`, up to 255 characters. Made from the display name when not given (*Ana Petrova* → `ana-petrova`, then `ana-petrova-2` if taken). A Nitrogen storefront finds an entry by `type` + `handle`, so the handle is in effect the entry's URL segment.
- **Required fields** must have a value. Fields left empty are simply absent from the entry.
- **Status**: Active or Draft, when the definition has the active/draft status.
- **Unnamed entries** (no display-name value) are shown as *"<definition name> #<id>"*.
- **Upsert**: the Admin GraphQL API's `metaobjectUpsert` creates or updates an entry by type and handle. This is how an import or sync keeps entries in step without looking up ids.
- **Used in**: an entry's page lists where it is referenced, from products, categories, customers and other entries.

### Deleting

- **An entry**: every reference to it is removed. A single reference is cleared, and a list loses the entry. Several entries can be deleted at once, up to 250 per batch, in the background.
- **A definition**: its entries, their values and every reference to them are deleted in the background. Metafield definitions and other metaobjects' fields that reference **only** this definition are deleted with their values. A `mixed_reference` that also allows other definitions only loses this one. The confirmation counts all of this before deleting. The deletion is refused if a smart collection's condition uses a metafield definition it would delete.

## Contrasts

- **Metaobject vs metafield**: a metafield is one field on an existing record. A metaobject is a new kind of record with up to 40 fields of its own. When the same content repeats on many products (a size chart, a material, a brand story), model it as a metaobject entry and reference it, rather than copying text into a metafield on each product.
- **Capabilities**: a metaobject definition has one, the active/draft status. A Nitrogen storefront builds each entry's route from its handle. Content in several languages follows [[metafields-use-case-multilanguage]].
- **Metaobject entries vs CMS pages** ([[page]]): pages are free-form documents with their own storefront URL on classic themes. Entries are structured and shown only where a Nitrogen storefront asks for them.

## Where it applies

- **Settings → Metaobjects**: the metaobject definitions with their entry counts; *Add definition*; each definition's page (`/admin/settings/metafields/metaobjects/{id}`) and its **Entries** list (`…/{id}/entries`), with search by display name or handle and an Active/Draft filter.
- The reference picker on products, categories, customers and entries lists entries by display name.
- Admin GraphQL: `metaobjectDefinitionCreate` / `Update` / `Delete`, `metaobjectCreate` / `Update` / `Upsert` / `Delete`, and `metaobjects(type:, query:)`.
- Storefront API: `metaobject(handle: {type, handle})` and `metaobjects(type:)` ([[metafields-nitrogen]]).

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-definitions]]: the reference metafields that attach entries to products, categories and customers.
- [[metafields-use-cases]]: metaobject patterns to start from.

## Open Questions

- None known.
