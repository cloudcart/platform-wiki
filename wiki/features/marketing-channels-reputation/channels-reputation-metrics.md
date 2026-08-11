---
type: feature
nav_path: "Marketing → Channels → Channels setup → Reputation → Metrics"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Reputation metrics", "Spam rate Open rate Bounce rate Click rate", "Reputation rate roll-up", "abusepercent openedpercent unknownuserspercent clickedpercent", "Метрики за репутация", "Спам процент процент отворени"]
tags: [marketing, channels, reputation, metrics, email, deliverability]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-reputation]]. See the hub for the other aspects (modal surface, sync cadence, auto-suspend).

# Channel reputation — Metrics

## Purpose

This page defines the **five reputation numbers** the Email channel reports: the headline **Reputation rate** roll-up plus the four card-level breakdown metrics — **Spam rate**, **Open rate**, **Bounce rate**, **Click rate**. Each comes from Elastic Email's reputation telemetry for the store's dedicated Email sub-account and reflects the store's actual send history. Three of the four cards (spam, bounce, open) are also the inputs to the auto-suspend logic; the fourth (click) is informational only. This page documents what each number means, its backend source field, its formatting, and its default.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → on the **Email** channel card → click **Reputation** (star icon). The headline rate is in the modal footer; the four metric cards are in the modal body — see [[channels-reputation-modal]] for the full layout.

## What the merchant can do here

- **Read the headline Reputation rate** — the single composite sender-reputation score.
- **Read each of the four card metrics** to diagnose which dimension of deliverability is weak (too many spam complaints, too many bounces, too few opens, or low engagement clicks).
- **Map a metric to the corresponding auto-suspend trigger** — see [[channels-reputation-auto-suspend]] for the thresholds.

## What the merchant cannot do here

- **Cannot edit any metric** — every value is read-only and provider-sourced.
- **Cannot change how a metric is computed** — the percentages are Elastic Email's, not a CloudCart calculation.
- **Cannot see a per-day or per-campaign breakdown** — each metric is a single full-account snapshot number; the window is fixed — see [[channels-reputation-sync]].

## Settings & fields

### Headline metric

| Field | Source | Display | Meaning |
|-------|--------|---------|---------|
| `reputation` | Elastic Email reputation roll-up | Modal footer, large green text (e.g., `98.50%`) | Provider's composite sender-reputation score (0–100%). A value **≥ 99%** exempts the channel from auto-suspend regardless of the other metrics — see [[channels-reputation-auto-suspend]]. |

### Card-level metrics

All four cards render the formatted percentage (e.g., `0.25%`) on a labelled card. Default value when no data has been synced is `0%`.

| Card label | Field | What it measures | Auto-suspend role |
|-----------|-------|------------------|-------------------|
| **Spam rate** | `abusepercent` | Percent of recipients who flagged the merchant's mail as spam (abuse reports back from the recipient's mailbox provider). | Auto-suspends if **> 0.5%** — see [[channels-reputation-auto-suspend]]. |
| **Open rate** | `openedpercent` | Percent of recipients who opened the message (tracked via Elastic Email open-pixel + tracking domain). | Auto-suspends if **< 5%** — list is dead / disengaged. |
| **Bounce rate** | `unknownuserspercent` | Percent of recipients flagged as unknown users / hard bounces by Elastic Email. | Auto-suspends if **> 5%** — too many invalid addresses on the list. |
| **Click rate** | `clickedpercent` | Percent of recipients who clicked any link inside the message. | Informational only — no auto-suspend trigger. |

### Formatting and defaults

Each metric arrives from the API as `{ value: float, formatted: '99.50%' }`. The cards render the `.formatted` string. When no data has been synced yet, every card defaults to `0%`, and the initial-data stub renders `0.00%` until the live fetch returns — see [[channels-reputation-modal]].

## Business rules

### Click rate has no suspend role

Click rate is purely an engagement signal — it never triggers an auto-suspend on its own. Only spam, bounce, and open feed the suspend logic — see [[channels-reputation-auto-suspend]].

### The headline rate can override the breakdown

A high composite `reputation` (≥ 99%) gives a clean sender the benefit of the doubt: the channel is exempt from auto-suspend even if an individual card looks noisy. So a merchant can see, for example, a slightly elevated bounce card yet remain un-suspended because the roll-up reputation is excellent. The exemption mechanics are on [[channels-reputation-auto-suspend]].

### Metrics reflect a full-account rolling window

These percentages are Elastic Email's own sliding evaluation of the sub-account's history — not a per-day or per-campaign CloudCart computation. The modal echoes whatever the provider reports at sync time — see [[channels-reputation-sync]].

### Per-store isolation

Every store uses a CloudCart-managed Elastic Email sub-account, and the Reputation modal always reads from the store's own sub-account. The merchant's metrics are theirs alone — bad email from another store cannot drag them down.

## Related

- [[marketing-channels-reputation]] — hub.
- [[channels-reputation-modal]] — the modal that renders these metrics.
- [[channels-reputation-auto-suspend]] — how spam / bounce / open thresholds drive suspension, plus the 99% exemption.
- [[channels-reputation-sync]] — where the numbers come from and how often they refresh.
- [[marketing-channels-usage]] — the sibling Usage modal tracks send quantity (Clicks / Opened counts there are 30-day campaign engagement, a different number from these full-account percentages).

## Open questions

No outstanding questions.
