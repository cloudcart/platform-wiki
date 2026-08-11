---
type: feature
nav_path: "Marketing → Discounts → Percent → Plan gates"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount plan gates", "discount_global quota", "discount_coupon quota", "Percent HTTP 403"]
tags: [marketing, discounts, percent, plan-gates]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, stacking, validity, programmatic access).

# Percent discount — plan gates + quotas

## Purpose

This page documents the two plan-feature quotas that a Percent discount counts against (`discount_global` for no-code, `discount_coupon` for code-based), what the merchant sees at the cap, and the inconsistency between the route-layer plan key naming and the configuration-file naming.

## Where to find it

The current-vs-cap counter is shown on the [[marketing-discounts]] list view (the *"X / N used"* badge for each plan-gated counter). The plan-feature configuration itself is administered via [[plan-features]] + [[plan-vs-feature-pack]]. The HTTP 403 fires on the discount create / update routes — both the admin form save and the JSON-API v2 / GraphQL writes ([[percent-discount-programmatic-access]]).

## What the merchant can do here

- Track quota usage via the in-product counter on the discounts list.
- Pick between adding a code (`discount_coupon` quota) or staying no-code (`discount_global` quota) when one quota has more headroom than the other.
- Extend either quota via a [[plan-vs-feature-pack|feature pack]] when the plan limit is reached.

## Settings & fields

The plan-feature keys consumed by Percent discount creation:

| Plan-feature key | Consumed by | Behaviour at cap |
|---|---|---|
| `discount_global` | No-code Percent (and no-code Flat / Shipping). Route-layer dash variant: `discount-global`. | HTTP 403 with *"Not supported by plan"*. The type-picker card greys out. |
| `discount_coupon` | Code-based Percent (and all other code variants). Route-layer dash variant: `discount-code`. | HTTP 403 with *"Not supported by plan"*. |

## Counters and what the merchant sees at the cap

- A Percent discount **without a code** counts toward the **`discount_global`** plan-feature quota (shared with no-code Flat and no-code Shipping discounts).
- A Percent discount **with a code** counts toward the **`discount_coupon`** quota (shared with all code-based variants).

If the merchant's plan is at the limit for either quota, the create attempt returns **HTTP 403 Forbidden** with the merchant-facing message *"Not supported by plan"* and a list of plans where additional capacity is available. (Older wiki phrasing said HTTP 402; corrected — the actual response code is 403.)

## Plan-feature key naming inconsistency

The plan-feature catalogue uses inconsistent key naming between the route layer (uses dashes — `discount-global`, `discount-code`) and the configuration files (uses underscores — `discount_global`, `discount_coupon`). For Percent discount create, the practical implication is that the listing UI's *"X / N used"* counter is the **reliable enforcement point**, not the HTTP 403 response. Merchants and integrators should rely on the in-product counter rather than expecting consistent HTTP behaviour at overflow.

## Plan-gating mapping

| Quota | Shape | Applies to | Notes |
|---|---|---|---|
| `discount_global` | Numeric + Access | No-code Percent (and no-code Flat / Shipping) | Lower plans cannot access the `discounts/add` route; the Discount type-picker card greys out at the cap. Extendable via [[plan-vs-feature-pack|feature pack]]. |
| `discount_coupon` | Numeric | Code-based Percent (and all other code variants — Container codes, Code PRO, etc.) | Same overflow HTTP 403 behaviour at the cap. |

## Side effects of plan-gate overflow

When the create attempt is rejected for plan reasons:

- **No discount row is persisted.**
- **No `discount.created` webhook fires** (see [[settings-hooks]]).
- **The in-product counter does not increment.**
- **The merchant sees the *"Not supported by plan"* message** + the upgrade path.

For JSON-API v2 / GraphQL writes, the same 403 is returned — see [[percent-discount-programmatic-access]].

## Business rules

- The `discount_global` quota is **shared** across no-code Percent / Flat / Shipping — a merchant on a 10-discount plan with 5 Flat discounts has only 5 slots left for no-code Percent + Shipping combined.
- The `discount_coupon` quota is **shared** across ALL code variants (Percent code, Flat code, Shipping code, Container codes, Code PRO entries).
- The plan-key naming inconsistency means support tickets like *"merchant got 403 but the in-product counter shows headroom"* should be investigated against the configuration-file key (`discount_global` / `discount_coupon`), not the route-layer dash version.

## Related

- [[marketing-discounts-percent]] — hub.
- [[plan-gates]] — full plan-feature mechanics.
- [[plan-vs-feature-pack]] — how feature packs extend plan quotas.
- [[plan-features]] — the catalogue of plan-feature keys.
- [[marketing-discounts-flat]] — sister quota counterpart for `discount_global`.
- [[marketing-discounts-codes]] — Container codes; same `discount_coupon` quota.
- [[marketing-discounts-code-pro]] — Code PRO; same `discount_coupon` quota.
- [[percent-discount-programmatic-access]] — same HTTP 403 on API writes.

## Open questions

- Confirm whether the in-product counter and the validator both consult the same underlying counter or whether the route-layer key vs config-file key drift can produce divergent answers `(verify)`.
