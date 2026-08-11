---
type: feature
nav_path: "Marketing → Campaigns → Types & action steps"
route_name: campaigns
route_path: /admin/marketing-new/campaigns
aliases: ["Regular vs Automated campaign", "Campaign action types", "Campaign step actions", "Trigger conditions", "Completion conditions"]
tags: [marketing, campaigns, types, actions, automation]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects (tabs & filters, create modal, AI assistant, row actions, rules, execution internals).

# Campaigns — Regular vs Automated, plus action types

## Purpose

This aspect catalogues the two campaign shapes (**Regular** vs **Automated**) and the per-step action types they can use. The shape is fixed at create time and cannot be changed later — picking Regular vs Automated is the most consequential decision on the create modal.

## Where to find it

The shape is chosen on the **+ Create campaign** modal — see [[campaigns-list-create-modal]]. After creation, the shape is encoded in the route: `campaigns-edit/regular/{id}` vs `campaigns-edit/automated/{id}` — see [[marketing-campaigns-edit]] for the editor.

## What the merchant can do here

- Pick the right shape for the use case (one-shot blast vs multi-step automation).
- Compose action steps from the catalogue below.
- Wire conditional branches and per-step delays (Automated only).

## Settings & fields

### Regular vs Automated

| Type | Shape | When to use |
|------|-------|-------------|
| **Regular** | One trigger ("Choose a segment for this campaign") → one or more delivery actions in sequence → optional exit conditions. Trigger condition is always `gets_in_segment` (set automatically on create). | One-time promotional blast to an existing segment. |
| **Automated** | Trigger condition picked from a list (`gets_in_segment`, `gets_out_of_segment`, `makes_an_order`, `is_in_segment`) → multi-step action graph with per-step conditions and delays → exit conditions + exit tag. | Drip sequences, welcome series, abandoned-cart recovery, post-purchase upsell, win-back. |

### Trigger conditions (Automated)

| Key | Meaning |
|-----|---------|
| `gets_in_segment` | Fires when a subscriber newly enters the segment |
| `gets_out_of_segment` | Fires when a subscriber leaves the segment |
| `makes_an_order` | Fires when a subscriber places an order |
| `is_in_segment` | Fires for every subscriber currently in the segment at launch (one-shot enrolment) |

For Regular campaigns, the trigger is always `gets_in_segment` (set automatically on create).

### Action types (per step)

From the action options translation list:

| Action key | Label | Description |
|-----------|-------|-------------|
| `email` | Email | Send an email via the configured Email channel |
| `sms_nth_message` | SMS (NTH Message) | Send an SMS through NTH provider |
| `sms_msghub_message` | SMS (msghub) | Send an SMS through msghub provider |
| `viber_message` | Viber message | Send a Viber business message |
| `web_push` | Web push notification | Send a browser push notification |
| `messenger_message` | Messenger message | Send a Facebook Messenger message (legacy) |
| `set_tags` | Set tags and continue campaign | Tag the customer, continue to next step |
| `remove_from_campaign` | Remove from campaign | Exit the customer from the funnel |
| `remove_from_campaign_and_set_tags` | Set tags and remove from campaign | Tag + exit |
| `set_customer_group` | (Set Customer Group) | Change the customer's group |

### Completion conditions per step

Each delivery action can have an associated **completion condition** that delays the next step until met (e.g., *"After: 2 days"* / *"To: 7 days"*), or branches on:

- `Link was clicked`
- `Link not clicked`
- `Message has been read`
- `Message has not read`

See [[campaigns-edit-step-3-conditions]] for the full per-step condition editor.

## Business rules

### Maximum action steps per campaign

The API enforces a hard cap on action-step count:

- **Regular** campaigns: max **1** action step. So the "one or more delivery actions in sequence" framing only applies to Automated — for Regular, a single send is the upper bound.
- **Automated** campaigns: max **5** action steps.

Exceeding the cap returns *"Rows may not be greater than 1"* or *"Rows may not be greater than 5"* on save. This is enforced server-side only — the Vue editor lets the merchant add steps freely, then the save fails at the API.

### "Existing subscribers in segment" toggle

For automated campaigns the merchant can toggle *"Execute campaign for existing subscribers in segment"* — when **ON**, all current segment members are enrolled at campaign launch; when **OFF**, only subscribers who newly enter the segment after launch are enrolled.

### Per-customer repeat behaviour

*"Repeat the campaign for customers that got into it more than once"* — if **ON**, a customer who re-enters the trigger segment re-enters the campaign; if **OFF**, each customer can only flow through the campaign once.

### Exit tagging

The setting key `box.title.campaign_exit_tag` — labelled *"Tag the customer who exit the campaign successfully with"* — when set, customers who finish the campaign without being filtered out get this tag (useful for re-targeting or downstream segmentation). See [[campaigns-edit-exit-and-tagging]].

### Subscribers who leave the trigger segment mid-flow

When a subscriber leaves the trigger segment of an Automated campaign they're already enrolled in (segment conditions no longer match, segment is recomputed), the platform fires a remove job with reason `gets_out_of_segment`. The subscriber's progress is flipped to **`removed`** and they stop receiving further steps. The pivot row stays in [[marketing-campaigns-subscribers]] with the `removed` badge for audit purposes — they do **not** finish the remaining steps.

### Auto-archive on completion (Regular only)

A Regular campaign auto-archives on completion (sets `progress = completed` AND `archived_at = now`). Automated campaigns can keep running indefinitely. See [[campaigns-list-tabs-and-filters]] for the progress-enum table.

### Shape is immutable after Start

The save validator allows edits only on Draft campaigns. Changing a Regular-vs-Automated decision after launch is impossible — the merchant must copy the campaign (producing a new Draft) and edit the copy. See [[campaigns-list-rules]] for the full editability rules.

## Related

- [[marketing-campaigns]] — hub.
- [[campaigns-list-create-modal]] — where the shape is picked.
- [[marketing-campaigns-edit]] — editor that adds/edits action steps.
- [[campaigns-edit-step-3-actions]] — per-step action editor.
- [[campaigns-edit-step-3-conditions]] — per-step completion / branch conditions.
- [[campaigns-edit-exit-and-tagging]] — exit-tag setting in the editor.
- [[marketing-segments]] — segments used as trigger audience.
- [[marketing-campaigns-subscribers]] — subscriber enrolment list, where `removed` badge appears.

## Open questions

None.
