---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage → Buy credit"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Buy credit", "Buy more credits", "Top up channel", "Feature pack purchase channel", "Plan feature modal channel", "Покупка на кредити", "Купи кредит за канал"]
tags: [marketing, channels, usage, plan-feature, purchase, top-up]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-usage]]. See the hub for the other aspects (metric cards, counter model, plan limit, engagement window, alerts).

# Channel usage — Buy credit flow

## Purpose

The **Usage** modal's footer Save button is **repurposed** — instead of saving anything, it is labelled **Buy credit** and opens the feature-pack purchase flow for the current channel. This page documents what the button does, where the merchant lands, and what changes back on the channel card after a successful top-up.

This is the merchant's primary path from "I see a banned channel / negative Remaining" to "the channel is working again". The Usage modal is therefore not only a meter — it is also the entry point to recovery.

## Where to find it

- The **Buy credit** button is the right-hand button in the modal footer of the Usage modal — Sidebar → **Marketing** → **Channels** → **Channels setup** → on any channel card → click **Usage** → look at the bottom-right.
- The left-hand button is **Close**.
- After clicking **Buy credit**, the merchant is taken to `plan/feature/{plan_feature_key}` for the channel's feature key.

## What the merchant can do here

- **Click Buy credit** to start a feature-pack purchase for the channel.
- **Land on the plan-feature purchase screen** for the matching `plan_feature_key`.
- **Complete the top-up** there (pricing tier selection, payment method, confirmation) — that flow is owned by [[plan-feature]].
- **Return to the channel card** afterwards to see the updated **Limit** and **Remaining** numbers immediately.

## What the merchant cannot do here

- **Cannot purchase from inside the Usage modal directly** — the button only navigates / opens the upstream PlanFeature modal. The actual checkout happens there.
- **Cannot top up multiple channels at once** — each channel has its own `plan_feature_key`; the merchant must run the flow per channel.
- **Cannot top up the subscription portion** of the cap — only the one-time bucket (see [[channels-usage-plan-limit]] for the one-time vs subscription split). To raise the subscription portion, the merchant must upgrade the plan tier.
- **Cannot cancel a credit purchase** from this modal — refunds go through CloudCart support.

## Settings & fields

### Button behaviour

| Element | Value |
|---------|-------|
| Button label | *"Buy credit"* (localized). |
| Modal-footer position | Right-hand (where a normal Save button would sit). |
| Click effect | Emits a `feature` event to the parent page with `{ mapping: channel.plan.feature_key, key: channel.mapping }`. |
| Resulting flow | Parent page (`MarketingChannelsMainPage`) opens the global PlanFeature purchase modal scoped to that feature key. |
| Navigation target | `plan/feature/{plan_feature_key}` in the admin panel. |

### Per-channel `plan_feature_key` (passed in the event)

| Channel | `plan_feature_key` value |
|---------|--------------------------|
| Email | `campaign.channel.email` |
| SMS MsgHub | `campaign.channel.sms_msghub_message` |
| SMS NTH | `campaign.channel.sms_nth_message` |
| Web Push | `campaign.channel.web_push` |
| Viber | `viber_messages` |

These same keys appear in [[channels-usage-plan-limit]] — Buy credit raises the **one-time bucket** for whichever key the channel maps to.

## Business rules

### Buy credit emits a `feature` event, does not save

The Save button slot in the modal footer is repurposed in the channel-usage context. Clicking **Buy credit** does **not** save settings (the modal has no settings to save) — it emits a `feature` event on the modal component. The parent page listens for this event and opens its global PlanFeature purchase modal with the passed `{ mapping, key }` payload.

### Top-up grows the one-time allowance

A successful feature-pack purchase raises the merchant's `{plan_feature_key}` value — the **one-time bucket**. The subscription bucket (`{plan_feature_key}_subscription`) is untouched. See [[channels-usage-plan-limit]] for how the two buckets sum into the displayed Limit.

This means a top-up survives plan renewals — the credits stay in the one-time bucket until consumed. Conversely, a top-up does NOT reset on a new billing month — it accumulates.

### Limit and Remaining update on return

After the PlanFeature modal closes successfully, the parent page re-loads the channel's `plan` + `usage` data via the lazy `loadChannelDetail(channel.mapping)` call. The next time the merchant opens the Usage modal — or refreshes the channel card — the **Limit** and **Remaining** cards reflect the new cap.

### Recovering a feature-limit-banned channel

When Remaining drops to 0 or below and the channel was banned with a feature-limit-reached reason (see [[marketing-channels]] for the per-channel banned-reason mechanic), a successful Buy credit purchase clears that ban on the next page refresh. The channel card's status badge flips back to active and campaigns can run again.

### Self-credentials Viber does NOT need Buy credit

For Viber with self-credentials enabled, the channel never enters the feature-limit-reached banned state regardless of the Remaining value — sends are unmetered from CloudCart's perspective (see [[channels-usage-counter-model]] for the counter exclusion). The Buy credit button is still rendered, but clicking it is unnecessary for keeping the channel working.

### Per-channel button — no cross-channel top-up

The button always emits the **current channel's** `plan_feature_key`. There is no way to top up multiple channels at once from this modal — the merchant must close, open the next channel's Usage modal, and click Buy credit again per channel.

### Currency, pricing, and confirmation live in PlanFeature

Feature-pack pricing tiers, payment method selection, VAT handling, and purchase confirmation are all handled by the upstream PlanFeature purchase modal — not the Usage modal. The Usage modal hands off entirely. See [[plan-feature]] for the purchase-side surface.

## Related

- [[marketing-channels-usage]] — hub.
- [[channels-usage-plan-limit]] — how the one-time bucket sums with the subscription bucket into the displayed Limit.
- [[channels-usage-metrics]] — the Limit and Remaining cards that update after a top-up.
- [[channels-usage-counter-model]] — the counter side; what gets consumed by sends.
- [[plan-feature]] — feature-pack purchase target.
- [[plan-gates]] — defines the `campaign.channel.*` and `viber_messages` keys.
- [[plans]] — plan tiers (for upgrading the subscription portion of the cap).
- [[marketing-channels]] — channel-setup hub where the banned-reason mechanic is documented.

## Open questions

No outstanding questions.
