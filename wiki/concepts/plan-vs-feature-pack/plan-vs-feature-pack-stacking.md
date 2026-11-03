---
type: concept
nav_path: "Concept → Plan vs. feature pack → Stacking & survival"
aliases: ["Feature pack stacking", "Plan base plus packs", "Effective quota", "Do packs survive plan upgrade", "Packs survive plan change", "Stacking rule", "Пакетите се натрупват", "Ефективен лимит"]
tags: [plans, plan-features, feature-pack, billing, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-vs-feature-pack]]. See the hub for the other aspects (downgrade, cost heuristic, availability gates, pack lifecycle).

# Plan vs. feature pack — stacking & survival

## Definition

The defining behaviour of feature packs is that they **stack on top of the plan's base quota** and **survive plan changes**. A plan upgrade ([[plans]]) replaces the merchant's tier base; a feature pack ([[plan-features]]) adds quota to ONE feature on top of whatever plan is currently active. The two are additive, not exclusive.

The gating engine computes, at every limit check:

```
effective_quota = plan_base_value + sum(active feature-pack subscription values for this feature)
```

Each active pack subscription contributes its `value` field (e.g., 100, 500, 1000) to the plan's base. Cancelled / Expired pack subscriptions do NOT contribute — only **Active** ones (and **Past due** ones until their final retry fails — see [[plan-vs-feature-pack-lifecycle]]).

Worked examples:

- Starter (500 products base) + no packs → **500** effective.
- Starter (500) + one *+100 products* pack → **600** effective.
- Starter (500) + one *+100* pack + one *+500* pack → **1100** effective.
- Pro (5000 products base) + same *+100* pack still active after upgrade → **5100** effective.

For **boolean** features (e.g., `discount-code-pro`, `support_meetings`), an Active pack subscription flips the feature ON — equivalent to switching to a plan that unlocks it — but only for the pack's duration.

## Scope

Covered:

- The stacking formula: effective limit = plan base + active packs.
- The survives-plan-change rule and the billing-surprise it causes.
- How boolean-feature packs stack (ON/OFF rather than numeric).
- Which subscription states contribute to the sum.

Not covered here:

- What happens when downgrade puts the merchant over quota — see [[plan-vs-feature-pack-downgrade]].
- When a pack is cheaper than an upgrade — see [[plan-vs-feature-pack-cost-heuristic]].
- Whether a pack is even purchasable on the current plan — see [[plan-vs-feature-pack-availability]].
- The pack's own billing cycle and cache flush — see [[plan-vs-feature-pack-lifecycle]].

## Contrasts

- **Plan upgrade vs. plan-feature stacking**: stacking is **additive** — a Pro plan (5000) plus a +500 pack = 5500 effective. Upgrade is **replacement** — moving from Starter (500) to Pro (5000) doesn't add the 500; the new plan's 5000 becomes the new base. If the merchant had a +100 pack on Starter (600 effective), upgrading to Pro keeps the +100 pack and adds it to the Pro base (5100 effective). The pack survives the upgrade.
- **Numeric pack vs. boolean pack**: numeric packs add a quantity to a quota; boolean packs flip a feature ON for the pack's duration. Both stack onto the plan, but a boolean pack is binary, not additive.

## Where it applies

### Packs survive a plan upgrade — NO state reset

A common merchant question: *"If I upgrade my plan, do I lose the packs I bought?"* — No. The plan upgrade only changes the plan on the merchant's site. Each feature-pack subscription is a SEPARATE subscription row with its own billing cycle and keeps charging independently of the plan.

This means:

- A Starter merchant with a +100 products pack upgrading to Pro KEEPS the pack — they now have 5100 effective products (Pro's 5000 base + pack's 100).
- If the merchant wants to drop the now-redundant pack, they must **manually cancel** it from [[subscriptions]] — the upgrade doesn't do it for them.

This is sometimes a **billing surprise**: merchants who upgrade thinking *"I don't need the pack anymore"* end up paying for both the new plan AND the now-redundant pack until they remember to cancel. Support should proactively prompt upgrading merchants to review active packs (this is also the standing [[plan-vs-feature-pack]] Open Question on cross-tier packs).

### Where the effective quota is consumed

- [[plan-gates]] — the gating engine reads plan base + active packs at lookup time. The lookup is cached for 1 week and flushed on any pack purchase / cancel (see [[plan-vs-feature-pack-lifecycle]]).
- Every Add-button gate across the admin panel (products, customers, blog articles, segments, etc.) reads the same effective figure.

## Related

- [[plan-vs-feature-pack]] — hub.
- [[plans]] — plan catalog; the upgrade path whose base the packs add to.
- [[plan-features]] — the per-feature pack-upsell paywall.
- [[plan-gates]] — gating engine that consumes plan base + pack values.
- [[subscriptions]] — both plan and pack subscriptions appear here as separate rows.

## Open Questions

None.
