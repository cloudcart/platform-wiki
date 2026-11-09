---
type: feature
nav_path: "Settings → Emails → Disambiguation vs other mail systems"
route_name: emails.settings
route_path: /admin/settings/emails
aliases: ["Hosted email vs site email", "Hosted mailbox vs transactional sender", "Mailbox vs marketing email", "Mail systems comparison", "site_email vs hosted mailbox"]
tags: [settings, emails, disambiguation, transactional, marketing, discontinued]
plan_gates: []
status: DISCONTINUED
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-emails]] (DISCONTINUED). See the hub for related aspects (create, management, billing, DNS records, discontinued context).

# Emails — Disambiguation vs other mail systems

## Purpose

CloudCart has **four distinct mail systems** that merchants regularly confuse. This page is the lookup table: which screen controls which mail flow, and which never affects which. The hosted-mailbox service documented in [[settings-emails]] is one of these four — and the most commonly misunderstood, because the name "Emails" sounds general but it's a narrow INBOX-style hosted-mailbox manager.

## Where to find it

Reference page only — no direct UI surface. The four mail systems live at:

- Hosted mailboxes: Settings → **Emails** (this cluster — [[settings-emails]]).
- Store outgoing sender: Settings → **General**.
- Transactional event gating: Settings → **Admin notifications**.
- Marketing email delivery: Marketing → **Channels** → **Email**.

## What the merchant can do here

This page does not expose actions. It maps merchant questions to the correct screen.

## Settings & fields

### The four mail systems at a glance

| System | Where | What it controls | What it does NOT control |
|--------|-------|------------------|--------------------------|
| **Hosted mailboxes** | [[settings-emails]] | Branded `@yourdomain` INBOX-style mailboxes for the merchant to receive customer mail (`support@`, `info@`, etc.). Modoboa-hosted. DISCONTINUED. | Anything the store sends. Does not set the From address of any transactional or marketing email. |
| **Store email (`site_email`)** | [[settings-general]] | The store's own address on its notifications to customers (order confirmations, password resets): their **Reply-To**, since the From is noreply@cloudcart.com with the store's name, or their **From** when the [[apps-smtp|SMTP app]] sends them. | The sender or Reply-To of campaigns (the Email channel's own sender address). The delivery path. |
| **Transactional event gating** | [[settings-admin-notifications]] | **Which** transactional events the store sends (using `site_email` from [[settings-general]] as the admin recipient). The admin's low-stock alerts, new-order notifications, etc. | The mailbox infrastructure. The marketing campaign delivery. |
| **Campaign email delivery** | [[marketing-channels-email]] | Campaign mail (newsletters, promotions, automated campaigns) and the subscriber confirmation, sent through the store's Elastic Email sub-account that CloudCart runs, From the channel's sender address with Reply-To the same address. | The notifications, including the abandoned-cart reminder. The hosted-mailbox infrastructure. |

### Setting key cross-reference

| Key | Where | What it sets |
|---|---|---|
| `site_email` | [[settings-general]] | Reply-To (From with the SMTP app) on notifications to customers, and the admin recipient on admin notifications. |
| Modoboa per-mailbox subscription | [[settings-emails]] | Hosted mailbox (DISCONTINUED). |
| Per-event toggles | [[settings-admin-notifications]] | Which transactional events fire. |
| Email channel sender address | [[marketing-channels-email]] | From and Reply-To of campaign mail. |

## Business rules

### Hosted email vs storefront sender — completely separate

This page (and [[settings-emails]]) does NOT affect:

- The sender of the store's notifications. They go From noreply@cloudcart.com with the store's name and Reply-To `site_email` from [[settings-general]], which need NOT be a hosted mailbox.
- The **delivery mechanism** for the notifications. The platform sends them through CloudCart's shared sending account, or the store's own server via the [[apps-smtp|SMTP app]]; never through the Email channel or the hosted mailbox SMTP.
- The **campaign mail**. It goes through the Email channel ([[marketing-channels-email]]), the store's Elastic Email sub-account that CloudCart runs.

### A common merchant configuration

A typical merchant can have all three running simultaneously, on the same domain:

- `support@mystore.bg` as a hosted mailbox (or, post-discontinuation, in Google Workspace) where customers email them directly.
- `info@mystore.bg` (or any other address) as the store's email in [[settings-general]] (`site_email`), the Reply-To of its notifications.
- `marketing@mystore.bg` configured for outgoing marketing campaigns via [[marketing-channels-email]].

All three can use the same domain but they are independent setups. Changing one does NOT affect the others.

### Support-ticket triage examples

| Merchant question | Where to point them |
|---|---|
| *"Customers are emailing `info@mystore.bg` but it bounces."* | [[settings-emails]] — is the hosted mailbox active and paid? Or migrate to a third-party provider. |
| *"My order confirmations are going to spam."* | Sent by CloudCart's shared account, they don't depend on the store's DNS. With the [[apps-smtp|SMTP app]], the store's domain needs SPF / DKIM for that server ([[settings-domains]]). |
| *"I want to stop getting low-stock alerts."* | [[settings-admin-notifications]] — toggle the event off. |
| *"My newsletter campaign didn't send."* | [[marketing-channels-email]] — check the Email card: Reconnect ([[email-channel-reconnect]]), suspension, plan limit. |
| *"How do I change the From address on order confirmation emails?"* | They go From noreply@cloudcart.com; `site_email` in [[settings-general]] is their Reply-To. A From on the store's own domain needs the [[apps-smtp|SMTP app]]. NOT [[settings-emails]]. |

### What `site_email` does (and doesn't)

`site_email` in [[settings-general]] is the **Reply-To** of the store's notifications to customers (their From is noreply@cloudcart.com), and their **From** only when the [[apps-smtp|SMTP app]] sends them; then the domain's SPF / DKIM must cover that server. It does NOT need to be a hosted mailbox — it can be any address the merchant controls.

If the merchant uses a hosted mailbox address (e.g., `no-reply@mystore.bg`) as `site_email`, the transactional mail still goes through CloudCart's transactional infrastructure — NOT through the hosted-mailbox SMTP. The address is only the Reply-To.

## Related

- [[settings-emails]] — hub (this disambiguation table's primary subject).
- [[settings-general]] — `site_email` (the transactional From address); two-step double-confirmation flow on change.
- [[settings-admin-notifications]] — which transactional events fire; admin-recipient gating.
- [[marketing-channels-email]] — campaign email delivery through the store's Elastic Email sub-account.
- [[apps-smtp]] — notifications through the store's own mail server.
- [[settings-domains]] — the shared domain layer that all four mail systems sit on top of.

## Open questions

None.
