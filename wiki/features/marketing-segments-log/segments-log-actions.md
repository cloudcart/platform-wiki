---
type: feature
nav_path: "Marketing → Segments → Log → Action vocabulary"
route_name: segments.core_new.log
route_path: /admin/marketing-new/segments/log/:id
aliases: ["Segment log actions", "Segment log event types", "Segment log action keys", "Segment log channel labels", "Видове събития в сегмент лог"]
tags: [marketing, segments, log, audit, actions]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
> Part of [[marketing-segments-log]]. See the hub for the other aspects (the table UI, the storage model, and batch rows).

# Segment log — action vocabulary & channel labels

## Purpose

This page is the reference for **what each Segment log row means**: the set of action keys that drive every row's icon, its merchant-facing label, and when it fires — plus the channel-label map that renders the Info column. When a merchant asks *"what does this icon mean / why does this row say 'Identified'?"*, this is the lookup table.

## Where to find it

The action icon + label appears in the **Action** column, and the channel detail in the **Info** column, of the Segment log table at `/admin/marketing-new/segments/log/:id`. See [[segments-log-table-ui]] for the table layout itself.

## What the merchant can do here

The merchant reads (not edits) these values:

- **Recognise the event type** from the Action column icon + label.
- **Read the channel + identifier** (or RFM / marketing detail) from the Info column.
- **Click the action label** to open the subscriber detail modal — see [[segments-log-table-ui]].

## Settings & fields

### Action vocabulary (the event types that appear in the log)

These are the action keys that drive the icon, the row label, and the underlying log entry:

| Action key | Merchant-facing label | When it fires |
|------------|----------------------|---------------|
| `added_to_segment` | "Subscriber is added to customer segment:segment_name" | A subscriber starts matching the segment's conditions (Automated) or the segment was regenerated and matched them (One-time). |
| `removed_from_segment` | "Subscriber is removed from customer segment:segment_name" | A subscriber stops matching the conditions, or was manually removed. |
| `begin_added_to_segment` | "Added subscribers to customer segment:segment_name" | Batch header — opens a group of additions from a single regeneration run. |
| `begin_removed_from_segment` | "Removed subscribers from customer segment:segment_name" | Batch header — opens a group of removals from a single regeneration run. |
| `identified_by` | "Subscriber is identified" | An anonymous visitor became a known subscriber and was attached. |
| `add_channel` | "Added new channel" | The subscriber added a new contact channel (Email, SMS, Phone, WebPush, Viber, Messenger). |
| `remove_channel` | "Remove channel" | The subscriber removed a contact channel. |
| `subscribed` | "Subscribed" | The subscriber subscribed (to email/SMS/etc.) — may add them to channel-filtered segments. |
| `unsubscribed` | "Unsubscribed" | The subscriber unsubscribed — may remove them from channel-filtered segments. |
| `confirmed_email` | "Confirmed his email" | The subscriber verified their email — relevant for the *Verified-email* segment condition. |
| `change_subscription` | "The subscriber changed his subscriptions" | The subscriber edited their channel preferences. |
| `attach_customer` | "Attach customer" | A subscriber was linked to a customer account. |
| `added_tags` | "Added tags to subscriber" | A tag was added — relevant for tag-filtered segments. |
| `remove_tags` | "Removed tags from subscriber" | A tag was removed. |
| `rfm` | "Changed from group" (combined with `rfm_old_new`, `rfm_new`, or `rfm_old` detail strings) | The subscriber's RFM bucket changed — relevant for RFM-filtered segments. |
| `marketing` | "Marketing" | The subscriber's marketing-consent flag changed (green when granted, red when revoked). |

The icons map to these keys: green plus for **Added to segment**, orange minus for **Removed from segment**, green target for **Identified**, plus / minus network icons for **Add channel / Remove channel**, tag icons for **Added tags / Removed tags**, mail-bulk for **Marketing**, plus-circle for **RFM** group changes.

### Channel labels in the Info column

When the row carries a `channel` value, the Info column renders `<channel label>: <identifier>` using this map:

| Channel key | Label |
|-------------|-------|
| `email` | Emails |
| `phone`, `sms` | Phone |
| `viber`, `viber_message` | Viber |
| `messenger` | Messenger |
| `web_push`, `webpush` | Web Push |
| `uuid` | UUID |

For RFM rows the Info column shows *"Changed from RFM group:old to:new"*, *"Added to RFM group:new"*, or *"Removed from RFM group:old"*. For marketing rows it shows a Marketing indicator.

## Business rules

- **The action key is rendered through a per-action Info partial** (the platform code) when one exists for that action; otherwise the row falls back to the channel-info string above.
- **The `marketing` row colour signals direction** — green when consent was granted, red when revoked. There is no separate "consent revoked" action key; the same `marketing` key carries the direction in its detail.
- **The `begin_*` keys are batch headers, not individual events** — they head a group of per-subscriber rows that are not shown on the modern list. See [[segments-log-batch-rows]] for how the batch is split.

## Related

- [[marketing-segments-log]] — hub.
- [[marketing-campaigns]] — campaign logs reuse the same collection with a partly-overlapping vocabulary (`send_message`, `link_clicked`, `message_read`, `unsubscribe`, `added_to_campaign`, `removed_from_campaign`, `non_execute_action`).
- [[subscriber]] — the entity whose channel / tag / RFM changes generate these events.

## Open questions

No outstanding questions.
