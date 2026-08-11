---
type: concept
nav_path: "Concept → Abandoned cart recovery → Threshold & sweep"
aliases: ["Abandoned cart threshold", "abandoned_remainder_interval", "Cart abandonment timer", "Abandoned cart sweep", "Every-3-minute sweep", "Cart aged out"]
tags: [orders, cart, abandoned, recovery, threshold, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (eligibility, restore link, channels, bulk send, attribution, plan quota).

# Abandoned cart — threshold & platform sweep

## Definition

The transition from "active" to "abandoned" is purely a **time-since-last-cart-activity** check, not a state column. A cart becomes abandoned when its `updated_at` ages past **`abandoned_remainder_interval`** (default **60 minutes**; options **30 / 45 / 60 / 90 / 180**) on [[settings-cart]]. The master switch is **`abandoned_remainder`** on the same screen — when OFF, abandoned-cart sweep skips the store entirely.

The `cart` row's state is **inferred** from `updated_at + threshold`, not stored. The `AbandonedCart` model is an alias model extending `Cart` — it saves to the same `cart` table; the `whereAbandoned` scope applies the threshold + eligibility filter at query time. There is no separate "abandoned" table; the same row alternates between Active and Abandoned states by virtue of its `updated_at`'s age. (verify)

## Scope

Covered:

- The `abandoned_remainder_interval` setting and its discrete options (30 / 45 / 60 / 90 / 180 minutes).
- The `abandoned_remainder` master switch on [[settings-cart]].
- What resets `updated_at` (every cart change: add / remove / edit qty / apply code / change shipping).
- The platform-wide sweep job that runs **every 3 minutes** and dispatches per-site jobs.
- The up-to-3-minute latency between threshold crossing and the recovery email actually firing.
- The site-level skip rules the sweep applies before processing any cart.

Not covered here:

- The seven-check eligibility filter per cart — see [[abandoned-cart-eligibility]].
- The restore-link URL and click behaviour — see [[abandoned-cart-restore-link]].
- The `abandoned_notification` plan-feature quota that gates sends — see [[abandoned-cart-plan-quota]].

## Contrasts

- **Threshold crossing vs eligibility pass** — crossing the timer is necessary but not sufficient. A cart older than `abandoned_remainder_interval` only triggers a recovery email if it ALSO passes the seven-check eligibility filter and the two-layer marketing consent. See [[abandoned-cart-eligibility]].
- **Cart `updated_at` vs cart `created_at`** — abandonment is measured from `updated_at` (last interaction), not `created_at`. A customer who keeps editing the cart resets the timer with each change.
- **Sweep latency vs threshold** — the recovery email fires at *threshold + up to 3 min*, not exactly at threshold. A cart abandoned at 10:00 with a 60-min threshold gets the email between 11:00 and 11:03.

## Where it applies

### What resets `updated_at`

Every cart-modifying action resets the timer:

- Add line item / remove line item / change quantity.
- Apply / remove discount code.
- Change shipping method / shipping address / billing address.
- Any storefront cart API write.

What does NOT reset `updated_at`:

- Read-only views of the cart (cart drawer open, cart page view) — these don't touch the cart row.
- Customer logging in without changing the cart.

### The every-3-minute platform sweep

A platform-wide scheduled job runs **every 180 seconds** on the system queue. Per tick:

1. Iterates over every store on the platform.
2. Dispatches one per-site job per store.
3. The per-site job **skips the store entirely** if any of these are true:
   - The site is plan-expired.
   - The site is in maintenance mode.
   - The site doesn't have the `abandoned_notification` plan feature (see [[abandoned-cart-plan-quota]]).
   - The master `abandoned_remainder` switch is OFF.
4. Otherwise: loads abandoned carts that haven't been emailed yet (`date_sent IS NULL`), runs each through the seven-check eligibility filter (see [[abandoned-cart-eligibility]]), generates a restore code, dispatches the recovery email, and stamps `date_sent`.

So the recovery email fires after `abandoned_remainder_interval` **plus up to 3 minutes** of sweep latency.

### Quota-exhaustion behaviour mid-sweep

The auto-sweep job throws a a plan-restriction error exception when the `abandoned_notification` quota is exhausted mid-run — the job **aborts at the first failing cart**, so subsequent carts in the same batch are NOT processed even if some could have qualified. The next sweep tick re-attempts from scratch. This is invisible to the merchant; the only visible signal is `date_sent` stamps stalling out before all eligible carts are sent. (verify)

### Example: 60-min timer, customer recovers after 6 hours

1. Customer adds 2 items at 10:00 → cart created, `updated_at = 10:00`.
2. Customer browses, removes an item at 10:05 → `updated_at = 10:05`.
3. Customer closes browser at 10:10 without checking out.
4. At **11:05** (60 min after last update), the next sweep tick marks the cart as abandoned. Cart appears in [[orders-abandoned]].
5. Sweep fires recovery email at **11:06** (next sweep tick after threshold). `date_sent = 11:06`. `abandoned_notification` counter increments by 1.
6. Customer ignores the email; cart sits in [[orders-abandoned]] with `date_sent = 11:06` stamp.
7. **17:00** — customer opens the email, clicks the restore link (see [[abandoned-cart-restore-link]]).

### Choosing the right threshold

- **30–45 min** — aggressive. Catches short abandonment windows; high recovery email volume; risk of "I just stepped away" annoyance.
- **60 min (default)** — balanced. Catches most genuine abandonments while letting transient distractions resolve.
- **90–180 min** — conservative. Lower email volume; misses recoveries the customer might have responded to within 60 min.

Lower the threshold to catch more carts; raise it to reduce email volume and quota pressure on [[abandoned-cart-plan-quota]].

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-eligibility]] — the seven-check filter that runs AFTER the threshold is crossed.
- [[abandoned-cart-plan-quota]] — the plan-feature quota that gates whether the sweep runs.
- [[settings-cart]] — `abandoned_remainder` master switch + `abandoned_remainder_interval` timer.
- [[cart]] — the cart entity whose `updated_at` drives the threshold.
- [[orders-abandoned]] — the merchant-facing list of carts past the threshold.
- [[cart-vs-order-lifecycle]] — the full Active → Abandoned → Recovered / Lost state machine.
- [[background-queue-inventory]] — catalogue of background processes including the 3-min sweep timing and Queue View visibility.

## Open Questions

None.
