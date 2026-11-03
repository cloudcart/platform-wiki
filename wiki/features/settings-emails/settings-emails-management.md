---
type: feature
nav_path: "Settings → Emails → Per-mailbox management"
route_name: emails.settings
route_path: /admin/settings/emails
aliases: ["Mailbox management", "Mailbox actions", "Change mailbox password", "Delete mailbox", "Mailbox row actions", "Webmail link"]
tags: [settings, emails, mailbox, password, delete, webmail, discontinued]
plan_gates: []
status: DISCONTINUED
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-emails]] (DISCONTINUED). See the hub for related aspects (create, billing, DNS records, vs-other-mail, discontinued context).

# Emails — Per-mailbox management

## Purpose

Once a mailbox is created and activated, each row in the Emails list exposes a column of **per-row actions**: open Webmail in a new tab, change the mailbox password, manage the quota tier (see [[settings-emails-billing]]), view setup instructions (see [[settings-emails-dns-records]]), and delete the mailbox. This page covers Webmail handoff, the change-password modal, the delete action and its 404-as-success edge, and the password-rotation side effects.

## Where to find it

Settings → Emails → per-row **Actions** column. Each active mailbox row shows: Webmail link, Password change, Quota change, Instructions, and a separate trash icon for Delete. If the mailbox subscription is unpaid, the row shows **Activate** instead of the normal action set — see [[settings-emails-billing]].

## What the merchant can do here

### Webmail (per-row link)

Opens `https://mail.cloudcart.com` in a new tab. The merchant signs in there with the mailbox credentials (email + password) to read / send messages. **There is no single-sign-on from the admin panel into Webmail** — Webmail uses a separate session.

### Change password modal

Standard b-modal (centred, not side-mounted). Header title: *"Change email account password"*. Body is a single-column b-card with three stacked PasswordInputComponent rows:

1. **Current password** (`current_password`) — required, validated server-side by Modoboa.
2. **New password** (`password`) — required.
3. **Confirm your password** (`password_confirmation`) — required, must match.

PATCHes the password-change endpoint. Modoboa returns 400 on wrong current password, surfaced inline.

### Change quota modal

Same standard b-modal shell as the password change modal (single Vue component `PasswordAndQuotaChange` handles both via a `type` prop — `password` or `quota`). Body is a single AJAX-fed SelectWithAjax labelled *"Quota"* (resolve-on-load), populated from `/admin/api/core/settings/emails/services`. See [[settings-emails-billing]] for the tier table and the HTTP 402 re-billing path.

### Instructions modal

Standard b-modal, content rendered by the `InstructionsPreview` component. Body fetches live connection details from `/admin/api/core/settings/emails/instructions/<account_id>/<domain_id>` so DKIM key + server hostnames are always current, not snapshotted. See [[settings-emails-dns-records]] for the full Instructions modal contents.

### Delete (per-row trash icon)

Triggered from the per-row icon column. Calls `DELETE /admin/api/core/settings/emails/<id>`.

**There is no Vue-side confirmation modal** for the delete — clicking immediately initiates the request. The backend may have its own confirm logic but the page-side UX is direct-action. (Compare with bulk-delete patterns elsewhere that DO confirm.)

On success:

- The mailbox account is deleted from the Modoboa platform (with retry on transient ClientException).
- The paid subscription is deactivated (no further billing).
- The local row is removed from the list.
- Toast: *"Deleted successfully"*.

## Settings & fields

### Change password modal

| Field | Required |
|-------|----------|
| **Current password** | YES |
| **Password** | YES (new password) |
| **Confirm your password** | YES (must match) |

### Change quota modal

| Field | What it does |
|-------|--------------|
| **Quota** | Dropdown of available storage tiers. Changing requires re-payment if the tier is more expensive — see [[settings-emails-billing]]. |

### Per-row Actions column

| Action | Trigger | Endpoint |
|--------|---------|----------|
| Webmail | New-tab link | `https://mail.cloudcart.com` |
| Password | Modal | `PATCH /admin/api/core/settings/emails/<id>` (password change) |
| Quota | Modal | `PATCH` change-quota endpoint |
| Instructions | Modal | `GET /admin/api/core/settings/emails/instructions/<account_id>/<domain_id>` |
| Activate (if unpaid) | Redirect | `/admin/services/purchase` — see [[settings-emails-billing]] |
| Delete | Direct (no confirm) | `DELETE /admin/api/core/settings/emails/<id>` |

## Business rules

### Password change must verify current password

The change-password endpoint requires the current password as a separate input. Modoboa rejects the change if the current password is wrong. The platform surfaces the rejection as a JSON 400 error.

There is **no admin-override "reset" button**. If the mailbox owner forgets their password, the merchant must delete the mailbox and recreate it (which loses inbox contents).

### Password rotation does NOT invalidate Webmail sessions

After a successful password change, existing logged-in Webmail sessions for that mailbox are NOT invalidated immediately. The merchant would need to log out manually in Webmail or wait for the session to expire. Only the new password works for fresh logins after the change.

### Webmail uses a separate session

Admin-panel login does NOT auto-log into Webmail. The merchant types the mailbox email + password at `mail.cloudcart.com` to access the inbox. This is intentional — Webmail is Modoboa's session, not CloudCart's.

### Mailbox deletion is irreversible

Deleting a mailbox:

- Removes the Modoboa account permanently (all inbox / sent / drafts are deleted).
- Deactivates the paid subscription.
- Removes the local row from CloudCart's database.

There is no soft-delete / recovery. If the merchant deletes a mailbox by mistake, they must recreate it via [[settings-emails-create]] (losing all historical inbox content) and re-pay the subscription.

### Delete does NOT remove auto-DNS records

If the merchant deletes their **last mailbox on a domain**, the auto-set MX / SPF / DMARC / DKIM records stay in the domain's Cloudflare zone until removed manually from [[settings-domains]]' DNS modal. See [[settings-emails-dns-records]] for the auto-DNS rule.

### 404 from Modoboa on delete is treated as success

If Modoboa returns a 404 during delete (i.e., the mailbox doesn't exist on Modoboa's side anymore), the platform proceeds with local cleanup as if the delete succeeded. This guards against orphan local records when Modoboa's state and CloudCart's state drift.

### What the merchant CANNOT do from row actions

- Configure aliases, forwarding rules, or auto-replies — those are managed inside Webmail by the mailbox owner directly.
- See email-by-email activity / logs — also Webmail-only, per-mailbox.
- Reset a mailbox password without knowing the current one.

## Related

- [[settings-emails]] — hub.
- [[settings-emails-create]] — create modal (the source of new mailboxes that then surface these row actions).
- [[settings-emails-billing]] — Activate action, subscription state, change-quota re-billing path.
- [[settings-emails-dns-records]] — Instructions modal contents (DKIM key + IMAP / SMTP / POP3 details).

## Open questions

None.
