---
type: concept
nav_path: "Concept → Plan vs. feature pack"
route_name: ""
route_path: ""
aliases: ["Plan vs feature pack", "When to upgrade plan vs buy feature pack", "Feature pack vs plan upgrade", "Plan upgrade or pack", "Plan upgrade or add-on", "Pack vs upgrade", "Quota top-up vs plan upgrade", "Upgrade or pack", "План срещу пакет", "Кога да купя пакет", "Кога да ъпгрейдна плана", "Допълнителен пакет или ъпгрейд"]
tags: [plans, plan-features, feature-pack, billing, gating, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Plan vs. feature pack

## Definition

The **plan-vs-feature-pack** decision is one of CloudCart's most-asked merchant questions: *"I hit a limit — should I upgrade my plan, or buy a feature pack?"* CloudCart's billing model deliberately offers BOTH paths so merchants can pick the cheaper option. A **plan upgrade** ([[plans]]) moves the merchant to a higher tier (Free → Starter → Pro → Business → Enterprise, with country-specific variants) — unlocking MANY features at once: higher product / customer / administrator / storage / channel limits, plus boolean features like SSL certificates, Storefront Builder, customer import/export. A **feature pack** ([[plan-features]]) is the opposite — it buys additional quota for ONE specific feature on top of the merchant's CURRENT plan, leaving everything else unchanged (*+100 products*, *+1000 newsletter sends/month*, *+5 GB storage*).

The two are not mutually exclusive — feature packs **stack** on top of the plan's base quota AND survive plan changes. A merchant on Starter (500 products base) who buys a +100 products pack has 600 effective; upgrading to Pro (5,000 base) keeps the pack active (5,100 effective). This cluster covers the trade-off, the stacking rules, the cost heuristic, and the merchant-confusing edge cases (downgrade with active packs, pack-availability restrictions, the `enable_feature_pack` flag, the `max_value` ceiling).

## Sub-pages (in this cluster)

This concept is split into 5 aspect pages. Drill into the one that matches the question rather than reading every page.

- [[plan-vs-feature-pack-stacking]] — the `effective_quota = plan base + active packs` formula; numeric vs. boolean packs; packs survive plan upgrade (and the billing surprise that creates).
- [[plan-vs-feature-pack-downgrade]] — what happens when downgrade / pack-cancellation puts the merchant over quota; no data loss, Add buttons blocked; prune-or-pack remedy.
- [[plan-vs-feature-pack-cost-heuristic]] — the "how many limits am I hitting?" decision table; the 2–3-packs ≈ one-upgrade rule of thumb; where the prices live.
- [[plan-vs-feature-pack-availability]] — the gates that decide whether a pack even surfaces: `enable_feature_pack`, `plan.restrict.feature_purchase` tier-locking, the `max_value` ceiling, dynamic-pricing ladders.
- [[plan-vs-feature-pack-lifecycle]] — the pack as a subscription: lifecycle states, renewal retry loop, 1-week cache flush, cart reset on purchase, post-purchase app activation.

## Scope

What this cluster covers:

- The plan-vs-pack mental model — what each is, what each affects.
- The stacking rule and survives-plan-change rule — see [[plan-vs-feature-pack-stacking]].
- Downgrade / cancellation over-quota blocking — see [[plan-vs-feature-pack-downgrade]].
- The cost-comparison heuristic — see [[plan-vs-feature-pack-cost-heuristic]].
- Pack-availability gates (`enable_feature_pack`, tier-locking, `max_value`, dynamic pricing) — see [[plan-vs-feature-pack-availability]].
- Pack lifecycle, billing, cache flush, cart reset, app activation — see [[plan-vs-feature-pack-lifecycle]].

What it does NOT cover:

- The full catalog of which features have packs — see [[plan-features]].
- The plan-tier comparison matrix — see [[plans]].
- The plan purchase flow UX — see [[plans-purchase]].
- The general plan-gating engine — see [[plan-gates]].
- The subscription state machine itself — see [[subscription-lifecycle]].

## Contrasts

- **Plan upgrade vs. feature pack — fundamental difference**: a plan upgrade unlocks MANY features at once; a feature pack unlocks ONE feature in isolation. Plan upgrade is broad; pack is surgical. Plan upgrade changes the merchant's overall tier (their badge reads the new plan); pack leaves the tier unchanged (the merchant stays Starter with a pack on top).
- **Plan billing vs. pack billing**: both are subscriptions on the same [[subscription-lifecycle]] with INDEPENDENT billing cycles — the plan renews on its date, each pack on its own. The merchant sees both as separate rows in [[subscriptions]]; cancelling one does not cancel the other. Detail in [[plan-vs-feature-pack-lifecycle]].
- **Feature pack vs. app subscription**: feature packs add QUOTA to a feature already on the plan; app subscriptions enable entirely new FUNCTIONALITY (Algolia search, AdScout retargeting, BumpCart upsell). Both create subscriptions but affect different layers — packs scale an existing capacity, apps add new capabilities.
- **Stacking (additive) vs. upgrade (replacement)**: a pack ADDS to the base; an upgrade REPLACES the base. Worked examples in [[plan-vs-feature-pack-stacking]].
- **"Buy pack" route vs. "Buy plan" route**: a pack purchase goes through `/admin/plan/feature/{mapping}` ([[plan-features]]); a plan purchase through `/admin/plan/{mapping}/purchase` ([[plans-purchase]]). Both end at `/admin/checkout` but the cart is seeded differently (one pack vs. one plan-billing-cycle + optional recommended services / apps).

## Where it applies

### The two entry points

- [[plans]] — the plan catalog. Click a plan card → [[plans-purchase]] → checkout. The "upgrade plan" path.
- [[plan-features]] — the per-feature upsell paywall. The "buy pack" path. Reached automatically when the merchant hits a quota limit anywhere in the admin panel, OR from a warning banner's *"Upgrade your quota from here"* link.

### Where the merchant hits the decision

Plan-gate exhaustion lands the merchant on [[plan-features]] for the specific feature they hit, BUT the page also shows the alternative — *"you can also upgrade your plan"* — with the list of qualifying plans. The merchant chooses on one screen. Entry-point screens where the redirect happens include: [[products]] (501st product on Starter), [[customers]] / [[customers-import]], [[marketing-blog-articles]], [[apps-bundles-overview-new]], [[products-smart-collections]], [[settings-staff]], [[settings-files]], [[settings-domains]], [[marketing-landing-pages]], [[apps-xml-sync]] / [[apps-xml-import]], [[marketing-segments]], and [[marketing-discounts]] (per discount type).

### Subscription / billing & gating surfaces

- [[subscriptions]] — both plan and feature-pack subscriptions appear here as separate rows.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription view; both types render identically.
- [[subscription-lifecycle]] — the shared state machine governs both.
- [[billing-cards]] — the same saved card pays for both.
- [[plan-gates]] — the gating engine that consumes plan base + active packs at lookup time; the 1-week-cached lookup is flushed on pack purchase / cancel (see [[plan-vs-feature-pack-lifecycle]]).

## Related

- [[plans]] — the plan catalog; the upgrade-instead alternative to buying a pack.
- [[plans-purchase]] — the per-plan purchase flow.
- [[plan-features]] — the per-feature pack-upsell paywall; where pack purchases happen.
- [[plan-gates]] — the gating engine that consumes plan + pack values.
- [[subscriptions]] — both plan and pack subscriptions appear here as separate rows.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail view.
- [[subscription-lifecycle]] — the shared state machine governing both plan and pack subscriptions.
- [[billing-cards]] — saved card used for plan + pack renewals.
- [[details-billing]] — invoicing details applied to each renewal's invoice.
- [[plan-apps]] — paid app subscriptions (a sibling type, distinct from feature packs).
- [[plan-services]] — Expert-service subscriptions (one-time or recurring).
- [[expired-subscription]] — the takeover screen when the plan subscription fully expires.
- [[plan]] — the Plan entity carrying restrictions.
- [[plan-feature]] — the Plan-Feature entity catalog.
- [[merchant-subscription-lifecycle]] — merchant-question hub: includes the plan-vs-pack guidance plus all related billing surfaces.

## Open Questions

- ⏸️ **Plan-downgrade with an active feature-pack that the new plan does not allow.** Feature packs are tied to the merchant's subscription, not to the current plan tier. If the merchant downgrades to a tier where a specific pack is not normally purchasable, the pack continues to bill against the merchant until they cancel it explicitly. Merchants downgrading their main plan should review their active feature-pack subscriptions and cancel any that don't make sense on the new tier — the platform doesn't auto-cancel for them.

All other previously-flagged questions resolved. See body sections for details.
