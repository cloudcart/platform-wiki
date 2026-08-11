---
type: feature
nav_path: "Expired Subscription → Free Start Up plan"
route_name: expired-subscription
route_path: /admin/expired-subscription
aliases: ["Expired subscription free plan", "Start Up plan inactivity", "Free plan expiry thresholds", "Inactivity takeover", "Sandbox expiry", "Изтекъл безплатен план", "Неактивност Start Up план"]
tags: [base, core, expired-subscription, subscriptions, billing, blocking-screen]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Expired Subscription — free Start Up plan

> Part of [[expired-subscription]]. See the hub for related aspects (redirect & allowlist, paid-plan timing, data lifecycle).

## Purpose

This aspect explains how the **free Start Up plan** funnels into the same takeover screen — but driven by **inactivity** rather than payment failure. There is nothing to charge on a free plan, so the platform expires it after a country-specific number of days with no admin login / no sandbox disable. Crucially, unlike the paid path, the free-plan takeover is **not permanent**: logging in during the warning window automatically reactivates the store.

## Where to find it

Reached via the standard redirect — see [[expired-subscription-redirect]]. The merchant sees the identical *"You have unpaid subscriptions!"* modal documented on the hub. For free-plan merchants the path back to normal access is simply to log in / disable sandbox (which auto-reactivates), or to buy a paid plan from [[plans]].

## What the merchant can do here

- **Return to normal by logging in / disabling sandbox** during the warning window — this auto-reactivates the store with no payment.
- **Buy a paid plan** from [[plans]] to leave the free tier entirely.
- A free-plan merchant who is **reseller-onboarded** does not see this screen at all — the middleware sends them to [[plans]] instead (see [[expired-subscription-redirect]]).

## Settings & fields

No merchant-editable settings. The inactivity thresholds below are platform constants keyed by the issuer company of the store:

| Issuer | Trigger condition | Threshold |
|--------|-------------------|-----------|
| **BG** (issuer company 5) | No admin login | **30 days** |
| **BG** | Sandbox mode enabled | **30 days** |
| **DE** (issuer company 7) | No admin login | **14 days** |
| **DE** | Sandbox mode enabled | **14 days** |

The merchant gets graduated warning emails at thirds of the threshold before the full expiry (notify counter at 1/3 then 2/3 of the limit, then the actual EXPIRED transition).

## Business rules

### Free Start Up plan — by-issuer thresholds

For the free `startup` plan, expiry is driven by **inactivity** instead of payment failures. The daily free-site-expiry sweep flips the site to EXPIRED when the relevant threshold above is exceeded — either no admin login or sandbox mode left enabled for the full window. BG-issued stores get 30 days; DE-issued stores get 14 days.

### Warning emails before expiry

The platform sends graduated warning emails as the inactivity window elapses: a `notify_count` advances at 1/3 then 2/3 of the threshold, then the actual EXPIRED transition fires. So a BG merchant (30-day window) is warned at roughly day 10 and day 20 before the takeover on day 30.

### Logging in auto-reactivates during the warning window

When the merchant returns to log in / disables sandbox during the warning window, the site is **automatically reactivated** — the free-plan-expiry check flips status back to ACTIVE and clears the `notify_count`. So the takeover is not permanent for free-plan merchants: logging in resets the timer. This is the key difference from the paid path, where recovery requires a successful charge (see [[expired-subscription-paid-timing]]).

### Reseller free-plan merchants never see this screen

If a free-`startup` merchant's site is flagged with a partner reseller (e.g., `reseller_id = 157` = UniCredit), the middleware redirects to [[plans]] instead of the takeover — their plan is governed by the partner contract, not by the inactivity sweep. The full redirect-exception rule is on [[expired-subscription-redirect]].

### Data destruction is harsher on free than paid

A free Start Up site that stays EXPIRED long enough is eventually **destroyed** (its data deleted) on a far shorter ladder than paid sites. See [[expired-subscription-data-lifecycle]] for the 3-month free vs 6-month paid destroy windows.

## Related

- [[expired-subscription]] — hub.
- [[plans]] — where free-plan merchants buy a paid plan, and the redirect destination for reseller-onboarded free merchants.
- [[subscriptions]] — the allowlisted subscriptions list reached from the modal.
- [[subscription-lifecycle]] — the state machine covering the EXPIRED / reactivation transitions.
- [[background-queue-inventory]] — the daily free-site-expiry and warning-notify jobs that drive the inactivity timing.
- [[merchant-subscription-lifecycle]] — merchant-facing hub answering "what happens when my plan expires?".

## Open questions

(All resolved.)
