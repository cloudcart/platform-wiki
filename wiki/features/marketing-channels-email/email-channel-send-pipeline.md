---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Send pipeline"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Email send pipeline", "Email pre-flight checks", "Email merge tags", "$verify_url", "$subscriber_email", "Saved templates", "Predefined templates", "Email test send", "Demo email", "message_html validation", "Local image paste rejected", "UTM injection email"]
tags: [marketing, channels, email, send, templates, merge-tags, utm, validation]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, DNS records, Elastic Email sub-account, webhook feedback, suspend thresholds, settings pane).

# Email channel — Send pipeline

## Purpose

Once the channel is configured ([[email-channel-setup-wizard]]) and verified ([[email-channel-dns-records]]), the **send pipeline** governs every outbound email. It runs per-recipient pre-flight checks, renders the HTML + subject + plain-text body, substitutes merge tags, injects UTM + tracking-attribution parameters into every link, queues one send job per recipient, and writes a log row that the [[email-channel-webhook-feedback|feedback webhook]] later updates with delivery status. This page covers: the pre-flight subscriber checks, merge-tag and UTM rules, the saved-vs-predefined templates, the message-template validation, and the demo / test send.

## Where to find it

- **Saved templates** live on a separate route — `campaigns-email-saved-templates` (`/admin/marketing-new/campaigns/configuration/channel/email/saved`).
- **Predefined templates** appear in the campaign editor's template picker alongside saved templates.
- **Demo / test send** is invoked from the campaign action editor (see [[marketing-campaigns-edit]]).
- **Pre-flight failures** appear as log rows on the campaign log with explicit error messages.

## What the merchant can do here

- Manage **Saved templates** — merchant-curated reusable HTML email layouts. The thumbnail image is auto-generated from the rendered HTML.
- Use **Predefined templates** — CloudCart-curated catalog, scoped by language with fallback to `app.fallback_locale` when the current language has no rows. Categorised, ordered, and shown as a starting point. Read-only to the merchant.
- Insert merge tags from the editor's dropdown: universal tags plus the two Email-channel-exclusive tags `{$verify_url}` and `{$subscriber_email}`.
- Send a **demo / test send** from the action editor — goes via the platform's transactional MailManager, NOT through the channel-send job and NOT through Elastic Email's sub-account API.
- View **Logs** — per-recipient log rows with status, sent_at, delivered_at, seen_at + full content preview (iframe).

## Settings & fields

### Validation rules on the message template editor

| Field | Validation |
|---|---|
| `name` | `required\|max:191` |
| `subject` | `required\|max:191` |
| `message_html` | `required\|string` AND base64-embedded local images are rejected: *"Local image paste has been disabled. Local images have been removed from pasted content."* |

### Subscriber-side pre-flight checks (per recipient, before queuing the send)

For each email send, the platform checks the recipient's Email channel row:

| Check | Required value | Error message on failure |
|---|---|---|
| `channel_identifier` | non-empty (subscriber has an email address) | (channel missing) |
| `unsubscribed` | 0 | *"You haven't consented to marketing"* (or analogous) |
| `marketing` | 1 | *"You haven't consented to marketing"* |
| `bounced` | 0 | (bounced — skipped) |
| `verified` | 1 (UNLESS `unconfirmed_send` is ON) | *"No message will be sent to this email because it has not been verified."* |

Any failure short-circuits the send and writes a log row with the matching error message. The campaign's reached-count is **not** incremented for these subscribers.

### UTM + tracking-attribution params injected on every link

Every link in the rendered email gets these parameters appended:

| Parameter | Value |
|---|---|
| `cc_campaign[...]` | Campaign attribution payload |
| `cc_subscriber[...]` | Subscriber attribution payload |
| `utm_source` | `cloudcart` |
| `utm_medium` | `email` |
| `utm_campaign` | `{campaign.title}` |

URL shortening is also done at this step.

### Email-channel-exclusive merge tags

`getMessageTags` injects two Email-channel-exclusive merge tags on top of the universal set:

| Tag | Resolves to |
|---|---|
| `{$verify_url}` | `/subscribers/verify/{encrypted_subscriber_id}` — the one-time verification link |
| `{$subscriber_email}` | The subscriber's email address |

Other channels (SMS, Viber, Web Push) do NOT surface these in their merge-tag dropdown.

### Saved vs predefined templates

| Type | Storage | Scope | Editable? |
|---|---|---|---|
| **Saved templates** | Merchant's saved-templates table | Per-merchant | Yes (merchant-curated) |
| **Predefined templates** | CloudCart catalog (`CampaignEmailDefaultTemplate`) | Scoped by language; fallback to `app.fallback_locale` | No (read-only to the merchant) |

Each predefined template thumbnail is rendered at 300×300. Saved-template thumbnails are auto-generated from the rendered HTML.

## Business rules

### Per-message dispatch and queuing

A campaign step targeting Email queues one send job per recipient on the campaign queue. The job calls Elastic Email's EmailSend API with the rendered HTML, subject, sender email (`send_email` from [[email-channel-setup-wizard]]), sender name, and per-message metadata (campaign_id, subscriber_id, action_id, channel_identifier, segment info, message_hash). Elastic Email assigns a `messageid` which gets stored on the log row — used later by [[email-channel-webhook-feedback]] to match inbound events back to the log row.

The platform also pre-emits the 80%-plan-cap notification if applicable, before the per-message send fan-out begins. Plan cap key: `campaign.channel.email`.

### Variable substitution is done before queuing

The platform's variable-substitution helper resolves template variables (`{$customer_first_name}`, `{$shop_name}`, `{$subscriber_email}`, `{$verify_url}`, `{$dynamic_discount_code}`, etc.) per recipient before the job is queued. This means a substitution failure (e.g., a tag the merchant typed wrong) fails per-recipient with a log error, not as a campaign-wide error.

### `{$verify_url}` powers the double-opt-in subscriber link

`{$verify_url}` resolves to `/subscribers/verify/{encrypted_subscriber_id}` — used in the "Email confirmation for subscription in store:site_name" template that lets unverified subscribers prove their email. Clicking the link sets their `verified = 1` and shows them: *"You have successfully verified your email address."*

This is the standard double-opt-in flow merchants can plug into onboarding campaigns.

### Local image paste is rejected — bloat prevention

The `message_html` validator rejects any value containing a `data:image/{type};base64` substring with the error: *"Local image paste has been disabled. Local images have been removed from pasted content."* This prevents bloated payloads (base64 images can be megabytes per email) and forces the merchant to upload images via the platform's image gallery first — keeping email payloads small and improving deliverability.

### Demo / test sends bypass Elastic Email entirely

`testCampaignAction` sends a one-off email via the platform's transactional MailManager (NOT the channel-send job and NOT Elastic Email's sub-account API). Useful because:

- Test sends do NOT count against the `campaign.channel.email` plan-cap.
- Test sends do NOT increment channel statistics.
- Test sends do NOT show up in the campaign log.
- Test sends use the platform's primary mailbox instead of the merchant's sender.

Returns a confirmation toast: *"Demo successfully sent to {to}"*. The trade-off: test sends do NOT exercise the merchant's verified sender domain — for that, the merchant must send a real campaign to a single test subscriber.

### Predefined templates use language fallback

Predefined templates are scoped by language with fallback to `app.fallback_locale` when the current language has no rows. So a merchant whose admin is set to a language with no curated catalog still sees the fallback-language predefined templates instead of an empty picker.

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-setup-wizard]] — sender email is what the send job uses as `from`.
- [[email-channel-webhook-feedback]] — the log row written by this pipeline is updated by inbound webhook events.
- [[email-channel-settings-pane]] — `unconfirmed_send` toggles the `verified` pre-flight check.
- [[email-channel-suspend-thresholds]] — channel must not be auto-suspended for the send pipeline to run.
- [[marketing-campaigns]] — campaign editor that drives this pipeline.
- [[marketing-campaigns-edit]] — Demo / test send invoked from the action editor.
- [[marketing-subscribers]] — pre-flight checks read per-subscriber Email channel flags.
- [[marketing-omnichannel-mails-list]] — transactional emails go through this same pipeline when pointed at the Email channel.

## Open questions

None.
