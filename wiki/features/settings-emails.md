---
type: feature
nav_path: "Settings → Emails"
route_name: emails.settings
route_path: /admin/settings/emails
aliases: ["Emails", "Mailboxes", "Email accounts", "Hosted email", "@-domain email", "Имейли", "Електронна поща", "Електронни кутии"]
tags: [settings, emails, mailbox, modoboa, webmail, discontinued]
plan_gates: ["change_email_notifications", "test_mail"]
status: DISCONTINUED
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Emails (DISCONTINUED)

> **⚠️ This service is discontinued.** CloudCart no longer offers hosted email mailboxes through this screen. New mailbox creation is not available, and existing mailboxes are being phased out. Merchants who need branded `@yourdomain` email accounts should use a third-party email provider (Google Workspace, Microsoft 365, Zoho Mail, etc.) and point their domain's MX records there via [[settings-domains]]. See [[settings-emails-discontinued]] for the migration path.

## Purpose

The merchant's **hosted email mailbox manager** (DISCONTINUED). From this screen the merchant could create and manage branded `@yourdomain` mailboxes (e.g., `info@mystore.bg`, `support@mystore.bg`) on CloudCart's Modoboa-powered mail infrastructure. Each mailbox was a separately-billed paid subscription at one of five quota tiers (1 GB to 20 GB). Once paid, the merchant logged into Webmail at `https://mail.cloudcart.com` OR configured an external client via the IMAP / SMTP / POP3 instructions surfaced from the per-row Instructions modal.

This page is the **hub** for the cluster; pick the aspect below that matches the question rather than reading end-to-end.

## Where to find it

Sidebar → Settings → **Emails**. Breadcrumb: "Settings → Emails". Header icon: `@`. The page shows an intro panel + a data table of existing mailboxes (Name, Email, Quota, Actions, Remove). The **+ Add new email** button surface is currently commented out — see [[settings-emails-discontinued]].

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice:

- [[settings-emails-create]] — the **Create new email** side modal (Name / Domain / Password / First+Last name / Quota), the POST to `/admin/api/core/settings/emails`, validation error strings, and the hand-off to `/admin/services/purchase`.
- [[settings-emails-management]] — per-row actions on an active mailbox: Webmail link, change-password modal, delete (with the 404-as-success Modoboa edge), and password-rotation side effects on Webmail sessions.
- [[settings-emails-billing]] — the per-mailbox paid subscription model, the five quota tiers (service IDs 47–51, 1 GB / 2 GB / 5 GB / 10 GB / 20 GB), the Activate flow, and the HTTP 402 re-billing path on quota upgrade.
- [[settings-emails-dns-records]] — the four DNS records auto-written to the domain's Cloudflare zone (MX, SPF, DMARC, DKIM), the per-domain DKIM selector rule, the Cloudflare-only constraint, and the contents of the Instructions modal (DKIM key, IMAP / SMTP / POP3 hostnames + ports, TLS settings).
- [[settings-emails-vs-other-mail]] — disambiguation: how this hosted-mailbox service differs from the store outgoing sender (`site_email` in [[settings-general]]), the transactional event gating in [[settings-admin-notifications]], and marketing email delivery in [[marketing-channels-email]].
- [[settings-emails-discontinued]] — deprecation context, why the two `plan_gates` (`change_email_notifications`, `test_mail`) actually enforce a different feature surface, and the recommended third-party migration path.

## What the merchant can do here

Across the cluster the merchant can:

- **List** existing mailboxes (Name, Email, Quota, Actions, Remove).
- **Create** a new mailbox when the button is enabled — see [[settings-emails-create]].
- **Activate** a mailbox after paying its subscription — see [[settings-emails-billing]].
- **Open Webmail** at `https://mail.cloudcart.com` — see [[settings-emails-management]].
- **Change password** (requires current password) — see [[settings-emails-management]].
- **Change quota tier** — see [[settings-emails-billing]] for the re-billing path.
- **View setup Instructions** for external mail clients — see [[settings-emails-dns-records]].
- **Delete** a mailbox (irreversible) — see [[settings-emails-management]].

What the merchant **CANNOT** do on this page:

- Create a mailbox on `*.cloudcart.net` or on a domain not yet attached + DNS-active in [[settings-domains]].
- Change the store's outgoing sender (`site_email`) — that's in [[settings-general]].
- Set up SMTP forwarding / aliases / auto-replies / bulk CSV import — aliases are managed inside Webmail.
- Reset a mailbox password without knowing the current one — no admin-override; the merchant must delete + recreate (losing inbox contents).
- Configure DKIM / SPF / DMARC manually — auto-set on first-mailbox activation (see [[settings-emails-dns-records]]).

## Settings & fields (top-level)

Top-level list columns (modal-level field shapes live in the aspect pages):

| Column | What it shows |
|--------|---------------|
| **Name** | First + Last name (From-header display name). |
| **Email** | Full address (`username@domain`). |
| **Quota** | Storage formatted as MB ("1 GB", "5 GB", etc.). |
| **Actions** | Webmail, Password, Quota, Instructions, Activate (if pending). |
| **Remove** | Delete icon (separate from Actions). |

The five quota tiers (service IDs 47–51) are defined in [[settings-emails-billing]]. The Instructions modal contents (DKIM, IMAP / SMTP / POP3, TLS) are in [[settings-emails-dns-records]]. Modal fields, validation messages, and UI shapes for Create / Change password / Change quota live in their respective aspect pages.

## Business rules (cluster-wide)

- **A mailbox is a separately-billed paid subscription.** Until paid, `active=no` — Webmail login fails and mail can't send / receive. Renewal failure deactivates an active mailbox. See [[settings-emails-billing]].
- **Domain must be attached + DNS-pointing first.** The Domain dropdown shows only attached external domains (`external=yes` in [[settings-domains]]); `*.cloudcart.net` is excluded. See [[settings-emails-create]].
- **DKIM / SPF / DMARC auto-configured on first mailbox per domain** — four records written to the domain's Cloudflare zone (MX, TXT `_dmarc`, TXT SPF, TXT DKIM under `<domain>._domainkey`). The DKIM selector is the domain name itself (per-domain isolation). Cloudflare-only — external-DNS domains skip silently. See [[settings-emails-dns-records]].
- **Auto-DNS records are NOT removed on mailbox deletion.** Deleting the last mailbox on a domain leaves MX / SPF / DMARC / DKIM behind; remove them manually via [[settings-domains]] → Manage DNS.
- **Hosted email vs storefront sender are separate systems.** This page never affects the `site_email` From address, the storefront transactional delivery path, or marketing campaign mail. See [[settings-emails-vs-other-mail]] for the four-system disambiguation table.
- **Mailbox deletion is irreversible.** Removes the Modoboa account permanently (inbox / sent / drafts lost), deactivates the subscription, removes the local row. No soft-delete. A 404 from Modoboa on delete is treated as success. See [[settings-emails-management]].
- **Webmail uses a separate session.** No SSO from admin into `https://mail.cloudcart.com`. Password rotation does NOT invalidate existing Webmail sessions immediately.
- **Permissions.** Requires the `settings` + `settings.emails` permission grants. Moderators ([[settings-staff]]) without the grant don't see the sidebar entry.
- **Plan gates on this hub (`change_email_notifications`, `test_mail`) enforce a different surface** — the transactional-mail template editor and the **Send test email** button on [[settings-admin-notifications]]. The mailbox subscription itself is billed via the standard service-order flow, NOT via a plan-feature gate. See [[settings-emails-discontinued]].

## Related

- [[settings]] — parent hub.
- [[settings-general]] — the store's outgoing sender (`site_email`) lives here, NOT on this page.
- [[settings-domains]] — the domain on which the mailbox is hosted must first be attached and DNS-active here; auto-DNS records appear in the DNS modal there after mailbox creation.
- [[settings-admin-notifications]] — controls WHICH transactional events the store sends. Unrelated to the hosted-mailbox service on this page.
- [[marketing-channels-email]] — marketing email delivery via the merchant's external SMTP provider — separate system, separate config.
- [[settings-staff]] — moderator permission grants for the Emails section.
- [[plan-services]] — paid services (including these mailboxes' subscriptions) are billed through the platform's plan / services billing.
- [[plan-gates]] — plan / app-purchase mechanics shared with mailbox subscriptions.
- [[background-queue-inventory]] — catalogue of all background processes; covers the daily Modoboa mailbox-sync job.

## Open questions

_None._
