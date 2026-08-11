---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Feature packs (stacking on plan)"
aliases: ["Feature pack flow", "Subscription feature packs", "Buy feature pack", "Plan feature pack", "Feature pack stacking", "Plan vs feature pack", "+100 products pack", "+5 GB storage pack"]
tags: [billing, subscription, plan, feature-packs, lifecycle, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, expiration, cancellation, payment methods, invoices, support flow).

# Subscription feature packs

## Definition

A **feature pack** is a paid recurring add-on that adds quota to **ONE specific feature** on the merchant's current plan — e.g., *+100 products*, *+1000 customers*, *+5 GB storage*, *+1 support meeting*. Boolean packs flip a feature ON (e.g., *Custom hostname*). Packs are purchased from [[plan-feature]] (the per-feature buy panel) reached via [[plan-features]] (the card grid) at `/admin/plan-features`, OR via an automatic redirect when the merchant hits a feature limit.

Packs **STACK on top of the plan base** and **survive plan upgrades / downgrades** — they continue billing on their own cycle until the merchant explicitly cancels them from [[subscriptions]].

## Scope

What this page covers:

- The merchant-facing buy flow for feature packs (entry points + checkout).
- The per-feature URL pattern + the seeded-cart behaviour.
- Edge cases: plan-tier requirement, packs disabled on plan, hard ceiling (`max_value`).
- Stacking with the plan base + survival across plan switches.
- Pack-specific cancellation behaviour at `next_billing_date`.

What it does NOT cover:

- The decision logic *"recommend a pack or recommend a plan upgrade?"* — see [[plan-vs-feature-pack]].
- The plan-gate engine that enforces the feature limit in the first place — see [[plan-gates]].
- The Plan-Feature entity catalog — see [[plan-feature]] (entity-style page).
- The Plan / Tier upgrade flow itself — see [[plans-purchase]] + [[subscription-renewal-retry]] (renewal at higher cycle).

## Contrasts

- **Plan upgrade vs feature pack purchase** — a plan upgrade moves the merchant to a higher tier and unlocks MANY features. A feature pack adds quota to ONE feature on the current tier. Both create subscriptions but with different `model_type` (`plan_details` vs `cloudcart_feature`) and different cancellation effects. See [[plan-vs-feature-pack]] for the recommendation logic.
- **Feature pack vs paid app** — feature packs add quota to a built-in CloudCart feature. Paid apps enable entirely new functionality not present on the plan at all (e.g., Algolia search). Both stack on the plan; both share the same subscription lifecycle.
- **Sidebar entry vs paywall redirect** — there is NO sidebar entry that opens [[plan-feature]] directly. The merchant either browses the [[plan-features]] card grid OR gets redirected on a paywall hit (HTTP 402) from an over-limit action.
- **Pack cancellation vs plan downgrade** — cancelling a pack drops the pack's added quota at `next_billing_date`. Downgrading the plan drops the plan's base quota at `next_billing_date`. Existing rows are preserved in both cases; only new creates are blocked.

## Where it applies

### Entry points to the buy flow

A merchant lands on the per-feature buy panel via one of three paths:

- **Automatic redirect on paywall hit** — trying to add a 501st product on a 500-product Starter plan returns HTTP 402 with `{message: "You reached the limit of feature **Products - 500**", info.key: "products", info.name: "Products", type: "feature"}`. The frontend renders a paywall modal that links to `/admin/plan/feature/products`.
- **Warning banner / inline link** — e.g., the orders-counters banner's *"Upgrade your quota from here"* link.
- **Plan-area Feature packages tab** ([[plan-features]]) at `/admin/plan-features` — a card grid with per-feature usage bars + a *Buy feature* / *Upgrade* button per card.

### The per-feature URL pattern

The per-feature pack-buy panel lives at `/admin/plan/feature/{feature-mapping}`. Concrete examples:

- `/admin/plan/feature/products`
- `/admin/plan/feature/customers`
- `/admin/plan/feature/storage`
- `/admin/plan/feature/support_meetings`
- `/admin/plan/feature/custom_hostname` (boolean pack)

The full screen documentation is on [[plan-feature]] (per-feature buy panel) + [[plan-features]] (card grid).

### The buy flow

1. The merchant lands on the per-feature panel for the feature they hit (e.g., Products).
2. A table lists available packs for that feature: *Pack name* (e.g., *+100 products*; for dynamic-pricing features it includes the chosen quantity like *2000 products*) + *Price* (e.g., *10.00 EUR / month*) + a **Buy feature** button per row.
3. Clicking *Buy feature* opens the same Checkout side panel as the plan-purchase flow. **The cart is SEEDED FRESH** — any prior cart contents are cleared first so the merchant can't accidentally combine multiple packs across multiple clicks.
4. The merchant completes the standard checkout: invoice details ([[billing-invoicing]]) AND a card on file ([[billing-cards]]) are required. Missing either piece returns HTTP 422 with *"Please, enter your invoice details"* or *"Please, add payment method"*.
5. On success, the parent feature card's quota updates IN PLACE (no refetch needed) — the merchant sees the new effective limit immediately. The plan-feature cache is also flushed server-side.

### Edge cases that block the buy flow

- **Feature requires a higher plan tier entirely** (e.g., `custom_hostname` requires Pro or Unicorn) — the pack table is replaced by a banner: *"This feature is not enabled for your plan. To access it, please upgrade your plan." / "Plans that support this functionality are: **Pro**, **Unicorn**"*. The merchant must upgrade their plan first.
- **Packs disabled on the merchant's current plan** (`enable_feature_pack = 0` on the plan-feature mapping) — the panel auto-closes and the plans-upgrade modal opens with the note *"No feature pack available, you can upgrade your plan."*.
- **Buying the pack would push quota above the feature's hard ceiling** (`max_value`, e.g., 100000 products) — the cart-add is rejected inline: *"Your package allows 100000 products"*. The merchant must upgrade the plan instead.

### Stacking with the plan base

The merchant's effective limit for a feature is `plan_base + sum(active_pack_quotas)`. A Starter merchant with a +100 products pack has an effective limit of `500 (Starter base) + 100 (pack) = 600 products`. Buying a second pack stacks again: `500 + 100 + 100 = 700`.

This is computed server-side and cached in the plan-feature cache; the cache is flushed on every subscription state change (renewal success, cancel, expire, plan switch).

### Pack survival across plan switches

Existing feature packs **survive plan upgrades AND downgrades** — they continue billing on their own cycle until the merchant cancels them explicitly. A Starter merchant with a +100 products pack who upgrades to Pro keeps the pack: effective products = `5000 (Pro base) + 100 (pack) = 5100`. To drop a now-redundant pack, the merchant must manually cancel it from [[subscriptions]]. See [[subscription-cancellation]] for the cancel behaviour.

Downgrade preserves data but blocks new creates above the new effective limit — see [[plan-vs-feature-pack]] for the recovery options.

### Pack-specific Cancel effect

Cancelling a feature pack (from [[subscriptions]]) flips its status to Canceled immediately. Until `next_billing_date`, the pack's quota STAYS in the effective limit. After `next_billing_date` (next-day expiry, no 1-month grace — see [[subscription-expiration]]), the pack's quota drops out of the lookup:

- Existing rows ABOVE the new effective limit stay editable.
- New creates are blocked by the standard plan gate as soon as the merchant is over the limit.
- Recovery: (1) buy the pack again, or (2) prune existing data until under the new effective limit, or (3) upgrade the plan to absorb the quota.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[plan-vs-feature-pack]] — when to recommend a pack vs a plan upgrade.
- [[plan-gates]] — the engine that enforces the per-feature limit.
- [[plan-features]] — the card grid screen at `/admin/plan-features`.
- [[plan-feature]] — the per-feature pack-buy panel + entity catalog.
- [[plans]] — plan catalog (the alternative to buying a pack).
- [[plans-purchase]] — full plan-purchase flow.
- [[billing-invoicing]] / [[billing-cards]] — prerequisites at checkout time.
- [[subscriptions]] — where to see / cancel an active pack.
- [[subscription-cancellation]] — the soft-cancel behaviour.
- [[subscription-renewal-retry]] — packs renew on the same daily pipeline as plans.

## Open Questions

None.
