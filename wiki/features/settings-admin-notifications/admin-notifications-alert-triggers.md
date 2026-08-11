---
type: feature
nav_path: "Settings → Notifications to administrators → Alert triggers"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["alert_notification triggers", "System alert channel", "Platform alerts to admins", "What raises an admin alert", "SSL expiry alert", "Webhook auto-disable alert"]
tags: [settings, notifications, email, alerts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (master switch, per-type toggles, mandatory three, recipient routing, delivery queue, permissions / locale).

# Admin notifications — alert triggers (the `alert_notification` channel)

## Purpose

`alert_notification` is the always-on, catch-all admin email channel for platform-level events that administrators MUST see. It is one of the three mandatory notifications — the merchant cannot silence it via the master switch or via a per-type toggle (see [[admin-notifications-mandatory-three]]). This page enumerates the known originators of `alert_notification` so the merchant can recognise what an incoming alert means and where to act on it.

## Where to find it

The channel name appears in the notifications table on [[settings-admin-notifications]] as "New notification" (the human-readable label), pinned at the bottom of the table with its toggle disabled. The actual alerts arrive in the recipient inbox (`site_email`).

## What the merchant can do here

- Recognise common alert types and know which admin page to act on.
- Configure `site_email` on [[settings-general]] to a monitored inbox so alerts aren't missed.

The merchant cannot:

- Filter which alert types fire. The channel is platform-controlled — any platform component can raise an alert via the platform's alert helper.
- Configure per-alert recipients. All alerts go to `site_email`. See [[admin-notifications-recipient-routing]].
- Silence the channel. The mandatory-three rule prevents it. See [[admin-notifications-mandatory-three]].

## Settings & fields

This aspect has no merchant-editable fields. The list of triggers below is informational.

### Known originators of `alert_notification`

The list is open-ended; any platform component can raise an alert via the platform's alert helper. Verified originators include:

| Trigger | Originating area | What the merchant should do |
|---------|------------------|-----------------------------|
| **SSL certificate expiry on a custom domain** | [[settings-domains]] | Renew the SSL certificate or verify the auto-renewal flow. The platform falls back to the main host until the cert is restored. |
| **Webhook auto-disable** | [[settings-hooks]] | A webhook receiver returned a permanent-failure HTTP code or asked the platform to unsubscribe. Inspect the webhook on [[settings-hooks]] and either fix the receiver or re-enable the subscription. |
| **Plan-feature limit reached** | (various paid features) | The merchant exceeded a paid plan feature limit (e.g., notification quota, storage). The alert explains next steps — typically upgrade the plan or reduce usage. See [[merchant-roles]] / the active plan on the dashboard. |
| **App uninstall on unpaid plans** | App subscriptions | An app subscription lapsed and the app was auto-uninstalled. The alert explains what was removed; the merchant can re-subscribe + reinstall. |
| **IP blocked / banned-IP enforcement events** | Security flows | Surfaced in some flows when an IP triggers automated blocking. |
| **CloudCart-platform-staff messages** | CloudCart support / billing | Billing notices, security advisories, planned maintenance announcements, end-of-life notices, important policy changes. |

The list above is verified against the platform code but is not guaranteed exhaustive — new originators can be added by any future platform release. `(verify)`

## Modals and sub-flows

None. `alert_notification` is delivered as a plain email; the merchant clicks through to the relevant admin page named in the email body.

## Business rules

### Channel is mandatory and bypasses both toggles

`alert_notification` is one of the three notifications that bypass the master switch AND have no per-type `mail_<label>` setting. See [[admin-notifications-mandatory-three]] for the three-layer enforcement.

### Recipient is `site_email`

Unlike the other two mandatory notifications (`email_confirmation` to the address being verified, `two_factor_action` to the user's own email), `alert_notification` goes to the store's `site_email`. So the single-recipient + shared-inbox guidance from [[admin-notifications-recipient-routing]] applies — a merchant with multiple administrators must use a shared inbox or distribution list to fan out alerts.

### Delivery is queued (not synchronous)

`alert_notification` goes through the standard `admin_notify` SiteQueue task → `system7` worker pipeline. So there can be a small (~1 minute under normal load) delay between the originating event and the alert arriving. See [[admin-notifications-delivery-queue]].

### Sender is CloudCart-branded

Like all admin notifications, `alert_notification` uses CloudCart's platform sender, not the store's own configured sender. Merchant inbox filters should match the CloudCart sender domain. See [[admin-notifications-recipient-routing]].

### "Catch-all" framing — this is the channel for things merchants cannot opt out of

`alert_notification` exists specifically because CloudCart needs a channel to reach the merchant for events that the merchant CANNOT choose to ignore: billing failures, security issues, legal / compliance notices, and platform-side actions that affect their store. If a merchant silences too many of the toggleable notifications and then later complains "I had no idea X was happening", `alert_notification` is the channel CloudCart points back to — *that* channel is always on, and critical platform messages went through it.

### Originators are open-ended

Any platform component can raise an alert via the platform's alert helper. The list above is the verified-as-of-this-page set; future platform changes can add more originators. There is no merchant-visible registry of registered alert originators. `(verify)`

## Related

- [[settings-admin-notifications]] — hub.
- [[admin-notifications-mandatory-three]] — why this channel cannot be silenced.
- [[admin-notifications-recipient-routing]] — recipient = `site_email`.
- [[admin-notifications-delivery-queue]] — queued via `admin_notify` → `system7`.
- [[settings-domains]] — SSL expiry alert originator.
- [[settings-hooks]] — webhook auto-disable alert originator.
- [[settings-general]] — where `site_email` (the alert recipient) is configured.

## Open questions

- A complete enumeration of `alert_notification` originators in the current platform release would be valuable but is currently best-effort. `(verify)`
- Whether the alert payload includes a deep-link to the originating admin page (and how reliably) is not consistently verified across alert types. `(verify)`
