---
type: feature
nav_path: "Details → Subscriptions → Subscription"
route_name: subscription-details
route_path: /admin/details/subscriptions/:id
aliases: ["Subscription details (modern Vue route)", "Subscription detail page", "Detail panel route"]
tags: [base, accounddetails, details, subscriptions, redirect-page]
plan_gates: []
created: 2026-05-21
updated: 2026-06-06
source_count: 0
---
# Subscription details (modern Vue route)

## Purpose

This is the **modern Vue route entry** for the per-subscription detail page at `/admin/details/subscriptions/:id`. It mounts the same `SubscriptionDetails` component documented in detail on the canonical page [[subscriptions-detail]] — header + three info cards (Details / Pricing / Next billing) + transactions table.

Both wiki pages describe the same screen — this file documents the URL pattern and Vue route name, while [[subscriptions-detail]] documents the full behaviour. For everything about what the merchant sees, what they can do, and the cancel / renew endpoint behaviour, **read [[subscriptions-detail]]**.

## Where to find it

[[subscriptions]] → click any row's ID column or Name expand → opens this URL.

URL pattern: `/admin/details/subscriptions/{unique_id}` — the `{unique_id}` segment is the subscription's short opaque ID (e.g., `66b3fa1...`).

Vue route name: `subscription-details`.

Component: ` => import('./../components/Tabs/SubscriptionDetails')` (also reused by the legacy Smarty `admin.subscriptions.show` route at `/admin/subscriptions/{unique_id}` — same component, different URL).

## What the merchant can do here

See [[subscriptions-detail]] for the full feature catalogue (info cards, transactions table, expandable card-details dropdown, invoice download). This file does not duplicate that content.

## Settings & fields

See [[subscriptions-detail]] for the full per-field documentation.

## Business rules

See [[subscriptions-detail]] for the cancel / renew endpoint behaviour, `canActivate` free-reactivation rule, plan-deprecation redirect logic, app re-install on late renewal, audit log, and discount carry-over.

See [[subscription-lifecycle]] for the shared status state machine that drives the badge displayed on this page.

## Related

- [[subscriptions-detail]] — **canonical detail page for this screen** (read this).
- [[subscriptions]] — the parent list page that links here.
- [[subscriptions-transactions]] — the transactions table rendered below the info cards on this screen.
- [[subscription-lifecycle]] — the shared status state machine.
- [[merchant-subscription-lifecycle]] — comprehensive merchant-question hub answering "where do I see my current subscription?" with cross-references.
- [[billing-cards]] — saved card used at renewal time.
- [[details-billing]] — invoicing details applied to each renewal's invoice PDF.
- [[expired-subscription]] — the takeover screen when the plan subscription fully expires.

## Open questions

None — this page is a thin route-documentation stub. All substantive content is on [[subscriptions-detail]].
