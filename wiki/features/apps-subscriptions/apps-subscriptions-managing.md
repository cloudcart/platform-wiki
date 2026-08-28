---
type: feature
nav_path: "Apps → Subscriptions → Subscriptions"
route_name: apps.subscriptions.list
route_path: /admin/apps/subscriptions/list
aliases: ["subscriptions list", "subscription details", "charge now subscription", "merchant cancel subscription", "subscription history", "subscription emails", "списък с абонаменти", "детайли на абонамент", "начисли сега"]
tags: [apps, subscriptions, admin, notifications, actions]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (setup, plans, billing cycle, failed payments, customer controls).

# Subscriptions — managing them as the merchant

## Purpose

The merchant's view of live contracts: the list, what one contract's page shows, the five actions available on it, and the four e-mails the app sends.

## Where to find it

**Apps → Subscriptions → Subscriptions** tab (`/admin/apps/subscriptions/list`); a contract opens at `/admin/apps/subscriptions/list/<id>`.

## What the merchant can do here

- Browse every subscription with its status and schedule.
- Open one to see its full history.
- Act on it — pause, resume, skip, cancel, or charge it now.

## Settings & fields

The list is a read-out, not a form. The detail page shows the contract's plan terms, its customer, its next dates, its cycle history and its events.

## Business rules

### Five actions, mirroring the customer's

| Action | What it does |
|---|---|
| **Pause** | Stops the schedule until resumed. |
| **Resume** | Puts a paused contract back on schedule. |
| **Skip** | Passes over the next delivery without charging. |
| **Cancel** | Ends the contract. |
| **Charge now** | Bills the contract immediately, off its schedule. |

The first four are what the customer can also do from their account when the merchant allows it ([[apps-subscriptions-customer-controls]]). **Charge now** is the merchant's alone.

The same state rules apply here as on the storefront — a contract that is not active cannot be paused, one not paused cannot be resumed, and one in a non-billable state refuses **Charge now** with *"This subscription cannot be charged in its current state."* The merchant's version is not a way around the state machine; it is a way around the **customer permissions**.

### Charge now is for recovery, not for pulling revenue forward

Its normal use is a contract sitting in `past_due` after a decline, once the customer says their card is fixed — rather than waiting days for the next scheduled retry ([[apps-subscriptions-failed-payments]]).

Using it on a healthy subscription charges the customer earlier than they agreed to, which is the kind of thing that produces a chargeback. The schedule exists because the customer consented to it.

### The history answers "what happened and when"

Each contract keeps its own event log — created, charged, payment failed, paused, resumed, cancelled — separately from the order history of the orders it produced ([[orders-history]]). A failure event records whether another attempt is expected, so the log itself says whether the merchant should wait or act.

Two logs, two questions: the contract's log explains the **subscription**, the order's log explains a **particular delivery**.

### Four e-mails, each independently switchable

| E-mail | When | Setting |
|---|---|---|
| **Subscription started** | The customer's first purchase on a plan | `notify_customer_started` |
| **Renewed** | Each successful charge | `notify_customer_renewed` |
| **Upcoming renewal** | A configurable number of days before the next charge | `notify_customer_upcoming` + `notify_upcoming_days` |
| **Payment failed** | On the first failure only | `notify_customer_failed` |

The **upcoming renewal** reminder is the one worth keeping on. A customer surprised by a charge disputes it; a customer reminded of it a few days earlier either lets it run or skips the delivery, and both outcomes are better than a chargeback.

Templates are per store language, so a store selling in more than one language should check each ([[settings-translations]]).

### The contract holds the customer, the orders hold the deliveries

A subscription belongs to a customer record and reuses their stored card and address. Everything it produces is an ordinary order in [[orders]] — so revenue, fulfilment and returns are answered there, not here.

The practical division: use this screen for questions about the **agreement** (is it running, when is the next charge, why did it stop) and the orders list for questions about a **delivery** (was it sent, was it invoiced, was it returned).

## Related

- [[apps-subscriptions]] — hub.
- [[apps-subscriptions-customer-controls]] — the same four actions from the customer's side.
- [[apps-subscriptions-failed-payments]] — what **Charge now** is usually recovering from.
- [[apps-subscriptions-billing-cycle]] — the cycle states shown in the history.
- [[orders]] — the orders produced by renewals.
- [[orders-history]] — the per-order log, distinct from the contract's own.
- [[customers-details]] — the customer the contract belongs to.
- [[settings-translations]] — per-language e-mail templates.

## Open questions

- Whether cancelling from the admin notifies the customer, or ends the contract silently.
