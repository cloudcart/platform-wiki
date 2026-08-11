---
type: concept
nav_path: "Concept → Subscriber vs Customer → Plan limits and subscriber cap"
aliases: ["customers plan cap", "subscribers plan cap", "subscribers.max_id", "Subscriber cap chronological", "Over-cap subscribers", "Customer pack subscriber pack"]
tags: [customers, subscribers, marketing, plan-gates, concepts]
plan_gates: [customers, subscribers]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, channels, consent, linkage, privacy, admin surfaces).

# Subscriber vs Customer — plan limits and the subscriber cap

## Definition

The platform enforces **two independent plan caps** that govern the two records separately:

| Plan feature | Caps | Paywall path |
|--------------|------|--------------|
| `customers` | Customer count (registered + guest). | [[customers]] over the cap → 402 paywall to add a customer pack. |
| `subscribers` | Subscriber count. | [[marketing-subscribers]] over the cap → 402 paywall to add a subscriber pack. |

A merchant can hit one cap while still under the other — they are two independent meters with separate paywall paths. The two caps reflect the two different costs the platform incurs: storing customer records (orders, addresses, login) vs reaching a marketing audience (channel rows, segment evaluation, deliverability tracking, campaign-dispatch cost).

The `subscribers` cap has a non-obvious mechanism: **it is chronological, not behavioural.** When the cap is finite, a recurring background job computes a `subscribers.max_id` watermark and segments / campaigns silently exclude any Subscriber with `id > max_id`. The first N chronologically-earliest opt-ins are the eligible ones; newer signups beyond the cap are invisible to sends until the cap is raised or the merchant prunes older subscribers.

## Scope

Covered:

- The independent `customers` vs `subscribers` caps.
- The chronological cap mechanism (`subscribers.max_id`).
- The 10-minute recomputation interval.
- What "over the cap" looks like in the admin panel.
- The paywall paths and customer-pack vs subscriber-pack upsells.

Not covered:

- How Subscribers are created / linked — see [[subscriber-vs-customer-records]] and [[subscriber-vs-customer-linkage]].
- The two-layer consent gate that further filters reach inside the cap — see [[subscriber-vs-customer-consent]].
- Channel-specific deliverability flags — see [[subscriber-vs-customer-channels]].

## Contrasts

- **`customers` plan cap vs `subscribers` plan cap** — separate meters with separate paywalls. Hitting one doesn't block the other.
- **Chronological cap vs random sampling** — the platform favours the earliest opt-ins, not the most engaged ones. A high-engagement recent signup beyond the cap is silently excluded; a long-dormant earliest signup inside the cap is included.
- **"Over the cap" Subscriber visible in the list vs excluded from sends** — over-cap Subscribers ARE shown on [[marketing-subscribers]] (the merchant can see, edit, delete them) but are silently dropped from segments and campaigns.

## Where it applies

### The two caps are independent

The merchant can hit either cap in isolation:

- **Lots of guest orders, no newsletter signups** → Customers grow fast, Subscribers stay flat. The merchant hits the `customers` cap first.
- **Lots of newsletter signups, few buyers** → Subscribers grow fast, Customers stay flat. The merchant hits the `subscribers` cap first.

A store with 10,000 Customers and 1,200 Subscribers and a 1,000-subscriber cap is over the Subscriber cap while well under the Customer cap. Every new newsletter signup goes into "over the cap" territory.

The paywall paths are separate:

- Customer-pack purchase raises the `customers` cap.
- Subscriber-pack purchase raises the `subscribers` cap.

The packs don't substitute for each other — buying more customer slots doesn't free a subscriber slot.

### How the subscriber cap is computed

When the plan's `subscribers` feature is finite, a recurring background job (every **10 minutes** (verify)) does the following:

1. Counts Subscribers, **restricted to channels with `bounced = 0`, `unsubscribed = 0`, `marketing = 1`** — i.e., it counts only the deliverable Subscribers, not the dead-channel ones.
2. Sorts the eligible Subscribers ascending by id.
3. Picks the **Nth** id (N = plan cap).
4. Stores that id as `subscribers.max_id`.

Every segment-eligibility / campaign-eligibility query then includes `WHERE subscribers.id <= max_id`. Subscribers with ids above `max_id` are silently excluded from sends.

The mechanism has several merchant-facing consequences:

- **The chronologically-earliest N opt-ins are the eligible ones.** Newer signups beyond the cap are invisible to segments and campaigns until the cap is raised or the merchant prunes older subscribers.
- **The cap is recomputed every 10 minutes.** Pruning older subscribers frees slots within ~10 minutes; the cap doesn't react instantly.
- **This is NOT random sampling.** The platform favours the earliest contacts even if their engagement is now low.
- **Over-cap Subscribers ARE visible** in the [[marketing-subscribers]] list — they're just silently excluded from sends. The merchant can browse, filter, edit, or delete them; they cannot receive campaigns.
- **Counting excludes dead channels.** A Subscriber whose only Email channel is `bounced = yes` doesn't consume a slot — they're excluded from the cap-eligibility count and so don't push the watermark down. This means the cap reflects "effective reach", not raw row count.

### What "over the cap" feels like to the merchant

- The merchant runs a popup signup form; new signups land successfully as Subscriber rows.
- The merchant builds a segment for "all newsletter subscribers"; the segment count is the count INSIDE the cap, not the total Subscriber rows.
- The merchant runs a campaign; the dispatch reach is the segment count further filtered by the two-layer consent gate (see [[subscriber-vs-customer-consent]]).
- The merchant goes to [[marketing-subscribers]] and sees the total row count including over-cap rows — there's no in-list flag distinguishing "in cap" from "over cap"; the merchant has to count or look at the campaign reach.

### Upgrade path

- [[marketing-subscribers]] over the cap → 402 paywall to add a subscriber pack.
- [[customers]] over the cap → 402 paywall to add a customer pack.

Both paywalls route through the merchant subscription / billing layer ([[merchant-subscription-lifecycle]]); the pack purchase raises the cap immediately (without waiting for the next 10-minute recomputation cycle, though `subscribers.max_id` itself updates on the cycle).

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-consent]] — the gate further filtering reach inside the cap.
- [[subscriber-vs-customer-records]] — what makes a Subscriber row in the first place.
- [[plan-gates]] — the catalogue of plan features including `customers` and `subscribers`.
- [[merchant-subscription-lifecycle]] — billing flow for pack purchases.
- [[marketing-subscribers]] — Subscriber list; over-cap rows show here.
- [[customers]] — Customer list; over-cap shows the paywall on new-customer creation.
- [[marketing-campaigns]] — reach is gated by the cap.
- [[marketing-segments]] — segment evaluation respects `subscribers.max_id`.

## Open Questions

- The recomputation interval is documented as 10 minutes; needs a fresh backend verification of the schedule cadence. (verify)
