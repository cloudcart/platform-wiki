---
type: api-resource
resource_path: /api/v2/store-quantity
http_methods: [GET, POST, PATCH, DELETE]
related_entity: product
related_features: [products-inventory, apps-stores, apps-store-locations]
aliases: ["Store quantity API", "Per-warehouse stock API", "Multi-store stock API", "Shop quantity API", "JSON-API v2 store-quantity", "API наличности по магазин", "/store-quantity"]
tags: [api, json-api-v2, multistore, inventory]
plan_gates: [stores]
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Store quantity (JSON-API v2)

## Purpose

A `store-quantity` resource is one **per-warehouse stock row** — a single `(product, variant, store)` triple carrying the available `qty` at that store. This is the canonical multi-warehouse stock surface: external ERP / WMS / inventory systems write one row per tuple so the storefront reflects accurate availability per warehouse. The `(shop_id, product_id, variant_id)` triple is **enforced unique** — re-POSTing the same triple returns 422 `Duplicate Entry`. To "move" stock between stores, DELETE the old row and POST a new one (atomicity is the integrator's responsibility).

Single-warehouse stores write stock through the [[api-variants|variants]] `quantity` field instead and ignore this resource; multi-warehouse stores write per-store rows here and treat `variants.quantity` as a legacy total.

## Endpoint

- **URL base:** `<store-host>/api/v2/store-quantity/`
- **GET collection** — `GET /api/v2/store-quantity`.
- **GET single** — `GET /api/v2/store-quantity/{id}`.
- **POST** — `POST /api/v2/store-quantity` — requires `qty` + the `store`, `product`, `variant` relationships.
- **PATCH** — `PATCH /api/v2/store-quantity/{id}` — only `qty` changes (the relationship triple is frozen after create).
- **DELETE** — `DELETE /api/v2/store-quantity/{id}`.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/store-quantity/{id}/relationships/<rel>` for `store`, `product`, `variant`, but all three are read-only after create.
- No custom action routes.
- **App-install requirement:** without the Stores app installed every request returns **HTTP 404** `"stores app not installed"`. See [[apps-stores]].

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `qty` | numeric (decimal 20,3, cast to float) | yes | yes | **POST: required**, PATCH: optional | Validation rule is `int`. Stored on `products_quantities.qty`. Fractional values depend on the [[apps-grocery-store-overview-new\|Grocery Store]] app's unit config; without it, treat `qty` as an integer. |
| `shop_id` | — | — | — | — | **Read-only.** Set via the `store` relationship. Frozen after create. |
| `product_id` | — | — | — | — | **Read-only.** Set via the `product` relationship. Frozen after create. |
| `variant_id` | — | — | — | — | **Read-only.** Set via the `variant` relationship. Frozen after create. |
| `created_at` / `updated_at` | timestamp | — | — | — | **Read-only.** System timestamps. |
| `id` | — | — | — | — | Exposed only as the JSON:API `id` member, not as an attribute. The row's natural key is the `(shop_id, product_id, variant_id)` triple. |

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `store` | hasOne (belongsTo) | stores | **required at POST** | Wire name `store` maps to model relation `shop`. The physical store / warehouse. Frozen after create. |
| `product` | hasOne (belongsTo) | products | **required at POST** | The product. Frozen after create. |
| `variant` | hasOne (belongsTo) | variants | **required at POST** | The variant — must be specified explicitly even for single-variant products; no "default variant" auto-lookup. Frozen after create. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters declared. All raw columns on `products_quantities` are auto-allowed (e.g. `filter[shop_id]=2`, `filter[product_id]=123`, `filter[variant_id]=456`).

**Allowed sort parameters** — `id`, `shop_id`, `qty`, `product_id`, `variant_id`. Prefix with `-` for descending.

**Allowed include paths** — auto-allowed from schema: `store`, `product`, `variant`.

## Side effects on write

POST:
- **Uniqueness guard** — duplicate `(shop_id, product_id, variant_id)` triples are rejected with 422 `Duplicate Entry`. Use PATCH to update an existing row.
- **Variant ↔ product consistency** — the check that a `variant` belongs to its `product` (i.e. `variant.item_id == product_id`) is **currently disabled**. A variant from a different product saves successfully but produces inconsistent storefront behaviour, so integrators should respect the invariant client-side.

PATCH:
- Only `qty` changes are accepted; the relationship triple is frozen.

DELETE:
- Removes the row. Deleting the parent product or shop cascades and drops their stock rows.

Storefront / order pipeline side-effects (apply equally to writes from this endpoint and from the admin UI on [[apps-stores]]):
- **Storefront stock recompute** — the next storefront request for the affected product / variant re-reads per-store stock. With [[apps-store-locations]] installed, the customer's `store_location` cookie maps to one geo-zone-bound store and the storefront returns THAT store's `qty` (not a sum across stores).
- **`continue_selling` interaction** — when `qty <= 0` AND the parent product has `continue_selling = no`, the variant is hidden / disabled in the storefront for customers in that store's geo zone.
- **Order decrement / restore** — orders pulling from this store decrement the corresponding `qty`; cancellation / abandonment restores it (see [[inventory-tracking]]).
- **No `store-quantity.*` webhook** — no per-row event exists in the platform catalogue (see [[settings-hooks]]); integrations needing change notifications must poll this endpoint OR subscribe to `order.created` / `order.updated` and read the stock delta there.
- **No platform-level audit log** beyond model timestamps.

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`. Requires the [[apps-stores|Stores]] app.

### GET collection (filter by store / product, sort, sideload)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/store-quantity?page[size]=50&filter[shop_id]=2&sort=-qty&include=store,product,variant"
```

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/store-quantity?filter[product_id]=42&filter[variant_id]=101"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/store-quantity/1024?include=store,product,variant"
```

### POST create (one stock row per `(store, product, variant)` triple)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/store-quantity" \
     -d '{
       "data": {
         "type": "store-quantity",
         "attributes": { "qty": 25 },
         "relationships": {
           "store": { "data": { "type": "stores", "id": "2" } },
           "product": { "data": { "type": "products", "id": "42" } },
           "variant": { "data": { "type": "variants", "id": "101" } }
         }
       }
     }'
```

### PATCH update (only `qty` changes — relationship triple is frozen)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/store-quantity/1024" \
     -d '{
       "data": {
         "type": "store-quantity",
         "id": "1024",
         "attributes": { "qty": 50 }
       }
     }'
```

### DELETE (to "move" stock, DELETE + re-POST the row)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/store-quantity/1024"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "store-quantity",
      "id": "1024",
      "attributes": {
        "shop_id": 2,
        "product_id": 42,
        "variant_id": 101,
        "qty": 25,
        "created_at": "2026-06-01 09:13:00",
        "updated_at": "2026-06-04 16:00:00"
      },
      "relationships": {
        "store": { "data": { "type": "stores", "id": "2" } },
        "product": { "data": { "type": "products", "id": "42" } },
        "variant": { "data": { "type": "variants", "id": "101" } }
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "store-quantity",
    "id": "1130",
    "attributes": {
      "shop_id": 2,
      "product_id": 42,
      "variant_id": 101,
      "qty": 25,
      "created_at": "2026-06-05 11:08:00",
      "updated_at": "2026-06-05 11:08:00"
    },
    "relationships": {
      "store": { "data": { "type": "stores", "id": "2" } },
      "product": { "data": { "type": "products", "id": "42" } },
      "variant": { "data": { "type": "variants", "id": "101" } }
    }
  }
}
```

### Common failures

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found","detail":"stores app not installed"}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Duplicate Entry","source":{"pointer":"/data/relationships/store"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The qty field is required.","source":{"pointer":"/data/attributes/qty"}}]}
```

## Testing checklist

1. `GET /stores` (via [[api-stores]]) — capture a `shop_id` to use below; if you get 404 `stores app not installed`, the app needs activation.
2. `GET /store-quantity?filter[shop_id]={shop_id}&page[size]=5` — confirm 200.
3. `POST /store-quantity` with a `(store, product, variant)` triple that does not yet exist — capture returned id.
4. `GET /store-quantity/{id}?include=store,product,variant` — verify the triple matches the create payload.
5. `PATCH /store-quantity/{id}` with `{"attributes":{"qty":999}}` — confirm 200.
6. `POST /store-quantity` with the **same** triple again — verify 422 `Duplicate Entry`.
7. `POST /store-quantity` without `qty` — verify 422 with pointer `/data/attributes/qty`.
8. `DELETE /store-quantity/{id}` — verify 204.
9. `GET /store-quantity/{id}` — verify 404.

## Equivalent UI

- [[apps-stores]] — the per-store **Products** tab → quantity-update modal. Manual per-store stock edits.
- [[products-inventory]] — bulk stock + price edits across the catalog (single-warehouse merchants edit `variants.quantity` here; multi-warehouse merchants see this column as the sum across all stores).
- [[apps-store-locations]] — geo-zone routing layer that maps customer location → which store's stock to show.

## Related

- [[json-api-v2]] — protocol contract.
- [[api-stores]] — read-only enumeration of warehouses / pickup points. **Always pair these two.**
- [[api-products]] — product catalog (the entities stock is tracked against).
- [[api-variants]] — variant resource. `variants.quantity` is the single-warehouse counterpart.
- [[apps-stores]] — admin UI for physical stores + per-store stock editor.
- [[apps-store-locations]] — geo-zone storefront routing (consumes these stock rows).
- [[products-inventory]] — admin-panel bulk inventory editor.
- [[inventory-tracking]] — stock decrement / restore pipeline reference.
- [[settings-hooks]] — webhook subscriptions (no dedicated `store-quantity.*` event).
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm the exact aggregation rule used for low-stock notifications on multi-warehouse stores (sum-across-all-stores vs per-store threshold).
- Verify the `variants.quantity` single-warehouse field's behaviour when [[apps-stores]] is installed — does it auto-sum across stores at read time or remain a stale legacy column?
- Document whether float `qty` values are accepted for products tied to a Grocery Store unit configuration with `decimals > 0` (validator says `int`; column cast is `float`).
- Confirm whether DELETE on a `store-quantity` row triggers any cart-level recompute for in-progress carts holding that variant.
- The validator's commented-out `validateVariant` check (variant must belong to product) is currently disabled — verify whether this is intentional or a temporary regression integrators should defensively enforce client-side.
