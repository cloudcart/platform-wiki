---
type: feature
nav_path: "Marketing → Channels → Channels setup → Reputation → Auto-suspend"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Reputation auto-suspend", "Email channel suspended by reputation", "SUSPENDED_SPAM SUSPENDED_BOUNCED SUSPENDED_OPEN", "500 message minimum suspend", "99% reputation exemption", "cc_denied manual denial", "Автоматично спиране по репутация", "Спрян имейл канал"]
tags: [marketing, channels, reputation, auto-suspend, email, deliverability]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-reputation]]. See the hub for the other aspects (modal surface, metrics, sync cadence).

# Channel reputation — Auto-suspend

## Purpose

This page documents **how reputation drives auto-suspension** of the Email channel. After each reputation sync (see [[channels-reputation-sync]]) the platform compares the just-synced spam, bounce, and open metrics against fixed Email-channel thresholds. If a threshold trips — and the channel has cleared a minimum send volume and is not already exempt by a high overall reputation — the channel is deactivated, the reason is recorded, every campaign that uses the channel is stopped, and an admin notification fires. This is the mechanism that protects the store's sender reputation from being driven into the ground by a bad list or bad content.

## Where to find it

The thresholds are surfaced to the merchant in the **yellow warning banner** at the top of the Reputation modal (Sidebar → **Marketing** → **Channels** → **Channels setup** → Email card → **Reputation**). When the channel is suspended, the **channel card** shows a banned-reason message. See [[channels-reputation-modal]] for the modal surface.

The warning banner text reads verbatim:

> *"We will suspend your account if your campaign has a high spam rate (Spam rate over 0.5%), bounce rate over 5%), or very low open rate (Open rate less than 5%)."*

These percentages are hard-coded to the Email channel's `SUSPENDED_SPAM`, `SUSPENDED_BOUNCED`, `SUSPENDED_OPEN` constants — they do not change per merchant or per plan.

## What the merchant can do here

- **Read the thresholds** in the warning banner before they are crossed.
- **Read the suspend reason** on the channel card if the channel has already been suspended.
- **Take corrective action** — clean the list, change content, lower send frequency — then wait for the next sync; the auto-suspend lifts when the metrics recover.

## What the merchant cannot do here

- **Cannot manually unsuspend from the modal** — recovery happens via the next sync once metrics improve, or via a CloudCart staff manual unsuspend.
- **Cannot change the thresholds** — they are platform constants, not merchant settings.
- **Cannot auto-restart stopped campaigns** — campaigns stopped by the cascade stay stopped; re-activating the channel does not auto-restart them.

## Settings & fields

### The four suspend triggers

After each sync the platform compares the metrics from [[channels-reputation-metrics]] against thresholds:

| Trigger key | Metric checked | Threshold (Email) | Reason recorded |
|------------|----------------|-------------------|-----------------|
| `spam` | `abusepercent` > threshold | `SUSPENDED_SPAM = 0.5` | The actual abuse % as the reason value. |
| `bounced` | `unknownuserspercent` > threshold | `SUSPENDED_BOUNCED = 5` | The actual bounce % as the reason value. |
| `open` | `openedpercent` < threshold | `SUSPENDED_OPEN = 5` | The actual open % as the reason value. |
| `cc_denied` | (manual entry by CloudCart staff) | — | The staff-supplied text reason. |

Multiple triggers can fire simultaneously — the `suspended_by` channel setting is an **array**, not a single value.

### Banned-reason messages (verbatim)

When suspended, the channel card shows one of:

- *"Your spam score is:value which is higher than our maximum of:number"*
- *"Your bounced score is:value which is higher than our maximum of:number"*
- *"Your open rate is:value which is lower than our minimum of:number"*
- *"This channel was suspended by a CloudCart employee with a reason: :value"*

## Business rules

### 500-message minimum applies to all three reputation triggers

Auto-suspend by reputation does **not** trigger if the channel has sent fewer than **500** messages total (`SUSPENDED_COUNT_LIMIT = 500`). This minimum gates spam, bounce, AND open-rate suspension. So a brand-new store with 100 sends and 0% opens won't be suspended even though 0% < 5%. The minimum is the per-channel cumulative total, not a rolling window — a brand-new Email channel with poor first-batch metrics is given headroom to recover before suspension kicks in.

### Reputation ≥ 99% exempts the channel

If the headline `reputation` value is **≥ 99%**, the channel is exempt from auto-suspend regardless of the individual spam / bounce / open percentages. A clean sender with strong overall reputation gets the benefit of the doubt on noisy individual metrics — see [[channels-reputation-metrics]].

### Manual CC denial overrides all reputation checks

If a CloudCart staff member has flagged the channel with a manual denial reason, the suspension result is immediately the `cc_denied` row with the staff-supplied reason — reputation thresholds are not even evaluated. The merchant sees the staff-written reason verbatim on the channel card.

### Auto-suspend cascades to campaigns

When a sync flips the channel into a suspended state, every Campaign whose action references the Email channel is automatically marked stopped. Re-activating the channel later does **not** auto-restart the affected campaigns — the merchant must re-enable each one. See [[marketing-campaigns]] and the cascade note on [[marketing-channels]].

### Suspension fires an admin notification

When the suspend check returns a non-empty result, the platform deactivates the channel, writes the `suspended_by` setting, AND fires an admin notification under the channel's group (`campaign.channel.email`). The notification text is built in the control-panel locale — an EN-locale CP shows the EN message, a BG-locale CP shows the BG message.

### API-key expiry deactivates without a suspend reason

If the reputation fetch throws an "APIKey Expired" error (Elastic Email rejecting the stored key), the platform deactivates the channel without writing a reputation snapshot row — see [[channels-reputation-sync]]. This is a **pure deactivation** with no reputation suspend reason. To re-activate, the merchant must reconfigure / re-verify the Email channel — see [[marketing-channels-email]].

### Recovery

The merchant fixes the underlying problem (clean the list, change content, reduce frequency), waits for the next reputation sync, and the auto-suspend lifts when the metrics recover. A manual unsuspend requires CloudCart staff.

## Related

- [[marketing-channels-reputation]] — hub.
- [[channels-reputation-metrics]] — the spam / bounce / open metrics that drive the triggers, plus the 99% headline exemption.
- [[channels-reputation-sync]] — the sync pass that runs this check, and the API-key-expiry deactivation path.
- [[channels-reputation-modal]] — the warning banner surfacing these thresholds.
- [[marketing-channels]] — channel-setup hub with the full auto-suspend / cascade flow.
- [[marketing-channels-email]] — re-verification path after an API-key-expiry deactivation.
- [[marketing-campaigns]] — campaigns auto-stopped by the cascade.

## Open questions

No outstanding questions.
