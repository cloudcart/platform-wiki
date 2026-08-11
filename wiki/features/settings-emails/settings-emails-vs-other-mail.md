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
updated: 2026-06-10
source_count: 3
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
| **Store outgoing sender (`site_email`)** | [[settings-general]] | The **From address** on transactional emails sent by the store (order confirmations, password resets, customer notifications). Typically a no-reply address. | The Reply-To address of marketing campaigns. The delivery path (CloudCart's own infrastructure or marketing channel — not the hosted mailbox SMTP). |
| **Transactional event gating** | [[settings-admin-notifications]] | **Which** transactional events the store sends (using `site_email` from [[settings-general]] as both sender and admin recipient). The admin's low-stock alerts, new-order notifications, etc. | The mailbox infrastructure. The marketing campaign delivery. |
| **Marketing email delivery** | [[marketing-channels-email]] | Marketing campaign mail delivery via the merchant's external SMTP provider (SendGrid, Mailgun, Mailchimp, etc.). Newsletters, promotions, abandoned-cart recovery. | The transactional events. The hosted-mailbox infrastructure. |

### Setting key cross-reference

| Key | Where | What it sets |
|---|---|---|
| `site_email` | [[settings-general]] | From address on transactional store emails (and the admin recipient on admin notifications). |
| Modoboa per-mailbox subscription | [[settings-emails]] | Hosted mailbox (DISCONTINUED). |
| Per-event toggles | [[settings-admin-notifications]] | Which transactional events fire. |
| Marketing channel SMTP config | [[marketing-channels-email]] | External SMTP relay for marketing mail. |

## Business rules

### Hosted email vs storefront sender — completely separate

This page (and [[settings-emails]]) does NOT affect:

- The **From address** on transactional emails sent by the store. That is `site_email` in [[settings-general]] — typically a no-reply address that need NOT be a hosted mailbox at all.
- The **delivery mechanism** for storefront transactional mail. The platform sends those through its own infrastructure (or through CloudCart's marketing channels — see [[marketing-channels-email]]); they do NOT go through the hosted mailbox SMTP.
- The **marketing campaign mail**. Marketing emails go through the configured marketing channel ([[marketing-channels-email]]) — typically the merchant's own SendGrid / Mailgun / Mailchimp etc.

### A common merchant configuration

A typical merchant can have all three running simultaneously, on the same domain:

- `support@mystore.bg` as a hosted mailbox (or, post-discontinuation, in Google Workspace) where customers email them directly.
- `no-reply@mystore.bg` (or any other address) as the store's transactional sender configured in [[settings-general]]'s `site_email`.
- `marketing@mystore.bg` configured for outgoing marketing campaigns via [[marketing-channels-email]].

All three can use the same domain but they are independent setups. Changing one does NOT affect the others.

### Support-ticket triage examples

| Merchant question | Where to point them |
|---|---|
| *"Customers are emailing `info@mystore.bg` but it bounces."* | [[settings-emails]] — is the hosted mailbox active and paid? Or migrate to a third-party provider. |
| *"My order confirmations are going to spam."* | [[settings-general]] (`site_email`) + [[settings-domains]] DNS records (SPF / DKIM for the sender domain). |
| *"I want to stop getting low-stock alerts."* | [[settings-admin-notifications]] — toggle the event off. |
| *"My newsletter campaign didn't send."* | [[marketing-channels-email]] — check the configured SMTP provider's status / quota. |
| *"How do I change the From address on order confirmation emails?"* | [[settings-general]] (`site_email`) — NOT [[settings-emails]]. |

### What `site_email` does (and doesn't)

`site_email` in [[settings-general]] is the **transactional From address**. It does NOT need to be a hosted mailbox — it can be any address the merchant controls. The merchant only needs to make sure the domain's SPF / DKIM are set up so receiving mail servers don't reject it as spoofed.

If the merchant uses a hosted mailbox address (e.g., `no-reply@mystore.bg`) as `site_email`, the transactional mail still goes through CloudCart's transactional infrastructure — NOT through the hosted-mailbox SMTP. The address is just the From label.

## Related

- [[settings-emails]] — hub (this disambiguation table's primary subject).
- [[settings-general]] — `site_email` (the transactional From address); two-step double-confirmation flow on change.
- [[settings-admin-notifications]] — which transactional events fire; admin-recipient gating.
- [[marketing-channels-email]] — marketing email delivery via external SMTP.
- [[settings-domains]] — the shared domain layer that all four mail systems sit on top of.

## Open questions

None.
