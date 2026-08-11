---
type: concept
nav_path: "Concept → Plan gates → Restriction shapes & lookup"
aliases: ["Plan restriction shapes", "Unrestricted boolean numeric", "Plan feature lookup", "Feature value lookup", "Feature pack stacking", "Effective cap", "Quota lookup", "Форми на ограничение", "Изчисляване на лимита"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-gates]]. See the hub for the other aspects (enforcement points, LTA contracts, trial / catalogs, feature naming).

# Plan gates — restriction shapes & lookup

## Definition

Every plan-feature mapping stores, for the merchant's current plan, exactly ONE of three **restriction shapes**. This shape is what the gating engine reads when it decides whether to let an action through. The three shapes are:

| Restriction value | What it means | Example mapping |
|-------------------|---------------|-----------------|
| **Unrestricted** (no row / null) | Feature is open with no cap. | `email_unlimited` on Enterprise. |
| **Boolean** (`true` = locked / `false` = unlocked) | Feature is a flat on/off paywall. | `discount-code-pro: true` on Starter (locked) / `false` on Pro (unlocked). |
| **Numeric** (an integer) | Feature has a quota; the platform compares used-vs-cap. | `products: 500` on Starter; `products: 5000` on Pro; `products: -1` (unlimited) on Enterprise. |

Two conventions worth remembering: a numeric value of `-1` means **unlimited** (the Enterprise pattern), and for the boolean shape `true` means *locked* (the inverse of what reads naturally — `true` = "this restriction is in force").

The lookup is **cached per `<feature, plan>` pair for 1 week**, so the same gate check across many requests is fast. When a merchant buys or cancels a feature pack, that cache is flushed so the new effective cap takes effect immediately (see [[plan-vs-feature-pack-lifecycle]]).

## Scope

What this covers:

- The three restriction shapes — *unrestricted*, *boolean*, *numeric* — and their value conventions (`-1` = unlimited, `true` = locked).
- The 1-week-cached `<feature, plan>` lookup.
- How feature-pack add-ons sum on top of the plan's base value to produce the effective cap.

What it does NOT cover:

- Where the gate is actually enforced and what response it returns — see [[plan-gates-enforcement-points]].
- The per-feature numeric caps per plan tier — runtime data on [[plans]] / [[plan-details]].
- When to buy a pack vs. upgrade the plan — see [[plan-vs-feature-pack]].
- The pack's billing cycle / cache-flush timing — see [[plan-vs-feature-pack-lifecycle]].

## Contrasts

- **Boolean vs. numeric**: a boolean gate is a flat paywall (locked / unlocked); a numeric gate compares used-against-cap and can be partially consumed (490 of 500 products). The HTTP response differs accordingly — see [[plan-gates-enforcement-points]].
- **Plan base value vs. effective cap**: the plan stores a *base* numeric value; the effective cap is base + the sum of active feature-pack subscriptions for that feature. The gate always reads the effective cap, never the bare base. Stacking detail lives on [[plan-vs-feature-pack-stacking]].
- **`-1` unlimited vs. unrestricted (no row)**: both behave as "no cap", but `-1` is an explicit numeric sentinel set on the plan, whereas unrestricted means the feature simply has no restriction row at all.

## Where it applies

### Feature-pack add-ons stack on top of the plan value

When the merchant buys a feature pack (e.g., *+100 products*) on [[plan-features]], a subscription row is created for that pack. At lookup time, the platform sums the plan's numeric value + every active feature-pack subscription for that feature → the effective cap. So a Starter merchant who bought one *+100 products* pack effectively has 600 products until the pack subscription ends.

For **boolean** features, an active feature-pack subscription flips the lock OFF — equivalent to switching to a plan that unlocks the feature, but only for the pack's duration.

The worked stacking examples (Starter 500 + pack 100 = 600 effective; pack survives a plan upgrade) live on [[plan-vs-feature-pack-stacking]] — this aspect only establishes that the lookup *sums* base + active packs.

### The cache, and why a fresh pack takes effect immediately

Because the `<feature, plan>` lookup is cached for a week, a naive implementation would leave a just-purchased pack invisible for up to 7 days. The platform avoids this by flushing the affected cache entry on pack purchase / cancel, so the higher (or lower) effective cap is read on the very next gate check. This is the same cache the [[plan-gates-enforcement-points]] create-endpoint check consults.

## Related

- [[plan-gates]] — hub.
- [[plan-features]] — the feature-pack upsell screen; where packs that stack onto the base are bought.
- [[plan-vs-feature-pack-stacking]] — the full `effective = plan base + active packs` formula with worked examples.
- [[plan-vs-feature-pack-lifecycle]] — the pack subscription lifecycle + the cache flush on purchase / cancel.
- [[plans]] / [[plan-details]] — where the per-tier numeric values live.
- [[plan-feature]] — the Plan-Feature entity catalog.

## Open Questions

None.
