---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Integration keys and back-office data"
aliases: ["ERP id metafield", "PIM id", "Supplier code", "Back-office product data", "Internal product data", "Purchase price metafield", "metafieldsSet integration", "metaobjectUpsert sync", "Код от ERP", "Код на доставчик", "Вътрешни данни за продукт", "Синхронизация с ERP"]
tags: [metafields, metaobjects, use-case, integrations, erp, admin-graphql]
plan_gates: []
created: 2026-10-20
updated: 2026-10-21
source_count: 4
---

# Use case: integration keys and back-office data

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Not every metafield is for shoppers. Integrations and staff need data the storefront must never show:

- a PIM or ERP code that has no place in SKU or barcode;
- the supplier's own article number and order page;
- a customs tariff code;
- a sourcing note.

Metafields with storefront access **`NONE`** hold this on the product, category or customer. The **`id`** type and **unique values** guarantee that a key appears once. Metaobjects synced by an integration (suppliers, warehouses, collections of a PIM) are kept in step with **`metaobjectUpsert`** by handle.

## Scope

### The data model

Product metafields in a namespace per system, created through the Admin GraphQL API:

| `namespace.key` | Type | Storefront access | Notes |
|---|---|---|---|
| `pim.product_id` | `id` | `NONE` | Always unique. The PIM's own key. |
| `supplier.article_no` | single-line text, **unique values** on | `NONE` | Refused if another product already has it. |
| `supplier.order_page` | `url`, `allowed_domains`: the supplier's domain | `NONE` | |
| `supplier.ref` | `metaobject_reference` → `supplier` | `NONE` | |
| `customs.hs_code` | single-line text, `regex` `^[0-9]{6,10}$` | `NONE` | |
| `ops.sourcing_note` | multi-line text | `NONE` | |
| `pim.raw` | `json` | `NONE` | An unparsed payload kept for troubleshooting, up to 128 KB. |

**Metaobject definition `supplier`**, storefront access `NONE`: `name`, `contact_email`, `lead_time` (`duration`), `min_order` (`money`), `portal` (`url`). The handle is the supplier's code in the ERP, so a sync can upsert it.

### How an integration works with it

- **Authenticate** with a personal access token ([[settings-pat-tokens]]) holding the narrowest scopes: `products` for product values, `settings` to create definitions, `metaobjects` for entries.
- **Write values** with `metafieldsSet`, up to 25 per call, across products, categories and customers in one call when the token has each scope. One owner, namespace and key holds one value. Writing again replaces it. The owner is named by its plain id, a referenced record by its global ID ([[metafields-admin-api]]).
- **Find by key**: with the admin filter on `pim.product_id`, the Admin GraphQL `products(query: "metafields.pim.product_id:P-10442")` returns the product ([[metafields-capabilities]]).
- **Sync entries** with `metaobjectUpsert(handle: {type: "supplier", handle: "SUP-017"}, …)`: it creates the entry the first time and updates it afterwards.
- **Values without a definition** are accepted as *unstructured* values. They are checked only against the type sent with them, with no validations, admin filter or unique values. Defining the key first avoids that ([[metafields-definitions]]).

### Admin visibility

Pinned definitions show in the product's **Metafields** card, so buyers and category managers see the supplier data where they work. Unpinned ones stay under *Show all*.

## Contrasts

- **Metafields vs the external-record mapping** ([[external-record-mapping]]): the platform's built-in integrations (ERP connectors, XML and CSV imports) already keep their ID-to-ID links in a mapping table of their own. Metafields suit a **custom** integration that needs a visible, filterable, unique key on the record, or data beyond a key.
- **Metafields vs SKU and barcode**: SKU and barcode are the platform's own identifiers, used by orders, feeds and stock. A second identifier from another system goes in a metafield rather than overloading them.
- **`NONE` vs not pinning**: unpinned only affects the admin's layout. `NONE` is what keeps a value off the storefront.

## Where it applies

- Stores with a PIM, an ERP or a supplier portal connected by a custom integration; stores that buy from many suppliers; cross-border sellers needing customs data.
- Up to 256 product definitions per store, 50 of them with the admin filter ([[metafields-limits]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[external-record-mapping]]: the built-in integrations' ID map.
- [[erp-integrations]]: connecting an ERP.
- [[settings-pat-tokens]]: tokens and scopes for the Admin GraphQL API.

## Open Questions

- None known.
