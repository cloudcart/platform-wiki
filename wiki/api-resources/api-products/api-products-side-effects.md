---
type: api-resource
resource_path: /api/v2/products
http_methods: [GET, POST, PATCH, DELETE]
related_entity: product
related_features: [products-products, products-inventory, products-variants-options]
aliases: ["Products API side effects", "products webhooks caveat", "products write pipeline", "products plan gating", "products 422 errors", "API продукти странични ефекти"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Products API — side effects, webhooks & plan gating

> Part of [[api-products]]. See the hub for the other aspects (attributes & relationships, filtering & sorting, examples).

## Purpose

This aspect documents **what happens after a write**: the shared POST / PATCH save pipeline, the DELETE behaviour, the critical webhook caveat (`product.created` / `product.updated` do NOT fire for API writes), the plan-feature slot caps that can reject a write, and the common 422 error shapes. For the field meanings, see [[api-products-attributes]]. For worked request / response payloads, see [[api-products-examples]].

## Endpoint

- **URL base:** `<store-host>/api/v2/products/`
- **Methods covered here:** `POST`, `PATCH /{id}`, `DELETE /{id}` — the write methods that trigger side effects.

Base URL, auth, headers, rate limits: see [[json-api-v2]].

## Attributes

The side effects below are triggered by writing the attributes documented on [[api-products-attributes]] — particularly the `parameter*` relationships (variant wipe), the boolean enum flags (default fill), and `unit_short_name` (unit resolution).

## Relationships

Changing the `parameter1` / `parameter2` / `parameter3` relationships is the highest-impact write — it can delete every child variant (see below). The `variant` relationship is recomputed by the platform after any variant save.

## Filtering & sorting

Reads have no write side effects; the allowed `filter[...]` parameters, `sort` columns, and `include` paths are documented on [[api-products-filtering]]. The query-parameter validation failures (bad sort column, bad include path, bad append value) surface as 422 — distinct from the write-time effects below.

## Side effects

Both POST and PATCH run the same save pipeline:

- **Variant-parameter validation** — `p2_id` requires `p1_id`; `p3_id` requires both `p1_id` and `p2_id`. The same parameter cannot occupy two slots. Failure returns 422 with title `Missing Parameter Relationship` or `Duplicate Parameter Relationship` and a JSON pointer to the offending `parameter*` relationship.
- **Default boolean fill** — on POST, any of `digital`, `sale`, `new`, `tracking`, `shipping`, `draft` left blank are forced to `no`.
- **Unit resolution** — when `unit_short_name` is sent AND the Grocery Store app is installed, the platform looks up the unit ID by short name; an unknown short name returns 422 `The unit short name is invalid. List of valid units: <comma-list>`.
- **Variant wipe on parameter change** — if `p1_id`, `p2_id`, or `p3_id` changes on PATCH, **all child variants are deleted** and `default_variant_id` is cleared. Integrators that change a product's parameters must re-create the variant grid afterwards.
- **Snapshot copy** — when `pN_id` changes, the parameter's `name` is copied into `pN` for fast read paths.
- **Audit / change-log** — every save records the dirty-attribute diff in the product's change log with `initiator = "api"` + `name = <request IP>` + `action = "edit"`. Visible in the merchant's product change-history view (see [[products-change-log]]).
- **Bundle reprice** — every bundle containing this product is repriced after save.
- **Discount re-eval** — any active product-level discount is re-evaluated against this product.
- **Search re-index** — the search re-index event fires, queuing the search engine / Algolia / Listing Engine re-index (storefront search reflects the change within minutes — see [[apps-listing-engine]] + [[background-queue-search-sync]]).
- **Meta merge** — when the request body contains a `meta` object, it merges into the product's meta storage.
- **`temporary` flag** — a request `meta.temporary = true` marks the row as a temporary product (used by the import-wizard preview flow).

DELETE:

- Soft-delete (`deleted_at` is set). Subsequent GETs return **404** (no `410 Gone` semantic — see [[json-api-v2]]).
- Fires the **`product.deleted` webhook** (the only product-related webhook that fires for API writes — see the table below).
- Fires the search-engine sync DELETE event.
- Bundles containing this product have their bundle link cleaned up.

**Webhooks — important caveat:**

| Webhook | Fires from API? |
|---|---|
| `product.created` | **No** — gated to `app_namespace == "sitecp"`. API POSTs do NOT trigger it. |
| `product.updated` | **No** — same `sitecp`-only gate. API PATCHes do NOT trigger it. |
| `product.deleted` | **Yes** — fires unconditionally on row delete (including API DELETE). |

Integrations needing change notification on API-driven create / update should poll the API or wire a separate observer outside the platform. See [[settings-hooks]].

## Plan-feature gating

No plan-feature gate on the resource itself (just the global JSON-API rate-limit per plan). Slot counters DO apply at write time:

- Product count limit — POSTs that would exceed the plan's product cap return **402 Payment Required**.
- Bundle count limit — bundle creates are counted separately.
- Hidden-products limit — `draft = yes` rows count against a separate cap.

See [[plan-vs-feature-pack]] for cap values per plan and [[platform-rate-limits]] for per-plan rate limits.

## Error examples (common 422 cases)

- Missing required `category` relationship on POST:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The category field is required.","source":{"pointer":"/data/relationships/category"}}]}
  ```
- Same parameter in two slots:
  ```json
  {"errors":[{"status":"422","title":"Duplicate Parameter Relationship","detail":"The parameter2 can not be the same as parameter1","source":{"pointer":"/data/relationships/parameter2"}}]}
  ```
- Unknown grocery unit short name:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The unit short name is invalid. List of valid units: kg, g, l, ml, piece","source":{"pointer":"/data/attributes/unit_short_name"}}]}
  ```

## Equivalent UI

- [[products-products]] — the admin save runs the same pipeline (parameter validation, variant wipe on parameter change, change-log entry).
- [[products-change-log]] — where the API-write audit entries (`initiator = "api"`) surface for the merchant.

## Related

- [[api-products]] — hub.
- [[json-api-v2]] — error envelope, status-code semantics, webhook side-effect principle.
- [[api-products-attributes]] — the fields whose writes trigger these effects.
- [[settings-hooks]] — `product.deleted` webhook subscription (and the created / updated gap).
- [[products-change-log]] — audit trail for API writes.
- [[apps-listing-engine]] — search re-index target.
- [[background-queue-search-sync]] — the queue that processes the re-index.
- [[plan-vs-feature-pack]] — product / bundle / hidden-product slot caps (402).
- [[platform-rate-limits]] — per-plan API rate limits.

## Open questions

- Confirm whether changing a product's variant parameters (`p1_id`/`p2_id`/`p3_id`) on PATCH is intended to wipe ALL existing variants — integrators expecting variant-preserve semantics will lose data here.
- Confirm whether the `temporary` meta flag is documented for external integrators or is reserved for the import-wizard preview flow.
- Verify whether bundle-membership effects (`product.deleted` cascading to bundle reprice) emit any dedicated event for the affected bundles.
