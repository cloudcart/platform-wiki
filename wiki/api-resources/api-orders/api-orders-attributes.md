---
type: api-resource
resource_path: /api/v2/orders
http_methods: [GET, PATCH]
related_entity: order
related_features: [orders, orders-details]
aliases: ["Orders API attributes", "orders writable fields", "orders read-only fields", "orders includes", "orders filtering sorting", "orders meta append", "API поръчки полета"]
tags: [api, json-api-v2, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Orders API — attributes, relationships & querying

> Part of [[api-orders]]. See the hub for the other aspects (side effects & failure modes, examples & testing).

## Purpose

This aspect is the **read/write field reference** for the `orders` resource: which attributes a PATCH may write, which are read-only but returned by GET, the relationship + allowed-include list, the `meta` sparse-field append, and the complete filtering / sorting / pagination reference for collection reads.

## Endpoint

This aspect describes the payload shape for `GET /api/v2/orders`, `GET /api/v2/orders/{id}`, and the attribute portion of `PATCH /api/v2/orders/{id}`. Base URL, auth, and headers: see [[json-api-v2]]. The cascade those PATCH writes trigger is on [[api-orders-side-effects]].

## Attributes

**Writable on PATCH** (no attribute is writable on POST — POST is blocked entirely):

| Attribute | Type | Required? | Validation | Notes |
|---|---|---|---|---|
| `status` | string | optional | must be one of the platform's status keys (default + merchant custom) | Triggers the same status-transition pipeline as the admin-panel status pill — see [[api-orders-side-effects]] and [[orders-status-change]]. Hard gates apply; invalid transitions return 422 with the localised gate-violation message. |
| `invoice_number` | string | optional | unique across orders; **can only be set once per order** | Subsequent PATCH attempts to overwrite return 422 *"You can set invoice number only once."* When set, also auto-stamps `invoice_date` to `now` if it was empty. |
| `invoice_date` | datetime (`Y-m-d H:i:s`) | optional | `date_format:Y-m-d H:i:s` | Manual invoice date override. |
| `usn` | string | optional | min 1, unique across orders; **can only be set once per order** | Merchant-defined external reference (accounting systems use this). Subsequent PATCH attempts to overwrite return 422 *"You can set USN only once."* |

**Read-only on PATCH** (returned by GET, validator rejects them in the payload):

`customer_id`, `customer_group_id`, `customer_first_name`, `customer_last_name`, `customer_email`, `customer_ip`, `customer_geoip`, `note_customer`, `abandoned`, `currency`, `status_fulfillment`, `desired_delivery_date`.

These are snapshotted at order creation time (per [[cart-vs-order-lifecycle]]) or managed elsewhere — `status_fulfillment` flips through [[api-order-fulfillment]]; `abandoned` is the [[abandoned-cart-recovery]] flag; `currency` is frozen at draft time; customer-snapshot fields are immutable so an order always reflects who the buyer was at the moment of purchase.

**Other GET-visible attributes** (not exhaustive — the model exposes everything except the platform-internal `date_locking`, `moderator_id`, `manual`, `locale` columns, which are hidden by the schema):

- `id`, `date_added`, `updated_at`, `date_archived` — lifecycle timestamps.
- `total`, `subtotal`, `tax`, `discount`, `shipping_price` — money fields (in store currency minor units).
- `notify_customer` — per-order toggle that gates customer notification emails (see [[orders-notify-customer]]).
- `status_fulfillment` — `not_fulfilled` / `partial` / `fulfilled`.
- `shipping_from`, `shipping_to`, `shipping_date` — date fields cast to the site's local timezone (ISO 8601) by the schema.
- `desired_delivery_date` — appended accessor for the customer's requested delivery date.

**Sparse-field append values:** `meta` is the only allowed value for `?append[orders]=`. Other values return 422 if a bogus append key is sent. Use `?append[orders]=meta` to surface the order's `meta` JSON payload (custom data attached by apps or the merchant).

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `products` | hasMany | order-products | Line items. See [[api-order-products]]. |
| `discounts` | hasMany | order-discount | Applied discounts. See [[api-order-discount]]. |
| `modifications` | hasMany | order-modification | Post-placement modifications. See [[api-order-modification]]. |
| `totals` | hasMany | order-total | Totals breakdown (subtotal, shipping, tax, discount, grand total). See [[api-order-total]]. |
| `taxes` | hasMany | order-tax | Per-bracket tax rows. See [[api-order-tax]]. |
| `payment` | hasOne | order-payment | Payment record. See [[api-order-payment]]. |
| `shipping` | hasOne | order-shipping | Shipping selection (provider, amount, geo zone). See [[api-order-shipping]]. |
| `shipping-address` | hasOne | order-shipping-address | Recipient address snapshot. See [[api-order-shipping-address]]. |
| `billing-address` | hasOne | order-billing-address | Invoice address snapshot. See [[api-order-billing-address]]. |

**Allowed include paths:** `products`, `payment`, `discounts`, `modifications`, `totals`, `taxes`, `shipping.provider`, `shipping-address`, `billing-address`. Nested includes beyond `shipping.provider` are NOT permitted; the framework returns 400 if an unlisted path is requested. Note that `products.options` is reachable through the framework's auto-merged schema relationships (the schema declares it) even though the validator doesn't list it explicitly — verify in integration if needed.

## Filtering & sorting

**Allowed filtering parameters:**

| Parameter | Type | Behaviour |
|---|---|---|
| `filter[start_date]` | datetime | Internally rewritten to `WHERE date_added >= ?`. Forces the `idx_date_added` index hint when used. |
| `filter[end_date]` | datetime | Internally rewritten to `WHERE date_added <= ?`. Forces the `idx_date_added` index hint when used. |
| `filter[geo_zone_id]` | integer | Match on the order's computed [[geo-zone\|Geo Zone]]. |
| `filter[geo_zone_name]` | string | Match on the geo-zone name snapshot. |
| `filter[<any column>]` | per column | The framework auto-merges every column on the `orders` table into the allowed-filters list — exact-equality only. There is NO generic comparison-operator syntax (`>`, `<`, `in`, `like` etc.). For date ranges use the dedicated `start_date` / `end_date` filters above. |

**Allowed sort parameters:** `id`, `date_added`, `updated_at`, `date_archived`. Prefix with `-` for descending. Sorting on a column outside this list returns 422.

**Pagination:** standard JSON:API `page[number]` (1-based) and `page[size]` (1–100, default 20). See [[json-api-v2]] for full pagination semantics.

For bulk-fetch loops, prefer `filter[start_date]` / `filter[end_date]` over synthesising column filters — they carry the forced index hint and are the only date-range mechanism (there are no comparison operators). Worked queries: see [[api-orders-examples]].

## Side effects

Reads (`GET`) have no side effects. The four writable attributes each carry write-time behaviour: `status` runs the transition pipeline, `invoice_number` / `usn` are single-write with uniqueness checks, and `invoice_number` auto-stamps `invoice_date`. The full cascade and failure catalogue are on [[api-orders-side-effects]].

## Equivalent UI

- [[orders]] — the orders list mirrors `GET /api/v2/orders`; the merchant column filters map to the equality filters here.
- [[orders-details]] — the detail view renders the same attribute envelope a single GET (with includes) returns.

## Related

- [[api-orders]] — hub.
- [[api-orders-side-effects]] — what the writable attributes trigger; failure modes.
- [[api-orders-examples]] — worked GET requests with filters / includes.
- [[json-api-v2]] — equality-only filter rule, pagination semantics, auth.
- [[cart-vs-order-lifecycle]] — when `currency` + customer-snapshot fields freeze.
- [[order]] — full order entity attribute reference.
- [[abandoned-cart-recovery]] — the `abandoned` flag.
- [[orders-notify-customer]] — the `notify_customer` per-order toggle.
- [[api-order-products]], [[api-order-payment]], [[api-order-shipping]], [[api-order-total]], [[api-order-tax]], [[api-order-discount]], [[api-order-modification]], [[api-order-shipping-address]], [[api-order-billing-address]] — included sub-resources.

## Open questions

- Confirm whether the `desired_delivery_date` accessor returns a string or a datetime object across all locales (the schema appends it; the underlying column type may differ per legacy migrations). `(verify)`
- Confirm whether `products.options` can be requested as an include path in practice, given the validator doesn't list it but the schema declares the relationship. `(verify)`
