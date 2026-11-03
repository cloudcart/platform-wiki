---
type: concept
nav_path: "Settings → Webhooks"
aliases: ["Metafields in webhooks", "Webhook metafields", "metafields_omitted", "customer_metafields", "category_metafields", "Метаполета в уебхук", "Метаполета в webhook"]
tags: [metafields, webhooks, api, integrations, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

# Metafields in webhooks

> Part of [[metafields-metaobjects]]. See the hub for definitions, types and limits. The webhook events themselves are on [[settings-hooks-events]].

## Definition

Product, customer, category and order webhooks carry the metafield values of what they are about, so a connected system receives them without a separate read. Values without a definition are left out.

## Scope

### Product, customer and category events

`product.created`, `product.updated`, `customer.created`, `customer.updated`, `category.created` and `category.updated` get a `metafields` key next to the rest of the payload, which stays as it was:

```json
{
  "metafields": [
    { "namespace": "custom", "key": "material", "type": "single_line_text_field", "value": "Cotton" }
  ]
}
```

### Order events

`order.created` and `order.updated` carry the values of the order's customer, its products and their categories. Where they sit depends on the webhook's **"It is used on a new structure"** toggle ([[settings-hooks-events]]):

| Owner | New structure | Legacy structure |
|---|---|---|
| Customer | `customer.metafields` | `customer_metafields` |
| Product | `products[].metafields` | `products[].metafields` |
| Category | `products[].category.metafields` | `products[].category_metafields` |

An order with no customer has an empty customer list.

### Very large orders

Many order lines multiply the values. A body that would pass 8 MiB with them goes out **without** them and with `metafields_omitted: true`, so the order's event is still delivered.

### What sends an event

- **Saving only values** sends one `updated` per owner: the Metafields card's save in the admin, `metafieldsSet` and `metafieldsDelete` on the [[metafields-admin-api|Admin GraphQL API]], and a category's save that changed only values.
- **A new category:** `category.created` waits until the save is finished, so its payload carries the values saved with it.
- **Background jobs** send no event for the values they write.

### Null values

The webhook strips null fields from a payload, but not inside these lists. A value that is the text `null` stays as it is.

## Contrasts

- **Metafields vs custom fields.** `customer_custom_fields` in a legacy order body are the customer's [[customers-custom-fields|custom fields]], a separate feature.
- **Webhook vs a read.** A webhook carries each value as a string, in the format of [[metafields-value-formats]].

## Where it applies

- [[settings-hooks]] and [[api-webhooks]]: subscribing to the events.
- [[metafields-definitions]]: the definitions a value needs in order to be sent.

## Related

- [[metafields-metaobjects]]: hub.
- [[settings-hooks-events]]: the event catalogue and payload shapes.
- [[settings-hooks-delivery]]: when a payload goes out.

## Open Questions

- None known.
