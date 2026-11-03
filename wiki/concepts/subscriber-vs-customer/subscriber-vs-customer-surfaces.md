---
type: concept
nav_path: "Concept → Subscriber vs Customer → Admin-panel surfaces"
aliases: ["Where customer vs subscriber shows", "Subscriber vs customer admin screens", "Customer subscriber UI map", "Subscribers list customer detail"]
tags: [customers, subscribers, marketing, navigation, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[subscriber-vs-customer]]. See the hub for the other aspects (records, channels, consent, linkage, privacy, plan limits).

# Subscriber vs Customer — where it shows up in the admin panel

## Definition

The Customer-vs-Subscriber distinction surfaces in **separate sections of the admin panel** because the two records live in two separate concerns: the Customers section is for buyer / order-history management, and the Marketing → Subscribers section is for audience / consent / channel management. Every screen that touches one OR the other (and a handful that surface both side-by-side) needs the merchant to know which record they're looking at.

This page is a navigation map. It does not redefine the records — see [[subscriber-vs-customer-records]] — and it does not describe the consent gate or the channel flags — see [[subscriber-vs-customer-consent]] and [[subscriber-vs-customer-channels]]. It catalogues the **screens, imports, settings, and integrations** where the distinction is visible.

## Scope

Covered:

- Customer-side lists and detail screens.
- Subscriber-side lists and detail screens.
- Imports and exports on each side.
- Subscribe forms and storefront-side surfaces.
- Settings that govern the distinction.
- Campaign / segment surfaces.
- Plan / privacy / lifecycle surfaces.
- The screens that surface BOTH records side-by-side.

Not covered:

- What the records carry — see [[subscriber-vs-customer-records]].
- The channels and deliverability flags — see [[subscriber-vs-customer-channels]].
- Consent gates and propagation — see [[subscriber-vs-customer-consent]].
- Linkage / conversion paths — see [[subscriber-vs-customer-linkage]].

## Contrasts

- **Customer-side surfaces vs Subscriber-side surfaces** — Customer-side carries order history / lifetime revenue / addresses; Subscriber-side carries channels / segments / RFM / consent flags. The merchant typically uses one or the other depending on whether they're answering a buyer question or an audience question.
- **Lists vs detail screens** — list screens show bulk-edit affordances; detail screens show the cross-record relationship (e.g., [[customers-details]] shows the linked Subscriber's channels in the overview tab; [[marketing-subscribers]] detail shows the Customers tab with every linked Customer + their order totals).

## Where it applies

### Customer-side lists and detail

- [[customers]] — Customer list. Shows the Customer-level `marketing` flag column. Bulk-edit marketing here.
- [[customers-details]] — Customer detail. Surfaces the linked Subscriber's channels in the overview tab.
- [[customers-details-overview]] — has a "Customers and Subscribers" surface showing the same email from both perspectives.
- [[customers-custom-groups]] — Customer Group management; Groups are Customer-only and never apply to Subscribers.
- [[customers-custom-fields]] — Customer custom-field configuration; distinct from Subscriber custom fields.

### Subscriber-side lists and detail

- [[marketing-subscribers]] — Subscriber list. Per-channel `marketing` / `verified` / `unsubscribed` / `bounced` flag columns; bulk-edit per channel here; "Second marketing" setting; subscriber-pack paywall when over the `subscribers` plan cap.
- [[subscriber]] — Subscriber entity / detail. Has a Customers tab listing every linked Customer + their order totals + their lifetime income.
- [[marketing-subscribers-custom-fields]] — Subscriber custom-field configuration; distinct from Customer custom fields.

### Imports, exports, and forms

- [[customers-import]] — imports Customers; the "Mark as subscriber" option co-creates Subscriber rows. Otherwise imports are Customer-only.
- [[customers-export]] — exports Customer fields only (addresses, orders, lifetime revenue, group). Does NOT include per-channel marketing details.
- [[marketing-subscribers]] → Import — imports Subscriber-only rows. Does NOT create Customer accounts.
- [[marketing-subscribers-subscribe-forms]] — storefront popups / signup forms that create Subscribers (NOT Customers).

### Storefront / customer-facing surfaces

- [[checkout-flow]] — where the marketing-consent checkbox at checkout decides whether a Subscriber row is auto-created with Email-channel `marketing = yes` or `marketing = no`.
- [[marketing-subscribers-subscribe-forms]] — popup / signup forms that create newsletter-only Subscribers.
- Storefront account → preferences — where Customers self-toggle their `marketing` flag, syncing the linked Subscriber's per-channel flag (per the cascade rule documented in [[subscriber-vs-customer-consent]]).

### Settings that govern the distinction

- [[settings-general]] — store-level GDPR / marketing-policy settings that set the storefront consent labels.
- [[marketing-subscribers]] → Settings — the **Second marketing** auto-reset rule, RFM interval, revenue statuses.
- [[settings-statuses]] — order statuses count toward Subscriber turnover only when listed under "Revenue statuses" in Subscriber Settings.
- [[settings-hooks]] — `customer.*` and `subscriber.*` webhook event families fire independently.

### Campaigns and segments

- [[marketing-campaigns]] — broadcasts that target Subscribers; reads per-channel deliverability before sending. Customers without a Subscriber are unreachable from campaigns.
- [[marketing-segments]] — built on the Subscriber pool. Customers with no Subscriber are invisible to every segment.
- [[marketing-segments-subscribers]] — segment members view; lists Subscribers (not Customers).
- [[marketing-segments-log]] — segment-execution log; surfaces Subscriber id ranges.

### Plan, privacy, lifecycle

- [[plan-gates]] — `customers` cap and `subscribers` cap are independent; see [[subscriber-vs-customer-limits]].
- [[notification-delivery]] — applies the two-layer consent check before dispatching marketing.
- [[merchant-subscription-lifecycle]] — billing path for customer-pack / subscriber-pack purchases.

### Screens that surface both records side-by-side

These are the screens where the merchant most often confuses Customer with Subscriber, because both are visible at once:

- [[customers-details]] — the Customer detail surfaces the linked Subscriber's channels and consent flags in the overview tab. The merchant editing the Customer here can also see — but not directly edit — the linked Subscriber's per-channel marketing flag (per-channel edit happens on the Subscriber detail).
- [[subscriber]] detail — surfaces a "Customers" tab listing every linked Customer with their order count, lifetime revenue, and last-order date. The merchant editing the Subscriber here can navigate to any linked Customer.
- [[customers-details-overview]] — the "Customers and Subscribers" overview block shows the same email from both perspectives — useful for explaining "this person is both" or "this person is only a Customer" to a confused merchant.

## Related

- [[subscriber-vs-customer]] — hub.
- [[subscriber-vs-customer-records]] — what each record carries.
- [[subscriber-vs-customer-channels]] — per-channel flag surface.
- [[subscriber-vs-customer-consent]] — the gate surfaces apply.
- [[subscriber-vs-customer-linkage]] — how the join row gets shown on [[customers-details]] and [[subscriber]] detail.
- [[subscriber-vs-customer-privacy]] — delete actions on each list / detail.
- [[subscriber-vs-customer-limits]] — paywall surfaces when over-cap.
- [[customers]] — Customer list.
- [[customers-details]] — Customer detail.
- [[marketing-subscribers]] — Subscriber list.
- [[subscriber]] — Subscriber entity / detail.
- [[marketing-campaigns]] — campaign builder.
- [[marketing-segments]] — segment builder.

## Open Questions

None.
