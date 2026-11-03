---
type: concept
aliases: ["Notification suppression", "notify_customer flag", "No global mute", "Pause notifications", "Customer-side suppression"]
tags: [notifications, email, suppression, orders, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[notification-delivery]]. See the hub for the other aspects (event spine, retry semantics, admin alerts, transactional email inventory).

# Notification delivery — suppression & the absence of a global mute

## Definition

How (and how little) a merchant can **silence** outbound notifications. There is exactly one per-order suppression control — the order's `notify_customer` flag — plus per-template and per-webhook toggles. There is **no** platform-wide "pause all notifications" or "mute the bell" switch in the merchant UI. A merchant who wants to "stop all emails for a moment" cannot do it from one place; suppression is per-channel and, for status emails, per-order.

## Scope

What this covers:

- The per-order `notify_customer` flag — what it suppresses and what it does NOT.
- The absence of a merchant-facing global mute, and what the closest controls are.
- The one ops-side kill switch that exists (analytics only).
- Account-wide marketing suppression vs. transactional suppression.

What it does NOT cover:

- The per-template Active toggle and master switch — see [[notification-delivery-email-inventory]].
- The webhook active / inactive toggle — see [[settings-hooks]].
- Admin-alert email escalation preferences — see [[settings-admin-notifications]].

## Contrasts

- **Per-order suppression vs. per-template suppression**: `notify_customer` silences status emails for ONE order; the template Active toggle silences a label for the WHOLE store. Different scopes.
- **Transactional suppression vs. marketing suppression**: `notify_customer` is transactional (this order's status emails). Account-wide marketing opt-out is the customer record's marketing flag — an independent system. See [[subscriber-vs-customer]].
- **Merchant-side mute (does not exist) vs. ops-side kill switch (analytics only)**: the only platform kill switch pauses analytics, not webhooks or mail, and is not in the merchant UI.

## Where it applies

- [[orders-notify-customer]] — the per-order toggle in the order view.
- [[order]] / [[orders-details]] — the order carrying the `notify_customer` flag.
- [[settings-hooks]] — webhook active / inactive toggle (the webhook-channel suppression).
- [[customer]] — account-wide marketing flag (independent of `notify_customer`).
- [[settings-statuses]] — status transitions whose emails `notify_customer` suppresses.

## The per-order `notify_customer` flag

Every order carries a `notify_customer` boolean, default `1`. When the merchant flips it to `0` via [[orders-notify-customer]], every future status-change email for **that specific order** is suppressed at the dispatch layer — the queue still receives the event, but the mail-render step short-circuits. Key behaviours:

- **Toggling does NOT re-fire the current status's email.** The merchant has to re-apply the status to restart notifications.
- **The flag is per-order.** It does NOT affect any other order.
- **It does NOT cascade to webhooks.** The `order.updated` webhook still fires regardless of `notify_customer`.
- **It does NOT affect admin alerts.** The bell-icon feed is unaffected.

So `notify_customer = 0` is precisely "stop emailing THIS customer about THIS order's status changes" — nothing broader.

## No global mute / pause (merchant side)

There is no merchant-facing "pause all notifications" or "mute the bell" switch. The closest available controls, each scoped narrowly, are:

- Individual webhooks toggled inactive on [[settings-hooks]].
- Individual mail templates toggled off per template on [[marketing-omnichannel-mails-list]] (subject to the master switch and the three bypass labels — see [[notification-delivery-email-inventory]]).
- Admin-alert email escalation preferences on [[settings-admin-notifications]].

There is no single platform-wide kill switch in the merchant UI that stops everything at once.

## The one ops-side kill switch (analytics only)

A platform-wide kill switch DOES exist at the configuration level (the platform code `$disableMessage`), but it only pauses **analytics** — not webhooks, not mail, not admin alerts. It is ops-side, not merchant-side, and not reachable from the admin panel.

## Account-wide marketing suppression is a different system

To stop sending a customer **marketing** messages account-wide, the merchant edits the [[customer]] record's marketing flag — an entirely separate system from `notify_customer`. Transactional emails (order confirmations, status changes) are not governed by the marketing flag, and marketing opt-out does not silence transactional notifications. See [[subscriber-vs-customer]] for the distinction between a marketing subscriber and a customer account.

## Related

- [[notification-delivery]] — hub.
- [[orders-notify-customer]] — the per-order `notify_customer` toggle.
- [[order]] / [[orders-details]] — the order entity carrying the flag.
- [[notification-delivery-email-inventory]] — per-template Active toggle + master switch.
- [[settings-hooks]] — per-webhook active / inactive toggle.
- [[settings-admin-notifications]] — admin-alert escalation preferences.
- [[customer]] — account-wide marketing flag.
- [[subscriber-vs-customer]] — marketing subscriber vs. customer account.
- [[settings-statuses]] — status transitions whose emails the flag suppresses.

## Open Questions

None.
