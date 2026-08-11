---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → Plan cap"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber plan cap", "viber_messages", "Viber usage", "Viber quota", "Buy more Viber credits", "Viber pricing", "viber_messages_subscription"]
tags: [marketing, channels, viber, plan-cap, billing]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (settings, self-credentials, send pipeline, DLR, system messages, message format).

# Viber channel — Plan cap & usage

## Purpose

Documents how CloudCart meters the merchant's Viber send volume against their plan. Viber is the only channel besides Web Push with a **dedicated plan-feature key** — it does NOT use the generic `campaign.channel.{mapping}` key pattern. Hitting the cap pauses campaigns using Viber and surfaces a `feature_limit_reached` banner on the channel card.

## Where to find it

The cap value, current usage, and the "Buy more credits" deep-link surface on the **Usage** modal of the Viber card and on the channel card itself when usage approaches the limit. See [[marketing-channels-usage]] for the cross-channel Usage modal layout.

## What the merchant can do here

- View sent-count vs the `viber_messages` plan cap.
- Click "Buy more credits" when approaching the limit (deep-link to plan upgrades / add-on credits).
- Bypass the cap entirely by switching to Self-credentials — see [[viber-channel-self-credentials]].

## Settings & fields

### Plan-feature key

| Key | What it controls |
|-----|------------------|
| `viber_messages` | Per-month Viber message bucket (the cap). Unlike Email / SMS / WebPush — which use `campaign.channel.{mapping}` — Viber's plan-feature key is hard-coded to a dedicated string. |
| `viber_messages_subscription` `(verify)` | Active Viber-credits subscription on the merchant's plan. Required for `different_sender` to actually use a non-default sender — see [[viber-channel-settings]]. |

Plan-cap accounting, "Buy more credits" deep-link, and the 80%-threshold notification all reference `viber_messages`. See [[plan-gates]] for the cross-cutting plan-feature-key reference.

### Self-credentials override

When [[viber-channel-self-credentials|Self-credentials]] is active, the channel's remaining-quota display returns `'global.unlimited'` instead of a number — InfoBip bills the merchant directly, so CloudCart doesn't meter the sends.

### Internal pricing units (platform-level config)

| Setting | Value | Notes |
|---------|-------|-------|
| `prices.mobile` | `10` | Internal pricing unit for mobile / SMS sends (likely cents). `(verify)` |
| `prices.viber` | `50` | Internal pricing unit for Viber sends. `(verify)` |

These are CloudCart's cost-side units — the merchant doesn't see them directly. They drive plan-design decisions: Viber is internally 5× more expensive than mobile, which is why Viber gets its own plan-feature key.

## Business rules

### Cap-reached pauses campaign sends

When the `viber_messages` cap is reached, the channel auto-banner shows `feature_limit_reached` and any campaign step that would dispatch a Viber send is paused. The merchant clicks the banner / **Buy more credits** to unlock.

### Service vs Promotional billing

InfoBip distinguishes **service messages** (transactional, e.g., order shipped notification) from **promotional messages** (marketing offers). Promotional messages are typically priced higher and have stricter sending-window rules in some markets. The platform routes between them automatically based on message content (see [[viber-channel-send-pipeline]] for the runtime decision).

The merchant's plan-cap accounting against `viber_messages` doesn't currently split service vs promo — both count against the same bucket. `(verify — confirm whether promo sends are weighted higher in the bucket)`.

### 80%-threshold notification

When usage crosses 80% of the `viber_messages` cap, the platform emits a notification (cross-channel pattern — see [[marketing-channels-cross-plan-caps]]). Gives the merchant time to upgrade before sends start failing.

### Self-credentials bypasses everything

Self-credentials merchants:

- Don't count against `viber_messages`.
- Don't get the 80%-threshold notification.
- Don't see `feature_limit_reached` banners.
- See `'global.unlimited'` in the Usage modal.

But they're also responsible for their own InfoBip billing — see [[viber-channel-self-credentials]].

### Customer-side requirements (no CloudCart-side billing impact)

The recipient must have Viber installed, internet connectivity, and the sender not blocked. Failures land as `UNDELIVERED` / `EXPIRED` — these still count against the `viber_messages` cap because InfoBip charged for the delivery attempt `(verify)`. See [[viber-channel-message-format]] for the customer-side requirements and [[viber-channel-dlr-status]] for the resulting status codes.

## How it works

The channel's `getRemainingValue` checks the `viber_messages` cap against the running send count, returning `'global.unlimited'` for Self-credentials accounts. The 80% threshold and `feature_limit_reached` banner are driven from the same query on the Usage modal.

The legacy counter merge (see [[viber-channel-send-pipeline]]) means historical send counts seeded before the modern logging system still count against the cap.

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-self-credentials]] — the path to bypass the plan cap entirely.
- [[viber-channel-send-pipeline]] — service-vs-promo routing decision.
- [[viber-channel-settings]] — `different_sender` requires `viber_messages_subscription`.
- [[plan-gates]] — cross-cutting plan-feature-key reference; lists `viber_messages` + `viber_messages_subscription`.
- [[marketing-channels-cross-plan-caps]] — cross-channel plan-cap reference.
- [[marketing-channels-usage]] — Usage modal that surfaces the cap value.

## Open questions

- Are promo Viber sends weighted heavier in the `viber_messages` bucket, or do they count 1:1 against the cap? `(verify)`
- Do `UNDELIVERED` / `EXPIRED` Viber sends count against the cap (InfoBip charged for the attempt) or only `SENT` / `SEEN`? `(verify)`
