---
type: concept
nav_path: "Concept → Plan vs. feature pack → Downgrade & over-quota"
aliases: ["Plan downgrade over quota", "Add button blocked", "Over quota after downgrade", "Pack cancellation effect", "Prune or buy pack", "Downgrade blocking", "Блокиран бутон Добави", "Надхвърлен лимит при понижаване"]
tags: [plans, plan-features, feature-pack, billing, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-vs-feature-pack]]. See the hub for the other aspects (stacking, cost heuristic, availability gates, pack lifecycle).

# Plan vs. feature pack — downgrade & over-quota

## Definition

When a merchant's effective quota **drops below their current usage** — either by downgrading the plan to a lower base, or by cancelling a feature pack that was propping the quota up — CloudCart does **not delete data**. Existing rows stay and remain fully accessible (read + edit). What the platform blocks is **new creates**: the relevant Add button is disabled and the merchant is sent to the paywall until they get back under the limit.

The gating engine enforces the rule at gate-check time only — it is reactive, never destructive. The merchant always keeps read-only access to everything they already created; the only restriction is "you can't add MORE".

## Scope

Covered:

- Plan-downgrade behaviour when usage exceeds the lower base.
- Pack-cancellation behaviour with the same over-quota effect.
- The merchant's two remedies: prune or buy a pack.
- The paywall message string and the no-data-loss guarantee.

Not covered here:

- The additive stacking formula itself — see [[plan-vs-feature-pack-stacking]].
- Choosing prune vs. pack vs. upgrade on cost grounds — see [[plan-vs-feature-pack-cost-heuristic]].
- Whether a remedy pack is even available on the new (lower) plan — see [[plan-vs-feature-pack-availability]].
- The pack subscription's cancellation timeline (usable until `next_billing_date`) — see [[plan-vs-feature-pack-lifecycle]].

## Contrasts

- **Plan downgrade vs. pack cancellation**: downgrade moves the merchant to a lower plan with lower base quotas; pack cancellation reduces the merchant's effective quota by the pack's contribution at the next pack billing date. Both can leave the merchant over quota with the SAME downstream effect on Add buttons. The difference is **what got cheaper**: downgrade reduces the plan's recurring cost; pack cancel reduces only the pack's recurring cost.
- **Over-quota block vs. data deletion**: the platform never deletes to fit a smaller plan. Over-quota means "no new creates", not "we trimmed your catalog".

## Where it applies

### Plan downgrade — blocks new Add buttons over quota

If a merchant on Pro (5000 products) holding 800 products downgrades to Starter (500 products), the existing 800 products **stay**. But:

- The Add Product button is blocked (the merchant is already over the Starter base of 500).
- The merchant gets a paywall message: *"You reached the limit of feature **Products - 500**."*
- The merchant must either:
  1. **Prune** — delete products until they're under the new base.
  2. **Buy a pack** — purchase a +500 pack to bring effective quota back up (subject to [[plan-vs-feature-pack-availability]] — the new plan must allow the pack).

### Pack cancellation — same over-quota pattern

The same pattern applies when a feature-pack subscription is cancelled and the merchant's row count is now over the plan's base: existing rows stay, new creates are blocked. The drop takes effect at the pack's `next_billing_date`, not immediately on clicking Cancel (the pack stays usable until then — see [[plan-vs-feature-pack-lifecycle]]).

### Cross-tier active packs after downgrade

Feature packs are tied to the merchant's subscription, not to the plan tier. If the merchant downgrades to a tier where a specific pack is not normally purchasable, the pack **continues to bill** until cancelled explicitly — the platform does not auto-cancel. Merchants downgrading should review their active feature-pack subscriptions ([[subscriptions]]) and cancel any that no longer make sense on the new tier. This is the standing Open Question carried on the [[plan-vs-feature-pack]] hub.

## Related

- [[plan-vs-feature-pack]] — hub.
- [[plan-vs-feature-pack-stacking]] — the effective-quota formula whose drop triggers the block.
- [[plans]] — plan catalog; downgrade target.
- [[plan-features]] — per-feature paywall the merchant is sent to when over quota.
- [[plan-gates]] — gating engine enforcing the block at gate-check time.
- [[subscriptions]] — where the merchant cancels a pack subscription.

## Open Questions

None.
