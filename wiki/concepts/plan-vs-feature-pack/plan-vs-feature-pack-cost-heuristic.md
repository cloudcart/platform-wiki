---
type: concept
nav_path: "Concept → Plan vs. feature pack → Cost heuristic"
aliases: ["When to upgrade vs buy pack", "Pack cheaper or plan cheaper", "Cost comparison plan pack", "Two or three packs equal upgrade", "Cost heuristic", "Кое е по-евтино пакет или ъпгрейд", "Кога да ъпгрейдна вместо пакет"]
tags: [plans, plan-features, feature-pack, billing, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-vs-feature-pack]]. See the hub for the other aspects (stacking, downgrade, availability gates, pack lifecycle).

# Plan vs. feature pack — cost heuristic

## Definition

The merchant's "upgrade or buy a pack?" decision comes down to **how many distinct feature limits they're hitting** and the **relative price** of the packs vs. the next-tier upgrade. A pack is surgical — it pays only for the one feature in question. An upgrade is broad — one charge raises many quotas and unlocks boolean features at once. The heuristic balances those.

A rough rule of thumb: **2–3 packs ≈ one plan upgrade in cost terms.** If the merchant is likely to need a third pack soon, upgrading first is usually cheaper.

## Scope

Covered:

- The decision table mapping "how many limits hit" → recommended choice.
- The 2–3-packs rule of thumb.
- Where the merchant reads the actual prices to compare.

Not covered here:

- The additive math behind effective quota — see [[plan-vs-feature-pack-stacking]].
- Cases where a pack is unavailable / a feature is plan-tier-locked (which forces an upgrade regardless of price) — see [[plan-vs-feature-pack-availability]].
- The over-quota remedy choice after a downgrade — see [[plan-vs-feature-pack-downgrade]].

## Contrasts

- **Pack-economical vs. upgrade-economical**: a single feature limit favours the pack; three-plus limits favour the upgrade; two limits are a genuine price comparison.
- **Surgical spend vs. broad spend**: packs pay for exactly what's needed but don't scale efficiently when several quotas all need lifting; an upgrade overshoots on the single-limit case but wins as soon as multiple quotas (or a boolean+numeric combo) are involved.

## Where it applies

### The decision table

| Situation | Recommended choice |
|-----------|--------------------|
| Hit 1 specific feature limit (e.g., out of products), all other quotas fine | **Pack** — pays only for what they need; cheaper |
| Hit 2 specific feature limits in close succession | **Compare prices**: if both packs combined > the plan-upgrade cost, upgrade |
| Hit 3+ feature limits | **Plan upgrade** — almost always cheaper; one charge unlocks many features |
| Need a feature that requires a higher plan (not extensible via packs) | **Plan upgrade required** — no pack option exists (see [[plan-vs-feature-pack-availability]]) |
| Need a boolean feature (e.g., `discount-code-pro`, `support_meetings`) that's on the next plan AND has a pack | **Compare**: pack price for boolean unlock vs. plan upgrade |
| Need a long-term broader capability (e.g., SSL + Storefront Builder + Cart Rules at once) | **Plan upgrade** — packs don't cover boolean+numeric combos efficiently |

### Where the prices live

Exact prices live in the catalog and are **country-specific**. The merchant eyeballs two screens:

- [[plans-purchase]] shows the next-tier plan price.
- [[plan-features]] shows the pack price for the specific feature.

The [[plan-features]] paywall also surfaces the alternative inline — *"you can also upgrade your plan"* — with the list of qualifying plans, so the merchant can make the comparison on a single screen without hunting for the plan catalog.

## Related

- [[plan-vs-feature-pack]] — hub.
- [[plan-vs-feature-pack-availability]] — when a pack isn't an option at all, forcing an upgrade regardless of price.
- [[plans]] — plan catalog for the upgrade alternative.
- [[plans-purchase]] — shows the next-tier price.
- [[plan-features]] — shows the pack price + the inline upgrade alternative.

## Open Questions

None.
