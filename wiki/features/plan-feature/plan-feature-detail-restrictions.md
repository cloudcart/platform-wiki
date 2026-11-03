---
type: feature
nav_path: "Plan → Feature → Restrictions & limits"
route_name: plan-feature-packs
route_path: /admin/plan/feature/:id
aliases: ["Plan feature restriction banner", "Feature not enabled for your plan", "No feature pack available", "max_value cap", "Dynamic-pricing formula", "Plans that support this functionality", "Ограничение по план"]
tags: [plans, plan-feature, feature-pack, restrictions, dynamic-pricing, vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-feature]]. See the hub for the other aspects (pack list, buy → checkout flow, pack lifecycle).

# Plan feature — restrictions & limits

## Purpose

This aspect covers everything that **blocks or shapes** a pack purchase on the *Plan feature* screen: the plan-restriction banner that hides the pack table, the empty-packs auto-redirect to the upgrade-plan modal, the hard `max_value` ceiling that rejects an over-cap buy, and the server-side dynamic-pricing formula that generates the price ladder. These are the rules the merchant runs into when they *can't* simply pick a pack and pay.

## Where to find it

- Reached on the same `/admin/plan/feature/{id}` Vue screen as [[plan-feature-detail-pack-list]] — the restriction states render **in place of** the pack table.
- The banner / empty-state appears automatically based on the feature's plan-restriction config and whether any packs exist for the merchant's plan; the merchant doesn't toggle anything to see it.

## What the merchant can do here

- **Read the restriction banner** explaining the feature needs a higher plan tier, and which plans support it.
- **Get funnelled to the upgrade-plan modal** when no packs are available for their plan (the screen opens it automatically).
- **Pick a step inside the dynamic-pricing ladder** — the ladder is generated server-side at fixed increments up to the feature's cap; the merchant picks one step, not a free-form value.

## What the merchant cannot do here

- **Buy a pack for a feature their plan disables** — when `enable_feature_pack` is false on the plan-restriction pivot for this feature, the pack list is empty and the upgrade-plan modal opens. The merchant must upgrade to a plan where packs are enabled for this feature.
- **Buy a pack for a feature restricted to higher tiers** — the banner blocks all purchases on this screen until the merchant is on a qualifying plan.
- **Exceed the feature's `max_value` cap** — the backend rejects a pack purchase that would push the merchant's total quota beyond the feature's hard ceiling.
- **Set a custom quantity outside the dynamic-pricing ladder** — the ladder is generated server-side at fixed increments; the merchant picks one step.

## Settings & fields

This is a read-only / gating surface — no editable fields. The merchant sees one of these states:

| State | What renders | Trigger |
|-------|--------------|---------|
| **Restriction banner** | Yellow `info-box-warning` card with two texts + a *View prices* button | `feature.purchaseRestrictMessage` is set (array of plan names) |
| **Empty-packs auto-redirect** | Panel auto-closes; shared upgrade-plan modal opens | `packs.length === 0 && !purchaseRestrictMessage` |
| **No-results note** | Localised *"No results found"* in place of the table | No packs but feature not fully restricted (verify) |

The restriction banner texts (verbatim):

> *"This feature is not enabled for your plan. To access it, please upgrade your plan."*
> *"Plans that support this functionality are: **<plan-names>**"*

A centered *View prices* button shows below the banner, but **in the current build it has no click handler** — it is a static button. The upgrade path is reached instead via the empty-packs auto-redirect or from [[plan-features]].

## Business rules

### Restriction banner sources its plan list from config

The "Plans that support this functionality" banner reads its plan list from `plan.restrict.feature_purchase.<feature_mapping>` in the platform config. When the requested feature has that key set AND the merchant's plan isn't in the allowed list, the backend response includes `purchaseRestrictMessage` as an array of plan names and the screen renders the banner instead of the pack table. When the restriction doesn't apply, the message is `false` and the table shows. Plans are filtered to active + with active details, so soft-disabled / country-restricted plans don't appear in the suggestion.

### Empty packs → upgrade-plan modal

If `packs` is empty — either the plan disables packs for this feature or no packs exist — the screen automatically opens a shared upgrade-plan modal with the translated note *"No feature pack available, you can upgrade your plan."* and routes the merchant to [[plans]].

### `max_value` cap on cart-add

When the merchant clicks *Buy*, the backend computes `current_value + pack_value` against the feature's `max_value`. If it would exceed the cap, the cart-add is rejected with the localised `plan.plan_limit` error message and the merchant stays on the screen.

### Dynamic-pricing ladder generation

For features with `dynamic_pricing = 1`, the price ladder is generated server-side. The algorithm starts at the pack's base (`value`, `price`) and walks up in multiples of `value`, computing each step's price with:

```
floor((price / value × current) × (0.9 − 1.5 × current / value / 100))
```

rounded to a 0.50 step, ending when the per-unit price stops decreasing OR when the feature's `max_value` is reached. This is why the ladder is a finite set of discrete steps, not an open-ended slider. The resulting steps are surfaced as individual rows in [[plan-feature-detail-pack-list]].

## Related

- [[plan-feature]] — hub.
- [[plan-feature-detail-pack-list]] — the pack table these states replace; the ladder steps this formula produces.
- [[plan-feature-detail-buy-flow]] — where the `max_value` rejection surfaces (on *Buy*).
- [[plan-features]] — the cards screen and alternate upgrade entry point.
- [[plans]] — the plan catalog the upgrade modal routes to.
- [[plan-gates]] — the gating concept that funnels merchants to this screen.

## Open questions

None.
