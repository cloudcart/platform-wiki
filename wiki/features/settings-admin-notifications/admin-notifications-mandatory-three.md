---
type: feature
nav_path: "Settings → Notifications to administrators → Mandatory three"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["Mandatory admin notifications", "Cannot disable admin notification", "email_confirmation", "two_factor_action", "alert_notification", "Always-on admin alerts"]
tags: [settings, notifications, email, security]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (master switch, per-type toggles, recipient routing, delivery queue, alert triggers, permissions / locale).

# Admin notifications — the mandatory three

## Purpose

Three notifications are hard-coded as always-on: `email_confirmation` (the two-code email-change verification), `two_factor_action` (2FA prompt codes), and `alert_notification` (platform-level system alerts). They appear in the notifications table on [[settings-admin-notifications]] for visibility, but their toggle is disabled and the dispatch path bypasses the master switch as well. This guarantees that security-critical events and platform-level advisories reach administrators regardless of merchant notification preferences.

## Where to find it

In the notifications table on [[settings-admin-notifications]], the three mandatory rows are pinned at the bottom of the list with their "Active" switch rendered disabled (visibly "always on").

## What the merchant can do here

- See, at a glance, that these three notifications cannot be silenced.
- (Indirectly) verify that 2FA codes and email-change confirmation codes will still arrive even after the master switch is turned off.

The merchant cannot:

- Disable any of the three from the UI. The toggle is disabled.
- Disable any of the three via a hand-crafted API call. The endpoint rejects the request with HTTP 422.
- Bypass the dispatch via any combination of the master switch + per-type toggle. The dispatch path doesn't read either gate for these three.

## Settings & fields

These three notifications **do not have a per-type `mail_<label>` setting key** that the merchant can edit. They appear in the table as informational only.

| Display name | Internal label | Triggered when | Recipient |
|--------------|----------------|----------------|-----------|
| Email confirmation | `email_confirmation` | The merchant changes the store email in [[settings-general]] — two codes go out, one to the OLD address and one to the NEW address. | The specific OLD or NEW email being verified |
| Two factor code verify | `two_factor_action` | An Admin/Moderator performs a 2FA-protected action and a verification code is required. | The user's own email |
| New notification | `alert_notification` | A system-level alert is raised that administrators must see (e.g., critical platform messages from CloudCart, SSL expiry, webhook auto-disable). See [[admin-notifications-alert-triggers]]. | `site_email` |

## Modals and sub-flows

None on the admin-notifications page itself. The flows that originate these three notifications live elsewhere:

- `email_confirmation` is triggered from the [[settings-general]] email-change flow.
- `two_factor_action` is triggered from any 2FA-protected admin action (login, sensitive setting change).
- `alert_notification` has many possible originators — see [[admin-notifications-alert-triggers]].

## Business rules

### Three layers enforce the always-on rule

The mandatory three are enforced in three independent layers, so no single bug can silence them:

1. **UI** — The toggle for these three rows is disabled in the Vue table. They render as always-active.
2. **API** — The update endpoint returns HTTP 422 with *"This notification cannot be disabled"* if a request tries to set `active=false` for any of them. Even a hand-crafted API call cannot turn them off.
3. **Helper bypass** — The dispatch helpers that send these notifications don't read the master toggle or any per-type `mail_<label>` setting. They enqueue / send directly. So even if a bug in the toggle UI somehow flipped the master switch off, these specific notifications would still go out.

This is intentional: security-critical events (email change confirmation, 2FA, system alerts) MUST reach administrators regardless of their notification preferences.

### Recipient varies per notification

Unlike the toggleable notifications (which all go to `site_email`), the mandatory three have different recipient rules:

- `email_confirmation` — addressed to the specific email being verified during the two-step email change flow. One code goes to the OLD address (proving control of the existing email), one goes to the NEW address (proving control of the proposed email). Neither goes to `site_email` directly unless that happens to be the OLD or NEW address.
- `two_factor_action` — addressed to the user's own email (the admin attempting the 2FA-protected action), NOT the store's `site_email`. So a moderator whose personal admin-user email is `bob@example.com` receives the code at `bob@example.com`, regardless of where the store-level recipient lives.
- `alert_notification` — addressed to `site_email`, like the toggleable notifications. The "single recipient" rule from [[admin-notifications-recipient-routing]] applies here too.

### 2FA codes use synchronous dispatch (no queue delay)

The `two_factor_action` path uses synchronous, in-process dispatch — the server sends the email inline, then returns the HTTP response to the user's 2FA prompt page. No queue worker involvement, no async delay. This is critical UX: a user actively waiting for a 2FA code at a login screen cannot tolerate the multi-second delay a queued email could introduce.

`email_confirmation` and `alert_notification` still go through the standard `admin_notify` SiteQueue task → `system7` worker pipeline. See [[admin-notifications-delivery-queue]].

### Sender is CloudCart, not the store

Like all admin notifications, the mandatory three use a CloudCart-branded From header rather than the store's own sender. See [[admin-notifications-recipient-routing]] for the sender rule.

## Related

- [[settings-admin-notifications]] — hub.
- [[admin-notifications-master-switch]] — the gate the mandatory three bypass.
- [[admin-notifications-per-type-toggles]] — the 14 toggleable rows for contrast.
- [[admin-notifications-recipient-routing]] — the recipient rules; mandatory three deviate.
- [[admin-notifications-delivery-queue]] — 2FA synchronous bypass.
- [[admin-notifications-alert-triggers]] — what raises `alert_notification`.
- [[settings-general]] — where `email_confirmation` is triggered (email change).
- [[settings-staff]] — 2FA setup for admin / moderator accounts.

## Open questions

- The exact list of admin actions gated by 2FA (and thus triggering `two_factor_action`) is platform-defined and could be enumerated as a separate reference. `(verify)`
