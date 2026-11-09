---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Delivery webhook"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Email delivery webhook", "Elastic Email feedback loop", "AbuseReport handler", "Email bounce handler", "Email open/click webhook", "Email status mapping", "HARD_BOUNCED", "CampaignChannelsLog status"]
tags: [marketing, channels, email, webhook, elastic-email, deliverability, bounce, abuse, unsubscribe]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, DNS records, Elastic Email sub-account, send pipeline, suspend thresholds, settings pane).

# Email channel — Delivery webhook & feedback loop

## Purpose

After DNS verification ([[email-channel-dns-records]]) succeeds, CloudCart auto-registers a delivery-status webhook on the Elastic Email sub-account. Elastic Email then calls this webhook on every status event for the merchant's sends — delivered, opened, clicked, bounced, complained (AbuseReport), unsubscribed, errored. The webhook events update the per-(subscriber × campaign action) log row so the merchant's **Logs** panel shows accurate delivery status, and they drive subscriber-side side-effects (auto-verify on open / click, auto-unsubscribe on Unsubscribed events, abuse marking on AbuseReport).

## Where to find it

- The webhook URL itself is `https://{site}/messages/elastic-email-campaign/{site_id}` (HTTPS-only). The merchant does not configure it — it is registered automatically, and only when all four DNS checks pass.
- Inbound events surface in the per-campaign **Logs** panel of the Email channel card and on the campaign log itself.
- Subscriber-side side-effects appear on [[marketing-subscribers]] — `verified` / `unsubscribed` / `bounced` flags flip as events arrive.

## What the merchant can do here

- View per-message delivery history with full content preview (iframe) in the channel's **Logs** panel.
- See the status of each send: SENT, SEEN, CLICKED, UNSUBSCRIBED, ERROR → HARD_BOUNCED, BOUNCED, ABUSE_REPORT, PENDING.
- Nothing to refresh by hand — rows a webhook event never resolved are re-checked automatically every hour (see Business rules).

## Settings & fields

### Webhook registration

Triggered automatically after all four `Domain.Verify*` calls succeed (see [[email-channel-dns-records]]):

1. Load existing webhooks via `Account.LoadWebhook` and skip if a webhook with the same URL is already present.
2. Otherwise call `Account.AddWebhook(url, name="Hook", notify=false, sent=true, opened=true, clicked=true, unsubscribed=true, complaint=true, bounced=true)`.

All eight event categories enabled, signed-up notifications disabled.

### Status mapping — Elastic Email to CloudCart

The status mapping collapses Elastic Email's nomenclature into CloudCart's canonical set:

| Elastic Email event | CloudCart status |
|---------------|-----------|
| Sent | SENT |
| Opened | SEEN |
| Clicked | CLICKED |
| Unsubscribed | UNSUBSCRIBED |
| Error | ERROR (then to HARD_BOUNCED in the log writer) |
| AbuseReport | ABUSE_REPORT |
| WaitingToRetry | PENDING |
| (anything else) | NOT_SENT |

### Error-category mapping — when ERROR → HARD_BOUNCED vs BOUNCED

The webhook handler inspects Elastic Email's error category:

| Elastic error category | CloudCart status |
|---|---|
| `Suppressed` | HARD_BOUNCED |
| `NoMailbox` | HARD_BOUNCED |
| `Spam` | HARD_BOUNCED |
| `NotDelivered` | HARD_BOUNCED |
| (other Error categories) | BOUNCED |

## Business rules

### Inbound webhook events — per-event side effects

The webhook handler dispatches `CampaignEmailWebHookProcess` to the queue. Inbound `messageid` lookups find the existing `CampaignChannelsLog` row, then apply:

- **Sent / Opened / Clicked** → update the log row's status to SENT / SEEN / CLICKED. **Sent arriving when log already shows CLICKED or SEEN is discarded** — engagement is never downgraded by a late Sent event.
- **Unsubscribed** → marks the subscriber's Email channel `unsubscribed = 1`; the campaign-step listener fires `triggerRemove` to halt further sends for that subscriber in any in-flight campaign.
- **Error / hard-bounce** → marks status HARD_BOUNCED or BOUNCED on the log (per the category map above); the subscriber flags follow the rules below.
- **AbuseReport** → status ABUSE_REPORT; campaign listener cascades: marks subscriber Email channel `bounced = 1`, marks them as rejecting marketing, removes them from the campaign with `key = 'abuse'`. Also counts toward the `SUSPENDED_SPAM` threshold (see [[email-channel-suspend-thresholds]]).
- **WaitingToRetry** → status PENDING, retried by Elastic Email.

### Subscriber flags set by each status

- **ERROR, HARD_BOUNCED and ABUSE_REPORT** always set `bounced`; a soft **BOUNCED** never does.
- **UNSUBSCRIBED, ERROR, HARD_BOUNCED and ABUSE_REPORT** also set marketing off and `unsubscribed` — but only while the campaign is active.
- **SEEN and CLICKED** set `verified` (below).

### Events are ignored on an expired plan or in maintenance

Webhook events that arrive while the store's plan is expired or the store is in maintenance are ignored.

### Engagement retroactively verifies the subscriber

**Opened** or **Clicked** events set the subscriber's Email channel `verified = 1`. Engagement is treated as proof of address ownership, retroactively verifying unverified subscribers. This means a merchant who turned ON `unconfirmed_send` (see [[email-channel-settings-pane]]) and sent to a fresh list will see unverified subscribers flip to verified as they engage.

### Webhook pings without `messageid` are acknowledged but ignored

Webhook calls without a `messageid` parameter, or with `channel = testchannel` (Elastic Email's verification ping), return `Ok` without processing. This keeps the webhook endpoint stable when Elastic Email checks reachability.

### The webhook URL is signed only by HTTPS — no secret

The webhook endpoint relies on HTTPS alone. The `site_id` in the URL is the store's numeric id, not a random value, and there is no shared secret.

### Hourly status check for unresolved rows

There is no manual refresh. An automatic **hourly** background check looks up unresolved rows in Elastic Email by the stored `messageid`, covering webhook events that were lost. A failed lookup (e.g. a dead store key) sets the row to **Error** with *"Empty status message"* — that is not a real bounce.

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-dns-records]] — webhook is registered ONLY after all four DNS checks pass.
- [[email-channel-send-pipeline]] — the per-message send writes the log row that the webhook later updates.
- [[email-channel-suspend-thresholds]] — `AbuseReport` events drive `SUSPENDED_SPAM`; hard-bounce events drive `SUSPENDED_BOUNCED`.
- [[email-channel-settings-pane]] — engagement events flip `verified = 1` on subscribers, affecting subsequent `unconfirmed_send` behaviour.
- [[marketing-subscribers]] — per-subscriber Email channel flags (`verified`, `bounced`, `unsubscribed`) are flipped by these events.
- [[marketing-campaigns-policy]] — anti-spam policy backed by the AbuseReport handler.

## Open questions

None.
