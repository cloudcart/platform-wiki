---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage → Plan limit"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Channel plan limit", "plan_value resolution", "One-time + subscription allowance", "plan_feature_key per channel", "getPlanValue", "getAllowExecuteByPlan", "Unlimited channel cap", "Лимит на план", "Месечен лимит + еднократен"]
tags: [marketing, channels, usage, plan, limit, feature-key, plan-gate]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-channels-usage]]. See the hub for the other aspects (metric cards, counter model, engagement window, buy-credit flow, alerts).

# Channel usage — Plan limit resolution

## Purpose

The **Limit** card in the Usage modal shows a single number — but that number is the **sum of two plan-feature allowances** for the channel. This page documents how the limit is resolved, what the per-channel feature keys are, why the `_subscription` suffix matters, and what happens at send time when `Remaining` hits zero.

Understanding limit resolution is the difference between a merchant who buys a one-time feature pack and is confused about where the rest of their cap comes from, and one who knows the recurring portion comes from their plan tier. The send counter it is measured against is cumulative and never resets — see [[channels-usage-counter-model]].

## Where to find it

- The **Limit** value renders on the Usage modal: Sidebar → **Marketing** → **Channels** → **Channels setup** → on any channel card → click **Usage** → **Limit** card.
- The **Buy credit** button in the same modal navigates to `plan/feature/{plan_feature_key}` to top up — see [[channels-usage-buy-credit]].
- The plan-feature configuration itself is managed by CloudCart staff per plan tier — merchants top up via feature packs.

## What the merchant can do here

- **See the effective cap** for the channel as the **Limit** card value.
- **See `Unlimited`** when the plan grants uncapped usage for that channel.
- **Click Buy credit** to top up the one-time allowance — see [[channels-usage-buy-credit]] for the full flow.
- **Upgrade the plan** (via the plan settings flow, not from this modal) to raise the subscription portion of the cap.

## What the merchant cannot do here

- **Cannot edit the limit directly** — the value is plan-driven, not a merchant setting.
- **Cannot see the breakdown** between one-time vs subscription portion in the Usage modal — only the sum is rendered. The breakdown lives on [[plans]] / [[plan-feature]].
- **Cannot change which feature key a channel uses** — the mapping is fixed in the channel-manager code.
- **Cannot share a cap across channels** — every channel has its own `plan_feature_key` and its own bucket; sending an SMS NTH does not deplete the Email cap.

## Settings & fields

### Per-channel plan-feature keys

The `plan_feature_key` (the key passed to **Buy credit** and read for the cap) varies by channel:

| Channel | Plan-feature key |
|---------|-----------------|
| Email | `campaign.channel.email` |
| SMS MsgHub | `campaign.channel.sms_msghub_message` |
| SMS NTH | `campaign.channel.sms_nth_message` |
| Web Push | `campaign.channel.web_push` |
| Viber | `viber_messages` |

Each key has a `_subscription` variant (e.g., `campaign.channel.email_subscription`) used for the recurring monthly bucket. The merchant's effective Limit is the sum of the two buckets — see [[plan-gates]] for how plan feature values resolve.

### `getPlanValue` resolution table

| One-time allowance | Subscription allowance | Effective Limit |
|--------------------|------------------------|-----------------|
| Numeric `A` | Numeric `B` | `A + B` (displayed as the sum). |
| Numeric `A` | Non-numeric (null / boolean) | `A` only. |
| Non-numeric | Numeric `B` | `B` only. |
| Non-numeric | Non-numeric | `null` → modal renders `Unlimited` (localized). |

### API response fields

| Field | What it carries |
|-------|-----------------|
| `plan_limit` | The numeric sum (or null). |
| `plan_limit_formatted` | Either the formatted numeric, or the localized `Unlimited` string. |
| `plan_remaining` | `plan_value - total_sent_counter`. Can be negative. Returns the `Unlimited` string when plan is uncapped. |

## Business rules

### Limit is one-time + subscription, summed

The `Limit` shown is the platform code. The two flavours map to two plan-allowance buckets:

- The **`{plan_feature_key}`** value is the one-time / promotional allowance — accumulates from feature-pack purchases and survives plan renewals.
- The **`{plan_feature_key}_subscription`** value is the recurring monthly allowance baked into the plan tier. Depending on tier billing rules, this portion may reset monthly.

Both numeric → summed. One non-numeric → only the numeric is shown. Both non-numeric → `Unlimited`.

### `Unlimited` is the only non-numeric outcome

When the plan resolves the feature key as boolean `true` or null sentinel rather than a numeric, the modal displays the localized `Unlimited` string in the Limit card. This is the only non-numeric the merchant ever sees here — there is no "Pending", no "Trial", no "Disabled" rendering. If the channel is not available on the plan at all, the Usage button is hidden from the channel card.

### The send-time block at Remaining ≤ 0

Before a send is dispatched, the channel allows it only when the plan is unlimited or `plan_remaining > 0`; zero or negative Remaining blocks it. At the cap:

- **Email** — each campaign step is dropped with an admin alert: *"You have reached:feature limit. Your limit is:limit."* plus *"Purchase more credits"*. No log row is written; the channel stays on and the campaign keeps showing as running.
- **SMS, Viber, Web Push** — the channel is also switched OFF with an important alert (*"… Campaign channel:channel is deactivated."*); later steps drop silently. Buying credits does **not** switch it back on — the merchant must.

Nothing is written to the campaign log. *"You do not have enough credits for:name"* is a different, save-time error — see [[channels-usage-alerts]].

### Subscription allowance vs one-time — what resets

- **One-time bucket** (`{key}`) — accumulates from feature-pack purchases. Survives plan renewals. Top-ups via **Buy credit** drop here.
- **Subscription bucket** (`{key}_subscription`) — defined by the plan tier. May reset on the plan billing cycle (depends on plan rules; see [[plans]]).

If a merchant sees their Limit drop on the first of the month, the `_subscription` portion just reset — the one-time portion is still intact.

### Self-credentials does NOT raise the Limit

Even for Viber-with-self-credentials (where the cap is effectively bypassed by the counter-exclusion in [[channels-usage-counter-model]]), the Limit and Remaining cards still display the **plan-cap numbers** unchanged. The visual cap stays the same; only the send-time block no longer fires when `Remaining ≤ 0`.

### Different channels do not pool

Each channel has its own `plan_feature_key` and its own counter — exhausting the SMS NTH cap does **not** affect Email send-capacity. A campaign that uses two channels can fail on one and succeed on the other; the campaign-runner gates each per-channel send independently.

## Related

- [[marketing-channels-usage]] — hub.
- [[channels-usage-metrics]] — the Limit card on the Usage modal.
- [[channels-usage-counter-model]] — the cumulative counter that drives `plan_remaining`.
- [[channels-usage-buy-credit]] — top-up flow that grows the one-time bucket.
- [[plan-gates]] — concept page on plan feature gating; defines the `campaign.channel.*` and `viber_messages` keys.
- [[plans]] — plan tiers that define the per-channel subscription cap defaults.
- [[plan-feature]] — feature-pack purchase target the **Buy credit** button navigates to.
- [[marketing-campaigns]] — surfaces the save-time *"You do not have enough credits for:name"* error.

## Open questions

No outstanding questions.
