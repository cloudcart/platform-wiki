---
type: feature
nav_path: "Plan → Feature → Pack lifecycle"
route_name: plan-feature-packs
route_path: /admin/plan/feature/:id
aliases: ["Plan feature pack lifecycle", "Feature pack subscription", "Cancel feature pack", "Pack survives plan downgrade", "Pack model_type subscription", "App-activation mapping alias", "Жизнен цикъл на пакет"]
tags: [plans, plan-feature, feature-pack, subscription, lifecycle, vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-feature]]. See the hub for the other aspects (pack list, buy → checkout flow, plan restrictions).

# Plan feature — pack lifecycle

## Purpose

A purchased feature pack is its own [[subscriptions|subscription]] with its own billing cycle, independent of the merchant's plan-tier subscription. This aspect covers what happens to that pack **over time**: how the subscription is created, what cancelling it does, why it survives a plan-tier downgrade, and the internal mapping aliases that trigger app activation after purchase.

## Where to find it

- The pack is **bought** on the `/admin/plan/feature/{id}` screen (see [[plan-feature-detail-buy-flow]]).
- The resulting subscription is **viewed and cancelled** from [[subscriptions]] — not from the *Plan feature* screen itself.
- For a boolean feature, once a pack is active the card on [[plan-features]] shows a *Cancel* link (routing to [[subscriptions]] filtered to that pack) instead of *Buy*.

## What the merchant can do here

- **See the active pack as a subscription** in [[subscriptions]], with its own next-billing date.
- **Cancel an active pack** from [[subscriptions]] — it stays active until its `next_billing_date`, then the effective quota drops back to the base plan value.
- **Keep packs through a plan-tier change** — downgrading the plan does not auto-cancel active packs.

## What the merchant cannot do here

- **Cancel a pack from the *Plan feature* screen** — cancellation lives on [[subscriptions]].
- **Reclaim over-quota records automatically after cancel** — existing over-quota records are preserved, not deleted; new creates are blocked by the standard gate until the merchant trims excess or re-buys.

## Settings & fields

No editable fields on this surface — pack lifecycle is driven by subscription state. The merchant reads:

| Field shown (in [[subscriptions]]) | What it represents |
|------------------------------------|--------------------|
| **Pack subscription row** | One row per active feature pack |
| **Next billing date** | When the pack renews (or when cancellation takes effect) |
| **Cancel link** | Schedules cancellation at the next billing date |

## Business rules

### Pack `model_type` drives subscription creation

Each pack has a `model_type` (e.g. `cloudcart_feature`). On successful payment, a new subscription is created with that `model_type` and the pack's `value` as the quota contribution. The checkout seeds the cart with `{ type: pack.model_type, mapping: pack.id }` — see [[plan-feature-detail-buy-flow]].

### Cancel-pack flow — existing records preserved

Cancelling an active pack (from [[subscriptions]]) takes effect at the pack's `next_billing_date`. After cancellation:
- The merchant's effective quota drops back to the base plan value.
- Existing over-quota records are **preserved** (not deleted).
- New creates are blocked by the standard plan gate until the merchant deletes excess records or re-buys the pack.

### Plan-tier downgrade — packs survive

Pack subscriptions are independent of the plan-tier subscription. Downgrading the plan does **not** auto-cancel active packs — they keep renewing on their own cycle until the merchant cancels them. During the overlap, the effective limit = `new_plan_base + sum(pack_values)`.

### Mapping translation for app activation

Some pack mappings are aliased to app keys for post-subscription hooks, so the right app's subscription handler runs after purchase:
- `shipping_payment_sync` → `omniship`
- `cloudio_ai` → `cloudio`
- `campaign.channels.messenger_message`, `campaign.channels.email`, `viber_messages` → `campaigns`

This rewrite is internal — the merchant doesn't see it. The URL and pack row use the public mapping; the alias only matters server-side.

### Boolean features: *Active* once a pack subscription exists

For boolean features (e.g. `discount-code-pro`, `support_meetings`, `authorize_payment`), the feature reads *Disabled* until an active pack subscription exists, then *Active*. The state is computed live from active-subscription presence — there's no stored enable flag the merchant flips. Cancelling the pack flips it back to *Disabled* at the next billing date.

## Related

- [[plan-feature]] — hub.
- [[plan-feature-detail-buy-flow]] — how the subscription is created on purchase.
- [[plan-feature-detail-pack-list]] — where boolean *Active* / *Disabled* state is rendered per row.
- [[subscriptions]] — where pack subscriptions appear and are cancelled.
- [[merchant-subscription-lifecycle]] — the broader subscription state machine packs participate in.
- [[plan-gates]] — the gate that re-applies the base limit after cancellation.
- [[expired-subscription]] — when a pack subscription's payment fails.

## Open questions

None.
