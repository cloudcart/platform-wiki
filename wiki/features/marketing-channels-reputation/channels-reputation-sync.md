---
type: feature
nav_path: "Marketing → Channels → Channels setup → Reputation → Sync cadence"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Reputation sync", "Reputation sync cadence", "12-hour reputation sync", "Reputation snapshot", "Reputation cache miss live fallback", "Синхронизация на репутация", "Снимка на репутация"]
tags: [marketing, channels, reputation, sync, background-job, email]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-reputation]]. See the hub for the other aspects (modal surface, metrics, auto-suspend).

# Channel reputation — Sync cadence

## Purpose

This page documents **how and when the reputation numbers refresh**. CloudCart pulls fresh reputation data from Elastic Email on a fixed **12-hour background interval** and caches one snapshot per UTC day; the Reputation modal reads that cached snapshot, falling back to a synchronous live provider call only when today's snapshot does not yet exist. The values reflect Elastic Email's **rolling full-account window**, not a CloudCart per-day computation — which is why the modal has no date picker and always shows "now". This explains the most common merchant question: *"I launched a campaign — why doesn't the reputation reflect it yet?"*

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → on the **Email** channel card → click **Reputation** (star icon). The footer rate and card percentages reflect the latest synced snapshot — see [[channels-reputation-modal]] for the layout and [[channels-reputation-metrics]] for the numbers.

## What the merchant can do here

- **See the most recent reputation snapshot** for the Email channel.
- **Watch the numbers move** as a newer sync writes a fresher row (over hours, not in real time).

## What the merchant cannot do here

- **Cannot trigger a manual recalculation** — there is no refresh button; the sync runs on its fixed background interval.
- **Cannot pick a historical date or range** — the modal always shows the current snapshot; there is no time-series view.
- **Cannot speed up the 12-hour cycle** — a freshly-launched campaign may not show for up to 12 hours depending on where in the cycle the merchant lands.

## Settings & fields

This is a background-behaviour page — there are no merchant-editable fields. The relevant mechanics:

### Sync cadence

| Aspect | Behaviour |
|--------|-----------|
| Interval | **12 hours** (43200 seconds). |
| Concurrency | Single-instance — only one sync runs at a time. |
| Scope per run | Iterates active channel managers per site; only the Email channel returns a real reputation value — every other channel returns null and is skipped, so the snapshot store only ever holds Email rows. |
| Stored snapshot | One row per (site, channel, sync day), holding the five reputation values — see [[channels-reputation-metrics]]. |
| Day key | The sync day is the **UTC start-of-day** at sync time, so a 03:00 UTC and a 14:00 UTC sync on the same date both upsert the same row — the modal always shows the most-recent value of the day. |

### What happens when the modal opens

1. CloudCart looks up today's snapshot (`sync day = today's UTC start-of-day`).
2. If today's snapshot exists, it returns the cached values (fast path, typically under 100 ms).
3. If no snapshot for today (e.g., the scheduled sync hasn't run yet on a freshly-onboarded store, or the merchant lands between syncs), it calls Elastic Email's reputation API **live** and returns those values (this fallback also feeds the in-controller refresh).

## Business rules

### Up to 12 hours of lag after a send

Because the sync runs twice a day, a campaign launched right after a sync may not influence the displayed reputation for up to 12 hours. The card percentages and footer rate refresh as the next sync writes a newer row.

### Snapshot window is the full account, not a date range

The reputation values reflect Elastic Email's own rolling reputation window — not a per-day or per-month CloudCart computation. Elastic Email keeps a sliding evaluation of the sub-account's spam, bounce, open, and click history; the modal echoes whatever percentages the provider reports at sync time. There is no UI to pick a different window — see [[channels-reputation-modal]] for the read-only surface.

### Live fallback can be slower

On a cache miss the API performs a synchronous live call to Elastic Email and returns those values directly. The merchant does not see a "Loading" placeholder for long, but on heavy reputation traffic the modal may take 1–2 seconds on a cache miss versus under 100 ms on a cache hit.

### Each sync feeds the auto-suspend check

Immediately after writing the snapshot, the same background pass evaluates the just-synced metrics against the channel's thresholds and updates the suspend state. The full threshold logic, the 500-message floor, and the 99% exemption are on [[channels-reputation-auto-suspend]].

### API-key expiry deactivates instead of writing a row

If the reputation fetch throws an "APIKey Expired" error (Elastic Email rejecting the stored key), the platform deactivates the channel without writing a reputation row, rather than recording a bad snapshot — the recovery path is on [[channels-reputation-auto-suspend]].

## Related

- [[marketing-channels-reputation]] — hub.
- [[channels-reputation-metrics]] — the five values written into each snapshot.
- [[channels-reputation-modal]] — the read-only surface that reads the snapshot (and why there is no date picker).
- [[channels-reputation-auto-suspend]] — the suspend check that runs after each sync, including the API-key-expiry deactivation path.
- [[marketing-channels]] — channel-setup hub.

## Open questions

No outstanding questions.
