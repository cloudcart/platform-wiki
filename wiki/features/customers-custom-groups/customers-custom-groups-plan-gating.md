---
type: feature
nav_path: "Customers → Customer groups → Plan gating"
route_name: customers-custom-groups
route_path: /admin/customers/groups
aliases: ["Customer groups plan cap", "customer_groups feature", "Group limit reached", "Groups used chip", "Капацитет на клиентски групи"]
tags: [customers, groups, plan-gated, capacity, billing]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# Customer groups — plan gating

> Part of [[customers-custom-groups]]. See the hub for the other aspects (manage, system groups, integration, API).

## Purpose

How the merchant's plan caps the number of customer groups, how the usage chip reflects that cap, and how the limit is enforced (server-side, un-bypassable) and extended (via add-on packs). This is the page for *"why can't I create another customer group?"* tickets.

## Where to find it

Sidebar → Customers → **Customer groups** (`/admin/customers/groups`). The cap surfaces in the header **"X of Y groups used"** chip and the **Upgrade plan** button; the access route itself is also URL-gated, so a plan without the feature redirects away from the page to the paywall.

## What the merchant can do here

- **See current usage** — the *"X of Y groups used"* chip is always visible. Y becomes ∞ when the plan tier has no cap.
- **Hit the cap gracefully** — when X = Y, the **+ Add customer group** button funnels through the upgrade modal (message: *"To be able to create mode customer groups, you must upgrade your plan"*) instead of opening the create form.
- **Upgrade or extend** — the **Upgrade plan** button opens the standard upgrade flow; numeric caps can also be extended via add-on packs (see [[plan-features]] / [[plan-vs-feature-pack]]).

## Settings & fields

| Surface | Value | Source |
|---------|-------|--------|
| **Y** (cap) | Max groups for the plan | Plan feature value of `customer_groups` |
| **X** (used) | Current group count | Total group count, **including** the 2 system groups |
| **∞** | Unlimited | Shown when the plan has no `customer_groups` cap |

## Business rules

### The `customer_groups` plan gate

This feature is gated by a single numeric plan feature (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `customer_groups` | Numeric (max customer groups) | Per-plan cap on the number of customer groups. |

### The count includes the 2 system groups

The cap is compared against the **total** group count — which includes the protected Default and Guests groups (see [[customers-custom-groups-system-groups]]). So a plan advertising *"5 customer groups"* yields **3** merchant-creatable slots. The usage chip reflects this same total, so a brand-new store shows *"2 of 5 groups used"* before the merchant has created anything.

### Enforced server-side — cannot be bypassed

The cap is enforced at create time and on every API write, not just in the UI. When the total group count meets or exceeds the plan's `customer_groups` value, the platform returns *"Group limit reached"* on overflow. The JSON-API v2 path hits the **same** server-side check — there is no way to exceed the cap programmatically (see [[customers-custom-groups-api]]).

### URL-gated access

Plans without the `customer_groups` feature are redirected away from `/admin/customers/groups` to the paywall — the page is not just visually disabled, the route itself is gated.

### Extending the cap

Numeric gates extend via add-on packs. The merchant can either upgrade the base plan or buy a pack that raises the `customer_groups` value (see [[plan-features]] and [[plan-vs-feature-pack]]).

## Related

- [[customers-custom-groups]] — hub.
- [[customers-custom-groups-system-groups]] — the 2 system groups counted against the cap.
- [[customers-custom-groups-api]] — the same cap enforced on API writes.
- [[plan]] — plan tier governs the cap.
- [[plan-gates]] — concept page on plan-based feature gating.
- [[plan-vs-feature-pack]] — how numeric caps extend via packs.
- [[plan-features]] — per-feature upsell / add-on packs.

## Open questions

None.
