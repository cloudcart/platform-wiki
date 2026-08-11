---
type: feature
nav_path: "Marketing → Campaigns → Subscribers → Progress"
route_name: campaigns.subscribers
route_path: /admin/campaigns/subscribers/{campaign_id}
aliases: ["Campaign subscriber progress", "Subscriber funnel state", "Waiting executing completed removed", "Enrolment vs received", "Removed subscribers"]
tags: [marketing, campaigns, subscribers, recipients]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign subscribers — progress model

> Part of [[marketing-campaigns-subscribers]]. See the hub for the other aspects (surfaces, columns, enrolment model).

## Purpose

This page documents the **per-subscriber progress model** of a campaign enrolment — the `subscriber_to_campaigns.progress` enum, what each value means, and the critical support fact that **being enrolled does NOT mean the subscriber received a message**. A support agent answering "the report says this customer is in the campaign but they say they never got the email" should land here.

## Where to find it

The progress state is shown in the **Progress** column of the Campaign-subscribers grid — Sidebar → **Marketing** → **Campaigns** → a campaign's **Subscribers (N)** button → legacy side-panel (see [[campaigns-subscribers-surfaces]]). On the modern redirect, the per-subscriber state is in the subscriber detail modal's **Campaigns** sub-section.

## What the merchant can do here

- Read whether a subscriber is waiting, executing, completed, removed, or paused in the funnel.
- Diagnose why a subscriber did or didn't receive a message (enrolled ≠ received).
- See subscribers who were removed mid-flow — they stay visible for audit.
- Cross-reference the exact delivery state via the [[marketing-campaigns-statistics-log|per-send log]].

## Settings & fields

### Progress values per subscriber

The `subscriber_to_campaigns.progress` enum captures where the subscriber is in the campaign:

| Progress | Meaning |
|----------|---------|
| `waiting` | Enrolled but no step has executed yet (e.g., waiting for a step delay to elapse). |
| `executing` | A step is currently being delivered or in-flight. |
| `completed` | The subscriber finished the full campaign and exited (with the exit tag applied). |
| `removed` | The subscriber was removed mid-flow — either explicitly via a `remove_from_campaign` step, or because they unsubscribed / bounced / completed the exit purpose condition. |
| `paused` | Paused mid-flow (rare; happens when a delay step is reached and time hasn't elapsed). |

The progress rendering is delegated to the platform code, a small Smarty view that colour-codes the badge. Note the **UI badge is binary** (Completed vs Pending) even though the enum is granular — see [[campaigns-subscribers-columns]] for the rendering detail.

## Business rules

### Enrolment ≠ "received the message"

A subscriber on the list MAY or MAY NOT have actually received a message:

- They could be **waiting** (no step has fired yet — `progress=waiting`).
- They could have been **removed** before any send happened (e.g., they unsubscribed within the delay window).
- They could be **executing** right now (the step is in-flight).
- They could have received **some** messages but not all (mid-funnel state — see the Step column on [[campaigns-subscribers-columns]]).

To see WHO actually received a specific message, the merchant should use [[marketing-campaigns-statistics-log]] (per-send log). This is the single most common "I'm enrolled but didn't get the email" support scenario.

### Removed subscribers don't disappear from the list

The `remove_from_campaign` action flips the progress to `removed` but does **not** delete the pivot row — the subscriber stays visible on the list with the `removed` badge (rendered as the binary "Pending" badge in the UI). The merchant can still see they were enrolled and where they exited. This is intentional for auditability.

### Removal triggers

A subscriber moves to `removed` for several reasons: an explicit `remove_from_campaign` step in the funnel, the subscriber unsubscribing or bouncing on the relevant channel mid-flow, or the subscriber satisfying the campaign's exit purpose condition before completing all steps. All of these leave the pivot row in place with `progress=removed`.

### Completion applies the exit tag

A subscriber reaching `completed` has run through to the campaign's exit tag; this is also the point at which the `times_completed` counter increments (see [[campaigns-subscribers-enrolment]] for how repeating campaigns accumulate completions).

## Related

- [[marketing-campaigns-subscribers]] — hub.
- [[campaigns-subscribers-columns]] — how the granular enum collapses to a binary Progress badge in the UI.
- [[campaigns-subscribers-surfaces]] — where the Progress column appears.
- [[marketing-campaigns-statistics-log]] — per-send log; the authoritative source for whether a message was actually delivered.
- [[marketing-campaigns-edit]] — campaign editor; defines the `remove_from_campaign` steps and exit conditions.
- [[subscriber]] — Subscriber entity.

## Open questions

No outstanding questions.
