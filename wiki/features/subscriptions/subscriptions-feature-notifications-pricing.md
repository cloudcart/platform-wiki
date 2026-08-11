---
type: feature
nav_path: "Profile → My subscriptions → Notifications & pricing"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["Subscription notifications", "Pre-billing notification", "Past-due email", "Subscription promo first cycle", "Subscription pricing", "Consultation modal Calendly", "Известия за абонамент"]
tags: [subscriptions, notifications, email, pricing, promo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions]]. See the hub for the other aspects (list columns, actions, status state machine, renewal retry, types).

# Subscriptions — notifications, pricing & UX divergence

## Purpose

This aspect documents the **outbound notifications** the platform sends around subscription events (7-day pre-billing notify, per-attempt failure emails on Past due, the absence of a "you-entered-Past-due" notification), the **promo first-cycle pricing** semantics (why the *Next billing amount* differs from the *Price* the merchant first paid), and the **UX divergence** between the legacy Smarty cancel flow (consultation modal + Calendly) and the modern Vue cancel flow (immediate).

## Where to find it

There is no dedicated UI surface for these settings — they are all platform-managed. The merchant sees:

- **Next billing amount** column on [[subscriptions]] — shows the regular price (not the promo first-cycle price). See [[subscriptions-feature-list-columns]].
- Inbox notifications — the pre-billing and per-attempt failure emails arrive at the email recipient configured on [[details-billing]].
- (Legacy Smarty only) The **consultation modal** when clicking Cancel on a Plan subscription at `/admin/subscriptions`.

## What the merchant can do here

- Update the **email recipient** for billing-related notifications via [[details-billing]] (invoicing details / recipient settings).
- Update the **saved card** at [[billing-cards]] before the next attempt to avoid further failure emails.
- Read the **Next billing amount** column to see what the next charge will actually be (regardless of what was paid on the promo first cycle).
- (Cannot) opt out of subscription notifications. The pre-billing notify and per-attempt failure emails fire automatically when their gating conditions are met.

## Settings & fields

There are no editable subscription-notification settings on the [[subscriptions]] screen itself. Recipient settings live on [[details-billing]]; card settings live on [[billing-cards]].

## Business rules

### "Past due + 7 days before billing" notify pipeline

The platform notifies the merchant 7 days before `next_billing_date` when:

- Status is Active
- `failed_attempts < 3`
- `next_billing_amount > 0`
- A `next_billing_date` exists

This pre-notification gives the merchant a window to update [[billing-cards]] before the first attempt fails. The email is sent to the recipient configured on [[details-billing]].

### Past-due notifications — per-attempt failure email only

When a subscription enters **Past due** (a renewal charge has failed), there is **NO separate "you entered Past Due" status-change notification**. The merchant only receives the per-attempt failure email — one per retry, on the 2 / 3 / 4 / 5 / 5-day backoff schedule (see [[subscriptions-feature-renewal-retry]] for the schedule).

The 7-days-before-billing pre-notify email is **ONLY sent for Active subscriptions** — Past-due subscriptions don't get pre-notifies (the platform assumes the merchant already knows because of the per-attempt failure emails). So a merchant who missed the per-attempt failure emails (e.g. filtered to spam) only finds out via the [[expired-subscription]] takeover screen once retries are exhausted and the daily sweep flips status to Expired.

### Promo first-cycle pricing — reverts to regular price at renewal

When a merchant buys a subscription with a discounted first cycle (e.g. through a promo landing URL), the **current `price`** charged at purchase is the promo amount, but the platform stores the regular catalog price in **`next_billing_amount`**. At renewal time, the new ongoing price is set to **the platform code** — so the renewal cycle moves up to the regular price automatically.

The merchant sees the regular price in the **Next billing amount** column from day one; the discount applies only to the FIRST cycle. If a merchant questions a higher charge after their first cycle, the explanation is: the promotional rate was first-cycle-only, and `Next billing amount` showed the regular rate the entire time.

This is also why the `Price` and `Next billing amount` columns on [[subscriptions-feature-list-columns]] can differ for the same row — `Price` is what the subscription is currently locked at; `Next billing amount` is what the *next* renewal will charge.

### Cancel-flow for Plan subscriptions opens a consultation modal first (Smarty only)

For **Plan** subscriptions (`model_type == 'plan_details'`), clicking **Cancel** in the **legacy Smarty UI** first opens the **consultation popup**:

> *"Are you sure you want to unsubscribe? We value each of our customers and strive to improve our service constantly. Let's discuss why you want to cancel your subscription."*

The merchant either books a Calendly consultation with a CloudCart account manager OR clicks *"I want to unsubscribe."* to confirm the actual cancellation. The Calendly URL is locale-specific — Bulgarian / Greek / Macedonian / English variants.

### Modern Vue cancels immediately — no consultation interstitial

The modern Vue UI at `/admin/details/subscriptions` cancels immediately on click without the consultation modal. This is a known UX divergence between the two generations of the UI.

The legacy `/admin/subscriptions` URL still shows the consultation modal because it's a thin redirect that loads the Smarty template stack underneath. A merchant who bookmarks the old URL will continue to see the consultation; a merchant arriving via the modern profile-dropdown navigation will not.

See [[subscriptions-feature-actions]] for the rest of the Cancel button's behaviour — including the toast on success and the backend rejection messages.

### Successful renewal sends an invoice email

When Renew (manual or automatic) succeeds, the platform issues a new invoice and sends an invoice email to the recipient configured on [[details-billing]]. This is the only positive-event notification in the subscription pipeline — there are no "renewal succeeded" / "subscription is back to Active" status-change emails beyond the invoice itself.

### Cancel does NOT trigger a notification

The Cancel action (whether self-service or platform-driven) does not fire a confirmation email to the merchant. The toast *"Subscription is canceled successfully"* on [[subscriptions-feature-actions]] is the only confirmation. A merchant who can't find a "subscription cancelled" email is not missing one — none is sent.

## Related

- [[subscriptions]] — hub.
- [[subscriptions-feature-actions]] — Cancel-flow UX divergence; toast messages.
- [[subscriptions-feature-renewal-retry]] — per-attempt failure email schedule.
- [[subscriptions-feature-status-state-machine]] — what status transitions trigger which notifications.
- [[subscriptions-feature-list-columns]] — Next billing amount column where promo pricing surfaces.
- [[billing-cards]] — saved card the merchant updates after a failure email.
- [[details-billing]] — recipient email for invoices and subscription notifications.
- [[expired-subscription]] — takeover screen that surfaces when retries are exhausted.

## Open questions

(None.)
