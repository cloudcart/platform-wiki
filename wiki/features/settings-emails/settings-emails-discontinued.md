---
type: feature
nav_path: "Settings → Emails → Discontinued context"
route_name: emails.settings
route_path: /admin/settings/emails
aliases: ["Hosted email discontinued", "Mailbox service deprecated", "Email service phase-out", "Third-party email migration", "Modoboa discontinuation"]
tags: [settings, emails, discontinued, deprecation, migration, plan-gates]
plan_gates: ["change_email_notifications", "test_mail"]
status: DISCONTINUED
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-emails]] (DISCONTINUED). See the hub for related aspects (create, management, billing, DNS records, vs-other-mail).

# Emails — Discontinued context

## Purpose

CloudCart's hosted email mailbox service is **discontinued**. New mailbox creation is not available through the live UI (the **+ Add new email** button surface is commented out), and existing mailboxes are being phased out. This page explains the deprecation context: why the service was wound down, the recommended third-party migration path, and why the two `plan_gates` listed on [[settings-emails]] (`change_email_notifications`, `test_mail`) actually enforce a different feature surface.

## Where to find it

Settings → Emails — the screen still loads with its discontinued banner at the top. The screen remains in the navigation so existing mailbox owners can still:

- View their list of existing mailboxes.
- Open Webmail (the underlying Modoboa platform is still serving them).
- Change passwords on existing mailboxes.
- Delete a mailbox they no longer need.

New mailbox creation is unavailable.

## What the merchant can do here

### Continue using existing mailboxes (phase-out period)

Existing mailboxes continue to work until the merchant deletes them or the platform completes its phase-out. Per-row actions (Webmail, Password, Quota, Instructions, Delete — see [[settings-emails-management]]) remain functional.

### Migrate to a third-party email provider

The recommended migration path:

1. Sign up with a third-party email provider — Google Workspace, Microsoft 365 (Outlook for Business), Zoho Mail, or any provider that supports custom-domain email hosting.
2. Configure the provider's mail accounts for the merchant's addresses (e.g., `support@mystore.bg`, `info@mystore.bg`).
3. Update the merchant's domain DNS to point MX records at the new provider. **This requires editing the auto-set MX record** that CloudCart wrote during hosted-email activation — see [[settings-emails-dns-records]] for the four auto-records. The MX (and likely the SPF + DKIM) need to be replaced with the new provider's values via [[settings-domains]] → per-row **Manage DNS**.
4. Migrate inbox contents — usually via the new provider's IMAP migration tool, using the IMAP credentials from the **Instructions** modal on the legacy CloudCart mailbox.
5. Once cutover is verified, delete the legacy CloudCart mailbox (see [[settings-emails-management]] — deletion is irreversible and removes the inbox permanently from Modoboa, so make sure migration completed first).

### What to update at the same time

- **Outgoing transactional sender** (`site_email` in [[settings-general]]) — if it was a hosted mailbox address, decide whether to point it at the new provider's mailbox OR keep it as a no-reply address using CloudCart's transactional infrastructure (recommended; see [[settings-emails-vs-other-mail]]).
- **Marketing channel** ([[marketing-channels-email]]) — if marketing campaigns were sent through the legacy SMTP, point them at the new provider's SMTP.

## Settings & fields

This page does not expose configuration. It documents the discontinued banner and migration guidance.

### The discontinued banner (verbatim)

> ⚠️ This service is discontinued. CloudCart no longer offers hosted email mailboxes through this screen. New mailbox creation is not available, and existing mailboxes are being phased out. Merchants who need branded `@yourdomain` email accounts should use a third-party email provider (Google Workspace, Microsoft 365, Zoho Mail, etc.) and point their domain's MX records there via Domains.

## Business rules

### Why the two listed plan_gates don't actually gate this screen

The [[settings-emails]] hub lists two plan-features in its frontmatter: `change_email_notifications` and `test_mail`. Both were assigned to this page in the audit pass, but they were **verified in code to enforce a different feature surface**:

| Mapping | Shape | What it ACTUALLY controls |
|---|---|---|
| `change_email_notifications` | Access gate | Path-restricts the **admin / customer notification email TEMPLATE editor** at `marketing/omnichannel/mails/edit/%` (the screen where the merchant customises the body of order-confirmation, password-reset, abandoned-cart and other transactional mails). Lower plans see HTTP 402 / redirect to the [[plan-features]] upsell when reaching the per-template editor. Properly belongs to [[settings-admin-notifications]] / the transactional-mail editing flow. |
| `test_mail` | Boolean (plan-level enable) | Gates the **Send test email** button in the admin notifications controller — when false, the controller exposes `allow_test_mail = false` and the action is rejected. Properly belongs to [[settings-admin-notifications]]. |

The discontinued mailbox subscription itself was paid **per-mailbox via the standard service-order flow** — see [[settings-emails-billing]] — NOT via a plan-feature gate. So in practice, lower-plan merchants could (when the service was live) still buy hosted mailboxes individually if they could pay for the service order.

These two `plan_gates` are kept on the hub frontmatter for legacy audit-trail reasons, but the active enforcement surface for both is the admin-notification mail-template editor (verify).

### The screen remains accessible (read-only-ish) during phase-out

The route `/admin/settings/emails` still resolves to the EmailsSettings component. Existing mailboxes render in the list. The Create modal surface is commented out, but the per-row management actions ([[settings-emails-management]]) and the billing surfaces ([[settings-emails-billing]]) remain available so existing mailbox owners can keep operating their accounts during migration.

### After complete phase-out

When CloudCart completes the phase-out (date not yet announced — verify), the screen may either be removed entirely or kept as a stub showing only the migration guidance. The Modoboa infrastructure will be decommissioned; mailbox owners who haven't migrated will lose access. Support guidance: encourage migration well ahead of any announced cutoff.

### Active state on existing mailboxes

Existing mailboxes whose subscriptions stay paid remain `active=yes` and continue to send / receive mail through Modoboa. Renewal failure deactivates the mailbox per the normal subscription lifecycle — see [[settings-emails-billing]]. The merchant cannot reactivate it via a fresh purchase because the Create surface is unavailable; they'd need to use the per-row Activate action if the row is still present, or migrate to a third-party provider.

## Related

- [[settings-emails]] — hub.
- [[settings-emails-create]] — Create flow, currently with the trigger button commented out.
- [[settings-emails-management]] — per-row actions that remain available during phase-out.
- [[settings-emails-billing]] — subscription lifecycle for existing mailboxes.
- [[settings-emails-dns-records]] — DNS records the merchant must edit when migrating to a third-party provider.
- [[settings-emails-vs-other-mail]] — disambiguation of the four mail systems; clarifies what migration affects and what it doesn't.
- [[settings-domains]] — where MX / SPF / DKIM records are edited when re-pointing to a third-party provider.
- [[settings-general]] — `site_email` may also need re-pointing during migration.
- [[settings-admin-notifications]] — the actual home for the two `plan_gates` listed on the hub.

## Open questions

- Final cutoff date for the phase-out is not announced in any code or config file currently visible (verify).
