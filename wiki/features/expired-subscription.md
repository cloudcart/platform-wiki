---
type: feature
nav_path: "Expired Subscription"
route_name: expired-subscription
route_path: /admin/expired-subscription
aliases: ["Expired subscription", "Expired plan", "Plan expired screen", "Subscription expired", "Unpaid subscriptions block", "Admin access blocked", "Изтекъл абонамент", "Изтекъл план", "Блокиран достъп до администрацията"]
tags: [base, core, expired-subscription, subscriptions, billing, blocking-screen]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 3
---

# Expired Subscription

## Purpose

The **Expired Subscription** screen is the **admin-panel takeover** the merchant sees after their store plan subscription has lapsed (Past due, Expired, or otherwise unpaid). It is a deliberate dead-end: the plan middleware redirects almost every admin URL to `/admin/expired-subscription`, and the page opens a modal saying *"You have unpaid subscriptions!"* with a single primary button **Subscriptions** that routes the merchant to [[subscriptions]] so they can Renew, update their card, or buy a new plan.

The merchant cannot reach any other admin screen except a short allowlist (subscription / billing / invoice / contracts / settings / payment-providers / offers) while this state is in effect — see [[expired-subscription-redirect]]. The merchant's only path back to normal access is to **clear the unpaid plan subscription** — click Renew on the plan row (immediate fresh charge), update the saved [[billing-cards]] and let the next auto-retry succeed, or buy a new plan from [[plans]].

This is the same takeover screen the **free Start Up plan** funnels into when its inactivity threshold is exceeded — see [[expired-subscription-free-plan]].

## Where to find it

URL: `/admin/expired-subscription`.

The merchant does NOT navigate here intentionally — they are redirected by the plan middleware whenever they try to load any admin URL while their site is in an unpaid state. The redirect conditions, the hardcoded allowlist of exempt paths, and the 402-vs-302 mechanics are documented in full on [[expired-subscription-redirect]].

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages. Drill into the one that matches the question rather than reading every page.

- [[expired-subscription-redirect]] — how the merchant lands here: the two trigger conditions, the hardcoded billing-only allowlist, the 402 (AJAX) vs 302 (browser) responses, middleware-before-controller ordering, and the reseller redirect exception.
- [[expired-subscription-paid-timing]] — paid-plan timing: the dunning takeover at first failed renewal, the 2 / 3 / 4 / 5-day retry backoff, the ~30-day grace before the site-level Expired flip, canceled-no-grace, bank-transfer invoice windows, and immediate re-activation on a successful Renew.
- [[expired-subscription-free-plan]] — free Start Up plan: inactivity-driven expiry (30 days BG / 14 days DE), graduated warning emails, and automatic reactivation on log-in / sandbox disable.
- [[expired-subscription-data-lifecycle]] — data preservation during the block, the 3-month (free) / 6-month (paid) destroy sweeps, and why the storefront's availability is decided independently of the admin takeover.

## What the merchant can do here

- **Read the takeover message.** A centered confirmation modal opens automatically on mount, with a warning icon and the text **"You have unpaid subscriptions!"**.
- **Click the *Subscriptions* button** in the modal. This is the ONLY primary action — it routes the merchant to [[subscriptions]] where they can click Renew on the failing row, update their saved card via [[billing-cards]], or pick a new plan from [[plans]].
- **Use the profile dropdown** to navigate to any of the allowlisted screens (My subscriptions, Billing / Cards, Invoices, Logout, etc.). The standard sidebar nav is still rendered but every link except the allowlist redirects back to the takeover — see [[expired-subscription-redirect]].

The page itself shows the merchant's first + last name (read from the user profile) as the screen header — a small personalisation touch to confirm the merchant is looking at THEIR account's expired state, not a generic error page.

## What the merchant CANNOT do here

- **Access any product / order / customer / marketing / analytics / dashboard screen.** Every non-allowlisted URL bounces back to this takeover.
- **Dismiss the modal and continue using the admin.** The modal opens on mount and has only one action (Subscriptions). There is no "later" / "skip" button.
- **Wait it out — the page does not auto-renew.** No background activity on this screen fires a renewal. The merchant must click Renew on [[subscriptions]] or wait for the next daily auto-retry to attempt a fresh charge — see [[expired-subscription-paid-timing]].
- **Edit the subscription directly from this screen.** No editing surfaces are rendered — the merchant must navigate to [[subscriptions]] / [[billing-cards]] for any action.

## Settings & fields

This is a blocking-state takeover screen, not a settings screen. The only UI elements are:

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Screen header** | Shows the logged-in admin's first + last name + a list icon | — | Identifies whose account is blocked; useful when staff manage multiple stores |
| **Centered modal** | Warning icon + the text *"You have unpaid subscriptions!"* | Auto-opens on mount | Cannot be dismissed except by clicking the button |
| ***Subscriptions* button** | Routes the merchant to [[subscriptions]] | — | The single primary action; styled `btn-primary` |

There are NO input fields, NO Cancel button on the modal (`show-no: false`), and NO secondary actions. Clicking outside the modal area doesn't dismiss it — the modal IS the page's only meaningful content. The button calls a router push to the **My subscriptions** list (`subscriptions-list`, `/admin/details/subscriptions`).

## Business rules

The detailed rules live on the aspect pages. The cluster-level summary:

- **Two triggers fire the takeover** — the `plan_expired` flag, OR a Past due / Expired site status combined with a Past due / Expired plan subscription. Full conditions + the exempt-path allowlist on [[expired-subscription-redirect]].
- **Paid merchants get ~30 days** from `next_billing_date` to recover before the site-level Expired flip; CANCELED subscriptions get no grace; re-activation after a successful Renew is immediate. See [[expired-subscription-paid-timing]].
- **Free Start Up plans expire on inactivity** (30 days BG / 14 days DE) and auto-reactivate when the merchant logs in or disables sandbox during the warning window. See [[expired-subscription-free-plan]].
- **No data is deleted by the takeover itself.** Long-term destroy sweeps drop the site database after 3 months (free) / 6 months (paid) of continuous expiry. The storefront's customer-facing availability is decided independently. See [[expired-subscription-data-lifecycle]].

## Related

- [[subscriptions]] — the destination of the modal's *Subscriptions* button; where the merchant clicks Renew on the failing plan subscription to recover.
- [[subscription-lifecycle]] — the state machine that drives the takeover; explains the Past due → Expired transitions and the renewal retry schedule.
- [[billing-cards]] — saved card used for auto-retries; the merchant typically updates the card here before clicking Renew.
- [[billing-invoicing]] — invoice details required for any plan purchase.
- [[plans]] — destination when the merchant's expired plan is no longer in the catalog; they must buy a new plan from here.
- [[plans-purchase]] — the per-plan purchase flow.
- [[details-billing]] — transaction history showing the failed renewal attempts.
- [[plan-gates]] — the platform's broader paywall engine; the takeover is the top-level case where ALL gates fail because there's no active plan.
- [[background-queue-inventory]] — full catalogue of the daily renewal, notify, expire, and destroy jobs that drive the lifecycle.
- [[merchant-subscription-lifecycle]] — comprehensive merchant-question hub answering "what happens when my plan expires?" with cross-references to all related screens.

## Open questions

(All resolved.)
