---
type: concept
nav_path: "Concept → Abandoned cart recovery → Plan quota"
aliases: ["abandoned_notification", "abandoned_notification plan feature", "Abandoned notifications quota", "plan.count.email.abandoned_notification", "Recovery plan gate", "Feature limit warning abandoned"]
tags: [orders, cart, abandoned, recovery, plan, quota, concepts]
plan_gates: ["abandoned_notification"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, eligibility, restore link, channels, bulk send, attribution).

# Abandoned cart — `abandoned_notification` plan quota

## Definition

The entire recovery flow is gated by the **`abandoned_notification`** plan feature (see [[plan-gates]]). Three regimes:

- **Feature absent / disabled on plan** — the automated sweep (see [[abandoned-cart-threshold]]) skips this store entirely; the bulk **Send restore link** action shows a paywall on the single-cart Send path (see [[abandoned-cart-bulk-send]]).
- **Feature present with numeric cap** — each successful send increments **`plan.count.email.abandoned_notification`** (a row in the `Setting` table). The counter at the top of [[orders-abandoned]] (*"Abandoned count: X"*) shows the running total for the period.
- **Quota exhausted mid-period** — further sends are blocked: the single-cart Send path surfaces a hard paywall; the bulk and auto-sweep paths fail silently (see [[abandoned-cart-bulk-send]]).

The counter is **centralised in one setting row** and **shared across the platform** — when external recovery providers (e.g. Mobica integrations under [[apps]]) plug into the abandoned-cart flow, their sends also count against this same meter.

## Scope

Covered:

- The `abandoned_notification` plan feature and the three regimes (absent / capped / exhausted).
- The `plan.count.email.abandoned_notification` Setting-row counter.
- The "Abandoned count: X" running total on [[orders-abandoned]].
- The merchant-facing "feature limit warning" message + paywall path.
- Period rollover behaviour — counter resets, `date_sent` stamps preserved.
- The shared-meter rule — third-party recovery integrations consume the same quota.
- Path-specific failure UX on quota exhaustion.

Not covered here:

- Per-path failure UX in general (silent-delete on bulk, hard-paywall on single, silent-skip on sweep) — see [[abandoned-cart-bulk-send]].
- The seven-check eligibility filter and consent gate that runs BEFORE quota check — see [[abandoned-cart-eligibility]].
- The plan-feature mechanics generally — see [[plan-gates]].

## Contrasts

- **Quota exhaustion vs eligibility failure** — eligibility failures (no email, expired token, marketing consent off) happen *before* the quota counter is touched. Quota exhaustion happens at send time, after all eligibility checks have passed.
- **Hard paywall vs silent block** — only the single-cart Send path on [[orders-abandoned]] surfaces a hard paywall on exhausted quota. The bulk Send and the auto-sweep both block silently. See [[abandoned-cart-bulk-send]] for the per-path failure semantics.
- **Period counter vs cart `date_sent`** — period rollover (plan renewal) zeros the `plan.count.email.abandoned_notification` counter. The underlying carts retain their `date_sent` stamps independent of the counter. So a cart with `date_sent` set in the previous period stays "already-sent" from the auto-sweep's perspective (which filters `date_sent IS NULL`), but manual re-sends are still permitted under the new period's fresh quota.

## Where it applies

### Three regimes

| Plan feature state | Auto-sweep | Manual bulk Send | Manual single-cart Send |
|---|---|---|---|
| **Absent / disabled** | Site skipped entirely | Shows paywall | Hard paywall (a plan-restriction error) |
| **Present with quota remaining** | Sends, increments counter | Sends, increments counter | Sends, increments counter |
| **Present, quota exhausted** | Silent skip; a plan-restriction error aborts the batch (see [[abandoned-cart-threshold]]) | Silent delete (mailer's underlying quota check) | Hard paywall (a plan-restriction error) |

(verify the exact silent-vs-hard split on each path against the bulk and sweep code paths)

### The `plan.count.email.abandoned_notification` counter

Every successful send (auto-sweep or manual) increments `plan.count.email.abandoned_notification` in the `Setting` table. Properties:

- **Single row** — one Setting row holds the platform's running total of abandoned-cart notifications consumed in the current plan period.
- **Centralised meter** — when external recovery providers (e.g. Mobica integrations under [[apps]]) plug into the abandoned-cart flow, their sends also count against this same meter.
- **Period rollover** — when the merchant's plan period rolls over (e.g. monthly), this counter zeros. `date_sent` stamps on individual carts persist and are independent of the counter.
- **Surface to merchant** — shown at the top of [[orders-abandoned]] as *"Abandoned count: X"*. The merchant uses this as the at-a-glance "how much quota have we used this period" indicator.

### Single-cart Send — the only path with a clean paywall

The per-cart **Send** action on a single cart's panel (from [[orders-abandoned]]) is the only path that explicitly checks the platform code BEFORE attempting to send and throws a a plan-restriction error exception with the merchant-facing "feature limit warning" message when the quota is exhausted. The merchant sees a paywall dialog with a link to [[plan-features]] to purchase more `abandoned_notification` quota via a feature-pack top-up.

The bulk Send restore link action and the auto-sweep both fail silently on quota exhaustion (see [[abandoned-cart-bulk-send]] for the path-specific failure UX). Merchants relying on bulk Send won't see a clear "you've hit your limit" signal — they'll just see "X emails sent" toasts where X is smaller than expected and carts disappearing from the list silently.

### What happens when the auto-sweep hits exhaustion mid-batch

The auto-sweep job throws a a plan-restriction error exception when the `abandoned_notification` quota is exhausted mid-run — the job **aborts at the first failing cart**, so subsequent carts in the same batch are NOT processed even if some could have qualified by per-cart criteria. The next sweep tick re-attempts from scratch but hits the same exhausted-quota check immediately. (verify) This is invisible to the merchant; the only visible signal is `date_sent` stamps stalling out before all eligible carts are sent, and the "Abandoned count: X" total plateauing at the cap.

### Period rollover behaviour

On plan renewal:

- The `plan.count.email.abandoned_notification` counter zeros.
- Carts that had `date_sent` set in the previous period **keep** their `date_sent` stamps.
- The auto-sweep continues to skip those carts (it filters `date_sent IS NULL`).
- The manual bulk and single-cart Send paths CAN re-send those carts (re-sends are not blocked by `date_sent` in the manual flow — see [[abandoned-cart-bulk-send]]) and consume fresh quota for the new period.

So the period rollover effectively un-blocks the manual paths against historical carts, while the auto-sweep stays focused on newly-eligible (`date_sent IS NULL`) carts.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-bulk-send]] — the per-path failure UX (silent-delete vs hard paywall vs silent-skip on quota exhaustion).
- [[abandoned-cart-threshold]] — the auto-sweep that consumes quota silently on each successful send.
- [[abandoned-cart-eligibility]] — what filters apply BEFORE the quota counter is touched.
- [[plan-gates]] — the plan-feature mechanism generally; lists `abandoned_notification` among the gates.
- [[plan-features]] — paywall destination when the merchant wants to top up the quota.
- [[orders-abandoned]] — surfaces the "Abandoned count: X" running total.
- [[settings-cart]] — `abandoned_remainder` and `abandoned_remainder_interval` settings on the same screen.
- [[apps]] — third-party recovery integrations that share the same quota meter.

## Open Questions

- Confirm the exact merchant-facing wording of the "feature limit warning" string surfaced by a plan-restriction error on the single-cart Send path. (verify against the message catalogue)
