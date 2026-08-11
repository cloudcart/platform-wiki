---
type: feature
nav_path: "Settings → Notifications to administrators → Master switch"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["Admin notifications master switch", "Send notifications to administrators toggle", "administrator_email_notifications", "Master toggle for admin email"]
tags: [settings, notifications, email]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (per-type toggles, mandatory three, recipient routing, delivery queue, alert triggers, permissions / locale).

# Admin notifications — master switch

## Purpose

The single "kill switch" for all toggleable admin email notifications. Lives in the top-right action slot of the [[settings-admin-notifications]] page header and saves immediately on flip — no separate Save button. When OFF, every notification that goes through the normal admin-notification helper is suppressed at dispatch time regardless of its individual per-type toggle. When ON, each per-type toggle (`mail_<label>`) governs its own row independently.

The master switch does **not** stop the three mandatory notifications — `email_confirmation`, `two_factor_action`, and `alert_notification` go out regardless. See [[admin-notifications-mandatory-three]].

## Where to find it

In the page header of [[settings-admin-notifications]], right-aligned next to the title. Rendered as a Vue switch component. There is no other place in the admin panel to flip this setting.

## What the merchant can do here

- Turn ALL toggleable admin email notifications on or off with one click — useful for a temporary blackout (e.g., during a stress test, a bulk import, a marketing-campaign spike that would otherwise flood the recipient inbox with new-order alerts).
- See immediately via toast feedback whether the save succeeded.

The merchant cannot:

- Undo via a "Cancel" button — saves are immediate. The only undo is to flip the switch back.
- Schedule the toggle (e.g., "off for the weekend"). There is no scheduling layer.
- See per-day or per-week toggle history. The audit trail (if any) lives in the platform's settings history log, not on this screen.

## Settings & fields

| Field / Control | Setting key | What it does | Notes |
|-----------------|-------------|--------------|-------|
| **Send notifications to administrators** | `administrator_email_notifications` | Master toggle. `yes` (on) / `no` (off). | Saves immediately on flip. No Save button. |

### Save flow

When the merchant flips the master switch:

- The new value is sent immediately to `POST /admin/api/core/settings/admin-notifications/settings` with `{administrator_email_notifications: <bool>}`.
- On success → toast *"Settings saved successfully"*.
- On error → the switch visually reverts to its previous state + toast *"Error while saving settings"*.

Each save flushes the settings cache, so the next dispatched notification anywhere in the platform immediately respects the new state — no propagation delay.

## Modals and sub-flows

None. The master switch is a single click. No confirm dialog. No "are you sure" prompt — flipping ALL notifications off is a one-click destructive action, by design.

## Business rules

### Master switch suppresses ALL toggleable notifications

When `administrator_email_notifications=no`, the admin notification helper short-circuits dispatch for every notification that goes through the normal helper path — the queue task is never created. Affects all 14 toggleable rows. Mandatory notifications bypass this gate entirely (see [[admin-notifications-mandatory-three]]).

### Two different defaults in code — the "flip once" gotcha (verify)

This is subtle and matters. Two code paths read `administrator_email_notifications` with DIFFERENT default values when the setting is missing:

- **The display path** (the page's `getSettings` endpoint that populates the master switch): defaults to **`yes`** when missing. So the switch appears ON to a new merchant who has never touched it.
- **The dispatch path** (the gate every notification goes through): defaults to **`no`** when missing. So if the setting is missing AND a notification fires, the notification is SUPPRESSED.

For a freshly created store where the setting has never been saved, the merchant sees "Notifications are ON" in the UI but the actual notifications are NOT being sent. As soon as the merchant flips the switch (even just OFF and back ON), the setting is persisted with an explicit `yes` / `no` value and both paths align.

**Practical guidance for a new merchant**: flip the master switch off and back on once after initial setup to ensure the setting is persisted with an explicit value. After that the displayed state matches reality.

### Save is immediate; no draft / cancel

Both this master switch and individual per-type toggles save the moment they are flipped — no Save button, no undo. On error, the switch visually reverts to its previous state and a red toast is shown.

### Cache invalidation is immediate

Each save flushes the settings cache. The next dispatched notification (anywhere in the platform) immediately respects the new state. There is no propagation delay; the merchant can flip the switch, fire a test event (e.g., place a test order), and verify behaviour within seconds.

## Related

- [[settings-admin-notifications]] — hub.
- [[admin-notifications-per-type-toggles]] — the 14 toggleable rows the master switch governs.
- [[admin-notifications-mandatory-three]] — the three notifications that bypass this switch.
- [[admin-notifications-delivery-queue]] — the queue path that respects (or is bypassed by) this gate.
- [[settings-general]] — where the recipient `site_email` is configured.

## Open questions

- The "two different defaults" gotcha should be verified against the current dispatch-path code before being treated as gospel — the wiki entry was based on a May 2026 audit. `(verify)`
