---
type: feature
nav_path: "Settings → Notifications to administrators → Delivery queue"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["admin_notify queue", "system7 queue", "Admin notification delivery", "Admin notification asynchronous send", "Admin notification failure visibility", "Why didn't I get the admin email"]
tags: [settings, notifications, email, queue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (master switch, per-type toggles, mandatory three, recipient routing, alert triggers, permissions / locale).

# Admin notifications — delivery queue + failure visibility

## Purpose

Documents the asynchronous pipeline that turns a "fire admin notification X" event into an email in the recipient's inbox. Toggleable admin notifications go through the `admin_notify` SiteQueue task, which the application framework background worker picks up on the `system7` queue and produces the actual outgoing email. Two-factor codes bypass the queue entirely (synchronous dispatch). Failure visibility is poor: there is no in-app surface that shows "did this notification reach the recipient?".

## Where to find it

Nothing on the [[settings-admin-notifications]] page itself surfaces queue state. Queue-monitoring information lives at [[settings-queue-view]] (the platform's queue inspector), but per-notification entries are typically marked `is_visible=false` and therefore don't show up there either.

## What the merchant can do here

- Expect notifications within ~1 minute under normal queue load. Backlogs (e.g., during a CSV import) can push delivery longer.
- Verify a notification was sent by checking the recipient inbox (no in-app indicator).

The merchant cannot:

- See per-notification delivery state on [[settings-admin-notifications]]. No "Last sent: 2026-06-09 14:33" column. No "Status: delivered / failed" indicator.
- See a delivery history of past admin emails anywhere in the admin panel.
- Manually retry a failed dispatch from the admin panel. (Platform-side retry follows the default `system7` queue retry policy.)
- See per-notification failures on [[settings-queue-view]]. Most `admin_notify` queue entries have `is_visible=false` and don't render there.

## Settings & fields

This aspect has no merchant-editable fields. The queue + delivery path is platform infrastructure.

### Delivery pipeline (toggleable notifications)

1. Platform code calls the admin-notification helper with `(label, parameters)`.
2. Helper checks `administrator_email_notifications` (master switch) — if `no`, abort. See [[admin-notifications-master-switch]].
3. Helper checks `mail_<label>` (per-type) — if `no`, abort. See [[admin-notifications-per-type-toggles]].
4. Helper enqueues an `admin_notify` SiteQueue task.
5. Background worker on the `system7` queue picks up the task.
6. Worker renders the email template (in the recipient's locale) and sends via the platform's mail transport.
7. On success: nothing surfaces in-app. On failure: error logged to platform log facility; nothing surfaces in-app.

### Delivery pipeline (mandatory two-factor)

1. Admin attempts a 2FA-protected action.
2. Platform calls the 2FA dispatch synchronously.
3. The email is sent inline (no queue) before the HTTP response returns to the user.
4. The user's 2FA prompt page lands and the email arrives nearly simultaneously.

See [[admin-notifications-mandatory-three]] for why this bypass exists.

### Delivery pipeline (email confirmation)

`email_confirmation` is mandatory but still goes through `admin_notify` → `system7`. So the two-code email-change flow can have a few seconds of delay between the merchant clicking Save on [[settings-general]] and the codes arriving in both inboxes.

## Modals and sub-flows

None on this page.

## Business rules

### Toggleable notifications are queued

`admin_notify` is the SiteQueue task name; the application framework job that processes it runs on the `system7` queue. So queue-monitoring screens display admin-notification jobs as `system7` queue entries, not as `admin_notify`. Expected delivery: within ~1 minute under normal queue load. Backlogged or contended workers can stretch this.

### Two-factor codes bypass the queue entirely

The 2FA dispatch path is synchronous (in-process). The user's 2FA prompt page submits → the server sends the email inline → the response returns. No queue worker involvement, no async delay. This is critical UX for "log in / approve action" flows where the user is actively waiting for the code.

### Email-change confirmation codes DO go through the queue

Unlike 2FA, `email_confirmation` uses the standard `admin_notify` → `system7` path. So clicking Save on the email-change flow at [[settings-general]] may have a few seconds of delay before the OLD-address and NEW-address codes arrive.

### Failed-notification visibility — no in-app surface

If a queued admin notification fails to deliver (SMTP rejection, template error, missing translation), the failure is logged in the platform's internal error log but is NOT surfaced anywhere in the admin panel:

- [[settings-admin-notifications]] has no "Status" or "Last sent" column.
- [[settings-queue-view]] does not surface per-notification failures because `admin_notify` queue entries are typically marked `is_visible=false`.

Practical guidance for "I should have received an alert; was it sent?":

1. Verify the recipient address by sending yourself a test from another sender to the configured `site_email` — see [[admin-notifications-recipient-routing]].
2. Check spam / junk / quarantine folders in the recipient inbox.
3. If notifications stop arriving consistently, contact CloudCart support — support can read the failure log directly.

### Settings cache invalidation is immediate

Each toggle save on [[settings-admin-notifications]] flushes the settings cache, so the next dispatch step 2 / step 3 immediately reads the new value. There is no propagation delay; the merchant can flip a toggle, fire a test event, and verify the new behaviour within seconds (modulo the queue latency for the toggleable notifications).

### Retry behaviour follows `system7` default (verify)

If a `system7` job fails, the platform's default retry policy for the queue applies. The merchant has no control over retry count, retry interval, or failure callback from the admin panel. `(verify)`

### Third-party apps participate in the same queue (verify)

When a third-party app uses the same admin-notification helper (passing a `notification_label` parameter), it enters the same `admin_notify` → `system7` path and respects the same master + per-type gates. There is no separate queue for app-originated admin notifications. `(verify)`

## Related

- [[settings-admin-notifications]] — hub.
- [[admin-notifications-master-switch]] — step 2 in the dispatch pipeline.
- [[admin-notifications-per-type-toggles]] — step 3 in the dispatch pipeline.
- [[admin-notifications-mandatory-three]] — the 2FA synchronous bypass; `email_confirmation` still queued.
- [[admin-notifications-recipient-routing]] — where the email is delivered.
- [[settings-queue-view]] — the queue inspector (limited use here because most `admin_notify` entries are not visible).
- [[background-queue-inventory]] — the platform-wide queue catalogue (covers `system7` and `admin_notify`).
- [[order-processing-pipeline]] — the order-side dispatch points that feed this queue (new order, status change, payment status change, low stock).

## Open questions

- The exact retry count + retry interval for failed `system7` admin-notification jobs is not currently documented on the merchant-facing wiki. `(verify)`
- Whether third-party-app-originated admin notifications obey both the master toggle AND a per-type `mail_<label>` setting (or only the per-type one) deserves a confirmation pass. `(verify)`
