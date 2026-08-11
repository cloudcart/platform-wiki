---
type: feature
nav_path: "Marketing → Channels → Channels setup → Auto-suspension"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel auto-suspend", "Channel suspension", "Suspended channel", "Spam threshold", "Bounce threshold", "Reputation suspend", "cc_denied", "Спрян канал", "Подозрителен канал"]
tags: [marketing, channels, suspension, reputation, spam, bounce]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, lifecycle, plan caps, sandbox, UI surfaces).

# Channels — auto-suspension & reputation

## Purpose

The four reasons a channel can be auto-suspended, the default thresholds, the merchant-visible messages that surface, the bootstrap exemption that protects new stores, the manual-override mechanism CloudCart support can grant, and the rules governing how a `suspended_by` channel behaves while in that state. Auto-suspension is currently active for the **Email** channel only — SMS, Viber, and Web Push inherit the threshold abstraction but do not actively report reputation back to the platform.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**. A suspended channel shows the **Suspended** status badge on its card; the textual `banned_reason` is exposed on the card AND on every campaign that references the channel. The Email channel additionally has a **Reputation** button that opens the modal documented at [[marketing-channels-reputation]].

## What the merchant can do here

- See **which** of the four triggers fired on a suspended channel (spam / bounced / open / cc_denied).
- See the current value vs the threshold that broke it.
- Resolve the underlying issue (clean list, pause sends, contact CloudCart support).
- Read the textual reason a CloudCart employee supplied when the suspension is `cc_denied`.

## Settings & fields

### The four auto-suspend triggers

| Reason key | Default threshold | Trigger condition |
|-----------|-------------------|-------------------|
| `spam` | `0.5` (Email's `SUSPENDED_SPAM`) | Spam complaint score exceeds the platform max. Subscribers flagging the merchant's mail as spam. |
| `bounced` | `5` (Email's `SUSPENDED_BOUNCED`) | Hard-bounce score exceeds the platform max. Too many invalid addresses on the list. |
| `open` | `5` (Email's `SUSPENDED_OPEN`) | Open rate falls below the platform min — the list is dead/disengaged. |
| `cc_denied` | — | A CloudCart employee has manually suspended the channel with a textual reason. |

The thresholds above are **defined only on the Email channel** — SMS, Viber, and Web Push do NOT actively report reputation back and so are not auto-suspended by these thresholds (verify). They CAN still be manually suspended via `cc_denied`.

### Merchant-visible suspension messages

When at least one trigger fires, the channel card and any dependent campaign surface one of these messages (the platform inserts the channel name + the breaking value):

- *"Your campaign channel:channel was suspended with a reason"*
- *"Your spam score is:value which is higher than our maximum of:number"*
- *"Your bounced score is:value which is higher than our maximum of:number"*
- *"Your open rate is:value which is lower than our minimum of:number"*
- *"This channel was suspended by a CloudCart employee with a reason: :value"*

## Business rules

### Bootstrap exemption — under 500 sends + 99% reputation

The auto-suspend only activates above a minimum send volume:

- Channels with fewer than **500** sends (`SUSPENDED_COUNT_LIMIT`) in their measurement window are **not** auto-suspended regardless of reputation. New stores are protected against noisy-signal suspensions during initial onboarding.
- Channels with reputation **≥ 99%** are exempt regardless of send volume — well-warmed senders aren't surprise-suspended by a transient blip.

Both exemptions apply only to auto-suspend; `cc_denied` (the manual route) ignores them entirely.

### Manual override — `manual_allowed_suspended`

A CloudCart employee can grant a **temporary bypass** via the `manual_allowed_suspended` setting on the channel. It carries:

- An **expiry timestamp** (ISO 8601 `expire` field) — once expired, the per-trigger threshold checks resume automatically.
- Optional **per-trigger custom thresholds** (e.g., `spam`, `bounced`, `open`) that supersede the channel's defaults until expiry. A merchant onboarding a freshly migrated list might be granted a higher temporary bounce threshold while they clean the list.

The override is requested through CloudCart support — the merchant cannot set it themselves.

### `cc_denied` trumps everything

When a CloudCart employee sets the `manual_denied_suspended` string setting:

- The channel is **immediately** suspended with the textual reason returned as the `banned_reason`.
- Auto-checks DO NOT run while `cc_denied` is set.
- Only an employee can clear the suspension.

This is the path used when CloudCart needs to stop the channel for reasons outside the four standard triggers (regulatory complaint, contract dispute, abuse investigation).

### What happens to in-flight campaigns when a channel auto-suspends

Auto-suspension follows the same cascade as manual deactivation — see [[marketing-channels-cross-lifecycle]]. Every campaign whose action references the suspended channel is marked stopped. The merchant must restart them manually after fixing the underlying issue and the channel returns to Active.

### Reputation reads (Email only)

The reputation call to the provider runs when the merchant opens the Channels setup page. The call uses a **10-second timeout** (other provider calls use 5 seconds). If the reputation call throws "expired", the platform surfaces a **Reset configuration** button on the Email card at that moment — the merchant clicks it to re-initialise the provider account binding.

The Reputation modal ([[marketing-channels-reputation]]) shows the live spam / open / click / bounce / reputation percentages and the thresholds for each.

### Inbound message-status → suspension feedback loop (Email)

The provider's per-send status feed drives suspension. When a send is reported back as `Error` with `category` in (`Suppressed`, `NoMailbox`, `Spam`, `NotDelivered`), the platform logs that send as HARD_BOUNCED — and HARD_BOUNCED counts feed the `bounced` trigger threshold. Other `Error` categories stay as BOUNCED (soft bounce) and do not contribute as heavily. Both flip the subscriber's per-channel `bounced = 1` flag — see [[marketing-channels-cross-magic-vars]] for the subscriber-side consequences.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-lifecycle]] — the lifecycle phase Suspended fits into.
- [[marketing-channels-cross-magic-vars]] — verification & bounced flag semantics on the subscriber side.
- [[marketing-channels-reputation]] — the Reputation modal showing the four reputation numbers.
- [[marketing-channels-email]] — the only channel currently with active reputation reporting.
- [[marketing-campaigns]] — pre-flight check that surfaces the suspension to a campaign.
- [[marketing-subscribers]] — subscribers' per-channel `bounced` / `unsubscribed` flags feed the suspension counters.

## Open questions

- Whether `SUSPENDED_COUNT_LIMIT` resets per measurement window or is cumulative across the channel's lifetime (verify).
