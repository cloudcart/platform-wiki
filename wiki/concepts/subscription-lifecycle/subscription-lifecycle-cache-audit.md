---
type: concept
nav_path: "Concept → Subscription lifecycle → Cache, audit & invariants"
aliases: ["Plan feature cache", "Plan feature cache flush", "Subscription transactions audit", "Pricing protection next_billing_amount", "Discount carry-over on renewal", "Next billing date computation", "Owner-only subscription access", "Кеш на план-фийчъри"]
tags: [subscriptions, billing, lifecycle, cache, audit, pricing, discounts, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, cancel, renew, cascades).

# Subscription lifecycle — cache, audit & invariants

## Definition

This aspect covers the **cross-cutting rules** that hold across every state and every transition in the subscription lifecycle: how plan-feature lookups are cached and invalidated, how renewal transactions are recorded as an immutable audit trail, how renewal pricing is protected from accidental edits, how subscription-level discounts carry across renewals, how the next billing date is computed to avoid scheduling charges in the past, and which user roles can even see this surface in the admin panel.

These rules are not specific to any one state — they apply to Active, Past due, Canceled, Expired, and Once subscriptions alike. They are the invariants that keep the lifecycle financially consistent and the merchant's data trustworthy.

## Scope

Covered:

- The 1-week plan-feature cache and its auto-flush on every subscription change.
- The transactions audit trail — every renewal / charge / refund creates an immutable row.
- Pricing protection on `next_billing_amount` — explicitly read-only via the platform API.
- Discount carry-over via `discount_id` at each renewal — automatic, no merchant action.
- The `next_billing_date` computation rule that prevents scheduling charges in the past.
- The owner-only access gate on the subscription surfaces (My subscriptions, billing cards, billing details).

Not covered here:

- The state enum and transitions that this cache flush reacts to — see [[subscription-lifecycle-states]].
- The cascades that consume the up-to-date plan-feature lookup — see [[subscription-lifecycle-cascades]].
- The Renew flow that uses the next-billing-date computation on success — see [[subscription-lifecycle-renew]].

## Contrasts

- **Plan-feature cache vs. plan-gates engine** — the cache is the in-memory speedup for repeated quota lookups; the gates engine is the policy layer that decides whether the merchant can perform an action. See [[plan-gates]] for the gating logic; this page covers only the cache that backs it.
- **`next_billing_amount` (pricing protection) vs. `discount_id` (discount carry-over)** — both shape the amount charged at the next renewal but at different layers. `next_billing_amount` is the final charge value and is locked from API edits; `discount_id` is the linked discount record whose effect is automatically applied on every renewal.
- **Audit trail (transactions) vs. operational state (subscription row)** — the subscription row mutates (status, `failed_attempts`, `next_billing_date` advance). The transactions are immutable history; cancelling a subscription does NOT delete the transaction trail, and invoices stay downloadable forever (see [[subscriptions-transactions]]).
- **Owner-only access vs. staff-accessible features** — the My subscriptions surface ([[subscriptions]], [[subscriptions-detail]], [[billing-cards]], [[details-billing]]) is gated to the store owner only. Staff / moderator accounts do not see the profile-dropdown entry. Most other admin-panel features are accessible to staff per their role permissions; this gate is unique to billing surfaces.

## Where it applies

### Plan-feature cache — 1-week TTL, flushed on subscription change

When the admin panel checks "can the merchant add a 501st product?", the platform looks up the merchant's plan-feature value (e.g., 500 from the plan) plus any active feature-pack subscription values (e.g., +500 from a pack). The result is cached per (feature, plan) pair for **1 week** to make repeated gate checks fast.

When the merchant buys, cancels, or modifies any subscription, the cache for the affected feature(s) is **automatically invalidated** so the new total is effective immediately. This is why a newly-purchased feature pack lifts the merchant's quota right away without a delay. See [[plan-gates]] for the full gating mechanism.

The cache flush also fires during the per-type cascades documented under [[subscription-lifecycle-cascades]] — feature-pack cancellation drops the corresponding pack's quota out of the cached lookup so the lower limit takes effect immediately.

### Audit trail — transactions per renewal

Every renewal / charge / refund creates a transaction row visible in [[subscriptions-transactions]] (or in the expandable row of [[subscriptions]]). Each row records:

- date,
- description,
- amount,
- gateway response (approved / declined),
- the response message for declined attempts,
- and a Download Invoice button for approved transactions.

Transactions are **immutable** — they are a financial audit trail. The merchant can download the invoice for any approved transaction at any time, including for subscriptions that have since been Canceled or Expired. The subscription row may go away from the default Active filter but the transaction history never disappears.

### Pricing protection — `next_billing_amount` is read-only

The platform explicitly rejects any attempt to change the renewal price (the `next_billing_amount` field) via the platform API with the validation error:

> *"Changing the next billing amount is disabled"*

Pricing changes go through the purchase / upgrade flow ([[plans-purchase]] for plans, [[plan-features]] for feature packs), NOT the subscription edit surface. This is what stops a misbehaving integration from accidentally raising or lowering a merchant's renewal cost.

### Discount carry-over on renewals

For subscriptions with a `discount_id` attached (typically a first-cycle promo or a long-term loyalty discount), the discount is automatically carried over at each renewal — **no merchant action needed**. Discounted subscriptions show the discounted `next_billing_amount` in [[subscriptions]] and continue to apply that discount on every renewal until the discount itself is revoked at the source.

A merchant who wants to remove a discount cannot do so via the subscription edit surface (pricing protection — see above). The discount must be removed at its source record; once removed, the next renewal computes `next_billing_amount` without it.

### Next billing date computation

The next billing date is computed as `last_next_billing_date + billing_cycle months`. If the last date was already more than a month in the past (e.g., the subscription was Past due for weeks and the merchant just renewed manually), the platform takes `now + billing_cycle` instead — so renewals never accidentally schedule the next charge in the past.

This rule matters most for late manual Renew — see [[subscription-lifecycle-renew]]. Without it, a subscription that was Past due for 2 months and then Renewed would still be scheduled for the original `next_billing_date` (already weeks in the past), and the next renewal job would immediately try to charge again.

### Owner-only access

The My subscriptions entry in the profile dropdown is gated on the store-owner check — staff / moderator accounts do not see this entry. A staff member who needs to view subscription state must ask the store owner. The same gating applies to [[billing-cards]], [[details-billing]], and [[subscriptions-detail]].

This is the only billing-related gate that is hard-wired to ownership rather than to a role permission — the merchant cannot grant a staff member access to the subscriptions surface even by creating a custom role.

## Related

- [[subscription-lifecycle]] — hub.
- [[subscription-lifecycle-states]] — sibling aspect; the enum whose changes flush this cache.
- [[subscription-lifecycle-cascades]] — sibling aspect; the per-type cascades that consume the up-to-date plan-feature lookup.
- [[subscription-lifecycle-renew]] — sibling aspect; the manual-charge flow that uses the next-billing-date computation on success.
- [[subscriptions]] — the My subscriptions list; owner-only.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail screen; owner-only.
- [[subscriptions-transactions]] — full immutable transaction history per subscription.
- [[plan-gates]] — the gating engine backed by the cached lookup.
- [[plans-purchase]] — the purchase flow where pricing changes actually happen.
- [[plan-features]] — the feature-pack upsell screen where quota changes actually happen.
- [[billing-cards]] — owner-only saved-cards surface.
- [[details-billing]] — owner-only invoicing-details surface.

## Open Questions

None.
