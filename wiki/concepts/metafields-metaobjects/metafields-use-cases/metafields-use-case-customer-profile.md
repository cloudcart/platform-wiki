---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Customer profile, loyalty and service data"
aliases: ["Customer metafields loyalty", "Loyalty tier metafield", "Customer preferences metafield", "VIP customer", "Personal stylist", "Customer notes metafield", "Лоялна програма", "Ниво на клиента", "VIP клиент", "Предпочитания на клиента", "Бележки за клиента"]
tags: [metafields, use-case, customers, loyalty, customer-account]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: customer profile, loyalty and service data

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

A store knows things about its customers that the platform has no field for:
- a loyalty tier and a points balance kept in a till or loyalty system;
- the customer's preferred shop;
- a personal stylist;
- clothing sizes noted in store;
- a service note such as *"prefers phone calls"*.

**Customer metafields** keep these on the customer record. Each definition decides whether the customer sees it on their **own account page** in a Nitrogen storefront, or whether it stays staff-only.

## Scope

### The data model

Customer metafields (owner type `CUSTOMER`), split by who should see them:

| `namespace.key` | Type | Customer account access | Purpose |
|---|---|---|---|
| `custom.loyalty_tier` | `metaobject_reference` → `loyalty_tier` | `READ` | Shown on the account page with its perks. |
| `custom.points` | `number_integer`, `min` 0 | `READ` | Balance synced from the loyalty system. |
| `custom.member_since` | `date` | `READ` | |
| `custom.preferred_store` | single-line text | `READ` | A shop id from `storeLocations` ([[apps-stores]]). |
| `custom.stylist` | single-line text | `READ` | The personal advisor's name. |
| `custom.sizes` | `json` | `READ` | `{"shirt": "M", "shoe": "42"}`, noted in store. |
| `custom.service_note` | multi-line text | `NONE` | Staff only. |
| `custom.risk_flag` | `boolean` | `NONE` | Staff only. |

**Metaobject definition `loyalty_tier`**: `name` (display name: *Gold*), `color` (`color`), `perks` (rich text), `threshold` (`number_integer`), `icon` (file).

### Who reads what

- **Staff** see and edit the values in the **Metafields** card on the customer's page, given the Customers permission ([[metafields-permissions]]).
- **The customer** sees only the `READ` ones, and only their own. A Nitrogen account page reads them through `customer { metafields(identifiers: …) }` with the customer's access token ([[headless-customer-accounts]]).
- **Nobody else**: customer metafields are never public, whatever their storefront access. A customer reference on another record never reveals the customer on the storefront.
- **Integrations** write the values with the Admin GraphQL API (`metafieldsSet`), e.g. a nightly sync of points from a loyalty or POS system, with a token holding the `customers` scope.

### What the customer cannot do

The customer cannot change these values from the storefront. `READ_WRITE` is accepted but acts as `READ` ([[metafields-nitrogen]]). Data the customer should **enter or edit** belongs in customer custom fields ([[customers-custom-fields]]).

## Contrasts

- **Metafields vs customer custom fields**: custom fields are asked at checkout or registration and edited by the customer. Metafields are written by the store or a system and at most read by the customer.
- **Metafields vs customer groups** ([[customer-group]]): groups drive prices, payment and shipping rules and discount targeting. A tier stored as a metafield **changes nothing** in the cart. When a tier must change prices, the customer is also put in the matching group, and the metafield only describes the tier.
- **Segments**: customer segments ([[marketing-segments]]) work on the platform's own data and custom fields, not on metafields, at the time of writing.

## Where it applies

- Retailers with a loyalty programme in a till or third-party system, personal-shopping and VIP services, stores combining online and in-store service.
- Up to 256 customer definitions and 50 pinned on the customer page ([[metafields-limits]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[metafields-permissions]]: customer account access.
- [[customers-custom-fields]]: fields the customer fills in.
- [[metafields-use-case-b2b-accounts]]: business customers' account data.

## Open Questions

- None known.
