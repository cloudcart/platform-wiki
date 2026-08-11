---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → Send pipeline"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber send pipeline", "Viber dispatch", "Viber retry", "Viber omni/1/advanced", "Service vs promo routing", "bulkId Viber", "viber_message campaign action"]
tags: [marketing, channels, viber, infobip, send, retry]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (settings, self-credentials, DLR, system messages, plan cap, message format).

# Viber channel — Send pipeline

## Purpose

Documents what happens between the merchant clicking "Send campaign" and InfoBip receiving the Viber request. Covers the campaign-action contract, the queued job, the retry policy, the length-cap defence in depth, and the automatic service-vs-promo routing decision.

## Where to find it

The send pipeline is invisible to the merchant — it runs server-side after a campaign step (action type **"Viber message"**, mapping `viber_message`) fires. The merchant observes the **result** via [[viber-channel-dlr-status]] (logs) and the campaign stats screens.

## What the merchant can do here

Nothing directly — this aspect documents the under-the-hood pipeline so support can answer "why didn't my Viber send?" questions. Merchant-facing controls are on [[viber-channel-settings]] and [[marketing-channels-viber|the hub]].

## Settings & fields

### Channel manager constants

| Constant | Value | Effect |
|----------|-------|--------|
| Channel ID | `viber_message` | The channel mapping key. |
| Group | `phone` | Shares the Phone subscriber-channel group with SMS. See [[viber-channel-message-format]] for per-subscriber pre-flight rules. |
| UTM medium | `viber` | Applied to shortened URLs in the message body. |
| Plan-feature key | `viber_messages` | NOT the default `campaign.channel.viber_message` — see [[viber-channel-plan-cap]]. |
| `MAX_MESSAGE_LENGTH` | `1000` | Body length cap in characters; enforced twice in the pipeline. |
| Retry policy | `retry(5, ..., 2000)` `(verify)` | 5 attempts, 2-second backoff. |

### Campaign action return value

The Viber campaign action returns `-1` (special "job dispatched" marker) instead of a status string — same convention as NTH and Web Push. The actual delivery state lands later, when the queue worker runs and the DLR comes back.

## Business rules

### Job-queued dispatch with 5× retry, 2-second backoff

Viber sends are queued through `CampaignViberMessageSend` with `retry(5, ..., 2000)`. The campaign action enqueues the job and returns `-1`. The 5-second InfoBip API timeouts (see "InfoBip timeouts" below) mean transient InfoBip outages get re-tried up to 5 times before the log row is marked `NOT_SENT` with an error message.

### Length cap is checked TWICE

`MAX_MESSAGE_LENGTH = 1000` is enforced both:

1. **Inside the campaign-action thread** — after URL shortening (so the *post-shortening* rendered length is what matters, not the raw template). If over the cap, the action returns the bounced-error template immediately and no job is queued. The error template is the platform code with `:max = 1000`.
2. **Inside `sendMessage`** — second-line defence inside the queue worker (the platform code short-circuit).

The merchant-facing error message reads: *"The message exceeds the maximum length of:max characters"*.

### Service vs Promo: routing is automatic and per-message

The InfoBip client's `viber` method starts each send with `promo = false`. It flips to `promo = true` if the message includes either `imageURL` OR `buttonText`/`buttonURL`. Flipping `promo` causes the client to switch credentials:

| Default account | Promo account |
|----------------|---------------|
| `env('INFOBIP_USERNAME')` | `env('INFOBIP_USERNAME_PROMO')` |
| `env('INFOBIP_PASSWORD')` | `env('INFOBIP_PASSWORD_PROMO')` |
| `env('INFOBIP_KEY')` | `env('INFOBIP_KEY_PROMO')` |

**The flip only takes effect if the current `username == env('INFOBIP_USERNAME')`** (CloudCart's default account). For Self-credentials merchants the `setUsePromo` check forces `promo = false` — see [[viber-channel-self-credentials]].

If `isAllowPromoMessages` is FALSE for the merchant `(verify — special-client carve-out)`, they can't send the promo variant at all, even with images / buttons set in the editor.

### Per-message `bulkId` enables per-store reconciliation

Each send sets `bulkId = '{site_id}_{microtime(true)}'`. InfoBip stores this against the send and includes it in DLR callbacks. The platform can recover the originating `site_id` from `bulkId.split('_')[0]` if needed — useful when a DLR webhook arrives without the URL-level `site_id` param.

### InfoBip API timeouts are tight

the platform code and `put` use `TIMEOUT = 5`, `CONNECT_TIMEOUT = 5`, `READ_TIMEOUT = 5` — **all 5 seconds**. A slow InfoBip response throws an exception that's caught by the channel's send job and recorded as the error on the log row. The retry policy means transient slowness can still resolve, but a consistently slow InfoBip endpoint will fail every attempt.

### Per-subscriber pre-flight checks before sending

For each Viber send, the platform checks the recipient's Phone channel row (see [[viber-channel-message-format]] for the field-level rules and what a failure looks like in the logs).

## How it works

The campaign editor's **"Viber message"** action type validates subscriber state, renders the message body (placeholder substitution + URL shortening with `utm_medium=viber` attribution), checks the post-render length against the 1000-character cap, then dispatches the Viber send job. The job posts to `{host}/omni/1/advanced` with the JSON body documented in [[viber-channel-message-format]]. Service-vs-promo routing is decided automatically per message; per-message `bulkId` lets DLR results map back to the originating site even across InfoBip-side reconciliation.

The job retries up to 5 times with 2-second backoff before giving up and marking the log row `NOT_SENT` with the captured error.

### Legacy counter merge

The Viber channel overrides its `count` to add an `old_counter` setting value into the running total — used to seed historical send counts from before the modern logging system was introduced. Merchant-visible effect: the Usage modal's total includes the historical seed.

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-message-format]] — the omni/1/advanced JSON payload shape, image / button fields, 1000-char cap, per-subscriber pre-flight rules.
- [[viber-channel-dlr-status]] — what happens *after* the send: DLR webhook, status mapping, cascade-to-prior-pending.
- [[viber-channel-self-credentials]] — promo routing is force-disabled for Self-credentials merchants.
- [[viber-channel-plan-cap]] — `viber_messages` plan-feature key + cap accounting.
- [[viber-channel-settings]] — `different_sender` flag that selects the sender at client-construction time.
- [[marketing-channels-cross-lifecycle]] — cross-channel job dispatch / retry conventions.

## Open questions

- Confirm the retry count `(verify)` — the 5-attempt / 2-second backoff matches NTH and Web Push siblings but should be re-verified against current code.
- Does the post-shortening length include the UTM-attributed shortened URL exactly, or is there a buffer to allow for variation? `(verify)`
