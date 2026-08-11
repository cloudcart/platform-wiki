---
type: feature
nav_path: "Plan → Services"
route_name: plan-services
route_path: /admin/plan-services
aliases: ["Service billing", "Service renewal", "Once-off services", "Recurring services", "Service subscription lifecycle", "Service plan gates", "support_meetings", "machine_translation", "Подновяване на услуги", "Еднократни услуги"]
tags: [plans, plan-services, services, subscription-billing, plan-gates]
plan_gates: ["support_meetings", "machine_translation"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-services]]. See the hub for the other aspects (catalogue, checkout).

# Plan services — billing & lifecycle

## Purpose

This aspect covers what happens to a service **after** purchase: how its billing period (`once` / `month` / `year`) decides whether it auto-renews, the renewal retry schedule and the PAST_DUE → EXPIRED path it shares with plans / apps / feature packs, and the two plan-feature mappings (`support_meetings`, `machine_translation`) that a couple of services on this tab consume once active. Browsing is on [[plan-services-catalog]]; the purchase flow on [[plan-services-checkout]].

## Where to find it

- The billing period of each service is shown on its card on **Plan → Services** (`/admin/plan-services`) as *price / period* — see [[plan-services-catalog]].
- After purchase, the service's billing cycle, next_billing_date, and cancel action live on [[subscriptions]].

## What the merchant can do here

- Read each service's billing period on the catalogue card before buying (one-time vs recurring).
- Track and cancel a purchased service from [[subscriptions]] (recurring services stop at next_billing_date; once-off services have no recurring charge to cancel).
- Buy additional quota packs from [[plan-features]] when a feature-mapped service's allowance is exhausted.

## Settings & fields

There are no editable fields on this screen for billing — the period is fixed per service in CloudCart's catalogue. The merchant-visible billing facts are:

| Billing-period value | Card label | Renews? |
|----------------------|-----------|---------|
| `once` | *One time* / *onetime* | No — single charge |
| `month` | *Monthly* (and the period multiples *Quarterly* / *Semi-annually*) | Yes |
| `year` | *Annually* (and *2 Years*) | Yes |

## Business rules

### Billing-period text

Each service has a billing period (`once`, `month`, `year`). The display formats it as *price / period* — e.g. *50.00 EUR / month* for a recurring service, *200.00 EUR / onetime* for a one-off. Recurring services renew automatically until cancelled.

### Once-off services don't auto-renew

Services with `billing_period = once` are charged a single time and do not auto-renew. The corresponding subscription record still exists for accounting / history but is effectively complete on the first charge — there is no next_billing_amount and no retry logic.

### Recurring services follow the standard renewal retry schedule

Services with monthly / yearly billing periods follow the same renewal retry rules as plans + apps + feature packs: 2 / 3 / 4 / 5 days between attempts, up to 5 total charge attempts before the auto-retry loop stops (see [[subscriptions]]). The subscription transitions to PAST_DUE on the first failed renewal and stays Past due until the daily `expire:subscriptions` sweep flips it to EXPIRED ~1 month after next_billing_date. The site-level [[expired-subscription]] takeover only fires when the **plan-detail** subscription is Past due / Expired — a Past-due service subscription on its own doesn't block admin access.

### Plan-feature mappings some services consume

The Services tab catalogue itself is NOT plan-gated — every merchant sees the same `recommend = 1` + non-archived list regardless of plan. The gates below apply to specific services in the catalogue that, once purchased, consume a plan-feature mapping (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `support_meetings` | Boolean (plan-level enable) → consumable quota when active | Default-restricted (restricted by default in the plan config). Once unlocked by an active subscription (typically purchased as a recurring service from this Services tab), the limit becomes a per-30-day meeting counter — the feature label is *"meetings for 30 days"*. Booking a meeting beyond the count surfaces the standard HTTP 402 paywall modal pointing at [[plan-features]]. |
| `machine_translation` | Numeric / boolean (counted jobs) | Gates machine-translation jobs in the multi-language manager. A translate job sets `machine_translation = 1` on the setting during execution; the platform consumes the merchant's allowed count per the plan-feature value. When exhausted, the merchant can purchase additional translation packs from [[plan-features]] (the feature is included in the recommended-pack list). |

Behaviour: lower plans get redirected to the per-feature upsell at [[plan-features]] or to a plan-upgrade panel. `support_meetings` is access-shaped at the plan level (default-restricted) but billed as a recurring service via this Services tab — each tier of the service ladder maps to a meeting-count quota. `machine_translation` is numeric — it extends via packs ([[plan-vs-feature-pack]]). Both are EXAMPLES of services on this tab that ALSO consume a plan-feature mapping after purchase; many other services on this tab (theme setup, migration, training, audits) are pure deliverables with no per-purchase plan-feature consumption.

## Related

- [[plan-services]] — hub.
- [[subscriptions]] — where the service subscription lives, renews, and is cancelled.
- [[plan-features]] — buy additional quota when a feature-mapped service's allowance is exhausted.
- [[plan-gates]] — the plan-feature gating system the two mapped services consume.
- [[plan-vs-feature-pack]] — how numeric features (e.g. `machine_translation`) extend via packs.
- [[expired-subscription]] — site takeover; only the plan-detail subscription triggers it, not a service.
- [[merchant-subscription-lifecycle]] — the cross-cutting merchant-question hub for subscription billing.

## Open questions

None.
