---
type: feature
nav_path: "Marketing → Discounts → Flat → Programmatic access"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Flat discount API", "Flat discount JSON-API v2", "Flat discount GraphQL", "Flat discount webhooks", "Flat discount side effects", "Flat discount audit log", "Flat discount attachment regeneration"]
tags: [marketing, discounts, flat, api, json-api-v2, graphql, webhooks]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, value mechanics, eligibility, stacking).

# Flat discount — programmatic access

## Purpose

This page documents **how Flat discounts can be created, updated, toggled, and deleted via API** — the JSON-API v2 REST endpoint, the GraphQL endpoint, what each validates and triggers, the webhook events that fire, and the absence of any audit-log row for the change.

Tickets that land here: *"can I bulk-create Flat discounts from my ERP"*, *"why does the storefront not show my newly-created discount immediately"*, *"is there an audit trail for who created this discount"*, *"can I create a Quantity discount via API".

## Where to find it

The two write surfaces:

- **JSON-API v2 REST endpoint** — `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]]. Resource [[api-discounts]].
- **GraphQL admin endpoint** — `Discount` resource (mutations: `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus`). Uses the admin login session or a personal access token, NOT the JSON-API v2 key.

## What the merchant can do here

- **Create** a Flat discount (no-code or code-based) — JSON-API v2 or GraphQL.
- **Update** any field on an existing Flat discount.
- **Toggle** `active` status; it takes effect immediately.
- **Delete** a Flat discount (single or bulk via GraphQL `discountsBulkDelete`).

### What the merchant CANNOT do here

- **Create a Quantity or Countdown discount via JSON-API v2** — the validator allows `discount_type ∈ {flat, percent, shipping, fixed, code-pro}` only. Quantity and Countdown are created through the admin panel or the Admin GraphQL API.
- **Get an audit-log row** capturing actor identity, source, or diff for the change — no audit log exists for discounts (see *"No audit-log row"* below).

## Settings & fields

GraphQL takes the admin form's field names. JSON-API v2 uses `discount_type` and a `target` object: `target.type` of `all`, `product`, `category`, `vendor`, `category_vendor`, `selection` or `order_over`, with `target.products`, `target.categories`, `target.vendors` or `target.selections`. It does not apply `force_save`. The field catalogue lives across:

- [[flat-discount-form-entry]] — `name`, `active`, `type`, `discount_amount_type_in_label`, `color`, `text_color`.
- [[flat-discount-targeting]] — `settings`, `order_over`, `force_save`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]`.
- [[flat-discount-value-mechanics]] — `type_value` (in cents).
- [[flat-discount-eligibility]] — `customer_groups_target`, `customer_groups[]`, `only_customer`, `customers[]`, `max_uses`, `maxused_user`, `geo_zone_id`, `all_regions`, `date_start`, `date_end`, `no_expire`.
- [[flat-discount-stacking]] — `code`, `code_format`, `barcode_prefix`, `code_apply`, `apply_regular_price`.

## Business rules

### JSON-API v2 — REST endpoint

Resource: `discounts` (see [[api-discounts]]). Full CRUD plus status toggle. Both no-code and code-based Flat variants are supported via the **same resource** — set the `code` attribute to switch between them. The base URL is `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]].

The validator allows `discount_type ∈ {flat, percent, shipping, fixed, code-pro}` on this endpoint — Quantity and Countdown discounts are **NOT** writable via JSON-API v2; they are created through the admin panel or the Admin GraphQL API.

Amounts are written in **cents** via the API — a 10 EUR flat discount is `type_value = 1000` regardless of source. See [[json-api-v2]] for authentication and rate-limit.

### GraphQL endpoint

Resource: `Discount`. Mutations:

- `createDiscount` — create a new Flat discount.
- `updateDiscount` — update any field on an existing one.
- `discountsBulkDelete` — delete one or many at once.
- `changeDiscountsStatus` — bulk active / inactive toggle.

Same field set as the admin panel; uses the admin login session or a personal access token, not the merchant-facing JSON-API v2 key.

### What each path validates and triggers

The three paths have separate validation:

- **Admin form** — name, code format and uniqueness on create, limits up to 100,000, target values.
- **JSON-API v2** — `name`, `discount_type`, `date_start` (`Y-m-d`), integer `type_value`, target type and ids, `code` (alphanumeric, max 20, unique).
- **GraphQL** — input types only.

Plan checks differ too — see [[flat-discount-eligibility]]. A save on any path rewrites the product rows of a no-code discount, refreshes smart collections and listings, and emits `discount.created` / `discount.updated` (see [[settings-hooks]]).

### Save-flow pipeline (admin OR API)

Creating / updating a Flat discount runs:

1. Validates the input, as far as that path does (see above).
2. Persists the discount row with `type = flat` and `type_value` in cents.
3. Syncs `customer_groups[]`, targets (`products[]` / `product_categories[]` / `vendors[]` / `selections[]` / region join), `customers[]`.
4. Fires `discount.created` / `discount.updated` events to [[settings-hooks]].
5. Refreshes what the storefront shows:
   - **Per-product attachment recompute** (no-code discounts) — rewritten as part of the save; updates the price-grid rendering on category and product pages for products covered by the discount.
   - **Smart-collection refresh** — recomputes "On sale" smart collections so they include / exclude the newly-discounted products.
   - **Listing engine repath** — patches the storefront listing cache with the new "was / now" pricing.

The Active switch and `changeDiscountsStatus` change only the status. They take effect immediately and trigger none of these steps.

### Order-level discount records

When an order is placed with a Flat discount, a per-order-discount row links `discount_id` + `order_id`. These rows feed:

- The `uses` recount (orders in a counted status — see [[flat-discount-eligibility]]).
- [[analytics-top-order-discounts]] (most-used order-level discounts dashboard).
- The merchant's order view (shows the applied discount as a line item).

### Webhook events

The following webhook events fire on Flat discount writes (see [[settings-hooks]]):

- `discount.created` — fires when a discount record is created.
- `discount.updated` — fires when a discount record is saved.
- `discount.deleted` — fires on `DELETE /api/v2/discounts/{id}`.

None fires on the Active switch, `changeDiscountsStatus`, the list delete, `discountsBulkDelete`, the expiry sweep or the uses recount.

Receivers must be idempotent.

### No audit-log row

There is **no audit-log row** captured for the create/update — the platform does not record actor identity, request source (admin vs API), or a diff. Merchants who need a change trail must keep their own log externally.

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-eligibility]] — plan checks per path.
- [[flat-discount-targeting]] — target values.
- [[flat-discount-value-mechanics]] — `type_value` cents storage applies to API writes too.
- [[flat-discount-stacking]] — `code_apply` + `apply_regular_price` settable via API.
- [[api-discounts]] — JSON-API v2 resource.
- [[json-api-v2]] — authentication, rate-limit.
- [[settings-api-keys]] — Site ID + API key headers.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` webhooks.
- [[analytics-top-order-discounts]] — analytics dashboard surfacing top order-level discounts.

## Open questions

None.
