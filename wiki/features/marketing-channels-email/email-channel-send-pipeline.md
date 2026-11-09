---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Send pipeline"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Email send pipeline", "Email pre-flight checks", "Email merge tags", "$verify_url", "$subscriber_email", "Saved templates", "Predefined templates", "Email test send", "Demo email", "message_html validation", "Local image paste rejected", "UTM injection email"]
tags: [marketing, channels, email, send, templates, merge-tags, utm, validation]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, DNS records, Elastic Email sub-account, webhook feedback, suspend thresholds, settings pane).

# Email channel — Send pipeline

## Purpose

Once the channel is configured ([[email-channel-setup-wizard]]) and verified ([[email-channel-dns-records]]), the **send pipeline** governs every outbound email. It runs per-recipient pre-flight checks, renders the HTML + subject + plain-text body, substitutes merge tags, injects UTM + tracking-attribution parameters into every link, queues one send job per recipient, and writes a log row that the [[email-channel-webhook-feedback|feedback webhook]] later updates with delivery status. This page covers: the pre-flight subscriber checks, merge-tag and UTM rules, the saved-vs-predefined templates, the message-template validation, and the demo / test send.

## Where to find it

- **Saved templates** live on a separate route — `campaigns-email-saved-templates` (`/admin/marketing/campaigns/configuration/channel/email/saved`).
- **Predefined templates** appear in the campaign editor's template picker alongside saved templates.
- **Demo / test send** is invoked from the campaign action editor (see [[marketing-campaigns-edit]]).
- **Pre-flight failures** show their reason in the campaign's statistics step log and the subscriber's own log, not in the channel **Log**.

## What the merchant can do here

- Manage **Saved templates** — merchant-curated reusable HTML email layouts. The thumbnail image is auto-generated from the rendered HTML.
- Use **Predefined templates** — CloudCart-curated catalog, scoped by language with fallback to `app.fallback_locale` when the current language has no rows. Categorised, ordered, and shown as a starting point. Read-only to the merchant.
- Insert merge tags from the editor's dropdown: universal tags plus the two Email-channel-exclusive tags `{$verify_url}` and `{$subscriber_email}`.
- Send a **demo / test send** from the action editor — it bypasses the channel send and Elastic Email (see Business rules).
- View **Logs** — per-recipient log rows with status, sent_at, delivered_at, seen_at + full content preview (iframe).

## Settings & fields

### Validation rules on the message template editor

| Field | Validation |
|---|---|
| `name` | `required\|max:191` |
| `subject` | `required\|max:191` |
| `message_html` | `required\|string` AND base64-embedded local images are rejected: *"Local image paste has been disabled. Local images have been removed from pasted content."* |

### Subscriber-side pre-flight checks (per recipient, at dispatch)

The platform checks the recipient's Email channel row, in this order:

| Check | Log reason (EN) | Log reason (BG) |
|---|---|---|
| missing address | *"Missing email address to send message"* | „Липсва имейл адрес до който да бъде изпратено съобщението“ |
| empty message | *"Empty message text"* | „Няма въведен текст за съобщение“ |
| unsubscribed | *"Unsubscribed"* | „Абонатът е прекратил своя абонамент“ |
| no marketing consent | *"Not accepts marketing"* | „Абонатът не приема маркетинг“ |
| bounced | *"SPAM"* (means bounced, not spam) | „Спам“ |
| unverified, `unconfirmed_send` OFF | *"The subscriber has not confirmed his email address"* | „Абонатът не е потвърдил имейл адреса си“ |

A failure writes **no** `NOT_SENT` row. It writes a campaign-log row with no delivery status and no channel, the reason as its message, and removes the subscriber from the campaign. The channel **Log** never shows it; the campaign's statistics step log does (reason in red under Destination), as does the subscriber's own log. Members excluded at launch leave no row at all — see [[campaigns-subscribers-enrolment]].

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

The Email channel adds two exclusive merge tags on top of the universal set:

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

A campaign step targeting Email queues one send job per recipient on the campaign queue. The job calls Elastic Email's EmailSend API with the rendered HTML, subject, sender email (`send_email` from [[email-channel-setup-wizard]]), sender name, and per-message metadata (campaign_id, subscriber_id, action_id, channel_identifier, segment info, message_hash). Elastic Email assigns a `messageid` which gets stored on the log row — used later by [[email-channel-webhook-feedback]] to match inbound events back to the log row. The row is written `NOT_SENT` when the job runs and turns `SENT` only once Elastic Email accepts the message; a rejected store key leaves it there with no reason — see [[email-channel-reconnect]].

The 80% usage notice is evaluated before each dispatch — see [[channels-usage-alerts]]. Plan cap key: `campaign.channel.email`.

### Variable substitution is done before queuing

The platform's variable-substitution helper resolves template variables (`{$customer_first_name}`, `{$shop_name}`, `{$subscriber_email}`, `{$verify_url}`, `{$dynamic_discount_code}`, etc.) per recipient before the job is queued. This means a substitution failure (e.g., a tag the merchant typed wrong) fails per-recipient with a log error, not as a campaign-wide error.

### `{$verify_url}` powers the double-opt-in subscriber link

`{$verify_url}` is used in the "Email confirmation for subscription in store:site_name" template that lets unverified subscribers prove their email. Clicking the link sets their `verified = 1` and shows them: *"You have successfully verified your email address."*

### Local image paste is rejected — bloat prevention

The `message_html` validator rejects any `data:image/{type};base64` content (error in the table above). Base64 images can be megabytes per email, so the merchant uploads images to the platform's image gallery first, keeping payloads small.

### Demo / test sends bypass Elastic Email entirely

`testCampaignAction` sends a one-off email via the platform's transactional MailManager (NOT the channel-send job and NOT Elastic Email's sub-account API). Useful because:

- Test sends do NOT count against the `campaign.channel.email` plan-cap.
- Test sends do NOT increment channel statistics.
- Test sends do NOT show up in the campaign log.
- Test sends use the platform's primary mailbox instead of the merchant's sender.

Returns a confirmation toast: *"Demo successfully sent to {to}"*. The trade-off: test sends do NOT exercise the merchant's verified sender domain — for that, the merchant must send a real campaign to a single test subscriber.

### Predefined templates use language fallback

A merchant whose admin language has no curated catalog sees the fallback-language predefined templates instead of an empty picker.

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-setup-wizard]] — sender email is what the send job uses as `from`.
- [[email-channel-webhook-feedback]] — the log row written by this pipeline is updated by inbound webhook events.
- [[email-channel-settings-pane]] — `unconfirmed_send` toggles the `verified` pre-flight check.
- [[email-channel-suspend-thresholds]] — channel must not be auto-suspended for the send pipeline to run.
- [[marketing-campaigns]] — campaign editor that drives this pipeline.
- [[marketing-campaigns-edit]] — Demo / test send invoked from the action editor.
- [[marketing-subscribers]] — pre-flight checks read per-subscriber Email channel flags.
- [[marketing-omnichannel-mails-list]] — order and system notifications never use this pipeline; they go through the platform's notification mailer.

## Open questions

None.
