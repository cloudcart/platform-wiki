---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Email channel", "Email setup", "Elastic Email", "Email marketing channel", "Имейл канал", "Настройка на имейл"]
tags: [marketing, channels, email, elastic-email, dkim, spf]
plan_gates: ["campaign.channel.email"]
created: 2026-05-23
updated: 2026-06-10
source_count: 11
---

# Email channel

## Purpose

The **Email channel** is the merchant's main outbound bulk-email delivery pipe — used for newsletters, promotional campaigns, abandoned-cart recovery, drip sequences, and any other marketing message sent via [[marketing-campaigns|Campaigns]]. Behind the scenes, CloudCart connects to **Elastic Email** (`api.elasticemail.com/v2/`) and creates a dedicated **sub-account** per store, isolating each merchant's sender reputation, bounce list, and statistics.

This is also the channel used for the platform's transactional emails (order confirmation, password reset, account verification, abandoned cart) when the merchant has the [[marketing-omnichannel-mails-list|Email notifications]] system point to the Elastic Email channel. The same plan-cap (`campaign.channel.email`) and sender-domain setup applies in both cases.

To send any production email, the merchant must complete a **four-step setup**: profile, domain, DNS verification (SPF / DKIM / Tracking CNAME / DMARC), then sender mailbox. The channel cannot be activated for campaign use until all four steps are green — see [[email-channel-setup-wizard]] for the full wizard and [[email-channel-dns-records]] for the four DNS records.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → click the **Email** channel card → **Configure** opens the email setup as a modal over the channels page. There is no separate route per step — the modal advances internally, driven by a `current_step` value. The modal's step keys are `profile` → `domain` → `verify` → `email`.

**Saved email templates** live on a separate route, `campaigns-email-saved-templates` (`/admin/marketing-new/campaigns/configuration/channel/email/saved`).

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[email-channel-setup-wizard]] — the 4-step Configuration modal (Profile / Domain / Verify / Sender email) + Completed review pane + Edit Profile / Edit Domain / Edit Email re-entry.
- [[email-channel-dns-records]] — the four required DNS records (SPF / Tracking CNAME / DKIM / DMARC); auto-CNAME on Cloudflare-managed zones; the per-method `Domain.Verify*` flow and post-verify webhook registration.
- [[email-channel-elastic-email-account]] — CloudCart-owned master account + per-store sub-account model; `{primary-host}@cloudcart.net` convention; credentials persistence + audit; **Reset configuration** flow (with preserved settings).
- [[email-channel-webhook-feedback]] — the delivery-status webhook (`messages/elastic-email-campaign/{site_id}`); status mapping (Sent / Opened / Clicked / Unsubscribed / Error / AbuseReport / WaitingToRetry); per-event subscriber-side effects.
- [[email-channel-send-pipeline]] — per-recipient send job; subscriber pre-flight checks; variable substitution + UTM injection; `{$verify_url}` / `{$subscriber_email}` merge tags; demo / test sends; saved vs predefined templates; `message_html` validation (incl. base64-image rejection).
- [[email-channel-suspend-thresholds]] — `SUSPENDED_SPAM = 0.5`, `SUSPENDED_BOUNCED = 5`, `SUSPENDED_OPEN = 5`; reputation ≥ 99 exemption; suspend recovery (no self-service unsuspend).
- [[email-channel-settings-pane]] — the **Settings - Email** modal + the single `unconfirmed_send` switch (default OFF); the per-recipient *"No message will be sent to this email because it has not been verified."* log when OFF.

## What the merchant can do here

- **Configure** the Email channel via the 4-step wizard — see [[email-channel-setup-wizard]].
- **Edit Profile / Edit Domain / Edit Email** to change any step after completion. Changing the domain wipes verify / email / send_email / configured settings — re-verification required.
- **Reset configuration** — nuclear wipe (offered when an `expired` error pops up) — see [[email-channel-elastic-email-account]].
- Toggle **Sending emails to unverified subscribers** (`unconfirmed_send`) — see [[email-channel-settings-pane]].
- View **Reputation** — live spam% / bounce% / open% / click% / reputation% from Elastic Email's `Account.LoadReputationImpact`. The thresholds that drive auto-suspend live on [[email-channel-suspend-thresholds]].
- Manage **Saved templates** — merchant-curated reusable HTML email layouts. See [[email-channel-send-pipeline]].
- View **Logs** — per-message delivery history with full content preview (iframe). Status values are written by the feedback webhook — see [[email-channel-webhook-feedback]].

## Settings & fields

Detail lives on the aspect pages; this is the quick-reference index.

### Wizard step endpoints (base `/admin/api/core/marketing/campaigns/channels`)

| Step | Step key | Endpoint | Aspect page |
|---|---|---|---|
| Profile | `profile` | `POST /email/configuration/profile` | [[email-channel-setup-wizard]] |
| Domain | `domain` | `POST /email/configuration/domain` | [[email-channel-setup-wizard]] |
| Verify | `verify` | `GET /email/configuration/verify-domain` (+ `/verify-domain/info`) | [[email-channel-dns-records]] |
| Sender email | `email` | `POST /email/configuration/email` | [[email-channel-setup-wizard]] |
| (state load) | — | `GET /email/configuration` | [[email-channel-setup-wizard]] |
| Reset | — | `campaigns.channels.channel.reset` | [[email-channel-elastic-email-account]] |

### Per-channel settings the merchant can toggle

| Setting | Default | Where to find it |
|---|---|---|
| `unconfirmed_send` | `false` | [[email-channel-settings-pane]] |

### Hard-coded thresholds (`EmailChannelManager`)

| Constant | Value | Aspect page |
|---|---|---|
| `API_URL` | `https://api.elasticemail.com/v2/` | [[email-channel-elastic-email-account]] |
| `SUSPENDED_SPAM` | `0.5` | [[email-channel-suspend-thresholds]] |
| `SUSPENDED_BOUNCED` | `5` | [[email-channel-suspend-thresholds]] |
| `SUSPENDED_OPEN` | `5` | [[email-channel-suspend-thresholds]] |

### Validation summary

| Field | Validation | Aspect page |
|---|---|---|
| Profile fields (First / Last / Country / State / City / Zip / Address / Phone) | All `required`; Phone via `phone_number` rule (E.164) | [[email-channel-setup-wizard]] |
| Company | Not required | [[email-channel-setup-wizard]] |
| Sender mailbox prefix | `email_prefix` custom rule — RFC-email-valid against synthetic `{prefix}@gmail.com` | [[email-channel-setup-wizard]] |
| Template `name` | `required\|max:191` | [[email-channel-send-pipeline]] |
| Template `subject` | `required\|max:191` | [[email-channel-send-pipeline]] |
| Template `message_html` | `required\|string`; base64-embedded local images rejected — *"Local image paste has been disabled. Local images have been removed from pasted content."* | [[email-channel-send-pipeline]] |

## Business rules

The deep mechanics live on each aspect page; what every merchant must know at this level:

- **CloudCart owns the Elastic Email account; per-store sub-accounts.** The merchant doesn't bring their own Elastic Email contract — CloudCart pays Elastic Email centrally and bills the merchant via the plan-cap `campaign.channel.email`. The `account_token` (sub-account API key) is stored server-side and never shown. See [[email-channel-elastic-email-account]].
- **The sender domain is the merchant's, not CloudCart's.** The domain must come from [[settings-domains]]. Sending from `*.cloudcart.com` is forbidden for campaigns — protects CloudCart's shared reputation. See [[email-channel-dns-records]].
- **Auto-suspend triggers.** Four thresholds run against each reputation pull: `SUSPENDED_SPAM = 0.5`, `SUSPENDED_BOUNCED = 5`, `SUSPENDED_OPEN = 5` (open-rate floor). Channel auto-suspends with the matching reason (`spam` / `bounced` / `open`). See [[email-channel-suspend-thresholds]] and [[marketing-channels#The four auto-suspend triggers]].
- **No merchant-self-service unsuspend.** After an auto-suspend, the merchant fixes their list / content and contacts support to clear `suspended_by` or set `manual_allowed_suspended` — see [[email-channel-suspend-thresholds]].
- **Step 4 completion also activates the channel.** Saving the sender mailbox flips `configured = true` AND `active = true` simultaneously — the Email channel is the only channel where wizard completion also turns it ON. See [[email-channel-setup-wizard]].
- **Test sends bypass Elastic Email.** Demo sends use the platform's transactional MailManager, don't count against the plan-cap, don't increment statistics, and don't appear in the campaign log — see [[email-channel-send-pipeline]].

## Related

- [[marketing-channels]] — parent hub (multi-channel framework + auto-suspend triggers).
- [[marketing-campaigns]] — campaigns use this channel as the most common delivery medium.
- [[marketing-omnichannel-mails-list]] — transactional email notifications use this same Email channel for delivery.
- [[apps-smtp]] — alternative integration for merchants who want to deliver via their own SMTP server instead of the CloudCart-managed Elastic Email pool.
- [[apps-mailchimp]] — sync subscribers to a Mailchimp list (different system; doesn't use this channel).
- [[settings-domains]] — sender domains must be defined here first.
- [[settings-hooks]] — `subscriber.*` events fire on email-driven subscribe/unsubscribe state changes.
- [[marketing-subscribers]] — subscribers with their per-channel `SubscriberChannel` rows, including the Email channel's `verified` / `bounced` / `unsubscribed` flags that gate sending.
- [[marketing-campaigns-policy]] — anti-spam policy.
- [[notification-delivery]] — outbound delivery concept page.
- [[channel]] — Channel entity reference.

## Open questions

No outstanding questions.
