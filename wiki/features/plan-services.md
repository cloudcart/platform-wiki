---
type: feature
nav_path: "Plan → Services"
route_name: plan-services
route_path: /admin/plan-services
aliases: ["Plan services", "Recommended services", "Services tab", "Buy services", "Professional services", "Препоръчани услуги", "Услуги за план"]
tags: [plans, plan-services, services, subscription-billing]
plan_gates: ["support_meetings", "machine_translation"]
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Plan Services

## Purpose

The **Services** tab inside the Plan area is a card grid of *recommended* professional services CloudCart offers — bundles of expert work the merchant can purchase to accelerate their store (e.g. theme setup, custom development, migration, training, audits). Unlike apps which run inside the store, services are human work delivered by CloudCart staff / partners. From this screen the merchant browses, searches, ticks one or more services, and proceeds to checkout for all of them in a single transaction. Each purchased service becomes its own [[subscriptions|subscription]] on the merchant's account.

The tab sits next to [[plans]], [[plan-apps]], and [[plan-features]] in the Plan area. This page is the **hub** for the Plan Services cluster — the detail lives in the sub-pages below.

## Where to find it

- **Plan → Services** tab in the Plan area's top-level tab bar.
- The Plan sidebar entry (owner-only) → click **Services** tab.
- The plan-purchase flow ([[plans-purchase]]) also surfaces a subset of these as the *Recommended services* block — that's a tied-to-a-plan bundling shortcut. This standalone tab lists them as buyable on their own.

URL pattern: `/admin/plan-services`.

## What the merchant can do here

- Browse the recommended-services catalogue as cards (icon, name, description, price, *Buy service* button) and search it by name / description — see [[plan-services-catalog]].
- Buy a single service immediately, or tick several and check out in one transaction — see [[plan-services-checkout]].
- See each purchased service appear as its own [[subscriptions|subscription]] with its own billing cycle and renewal behaviour — see [[plan-services-billing-lifecycle]].

What the merchant **cannot** do here: edit pricing / definitions, surface a non-recommended service, cancel a service (done from [[subscriptions]]), adjust quantity, or apply a discount code (applied at the checkout step). Full list on [[plan-services-catalog]].

## Settings & fields

This is a browse / select screen — no editable fields. Per card the merchant sees: a fixed user-with-gear icon, a selection checkbox, the localised name, a Markdown description (truncated with *Show more*), pricing (price excl. VAT + billing period), and a *Buy service* button. The header carries a search box and a *Buy selected services ({count})* bulk button. The exact field table is on [[plan-services-catalog]].

## Business rules

- The catalogue is filtered to *recommended* (`recommend = 1`) + non-archived services, ordered by `sort_order` — see [[plan-services-catalog]].
- The Services tab catalogue itself is NOT plan-gated; every merchant sees the same list. A few specific services consume a plan-feature mapping after purchase (`support_meetings`, `machine_translation`) — see [[plan-services-billing-lifecycle]].
- Purchase requires invoice details ([[billing-invoicing]]) + a payment method ([[billing-cards]]) — see [[plan-services-checkout]].
- Once-off (`once`) services are charged once and don't auto-renew; recurring services follow the standard renewal retry schedule — see [[plan-services-billing-lifecycle]].

## Sub-pages (in this cluster)

This feature is split into 3 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[plan-services-catalog]] — the card-grid browse / search UI; what each card shows; what the merchant can and cannot do; the *recommended* + non-archived + `sort_order` filter; per-language name / description.
- [[plan-services-checkout]] — single-service vs multi-select bulk checkout; the cart shape sent to checkout; invoice-details + card-on-file gate; one subscription created per service; post-purchase selection reset; standalone tab vs the plan-purchase recommended bundle.
- [[plan-services-billing-lifecycle]] — billing periods (`once` / `month` / `year`); once-off vs recurring renewal; the renewal retry schedule and PAST_DUE → EXPIRED path; the `support_meetings` + `machine_translation` plan-feature mappings some services consume.

## Related

- [[plans]] — pick-a-plan catalog (the default tab in this area).
- [[plan-apps]] — paid apps available to add to the plan.
- [[plan-features]] — buy additional quota on individual features.
- [[plans-purchase]] — the per-plan purchase flow, which also bundles recommended services into a plan-checkout.
- [[subscriptions]] — where purchased services appear as subscriptions; cancellation happens there.
- [[billing-cards]] — saved card that pays for service subscriptions.
- [[billing-invoicing]] — invoice details printed on the service invoice.
- [[merchant-subscription-lifecycle]] — merchant-question hub: "how do I buy a service / what's the difference between service / app / plan subscriptions?".

## Open questions

None.
