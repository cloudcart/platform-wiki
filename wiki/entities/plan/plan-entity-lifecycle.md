---
type: entity
nav_path: "Entity → Plan → Lifecycle"
aliases: ["Plan lifecycle", "Plan switching", "Plan upgrade downgrade", "Plan renewal", "Plan cancel", "Plan expire", "One active plan"]
tags: [entity, billing, plans, lifecycle, subscription]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (catalog structure, billing cycles, feature restrictions, free-plan expiry + demo, LTA + partner overrides).

# Plan — Lifecycle

## Identity

The lifecycle of a [[plan|Plan]] has two distinct axes:

1. **Catalog lifecycle** — how a plan record moves through CloudCart staff's catalog management (catalog-defined → active → soft-disabled → hidden). Merchants never see this directly; they only see whether the plan appears on [[plans]].
2. **Merchant subscription lifecycle** — how a specific merchant moves between plans (purchase → renew → cancel → expire → downgrade → LTA migration). This is the lifecycle a support agent asks about most often.

The shared "exactly ONE active Plan at a time" rule means switching Plans is replacement, not addition. The detailed state machine for the underlying subscription record is on [[subscription-lifecycle]]; this page documents the Plan-level lifecycle events.

## Aliases

- **Plan switching** — generic merchant term for changing tier.
- **Upgrade** / **Downgrade** — directional plan switch (higher-priced / lower-priced).
- **Plan renewal** — auto-charge at the cycle anniversary.
- **Plan cancel** — auto-renewal off, stays usable until cycle end.
- **Plan expire** — final state after exhausted retries.

## Key Attributes

The Plan record itself does not carry per-merchant lifecycle state — that lives on the [[subscription-lifecycle|subscription record]]. The Plan-level lifecycle data this page covers:

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Active in catalog** | yes / no | Catalog-level published flag — when no, the plan is filtered out of [[plans]] entirely. See [[plan-entity-catalog-structure]]. |
| **All price variants active** | yes / no (derived) | When CloudCart deactivates every price-detail variant, the plan disappears from the catalog while existing subscribers continue. See [[plan-entity-billing-cycles]]. |

## Business rules

### The merchant has exactly ONE active Plan at any time

The [[site|Site]] carries one active plan-mapping. Every gate check resolves against that mapping. The merchant cannot be on two plans simultaneously — they can only have ONE plan-type subscription Active at a time. Switching plans replaces the old subscription with a new one (typically pro-rated at the purchase moment).

### Catalog lifecycle states

1. **Catalog-defined** — CloudCart staff adds the plan to the catalog with a mapping, name, type, issuer-company binding, billing-cycle variants, and feature restriction values. Not editable by merchants.
2. **Active in catalog** — visible to matching merchants on [[plans]] (with at least one active price-detail variant). Merchants can purchase it via [[plans-purchase]].
3. **Soft-disabled** — CloudCart deactivates all price-detail variants. The plan record stays but it disappears from the [[plans]] catalog. Existing subscribers continue on the plan until they switch.
4. **Hidden** — `Active in catalog = no`. The plan is filtered out of [[plans]] entirely. Existing subscribers may still be on it (no auto-migration); new sign-ups can't pick it.

### Merchant lifecycle events

From the merchant's perspective, the Plan they're on goes through these events via the underlying [[subscription-lifecycle]]:

- **Purchase** — the merchant clicks **Upgrade now** on a plan card on [[plans]], picks a billing cycle on [[plans-purchase]], pays through admin checkout. A new plan-type subscription is created with status `Active` and the merchant's [[site|Site]] is bound to the new Plan mapping.
- **Renew** — at `next_billing_date`, the subscription's saved card is charged; on success, the subscription stays Active for another cycle. On failure, status → `Past due`; the platform retries (5 attempts with 2/3/4/5/5-day spacing) per [[subscription-lifecycle]].
- **Cancel** — the merchant clicks Cancel; the subscription's auto-renewal stops but the Plan remains usable until `next_billing_date`.
- **Expire** — 5 consecutive renewal failures exhausts retries; status → `Expired`. (For the free *Start Up* plan, auto-expiry also fires on inactivity — see [[plan-entity-free-expiry-and-demo]].) The merchant is redirected to [[expired-subscription]] until they switch to a paid plan or log in.
- **Downgrade** — the merchant picks a lower plan on [[plans]] → new subscription replaces the old; over-quota data (excess products / customers / etc.) is not auto-deleted but new additions are gated by the new lower caps (see the "preserved on downgrade" rule below).
- **LTA migration** — see [[plan-entity-overrides-lta-and-partner]].

### Existing data is preserved on downgrade

The [[plans]] catalog does NOT visually distinguish upgrades from downgrades — every card shows *Upgrade now* regardless of relative price. Merchants can downgrade, but over-quota data (products / customers above the lower cap) is **preserved** — new additions are gated by the new lower cap, but existing rows stay intact. To recover headroom, the merchant either prunes data or buys a feature pack to top up.

The [[plan-gates]] engine implements this as a soft-block: existing records are not deleted, hidden, or warned-against on their own. The next *new* record write at the cap point gets the *"Plan limit reached"* paywall. Common gates that behave this way: `products`, `customers`, `categories`, `staff_members`, `segments`.

### Renew vs cancel are independent of catalog state

A merchant on a soft-disabled plan continues to renew normally. Soft-disable only affects new sign-ups (the plan is hidden from [[plans]]); the existing subscription's recurring charge fires on its cycle anniversary regardless. The plan record + plan-feature restrictions stay intact for the duration of the subscription.

### Switching cycles is also a plan switch

Changing from monthly → yearly on the same Plan is implemented as a replacement subscription — the old subscription is cancelled and a new one created with the new cycle. The Plan record itself is unchanged; the change is in the subscription's chosen variant. Pro-ration handles the partial cycle on the old subscription.

## Where it appears

- [[plans]] — the merchant clicks *Upgrade now* on any card to enter purchase / switch flow.
- [[plans-purchase]] — pro-rated purchase summary on switch; renewal-detail confirmation.
- [[subscriptions]] / [[subscriptions-detail]] / [[subscription-details]] — current Plan subscription with its lifecycle status (Active / Past due / Cancelled / Expired).
- [[subscriptions-transactions]] — per-charge log including renewal attempts.
- [[expired-subscription]] — the takeover screen on Expired status.
- Profile dropdown → Plan badge — shows current Plan + lifecycle hint.

## Related

- [[plan]] — hub.
- [[subscription-lifecycle]] — the underlying state machine (Active / Past due / Cancelled / Expired + retry schedule).
- [[merchant-subscription-lifecycle]] — merchant-question hub answering *"how do I upgrade / cancel / switch plan / what happens at expiry"*.
- [[plans]] — catalog screen.
- [[plans-purchase]] — purchase / switch flow.
- [[plan-gates]] — soft-block behaviour on downgrades.
- [[plan-vs-feature-pack]] — when to upgrade vs. buy a pack instead of downgrading + repurchasing.
- [[expired-subscription]] — takeover after final expiry.

## Open Questions

- Whether downgrade pro-ration credits the unused portion of the previous Plan's cycle in full or partially (verify against [[plans-purchase]]'s pro-ration logic).
