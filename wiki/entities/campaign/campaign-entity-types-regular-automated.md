---
type: entity
nav_path: "Entity → Marketing Campaign → Types (Regular vs Automated)"
aliases: ["Campaign types", "Regular campaign", "Automated campaign", "Campaign type field", "Drip campaign type", "Trigger condition", "gets_in_segment", "Видове кампании", "Регулярна кампания", "Автоматизирана кампания"]
tags: [entity, marketing, campaigns, automation, triggers]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[campaign]]. See the hub for the other aspects (attributes schema, lifecycle, relationships, consent gating, attribution & statistics).

# Campaign — Types (Regular vs Automated)

## Identity

The `type` field on a Campaign is set at creation time via the **Create campaign** modal and is one of two literal string values: `regular` or `automated`. The shape decides scheduling semantics, recipient picking strategy, edit-time behaviour, and re-enrolment rules. **Both shapes share the same Campaign entity** — there's one record type, one set of action / channel / log / statistics relationships, one anti-spam policy gate — but the lifecycle expectations diverge.

- **Regular** — a one-shot blast. The merchant picks a Segment, composes per-channel messages, picks a send time (immediate OR scheduled future date / time), and the campaign fires once. Used for newsletters, promotional announcements, sale launches, seasonal greetings.
- **Automated** — a multi-step automation. The campaign is triggered by a customer event (entering a Segment, placing an order, being inactive N days, abandoning a cart) and fires a sequence of messages with conditional branches and per-step delays. Used for welcome series, post-purchase drip, win-back flows, re-engagement, birthday offers.

The `type` cannot be switched after creation — the merchant must copy or recreate to change shape.

## Aliases

- **Regular** = "newsletter blast", "one-shot campaign", "promotional campaign" (informal).
- **Automated** = "automation campaign", "drip campaign", "welcome series", "post-purchase flow", "win-back sequence".
- The Bulgarian admin UI uses **"Регулярна"** for regular and **"Автоматизирана"** for automated.

## Key Attributes

| Attribute | Regular | Automated |
|-----------|---------|-----------|
| **`type`** | `'regular'` | `'automated'` |
| **Recipient picking** | Snapshot at send time — every subscriber currently in the Segment receives one message. | Stream — every subscriber enters the flow as they hit the trigger event. |
| **`trigger_condition`** (verified) | Auto-set to `'gets_in_segment'` by a boot hook at create time. The UI does not expose this for Regular campaigns since they only have one possible trigger. | Set by the merchant via the editor — values include `'gets_in_segment'`, `'place_order'`, `'cart_abandoned'`, `'inactivity'`. |
| **Schedule** | Immediate OR scheduled for a future date / time. | No explicit send time — the trigger event drives entry; per-step delays drive timing within the flow. |
| **Number of actions per channel** | One — the merchant composes one Email body, one SMS body, one Viber body, one Web Push body. | Many — across steps and channels. Step 1: send Email; Step 2: wait 3 days; Step 3: send SMS if Email not opened. |
| **Auto-archive on completion** | Yes — hourly aggregation calls `markAsCompleted` when `successfully_sent >= subscribers_to_campaign_count > 0`, sets `progress = 'completed'` AND `archived_at = now`. The Regular campaign silently moves to the Archived tab. | No — by design Automated campaigns are "always-on" listeners. They never auto-archive. |
| **Re-enrolment** | N/A — a Regular campaign sends once per subscriber per (campaign, channel). | Allowed by default — subscribers re-enter on repeat triggers via separate pivot rows on `subscriber_to_campaigns`, each with its own `times_completed` counter. |

## Where it appears

- [[marketing-campaigns]] — the **Create campaign** modal picks the type; the campaign list filters by Active / Inactive / Draft / Archived but does not directly filter by type (the `type` field is visible in the row).
- [[campaign-entity-attributes-schema]] — for the full column-level reference of `type`, `trigger_condition`, and the related state columns.
- [[campaign-entity-lifecycle]] — for how `auto-archive on completion` differs between the two types.
- [[campaign-entity-consent-gating]] — the two-layer consent model is identical between Regular and Automated; only the trigger-time differs.

### How the two shapes are distinguished operationally

- **Regular** has a single "send time" (immediate or scheduled). Subscribers are picked from the Segment as a **snapshot** at send time. One delivery per recipient.
- **Automated** has a **trigger event** + a **multi-step flow**. The Segment defines the audience; the trigger defines WHEN within that audience the customer enters the flow. Each subscriber moves through the steps independently, gated by per-step delays and per-step conditions.

Both share the same actions / channels / logs / statistics structure — only the entry semantics differ. The per-step editor for Automated campaigns is part of [[marketing-campaigns]].

### Automated re-enrolment cycle (verified against backend)

An Automated campaign re-fires for the SAME subscriber each time the trigger event happens again — e.g., the merchant has an Automated "post-purchase thank-you" campaign; every time the customer places a new order, the trigger fires and they re-enter the flow.

The platform supports re-enrolment via separate pivot rows on `subscriber_to_campaigns` — each re-enrolment is a new pivot row with its own `times_completed` counter and `progress` state. So a subscriber who completes an Automated post-purchase campaign three times has three pivot rows, each marking one cycle through the flow. Whether the customer also gets the second send depends on per-campaign settings (some Automated flows are once-only per subscriber, others are recurring) — see Open Questions on [[campaign]] for unresolved edge cases.

## Related

- [[campaign]] — hub.
- [[campaign-entity-attributes-schema]] — full attribute / column reference including `trigger_condition` values.
- [[campaign-entity-lifecycle]] — auto-archive on completion (Regular only).
- [[campaign-entity-relationships]] — how subscribers attach to a campaign via the `subscriber_to_campaigns` pivot (the row backing re-enrolment).
- [[segment]] — the audience-definition entity that gates entry on both shapes.
- [[subscriber]] — the recipient entity that holds the per-channel consent flags.
- [[marketing-campaigns]] — the list / create / edit / statistics screens.

## Open Questions

- ⏸️ Whether an Automated campaign with `trigger_condition = 'gets_in_segment'` re-fires when the same subscriber re-enters the segment after exiting — or whether each subscriber can pass through the flow only once even with re-enrolment enabled. `(verify)`
- ⏸️ The exact behavior when a Regular campaign's Segment changes between save time and send time. `(verify)`
