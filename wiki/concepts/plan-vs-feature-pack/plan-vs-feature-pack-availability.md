---
type: concept
nav_path: "Concept → Plan vs. feature pack → Availability gates"
aliases: ["enable_feature_pack flag", "Pack not available on my plan", "Feature plan-tier restricted", "max_value ceiling", "Dynamic-pricing packs", "Why no pack option", "Availability gates", "Защо няма пакет за моя план", "Таван на лимита"]
tags: [plans, plan-features, feature-pack, billing, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-vs-feature-pack]]. See the hub for the other aspects (stacking, downgrade, cost heuristic, pack lifecycle).

# Plan vs. feature pack — availability gates

## Definition

Even when a feature has packs in the catalog, **whether a pack actually surfaces** for a given merchant depends on three independent gates: the per-plan `enable_feature_pack` flag, the separate `plan.restrict.feature_purchase` plan-tier restriction, and the per-feature `max_value` ceiling. A fourth wrinkle — **dynamic-pricing** packs — changes the shape of the pack list itself. When any gate is closed, the merchant's only path is a plan upgrade, no matter what the [[plan-vs-feature-pack-cost-heuristic|cost comparison]] would otherwise suggest.

## Scope

Covered:

- `enable_feature_pack` — per-plan, per-feature flag that turns the pack list on or off.
- `plan.restrict.feature_purchase` — features locked to specific plan tiers entirely.
- `max_value` — the absolute quota ceiling no amount of packs can pass.
- Dynamic-pricing packs — the volume-discount ladder shape.

Not covered here:

- The effective-quota math once a pack IS allowed — see [[plan-vs-feature-pack-stacking]].
- Price-based choice between an allowed pack and an upgrade — see [[plan-vs-feature-pack-cost-heuristic]].
- The pack subscription lifecycle after purchase — see [[plan-vs-feature-pack-lifecycle]].

## Contrasts

- **`enable_feature_pack` vs. `plan.restrict.feature_purchase`**: two distinct config entries. `enable_feature_pack` governs whether packs are sold for a feature on a given plan (the feature exists on the plan, but extension is on/off). `plan.restrict.feature_purchase` locks the entire feature to specific tiers — on lower tiers there is no feature and no pack. They work together: a feature can be tier-restricted entirely on Free / Starter, then have `enable_feature_pack` govern extension on Pro / Business / Enterprise.
- **Pack-extensible vs. plan-tier-only**: a pack-extensible feature can grow via packs on the qualifying plans; a plan-tier-only feature can ONLY be unlocked by moving to a qualifying plan — no pack helps.
- **Fixed-size packs vs. dynamic-pricing packs**: fixed packs are a small/medium/large menu; dynamic packs are a ladder of arbitrary quantities at a per-unit price that decreases as quantity grows.

## Where it applies

### `enable_feature_pack` — per-plan, per-feature flag

The catalog stores an `enable_feature_pack` flag per plan-restriction (per feature × per plan). When it is OFF for the merchant's current plan × the specific feature, the pack list on [[plan-features]] is **EMPTY** — even if packs exist in the catalog, they don't surface for that merchant.

Example: the Free plan deliberately doesn't allow product-quota extensions via packs (`enable_feature_pack = 0` for `products` on Free). Merchants on Free must upgrade to Starter before they can buy product packs — Free is meant for evaluation, not indefinite pack extension.

When the flag is OFF but packs exist on other plans, the merchant sees: *"This feature is not enabled for your plan. To access it, please upgrade your plan."* plus a list of plans that DO support pack purchases — e.g., *"Plans that support this functionality are: **Pro**, **Unicorn**"*.

### Plan-tier-restricted features — pack can't unlock

Some features are restricted to specific plan tiers entirely — no pack unlocks them on a lower plan. Example: `custom_hostname` (additional storefront domains beyond the default subdomain) is restricted to Pro and Unicorn. A Starter merchant visiting `/admin/plan/feature/custom_hostname` sees the restriction banner with the qualifying plans + an upgrade button, and **no pack list**. Pack purchases are disabled. This is configured via the separate `plan.restrict.feature_purchase` config entry.

### Max-value ceiling — even packs can't push past

Each feature has a `max_value` ceiling — the absolute maximum quota even with packs (e.g., 100,000 products). Before placing a pack in the cart, the platform computes the projected total (plan base + active packs + this new pack) and **rejects** the purchase if it would exceed `max_value`. The merchant sees an inline error: *"Your package allows **100000** products"* and stays on the feature screen. Above this ceiling the merchant must upgrade to a higher plan with a different `max_value` (typically Enterprise has the highest caps).

### Dynamic-pricing packs — volume-discount ladder

A handful of features support **dynamic pricing** — the pack list isn't a fixed small / medium / large but a ladder of arbitrary quantities (e.g., 500, 1000, 2000, 5000 products) with the per-unit price decreasing as quantity grows. The merchant picks a step; the platform computes the price via the volume-discount formula and seeds the cart. For these features the choice is less "pack vs. upgrade" and more "how much capacity at what unit price?" — the upgrade alternative is still shown for comparison.

## Related

- [[plan-vs-feature-pack]] — hub.
- [[plan-vs-feature-pack-cost-heuristic]] — when a pack IS available, the price comparison; this page covers when it is NOT.
- [[plan-features]] — the paywall that renders (or hides) the pack list per these gates.
- [[plans]] — plan catalog; the only path when a feature is tier-locked.
- [[plan-gates]] — gating engine reading the same restriction config.

## Open Questions

None.
