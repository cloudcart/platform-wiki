---
type: feature
nav_path: "Marketing → Channels → Channels setup → Template vars & subscriber feedback"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel template variables", "Magic links in campaigns", "Unsubscribe url variable", "Cart url variable", "Auto-verified subscribers", "Subscriber removal on fail", "Triggered products limit"]
tags: [marketing, channels, template-variables, subscriber-feedback, unsubscribe]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, lifecycle, suspension, plan caps, sandbox, UI surfaces).

# Channels — template variables & subscriber feedback

## Purpose

The cross-channel template variables (magic links) every channel-rendered message supports, the per-send subscriber-feedback loop that reacts to provider-reported delivery statuses (HARD_BOUNCED suppressing the subscriber, CLICKED/SEEN retroactively verifying, ERROR/HARD_BOUNCED/UNSUBSCRIBED/ABUSE_REPORT removing the subscriber from the in-flight campaign), and the cross-channel quirks (triggered-products clamp at 12, HARD_BOUNCED categorisation rules). This is the layer that makes the merchant's list **self-cleaning** without explicit merchant intervention.

## Where to find it

These behaviours are surfaced indirectly:

- **Logs modal** ([[marketing-channels-logs]]) — the per-(subscriber, campaign action) status column is the artifact of this feedback loop.
- **Subscribers list** ([[marketing-subscribers]]) — `verified` / `bounced` / `unsubscribed` flags per `SubscriberChannel` row reflect the loop's writes.
- **Campaign editor** — the template variables are inserted via the email/SMS/Viber/WebPush message-body editor for each campaign action.

## What the merchant can do here

- Insert `{$unsubscribe_url}`, `{$cart_url}`, `{$checkout_url}`, `{$triggered_products:N}` placeholders into a campaign message body.
- Read the per-send status returned by the provider via the channel's Logs view.
- Filter subscribers by per-channel `bounced` / `unsubscribed` / `verified` state in the Subscribers segment builder.

## Settings & fields

### Universal template variables

Every channel-rendered message body (Email, SMS, Viber, Web Push) supports these placeholders:

| Variable | Resolves to | Notes |
|----------|-------------|-------|
| `{$unsubscribe_url}` | Per-subscriber one-time unsubscribe link | Encrypted ID is regenerated on every send (includes the current timestamp). Links can't be reused beyond the campaign send window. |
| `{$cart_url}` | Subscriber-attributed magic link to the cart | Auto-logs the subscriber in (no password) when clicked. Useful for abandoned-cart recovery. |
| `{$checkout_url}` | Subscriber-attributed magic link to checkout | Same auto-login semantics as `{$cart_url}`. |
| `{$triggered_products:N}` | First N products that triggered the campaign | `N` is capped at **12** per render — larger requested counts are silently clamped (verify). |

The platform does NOT auto-append `{$unsubscribe_url}` — the merchant is responsible for inserting it. Legal compliance (CAN-SPAM, GDPR) makes its inclusion effectively mandatory.

### Per-send status enum (cross-channel)

Every channel's per-(subscriber, action) delivery record carries a status. The cross-channel status values:

`SENT`, `DELIVERED`, `SEEN`, `CLICKED`, `UNDELIVERED`, `NOT_SENT`, `ERROR`, `BOUNCED`, `HARD_BOUNCED`, `UNSUBSCRIBED`, `ABUSE_REPORT`, `EXPIRED`, `REJECTED`, `UNDELIVERABLE`, `ACCEPTED`, `COMPLETED`, `PENDING`, `PURCHASE`.

Surfaced in the [[marketing-channels-logs|Logs]] panel's status filter.

## Business rules

### Auto-verification on engagement (Email)

When an Email log goes to `STATUS_CLICKED` or `STATUS_SEEN`, the subscriber's Email channel row gets `verified = 1` automatically. **Opening or clicking is treated as proof of address ownership**, retroactively verifying unverified subscribers without an explicit confirmation click.

This means a list imported with `verified = 0` will progressively self-verify as opens / clicks roll in, raising deliverability over time.

### HARD_BOUNCED vs BOUNCED categorisation (Email)

When the provider reports a send as `Error` with `category` in (`Suppressed`, `NoMailbox`, `Spam`, `NotDelivered`), the log row's status is **upgraded to HARD_BOUNCED**. Other Error categories stay as **BOUNCED** (soft bounce). Consequences:

| Status | Subscriber-side write | Suppression-list effect |
|--------|----------------------|-------------------------|
| BOUNCED | `bounced = 1` on the Email channel row | Soft — subscriber may recover. |
| HARD_BOUNCED | `bounced = 1` on the Email channel row | Triggers **permanent suppression** logic — subscriber will not receive future sends on this channel even if `bounced` is later reset (verify). |

Both flip `bounced = 1`, but only HARD_BOUNCED triggers the permanent suppression path. This is the mechanism that feeds the `bounced` auto-suspend trigger in [[marketing-channels-cross-suspension]].

### Subscriber removal on fail — cascading

When an Email send returns `STATUS_ERROR`, `STATUS_HARD_BOUNCED`, `STATUS_UNSUBSCRIBED`, or `STATUS_ABUSE_REPORT`, the platform calls the campaign-manager's removal hook with:

- `earlyExit = true` — subscriber is removed from the **in-flight campaign** (no further actions on this run).
- `rejectsMarketing = true` — subscriber is marked as **rejecting marketing across the store** (subscriber-level `marketing = 0`).

`ABUSE_REPORT` additionally fires the removal with `key = 'abuse'` (separate semantic from generic error) — this lets the merchant trace abuse-complaint origins separately from technical-failure removals.

The cascade is symmetric across the four trigger statuses — each represents either an explicit subscriber refusal (UNSUBSCRIBED, ABUSE_REPORT) or a delivery-blocking failure that justifies de-listing (ERROR, HARD_BOUNCED).

### Triggered-products payload limit

For campaigns that include `{$triggered_products:N}` variables, the platform caps `N` at **12 products** per render (Email-channel-specific override). Larger requested counts are silently clamped — the merchant who asks for `{$triggered_products:50}` gets only the first 12 (verify).

### Two-layer consent check at send time

Every send (regardless of channel) checks consent in two layers:

1. **Customer-level** `marketing` flag.
2. **Per-channel** `marketing` flag AND `verified = 1` AND `unsubscribed = 0` AND `bounced = 0`.

If either layer fails, the send is skipped. The subscriber-removal cascade above writes the per-channel layer's flags; the customer-level layer is written through subscriber-list management ([[marketing-subscribers]]).

This is the same gate used by both campaign sends AND the [[marketing-omnichannel-mails-list|transactional Email notifications]] — see [[notification-delivery]].

### Programmatic mirror (JSON-API v2)

The same per-channel feedback fields are exposed programmatically at [[api-subscribers-channels]]. A PATCH to a channel row triggers the same segment-membership re-evaluation, channel-identifier uniqueness validation, phone-number E.164 normalisation, and standard subscriber `updated` webhook. External integrations syncing `unsubscribed` / `bounced` from an external ESP write through this resource.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-suspension]] — HARD_BOUNCED counts feeding the `bounced` auto-suspend trigger.
- [[marketing-channels-logs]] — where the per-send status flow surfaces.
- [[marketing-subscribers]] — per-`SubscriberChannel` `verified` / `bounced` / `unsubscribed` flags.
- [[api-subscribers-channels]] — JSON-API v2 mirror of these fields.
- [[marketing-campaigns]] — where the template variables are inserted.
- [[marketing-omnichannel-mails-list]] — transactional notifications using the same consent layer.
- [[notification-delivery]] — concept page on the two-layer consent gate.
- [[json-api-v2]] — authentication and side-effects principle.

## Open questions

- Whether the 12-product `{$triggered_products}` clamp is Email-only or applies across channels (verify).
- Whether HARD_BOUNCED's permanent-suppression bypass survives a `bounced = 0` reset by the merchant (verify).
