---
type: concept
nav_path: "Concept → JSON-API v2 → Filtering, sorting, sparse fields, includes"
aliases: ["JSON-API v2 filtering", "JSON-API v2 sorting", "JSON-API v2 sparse fieldsets", "JSON-API v2 includes", "filter[]", "fields[]", "sort=", "include=", "?append[]", "Sideloading"]
tags: [api, json-api, filtering, sorting, includes, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, endpoints, status codes, webhooks, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Filtering, sorting, sparse fieldsets, includes

## Definition

JSON-API v2 exposes four query-string conventions for reading collections: `filter[<field>]=<value>` (filters), `sort=<field>` or `sort=-<field>` (sorts), `fields[<type>]=<field1>,<field2>` (sparse fieldsets), and `include=<rel1>,<rel2>.<nested>` (sideloading). On top of the spec, the platform adds a custom `append[<type>]=<accessor>` parameter to materialise specific computed-accessor values (e.g. `meta`, `discount`) that are otherwise omitted from the response.

**Critical limitation:** there is **NO generic comparison-operator syntax** (`>=`, `<`, `in`, `like`) — filtering is keyed only by field name and value-equality unless the resource exposes a **named filter** that does its own comparison internally (e.g., `orders` exposes `filter[start_date]`, which is internally interpreted as "orders added on or after this date").

## Scope

- `filter[]` syntax, auto-merged column allow-list, and per-resource named filters.
- `sort` syntax, multi-sort comma syntax, and per-resource sort allow-lists.
- `fields[]` sparse fieldsets — silently omits unknown fields, no per-resource allow-list.
- `include=` sideloading — auto-merged with relationship declarations; nested includes via dot-notation; deduplicated in the top-level `included` array.
- Custom `append[]` — per-resource allow-list for extra computed accessors.

Not covered:

- Pagination of the filtered/sorted result — see [[json-api-pagination]].
- Per-resource attribute schemas — see the resource page under `wiki/api-resources/`.
- Filter validation failures (422 responses) — see [[json-api-status-codes]].

## Contrasts

- **Equality filters vs comparison operators** — every column is an equality filter by default. Comparisons (`>=`, `<=`, `LIKE`) only exist where a resource explicitly declares a named filter that internalises the operator (e.g., `orders.filter[start_date]`).
- **Sparse fieldsets vs `append[]`** — `fields[]` REMOVES attributes from the response; `append[]` ADDS extra accessors (`products.meta`, `variants.discount`) that are otherwise omitted to save bandwidth.
- **`include=` vs the relationship endpoint** — `?include=variants` returns the parent record with `included[]` sideloaded inline. `GET /products/{id}/variants` returns the related records as their own resource collection. Both are valid; sideloading saves a round-trip.
- **Auto-merged vs explicit allow-list** — for `filter[]`, the framework auto-merges every column on the underlying table into the allowed list. For `include=`, it auto-merges every declared relationship. For `sort`, it does NOT auto-merge — each resource declares its sort allow-list explicitly, and unknown sort keys return **422**.

## Filtering

- **Syntax:** `filter[<field>]=<value>`.
- **Every column on the underlying resource table is a valid filter key by default** (the framework auto-merges the resource model's table columns into the allowed-filters list). On top of that, each resource can declare **additional filters** (computed scopes, joins) that don't map to a raw column.
- **Multi-value support** is per-resource — some accept comma-separated, some accept array syntax `filter[id][]=1&filter[id][]=2`.
- **No generic comparison operators.** Comparisons live only inside named filters.

Examples of resource-specific named filters:

- `products`: `filter[sku]`, `filter[barcode]`, `filter[property_id]`, `filter[property_option_id]`, `filter[url_handle]` (triggers single-record mode).
- `orders`: `filter[start_date]`, `filter[end_date]`, `filter[geo_zone_id]`, `filter[geo_zone_name]`.
- `customers`: `filter[email]` (triggers single-record mode; validates as email).
- `subscribers`: `filter[segment]` (joins segments table).
- `variants`: `filter[has_images]`.
- `discount-codes-pro`: `filter[discount_id]`.
- `payment-providers`: `filter[active]`.

Each resource's wiki page (`wiki/api-resources/api-<name>.md`) lists its full allowed filters in the *"Allowed filtering parameters"* section.

## Sorting

- **Syntax:** `sort=field` (ascending) or `sort=-field` (descending). Comma-separated for multi-sort: `sort=-date_added,id`.
- **Per-resource allow-list** — sorting on a column not in the allow-list returns **422 Unprocessable Entity**.

Examples of allowed sorts:

| Resource | Allowed sort keys |
|---|---|
| `products` | `id`, `name`, `date_added`, `date_modified`, `sort_order`, `views` |
| `orders` | `id`, `date_added`, `updated_at`, `date_archived` |
| `customers` | `id`, `first_name`, `last_name`, `email`, `date_added`, `updated_at`, `date_banned` |
| `discounts` | `id`, `date_start`, `date_end`, `created_at`, `updated_at` |
| `subscribers` | `id`, `first_name`, `last_name`, `country` |
| `variants` | `id`, `quantity`, `price`, `weight` |
| `discount-codes-pro` | `id`, `name`, `code`, `active`, `date_start`, `date_end`, `uses`, `created_at`, `updated_at` |
| `categories` | `id`, `name`, `created_at`, `updated_at`, `order` |
| `webhooks` | `id`, `url`, `event` |

Resources without a declared sort allow-list (e.g., `shipping-providers`, `payment-providers`, `authors`, `segments`, `tags`) use natural ordering (insertion order, typically by `id` ASC).

## Sparse fieldsets

- **Syntax:** `fields[<resource-type>]=field1,field2`.
- Standard JSON:API behaviour — limits the attributes returned in the `data.attributes` block to the listed fields.
- The library does NOT enforce a per-resource allow-list; it silently omits fields the resource doesn't actually have.

### Custom extension — `?append[<resource-type>]=<accessor>`

Materialises extra computed-accessor values that are otherwise omitted (to save bandwidth). Validated by an allow-list per resource:

| Resource | Allowed `append` values |
|---|---|
| `products` | `meta`, `discount` |
| `variants` | `discount` |
| `orders` | `meta` |
| All other resources | (none — request returns 422) |

## Including relationships (sideloading)

- **Syntax:** `include=relation1,relation2.nested` (dot-notation for nested includes).
- The allowed-include list is **auto-merged with every relationship declared in the resource's schema** — so the per-resource wiki page lists ONLY the additional nested paths that are explicitly allowed beyond the top-level relationships.
- **No depth limit** beyond what each resource's allow-list lists; nested paths must be declared explicitly.
- Included resources appear in the top-level `included` array (deduplicated by `type` + `id`).

Examples of allowed includes:

| Resource | Allowed include paths |
|---|---|
| `products` | All schema relationships (`variants`, `variant`, `images`, `image`, `category`, `categories`, `vendor`, `parameter1`, `parameter2`, `parameter3`, `property-options`, `linked-products`, `product-to-discount`) + nested: `variant.images`, `variants.images`, `property-options.property` |
| `orders` | `products`, `payment`, `discounts`, `modifications`, `totals`, `taxes`, `shipping.provider`, `shipping-address`, `billing-address` |
| `customers` | `group`, `orders`, `shipping-address`, `shipping-addresses`, `billing-address`, `billing-addresses` |
| `subscribers` | `channels`, `tags` |
| `categories` | `parent`, `properties`, `properties.options` |
| `posts` | `blog`, `author`, `tags` |
| `payment-providers`, `shipping-providers`, `authors` | (none — empty allow-list) |

## Where it applies

- Every collection-read endpoint (`GET /api/v2/<resource>`) — filters, sorts, sparse fields, and includes are all parsed at the query layer.
- Single-record reads (`GET /api/v2/<resource>/{id}`) support `include=`, `fields[]`, and `append[]` — but not `filter[]` / `sort` (a single record has no collection to filter or sort).
- POST and PATCH bodies do NOT honour these query-string conventions; their semantics are governed by the JSON:API envelope — see [[json-api-headers-envelope]].

## Related

- [[json-api-v2]] — hub.
- [[json-api-pagination]] — pagination is applied AFTER filter + sort.
- [[json-api-endpoints]] — per-resource pages list their full allowed filters / sorts / includes.
- [[json-api-status-codes]] — 422 returned on disallowed sort key or filter validation failure.

## Open Questions

- **Generic comparison operators** — the API has no native `filter[price][gte]=100` syntax. Each resource that needs range filters declares them explicitly (e.g., `orders.filter[start_date]`). A future generic operator framework would unify these per-resource carve-outs `(verify roadmap)`.
- **`fields[]` allow-list** — the library silently omits unknown fields without warning. Strict mode (returning 422 on unknown field) would catch integrator typos earlier `(verify)`.
