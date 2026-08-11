---
type: feature
nav_path: "Plan → Feature pack → Subscription lifecycle"
route_name: admin.plan.feature
route_path: /admin/plan/feature/{mapping}
aliases: ["Pack subscription provisioning", "Pack cancel lifecycle", "Pack downgrade lifecycle", "Plan-feature cache", "next_billing_date", "Cancelled-but-paid pack"]
tags: [plans, plan-feature, feature-pack, subscription, billing, cache, lifecycle]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (warning banners, pack list, purchase flow, restrictions & limits, modern Vue grid, middleware mappings).

# Plan features — subscription lifecycle

## Purpose

A successful feature-pack checkout doesn't deliver a one-shot perk — it **creates a subscription** on the merchant's account that adds its quota to the plan's base quota for the lifetime of the subscription. This page covers the lifecycle of that subscription: provisioning at checkout-success, the 1-week feature-value cache flush, what happens on cancel / downgrade / re-buy, and the "paid until next_billing_date" semantics that govern when quota actually drops off.

## Where to find it

- Triggered automatically when the merchant completes checkout from [[plan-features-purchase-flow]].
- Visible to the merchant on [[subscriptions]] (the active-subscriptions list).
- Surfaced on [[expired-subscription]] when a pack's payment fails.

## What the merchant can do here

- View their purchased packs as active subscriptions on [[subscriptions]].
- Cancel a pack from there (the cancellation takes effect at the next billing date).
- See the pack's contribution to their effective quota immediately on every admin screen after a successful purchase (no refresh needed).

## Settings & fields

### Post-purchase provisioning steps

| Step | What happens |
|------|--------------|
| 1 | New subscription record created on the merchant's account (`model_type = cloudcart_feature`) |
| 2 | Plan-feature cache flushed — the new total quota becomes effective immediately |
| 3 | For some packs, a post-subscription hook activates the underlying app subscription (e.g. `omniship`, `cloudio`, `campaigns` — see [[plan-features-middleware-mappings]]) |
| 4 | Merchant returns from `/admin/checkout` to the admin panel with the new quota available |

### Feature-value cache parameters (verify)

| Parameter | Value |
|-----------|-------|
| **TTL** | 1 week |
| **Cache key shape** | per (feature, plan) pair |
| **Cache tag** | `plan` |
| **Flush trigger** | Pack purchase / cancellation (per-feature flush) + plan / subscription changes (full `plan` tag flush) |
| **`null` sentinel** | `'@@@'` (see [[plan-features-restrictions-limits]]) |

### Subscription "paid" status enum values

A pack subscription counts toward quota when its status is one of:

- Any status **NOT** in `EXPIRED` or `CANCELED`, OR
- Status `CANCELED` **BUT** `next_billing_date` is still in the future.

This means: a cancelled pack still contributes quota until its original `next_billing_date` passes.

## Business rules

### Pack purchase creates a subscription, not a one-shot

When the merchant completes checkout, the pack becomes a **subscription** on the merchant's account ([[subscriptions]]) with its own billing cycle (monthly / yearly / once depending on the pack). The pack's quota is **added to the plan's base quota** at gate-check time. Cancelling the subscription removes the added quota at the next billing cycle (not immediately — see below).

### Feature-value lookup adds active subscriptions to plan value

When the admin panel checks "can the merchant add a 501st product?", the platform looks up the plan's base value (e.g. 500), then queries active subscriptions for the *products* feature and adds their values (e.g. +500 from a pack). So buying a +500 pack effectively means the merchant's *products* gate is now 1000 — until the subscription ends.

### Plan-feature value cache is per-feature

The computed plan-feature value is cached for **1 week** per (feature, plan) pair, tagged `plan`. When the merchant buys a pack, the cache for that feature is invalidated so the new total is effective immediately. See [[plan-gates]] for the broader cache lifecycle.

### Cancelling a pack — existing records preserved, new creates blocked

When the merchant cancels a pack subscription from [[subscriptions]]:

1. The cancellation takes effect at the pack's **`next_billing_date`** (consistent with all subscriptions).
2. After that date the platform recomputes the merchant's effective quota DOWN to the base plan limit (the pack's contribution drops off).
3. Existing over-quota records ARE preserved on disk — products / customers / campaigns the merchant created while the pack was Active stay visible.
4. New creates / edits are blocked by the standard plan gate from that point on, until the merchant either deletes excess records to get back under the limit, or re-buys the pack.

A merchant who panics about "if I cancel my +1000 pack do I lose products?" can be reassured: **nothing is deleted, only blocked**.

### Subscription "paid" state spans cancelled-but-not-yet-expired

Critical for pack-cancellation UX: a pack subscription is considered "paid" (and its quota counted) as long as either:

- Its status is NOT in `EXPIRED` or `CANCELED`, **OR**
- Its status is `CANCELED` BUT `next_billing_date` is still in the future.

After cancelling a pack, the merchant retains its quota until the original `next_billing_date` passes — they don't lose access mid-cycle. Only after that date does the quota drop off and the pack stops counting in [[plan-gates]] enforcement.

### Plan-tier downgrade — packs survive the downgrade

Pack subscriptions are **independent** of the plan-tier subscription. If a merchant on Pro buys a +1000 pack and later downgrades to Starter:

- The +1000 pack stays Active until its own next_billing_date (it's NOT auto-cancelled with the plan change).
- Effective limit during this period: `starter_base + pack_value`. So if the Starter base is 500 products and the pack is +1000, the merchant has 1500 products available.
- When the pack eventually expires (or the merchant cancels it), the limit drops to the Starter base.

The pack continues to renew on its own cycle until the merchant cancels it explicitly — so a merchant who wants to "fully downgrade" should also cancel any active packs from [[subscriptions]].

### Boolean-feature packs — Active subscription = feature enabled

For boolean features (e.g. `discount-code-pro`, `support_meetings`), the limit warning displays the literal text **Disabled** when the merchant doesn't have the feature (see [[plan-features-warning-banners]]). Buying the corresponding pack creates an Active subscription, after which the feature check returns true (feature enabled — buttons / screens appear). Cancelling the pack reverts the feature to false at `next_billing_date`. The "enabled / disabled" state is computed live from the **active-subscription presence** — there is no separate `enabled` toggle the merchant can flip independently.

### Post-purchase cache flush propagates immediately

The Plan area cache for the purchased feature is flushed server-side at purchase time — so any other admin screen the merchant navigates to picks up the new effective quota immediately, **no refresh needed**. The modern Vue grid at [[plan-features-modern-vue-grid]] additionally updates its own in-memory card state without a refetch.

### Bank-transfer unpaid invoices grace period varies by reseller (verify)

For sites that pay via bank transfer:

- **Standard merchants**: 30 days grace on UNPAID bank invoices.
- **Reseller-onboarded merchants** (`reseller_id` set): 90 days grace.

The effect on packs: an unpaid bank-transfer invoice past the threshold surfaces as a warning banner or access restriction — eventually the pack subscription transitions to `EXPIRED` if not paid. See [[plan-features-restrictions-limits]] for the threshold values.

## Related

- [[plan-features]] — hub.
- [[plan-features-purchase-flow]] — the checkout flow this lifecycle picks up after.
- [[plan-features-modern-vue-grid]] — in-place card update after success.
- [[plan-features-middleware-mappings]] — pack → app activation hooks (`omniship`, `cloudio`, `campaigns`).
- [[plan-features-restrictions-limits]] — the 1-week feature-value cache + bank-transfer grace.
- [[subscriptions]] — where purchased packs appear; the merchant cancels from there.
- [[expired-subscription]] — when a pack-subscription's payment fails.
- [[merchant-subscription-lifecycle]] — broader merchant-question hub.
- [[plan-gates]] — gating concept.

## Open questions

None.
