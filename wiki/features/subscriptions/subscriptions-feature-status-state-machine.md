---
type: feature
nav_path: "Profile → My subscriptions → Status state machine"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["Subscription status", "Subscription state machine", "Active Canceled Past due Expired", "Subscription transitions", "Статус на абонамент"]
tags: [subscriptions, status, state-machine, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions]]. See the hub for the other aspects (list columns, actions, renewal retry, types, notifications & pricing).

# Subscriptions — status state machine

## Purpose

This aspect documents the **4-state status enum** that drives every subscription's lifecycle: **Active**, **Canceled**, **Past due**, **Expired**. It explains what each badge means in merchant terms, when the platform moves between them, and the two often-misunderstood rules: *Cancel does NOT immediately terminate access* and *Active does not mean currently being charged*.

## Where to find it

The Status column appears on the [[subscriptions]] list (`/admin/details/subscriptions`) as a coloured badge and is the default sort key (descending, so Active surfaces first). See [[subscriptions-feature-list-columns]] for the column context.

## What the merchant can do here

- Read the **Status** badge on any row to know whether the subscription is currently being honoured, has been cancelled, has a failing card, or has been terminated.
- Transition a subscription by clicking **Cancel** or **Renew** — see [[subscriptions-feature-actions]] for the button matrix and the transition semantics on click.
- Filter the list by Status to see, e.g., only the Expired rows. See [[subscriptions-feature-list-columns]] for the Filters surface.

## Settings & fields

### The 4 status values

The status enum has 4 values:

- **Active (1)** — successfully charged or within paid period. Default for a newly created paid subscription.
- **Canceled (0)** — the merchant clicked Cancel (or the platform cancelled on the merchant's behalf). The subscription remains usable until `next_billing_date` if it was still inside its paid period — `isPaid` returns true while `now < next_billing_date`. After that, the service stops.
- **Past due (2)** — last renewal charge failed AND `failed_attempts > 0`. The platform retries on a backoff schedule — see [[subscriptions-feature-renewal-retry]].
- **Expired (3)** — terminal state. Set by the daily `expire:subscriptions` sweep when `next_billing_date <= now - 1 month` (for non-Canceled) or `next_billing_date <= yesterday` (for Canceled). The auto-retry loop having stopped at `failed_attempts = 5` is a NECESSARY precursor but does NOT itself flip to Expired — the sweep does.

The Status filter values on the list map: Active=1, Canceled=0, Past due=2, Expired=3 (matches the platform constants).

### Transitions

Transitions surfaced via the UI buttons on [[subscriptions-feature-actions]]:

- **Cancel** (from Active or Past due) → Canceled. No proration / refund. The merchant continues to have access until `next_billing_date`.
- **Renew** (from Past due, Canceled, or Expired) → attempts to charge the saved card immediately. On success → Active with a new `next_billing_date` advanced by `billing_cycle` months. On failure → Past due (or stays Expired if no card / no plan).

Automatic transitions driven by the background pipeline:

- **Active → Past due** when a renewal charge fails and `failed_attempts > 0`.
- **Past due → Active** when a retry charge (manual Renew or automatic retry) succeeds.
- **Past due → Expired** when the daily `expire:subscriptions` sweep finds `next_billing_date <= now - 1 month`. See [[subscriptions-feature-renewal-retry]] for the sweep gating and how `failed_attempts = 5` relates.
- **Canceled → Expired** when the daily sweep finds `next_billing_date <= yesterday` (Canceled subscriptions don't need a full month grace window — they expire the day after their paid period ends).

## Business rules

### Cancel does NOT immediately terminate access

The Cancel button writes status = Canceled but does NOT cut off the service mid-cycle. The merchant keeps using the feature / app / plan until `next_billing_date`. After that date passes, the platform stops including this subscription in active-feature checks. There is no proration / refund. See [[subscriptions-feature-actions]] for the Cancel button's full behaviour and backend rejections.

### Renew triggers an immediate charge

Renew immediately fires a charge against the saved card on file (see [[billing-cards]]). On success, the cycle resets — new invoice issued, new `next_billing_date` set to `now + billing_cycle months`, `failed_attempts` zeroed, and an invoice email is sent to the recipient. On failure, `failed_attempts` increments and the subscription flips (or stays) Past due.

### Cancel is "soft" — the subscription stays in the database forever

Cancel sets status=0 but never deletes the row. Past cancelled subscriptions remain visible in the list (filtered by Status = Canceled) and their transaction history / invoices remain downloadable. This matters for accounting / audit follow-up — the merchant can always pull the invoice for a cancelled service.

### "Active" doesn't mean "currently being charged"

Active subscriptions with `next_billing_amount = 0` (e.g., free trials, complimentary add-ons issued by support) still show **Active** but don't generate transactions. The next billing field is empty when amount is 0. A merchant questioning "why is this Active but I'm not paying for it" should be told: complimentary / trial subscriptions still render Active because the service is active — billing simply hasn't been switched on.

### Past due is NOT terminal

A Past-due subscription is still receiving service (`isPaid` checks the period, not the status). The merchant can still use the feature / app / plan until `next_billing_date + 1 month` (the Expired sweep window). The Past-due badge is a warning, not a cutoff. Once the daily sweep flips it to Expired, the [[expired-subscription]] takeover screen kicks in for Plan subscriptions.

### Expired is terminal — re-arrival requires Renew

Expired is the only true terminal status. The merchant can still click **Renew** to attempt a fresh charge — if the card succeeds the subscription returns to Active with a new `next_billing_date` from today. Expired Plan subscriptions where the underlying plan is no longer active route the merchant to [[plans]] instead — see [[subscriptions-feature-actions]] for the plan-purchase modal.

### Visual hierarchy in the list

The default sort is Status descending (Past due = 2 and Expired = 3 outrank Active = 1, which outranks Canceled = 0 — but the actual sort order on the list surfaces Active first because the UI's "descending" is over the human-readable status label, not the numeric value). The practical effect: the merchant scrolls to find Canceled / Expired rows; warning states (Past due) and current state (Active) surface near the top.

## Related

- [[subscriptions]] — hub.
- [[subscriptions-feature-actions]] — the Cancel / Renew buttons that drive transitions.
- [[subscriptions-feature-renewal-retry]] — the retry pipeline + Expired sweep.
- [[subscriptions-feature-notifications-pricing]] — which transitions trigger which emails.
- [[expired-subscription]] — Plan-subscription takeover screen when status flips to Expired.
- [[billing-cards]] — saved card used by Renew.

## Open questions

(None.)
