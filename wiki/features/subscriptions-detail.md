---
type: feature
nav_path: "Profile → My subscriptions → Subscription"
route_name: admin.subscriptions.show
route_path: /admin/subscriptions/{unique_id}
aliases: ["Subscription details", "Subscription view", "Subscription cancel", "Subscription renew", "Детайли на абонамент", "Преглед на абонамент"]
tags: [subscriptions, details, cancel, renew, billing, account, modern-vue]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 0
---
# Subscription detail

## Purpose

The **per-subscription view** — opened by clicking a row in [[subscriptions]]. It shows everything the merchant needs to know about one subscription: a header with the subscription's name + icon, three info cards (**Details** / **Pricing** / **Next billing**), the current status badge, and the full transaction history table below (see [[subscriptions-transactions]] for the column-by-column breakdown of that table).

This is also the conceptual home of the **Cancel** action (when allowed) and the **Renew** action (for a subscription that's past due / canceled / expired). On the modern Vue UI those buttons live on the [[subscriptions]] list page's Actions column, not on the detail screen — but the endpoint behaviour they trigger is documented in this cluster.

The canonical screen is the modern Vue page at `/admin/details/subscriptions/<unique_id>`. The legacy Smarty route `/admin/subscriptions/<unique_id>` renders the older read-only view (which additionally shows a contract link when applicable + a service description for Expert Services).

This page was split into three aspect sub-pages because it covered three distinct concepts: the on-screen display, the Cancel/Renew endpoint behaviour, and the downstream lifecycle side-effects. Drill into the aspect that matches the question.

## Where to find it

[[subscriptions]] → click any row's ID/Name → opens `/admin/details/subscriptions/<unique_id>`.

The breadcrumb reads **Subscriptions → `<unique_id>`**. The page title in the header is `<unique_id> - <subscription name>` (example: `66b3fa1abcd - Plan: Business — Year`).

## Sub-pages (in this cluster)

- [[subscriptions-detail-screen]] — the visible UI: header, the three info cards (Details / Pricing / Next billing), the status badge, the transactions table placement, read-only field list, and the legacy-vs-modern display differences (contract link, service description).
- [[subscriptions-detail-cancel-renew]] — the Cancel and Renew endpoint behaviour: cancel guards (LTA contract, unpaid turnover), the `canActivate` "free reactivation" rule, the renew matrix per subscription type, charge success/failure handling, price-edit protection, and discount carry-over.
- [[subscriptions-detail-lifecycle-effects]] — downstream effects after a state change: plan-cancellation site-status cascade, app re-install on late renewal, app-expiry behaviour (data stays, features stop), the audit log, the per-subscription retry slot, and which dunning emails fire in which state.

## What the merchant can do here

The detail screen itself is **read-only display + transaction history**. The merchant views the subscription's metadata and history here; the Cancel / Renew action buttons are on the [[subscriptions]] list page. For the full on-screen surface (cards, fields, status badge), see [[subscriptions-detail-screen]]. For what Cancel / Renew actually do, see [[subscriptions-detail-cancel-renew]].

## Settings & fields

All fields on this page are read-only. The full per-field table (`unique_id`, `created_at`, `model_type`, `name`, `price`, `billing_period`, `value`, `next_billing_date`, `next_billing_amount`, `status`, `failed_attempts`, `lta_contract_id`) is documented on [[subscriptions-detail-screen]].

## Business rules

The substantive rules live on the aspect pages:

- **Cancel** is blocked for LTA-contract subscriptions and for subscriptions with unpaid plan turnover; otherwise it sets status to Canceled and the service stays usable until `next_billing_date` — see [[subscriptions-detail-cancel-renew]].
- **Renew** behaves differently for Plan / LTA-contract / other subscription types, and is a free reactivation (no fresh charge) when paid time still remains — see [[subscriptions-detail-cancel-renew]].
- **`next_billing_amount` cannot be edited** — the platform rejects it with *"Changing the next billing amount is disabled"* — see [[subscriptions-detail-cancel-renew]].
- **Cancelling a Plan subscription cascades to site status**; non-Plan subscriptions affect only themselves — see [[subscriptions-detail-lifecycle-effects]].
- **Owner-only access** — same as the list, only store owners reach this screen via the profile dropdown.

## Related

- [[subscriptions]] — the parent list (Cancel / Renew buttons live here on the modern UI).
- [[subscriptions-transactions]] — the transaction history rendered below the info cards on this page.
- [[subscription-details]] — the modern Vue route stub that mounts this screen.
- [[plans]] — where a deactivated Plan subscription redirects on renew.
- [[plans-purchase]] — the purchase flow that originally created this subscription row.
- [[plan-apps]] — App-type subscriptions originate here.
- [[plan-features]] — Feature-pack subscriptions originate here.
- [[plan-services]] — Service-type subscriptions originate here.
- [[billing-cards]] — saved card used for the renewal charge.
- [[details-billing]] — invoicing details / recipient applied to each renewal invoice.
- [[expired-subscription]] — the takeover screen when the Plan subscription expires fully.
- [[merchant-subscription-lifecycle]] — merchant-question hub for the full billing lifecycle.

## How it works (verified against backend)

- The URL path segment is the subscription's `unique_id` (a short generated token); the numeric ID is internal and never exposed. The same `unique_id` is the foreign key on transactions and invoices for this subscription. Note the route mismatch: the show route uses `{unique_id}` but the cancel / renew / transactions routes use `{id}` (the numeric primary key) — the Vue list page handles this internally, so the merchant never types these URLs.
- The on-screen mechanics (status colour coding, legacy contract link, service description, `value`-field usage by type) are documented on [[subscriptions-detail-screen]].
- The endpoint mechanics (`canActivate`, renewal date advance, retry handling) are documented on [[subscriptions-detail-cancel-renew]] and [[subscriptions-detail-lifecycle-effects]].

## Open questions

(All resolved.)
