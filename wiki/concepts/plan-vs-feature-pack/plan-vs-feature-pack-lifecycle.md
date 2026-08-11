---
type: concept
nav_path: "Concept → Plan vs. feature pack → Pack lifecycle & billing"
aliases: ["Feature pack lifecycle", "Pack subscription billing", "Pack renewal retry", "Plan-feature cache flush", "Cart reset on pack purchase", "Pack app activation", "Pack billing cycle", "Жизнен цикъл на пакет", "Подновяване на пакет"]
tags: [plans, plan-features, feature-pack, billing, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-vs-feature-pack]]. See the hub for the other aspects (stacking, downgrade, cost heuristic, availability gates).

# Plan vs. feature pack — lifecycle & billing

## Definition

Once purchased, a feature pack becomes a **subscription** on the merchant's account ([[subscriptions]]) and follows the standard [[subscription-lifecycle]] — the same state machine that governs plan subscriptions, with an independent billing cycle. This page covers the pack's billing mechanics: its lifecycle states, the renewal retry loop, the plan-feature cache flush that makes a new pack effective immediately, the cart reset on purchase entry, and the post-purchase app activation that some packs trigger.

## Scope

Covered:

- The pack-as-subscription lifecycle (Active / Past due / Canceled / Expired).
- The renewal retry loop and the daily expiry sweep.
- The 1-week plan-feature cache and its flush on subscription change.
- The cart reset on entering the pack purchase flow.
- The post-purchase underlying-app activation some packs trigger.

Not covered here:

- The effective-quota stacking math — see [[plan-vs-feature-pack-stacking]].
- The over-quota Add-button block after a pack is cancelled — see [[plan-vs-feature-pack-downgrade]].
- Whether a pack is purchasable on the plan at all — see [[plan-vs-feature-pack-availability]].

## Contrasts

- **Plan billing vs. pack billing**: both are subscriptions on the same [[subscription-lifecycle]], but with INDEPENDENT billing cycles — the plan renews on its date, each pack renews on its own. The merchant sees both as separate rows in [[subscriptions]]; cancelling one does not cancel the other. Both are paid by the same saved card ([[billing-cards]]).
- **Feature pack vs. app subscription**: a feature pack adds QUOTA to a feature already on the plan; an app subscription enables entirely new FUNCTIONALITY (Algolia search, AdScout retargeting, BumpCart upsell). Both create subscriptions, but they affect different layers — packs scale an existing capacity, apps add new capabilities. Note the wrinkle below: some packs activate an underlying app as a side effect.

## Where it applies

### Pack lifecycle = standard subscription lifecycle

A pack subscription follows the standard states of [[subscription-lifecycle]]:

- **Active** until renewal fails or the merchant cancels.
- **Past due** on a failed renewal; up to 5 total charge attempts (1 initial + 4 retries spaced 2 / 3 / 4 / 5 days) before the auto-retry loop stops. A Past due pack still contributes to effective quota until the final retry fails.
- **Canceled** → stays usable until `next_billing_date`, then quota drops back to the plan base (triggering the [[plan-vs-feature-pack-downgrade|over-quota block]] if usage now exceeds it).
- **Expired** → terminal state set by the daily `expire:subscriptions` sweep ~1 month past `next_billing_date`; a manual Renew is required to re-activate (firing an immediate fresh charge).

A pre-billing notification fires 7 days before the next billing for Active pack subscriptions, same as for plans.

### Plan-feature cache — 1-week TTL, flushed on subscription change

The platform caches the per-(feature, plan) lookup value for 1 week to speed up repeated gate checks. When the merchant buys, cancels, or modifies a pack subscription, the cache for the affected feature is **automatically invalidated** so the new total is effective immediately. Same on plan upgrade / downgrade. This is why a freshly-purchased pack lifts the quota the moment the purchase completes — the merchant doesn't wait out the TTL.

### Cart is reset on pack purchase entry

Like the plan-purchase flow, clicking *Buy* on a pack row in [[plan-features]] **clears the merchant's checkout cart** first, then seeds it with just that pack. The merchant cannot accumulate multiple packs across multiple clicks — they buy one at a time. To buy *2× +100 products*, the merchant buys *+200 products* (a different pack) or repeats the flow.

### Some packs trigger app activation post-purchase

Some feature-pack mappings have side effects — after the pack subscription is provisioned, the platform activates an underlying app (e.g., the `omniship` app for shipping-payment-sync packs, the `cloudio` app for AI-related packs, the `campaigns` app for messaging packs). The merchant doesn't see this aliasing — they buy the pack, the new capability appears, and the app's subscription handler runs in the background.

## Related

- [[plan-vs-feature-pack]] — hub.
- [[plan-vs-feature-pack-stacking]] — the effective-quota the Active pack contributes to.
- [[plan-vs-feature-pack-downgrade]] — the over-quota block when a pack is cancelled and quota drops.
- [[subscription-lifecycle]] — the shared state machine governing plan + pack subscriptions.
- [[subscriptions]] — both plan and pack subscriptions appear here as separate rows.
- [[plan-features]] — where the pack is bought; the flow that resets the cart.
- [[billing-cards]] — saved card used for plan + pack renewals.

## Open Questions

None.
