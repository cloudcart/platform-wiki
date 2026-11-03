---
type: feature
nav_path: "Settings → Notifications to administrators → Recipient routing"
route_name: admin-notifications.settings
route_path: /admin/settings/admin-notifications
aliases: ["Admin notification recipient", "site_email recipient", "Where do admin notifications go", "Single recipient model", "Admin notification sender", "CloudCart sender"]
tags: [settings, notifications, email]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-admin-notifications]]. See the hub for the other aspects (master switch, per-type toggles, mandatory three, delivery queue, alert triggers, permissions / locale).

# Admin notifications — recipient routing

## Purpose

Documents who receives admin notifications. For 15 of the 17 notification types, the recipient is a single address — the store's primary email (`site_email`) configured on [[settings-general]]. The other two types (`email_confirmation`, `two_factor_action`) route to specific addresses for security reasons. The sender (From header) is CloudCart-branded for all admin notifications, not the store's own configured sender.

This is a single-recipient model — there is no per-administrator opt-in, no copy-everybody fan-out, and no "send to all moderators" option.

## Where to find it

The recipient address itself is not edited on the admin notifications page. It lives on [[settings-general]] under Store Details → Email (the `site_email` field). The [[settings-admin-notifications]] page only controls **which** notifications fire and **whether** the master switch is on; **where** they go is determined elsewhere.

## What the merchant can do here

- Decide which recipient strategy to use by editing `site_email` on [[settings-general]] — a personal mailbox, a shared inbox, or a forwarding alias.
- (Indirectly) ensure 2FA codes arrive at each admin user's personal address by keeping their admin-user email up to date on [[settings-staff]].

The merchant cannot:

- Configure per-administrator opt-in or per-administrator copies. The single-recipient model has no fan-out layer.
- Configure a different recipient per notification type. The 15 non-exception types all share `site_email`.
- Override the From / sender header. Admin notifications always send from CloudCart's platform sender.
- Add a CC or BCC. The platform sends to exactly one recipient per dispatch.

## Settings & fields

The relevant fields all live on other pages (none on this one):

| Setting | Where to edit | What it does |
|---------|---------------|--------------|
| `site_email` | [[settings-general]] → Store Details → Email | Default recipient for 15 of 17 notification types. |
| Admin user's email | [[settings-staff]] → Edit user | Recipient for `two_factor_action` codes for that specific admin. |
| Sender / From address | (not editable) | Fixed to CloudCart's platform sender for admin notifications. |

## Modals and sub-flows

None on this page. The two-code email-change flow that triggers `email_confirmation` is a sub-flow of [[settings-general]], not of [[settings-admin-notifications]].

## Business rules

### Recipient is `site_email` (with two exceptions)

For 15 of the 17 notification types, the recipient is `site_email` — the store's primary email configured on [[settings-general]]. This means:

- If the merchant has multiple administrators or moderators, **only the store email gets the notifications**. Individual admins do not receive their own copies. There is no per-administrator opt-in/opt-out.
- Changing the store email on [[settings-general]] redirects ALL admin notifications to the new address starting from the next dispatched email.
- If `site_email` is wrong or has a typo, **every admin notification is silently misdelivered** until corrected.

The two exceptions:

- **`email_confirmation`** — addressed to the specific email being verified during the two-step email change flow (one code to the OLD address, one to the NEW). Documented under [[settings-general]] → Business rules and on [[admin-notifications-mandatory-three]].
- **`two_factor_action`** — addressed to the user's own email (the admin attempting the 2FA-protected action), not the store email.

### Single-recipient — no per-administrator copies

The platform has NO mechanism for sending copies of admin notifications to individual administrators or moderators on top of the store's `site_email`. All notifications go to that one address. If a merchant wants multiple humans to receive admin notifications, the recommended pattern is:

- **Set `site_email` to a shared inbox** (e.g., `team@merchant.com`) and rely on the merchant's own email provider to forward to multiple recipients.
- Or **set `site_email` to a distribution list / Google Group / Microsoft 365 distribution group** that fans out to the desired recipients.

The platform itself does not implement any fan-out — that's the merchant's email provider's job.

### Sender is CloudCart, not the store

Outgoing admin notifications use a CloudCart-branded From header — the platform's system sender, not the store's own configured sender (which is used for customer-facing transactional mail). Merchants should expect admin notifications to arrive from a CloudCart-branded address, not from their store's own domain. This means:

- Filtering rules in the merchant's inbox should match the CloudCart sender domain, not the store's domain.
- The admin notification will not appear in the "Sent" folder of the store's own SMTP / Gmail-with-aliases setup, because the store's sender wasn't used.
- SPF / DKIM alignment is on the CloudCart domain, not the store's domain.

### Typo in `site_email` = silent misdelivery

There is no "delivery confirmed" indicator on either [[settings-admin-notifications]] or [[settings-general]]. A typo in `site_email` causes every admin notification to bounce or land somewhere the merchant doesn't read — without any in-app warning. Practical guidance: after changing `site_email`, the merchant should trigger one of the toggleable notifications (e.g., place a small test order) and verify it arrives in the inbox.

### Mandatory-three exceptions are documented separately

The recipient-routing exceptions for `email_confirmation` and `two_factor_action` are covered on [[admin-notifications-mandatory-three]]. This page covers the rule + names the exceptions; the mandatory-three page covers why those exceptions exist (security: prove control of the specific address being verified or used).

## Related

- [[settings-admin-notifications]] — hub.
- [[settings-general]] — where `site_email` is configured.
- [[settings-staff]] — admin user emails (recipient for `two_factor_action`).
- [[admin-notifications-mandatory-three]] — the recipient rules for the two exception types.
- [[admin-notifications-delivery-queue]] — how the dispatch reaches the recipient.
- [[admin-notifications-master-switch]] — the gate that, when off, suppresses dispatch entirely (no recipient at all).

## Open questions

None.
