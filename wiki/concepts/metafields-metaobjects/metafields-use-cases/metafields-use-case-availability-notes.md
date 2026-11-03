---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Lead times, pre-orders and delivery notes"
aliases: ["Lead time metafield", "Pre-order date", "Restock date", "Made to order", "Ships separately", "Bulky item note", "Delivery note per product", "Срок за доставка", "Предварителна поръчка", "Очаквана наличност", "Изработка по поръчка", "Обемна стока"]
tags: [metafields, use-case, products, availability, shipping, messaging]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: lead times, pre-orders and delivery notes

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Shoppers want to know **when** they will get a product, and **what is special** about delivering it:

- *"Made to order — ships in 3 weeks"*;
- *"Back in stock on 15 November"*;
- *"Pre-order: released 1 December"*;
- *"Delivered by pallet, kerbside only"*.

The platform's **product statuses** already give a stock-based label (*In stock*, *Out of stock*, *On request* …) that the Storefront API returns with each product ([[product-status]]). **Product metafields** add the product-specific facts behind that label, so a Nitrogen storefront can say exactly when and how.

## Scope

### The data model

| `namespace.key` | Type | Purpose |
|---|---|---|
| `custom.lead_time` | `duration` (days or weeks) | Production or supplier time for made-to-order items. |
| `custom.restock_on` | `date` | Expected date back in stock. |
| `custom.release_on` | `date` | Pre-order release date. |
| `custom.preorder_note` | single-line text, `max` 120 | *"Ships from 1 December"*. |
| `custom.ships_separately` | `boolean` | Delivered apart from the rest of the order. |
| `custom.delivery_kind` | single-line text, `choices`: *Parcel, Pallet, Two-person delivery, Collection only* | **Smart-collection condition** on. |
| `custom.assembly_required` | `boolean` | |
| `custom.handling_note` | multi-line text | *"Kerbside delivery; please be present"*. |

A **category** can carry a default `custom.lead_time` for everything in it (e.g. all sofas: 6 weeks). The storefront uses the product's value when present.

### On the Nitrogen storefront

- **Product page**: beside the native status label, *"Made to order — about 3 weeks"* from `custom.lead_time`, or *"Back on 15 November"* from `custom.restock_on` when the product is out of stock.
- **Pre-orders**: when `custom.release_on` is in the future, the storefront labels the button and shows the date.
- **Cart**: the storefront repeats the notes on the cart lines that carry them, e.g. *"This item ships separately"*, by reading the line's product.
- **Collections**: *"Two-person delivery"* or *"Collection only"* gathers matching products in a smart collection from `custom.delivery_kind` ([[products-smart-collections]]).

### What the metafields do not change

These are **messages**:
- They do not change stock, availability or whether the product can be bought. Those come from quantities and the product's status ([[product-status]]).
- They do not change delivery prices or couriers ([[shipping-calculation]]).
- They do not change delivery days and time slots ([[delivery-scheduling]]).

A date in `restock_on` does not open the product for ordering; only stock and status do.

## Contrasts

- **Product status vs metafields**: the status is the platform's rule-driven label and is used everywhere, including classic themes and feeds. The metafields give per-product detail that only a Nitrogen storefront shows.
- **Per product vs per variant**: the values sit on the product. A lead time that differs by variant (a fabric colour made to order) goes in a `json` map on the product, keyed by variant SKU.
- **Notes vs shipping rules**: if bulky items must cost more to ship, that is a shipping rule. The metafield only explains it to the shopper.

## Where it applies

- Furniture and made-to-order goods, pre-release books, games and electronics, seasonal stock, oversized and fragile items, products delivered by supplier.
- Integrations can keep `restock_on` and `lead_time` current from a supplier feed with `metafieldsSet` ([[metafields-use-case-integration-data]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[product-status]]: native availability labels.
- [[delivery-scheduling]]: how delivery days are actually decided.
- [[shipping-calculation]]: how delivery is priced.

## Open Questions

- None known.
