---
type: concept
nav_path: "Concept → Abandoned cart recovery → Manual bulk send"
aliases: ["Send restore link", "Manual bulk send", "Bulk Send restore link action", "Manual single send", "Re-send restore link", "Silent delete on bulk send", "date_sent stamp"]
tags: [orders, cart, abandoned, recovery, bulk, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[abandoned-cart-recovery]]. See the hub for the other aspects (threshold, eligibility, restore link, channels, attribution, plan quota).

# Abandoned cart — manual bulk send

## Definition

In addition to the automated every-3-minute sweep (see [[abandoned-cart-threshold]]), the merchant can manually trigger restore links via the **Send restore link** bulk action on [[orders-abandoned]]. The merchant picks one or many carts from the list, clicks Send restore link, and each cart runs through the same seven-check eligibility filter + two-layer marketing consent (see [[abandoned-cart-eligibility]]) at trigger time. Re-sends to a cart that already has `date_sent` ARE allowed; the platform doesn't block multiple restore-link emails for the same cart in this flow.

There are actually **three send paths** with subtly different failure semantics — covered below.

## Scope

Covered:

- The bulk **Send restore link** action — silent-delete on eligibility failure, aggregate toast, re-send permitted.
- The per-cart single **Send** action from a cart's details panel — hard paywall on plan quota.
- The auto-sweep — silent-skip on eligibility failure.
- The `date_sent` stamp — what it means and what it does NOT do (re-send guard).
- The commented-out re-send-block code.
- Mixed-eligibility bulk-send example.

Not covered here:

- What "eligibility" actually is (the seven-check filter + consent gate) — see [[abandoned-cart-eligibility]].
- The plan quota that gates send attempts — see [[abandoned-cart-plan-quota]].
- What the recipient sees when they click the link — see [[abandoned-cart-restore-link]].

## Contrasts

- **Bulk Send vs single-cart Send vs auto-sweep — three different failure UX paths**:
  - **Bulk Send restore link** — iterates over the selected carts that have no `date_sent` yet; carts that fail eligibility are silently removed. Merchant sees aggregate "X emails sent" toast.
  - **Single-cart Send** (from a cart's details panel on [[orders-abandoned]]) — checks the remaining `abandoned_notification` allowance BEFORE sending and shows the merchant-facing "feature limit warning" message when the quota is exhausted. Merchant sees a **hard paywall** on the single-cart path.
  - **Auto-sweep** — silently skips failing carts; merchant sees no signal beyond `date_sent` stamps not appearing.
- **`date_sent` stamp vs re-send guard** — `date_sent` shows when the last restore-link email was dispatched. The bulk action and the auto-sweep skip carts that have it; the single-cart Send does not.

## Where it applies

### The bulk Send restore link action on [[orders-abandoned]]

1. Merchant ticks one or many carts in the abandoned-cart list.
2. Clicks **Send restore link**.
3. Each cart runs through the seven-check eligibility filter + two-layer marketing consent (see [[abandoned-cart-eligibility]]) at trigger time.
4. **Failing carts** are **silently deleted from the list** (the platform reports the count of carts that actually got sent; failures absorbed in the counter).
5. **Passing carts** get a fresh restore-link email; `date_sent` is stamped.
6. Toast shows: *"X emails sent"*.

So a merchant sending to 10 carts may see "4 emails sent" + 6 carts disappeared from the list with no per-cart reason. To investigate, the merchant has to inspect each missing cart's details (was the email blank? token expired? marketing consent off?) before clicking Send.

### The single-cart Send action (from a cart's details panel)

The per-cart **Send** action on a single cart's panel takes a different path:

- It checks the remaining `abandoned_notification` allowance **before** sending.
- On quota exhaustion, the merchant sees a **hard paywall** dialog with the "feature limit warning" message and a link to [[plan-features]].
- The seven-check eligibility filter still applies; failing checks still silent-skip (no per-check error to the merchant — same as bulk).

So the path that surfaces a paywall to the merchant is the single-cart Send; the auto-sweep stops without notice. See [[abandoned-cart-plan-quota]].

### Re-sends are allowed (the commented-out guard)

Re-sends to a cart that already has `date_sent` are NOT blocked on the single-cart Send. So a merchant can:

- Send the restore link to a stubborn cart on Monday.
- Send it to the same cart again on Wednesday.
- Send it to the same cart again on Friday.

…each send consumes one unit of the `abandoned_notification` allowance (see [[abandoned-cart-plan-quota]]). `date_sent` updates on each send but doesn't function as a "don't send twice" guard.

The auto-sweep and the bulk action DO filter for `date_sent IS NULL`, so they won't re-send. Only the single-cart Send permits re-sends.

### Example: Bulk send with mixed eligibility

1. Merchant selects 10 abandoned carts and clicks **Send restore link**.
2. **4 carts pass** eligibility → recovery emails go out, `date_sent` stamped.
3. **6 carts fail** (no email, expired token, marketing consent off, etc.) → deleted from the list silently.
4. Toast shows: *"4 emails sent"*.
5. The merchant looks at the list — 6 carts gone, 4 carts have `date_sent` stamps. No per-cart error log.

### Per-cart Delete action

In addition to the Send action, the merchant can **Delete** an individual cart from [[orders-abandoned]]. This soft-deletes the cart row (sets `deleted_at`); the cart disappears from the list but the underlying cart row remains in the database. Soft-deleted carts fail eligibility check #7 (`cart is not soft-deleted`) so they cannot be re-sent.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-eligibility]] — the seven-check filter + consent gate that runs at trigger time on every send path.
- [[abandoned-cart-plan-quota]] — the `abandoned_notification` allowance per plan year.
- [[abandoned-cart-threshold]] — the auto-sweep cadence that the manual flow supplements.
- [[abandoned-cart-restore-link]] — what the customer sees when they click the link.
- [[orders-abandoned]] — the list where the bulk action lives.
- [[plan-features]] — paywall destination when quota is exhausted on single-cart Send.

## Open Questions

None.
