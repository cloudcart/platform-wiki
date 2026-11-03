---
type: concept
nav_path: "Settings → Metaobjects → Products | Customers | Categories"
route_name: metafields.definitions
route_path: /admin/settings/metafields/products
aliases: ["Metafield definition", "Product metafields", "Category metafields", "Customer metafields", "custom.key", "namespace and key", "Pinned definitions", "Unstructured metafields", "Metafields card", "Metafields card save bar", "Show all metafields", "Storefront API access", "Customer accounts access", "Validating values…", "Some values are invalid", "Delete the values too", "Дефиниция на метаполе", "Метаполета на продукт", "Метаполета на категория", "Метаполета на клиент"]
tags: [metafields, custom-data, products, categories, customers, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-11-03
source_count: 7
---

# Metafield definitions

> Part of [[metafields-metaobjects]]. See the hub for types, metaobjects, limits and permissions.

## Definition

A **metafield definition** declares one extra field for one kind of owner: *every product has a "Care instructions" text*, *every category may have a "Hero image"*. The values are then filled in per product, category or customer. A definition holds:

| Attribute | Rule |
|---|---|
| Owner type | `PRODUCT`, `CATEGORY` or `CUSTOMER`. A category is a `Collection` on the Storefront API. |
| Name | Shown to staff, up to 255 characters. |
| Description | Optional, up to 255 characters; also returned by the Storefront API. |
| Namespace | 3–255 characters: letters, digits, `-` and `_`. Definitions made in the admin always use **`custom`**. Namespaces beginning `app--` are reserved for apps and refused. |
| Key | 2–64 characters, same characters. |
| Type | One of the types in [[metafields-types]], single or `list.`. |
| Validations | The type's own rules: length, range, choices, regex, allowed domains … |
| Storefront access | The **Storefront API access** switch, *"Nitrogen storefronts can read it."*: `PUBLIC_READ` (default) or `NONE`. |
| Customer account access | Customers only, the **Customer accounts access** select: *No access* `NONE` (default), *Read* `READ` or *Read and write* `READ_WRITE`. See [[metafields-permissions]]. |
| Capabilities | The **Filtering**, **Unique values** and **Smart collections** switches. See [[metafields-capabilities]]. |
| Pinned | Whether, and where, it shows first on the owner's page. |

A value is addressed as `namespace.key`, for example `custom.care_instructions`. The pair is unique per owner type, so a product's `custom.material` and a category's `custom.material` are two separate definitions.

## Scope

### What can change later

**Name, description, validations, access and pinning** can change. **Owner type, namespace, key and type** are fixed from the moment of creation. Changing a type means a new definition and moving the values over.

New validations on a definition that already has values are checked against those values in the background. While the check runs, the page's header carries the badge **Validating values…**, and afterwards **Some values are invalid** if any failed. A value that no longer passes is kept, and shows its error on the owner's page until someone changes it.

### Pinning

Pinned definitions appear in every product's editor, category's window and on every customer's page, in the pinned order, inside the **Metafields** card. The others are under *Show all*. A definition made in the admin is pinned at the end while there is room: 50 pinned per owner type. The order can be rearranged.

### Values without a definition

An integration can write a value whose `namespace.key` has no definition. It is an **unstructured** value:

- it is kept and listed per owner type under *Unstructured*, by namespace, key and type;
- it can only be deleted there, not edited;
- the Storefront API never returns it.

Creating a definition with the same owner type, namespace and key adopts those values and checks them against the definition.

### Deleting a definition

*Delete definition* opens the confirmation *"Delete «{name}»?"*. When it opens it counts the owners with a value (*"{count} products have a value for it."* and likewise). **Delete the values too** is on by default:

- on: *"The values are deleted in the background."*
- off: *"The values stay as unstructured metafields."*

The definition is gone at once. Two exceptions:

- A **reference** or **`id`** definition can only be deleted together with its values, so the box stays on: *"A reference or ID definition is deleted only with its values."*
- A definition that a smart collection uses as a condition cannot be deleted. The refusal names the collections: *"Action cannot proceed. Definition is currently in use by the smart collections …"*

While the values of a deleted definition are being removed or released, a new definition with the same owner type, namespace and key is refused with `TAKEN`: *"The values of a deleted definition with this namespace and key are still being released; try again shortly."*

### When an owner or a referenced record is deleted

Deleting a product, category or customer deletes its metafield values. Deleting a record that values **point to** removes the pointer everywhere. This covers a product, variant, category, customer, page, file or metaobject entry. A single reference is cleared; a list loses that item and is removed when nothing is left. Very large clean-ups finish in the background.

## Contrasts

- **Definition vs value**: the definition is set once in Settings by whoever has the definitions permission. Values are edited on each owner's page by whoever may edit that owner ([[metafields-permissions]]).
- **Admin-made vs API-made**: in the admin the namespace is always `custom`. The Admin GraphQL API may use any other valid namespace (`specs`, `erp`, `seo` …) to keep groups of fields apart. The Storefront API needs the namespace on every read, because there is no app-reserved default.
- **Metafield vs metaobject field**: a metaobject's fields have no namespace, pinning, or storefront access of their own. They follow their metaobject definition ([[metaobjects-definitions]]).

## Where it applies

- **Settings → Metaobjects → Products / Customers / Categories** (`/admin/settings/metafields/products`, `…/customers`, `…/categories`): the list, *Add definition*, *Unstructured*.
- The **Metafields** card, saved differently on each owner's page:
  - **Product editor** (`/admin/products/edit/:id`, below the Categories card): with the page's save bar, all or none. *Add product* saves a draft first, so a new product shows its fields at once.
  - **Category window** (Products → Categories, `/admin/products/categories`): with the window's save. A new category shows the definitions without values; changed values go with the create, and a refused value creates no category.
  - **Customer page** (`/admin/customers/details/:id`, above the tabs, between the note and the customer's tags): the card has **its own save bar**, which saves only the metafield values, all or none. The bar appears when a value differs from the saved one, and *Discard* puts the saved values back.
  - A refused value shows on its field.
  - The card's own texts: *Show all ({count})*, *Show pinned only*, *"No metafield is pinned."*, *"No metafield definitions yet. They are added in Settings → Metaobjects."*, and *"The metafields could not be loaded."* with *Try again*.
- Admin GraphQL: `metafieldDefinitionCreate`, `metafieldDefinitionUpdate`, `metafieldDefinitionDelete`, `metafieldDefinitionPin` / `Unpin`, and `metafieldsSet` (up to 25 values per call) / `metafieldsDelete` (up to 250), see [[metafields-admin-api]].

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: the types a definition can have.
- [[products-smart-collections]]: collections that can depend on a product definition.

## Open Questions

- None known.
