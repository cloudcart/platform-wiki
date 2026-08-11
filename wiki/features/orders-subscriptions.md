---
type: feature
nav_path: "Orders → Subscriptions"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership", "Membership subscriptions", "Storefront subscriptions", "Membership app", "Абонаменти на клиенти", "Членство"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---
# Subscriptions (Membership app overview)

## Purpose

The **Subscriptions** entry under Orders is the front-door for CloudCart's **Membership app** — when installed, this is where the merchant manages storefront subscriptions (customer-side memberships, gated content access, recurring access to specific products). When the Membership app is NOT installed, the entry shows the app's install/overview screen instead — the merchant clicks Install to enable the feature.

The Membership app lets the merchant create "locked" pages or product-tier gates that customers unlock after purchasing specific membership products. Each customer subscription is tracked here with status, days remaining, and the products it unlocks.

This is DISTINCT from CloudCart's own subscriptions ([[subscriptions]]) — that surface is about the merchant's bill for CloudCart plans/apps/services. THIS surface is about the merchant's CUSTOMERS' subscriptions for accessing membership content on the storefront.

## Where to find it

Sidebar → **Orders** → **Subscriptions**.

The page is part of the Orders module. When the Membership app is not yet installed, the link routes through `apps.membership.overview` and shows the app's install card. After install, the route resolves to the subscriptions list managed by the app.

The legacy POST/GET to `/orders/subscriptions` is routed through a redirect controller that points back to this overview entry. Old bookmarks continue to work.

## Sub-pages (in this cluster)

This topic is split into 5 aspect pages. Drill into the one that matches the question — don't read all five.

- [[orders-subscriptions-overview]] — the overview screen surface: subscriptions data-table (columns, sort, free-text search), the 5 filters, and the three modals (Add Subscription, Additional days, Delete).
- [[orders-subscriptions-auto-lifecycle]] — the hidden engine: subscriptions are auto-created when an order turns `paid`/`completed` and auto-removed when it reverts to a non-paid status; quantity multiplier, multi-page grants, the `order-*` status exemption.
- [[orders-subscriptions-manual-admin]] — admin-initiated subscriptions: the manual Create (VIP/gift), Add Extra Days bonus flow, the same-customer extend quirks (the double-days bug), and the unlimited-flip edge.
- [[orders-subscriptions-status-model]] — the minimal subscription record; status is COMPUTED from the single `expired` date; `NULL = Unlimited`; no daily expiry cron; the filter gap that hides unlimited rows.
- [[orders-subscriptions-integration]] — system integration: Apps-permission gating, silent failure logging, the customer-segment condition hooks that drive renewal campaigns.

## What the merchant can do here

### Before install (app overview)

- See the app's introduction: *"The membership app will allow you to create 'locked' pages that users will have access to after purchasing certain products."*
- Click **Install** to enable the Membership app.

### After install (subscriptions list — basic actions)

- Browse the list of customer membership subscriptions (one row per subscriber × subscription bundle) — see [[orders-subscriptions-overview]].
- **Add extra days** to a customer's subscription (bonus / compensation flow) — see [[orders-subscriptions-manual-admin]].
- **Delete** a customer subscription (row-level X icon with confirmation modal).
- **Create** a new customer subscription manually (admin-initiated, for VIP / gift cases) — see [[orders-subscriptions-manual-admin]].
- See subscription status (Active / Inactive — see [[orders-subscriptions-status-model]]).
- Filter by status, date, customer, product, page.

## Settings & fields

This is an overview page — settings live in the [[orders-subscriptions-settings]] sub-screen and in the Membership app's per-row management panel. The per-product membership configuration (which pages a product unlocks, how many `days` each grants) is set on the product editor in [[products-products]], not here.

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button (pre-install) | Activates the Membership app on the store | — | — |
| **Uninstall** button (post-install) | Removes the app + its subscription data | — | Drops ALL customer subscriptions — see [[orders-subscriptions-settings]]. |

## Business rules

### Membership is an app subscription, not a plan-feature

Installing Membership creates a `cloudcart_app` subscription on the merchant's account ([[subscriptions]]) and unlocks the storefront-side flow. Uninstalling cancels that app subscription at the next renewal.

### Customer subscriptions are independent of CloudCart subscriptions

When a customer buys a membership product on the storefront, the Membership app creates a *customer-side* subscription record (separate database, separate lifecycle). These subscriptions are listed here. They do NOT affect the merchant's plan limits.

### Subscriptions happen automatically — not at the click of a button

The merchant rarely issues subscriptions by hand. They are created automatically when an order is paid/completed and revoked when it reverts — see [[orders-subscriptions-auto-lifecycle]]. Manual create / extra-days are the exception for VIP / gift / compensation cases — see [[orders-subscriptions-manual-admin]].

## Related

- [[orders]] — parent orders area; the entry sits under the Orders sidebar group.
- [[orders-subscriptions-settings]] — sub-screen for the app's settings (status taxonomy, app-namespace migration, digital-product rule).
- [[subscriptions]] — the merchant's OWN subscriptions for CloudCart plans/apps/services (different surface, different scope).
- [[products-products]] — product editor where each digital product is linked to pages with a per-page `days` value.
- [[apps]] — where the Membership app can also be installed/uninstalled.

## Open questions

(none — Membership is a paid app; the post-install UI is owned by the app module. Per-row column list and detailed customer-subscription management UX are deferred to a dedicated Membership-app page when that documentation is generated.)
