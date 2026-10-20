---
type: concept
nav_path: "Settings → Staff → permissions; Settings → PAT Tokens → scopes"
aliases: ["Metafield permissions", "Metaobject permissions", "Who can edit metafields", "Metafields and metaobjects permission", "Metaobjects permission", "metaobjects scope", "metaobjects:read", "Storefront access PUBLIC_READ", "Customer account access", "PUBLIC_READ", "READ_WRITE", "Права за метаполета", "Права за метаобекти", "Видимост в сторфронта"]
tags: [metafields, metaobjects, custom-data, permissions, security, storefront-api, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Metafields and metaobjects: permissions and visibility

> Part of [[metafields-metaobjects]]. See the hub for definitions, types and limits.

## Definition

Three separate questions decide who sees and changes metafield and metaobject data:

1. **Staff in the admin**: which permission sections a staff member holds ([[settings-staff]]).
2. **API tokens**: which scopes a personal access token carries, on top of its owner's sections ([[settings-pat-tokens]]).
3. **The storefront and the shopper**: the storefront access set on each definition, and for customers, the customer account access.

The store owner passes every check.

## Scope

### Staff and token rules

| What | Staff permission (any of) | Token scope to change | Token scope to read |
|---|---|---|---|
| Metafield and metaobject **definitions** | Settings, or Settings → **Metafields and metaobjects** | `settings` | `settings:read` |
| **Product** values | Products, or Products → Products | `products` | `products:read` |
| **Category** values | Products, or Products → Categories | `products` | `products:read` |
| **Customer** values | Customers | `customers` | `customers:read` |
| Metaobject **entries** | **Metaobjects** | `metaobjects` | `metaobjects:read` |
| Picking or uploading a **file** for a file field | Settings, or Settings → Files | `settings` | `settings:read` |
| Metafield conditions in **smart collections** | Products, or Products → Smart Collections | `products` | `products:read` |

- A token with `full-access` has every scope. `read-only` reads everything and changes nothing.
- **Values follow their owner**: whoever may open a product page may edit its metafields. Definitions are a separate, Settings-level permission. A staff member can fill in values without being able to add or change definitions.
- **Entries vs definitions**: with **Metaobjects** alone, a staff member sees the metaobject definitions in Settings → Metaobjects and adds, edits and deletes their entries, but changes no definition.
- **Reference pickers**: someone who may edit products but not entries can still pick entries in a product's reference field. Only the definitions that the product's reference fields allow are offered.
- **What a reference reveals**: on the admin side, a reference shows its target only to someone who may read that target. A product editor without customer access sees a customer reference only as its id. A page or a file needs nothing more than the value.
- **Showing a file**: no file permission is needed to see a file a value already holds. Picking a different one, or uploading, needs the Files permission.
- **Who made it**: each definition records which staff member, or which token, created it.

### Storefront visibility

Set on each definition, and read the same way by every Nitrogen storefront ([[headless-storefront-api]]):

| Data | Readable on the Storefront API when |
|---|---|
| A product or category metafield | its definition's storefront access is `PUBLIC_READ` (the default) |
| A customer metafield | the shopper **is that customer**, signed in with their customer access token, and the definition's customer account access is `READ` or `READ_WRITE`. Customer definitions are never public. |
| A metaobject entry and its fields | its definition's storefront access is `PUBLIC_READ`, and, with the active/draft status, the entry is **Active** |
| A value with no definition | never |

- **Visibility is per definition, not per field.** Every field of a `PUBLIC_READ` metaobject definition is readable on the storefront. Staff-only data goes in a separate definition with storefront access `NONE`.
- **`NONE`** keeps a definition admin-only: internal codes, purchase notes, supplier data. The value exists, but the storefront never sees it, whatever the token.
- **`READ_WRITE`** is accepted for customer definitions, but the storefront cannot write metafields yet; it behaves as `READ`. A shopper cannot change their own customer metafields from a Nitrogen storefront.
- **Customer references** never return the customer on the Storefront API. The value holds only the id.
- **References to hidden records** come back empty: a referenced product or entry that the storefront does not show is left out of `reference` and `references`.

## Contrasts

- **Storefront access vs storefront token scopes**: a Nitrogen storefront's token scopes ([[headless-storefront-api]]) decide which parts of the API it may call. Whether a given metafield or entry is visible is decided by its definition. Two storefronts of the same store see the same metafields.
- **Customer account access vs customer custom fields**: custom fields ([[customers-custom-fields]]) are filled in and changed by the shopper. Customer metafields are written by the store and, at most, read by the shopper.
- **Definitions permission vs Settings as a whole**: Settings → Metafields and metaobjects can be granted alone, without the rest of Settings.

## Where it applies

- **Settings → Staff** → a staff member's permissions: *Metaobjects* (entries) and, under *Settings*, *Metafields and metaobjects* (definitions).
- **Settings → PAT Tokens** → scopes: *Metaobjects* / *Metaobjects (Read)*, beside *Settings*, *Products* and *Customers*.
- The **Storefront access** and **Customer account access** choices on each metafield definition, and Storefront access on each metaobject definition.
- Refusals name what is missing, e.g. *"Changing metaobject entries needs the "metaobjects" permission."*

## Related

- [[metafields-metaobjects]]: hub.
- [[settings-staff]]: granting permission sections to staff.
- [[settings-pat-tokens]]: token scopes for the Admin GraphQL API.
- [[headless-customer-accounts]]: how a shopper signs in on a Nitrogen storefront.

## Open Questions

- None known.
