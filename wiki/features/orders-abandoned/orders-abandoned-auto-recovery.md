---
type: feature
nav_path: "Orders → Abandoned → Auto recovery"
route_name: (scheduled — every 180 seconds)
route_path: (no route — cron-driven)
aliases: ["Abandoned auto recovery", "Scheduled abandoned recovery", "Abandoned cart cron", "3-minute recovery job", "Abandoned cart reminder", "Автоматично възстановяване на изоставени колички"]
tags: [orders, abandoned, scheduled-job, cart-recovery, background-job]
plan_gates: ["abandoned_notification"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, detail view, eligibility, restore link, plan gates, cart lifecycle).

# Abandoned carts — Auto-recovery

## Purpose

Documents the **scheduled abandoned-cart recovery job** that runs every 180 seconds (3 minutes), automatically sending the restore-link email to every newly-abandoned cart that crosses the inactivity threshold — provided the store-wide **Abandoned cart reminder** master switch is ON.

When this is enabled, the merchant typically does NOT need to bulk-send manually from [[orders-abandoned-list-view]] — the cron already takes care of every newly-abandoned cart within minutes of crossing the threshold. The manual Send actions are for one-off nudges (per-cart resend, VIP customer, etc.).

## Where to find it

Not a screen — runs in the background. The merchant configures it via:

- The `abandoned_remainder` master switch on store settings ([[settings-cart]]).
- Observes its effect on [[orders-abandoned-list-view]] (sent carts get a `date_sent` timestamp and stop appearing in the "needs send" subset).

The job is catalogued alongside other background processes in [[background-queue-inventory]].

## What the merchant can do here

Nothing directly — this is a platform background job. The merchant influences it by:

- Toggling **Abandoned cart reminder** (`abandoned_remainder = yes` / `no`).
- Lowering / raising `abandoned_remainder_interval` to shift the threshold. See [[orders-abandoned-cart-lifecycle]].
- Configuring a recovery discount code that the auto-job will attach to every restore link. See [[marketing-discounts]].

## Settings & fields

The job reads two store settings:

- `abandoned_remainder` (yes / no) — master switch. When `no`, the job exits without doing anything. When `yes`, the job iterates over eligible carts.
- `abandoned_remainder_interval` (minutes, default 60, floor 30) — the inactivity threshold. See [[orders-abandoned-cart-lifecycle]] for the floor-clamp rule.

Plus the `abandoned_notification` plan cap (the job checks this BEFORE sending each email) — see [[orders-abandoned-plan-gates]].

## Business rules

### Runs every 180 seconds (3 minutes)

The platform runs the abandoned-cart sweep automatically every **180 seconds**. The job:

- Only runs when the store-wide setting **Abandoned cart reminder** is turned ON (`abandoned_remainder = yes`) — when OFF, the job exits without doing anything.
- Picks up every abandoned cart matching the same eligibility rules as the merchant's manual Send. See [[orders-abandoned-eligibility]] for the 7-rule check.
- Sends the restore link ONCE per cart, ever — carts that already have a `date_sent` timestamp are skipped (the auto-job filters `whereNull('date_sent')`). The auto-job CANNOT re-send.
- Counts toward the same `abandoned_notification` plan quota as the merchant's manual sends — the per-period cap applies uniformly.

### Same eligibility gate as manual sends

The scheduled job applies the same 7-rule eligibility gate as manual Send actions. See [[orders-abandoned-eligibility]]. Carts that fail any rule are silently skipped (and silently deleted on the same failure-cleanup path as manual Send).

### Sends are queued with a 10-second delay

The recovery email is dispatched onto the order-events queue with a **10-second delay** (same pipeline as status-change emails). Typical delivery: under 5 minutes from when the auto-job picks up the cart. So end-to-end, the customer typically receives the recovery email within **5–8 minutes** of the cart crossing the threshold:

- Threshold crossing (cart inactivity reaches `abandoned_remainder_interval`).
- + up to 3 minutes for the next auto-job cycle.
- + 10-second queue delay.
- + queue processing time (under 5 minutes in normal conditions).

### Subscriber email channel resolved at the cart's update time

For subscriber-only carts (no registered customer), the auto-job resolves the recovery email by looking up the subscriber's email-channel record that existed AT OR BEFORE the cart's last update timestamp. This avoids sending the restore link to a different person who later got linked to the same subscriber via shared UUID cookie. If no valid channel email is found at that point in time, the cart is silently DELETED instead of sent. See [[orders-abandoned-eligibility]].

### Auto-job + manual Send do not collide

The bulk Send from [[orders-abandoned-list-view]] and the auto-job apply the same `date_sent` skip — so manually bulk-sending a list of carts that the auto-job ALSO picks up that same minute can race, but only one Send actually fires (whichever updates `date_sent` first; the other observes the timestamp and skips). The merchant never observes a duplicate send caused by this race.

### Recovery discount code attaches the same way

When a recovery discount code is configured, the auto-job attaches it to the restore link's `{discount_code?}` URL segment exactly the same as the manual Send path. See [[orders-abandoned-restore-link]] for the URL contract.

### Plan-cap behaviour — silent skip per cart

When the `abandoned_notification` per-period cap is exhausted, the auto-job checks the platform code per cart and silently stops sending — the merchant does NOT receive a notification that the cap was hit. The cap state is observable on the dashboard counter (the same value as `plan.count.email.abandoned_notification`). See [[orders-abandoned-plan-gates]].

### Counter increments per send, persists across plan resets

Every successful auto-send increments `plan.count.email.abandoned_notification` — the same permanent counter as manual sends. The counter does NOT auto-reset on plan renewal or upgrade. To reset requires platform-staff intervention. See [[orders-abandoned-plan-gates]] for the persistence rationale.

## Plan gates

- `abandoned_notification` — numeric cap on sends per period. The auto-job checks this per cart before dispatching; when exhausted, silently skips.

The auto-job does NOT depend on `abandoned_orders` (the access gate) — the auto-job runs regardless of whether the merchant can reach the admin page. So stores on plans without `abandoned_orders` can still benefit from automated recovery if they have `abandoned_notification`. (In practice the two are usually granted together — see [[orders-abandoned-plan-gates]].)

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-eligibility]] — the 7-rule gate the auto-job applies.
- [[orders-abandoned-restore-link]] — the URL the auto-job emits.
- [[orders-abandoned-plan-gates]] — the numeric cap the auto-job checks.
- [[orders-abandoned-cart-lifecycle]] — the threshold the auto-job reads.
- [[settings-cart]] — `abandoned_remainder`, `abandoned_remainder_interval`.
- [[marketing-discounts]] — recovery discount code attached automatically.
- [[background-queue-inventory]] — catalogue of background jobs (auto-recovery + hourly cart cleanup live here).

## Open questions

None.
