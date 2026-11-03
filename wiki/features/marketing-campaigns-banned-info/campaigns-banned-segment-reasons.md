---
type: feature
nav_path: "Marketing → Campaigns → Banned info → Segment & missing-channel reasons"
route_name: admin.api.campaigns.banned-info
route_path: /admin/api/core/marketing/campaigns/banned-info/{campaign}
aliases: ["Segment banned reasons", "Inactive segment campaign error", "Missing channel type", "Segment disabled error", "Soft-deleted segment campaign"]
tags: [marketing, campaigns, banned, segments, channels]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign banned info — segment & missing-channel reasons

> Part of [[marketing-campaigns-banned-info]]. See the hub for the other aspects (surfaces, aggregation, channel reasons, activation).

## Purpose

This page documents the two reason sources that are **not** the channel's reputation state: the **trigger-segment inactive errors** (with their localized text and the soft-deleted-segment edge case) and the **"Missing channel type"** reason that appears when a campaign action references a channel key that no longer resolves.

## Where to find it

These reasons surface in the banned-info side-panel or tooltip (see [[campaigns-banned-surfaces]]) alongside any channel reasons. The merchant fixes segment issues on [[marketing-segments]] and missing-channel issues by editing the campaign on [[marketing-campaigns-edit]].

## What the merchant can do here

Nothing on the banned-info surface (read-only). To clear a segment reason the merchant re-activates / repairs the segment; to clear a "Missing channel type" reason the merchant edits the campaign and replaces or removes the affected step.

## Settings & fields

### Segment-side reasons

If the campaign's `trigger_segment` is set, exists, and is `active=0`, the segment's own inactive-errors text is appended to the banned list. Common segment failure reasons:

- The segment's conditions reference a deleted product / category.
- The segment was manually deactivated.
- The segment's auto-filter job is failing.

### "Missing channel type"

A campaign action references a channel mapping (e.g. `email`, `viber_message`, `web_push`) by string key. When the resolved key isn't present in the channel registry, the panel surfaces *"Missing channel type: <name>"* for each unresolved key.

## Business rules

### Segment-inactive reason text is localized

When the trigger segment is inactive, the alert text comes from a translation key (the platform code) — *"The segment is disabled due to the following error: :errors|The segment has been disabled due to the following errors: :errors"*. The `:errors` placeholder is replaced by the segment's stored inactive-error list joined with `<br>` line breaks. Because the side-panel renders the HTML, the line breaks are preserved.

### Soft-deleted segment is skipped

If the trigger segment has been soft-deleted, the campaign's segment relation returns null and the panel's segment-inactive check is skipped entirely — so a deleted segment contributes no banned reason here. The merchant instead sees a different error in the campaign editor when they try to re-activate ("missing segment" or similar).

### "Missing channel type" — when it happens

A campaign created using a channel that has since been retired or renamed (legacy data migration, plugin / app uninstall, or a deprecated provider being removed) leaves the action's channel key unresolvable in the registry. The panel then surfaces *"Missing channel type: <name>"* for each unresolved key. The merchant **cannot** fix this from the panel — they must edit the campaign and replace / remove the affected step. This is also the check that blocks status-toggle activation — see [[campaigns-banned-activation]].

### These reasons are deduplicated alongside channel reasons

Both the segment text and any "Missing channel type" entries go through the same `array_unique` step as the channel reasons — see [[campaigns-banned-aggregation]].

## How it works

After the action-channel walk (see [[campaigns-banned-aggregation]]), the platform checks `trigger_segment`. If it resolves to an existing, inactive segment, the localized segment-disabled message is built from the segment's stored inactive-error list and appended. During the action walk itself, any action whose channel key fails to resolve in the registry contributes a *"Missing channel type: <name>"* entry. Both feed into the same deduplicated list that the surfaces render.

## Related

- [[marketing-campaigns-banned-info]] — hub.
- [[marketing-segments]] — segments; where the merchant repairs / re-activates an inactive segment.
- [[marketing-campaigns-edit]] — campaign editor; where the merchant removes a missing-channel step.
- [[segment]] — Segment entity (the source of the inactive-errors text).
- [[channel]] — Channel entity (an unregistered key produces "Missing channel type").

## Open questions

No outstanding questions.
