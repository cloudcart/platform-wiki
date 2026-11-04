---
type: feature
nav_path: "Marketing → Discounts → Products → Plan gates"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Fixed discount plan gates", "discount_fixed quota", "total_discounts", "This feature is not enabled for your plan"]
tags: [marketing, discounts, fixed, plan-gates, permission]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation rules, row writes, API access, storefront display).

# Fixed discount — plan gates, permission

## Purpose

This aspect documents **what blocks a merchant from creating** a Fixed discount: the plan check on the admin create form, the `discount_fixed` quota on the APIs, the `total_discounts` figure, and the `marketing.discounts` permission scope. The Active switch takes effect immediately, any number of times.

For what the merchant clicks, see [[fixed-discount-product-modal]]. For the per-variant rows behind a discount, see [[fixed-discount-row-writes]].

## Where to find it

The plan checks surface in these places, all on create only:

- **Discount-type picker** (when creating a new discount from [[marketing-discounts]]) — the **Fixed discount** card stays clickable; only the Discount code (PRO) card is gated.
- **Admin create form** — checks whether the kind is enabled on the plan (`discount-fixed`). If not, the create call returns HTTP 403 with *"This feature is not enabled for your plan. To access it, please upgrade your plan."* There is no numeric limit here.
- **JSON-API v2** — compares usage with `discount_fixed` and returns **HTTP 402 Payment Required**.
- **Admin GraphQL API** — `createDiscount` with type `fixed` compares usage with `discount_fixed`.

## What the merchant can do here

- Extend the `discount_fixed` quota via a feature pack purchase (see [[plan-vs-feature-pack]]).
- Delete unused Fixed discounts: usage counts discounts whether active or not, and only deleting lowers it.

## Settings & fields

There are no merchant-editable fields specific to this aspect. The relevant plan-feature keys (read-only from the merchant's perspective) are:

| Plan-feature key | Type | What it controls |
|---|---|---|
| `discount-fixed` | Enabled or not | Checked by the admin create form. |
| `discount_fixed` | Numeric | Usage quota for Fixed discounts, compared on create through JSON-API v2 and the Admin GraphQL API. Extendable via feature pack. |
| `total_discounts` | Displayed figure | A count across all discount types; not enforced. |

## Business rules

### Plan-gate mapping

The keys above are the plan-features for this discount type (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]). Only creating is checked; updates are not, on any path.

### Quota counter is at the **discount** level, not the product level

Fixed discounts count toward the `discount_fixed` quota one **per discount**, not per attached product. Concretely:

- Adding 100 products to one Fixed discount consumes **one slot**.
- Creating 5 Fixed discounts each with 20 products consumes **5 slots**.

Each Fixed discount can attach an unlimited number of products. This makes Fixed-type the cheapest plan-wise when many products need the same effective campaign price — the merchant rolls them all under one parent Fixed discount.

### `discount_fixed` is independent of `discount_global` and `discount_coupon`

Fixed discounts count toward the **`discount_fixed`** plan-feature quota — a counter independent of:

- `discount_global` — no-code Flat / Percent / Shipping.
- `discount_coupon` — discounts holding their own code.

Each quota is compared separately on API create.

### API paths

Creating through JSON-API v2 or the Admin GraphQL API is checked against `discount_fixed`. JSON-API v2 returns **HTTP 402 Payment Required**. Updates are not checked. See [[fixed-discount-api-access]] for the full API-side pipeline.

### Permission scope

The page and all CRUD endpoints are scoped under the standard `marketing.discounts` permission. Sub-users without this permission see neither the discount in the [[marketing-discounts]] list nor the products page itself. The permission is granted at the role level — see [[merchant-roles]] for role assignment.

### Plan messages — quick reference

| Trigger | Response | Where surfaced |
|---|---|---|
| Admin create form, kind not enabled on the plan | HTTP 403, *"This feature is not enabled for your plan. To access it, please upgrade your plan."* | Create form. |
| JSON-API v2 create at the `discount_fixed` quota | HTTP 402 Payment Required | API response. |
| Admin GraphQL API `createDiscount` at the `discount_fixed` quota | Refused with a plan error | API response. |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-row-writes]] — what each save and toggle writes.
- [[fixed-discount-api-access]] — API-side plan checks.
- [[fixed-discount-product-modal]] — the inline / bulk toggle surfaces.
- [[discount-stacking]] — multi-discount evaluation rules.
- [[plan-gates]] — overview of the plan-gate enforcement model.
- [[plan-vs-feature-pack]] — how numeric gates extend via feature packs.
- [[plan-features]] — full plan-feature catalogue.
- [[marketing-discounts]] — parent feature; the Fixed discount type lives there.
- [[merchant-roles]] — where the `marketing.discounts` permission is assigned.

## Open questions

No outstanding questions.
