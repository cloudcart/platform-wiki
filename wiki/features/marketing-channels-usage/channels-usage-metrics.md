---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage → Metric cards"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Usage metric cards", "Limit Remaining Total sent Clicks Opened", "Usage modal body", "Five usage metrics", "Card layout usage", "Метрични карти за потребление", "Лимит остатък изпратени"]
tags: [marketing, channels, usage, metrics, monitoring]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-usage]]. See the hub for the other aspects (counter model, plan limit resolution, engagement window, buy-credit flow, alerts).

# Channel usage — Metric cards

## Purpose

The body of the **Usage** modal renders **five** labelled metric cards in a responsive grid (3-column on medium screens, 2-column on small, 1-column on mobile). Each card answers one specific question the merchant has about their channel: *how big is my cap?*, *how much do I have left?*, *how much have I sent ever?*, *how many people clicked?*, *how many people opened?* This page documents what each card shows, where its number comes from, and how it is formatted.

The five-card grid is the only content of the modal body — there is no chart, no date picker, no per-day breakdown, no drill-down. It is a snapshot. The grid loads behind a spinner while the usage API call is in flight, then renders the cards in one paint.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → on any channel card → click **Usage** (pie-chart icon). The five metric cards appear in the modal body once the API call returns.

## What the merchant can do here

- **See the plan cap** for this channel in the **Limit** card.
- **See how many sends are left** before hitting the cap in the **Remaining** card.
- **See the cumulative all-time send count** in the **Total sent** card.
- **See click counts** for messages on this channel over the last 30 days in the **Clicks** card.
- **See open counts** for messages on this channel over the last 30 days in the **Opened** card.

## What the merchant cannot do here

- **Cannot change the date range** for Clicks / Opened — the engagement window is fixed server-side at 30 days, see [[channels-usage-engagement-window]].
- **Cannot reset the Total sent counter** — it never rolls over, see [[channels-usage-counter-model]].
- **Cannot drill into individual sends** from a card — for per-message detail use the **Logs** action on the same channel card (see [[marketing-channels-logs]]).
- **Cannot filter by campaign** — the cards aggregate across all campaign + system-message traffic for the channel.

## Settings & fields

| Card label | Backend field | What it shows | Numeric formatting |
|-----------|---------------|---------------|---------------------|
| **Limit** | `plan_limit_formatted` | The merchant's plan cap for this channel: one-time allowance + subscription allowance summed. If both are non-numeric, displays the localized `Unlimited` string. | Numeric formatted with thousands separators, or the literal `Unlimited` label. |
| **Remaining** | `plan_remaining` | `plan_limit - total_sent`. Can render negative values when the cap was overrun (see [[channels-usage-counter-model]]). Renders `Unlimited` for uncapped plans. | Numeric or `Unlimited`. |
| **Total sent** | `usage_count` | Cumulative all-time send count from the per-channel counter document. Never resets. | Numeric formatted with thousands separators. |
| **Clicks** | `opened_url` | Count of click events on this channel's campaign messages in the last 30 days. | Numeric, defaults to 0. |
| **Opened** | `seen_message` | Count of open events on this channel's campaign messages in the last 30 days. | Numeric, defaults to 0. |

### Card rendering rules

- Each card uses a labelled card wrapper with a large value (`text-xl`).
- Numeric values are formatted with thousands separators via the client-side `numberFormat` helper.
- If a value is `NaN` (the API returned a non-numeric string like `Unlimited`), the **unformatted string** is rendered as-is — no parsing fallback.
- The Limit and Remaining cards use the `_formatted` API field where present; the others use the raw integer.

## Business rules

### Limit and Remaining can both show `Unlimited`

For plans where the per-channel feature value resolves to a non-numeric (boolean true or null sentinel), both Limit and Remaining display the localized `Unlimited` string. The merchant on such a plan never hits a hard cap — see [[channels-usage-plan-limit]] for how the platform decides numeric vs unlimited.

### Total sent will exceed Limit over time

Because Total sent is cumulative (never resets) but Limit is the current cap, on long-running stores Total sent routinely exceeds Limit by an order of magnitude. This is expected — the gating field is **Remaining**, not the ratio of Total sent vs Limit. See [[channels-usage-counter-model]] for why there is no monthly rollover.

### Remaining can render as a negative number

If a campaign races past the cap before the platform's pre-flight check catches it (concurrent send jobs, self-credentials interplay), `total_sent` can exceed `plan_value` and `Remaining` becomes negative. The modal renders the raw integer — no clamp to zero. Treat any negative Remaining as *"overdrawn — buy credits or upgrade"*.

### Clicks and Opened are campaign-only

The two engagement counters exclude transactional / system-message traffic — they are filtered to events where `campaign_id != null`. So a store with active order-confirmation emails but no marketing campaigns will see Total sent rising but Clicks / Opened at 0. See [[channels-usage-engagement-window]] for the full filter.

### Card grid breakpoints

The grid uses `md:grid-cols-3` (3 columns on medium and up), falling back to 2 columns on small screens and 1 column on mobile. The card order is fixed and not configurable: Limit, Remaining, Total sent, Clicks, Opened.

### No drill-down from a card

Clicking any of the five cards has no effect — they are display-only. To investigate further, the merchant must close the modal and use the channel card's **Logs** action.

## Related

- [[marketing-channels-usage]] — hub for the Usage modal cluster.
- [[channels-usage-counter-model]] — what drives Total sent and the per-channel counter mechanics.
- [[channels-usage-plan-limit]] — how Limit is resolved (one-time + subscription).
- [[channels-usage-engagement-window]] — why Clicks and Opened use a fixed 30-day window.
- [[channels-usage-buy-credit]] — the **Buy credit** CTA in the modal footer.
- [[marketing-channels-logs]] — per-recipient drill-down available on the same channel card.
- [[marketing-channels]] — channel-setup hub.

## Open questions

No outstanding questions.
