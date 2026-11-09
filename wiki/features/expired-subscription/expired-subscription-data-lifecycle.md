---
type: feature
nav_path: "Expired Subscription → Data lifecycle"
route_name: expired-subscription
route_path: /admin/expired-subscription
aliases: ["Expired subscription data lifecycle", "Data preservation during block", "Expired site destruction", "3 month destroy free", "6 month destroy paid", "Storefront vs admin during block", "Изтриване на данни след изтичане", "Запазване на данни при блокировка"]
tags: [base, core, expired-subscription, subscriptions, billing, blocking-screen]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

# Expired Subscription — data lifecycle & storefront

> Part of [[expired-subscription]]. See the hub for related aspects (redirect & allowlist, paid-plan timing, free Start Up plan).

## Purpose

This aspect answers the two questions merchants ask most once they understand they are blocked: **"Is my data still there?"** and **"Is my storefront still up for customers?"** The short answers: yes, all data is preserved during the blocked window (the takeover deletes nothing on its own), the storefront's customer-facing availability is decided independently of the admin takeover, and data is only ever destroyed by separate long-term cleanup sweeps (3 months for free sites, 6 months for paid).

## Where to find it

This is reached via the standard redirect — see [[expired-subscription-redirect]]. There is no dedicated screen for the data-lifecycle behaviour; it is the set of rules governing what happens to the merchant's data and storefront while (and long after) the takeover is in effect.

## What the merchant can do here

- **Recover all data intact** by clearing the unpaid state before the destroy window passes — for paid plans see [[expired-subscription-paid-timing]], for free plans see [[expired-subscription-free-plan]].
- **Still pull historical invoice PDFs** during the block (invoice downloads are not gated — see [[expired-subscription-redirect]]).
- The merchant **cannot** prevent the long-term destroy sweeps by any action on the takeover screen — the only way to preserve data is to clear the unpaid / inactive state before the window elapses.

## Settings & fields

No merchant-editable settings. The destroy windows below are platform constants:

| Site type | Destroy trigger | Window |
|-----------|-----------------|--------|
| Free Start Up | EXPIRED continuously | **3 months** — site database is dropped |
| Paid plan | EXPIRED continuously | **6 months** — site database is dropped |

## Business rules

### Data is preserved during the blocked window

The takeover does NOT delete any merchant data on its own. Products, customers, orders, settings, invoices, transaction history, themes, apps — everything stays in the database. The only thing the merchant loses is the ability to **view / edit / create** in the blocked admin screens. When the unpaid state clears, all data is exactly where they left it.

### After 3 months expired — free plans are destroyed

Free Start Up sites that have been EXPIRED for **3 months** are picked up by the daily expired-startup destroy sweep and their data is deleted from the platform (the underlying site database is dropped). After this, the merchant cannot recover their data even by paying — the data is gone.

### After 6 months expired — paid plans are destroyed

Paid sites that expire follow a longer ladder: the expired-site destroy sweep deletes paid sites that have been expired for **6 months**. Merchants who want to preserve their data MUST clear the unpaid state before this window passes. These long-term destroy sweeps are entirely separate from the takeover itself — they run as scheduled cleanup jobs, not as part of the blocking screen.

### What the Terms of Use promise

The Terms of Use commit CloudCart to keep a store's information for **30 days** after the last paid period ends (§11.11), and give the merchant 30 days after the contract ends to download their data (§19.3). The 3- and 6-month sweeps above are current practice and go beyond that commitment. Support gives the merchant 30 days as the window they can rely on. See [[terms-of-use-termination-data]].

### Storefront vs admin are independent decisions

The takeover only affects the **admin panel** at `/admin/*`. The storefront (the customer-facing site) is governed by the SITE's `status` field at the load-balancer / router layer, which may or may not suspend the storefront depending on the plan's grace policy. So the storefront may stay up for customers while the merchant sees the admin takeover — they are independent decisions made by different layers of the platform.

The APIs follow the store's status. While the store is Past due or Expired, or its plan has expired, the Storefront API (`/api/sf`) answers *"Store is currently unavailable."*, so a headless storefront stops working. The other two APIs refuse every call with HTTP **402**:

| API | Answer | Alert in the admin |
|---|---|---|
| JSON-API v2 (`/api/v2`) | `Payment Required`, detail *"You have failed payments"* | *"API: You have failed payments"* |
| Admin GraphQL (`/api/gql`) | code `PAYMENT_REQUIRED`, *"GraphQL API: You have failed payments"* | *"GraphQL API: You have failed payments"* |

The messages are in English whatever the admin language. A free-plan store that expired gets its own expiry message instead.

**The API check is stricter than the admin's.** The admin is blocked only when the plan subscription itself is Past due or Expired ([[expired-subscription-redirect]]). The APIs refuse whenever the store is Past due, and one past-due add-on (a search pack, an app, a feature pack) is enough, even with the plan paid ([[subscription-states]]). So the admin works while the integrations get 402.

**What clears it.** Paying what is past due: **Renew** on [[subscriptions]], or a successful automatic retry. When nothing else is past due and the plan is active, the store returns to Active at that moment and the next API call passes; nothing has to be re-checked by hand. A declined **first** purchase creates no subscription, so it never causes this 402. The alert is an Important alert, raised again unread on every refused call; paying stops it coming back, but the existing alert is not removed by itself.

## Related

- [[expired-subscription]] — hub.
- [[expired-subscription-paid-timing]] — the paid-plan recovery window before the 6-month destroy.
- [[expired-subscription-free-plan]] — the free-plan inactivity expiry before the 3-month destroy.
- [[subscriptions]] — where the merchant clears the unpaid state to preserve data.
- [[terms-of-use-termination-data]] — the contractual 30-day retention and export window.
- [[background-queue-inventory]] — the daily destroy sweeps (3-month expired-startup, 6-month expired-paid) that run as scheduled cleanup jobs.
- [[platform-rate-limits]] — the edge layer that decides storefront availability independently of the admin takeover.

## Open questions

(All resolved.)
