---
type: feature
nav_path: "Marketing → Discounts → Products → Plan gates & cooldown"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Fixed discount plan gates", "discount_fixed quota", "total_discounts", "Fixed discount cooldown", "Not supported by plan"]
tags: [marketing, discounts, fixed, plan-gates, cooldown, permission]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation rules, row writes, API access, storefront display).

# Fixed discount — plan gates, cooldown, permission

## Purpose

This aspect documents **what blocks a merchant from creating, activating, or toggling** a Fixed discount: the `discount_fixed` plan quota, the `total_discounts` aggregate ceiling, the *"Not supported by plan"* HTTP 403 response, the 10-minute activation cooldown that throttles repeated toggles, and the `marketing.discounts` permission scope.

For what the merchant clicks, see [[fixed-discount-product-modal]]. For the data the cap protects (per-variant rows), see [[fixed-discount-row-writes]].

## Where to find it

The plan-gate enforcement surfaces in three places:

- **Discount-type picker** (when creating a new discount from [[marketing-discounts]]) — the Fixed-type card is grayed out and labeled *"Not supported by plan"* when the merchant's plan lacks access or has hit the cap.
- **Create endpoint response** — the create call itself returns HTTP 403 with *"Not supported by plan"* if the merchant bypasses the picker (e.g., via a direct URL or the JSON-API v2 path).
- **Inline / parent toggle on `/admin/marketing-new/discounts/products/:id`** — the cooldown message *"You've already activated this discount…"* appears as a toast next to the Active switch.

## What the merchant can do here

- See whether the current plan allows another Fixed discount (the type-picker card is the canonical signal).
- Extend the `discount_fixed` cap via a feature pack purchase (numeric gate; see [[plan-vs-feature-pack]]).
- Plan toggle timing around the 10-minute cooldown — once-per-discount, not once-per-click.
- Read the cap-overflow message to distinguish *"Not supported by plan"* (plan / cap issue) from *"You've already activated this discount…"* (cooldown).

## Settings & fields

There are no merchant-editable fields specific to this aspect. The relevant plan-feature keys (read-only from the merchant's perspective) are:

| Plan-feature key | Type | What it controls |
|---|---|---|
| `discount_fixed` | Numeric + Access | Per-plan cap for Fixed-type discounts; lower plans cannot access the type at all. Extendable via feature pack. |
| `total_discounts` | Numeric (aggregate) | Aggregate cap across all discount types. |

## Business rules

### Plan-gate mapping

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `discount_fixed` | Numeric + Access | Per-plan cap for Fixed-type discounts. Counted against the platform code. Lower plans cannot access the Fixed discount type at all — the type-picker card shows *"Not supported by plan"*. Access route: `discounts/add/fixed`. Each Fixed discount can attach an unlimited number of products (no per-product plan limit). Extendable via feature pack. |
| `total_discounts` | Numeric (aggregate) | Aggregate cap across all discount types — Fixed discounts also count toward this global ceiling. |

When over the cap or below the access tier, the create endpoint returns **HTTP 403 Forbidden** with *"Not supported by plan"*, and the type-picker modal grays out the Fixed card. Numeric gates extend via packs ([[plan-vs-feature-pack]]); boolean / access gates require a plan upgrade.

> Older wiki phrasing claimed HTTP 402 on cap-overflow — that was incorrect. The actual response is HTTP 403.

### Quota counter is at the **discount** level, not the product level

Fixed discounts count toward the `discount_fixed` quota one **per discount**, not per attached product. Concretely:

- Adding 100 products to one Fixed discount consumes **one slot**.
- Creating 5 Fixed discounts each with 20 products consumes **5 slots**.

Each Fixed discount can attach an unlimited number of products. This makes Fixed-type the cheapest plan-wise when many products need the same effective campaign price — the merchant rolls them all under one parent Fixed discount.

### `discount_fixed` is independent of `discount_global` and `discount_coupon`

Fixed discounts count toward the **`discount_fixed`** plan-feature quota — a counter independent of:

- `discount_global` — no-code Flat / Percent / Shipping (the cart-evaluation-time discounts).
- `discount_coupon` — code-based variants (Container codes, Code PRO).

The merchant's plan determines how many Fixed-type discounts they may create separately from the other discount-type quotas. A merchant with all `discount_global` slots used can still create Fixed discounts up to the `discount_fixed` cap.

### 10-minute activation cooldown (applies to Fixed)

Toggling a Fixed discount's active status is rate-limited to **once per 10 minutes per discount** (same as no-code Flat / Percent / Shipping). Within the cooldown window the toggle response is:

> *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."*

The cooldown applies because each toggle triggers a per-variant attachment regeneration cycle — see [[fixed-discount-row-writes]]. The throttle prevents thrashing the background queue on high-catalog stores.

The cooldown is bypassed in development environments and command-line contexts.

#### Scope of the cooldown (per-type table)

The cooldown applies to no-code Flat / Percent / Shipping / **Fixed** discounts. Code-based variants, Container codes, Quantity, Countdown, and Code PRO have NO cooldown. See [[discount-stacking]] for the full per-type cooldown table.

### Inline-toggle and bulk-toggle also count

The cooldown is per discount (not per click). The following all count toward the same per-discount 10-minute window:

- The parent Fixed-discount on/off toggle on the [[marketing-discounts]] list page.
- The inline Active toggle on a single product row inside this discount's products list.
- Bulk **Set status active** / **Set status unactive** from the products list action bar.

The merchant who flips the parent off, then immediately tries to bulk-activate products inside, will hit the cooldown.

### API-path overflow still returns HTTP 403

A create or update request through JSON-API v2 or GraphQL is subject to the **same** `discount_fixed` + `total_discounts` checks. Overflow returns **HTTP 403 Forbidden** with *"Not supported by plan"* — same response as the admin form. See [[fixed-discount-api-access]] for the full API-side pipeline.

The 10-minute cooldown also applies to API-driven status toggles.

### Permission scope

The page and all CRUD endpoints are scoped under the standard `marketing.discounts` permission. Sub-users without this permission see neither the discount in the [[marketing-discounts]] list nor the products page itself. The permission is granted at the role level — see [[merchant-roles]] for role assignment.

### Cap-overflow merchant message — quick reference

| Trigger | Response | Where surfaced |
|---|---|---|
| Create a new Fixed discount over the `discount_fixed` cap | HTTP 403, *"Not supported by plan"* | Toast on the create form; type-picker card grays out. |
| Create a new Fixed discount over the `total_discounts` aggregate cap | HTTP 403, *"Not supported by plan"* | Same toast; aggregated across all discount types. |
| Toggle within 10 min of last toggle | Same-page error: *"You've already activated this discount. Please wait:minutes minutes…"* | Inline toast next to the Active switch. |
| Access route `discounts/add/fixed` on a plan below the access tier | HTTP 403 redirect to the discounts list | Grayed-out type-picker card. |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-row-writes]] — what each toggle / save regenerates (and why the cooldown exists).
- [[fixed-discount-api-access]] — API-side plan-gate and cooldown enforcement.
- [[fixed-discount-product-modal]] — the inline / bulk toggle surfaces that also count toward the cooldown.
- [[discount-stacking]] — per-type cooldown table covering all discount types.
- [[plan-gates]] — overview of the plan-gate enforcement model.
- [[plan-vs-feature-pack]] — how numeric gates extend via feature packs.
- [[plan-features]] — full plan-feature catalogue.
- [[marketing-discounts]] — parent feature; the Fixed discount type lives there.
- [[merchant-roles]] — where the `marketing.discounts` permission is assigned.

## Open questions

No outstanding questions.
