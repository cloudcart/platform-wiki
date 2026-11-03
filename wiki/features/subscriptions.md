---
type: feature
nav_path: "Profile → My subscriptions"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["My subscriptions", "Subscriptions list", "Active subscriptions", "Subscriptions", "Details → Subscriptions", "Mои абонаменти", "Абонаменти"]
tags: [subscriptions, list, billing, account]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 0
---
# Subscriptions

## Purpose

The **My subscriptions** list is the merchant's central view of every paid CloudCart service that recurs on a billing cycle: the **store plan**, every purchased **feature pack** (extra products, extra storage, extra admins, etc.), every paid **app subscription** (Algolia, AdScout, BumpCart, etc.), every paid **service** (Expert Services / agency add-ons), and any **hosted template / theme** subscription. Each row exposes the price, billing period, next billing date, next billing amount, current status, count of failed renewal attempts, and the per-row **Cancel** / **Renew** action appropriate for that subscription's state.

The list is the merchant's primary surface for two recurring questions: *"What am I currently paying for?"* and *"What renews next, when, and for how much?"*. From here the merchant drills into a single subscription (see [[subscriptions-detail]]) to see its transaction history, download invoices, and access detailed billing metadata.

The legacy Smarty list (`/admin/subscriptions`) is now a thin redirect — the canonical screen is the modern Vue list at `/admin/details/subscriptions`. Both route names (`admin.subscriptions`, `subscriptions-list`) end up on the same Vue component; existing bookmarks to either URL continue to work.

## Where to find it

Top-right **profile avatar** dropdown → **My subscriptions**.

The page's breadcrumb / title reads **Subscriptions** (translated per locale). The canonical URL is `/admin/details/subscriptions`. Old links and the legacy `/admin/subscriptions` URL bounce to the same Vue screen.

Only **store owners** see this menu entry. Staff / moderator accounts do not — the user-account dropdown gates the "My subscriptions", "Billing", and "Invoices" entries behind the owner-only check.

## What the merchant can do here

- **Review every recurring charge** in one place — plan, apps, feature packs, services, themes — sortable by Status (Active rows surface first by default).
- **Cancel** an Active subscription, or **Renew** a Canceled / Past due / Expired one, via per-row buttons. State-driven — see [[subscriptions-feature-actions]] for the button matrix and AJAX behaviour.
- **Filter** by Status (Active / Canceled / Past due / Expired) and Type (Feature / Application / Service / Plan).
- **Expand a row** to preview that subscription's recent transactions inline without navigating away. For the full transaction history see [[subscriptions-transactions]].
- **Drill into a single subscription** via the row's ID link to see invoices, full transaction history, and detailed billing metadata on [[subscriptions-detail]].

What the merchant **cannot** do here: bulk-cancel / bulk-renew, edit price / billing-period / next-billing fields inline, cancel LTA-contract subscriptions, export to CSV/Excel, or pause a subscription (Cancel is the only off-switch; see [[subscriptions-feature-status-state-machine]]).

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscriptions-feature-list-columns]] — the 9 list columns, default sort, expandable-row transaction preview, 2 filters, source endpoint.
- [[subscriptions-feature-actions]] — per-row Cancel / Renew buttons; state-driven visibility; AJAX endpoints + toasts; backend guards (LTA contracts, unpaid turnover); plan-purchase modal on inactive plans.
- [[subscriptions-feature-status-state-machine]] — the 4-state enum (Active / Canceled / Past due / Expired), transitions, "Cancel doesn't terminate" semantics, "Renew triggers immediate charge" semantics, soft-delete behaviour.
- [[subscriptions-feature-renewal-retry]] — the 5-attempt retry schedule with backoff, the renewal-pipeline gating conditions, the daily Expired sweep, and "Active doesn't mean currently being charged".
- [[subscriptions-feature-types]] — the 5 subscription types (Plan, Application, Feature, Service, Theme), what each affects, LTA-contract carve-out, one-time subscriptions, owner-only access gate.
- [[subscriptions-feature-notifications-pricing]] — pre-billing 7-day notify pipeline, per-attempt failure emails (no separate Past-due notify), promo first-cycle pricing semantics, Cancel-flow UX divergence between Smarty and Vue.

## Settings & fields

This is a read-only list. The merchant cannot edit the displayed values from this screen. The fields shown are aggregates of the underlying subscription record — see [[subscriptions-feature-list-columns]] for the full column table and source field mapping, and [[subscriptions-detail]] for the per-subscription field surface.

The list itself reads from `/admin/api/core/subscriptions` (paginated, with `status` and `type` filters applied via query string). Default page size is 25.

## Business rules

The business-rule surface for this screen is broad enough that it's split across aspect pages. Each aspect documents one rule cluster:

- **State machine** (what each status means + transition semantics) — see [[subscriptions-feature-status-state-machine]].
- **Retry pipeline** (when renewal charges retry, when they stop, when Expired flips) — see [[subscriptions-feature-renewal-retry]].
- **Action gating** (when buttons appear, what they fire, backend rejections) — see [[subscriptions-feature-actions]].
- **Subscription types** (what Plan / App / Feature / Service / Theme means, LTA carve-out, one-time semantics, owner-only access) — see [[subscriptions-feature-types]].
- **Notifications + pricing** (when emails fire, promo first-cycle pricing, UX divergence) — see [[subscriptions-feature-notifications-pricing]].

A single cross-cutting rule worth restating at the hub level: **Cancel is "soft"**. Cancel sets the row's status to `Canceled` but never deletes — past cancelled subscriptions remain visible (filterable by Status = Canceled) and their transaction history / invoices remain downloadable.

## Related

- [[subscriptions-detail]] — per-subscription view (price, billing period, status, transaction history).
- [[subscriptions-transactions]] — full transaction list for one subscription, with invoice download.
- [[plans]] — buying a plan creates a `plan_details`-type subscription on this list.
- [[plans-purchase]] — the purchase flow that creates a new subscription row here.
- [[plan-apps]] — buying a paid app creates a `cloudcart_app`-type subscription on this list.
- [[plan-features]] — feature packs that create `cloudcart_feature`-type subscriptions.
- [[plan-services]] — Expert Services that create `cloudcart_service`-type subscriptions.
- [[billing-cards]] — saved card used for the auto-renewal charge.
- [[details-billing]] — sibling **Billing** tab in the same Account-Details area; also surfaces invoicing details / recipient settings reflected on each renewal's invoice PDF.
- [[expired-subscription]] — the takeover screen the merchant sees when their plan subscription has fully expired.
- [[merchant-subscription-lifecycle]] — comprehensive merchant-question hub for "where do I see my subscription / how do I cancel / what happens at expiry" — bookmark this for support-agent reference.

## Open questions

(All resolved.)
