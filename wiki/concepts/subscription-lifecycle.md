---
type: concept
nav_path: "Concept → Subscription lifecycle"
route_name: ""
route_path: ""
aliases: ["Subscription lifecycle", "Subscription state machine", "Subscription renewal", "Subscription cancel", "Subscription expiry", "Subscription billing cycle", "Renewal retry schedule", "Past due lifecycle", "Жизнен цикъл на абонамент", "Подновяване на абонамент", "Просрочен абонамент"]
tags: [subscriptions, billing, lifecycle, plans, feature-packs, apps, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Subscription lifecycle

## Definition

The **subscription lifecycle** is the shared state machine every paid recurring item on the merchant's CloudCart account goes through — from creation at purchase, through periodic renewals, retries on failure, and eventual cancellation or expiry. The same five-state lifecycle (`Active`, `Past due`, `Canceled`, `Expired`, plus the one-time `Once` variant) and the same retry / pre-notification / cancel-cascade rules apply to every subscription type the merchant can own:

- **Plan** subscription — the store tier (Free / Starter / Pro / Business / Enterprise). One per store; cancellation expires the entire store.
- **Feature-pack** subscription — extra quotas (extra products, customers, storage, etc.) on top of the plan.
- **App** subscription — paid apps (Algolia, AdScout, BumpCart, etc.).
- **Service** subscription — Expert Services / agency add-ons (one-time or recurring).
- **Theme** subscription — paid templates.

This is why [[subscriptions]] surfaces all five types in one list with one set of column semantics — they are variants of the same underlying lifecycle. When a merchant asks "what happens if my card fails?", "can I get a refund if I cancel?", "how do I reactivate?", or "why is my subscription Past due?", the answer derives from this lifecycle.

> Critical rule, repeated often as the single most-misunderstood point: **Cancel is soft.** Clicking Cancel sets `status = Canceled` but does NOT cut off the service. The merchant keeps using the subscription until `next_billing_date` passes. No proration, no partial refund. See [[subscription-lifecycle-cancel]].

## Sub-pages (in this cluster)

This concept is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscription-lifecycle-states]] — the four-state status enum (`Active`, `Past due`, `Canceled`, `Expired`) + the one-time `Once` variant; the full transition matrix and what triggers each move.
- [[subscription-lifecycle-renewal-retry]] — the 5-attempt retry schedule with 2 / 3 / 4 / 5-day backoff; the daily renewal job; the daily expire sweep; the 7-day pre-billing notification.
- [[subscription-lifecycle-cancel]] — soft-cancel semantics; LTA-contract block; unpaid-turnover block; the `canActivate` free-reactivation rule.
- [[subscription-lifecycle-renew]] — Renew button immediate-charge flow; plan-deprecation redirect; app re-install on successful late renew; feature-pack quota re-apply.
- [[subscription-lifecycle-cascades]] — per-type side effects when a subscription cancels or expires (plan / feature-pack / app / service / theme); per-channel reputation impact on paid marketing channels.
- [[subscription-lifecycle-cache-audit]] — the 1-week plan-feature cache + auto-flush on subscription change; transactions audit trail; pricing protection on `next_billing_amount`; discount carry-over; next-billing-date computation; owner-only access gate.

## Scope

What this hub covers:

- The five subscription types and the fact that they share one lifecycle.
- A short orientation to the state machine and the critical "Cancel is soft" rule.
- Cross-references into the aspect pages that hold the operational detail.

What it does NOT cover (each aspect owns its own slice):

- The full UI of the My subscriptions list — see [[subscriptions]].
- The per-subscription detail screen — see [[subscriptions-detail]] / [[subscription-details]].
- The exact catalog of which feature packs exist — see [[plan-features]].
- The plan purchase flow that creates a subscription in the first place — see [[plans-purchase]].
- The billing / invoicing surface — see [[details-billing]].
- The merchant's saved cards used at renewal time — see [[billing-cards]].
- The plan-gating concept itself — see [[plan-gates]] and [[plan-vs-feature-pack]].

## Contrasts

- **Subscription lifecycle vs. order lifecycle** — subscriptions are recurring merchant-to-CloudCart billing; orders are one-time customer-to-merchant purchases. Entirely different state machines. The order lifecycle is [[order-status-workflow]]; this hub covers the subscription lifecycle.
- **Plan subscription vs. feature-pack subscription** — a plan subscription is the store tier (one per store; cancellation expires the entire store). A feature-pack subscription is an add-on quota for ONE specific feature; cancelling shrinks that quota at next billing only. See [[plan-vs-feature-pack]].
- **Cancel vs. Expire** — Cancel is a deliberate merchant action; Expire is the platform's terminal state after the auto-retry loop exhausts and the daily sweep flips the subscription. See [[subscription-lifecycle-states]].
- **Past due vs. Expired** — Past due means "auto-retry loop still in scope"; Expired is terminal. See [[subscription-lifecycle-states]] for the full distinction.
- **Renew (paid) vs. canActivate (free reactivation)** — Renew normally fires an immediate fresh charge; the canActivate exception flips a Canceled subscription back to Active for free when there is paid time remaining. See [[subscription-lifecycle-cancel]] and [[subscription-lifecycle-renew]].
- **LTA contract subscription vs. standard subscription** — LTA subscriptions cannot be cancelled or renewed from the merchant UI; the account manager owns the lifecycle. See [[subscription-lifecycle-cancel]].
- **One-time service subscription vs. recurring subscription** — one-time (`billing_period == 'once'`) has no `next_billing_date`, no Cancel / Renew, no retry loop. See [[subscription-lifecycle-states]].

## Where it applies

The lifecycle drives a fan-out of screens and side-effects across the platform. The aspect pages own the detail; this hub maps where to drill.

**Subscription surfaces** — [[subscriptions]] (the My subscriptions list), [[subscriptions-detail]] / [[subscription-details]] (per-subscription detail), [[subscriptions-transactions]] (transaction history).

**Subscription-creating surfaces** — [[plans]] → [[plans-purchase]] (plan-type), [[plan-features]] (feature-type), [[plan-apps]] (app-type), [[plan-services]] (service-type), [[design-themes]] (theme-type).

**Lifecycle-driven UIs** — [[billing-cards]] (the saved card used for renewals), [[details-billing]] (invoicing applied per renewal), [[expired-subscription]] (the takeover screen after full plan expiry).

**Gating / cache** — [[plan-gates]] consumes subscription state for quota lookups; see [[subscription-lifecycle-cache-audit]] for the cache-flush behaviour. [[plan-vs-feature-pack]] is the sister concept for choosing the right upgrade path.

## Related

- [[subscriptions]] — the merchant's My subscriptions list; the central UI for this lifecycle.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail screen.
- [[subscriptions-transactions]] — full transaction history per subscription.
- [[plans]] — the plan catalog; buying a plan creates a plan-type subscription.
- [[plans-purchase]] — the purchase flow that creates plan-type subscriptions.
- [[plan-features]] — buying a feature pack creates a feature-type subscription.
- [[plan-apps]] — paid app subscriptions.
- [[plan-services]] — Expert-service subscriptions.
- [[billing-cards]] — saved cards used at renewal time.
- [[details-billing]] — invoicing details / recipient applied to each renewal.
- [[expired-subscription]] — the takeover screen when a plan subscription fully expires.
- [[plan-gates]] — the gating engine that consumes subscription state for quota lookups.
- [[plan-vs-feature-pack]] — sister concept on choosing between plan upgrade and feature pack.
- [[design-themes]] — paid theme subscriptions.
- [[notification-delivery]] — pre-billing notification, renewal-failure email, and admin alerts dispatch via this pipeline.
- [[background-queue-inventory]] — catalogue of background processes; explains the daily subscription-renewal, billing-charge, and expiry-sweep jobs that drive this lifecycle.
- [[merchant-subscription-lifecycle]] — merchant-question-driven hub answering "where do I see / change / cancel my subscription?"; read that for the merchant-support perspective, this hub for the state-machine semantics.

## Open Questions

- ⏸️ **No "Pause" subscription action.** CloudCart does NOT offer a pause / freeze / temporarily-stop button today. The only off-switch is **Cancel**, which terminates the subscription and stops billing — the merchant cannot suspend for a month and resume later. A merchant who needs to pause must cancel and re-subscribe later (potentially at a new price tier if pricing has changed).
