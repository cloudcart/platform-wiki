---
type: feature
nav_path: "Marketing → Discounts → Percent → Programmatic access"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Percent discount API", "Percent discount GraphQL", "Percent discount JSON-API v2", "Percent discount webhooks"]
tags: [marketing, discounts, percent, api, graphql, webhooks]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, stacking, validity, plan gates).

# Percent discount — programmatic access (JSON-API v2 + GraphQL + webhooks)

## Purpose

Percent discounts can be created, updated, toggled, and deleted via two API surfaces: the JSON-API v2 `discounts` resource and the GraphQL endpoint. This page documents the available surfaces, what each validates and triggers, and what the merchant gets in the way of audit trail (currently nothing).

## Where to find it

JSON-API v2 base URL is `<store>/api/v2/discounts` — authenticated via Site ID + API key headers managed at [[settings-api-keys]]. The GraphQL endpoint takes the admin login session or a personal access token — see [[json-api-v2]] for the broader API surface. Webhooks fired (`discount.*`) are subscribed via [[settings-hooks]].

## What the merchant can do here

- Create / update / delete Percent discounts (no-code and code variants) via JSON-API v2.
- Toggle status, bulk-delete, and run the same field updates via GraphQL mutations.
- Subscribe to `discount.created` / `discount.updated` / `discount.deleted` webhooks to follow saved changes in an external system; *Webhooks fired* lists what sends none.
- Provision the same target combinations through any surface. Validation and plan checks differ by surface.

## Settings & fields

GraphQL takes nearly the same field shape as the admin form. JSON-API v2 uses `discount_type` and a `target` object (`target.type` of `all`, `product`, `category`, `vendor`, `category_vendor`, `selection` or `order_over`). Both differ from the form on **`type_value`** (see the value-convention note below the table):

| Surface | Endpoint / mutation | Writes accepted |
|---|---|---|
| JSON-API v2 | `<store>/api/v2/discounts` (GET / POST / PATCH / DELETE) | `discount_type ∈ {flat, percent, shipping, fixed, code-pro}` — Quantity + Countdown NOT writable here. |
| GraphQL | `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus` | Same field set as the admin panel. |
| Webhooks | `discount.created`, `discount.updated`, `discount.deleted` | See *Webhooks fired*. |

The admin form's validation lives on [[percent-discount-fields]]; target rules on [[percent-discount-targeting]].

> **`type_value` on the API is the RAW stored value — not the whole percent.** The admin form multiplies the percent you type by 100 **client-side** before saving (you type `15` → it stores `1500`). The API does **not** do this: `createDiscount` / JSON-API v2 persist `type_value` exactly as sent. So to create a **15%** discount programmatically you must send **`type_value: 1500`** (percent × 100) — sending `15` produces a **0.15%** discount. (Verified: a `createDiscount` call with `type_value: 15` stored `15`, which the admin form then renders as `0.15 %`; real 15% discounts on a store are stored as `1500`.) Money-based types store their own integer form too (e.g. Flat in cents — see [[flat-discount-value-mechanics]]); send the stored value, not the display value.

> **Passing the discount target on GraphQL.** Set `settings` to the target-type enum value **plus** the matching companion array: `all` / `order_over` (no array), `product` → `products: [ids]`, `product_category` → `product_categories: [ids]`, `product_vendor` → `vendors: [ids]`, **`selection` → `selections: [smartCollectionIds]`**, `category_vendor` → `product_categories` + `vendors`. **The target-type value is singular** — use **`settings: "selection"`** (not `"selections"`) for a smart-collection; sending the plural creates the discount with **no target at all** (verified: `settings:"selections"` produced `targets:[]`, while `settings:"selection"` produced `targets:[{selection, id}]`). The smart-collection ids are the ones from `createSmartCollection` / `smartCollections`.

> **`date_start` on GraphQL — always send it, in full `Y-m-d H:i:s` form.** The admin form **requires** a start date; via GraphQL, **always send `date_start`** (default it to **today** unless a later start is wanted) so the discount is valid and its activity gate (`date_start <= today`) passes — see [[percent-discount-validity]]. Format matters: the `DateTime` scalar rejects a **bare date** (`"2026-07-17"` → *"Not enough data available to satisfy format"*); send the full datetime, e.g. **`"2026-07-17 00:00:00"`**. (Note: `createDiscount` does **not** hard-reject a create with no `date_start`, but the resulting discount is missing its required start — don't rely on that.)

## JSON-API v2 — REST endpoint

Resource: `discounts` (see [[api-discounts]]). Full CRUD plus status toggle. Both no-code and code-based Percent variants are supported via the same resource — set the `code` attribute to switch between them. The base URL is `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]].

The validator allows `discount_type ∈ {flat, percent, shipping, fixed, code-pro}` on this endpoint — Quantity and Countdown discounts are **NOT** writable via JSON-API v2; they are created through the admin panel or the Admin GraphQL API.

## GraphQL endpoint

Resource: `Discount` with mutations `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus`. Same field set as the admin panel; uses the admin login session or a personal access token.

## What each path validates and triggers

The three paths have separate validation:

- **Admin form** — name, code format and uniqueness on create, percent above 0 and up to 100, limits up to 100,000, target values. See [[percent-discount-fields]].
- **JSON-API v2** — `name`, `discount_type`, `date_start` (`Y-m-d`), integer `type_value`, target type and ids, `code` (alphanumeric, max 20, unique). It does not limit a percent to 100.
- **GraphQL** — input types only. It does not limit a percent to 100.

Plan checks differ too — see [[percent-discount-plan-gates]]. A save on any path rewrites the product rows of a no-code discount, refreshes smart collections and listings, and emits `discount.created` / `discount.updated` (see [[settings-hooks]]).

See [[json-api-v2]] for authentication and rate-limit.

## No audit-log row captured

There is **no audit-log row** captured for the create / update — the platform does not record actor identity, request source (admin vs API), or a diff between revisions. Merchants who need a change trail must keep their own log externally.

## Webhooks fired

| Webhook event | When it fires |
|---|---|
| `discount.created` | When a discount record is created. |
| `discount.updated` | When a discount record is saved. |
| `discount.deleted` | On `DELETE /api/v2/discounts/{id}`. |

None fires on the Active switch, `changeDiscountsStatus`, the list delete, `discountsBulkDelete`, the expiry sweep or the uses recount.

Receivers must be idempotent — see [[settings-hooks]].

## Save flow (admin + API + GraphQL)

Creating / updating a Percent discount runs:

1. Validates the input, as far as that path does (see above).
2. Persists the discount row with `type = percent` and `type_value` **exactly as sent** (the stored form is percent × 100 = `1500` for 15% — the API does **not** convert; the admin form's ×100 is client-side only, see the value-convention note above).
3. Syncs `customer_groups[]`, targets (products / categories / vendors / selections / regions), customers.
4. Fires `discount.created` / `discount.updated` events to [[settings-hooks]].
5. Refreshes what the storefront shows:
   - **Per-product attachment recompute** (no-code discounts) — rewritten as part of the save; updates the price-grid rendering on category and product pages for products covered by the discount.
   - **Smart-collection refresh** — recomputes "On sale" smart collections so they include / exclude the newly-discounted products.
   - **Listing engine repath** — patches the storefront listing cache with the new "was / now" pricing.

The Active switch and `changeDiscountsStatus` change only the status. They take effect immediately and trigger none of these steps.

## Order-level discount records

When an order is placed with a Percent discount, a per-order-discount row links `discount_id` + `order_id`. These rows feed:

- The `uses` recount (orders in a counted status — see [[percent-discount-validity]]).
- [[analytics-top-order-discounts]] (most-used order-level discounts dashboard).
- The merchant's order view (shows the applied discount as a line item).

## Business rules

- Validation differs between the admin form and the APIs, and there is **no audit log**. Integrations should mirror their writes to their own log if attribution matters.
- Quantity and Countdown are NOT writable via JSON-API v2; they are created in the admin panel or through the Admin GraphQL API. Percent has no such limitation — both no-code and code-based Percent variants are JSON-API v2 writable.

## Related

- [[marketing-discounts-percent]] — hub.
- [[api-discounts]] — the JSON-API v2 resource page.
- [[json-api-v2]] — authentication, rate-limit.
- [[settings-api-keys]] — Site ID + API key authentication.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` webhooks.
- [[percent-discount-fields]] — the admin form's validation rules.
- [[percent-discount-targeting]] — target values.
- [[percent-discount-plan-gates]] — plan checks per path.
- [[percent-discount-validity]] — date window and uses counter.
- [[analytics-top-order-discounts]] — uses-counter dashboard.

## Open questions

- The list query's `targets` field returns `[]` for every discount (it does not eager-load targets); read a discount's targets from the `createDiscount` / `updateDiscount` response (which reloads them) rather than the list. `(verify — whether a single-discount read exposes targets.)`
