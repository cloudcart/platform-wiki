---
type: feature
nav_path: "Profile → My subscriptions → Subscription → Lifecycle effects"
route_name: admin.subscriptions.renew
route_path: /admin/subscriptions/{id}/renew
aliases: ["Subscription lifecycle effects", "Subscription site-status cascade", "App subscription expiry", "Subscription audit log", "Subscription dunning emails", "Ефекти от абонамент"]
tags: [subscriptions, lifecycle, billing, dunning, audit, modern-vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions-detail]]. See the hub for the other aspects (on-screen display, cancel/renew endpoint behaviour).

# Subscription detail — lifecycle side-effects

## Purpose

What happens to the store, the installed app, and the merchant's notifications **after** a subscription changes state (the Cancel / Renew mechanics that trigger these are on [[subscriptions-detail-cancel-renew]]). This page answers merchant questions like *"I cancelled my plan, what happens to my store?"*, *"my app subscription expired, is my data gone?"*, and *"why am I (not) getting renewal reminder emails?"*.

## Where to find it

These effects are not a screen — they are downstream consequences observed across the store. The merchant sees the resulting state on [[subscriptions-detail-screen]] (status badge), on [[expired-subscription]] (the takeover screen for a fully expired Plan), and in the renewal / failure emails. CloudCart support sees the audit log.

## What the merchant can do here

Nothing to click — these are automatic effects. The merchant influences them only by performing Cancel / Renew on [[subscriptions-detail-cancel-renew]] or by letting a subscription lapse.

## Settings & fields

Effects are driven by `status`, `next_billing_date`, `failed_attempts`, `last_try_at`, and `model_type`. Field meanings are tabulated on [[subscriptions-detail-screen]].

## Business rules

### Plan-subscription cancellation cascades to site status

When a **Plan**-type subscription is cancelled, the store's site record is updated with the new status, and (when status flips to Past due / Expired) the site enters the dunning state. After the paid cycle ends, the merchant sees [[expired-subscription]] when they log in, until they buy a new plan.

For non-Plan subscriptions (apps / features / services / themes), cancellation only affects that specific subscription's state — the store's overall plan stays active.

### Activation also re-installs the underlying App

When a renew (after expiry) succeeds for an **App**-type subscription, the platform re-installs the app on the store (per the renewal flow). For **Feature-pack** subscriptions, the activate-app job runs to re-apply the feature-pack's limits. The merchant doesn't need to re-install / re-configure anything after a successful late renewal.

### App-subscription expiry — app stays installed, features stop working

When an Application subscription transitions to **Expired**, the app is NOT forcibly uninstalled:

- The app's database tables, settings, and code REMAIN in place on the store.
- The platform's "is this subscription paid?" check returns false → the app's features stop working for the merchant (e.g. the storefront drops the feature, admin screens block actions).
- A subscription-expire event is recorded in the site event log (visible to CloudCart support, not surfaced as a merchant-facing log).
- On successful late renewal, the platform re-applies the feature limits — the app starts working again without requiring re-install.

So a merchant who lets an app subscription lapse can recover by paying late; their app data isn't wiped.

### Renewal failures share retry slot across subscriptions

Each subscription tracks its own `failed_attempts` and `last_try_at`. The backoff schedule (2 / 3 / 4 / 5 days between attempts; up to 5 total attempts before the auto-retry loop stops) is **per-subscription** — different subscriptions on the same card retry independently.

### Audit log — every Cancel / Renew is recorded

The platform records every subscription state change (Active → Cancelled, Cancelled → Active via Renew, etc.) in a subscription log. Each log row captures the actor implicitly via the admin session context — the admin email at the time of the change is recorded. The log does NOT have an explicit "merchant-clicked vs system-triggered" flag, so a system retry that flips the status will be attributed to whichever admin was last active in session (or null if triggered by a scheduled job with no session).

The log is currently visible only to CloudCart support — it's not surfaced as a merchant-facing history view.

### Dunning emails — only Active subscriptions get the 7-day pre-notify

The pre-billing notification email (sent ~7 days before next billing date) fires ONLY for subscriptions in **Active** status. Past-due subscriptions do NOT get a pre-billing reminder — they only receive the per-retry failure email after each failed charge attempt (every 2–5 days during the backoff schedule). Once the subscription transitions to Expired or Cancelled, no further automated emails are sent for that subscription.

## Related

- [[subscriptions-detail]] — hub.
- [[subscriptions-detail-cancel-renew]] — the actions that trigger these effects.
- [[expired-subscription]] — the takeover screen when a Plan subscription expires fully.
- [[plans]] — where a deactivated Plan subscription redirects on renew.
- [[merchant-subscription-lifecycle]] — merchant-question hub for the full billing lifecycle.

## Open questions

(All resolved.)
