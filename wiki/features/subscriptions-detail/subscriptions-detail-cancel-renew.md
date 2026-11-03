---
type: feature
nav_path: "Profile → My subscriptions → Subscription → Cancel / Renew"
route_name: admin.subscriptions.cancel
route_path: /admin/subscriptions/{id}/cancel
aliases: ["Subscription cancel", "Subscription renew", "Cancel subscription", "Renew subscription", "canActivate reactivation", "Откажи абонамент", "Поднови абонамент"]
tags: [subscriptions, cancel, renew, billing, account, modern-vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions-detail]]. See the hub for the other aspects (on-screen display, lifecycle side-effects).

# Subscription detail — Cancel & Renew

## Purpose

What the **Cancel** and **Renew** actions actually do at the endpoint level. On the modern Vue UI these buttons live in the [[subscriptions]] list page's Actions column, but they apply to one specific subscription and trigger the behaviour documented here. This page covers the cancel guards, the renew matrix per subscription type, the free-reactivation rule, charge success / failure handling, and the price-edit protection.

## Where to find it

The action buttons appear in the Actions column of [[subscriptions]] for each row. The legacy `/admin/subscriptions/<unique_id>` detail page and the modern Vue detail screen ([[subscriptions-detail-screen]]) are both read-only display — neither hosts the buttons. Cancel hits `admin.subscriptions.cancel`; Renew hits `admin.subscriptions.renew` (both keyed by the numeric `{id}`).

## What the merchant can do here

- **Cancel** a single subscription (when not blocked by a contract / unpaid turnover).
- **Renew** a subscription that is past due, canceled, or expired — either as a free reactivation or a fresh charge depending on remaining paid time.

The merchant cannot pause / suspend, cannot change the renewal amount, and cannot change the saved card per subscription (see [[subscriptions-detail-screen]] for the "cannot do" surface).

## Settings & fields

This action surface reads / writes: `status`, `next_billing_date`, `next_billing_amount`, `failed_attempts`, `last_try_at`, `discount_id`, `lta_contract_id`. Field meanings are tabulated on [[subscriptions-detail-screen]].

## Business rules

### Cancel — endpoint behaviour (`admin.subscriptions.cancel`)

Hitting the cancel endpoint for a subscription:

1. Validates that the subscription is NOT bound to an LTA contract — otherwise rejects with *"This subscription has a related contract. Contact your account manager!"*.
2. Validates that the subscription has no unpaid plan turnover — otherwise rejects with *"This subscription has unpaid turnover amount. Contact your account manager!"*.
3. Sets status = Canceled (`0`).
4. Updates the store's site status flag accordingly (so platform site-level access checks reflect the cancelled state) — the full cascade is on [[subscriptions-detail-lifecycle-effects]].

The merchant retains access to the service until `next_billing_date`, because the paid-check returns true while `now < next_billing_date && status == Canceled`. Once `next_billing_date` passes, the service stops being included in active-feature checks. There is no proration, no partial refund, and no end-of-period grace beyond the already-paid cycle.

### Renew — endpoint behaviour (`admin.subscriptions.renew`)

Hitting the renew endpoint:

1. **For Plan subscriptions** — first verifies the underlying plan is still active. If not, forces Past due, updates the site status, and redirects to [[plans]] (response includes `redirect_url`).
2. **For Plan subscriptions with unpaid turnover** — pays the turnover invoice first; renewal of the subscription itself only proceeds after.
3. **For LTA-contract subscriptions** — delegates to the contract's renew flow (the contract's offer item is matched and its status synced).
4. **For all others** — if `canActivate` is true (status != Active AND `next_billing_date` > end of today), simply activates without a fresh charge. Otherwise, calls the regular renew which issues a new invoice, charges the saved card, advances `next_billing_date` by `billing_cycle` months, zeros `failed_attempts`, and sends the invoice email.

On a successful charge the platform also fires the `SubscriptionRenew` and `InvoiceCreate` events, sends GA / GA4 purchase analytics events, records Google Ads / Facebook Ads conversions (when `gclid` / `fbclid` cookies are present), and installs the App / activates the Feature Pack on the store (when relevant) — see [[subscriptions-detail-lifecycle-effects]] for the app re-install detail.

On a failed charge: `failed_attempts` increments, `last_try_at` is set to now, and status flips to Past due if not already past-due / expired. The retry backoff schedule is documented on [[subscriptions-detail-lifecycle-effects]].

### canActivate — when Renew is a "free reactivation"

If the subscription was just cancelled but the merchant still has paid time remaining (`next_billing_date > now`), Renew simply re-activates the subscription **without** making a new charge — it just flips status back to Active. This handles the "I cancelled by mistake, restore me" case.

### Renewal advances next_billing_date in months

The next billing date is computed as `last_next_billing_date + billing_cycle months`. If the last date was already more than a month in the past (e.g. the subscription was Past due and the merchant just renewed manually), the platform takes `now + billing_cycle` instead — so renewals never accidentally schedule the next charge in the past.

### Price-edit protection

The platform explicitly rejects any attempt to change the `next_billing_amount` (the renewal price) with the validation error *"Changing the next billing amount is disabled"*. Pricing changes go through the purchase / upgrade flow, not the subscription edit surface.

### Discount carry-over

When the subscription has a `discount_id`, the renewal applies that same discount automatically — no merchant action needed. Discounted subscriptions show the discounted `next_billing_amount` on [[subscriptions-detail-screen]].

### Permission — owner-only

Only store owners can trigger Cancel / Renew (the My subscriptions surface is gated to the owner via the profile dropdown).

## Related

- [[subscriptions-detail]] — hub.
- [[subscriptions]] — the list page that hosts the Cancel / Renew buttons.
- [[plans]] — where a deactivated Plan subscription redirects on renew.
- [[billing-cards]] — saved card charged on a fresh renewal.
- [[details-billing]] — invoicing details applied to each renewal invoice.

## Open questions

(All resolved.)
