---
type: feature
nav_path: "Marketing → Discounts → Percent → Plan gates"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Percent discount plan gates", "discount_global quota", "discount_coupon quota", "Percent HTTP 403"]
tags: [marketing, discounts, percent, plan-gates]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, stacking, validity, programmatic access).

# Percent discount — plan gates + quotas

## Purpose

This page documents what each path checks when a Percent discount is created: the admin form's plan check, the JSON-API v2 quotas (`discount_global` for no-code, `discount_coupon` for code-based), and GraphQL.

## Where to find it

The plan-feature configuration is administered via [[plan-features]] + [[plan-vs-feature-pack]]. The checks run on create only, on the admin form save and on JSON-API v2 writes ([[percent-discount-programmatic-access]]). Neither the type-picker cards on [[marketing-discounts]] nor its list show these quotas; only the Code PRO card checks the plan.

## What the merchant can do here

- Through JSON-API v2, pick between adding a code (`discount_coupon` quota) or staying no-code (`discount_global` quota) when one quota has more headroom than the other.
- Extend either quota via a [[plan-vs-feature-pack|feature pack]] when the plan limit is reached.

## Settings & fields

The plan-feature keys checked when a Percent discount is created:

| Path | Key | Behaviour |
|---|---|---|
| Admin form | `discount-global` (no code), `discount-code` (code) | Checks whether that kind is enabled on the plan. If not, HTTP 403 with *"This feature is not enabled for your plan. To access it, please upgrade your plan."* No numeric limit. |
| JSON-API v2 | `discount_global` (no code), `discount_coupon` (code) | Compares usage with the plan's quota. At the limit, **HTTP 402 Payment Required**. |
| GraphQL `createDiscount` | — | These quotas are not checked for a Percent discount. |

## Counters

- `discount_global` counts no-code Percent, Flat and Shipping discounts.
- `discount_coupon` counts only discounts holding their own code. Container and Code PRO discounts do not add to it.
- Usage counts discounts whether active or not; only deleting lowers it.

## Side effects of plan-gate overflow

When the create attempt is rejected for plan reasons:

- **No discount row is persisted.**
- **No `discount.created` webhook fires** (see [[settings-hooks]]).

## Business rules

- On JSON-API v2, the `discount_global` quota is **shared** across no-code Percent / Flat / Shipping.
- On JSON-API v2, the `discount_coupon` quota is **shared** across discounts holding their own code: Percent, Flat and Shipping codes.

## Related

- [[marketing-discounts-percent]] — hub.
- [[plan-gates]] — full plan-feature mechanics.
- [[plan-vs-feature-pack]] — how feature packs extend plan quotas.
- [[plan-features]] — the catalogue of plan-feature keys.
- [[marketing-discounts-flat]] — sister quota counterpart for `discount_global`.
- [[marketing-discounts-codes]] — Container codes.
- [[marketing-discounts-code-pro]] — Code PRO.
- [[percent-discount-programmatic-access]] — API writes.

## Open questions

None.
