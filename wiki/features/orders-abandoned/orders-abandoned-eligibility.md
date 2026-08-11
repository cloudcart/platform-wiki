---
type: feature
nav_path: "Orders → Abandoned → Eligibility"
route_name: admin.abandoned.list
route_path: /admin/abandoned
aliases: ["Abandoned cart eligibility", "Abandoned send rules", "Restore link eligibility", "Allowed-to-send rules", "Условия за изпращане на restore link"]
tags: [orders, abandoned, eligibility, validation, cart-recovery]
plan_gates: ["abandoned_notification"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, detail view, restore link, auto-recovery, plan gates, cart lifecycle).

# Abandoned carts — Eligibility check

## Purpose

Documents the **7-rule eligibility gate** that every abandoned-cart Send (manual, bulk, or via the scheduled 3-minute recovery job) must pass before the restore-link email is dispatched. The gate is the same across all entry points; failure modes differ slightly.

Closely related to the silent-deletion behaviour: clicking Send on an ineligible cart **does not** show an error — the cart is removed from the list and the merchant sees a success toast. This is intentional cleanup, but it surprises support agents triaging "why did the cart disappear" tickets.

## Where to find it

Not a screen — runs server-side whenever:

- The merchant clicks **Send restore link** from [[orders-abandoned-detail-view]] (per-cart).
- The merchant runs the bulk **Send restore link** from [[orders-abandoned-list-view]].
- The scheduled job from [[orders-abandoned-auto-recovery]] iterates over candidate carts every 180 seconds.

## What the merchant can do here

Nothing directly — this is platform validation. The merchant observes it indirectly through:

- Carts that vanish from the list after Send (failed eligibility → silent deletion).
- Bulk Send returning a smaller "X emails sent" count than the number of selected rows.
- Subscriber carts that never appear in the list at all (excluded by the verification rule below).

## Settings & fields

The eligibility check has no configurable knobs. The two pieces of platform state it inspects are:

- The email channel's `unconfirmed_send` setting — controls whether unverified subscribers are eligible.
- The cart's metadata + linkage state (customer, subscriber, email, key, soft-deleted, prior order references).

## Business rules

### The 7-rule eligibility check

A cart qualifies for the Send restore link action ONLY when ALL of these are true:

1. The cart has at least one item.
2. Either a known customer is attached OR an identified email subscriber exists.
3. The customer/subscriber has a non-empty email address.
4. The cart still has a valid `key` token.
5. No order has been placed against this cart yet.
6. No prior order's metadata references this cart.
7. The cart is not soft-deleted.

If any condition fails when the merchant clicks Send, **the cart is silently deleted from the abandoned list instead** — the merchant sees a successful "email sent" toast but the cart is removed. This is intentional cleanup: invalid carts are flushed rather than left to clutter the list.

### Subscriber email-confirmation requirement

When the cart belongs to a SUBSCRIBER (not a registered customer), the platform requires the subscriber to be **email-verified** IF the email channel's `unconfirmed_send` setting is OFF. Unverified subscribers are excluded from the abandoned list AND from bulk-send. (Configurable per channel — when `unconfirmed_send = yes`, unverified subscribers are still sent the restore link.)

### Subscriber email channel resolved at the cart's update time

For subscriber-only carts (no registered customer), the platform resolves the recovery email by looking up the subscriber's email-channel record that **existed AT OR BEFORE the cart's last update timestamp**. This avoids sending the restore link to a different person who later got linked to the same subscriber via shared UUID cookie. If no valid channel email is found at that point in time, the cart is **silently DELETED** instead of sent — the same intentional-cleanup behaviour as failed 7-rule checks.

### Bulk vs per-cart — eligibility behaves the same

The 7-rule gate runs on every Send entry point. Where bulk and per-cart Send diverge is the **`date_sent` skip behaviour**, not the eligibility gate:

- Bulk Send → silently skips carts with a `date_sent` value (filtered out of the bulk query). Carts that fail the 7-rule gate are silently deleted.
- Per-cart Send (from [[orders-abandoned-detail-view]]) → does NOT skip by `date_sent` (allows re-send) but still applies the 7-rule gate. Carts that fail the gate are silently deleted.

See [[orders-abandoned-restore-link]] for the `date_sent` mechanics.

### Bulk send — partial success counting

When the merchant bulk-sends to many carts, the platform reports *"X emails sent"* (`order.succ.abandoned_%d_emails_sent`). Carts that fail the eligibility check (no items, no email, no key, soft-deleted, etc.) are silently skipped AND silently deleted. If zero emails were sent, the merchant sees *"No emails were sent"* (`order.err.abandoned_no_emails_sent`).

### Carts already linked to an order

Conditions 5 and 6 are the most common silent-deletion cause:

- **Condition 5** — a customer who placed an order keeps the same cart record as a session reference for a short time. The cart is no longer "abandoned" but may linger in the list until the merchant bulk-clears.
- **Condition 6** — even after an order is placed via [[orders-add]] referencing the cart, the cart is no longer eligible. The same applies for orders restored through a previous restore-link click — the new order's metadata references the original cart key.

## Plan gates

Eligibility itself is not plan-gated — every store on every plan applies the same 7-rule check. But the Send action that triggers eligibility is gated by `abandoned_notification` (numeric cap) and on per-cart Send also by `test_mail` — see [[orders-abandoned-plan-gates]].

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-list-view]] — bulk Send context.
- [[orders-abandoned-detail-view]] — per-cart Send context.
- [[orders-abandoned-restore-link]] — what gets sent when eligibility passes (and the `date_sent` skip rules).
- [[orders-abandoned-auto-recovery]] — the scheduled job that applies the same 7-rule check.
- [[orders-abandoned-cart-lifecycle]] — covers cart soft-deletion (rule 7).
- [[subscriber]] / [[marketing-subscribers]] — subscriber side of the population.
- [[cart]] — entity page; carries the `key` token referenced in rule 4.

## Open questions

None.
