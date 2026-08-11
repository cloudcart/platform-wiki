---
type: feature
nav_path: "Marketing → Campaigns → Banned info → Aggregation"
route_name: admin.api.campaigns.banned-info
route_path: /admin/api/core/marketing/campaigns/banned-info/{campaign}
aliases: ["Banned reason aggregation", "How banned reasons are assembled", "Banned reason deduplication", "Recompute banned reasons", "Empty banned list"]
tags: [marketing, campaigns, banned, aggregation, dedup]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign banned info — aggregation

> Part of [[marketing-campaigns-banned-info]]. See the hub for the other aspects (surfaces, channel reasons, segment reasons, activation).

## Purpose

This page documents **how the combined banned-reason list is assembled** — the walk over the campaign's actions and channels, the trigger-segment check, the deduplication step, and the rule that the list is recomputed on every open (never cached).

## Where to find it

The merchant never sees the assembly directly — they see only the final list (multiple alert boxes on the legacy side-panel, or a comma-joined tooltip on the modern Vue list — see [[campaigns-banned-surfaces]]). This page describes what the backend does before rendering either surface.

## What the merchant can do here

Nothing directly — this is the computation behind the displayed list. The merchant's only lever is to fix the underlying channel / segment and reopen the panel to see the recomputed result.

## Settings & fields

There are no settings on this surface — the inputs to the aggregation are the campaign's actions, the channels those actions reference, and the campaign's `trigger_segment`.

## Business rules

### What gets aggregated into the banned list

The platform walks the campaign's actions, collects every unique action type, and for each:

1. Resolves the channel by name.
2. If the channel isn't registered: adds *"Missing channel type: $channelName"* to the list (see [[campaigns-banned-segment-reasons]]).
3. If the channel has a non-empty `banned_reason` (the channel's computed status reason): adds it to the list (see [[campaigns-banned-channel-reasons]]).

Then, separately, it checks the trigger segment:

- If `trigger_segment` is set AND the segment exists AND the segment is `active=0`: adds the segment's own list of why-it's-inactive errors (see [[campaigns-banned-segment-reasons]]).

Finally, the list is deduplicated.

### Deduplication

The alert list deduplicates (`array_unique`) so the merchant doesn't see the same channel-suspension reason multiple times if several steps use the same channel. If the campaign has 3 Email steps, the channel-not-configured reason is added 3 times during the walk but deduplicated to once. So the alert list is as short as possible.

### Reasons are recomputed on every open

The `banned_reason` for each channel is NOT cached at the campaign level — it's computed every time the surface opens by inspecting the current state of each channel. So:

- If the merchant just re-configured a channel: reopening shows fewer (or zero) reasons.
- If the merchant just re-installed a channel: the list reflects the current state.
- If the merchant is waiting for a suspension to expire: the reason persists as long as the suspension is active.

There's no "refresh banned info" button — the merchant just closes and reopens the surface.

### Empty alerts list

If the campaign has zero banned reasons (everything is healthy), the panel still opens — it just shows the campaign title and an empty body below. This is rare in practice because the merchant only sees the banned-info chip when there IS a reason.

### Multi-reason channels return one combined message before dedup

When a single channel has multiple reputation issues simultaneously (e.g. high spam AND low open rate), the channel joins all of its own reasons with `<br>` line breaks into ONE message string. The deduplication on the panel level then operates on that combined string — so two issues on the same channel appear as one alert box with two lines, not two boxes. See [[campaigns-banned-channel-reasons]] for which reasons can combine.

## How it works

The platform loads the campaign with its actions, walks each action to its channel, appends either a "Missing channel type" message or the channel's non-empty `banned_reason`, then appends the trigger segment's inactive-errors text if the segment exists and is inactive. The combined list is run through `array_unique` and handed to whichever surface is rendering. Because nothing is cached, the list always reflects the live state of every channel and the segment at the moment the surface opens.

## Related

- [[marketing-campaigns-banned-info]] — hub.
- [[marketing-campaigns]] — the campaign whose actions are walked.
- [[campaign]] — Campaign entity (carries the actions + `trigger_segment`).
- [[channel]] — Channel entity (the source of each `banned_reason`).
- [[segment]] — Segment entity (the trigger-segment side of the walk).

## Open questions

No outstanding questions.
