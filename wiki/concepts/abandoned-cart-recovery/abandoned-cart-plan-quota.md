---
type: concept
nav_path: "Concept → Abandoned cart recovery → Plan quota"
aliases: ["abandoned_notification", "abandoned_notification plan feature", "Abandoned notifications quota", "plan.count.email.abandoned_notification", "Recovery plan gate", "Feature limit warning abandoned", "Abandoned cart e-mails per plan year", "Лимит имейли за изоставени колички", "Общо изпратени съобщения"]
tags: [orders, cart, abandoned, recovery, plan, quota, concepts]
plan_gates: ["abandoned_notification"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, eligibility, restore link, channels, bulk send, attribution).

# Abandoned cart — `abandoned_notification` plan quota

## Definition

The entire recovery flow is gated by the **`abandoned_notification`** plan feature (see [[plan-gates]]). The allowance is **yearly on every billing period** (monthly, yearly, two years). Three regimes:

- **Feature absent / disabled on plan** — the automated sweep (see [[abandoned-cart-threshold]]) skips this store entirely; the single-cart **Send** action shows a paywall (see [[abandoned-cart-bulk-send]]).
- **Feature present with numeric cap** — each e-mail sent increments **`plan.count.email.abandoned_notification`**. The counter at the top of [[orders-abandoned]] (*"Total sent messages: X"*, BG *"Общо изпратени съобщения: X"*) shows the count for the current plan year.
- **Quota exhausted mid-year** — the single-cart Send path surfaces a hard paywall; the auto-sweep stops, and within 12 hours the platform switches **Abandoned cart reminder** off (see "When the allowance runs out" below).

**The plan year runs from the plan purchase date**: a plan bought on 15 March counts 15 March to 15 March. A store with no plan subscription (free, trial) counts by calendar year.

**The limit** is the plan's `abandoned_notification` value plus any paid feature packs for the same feature. A send is allowed while the count is below it.

## Scope

Covered:

- The `abandoned_notification` plan feature and the three regimes (absent / capped / exhausted).
- The `plan.count.email.abandoned_notification` counter and the plan year it counts.
- The "Total sent messages: X" counter on [[orders-abandoned]].
- The merchant-facing "feature limit warning" message + paywall path.
- A new plan year, and what happens at the cap (incl. the automatic reminder switch-off).

Not covered here:

- Per-path failure UX in general — see [[abandoned-cart-bulk-send]].
- The seven-check eligibility filter and consent gate that runs BEFORE quota check — see [[abandoned-cart-eligibility]].
- The plan-feature mechanics generally — see [[plan-gates]].

## Contrasts

- **Quota exhaustion vs eligibility failure** — eligibility failures (no email, expired token, marketing consent off) happen *before* the quota counter is touched. Quota exhaustion happens at send time, after all eligibility checks have passed.
- **Hard paywall vs delayed switch-off** — the single-cart Send path on [[orders-abandoned]] surfaces a hard paywall on exhausted quota. The auto-sweep stops with no message at that moment; the switch-off and the alert follow within 12 hours. See [[abandoned-cart-bulk-send]] for the per-path failure semantics.
- **Plan-year counter vs cart `date_sent`** — the start of a new plan year zeros the `plan.count.email.abandoned_notification` counter. The underlying carts retain their `date_sent` stamps independent of the counter. So a cart with `date_sent` set in the previous plan year stays "already-sent" from the auto-sweep's perspective (which filters `date_sent IS NULL`), but a re-send from the cart's panel is still permitted under the new year's allowance.

## Where it applies

### Three regimes

| Plan feature state | Auto-sweep | Manual single-cart Send |
|---|---|---|
| **Absent / disabled** | Site skipped entirely | Hard paywall |
| **Present with quota remaining** | Sends, increments counter | Sends, increments counter |
| **Present, quota exhausted** | Stops; the rest of the batch waits (see [[abandoned-cart-threshold]]) | Hard paywall |

### The `plan.count.email.abandoned_notification` counter

Each e-mail that actually goes out from the auto-sweep, the single-cart Send or the Admin GraphQL `sendRestoreEmail` mutation increments it. A cart dropped without sending (no e-mail, no products, already ordered) uses no allowance. Properties:

- **One number everywhere** — plan usage, the *"Total sent messages: X"* counter, the single-cart Send check and the mutation all use it.
- **No scheduled reset** — no timer zeros it. Whenever the count is read or a send is counted, it is matched to the current plan year and zeroed if a later year has begun.
- **A later plan year restarts it** — once a later plan year starts, the count restarts from zero. `date_sent` stamps on individual carts persist and are independent of the counter.
- **A renewal alone does not reset it** — plans renewed or bought from the admin are treated the same as automatic renewals, and a start date that moves backwards hands out no fresh allowance.
- **Changing plan keeps the year** — the purchase date is the date the store's plan subscription was created. Buying a different plan updates that subscription, so the date and the count stay, and the new plan's limit applies to the count so far.
- **A first plan starts a new count** — a store counting by calendar year starts from zero on the date it buys its first plan.
- **Stores already counting kept their number** — nothing was reset when this rule arrived; such a store restarts when its next plan year begins.

### Single-cart Send — the paywall

The per-cart **Send** action on a single cart's panel (from [[orders-abandoned]]) checks the remaining allowance BEFORE attempting to send. When the quota is exhausted, the merchant sees a paywall dialog with the "feature limit warning" message and a link to [[plan-features]] to purchase more `abandoned_notification` quota via a feature-pack top-up.

### What happens when the auto-sweep hits exhaustion mid-batch

When the `abandoned_notification` quota is exhausted mid-run, the auto-sweep job **stops at that cart**, so subsequent carts in the same batch are NOT processed even if some could have qualified by per-cart criteria. The next sweep tick re-attempts from scratch but hits the same exhausted-quota check immediately. Until the switch-off below, the visible signals are `date_sent` stamps stalling out and the "Total sent messages: X" count sitting at the cap.

### When the allowance runs out — the reminder is switched off

Every 12 hours a platform-wide plan check (`disable_un_paid_functionality`, see [[settings-queue-view-recurring-jobs]]) visits each store. If the allowance is used up and **Abandoned cart reminder** is ON, it:

- switches **Abandoned cart reminder** OFF (see [[settings-cart-abandoned-reminder]]);
- posts an **Important** alert in [[notifications]] whose text starts *"You have reached [feature] limit. Your limit is [limit]."* (BG *"Достигнахте ограничение на [feature]. Вашият лимит е [limit]."*).

Nothing switches the reminder back on. A new plan year or a feature pack restores the allowance, but automatic e-mails resume only once the merchant turns **Abandoned cart reminder** on again. Turned on while the allowance is still used up, it is switched off again at the next check.

### When a new plan year starts

- The `plan.count.email.abandoned_notification` counter zeros.
- Carts sent in the previous plan year **keep** their `date_sent` stamps, so the auto-sweep (which filters `date_sent IS NULL`) still skips them.
- The single-cart Send CAN re-send those carts (see [[abandoned-cart-bulk-send]]) and uses the new year's allowance.
- If the plan check had switched **Abandoned cart reminder** off, it stays off until the merchant turns it on.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-bulk-send]] — the per-path failure UX.
- [[abandoned-cart-threshold]] — the auto-sweep that consumes quota on each send.
- [[abandoned-cart-eligibility]] — what filters apply BEFORE the quota counter is touched.
- [[plan-gates]] — the plan-feature mechanism generally; lists `abandoned_notification` among the gates.
- [[plan-features]] — paywall destination when the merchant wants to top up the quota.
- [[orders-abandoned]] — surfaces the "Total sent messages: X" count.
- [[settings-cart]] — `abandoned_remainder` and `abandoned_remainder_interval` settings on the same screen.

## Open Questions

None.
