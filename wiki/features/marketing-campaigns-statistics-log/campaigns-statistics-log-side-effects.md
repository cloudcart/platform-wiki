---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Side-effects"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["Auto-bounce", "Auto-unsubscribe (from log)", "Auto-verify", "triggerRemove from log", "earlyExit rejectsMarketing", "Click-through tracking middleware", "CampaignTrack middleware", "cc_campaign query"]
tags: [marketing, campaigns, statistics, logs, side-effects, subscriber-state]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status values, status archive, filters & table, view-message, Email mapping, storage).

# Per-send log — status side-effects on the subscriber

## Purpose

A log row's status isn't just a passive record — certain transitions automatically update the **subscriber's** state. A HARD_BOUNCED email flips the subscriber's channel-row `bounced=1` flag so future sends skip them. An ABUSE_REPORT auto-unsubscribes them. A SEEN or CLICKED on an unverified channel marks the channel verified. And tracked-link clicks flow back through the storefront, advancing automated-campaign steps. This page documents these automatic side-effects — which statuses trigger which subscriber-state changes, and how the click-through middleware funnels engagement back into the campaign engine.

## Where to find it

The side-effects are not directly visible in the log surface — they fire **behind the scenes** when statuses change. The merchant observes the **results** in three places:

- The subscriber's profile at [[marketing-subscribers]] shows the updated channel flags (`bounced`, `unsubscribed`, `verified`).
- The campaign's per-subscriber **removal log** (on [[marketing-campaigns-subscribers]]) shows the reason key (`hard_bounced`, `abuse`, `error`) for the auto-removal.
- Storefront-side click-through tracking advances the campaign step automatically — visible on [[marketing-campaigns-statistics]] as a step transition.

## What the merchant can do here

There are no merchant-controlled actions for the side-effects — they're automatic and unconditional. What the merchant CAN do:

- **Investigate why a subscriber was auto-removed** by reading the reason key on the campaign's removal log.
- **Recover a wrongly-bounced subscriber** by manually clearing the `bounced` flag on the subscriber's channel record (see [[marketing-subscribers]]).
- **Understand the impact of a single bad-list import** — every HARD_BOUNCED row triggers removal across the active campaign, so a bad list spike causes a removal spike.

## Settings & fields

There are no merchant-editable settings for the side-effects — they're automatic. The merchant sees the *result* on the subscriber's channel record (`bounced`, `unsubscribed`, `verified` flags on the per-channel row) and on the campaign-removal log.

The triggering statuses:

| Status transition | Subscriber-channel side-effect | Campaign-membership side-effect |
|-------------------|-------------------------------|---------------------------------|
| → `HARD_BOUNCED` | `bounced=1`, `bounced_status='hard_bounced'` | Auto-remove from current campaign (`triggerRemove` with `earlyExit=true`, `rejectsMarketing=true`). Reason key: `'hard_bounced'`. |
| → `ABUSE_REPORT` | `unsubscribed=1` (auto-unsubscribed) | Auto-remove from current campaign. Reason key: `'abuse'`. |
| → `ERROR` | `bounced=1`, `bounced_status=<error reason>` | Auto-remove from current campaign. Reason key: `'error'`. |
| → `SEEN` | `verified=1` (channel is real and engaged) | None. |
| → `CLICKED` | `verified=1` | Click-tracking middleware advances campaign steps with "link clicked" continue conditions. |

## Business rules

### Auto-bounce + auto-remove on ERROR / HARD_BOUNCED / ABUSE_REPORT

When a log row's status transitions to one of these terminal-failure states:

1. **The SubscriberChannel is marked bounced** — `bounced=1`, `bounced_status=<error reason>`. Future sends skip this channel (segment-membership and consent-gate filters skip bounced channels).
2. **The campaign-remove flow is triggered** with `earlyExit=true` and `rejectsMarketing=true` — pulling the subscriber out of the current campaign AND flipping their per-channel marketing-acceptance flag to false. Automatic suppression — the merchant doesn't have to manually clean their list.
3. The reason key surfaces on the per-subscriber removal log: `'hard_bounced'`, `'abuse'`, or `'error'`.

### Auto-verify on SEEN / CLICKED

When a status transitions to `SEEN` or `CLICKED`, the platform **sets `verified=1`** on the (subscriber, channel, identifier) row. An opened / clicked email automatically counts as verified even without double-opt-in. The verified flag affects segment membership (filters that require `verified=1`) and deliverability scoring.

### Click-through tracking flows through the storefront

Tracked links route through the merchant's own storefront URL with a `cc_campaign=<base64-json-blob>` query parameter. The storefront-side `CampaignTrack` middleware reads it and:

1. Increments the campaign action's `OPENED_URL` + `SUCCESSFULLY_SENT` stat counters.
2. Updates the log row's status to `CLICKED` (which also auto-verifies the channel).
3. Dispatches a job that advances Automated campaign steps with "link clicked" continue conditions.
4. **Redirects** to the destination URL with `cc_campaign` / `cc_subscriber` stripped — the customer's address bar shows the clean URL.

### `rejectsMarketing=true` flips the channel-level consent

The removal flow's `rejectsMarketing=true` flips the subscriber's per-channel marketing-acceptance flag to false. So a HARD_BOUNCED email stops ALL future marketing sends to that address until the subscriber re-confirms — the suppression-list mechanism. See [[marketing-subscribers]].

### Side-effects are per-channel, not per-subscriber

A subscriber with both Email and SMS channels who hard-bounces email still receives SMS — only the Email channel row is flagged. Segment filters that allow either channel still reach the subscriber.

### Auto-verify is sticky

Once `verified=1` is set by SEEN / CLICKED, the platform does not auto-reset it on subsequent BOUNCED events. Verified status represents a historical engagement fact. Manual reset from the subscriber profile is possible.

## How it works

The auto-bounce + auto-remove + auto-unsubscribe side-effects fire from the same code path that updates the log row's status. When the channel-specific webhook handler maps the provider status to `ERROR` / `HARD_BOUNCED` / `ABUSE_REPORT` (see [[campaigns-statistics-log-email-mapping]] for the Elastic Email mapping table), it:

1. Updates the log row's status (which triggers the [[campaigns-statistics-log-status-archive|status archive]] append).
2. Looks up the SubscriberChannel for `(subscriber_id, channel, identifier)`.
3. Sets the bounced / unsubscribed flag on that channel row.
4. Calls the campaign-remove trigger with the appropriate reason key.

The campaign-remove call cascades: it removes the subscriber from the current campaign's enrolment, writes the removal-log row with the reason, and (with `rejectsMarketing=true`) flips the per-channel marketing-acceptance flag.

The auto-verify on SEEN / CLICKED is simpler — the same mapping path that sets the status to SEEN / CLICKED also updates `SubscriberChannel.verified = 1` on the matched (subscriber, channel, identifier) row.

Click-through tracking is the inverse direction — it's the storefront triggering an update on the log, not the log triggering an update on the subscriber. The merchant's storefront request carrying `cc_campaign=...` enters the storefront's middleware stack, the `CampaignTrack` middleware parses the parameter (base64-decoded JSON containing the action ID + subscriber ID), increments counters, marks the log row CLICKED, dispatches the campaign-step-advance job, and redirects clean.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-status-values]] — the statuses that trigger side-effects.
- [[campaigns-statistics-log-status-archive]] — the archive append happens before the side-effects.
- [[campaigns-statistics-log-email-mapping]] — provider-status → canonical-status mapping that decides which side-effect fires.
- [[marketing-subscribers]] — the SubscriberChannel record that gets updated.
- [[marketing-campaigns]] — the campaign-remove flow that pulls the subscriber out mid-campaign.
- [[marketing-channels-email]] — channel-level handling of bounces.

## Open questions

- Verify that NOT_SENT does NOT trigger auto-bounce / auto-remove (it's the platform's pre-emptive skip, not a delivery failure).
