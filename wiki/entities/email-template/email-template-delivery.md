---
type: entity
aliases: ["Email template delivery", "Elastic Email sending", "Email channel mechanics", "Webhook feedback", "Bounce suppression", "Sub-account credentials", "Доставка на имейл шаблон"]
tags: [marketing, email, templates, delivery, elastic-email, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[email-template]]. See the hub for the other aspects (transactional family, campaign authoring, merge variables).

# Email Template — channel delivery

## Identity

When an Email Template (transactional or campaign) is sent for real, it leaves through the configured **Email channel** — typically **Elastic Email** for both families (see [[marketing-channels-email]]). This page documents the channel-side mechanics that decide whether a send succeeds, how delivery feedback flows back into per-template / per-campaign stats, and how bad addresses get suppressed.

(The Test/Demo send path is different — it uses the platform's transactional sender, not the merchant's Elastic Email sub-account. See [[email-template-campaign-authoring]].)

## Aliases

- **Email channel mechanics** — the delivery-side behaviour of the Email channel.
- **Webhook feedback** — Elastic Email's event callbacks that update template/campaign stats.
- **Bounce suppression** — the address-level blocking applied after hard bounces.
- **Доставка на имейл шаблон** — Bulgarian phrasing.

## Key Attributes

| Mechanic | What happens |
|----------|--------------|
| **Sub-account credentials are NOT merchant-supplied** | The platform provisions a per-store sub-account on CloudCart's master Elastic Email account; merchants don't see the API key. The account email follows the convention `{primary_host}@cloudcart.net` and the password is a 32-char random string. Credentials are persisted both in channel settings AND in `application_history` for recovery. |
| **Webhook auto-installed after domain verification** | After domain verification, the platform calls Elastic Email's `Account.AddWebhook`, enabling all 8 event types (sent, opened, clicked, unsubscribed, complaint, bounced, AbuseReport, error) — so subsequent template sends feed back into the per-template / per-campaign stats automatically. |
| **Tracking CNAME auto-creation requires an active Cloudflare zone** | Only when the host's `cloudflare_zone_id` is set AND the zone status is "active" does the platform auto-create the `tracking.{domain}` → `api.elasticemail.com` CNAME via the Cloudflare API. For self-managed DNS, the merchant adds it manually. |
| **Reset preserves two settings** | The Reset configuration option preserves the merchant's preferences for unverified-recipient sending and any support-granted override (`unconfirmed_send` and `manual_allowed_suspended`), even when wiping the rest of the channel's settings. |

### Delivery feedback cascades

| Event | Effect |
|-------|--------|
| **AbuseReport (spam complaint)** | When a recipient hits "Mark as spam", the inbound webhook event drives the platform code — the subscriber is removed from the in-flight campaign AND flagged as rejecting marketing. Other transactional templates to the same address still go through unless the master `customer_email_notifications` toggle is off (see [[email-template-transactional]]). |
| **Hard-bounce categorisation** | When Elastic Email reports `status = Error` with category in (`Suppressed`, `NoMailbox`, `Spam`, `NotDelivered`), the log row is upgraded to HARD_BOUNCED and the subscriber's Email channel gets `bounced = 1` — **permanently suppressed** for future Email sends to that address. |
| **Engagement implicitly verifies the address** | An Email log going to `STATUS_CLICKED` or `STATUS_SEEN` triggers the platform code retroactively — interpreted as proof of address ownership. |

These cascades are why a [[subscriber]]'s deliverability state changes without explicit merchant action: opens/clicks promote an address to verified; spam complaints and hard bounces demote or suppress it.

## Where it appears

- [[marketing-channels-email]] — the Email channel setup screen where domain verification, credentials, and reset live.
- [[marketing-campaigns]] — per-campaign send stats fed by the webhook events.
- [[marketing-omnichannel-mails-list]] — transactional sends that travel the same channel.

## Related

- [[email-template]] — hub.
- [[marketing-channels-email]] — Elastic Email integration that actually delivers the rendered template.
- [[notification-delivery]] — the platform-wide notification pipeline that routes templates through the configured email channel.
- [[email-template-transactional]] — the master toggle that overrides per-address state for transactional mail.
- [[email-template-campaign-authoring]] — the Test/Demo send path that bypasses this channel.
- [[subscriber]] — the identity whose `verified` / `bounced` channel state these cascades mutate.

## Open Questions

None.
