---
type: feature
nav_path: "Marketing → Discounts → Flat → Programmatic access"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Flat discount API", "Flat discount JSON-API v2", "Flat discount GraphQL", "Flat discount webhooks", "Flat discount side effects", "Flat discount audit log", "Flat discount attachment regeneration"]
tags: [marketing, discounts, flat, api, json-api-v2, graphql, webhooks]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, value mechanics, eligibility, stacking).

# Flat discount — programmatic access

## Purpose

This page documents **how Flat discounts can be created, updated, toggled, and deleted via API** — the JSON-API v2 REST endpoint, the admin-session GraphQL endpoint, the shared side-effects pipeline they trigger, the webhook events that fire, and the absence of any audit-log row for the change.

Tickets that land here: *"can I bulk-create Flat discounts from my ERP"*, *"why does the storefront not show my newly-created discount immediately"*, *"is there an audit trail for who created this discount"*, *"can I create a Quantity discount via API".

## Where to find it

The two write surfaces:

- **JSON-API v2 REST endpoint** — `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]]. Resource [[api-discounts]].
- **GraphQL admin endpoint** — `Discount` resource (mutations: `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus`). Uses the admin-session login cookie, NOT the JSON-API v2 key.

## What the merchant can do here

- **Create** a Flat discount (no-code or code-based) — JSON-API v2 or GraphQL.
- **Update** any field on an existing Flat discount.
- **Toggle** `active` status (subject to the 10-minute cooldown — see [[flat-discount-eligibility]]).
- **Delete** a Flat discount (single or bulk via GraphQL `discountsBulkDelete`).

### What the merchant CANNOT do here

- **Create a Quantity or Countdown discount via JSON-API v2** — the validator allows `type ∈ {flat, percent, shipping, fixed, code-pro}` only. Quantity and Countdown must be created through the admin panel.
- **Get an audit-log row** capturing actor identity, source, or diff for the change — no audit log exists for discounts (see *"No audit-log row"* below).

## Settings & fields

API writes use the **same field names** as the admin form. The full field catalogue lives across:

- [[flat-discount-form-entry]] — `name`, `active`, `type`, `discount_amount_type_in_label`, `color`, `text_color`.
- [[flat-discount-targeting]] — `settings`, `order_over`, `force_save`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]`.
- [[flat-discount-value-mechanics]] — `type_value` (in cents).
- [[flat-discount-eligibility]] — `customer_groups_target`, `customer_groups[]`, `only_customer`, `customers[]`, `max_uses`, `maxused_user`, `geo_zone_id`, `all_regions`, `date_start`, `date_end`, `no_expire`.
- [[flat-discount-stacking]] — `code`, `code_format`, `barcode_prefix`, `code_apply`, `apply_regular_price`.

## Business rules

### JSON-API v2 — REST endpoint

Resource: `discounts` (see [[api-discounts]]). Full CRUD plus status toggle. Both no-code (cart-wide) and code-based Flat variants are supported via the **same resource** — set the `code` attribute to switch between them. The base URL is `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]].

The validator allows `type ∈ {flat, percent, shipping, fixed, code-pro}` on this endpoint — Quantity and Countdown discounts are **NOT** writable via JSON-API v2; they must be created through the admin panel.

Amounts are written in **cents** via the API — a 10 EUR flat discount is `type_value = 1000` regardless of source. See [[json-api-v2]] for authentication, rate-limit, and the same-side-effects principle.

### GraphQL — admin admin-session endpoint

Resource: `Discount`. Mutations:

- `createDiscount` — create a new Flat discount.
- `updateDiscount` — update any field on an existing one.
- `discountsBulkDelete` — delete one or many at once.
- `changeDiscountsStatus` — bulk active / inactive toggle.

Same field set as the admin panel; uses admin-session authentication (the same login cookie as the admin panel), not the merchant-facing JSON-API v2 key.

### Same side effects regardless of source

A create / update through JSON-API v2 or GraphQL triggers the **same pipeline** as the admin-panel save:

- All validation rules apply (target enum, parent-child category rejection, 10,000-combinations cap, code uniqueness, `type_value` and `order_over` character-length validation).
- Plan-feature usage counters consume (`discount_global` for no-code, `discount_coupon` for code-based) — overflow returns **HTTP 403 Forbidden** with the *"Not supported by plan"* message. See [[flat-discount-eligibility]].
- Per-product attachment regeneration runs (rebuilds the storefront's *"from X / now Y"* pricing display).
- Smart-collection refresh fires.
- The `discount.created` / `discount.updated` webhooks emit (see [[settings-hooks]]).
- The 10-minute activation cooldown applies on subsequent status-toggle attempts (no-code Flat only — see [[flat-discount-eligibility]]).

### Save-flow pipeline (admin OR API)

Creating / updating a Flat discount runs:

1. Validates name, code (if code-based), `max_uses`, `maxused_user`, `type`, `type_value`, `settings`, target arrays, date range.
2. Persists the discount row with `type = flat` and `type_value` in cents.
3. Syncs `customer_groups[]`, targets (`products[]` / `product_categories[]` / `vendors[]` / `selections[]` / region join), `customers[]`.
4. Fires `discount.created` / `discount.updated` events to [[settings-hooks]].
5. Schedules background regeneration:
   - **Per-product attachment recompute** — updates the price-grid rendering on category and product pages for products covered by the discount.
   - **Smart-collection refresh** — recomputes "On sale" smart collections so they include / exclude the newly-discounted products.
   - **Listing engine repath** — patches the storefront listing cache with the new "was / now" pricing.

These are **async**; the merchant sees a *"Latest update: :date"* badge on the discount until the jobs complete. For high-catalog stores (10,000+ products) regeneration can take minutes — hence the 10-minute activation cooldown.

### Order-level discount records

When an order is placed with a Flat discount, a per-order-discount row links `discount_id` + `order_id`. These rows feed:

- The `uses` counter sync (incremented when the order reaches a counted status — see [[flat-discount-eligibility]]).
- [[analytics-top-order-discounts]] (most-used order-level discounts dashboard).
- The merchant's order view (shows the applied discount as a line item).

### Webhook events

The following webhook events fire on Flat discount writes (see [[settings-hooks]]):

- `discount.created` — fires on every successful create (admin, JSON-API v2, GraphQL).
- `discount.updated` — fires on every successful update, including the auto-disable UTC sweep and every active-status toggle.
- `discount.deleted` — fires on row delete.

Receivers must be idempotent — bulk updates can fire many `discount.updated` events in close succession.

### No audit-log row

There is **no audit-log row** captured for the create/update — the platform does not record actor identity, request source (admin vs API), or a diff. Merchants who need a change trail must keep their own log externally.

(Note: older wiki phrasing claimed an `api2` source tag in the audit log — that phrasing was incorrect; no audit log exists for discounts.)

## Related

- [[marketing-discounts-flat]] — hub.
- [[flat-discount-eligibility]] — plan-feature quotas + activation cooldown also enforced on API writes.
- [[flat-discount-targeting]] — validation rules (target enum, parent-child rejection) also enforced on API writes.
- [[flat-discount-value-mechanics]] — `type_value` cents storage applies to API writes too.
- [[flat-discount-stacking]] — `code_apply` + `apply_regular_price` settable via API.
- [[api-discounts]] — JSON-API v2 resource.
- [[json-api-v2]] — authentication, rate-limit, same-side-effects principle.
- [[settings-api-keys]] — Site ID + API key headers.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` webhooks.
- [[analytics-top-order-discounts]] — analytics dashboard surfacing top order-level discounts.

## Open questions

None.
