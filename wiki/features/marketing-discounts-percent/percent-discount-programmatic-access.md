---
type: feature
nav_path: "Marketing → Discounts → Percent → Programmatic access"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount API", "Percent discount GraphQL", "Percent discount JSON-API v2", "Percent discount webhooks"]
tags: [marketing, discounts, percent, api, graphql, webhooks]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, stacking, validity, plan gates).

# Percent discount — programmatic access (JSON-API v2 + GraphQL + webhooks)

## Purpose

Percent discounts can be created, updated, toggled, and deleted via two API surfaces: the JSON-API v2 `discounts` resource and the GraphQL admin-session endpoint. This page documents the available surfaces, what writes trigger the **same side effects** as an admin-panel save, and what the merchant gets in the way of audit trail (currently nothing).

## Where to find it

JSON-API v2 base URL is `<store>/api/v2/discounts` — authenticated via Site ID + API key headers managed at [[settings-api-keys]]. The GraphQL admin-session endpoint is the same one driving the admin SPA — see [[json-api-v2]] for the broader API surface. Webhooks fired (`discount.*`) are subscribed via [[settings-hooks]].

## What the merchant can do here

- Create / update / delete Percent discounts (no-code and code variants) via JSON-API v2.
- Toggle status, bulk-delete, and run the same field updates via GraphQL admin-session mutations.
- Subscribe to `discount.created` / `discount.updated` / `discount.deleted` webhooks to mirror admin + API + GraphQL changes into an external system.
- Provision the same target combinations through any surface — same validation, same plan-gate enforcement.

## Settings & fields

The API surfaces accept nearly the same field shape as the admin form — with **one important difference: `type_value`** (see the value-convention note below the table):

| Surface | Endpoint / mutation | Writes accepted |
|---|---|---|
| JSON-API v2 | `<store>/api/v2/discounts` (GET / POST / PATCH / DELETE) | `type ∈ {flat, percent, shipping, fixed, code-pro}` — Quantity + Countdown NOT writable here. |
| GraphQL admin-session | `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus` | Same field set as the admin panel. |
| Webhooks | `discount.created`, `discount.updated`, `discount.deleted` | Fire on any successful create / update / delete regardless of source. |

Full field validation lives on [[percent-discount-fields]]; target rules on [[percent-discount-targeting]].

> **`type_value` on the API is the RAW stored value — not the whole percent.** The admin form multiplies the percent you type by 100 **client-side** before saving (you type `15` → it stores `1500`). The API does **not** do this: `createDiscount` / JSON-API v2 persist `type_value` exactly as sent. So to create a **15%** discount programmatically you must send **`type_value: 1500`** (percent × 100) — sending `15` produces a **0.15%** discount. (Verified: a `createDiscount` call with `type_value: 15` stored `15`, which the admin form then renders as `0.15 %`; real 15% discounts on a store are stored as `1500`.) Money-based types store their own integer form too (e.g. Flat in cents — see [[flat-discount-value-mechanics]]); send the stored value, not the display value.

> **Passing the discount target.** Set `settings` to the target-type enum value **plus** the matching companion array: `all` / `order_over` (no array), `product` → `products: [ids]`, `product_category` → `product_categories: [ids]`, `product_vendor` → `vendors: [ids]`, **`selection` → `selections: [smartCollectionIds]`**, `category_vendor` → `product_categories` + `vendors`. **The target-type value is singular** — use **`settings: "selection"`** (not `"selections"`) for a smart-collection; sending the plural creates the discount with **no target at all** (verified: `settings:"selections"` produced `targets:[]`, while `settings:"selection"` produced `targets:[{selection, id}]`). The smart-collection ids are the ones from `createSmartCollection` / `smartCollections` (the `selection` target morphs to the ProductSelection / smart-collection model).
>
> **Admin-form display caveat.** A smart-collection-targeted discount created this way stores the target correctly (and applies on the storefront), but the **admin discount form currently shows the target dropdown as empty** for it — the form's target composable reads/writes `"selections"` (plural) while the dropdown, picker, and backend use `"selection"` (singular). This is a UI plural/singular mismatch in the form, independent of the API payload. `(verify — whether the admin form has since been fixed.)`

> **`date_start` — always send it, in full `Y-m-d H:i:s` form.** The admin form **requires** a start date; via the API, **always send `date_start`** (default it to **today** unless a later start is wanted) so the discount is valid and its activity gate (`date_start <= today`) passes — see [[percent-discount-validity]]. Format matters: the `DateTime` scalar rejects a **bare date** (`"2026-07-17"` → *"Not enough data available to satisfy format"*); send the full datetime, e.g. **`"2026-07-17 00:00:00"`**. (Note: `createDiscount` does **not** hard-reject a create with no `date_start`, but the resulting discount is missing its required start — don't rely on that.)

## JSON-API v2 — REST endpoint

Resource: `discounts` (see [[api-discounts]]). Full CRUD plus status toggle. Both no-code (cart-wide) and code-based Percent variants are supported via the same resource — set the `code` attribute to switch between them. The base URL is `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]].

The validator allows `type ∈ {flat, percent, shipping, fixed, code-pro}` on this endpoint — Quantity and Countdown discounts are **NOT** writable via JSON-API v2; they must be created through the admin panel.

## GraphQL — admin admin-session endpoint

Resource: `Discount` with mutations `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus`. Same field set as the admin panel; uses admin-session authentication.

## Same side effects regardless of source

A create / update through JSON-API v2 or GraphQL triggers the **same pipeline** as the admin-panel save:

- All validation rules apply (target enum, percent ≤ 100, parent-child category rejection, 10,000-combinations cap, code uniqueness) — see [[percent-discount-fields]] + [[percent-discount-targeting]].
- Plan-feature usage counters consume (`discount_global` for no-code, `discount_coupon` for code-based) — overflow returns **HTTP 403 Forbidden** with *"Not supported by plan"*. See [[percent-discount-plan-gates]].
- Per-product attachment regeneration runs (rebuilds the storefront's *"from X / now Y"* pricing display).
- Smart-collection refresh fires for any selection-target.
- The `discount.created` / `discount.updated` webhooks emit (see [[settings-hooks]]).
- The 10-minute activation cooldown applies on subsequent status-toggle attempts (no-code Percent only) — see [[percent-discount-validity]].

The same target combinations apply: `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor` — with the same cross-validation rules (parent + child categories rejected; products incompatible with order_over). See [[json-api-v2]] for authentication, rate-limit, and the same-side-effects principle.

## No audit-log row captured

There is **no audit-log row** captured for the create / update — the platform does not record actor identity, request source (admin vs API), or a diff between revisions. Merchants who need a change trail must keep their own log externally. `(verify)` — confirm against the current audit-log scope.

## Webhooks fired

| Webhook event | When it fires |
|---|---|
| `discount.created` | On successful create through any surface (admin / JSON-API v2 / GraphQL). |
| `discount.updated` | On successful field update OR active-toggle through any surface. |
| `discount.deleted` | On successful delete (admin trash icon or `DELETE /api/v2/discounts/{id}` or GraphQL `discountsBulkDelete`). |

Receivers must be idempotent — see [[settings-hooks]].

## Save flow (admin + API + GraphQL — identical pipeline)

Creating / updating a Percent discount runs:

1. Validates name, code (if code-based), max_uses, maxused_user, type, type_value (must be > 0 and ≤ 100), settings, target arrays, date range — see [[percent-discount-fields]].
2. Persists the discount row with `type = percent` and `type_value` **exactly as sent** (the stored form is percent × 100 = `1500` for 15% — the API does **not** convert; the admin form's ×100 is client-side only, see the value-convention note above).
3. Syncs `customer_groups[]`, targets (products / categories / vendors / selections / regions), customers.
4. Fires `discount.created` / `discount.updated` events to [[settings-hooks]].
5. Schedules background regeneration:
   - **Per-product attachment recompute** — updates the price-grid rendering on category and product pages for products covered by the discount.
   - **Smart-collection refresh** — recomputes "On sale" smart collections so they include / exclude the newly-discounted products.
   - **Listing engine repath** — patches the storefront listing cache with the new "was / now" pricing.

These are async; the merchant sees a *"Latest update: :date"* badge on the discount until the jobs complete. For high-catalog stores (10,000+ products) regeneration can take minutes — hence the 10-minute activation cooldown documented in [[percent-discount-validity]].

## Order-level discount records

When an order is placed with a Percent discount, a per-order-discount row links `discount_id` + `order_id`. These rows feed:

- The `uses` counter sync (incremented when the order reaches a counted status — see [[percent-discount-validity]]).
- [[analytics-top-order-discounts]] (most-used order-level discounts dashboard).
- The merchant's order view (shows the applied discount as a line item).

## Business rules

- A merchant relying on JSON-API v2 to mirror admin discount edits gets **bit-for-bit equivalent** validation, side effects, and webhooks — but **no audit log**. Integrations should mirror their writes to their own log if attribution matters.
- Quantity and Countdown are NOT writable via JSON-API v2; they must be created in the admin panel. Percent has no such limitation — both no-code and code-based Percent variants are JSON-API v2 writable.

## Related

- [[marketing-discounts-percent]] — hub.
- [[api-discounts]] — the JSON-API v2 resource page.
- [[json-api-v2]] — authentication, rate-limit, and the same-side-effects principle.
- [[settings-api-keys]] — Site ID + API key authentication.
- [[settings-hooks]] — `discount.created` / `discount.updated` / `discount.deleted` webhooks.
- [[percent-discount-fields]] — validation rules that apply on every write.
- [[percent-discount-targeting]] — target-array cross-validation.
- [[percent-discount-plan-gates]] — HTTP 403 on quota overflow.
- [[percent-discount-validity]] — 10-minute activation cooldown on status-toggle.
- [[analytics-top-order-discounts]] — uses-counter dashboard.

## Open questions

- Confirm the absence of audit-log rows for Percent CRUD — `(verify)` against the current audit-log capture scope.
- Smart-collection targeting via `createDiscount` is **resolved** (see the target note under Settings & fields): `settings: "selection"` (singular) + `selections: [ids]` binds the target; the plural does not. The remaining `(verify)` is only whether the admin form's plural/singular display mismatch has been fixed.
- The list query's `targets` field returns `[]` for every discount (it does not eager-load targets); read a discount's targets from the `createDiscount` / `updateDiscount` response (which reloads them) rather than the list. `(verify — whether a single-discount read exposes targets.)`
