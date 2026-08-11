---
type: concept
nav_path: "Concept → Abandoned cart recovery → Manual bulk send"
aliases: ["Send restore link", "Manual bulk send", "Bulk Send restore link action", "Manual single send", "Re-send restore link", "Silent delete on bulk send", "date_sent stamp"]
tags: [orders, cart, abandoned, recovery, bulk, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
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
  - **Bulk Send restore link** — iterates, calls `generateRestoreCode` per cart, the underlying mailer's quota check then silently delete-removes failing carts. Merchant sees aggregate "X emails sent" toast.
  - **Single-cart Send** (from a cart's details panel on [[orders-abandoned]]) — explicitly checks the platform code BEFORE sending and throws a a plan-restriction error exception with the merchant-facing "feature limit warning" message when the quota is exhausted. Merchant sees a **hard paywall** on the single-cart path.
  - **Auto-sweep** — silently skips failing carts; merchant sees no signal beyond `date_sent` stamps not appearing.
- **`date_sent` stamp vs re-send guard** — `date_sent` is purely an informational stamp showing when the last restore-link email was dispatched. It is **not** a "don't send twice" guard in the manual flow. The code path that would block re-sending is present but commented out. (verify)

## Where it applies

### The bulk Send restore link action on [[orders-abandoned]]

1. Merchant ticks one or many carts in the abandoned-cart list.
2. Clicks **Send restore link**.
3. Each cart runs through the seven-check eligibility filter + two-layer marketing consent (see [[abandoned-cart-eligibility]]) at trigger time.
4. **Failing carts** are **silently deleted from the list** (the platform reports the count of carts that actually got sent; failures absorbed in the counter).
5. **Passing carts** get a fresh restore-link email; `date_sent` is stamped (or updated, on re-sends).
6. Toast shows: *"X emails sent"*.

So a merchant sending to 10 carts may see "4 emails sent" + 6 carts disappeared from the list with no per-cart reason. To investigate, the merchant has to inspect each missing cart's details (was the email blank? token expired? marketing consent off?) before clicking Send.

### The single-cart Send action (from a cart's details panel)

The per-cart **Send** action on a single cart's panel takes a different path:

- It explicitly calls the platform code **before** sending.
- On quota exhaustion, throws a a plan-restriction error exception with the merchant-facing "feature limit warning" message — the merchant sees a **hard paywall** dialog with a link to [[plan-features]].
- The seven-check eligibility filter still applies; failing checks still silent-skip (no per-check error to the merchant — same as bulk).

So the **only path that explicitly surfaces a paywall to the merchant** is the single-cart Send. Bulk Send and auto-sweep both fail silently on quota exhaustion. See [[abandoned-cart-plan-quota]].

### Re-sends are allowed (the commented-out guard)

Re-sends to a cart that already has `date_sent` are NOT blocked in the manual flow. The code path that would block re-sending a cart that already has `date_sent` is present but commented out. (verify) So a merchant can:

- Send restore link to a stubborn cart on Monday.
- Send restore link to the same cart again on Wednesday.
- Send restore link to the same cart again on Friday.

…each send consumes one unit of the `abandoned_notification` quota (see [[abandoned-cart-plan-quota]]). `date_sent` updates on each send but doesn't function as a "don't send twice" guard.

The auto-sweep DOES filter for `date_sent IS NULL`, so the sweep won't re-send. Only the manual paths permit re-sends.

### Example: Bulk send with mixed eligibility

1. Merchant selects 10 abandoned carts and clicks **Send restore link**.
2. **4 carts pass** eligibility → recovery emails go out, `date_sent` stamped.
3. **6 carts fail** (no email, expired token, marketing consent off, etc.) → deleted from the list silently.
4. Toast shows: *"4 emails sent"*.
5. The merchant looks at the list — 6 carts gone, 4 carts have `date_sent` stamps. No per-cart error log.
6. The 4 surviving sends each decremented the `abandoned_notification` quota by 1 (the 6 silent-deletes did NOT consume quota since they failed before the mailer ran). (verify)

### Per-cart Delete action

In addition to the Send action, the merchant can **Delete** an individual cart from [[orders-abandoned]]. This soft-deletes the cart row (sets `deleted_at`); the cart disappears from the list but the underlying cart row remains in the database. Soft-deleted carts fail eligibility check #7 (`cart is not soft-deleted`) so they cannot be re-sent.

## Related

- [[abandoned-cart-recovery]] — hub.
- [[abandoned-cart-eligibility]] — the seven-check filter + consent gate that runs at trigger time on every send path.
- [[abandoned-cart-plan-quota]] — the `abandoned_notification` plan quota; why single-cart Send hits a paywall but bulk Send doesn't.
- [[abandoned-cart-threshold]] — the auto-sweep cadence that the manual flow supplements.
- [[abandoned-cart-restore-link]] — what the customer sees when they click the link.
- [[orders-abandoned]] — the list where the bulk action lives.
- [[plan-features]] — paywall destination when quota is exhausted on single-cart Send.

## Open Questions

- Confirm whether the 6 silent-delete failures in the bulk example actually skip the quota counter, or whether the per-cart mailer call increments before the eligibility check. (verify against the bulk-send code path)
