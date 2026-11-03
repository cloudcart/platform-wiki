---
type: entity
nav_path: "Entity → Admin Notification → Delivery & lifecycle"
aliases: ["Admin notification delivery", "admin_notify queue", "Bell-icon alert delivery", "Grouped alerts", "Rate-limited notifications", "Synchronous 2FA dispatch", "Notification mapping key", "Доставка на известията"]
tags: [entity, notifications, delivery, queue, async, bell-icon]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[admin-notification]]. See the hub for the other aspects (types, master switch, recipient, alert channel, low-stock).

# Admin Notification — Delivery & lifecycle

## Identity

An Admin Notification has **two delivery halves**: an **email** (asynchronous via the `admin_notify` queue, except for synchronous 2FA dispatch) and a **bell-icon alert** in the admin panel header (synchronous DB write). Both halves are gated by the same suppression rules (see [[admin-notification-entity-master-switch]]), both halves rate-limit and group on the same `mapping` key, and the merchant has **no in-app failure surface** if either half fails to deliver.

This page covers the lifecycle from event-fires → gate-check → translation → dispatch → delivery → read, plus the grouping / rate-limit rules that prevent bell-icon spam.

## Aliases

- **`admin_notify` queue** — the background queue carrying asynchronous admin emails.
- **Bell-icon alert** / **Камбанка** — the in-panel half of the delivery (the bell icon at the top right of every admin page).
- **Mapping key** / **Grouping key** — the identifier that collapses repeated alerts for the same root cause.
- **Rate-limit window** — the 1-day / 5-minute suppression windows for repeated alerts on the same mapping.

## Key Attributes

### The 8-phase lifecycle

An Admin Notification moves through these phases (the 3 mandatory types skip phase 3):

1. **Event fires** — a platform action triggers the underlying domain event (a new order is placed, a webhook fails permanently, an export completes, a low-stock threshold is crossed, etc.).
2. **Type lookup** — the platform maps the event to one of the 17 notification types (see [[admin-notification-entity-types]]).
3. **Gate check** — for toggleable types, the platform checks (a) the master switch and (b) the per-type toggle. If either is OFF, the notification is suppressed (no email, no bell alert). For mandatory types, this step is skipped entirely. See [[admin-notification-entity-master-switch]].
4. **Translation** — title + body are rendered in the admin panel's selected language, falling back to the store's default language if a translation row doesn't exist.
5. **Email dispatch** — the email is enqueued to the `admin_notify` queue (asynchronous, expected delivery within ~1 minute). Two-factor codes are dispatched synchronously and bypass the queue so the user isn't blocked waiting on a queue worker.
6. **Bell-icon alert** — an alert row is written synchronously, surfacing immediately on the bell icon.
7. **Delivered** — the email lands in the recipient's inbox; the alert sits in the bell-icon feed.
8. **Read** — the merchant clicks the alert; the unread counter decrements. Reading dismisses from the counter but does NOT delete the row.

### Asynchronous email — `admin_notify` queue

Toggleable notifications are queued on the dedicated `admin_notify` queue and processed by a background worker. Expected delivery: within ~1 minute under normal load. If the queue is backlogged (bulk import / export running), delivery can be longer.

The 2FA exception: `two_factor_action` codes dispatch **synchronously** — the user is actively waiting on the code to complete a 2FA-protected action, so blocking on a queue worker would break the UX. The synchronous path also bypasses the master-switch gate (because the type is mandatory).

### Grouping by `mapping` key

Each alert carries an optional grouping key (called `mapping`). Repeated alerts for the same root cause **collapse into one entry** — a single broken webhook produces ONE alert row, not one alert per failed delivery attempt. The underlying record is updated-or-created keyed on the mapping:

| Trigger pattern | Resulting alert rows |
|-----------------|----------------------|
| 1 webhook failure, mapping `X` | 1 alert row created |
| 5 webhook failures, all mapping `X` | 1 alert row, updated 5 times |
| 5 webhook failures across 5 mappings | 5 alert rows |

Notifications without a `mapping` key always create a new row (no collapsing).

### Rate limits on both halves

On top of grouping, the platform rate-limits both delivery halves for a given mapping:

| Half | Rate-limit window |
|------|-------------------|
| Email for `mapping = X` | 1 per day (suppressed if one already sent for that mapping within 24 hours) |
| Bell-icon push event for `mapping = X` | 1 per 5 minutes (suppressed if one already pushed for that mapping within 5 minutes) |

So a webhook that fails on 5 different events within an hour produces:

- One alert row (collapsing).
- One email (if not already sent today for that mapping).
- At most one bell-icon push per 5-minute window for the same mapping.

### No in-app failure surface

If a queued notification fails (SMTP rejection, template missing, missing translation), the failure is logged in the platform's internal log but is **NOT surfaced anywhere in the admin panel** — no banner, no bell alert, no queue-view entry. The merchant has no in-app way to ask "I should have received an alert; was it sent?".

Practical troubleshooting:

1. Verify the recipient address by sending a test from another sender.
2. Check spam folders.
3. Contact CloudCart support if notifications go missing consistently — support can read the failure log directly.

### Read state and bell-icon counter

The bell icon shows a counter of **unread** alerts. Clicking the bell opens the alert list; clicking an alert marks it read and decrements the counter. Read state is store-level, not per-administrator. There is no "Mark all read" bulk action documented (verify).

### Notification list is locale-filtered on the settings page

The [[settings-admin-notifications]] table only shows notification types that have a translation in the admin panel's currently selected language. For less-common admin languages, some rows may be missing — the dispatch path still works, but the merchant has no UI to toggle them. This is uncommon — CloudCart ships translations for the major languages — but explains why the list could appear shorter for some locales.

## Where it appears

- The bell icon at the top right of every admin page — the in-panel half of delivery.
- [[settings-admin-notifications]] — locale-filtered notification table.
- Admin recipient's inbox — actual email delivery surface.
- [[settings-hooks]] — webhook failures are the canonical example of `mapping`-based grouping.

## Related

- [[admin-notification]] — hub.
- [[admin-notification-entity-types]] — which types use which dispatch path (queue vs synchronous).
- [[admin-notification-entity-master-switch]] — the gates that run BEFORE dispatch.
- [[admin-notification-entity-recipient]] — recipient resolution at dispatch time.
- [[admin-notification-entity-alert-channel]] — the `alert_notification` channel is the heaviest user of grouping (webhook failures, plan limits).
- [[settings-admin-notifications]] — configuration screen + locale-filtered table.
- [[notification-delivery]] — cross-cutting concept; admin notifications are one of four parallel consumers.

## Open Questions

- Whether the bell-icon "Mark all read" bulk action exists in the current UI (verify).
- The exact retry semantics on `admin_notify` queue jobs (number of attempts, backoff) (verify).
- Whether some notification types are bell-only or email-only, vs. always-both (verify — the 17 listed types all appear to be email-driven; bell-icon-only system events may exist but are not listed on [[settings-admin-notifications]]).
