---
type: feature
nav_path: "Marketing → Discounts → Shipping → Plan gates & API"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Free shipping plan gates", "Shipping discount API", "Shipping discount webhooks", "discount_global", "discount_coupon"]
tags: [marketing, discounts, shipping, plan-gates, api, webhooks]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, stacking, force-save, other zero-paths, examples).

# Shipping discount — plan gates, API, webhooks

## Purpose

This page collects the **non-form mechanics** of the Free-shipping discount: the plan check on create, the usage counters (`discount_global` for no-code, `discount_coupon` for code-based), the JSON-API v2 + GraphQL write paths, and the webhook events.

## Where to find it

The plan check runs on the create endpoint (`POST /admin/api/core/discounts`). The `active` switch is on each row of the [[marketing-discounts]] list and on the edit form. See [[marketing-discounts-shipping]] for the form entry-surface.

## What the merchant can do here

- Create / update / delete a shipping discount via JSON-API v2 (`<store>/api/v2/discounts`, see [[api-discounts]]).
- Create / update via GraphQL (`createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus` mutations).
- Subscribe to the `discount.created` / `discount.updated` / `discount.deleted` webhooks via [[settings-hooks]].
- Switch `active` at any time; it takes effect immediately.
- (Cannot) audit who-changed-what — there is no audit-log row for discount writes.

## Settings & fields

Plan-feature usage counters (read-only from the merchant's perspective):

| Mapping | Shape | What it counts |
|---|---|---|
| `discount_global` | Numeric | No-code Flat, Percent and Free-shipping discounts, Countdown included — see [[plan-gates]] for the codeless-vs-coupon split. |
| `discount_coupon` | Numeric | Discounts holding their own code, so code-based Free shipping. |

Usage counts discounts whether active or not; only deleting lowers it. Both counters extend via packs ([[plan-vs-feature-pack]]). `total_discounts` is a displayed figure, not enforced.

No card in the type-picker modal greys out for free shipping; only the Code PRO card is gated.

## Business rules

### The plan check on create

Each path checks differently, and only on create:

- **Admin form:** checks whether that kind of discount is enabled on the plan (`discount-<type>`). If not: HTTP 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* There is no numeric limit on this path.
- **JSON-API v2:** compares usage with `discount_global` or `discount_coupon`. Over the quota it returns HTTP 402 Payment Required.
- **GraphQL `createDiscount`:** only Fixed and Quantity quotas are checked, so free shipping is not. Updates are not checked.

### Webhook events

Saving a discount record fires the same platform-wide [[settings-hooks]] events as the rest of the discount engine:

| Event | When | Payload |
|-------|------|---------|
| `discount.created` | A shipping discount is created through the form, JSON-API v2 or GraphQL. | The Discount record. |
| `discount.updated` | A shipping discount is edited and saved through the form, JSON-API v2 or GraphQL. | The updated Discount. |
| `discount.deleted` | A shipping discount is deleted through JSON-API v2. | The deleted Discount's last state. |

The `active` switch in the list, bulk status, list delete, `changeDiscountsStatus`, `discountsBulkDelete`, the expiry sweep and the uses recount send none.

### JSON-API v2 — REST endpoint

Resource: `discounts` (see [[api-discounts]]). Full CRUD plus status toggle. Both no-code (always-on / `order_over` free shipping) and code-based variants are supported via the same resource — set the `code` attribute to switch between them. The base URL is `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]].

The validator allows `discount_type ∈ {flat, percent, shipping, fixed, code-pro}` on this endpoint — Quantity and Countdown discounts cannot be created through JSON-API v2.

### GraphQL

Resource: `Discount` (mutations: `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus`). Same field set as the admin panel; authenticates with an admin session token or a personal access token.

### Each path validates separately

The admin form, JSON-API v2 and GraphQL have separate validation:

- **Admin form:** a value on a free-shipping discount is refused with *"Type value must be empty"*, and the `force_save` field has to be sent, on or off.
- **JSON-API v2 and GraphQL:** neither runs the admin form's checks. JSON-API v2 does not store the **Save the discount on your order** setting.

### No audit-log row for discount writes

There is **no audit-log row** captured for the create / update — the platform does not record actor identity, request source (admin vs API), or a diff.

For support tickets that ask "who created this discount" or "when did this discount change", the only signals available are:

- The `created` / `updated` timestamps on the Discount record itself.
- Webhook delivery logs (if the merchant captures them on their side).
- Indirect: orders that consumed the discount have a timestamp.

There is no in-product audit screen for discount history.

### Cart-engine selection rules apply identically

Only ONE shipping discount applies per cart at totals time — the first that qualifies in the no-code shipping pool (no threshold sort; a discount that does not qualify no longer ends the search). For predictable behaviour, the merchant should avoid overlapping no-code Free-shipping discounts. See [[shipping-discount-stacking]] for the full selection rules.

### Permissions

The form and CRUD endpoints are scoped under the standard `marketing.discounts` permission.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[api-discounts]] — JSON-API v2 resource for discount CRUD.
- [[settings-hooks]] — `discount.created` / `updated` / `deleted` webhook events.
- [[settings-api-keys]] — Site ID + API key auth for JSON-API v2.
- [[plan-gates]] — codeless-vs-coupon split + plan-gate model.
- [[plan-features]] — per-feature upsell screen.
- [[plan-vs-feature-pack]] — extending quotas via packs.
- [[discount-stacking]] — cross-discount stacking.

## Open questions

None.
