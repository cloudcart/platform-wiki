---
type: feature
nav_path: "Marketing → Campaigns → Banned info → Activation"
route_name: admin.api.campaigns.banned-info
route_path: /admin/api/core/marketing/campaigns/banned-info/{campaign}
aliases: ["Why won't my campaign send", "Campaign won't activate", "Campaign status toggle blocked", "Campaign pre-flight checks", "Inactive campaign won't turn on"]
tags: [marketing, campaigns, banned, activation, status]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign banned info — activation relationship

> Part of [[marketing-campaigns-banned-info]]. See the hub for the other aspects (surfaces, aggregation, channel reasons, segment reasons).

## Purpose

This page documents **why the banned-info surface is the source of truth for "why won't my campaign send"** — the banned reasons map 1:1 to the pre-flight checks that block the status toggle from flipping a campaign back to Active — and the fix workflow the merchant follows.

## Where to find it

The relationship is felt at two places: the **status toggle** on the campaigns list / editor (which refuses to flip Inactive → Active) and the **banned-info surface** that explains why (see [[campaigns-banned-surfaces]]). The merchant typically tries the toggle first, sees it bounce back, then opens the banned-info chip to find out which check failed.

## What the merchant can do here

- Read the banned reasons to learn exactly why activation is being refused.
- Act on each reason on its own screen, then return and retry the toggle.

## Settings & fields

There are no fields on this surface — the inputs are the same channel + segment states described on [[campaigns-banned-channel-reasons]] and [[campaigns-banned-segment-reasons]].

## Business rules

### This panel is the SOURCE OF TRUTH for "why won't my campaign send"

When a campaign is Inactive and the merchant's status toggle won't flip it back to Active, this surface is where to look first. The pre-flight checks that block activation (channel not configured, channel not active, credits exhausted, missing channel type, inactive segment, etc.) are the **same** checks that compute the banned reasons — so the surface's reasons map 1:1 to the activation failures.

### Status-toggle activation runs the same channel checks

When the merchant flips the campaign status toggle from Inactive to Active, the same channel-walk runs as a pre-flight check. If any channel returns `false` from the registry's `hasChannel($templateType)` check (i.e. the channel type isn't registered), activation is rejected with a "status error" — the merchant cannot activate until all action templates target a registered channel. This is the activation-side face of the "Missing channel type" reason — see [[campaigns-banned-segment-reasons]].

### No "Fix now" button — fixes happen on the owning screen

The banned-info surface only diagnoses. There's no inline fix action: the merchant navigates to [[marketing-channels]] (channel issues), [[marketing-segments]] (segment issues), or [[marketing-campaigns-edit]] (missing-channel steps), acts there, then returns to retry the toggle.

### Reasons clear as soon as the underlying state is fixed

Because the reasons are recomputed on every open and on every activation attempt (nothing is cached — see [[campaigns-banned-aggregation]]), a merchant who fixes a channel and immediately retries the toggle will succeed the moment the last reason is resolved. There's no propagation delay or cache to wait out — except a reputation suspension, which clears on its own timeline rather than on a config save (see [[campaigns-banned-channel-reasons]]).

### Permission and policy gates apply too

Standard campaign permission applies, and — like every campaign endpoint — this surface sits behind the campaign anti-spam policy gate (a separate gate from channel suspension). A merchant who hasn't accepted the policy is redirected to it before reaching any campaign surface. See [[marketing-campaigns-policy]].

## How it works

The status-toggle activation path re-runs the same action-channel walk used to build the banned list (see [[campaigns-banned-aggregation]]): it resolves each action's channel, rejects activation if any channel type is unregistered, and otherwise relies on each channel's `banned_reason` / suspension state to decide whether the campaign can run. Because the diagnostic surface and the activation gate share this logic, what the merchant reads in banned-info is exactly what they must clear to activate.

## Related

- [[marketing-campaigns-banned-info]] — hub.
- [[marketing-campaigns]] — campaigns list; the status toggle lives on the rows.
- [[marketing-campaigns-draft]] — Inactive tab where blocked campaigns land.
- [[marketing-campaigns-edit]] — campaign editor; where missing-channel steps are fixed.
- [[marketing-channels]] — channel setup; where channel reasons are fixed.
- [[marketing-segments]] — segments; where inactive-segment reasons are fixed.
- [[marketing-campaigns-policy]] — the separate anti-spam policy gate.
- [[campaign]] — Campaign entity (the object being activated).

## Open questions

No outstanding questions.
