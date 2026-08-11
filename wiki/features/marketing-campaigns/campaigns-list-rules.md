---
type: feature
nav_path: "Marketing → Campaigns → Business rules"
route_name: campaigns
route_path: /admin/marketing-new/campaigns
aliases: ["Campaigns business rules", "Campaign validation", "Campaign quota", "Anti-spam policy gate", "Channel suspension", "Last-touch attribution", "Title uniqueness", "Campaign autosave"]
tags: [marketing, campaigns, rules, validation, quota, attribution]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects.

# Campaigns — business rules

## Purpose

This aspect catalogues every business rule that gates campaign creation, save, launch, and attribution.

## Where to find it

The rules apply globally to every campaign action reached from the [[marketing-campaigns]] list, the [[marketing-campaigns-edit]] editor, the [[campaigns-list-create-modal]], and [[campaigns-list-ai-assistant]].

## What the merchant can do here

The merchant cannot configure these rules — they are platform invariants. This is the catalogue for diagnosing *"why can't I start my campaign"* / *"why is my title rejected"* / *"why was my campaign auto-deactivated"* tickets.

## Settings & fields

No merchant-facing settings — this is a rules reference. The error strings and setting keys below are verbatim merchant-facing text.

## Business rules

### Title uniqueness

A campaign's title must be unique per store; a duplicate surfaces *"Campaign with this title already exists"*. Uniqueness ignores `active` value and archived state — an Archived or Inactive title is NOT reusable. Soft-deleted (trashed) campaigns are excluded, so a deleted title can be reused.

### A new campaign starts as Draft

Creating a campaign sets `type` from the URL (`regular` or `automated`), a null title, and `active = 2` (Draft), then opens the edit page. Drafts appear only on the Draft tab, not Active / Inactive.

### Anti-spam policy is required before any campaign action

If `campaigns.anti_spam_policy_accepted` is falsy, reaching the channels or saved-templates screens redirects to the policy screen; the gate applies to every campaign action. See [[marketing-campaigns-policy]].

### Starting a campaign requires all steps + messages saved

Clicking **Start campaign** runs pre-flight checks:

- *"You must save all steps and conditions first!"* — a step is unsaved.
- *"You haven't filled all the settings!"* — a required setting is empty.
- *"You need to set all the messages"* — a step's message template isn't filled.
- *"Campaign was not started"* — generic failure.

A confirm modal warns: *"Clicking the 'Start Campaign' button will launch your chosen campaign, and you won't be able to edit it once it's started."* See [[campaigns-edit-launch-flow]].

### Channel-level guards

Before sending, the platform checks the channel:

- *"Channel ":name" is not configured"* — not installed or settings incomplete.
- *"Channel ":name" is not active"* — installed but inactive (`status = 0`).
- *"You do not have enough credits for:name"* — credit-billed channel, empty balance.

A campaign requiring a turned-off channel auto-deactivates (see channel-status flip below).

### Channel suspension by spam/bounce/open thresholds

A channel can be **auto-suspended** for one of these reasons:

| Reason key | Threshold |
|------------|-----------|
| `suspended_by.spam` | Spam complaint score > platform max |
| `suspended_by.bounced` | Bounce score > platform max |
| `suspended_by.open` | Open rate < platform min |
| `suspended_by.cc_denied` | Manually suspended by a CloudCart employee with a reason |

A campaign on a suspended channel shows *"The campaign is disabled due to the following reason"*; the channel must be fixed first. See [[marketing-campaigns-banned-info]] for the title-cell badge.

### Statistics aggregation lag

The reached / opened / clicked / orders / turnover columns refresh hourly; the list tooltip states *"The statistical information is updated every hour"*. The sent count updates faster, but engagement metrics (open / click / conversion) lag up to 60 minutes. See [[campaigns-list-execution-internals]].

### Segment-completion gate

A segment must finish its initial subscriber-filtering before a campaign can target it; otherwise: *"Subscribers are still being filtered"*.

### Segment swap on a started campaign is blocked

Only Draft campaigns are editable — saving any other status returns *"Campaign has status {status}! You can only edit draft campaigns!"*. Changing a started campaign's trigger segment is therefore **not permitted, from UI or API**. To change the audience the merchant copies the campaign (a new Draft), edits the trigger, and launches that. See [[marketing-campaigns-copy]].

### Attribution on "orders" / "turnover" columns is last-touch

A campaign link carries `?cc_campaign=...`; clicking through stores the campaign in the customer's session, and later clicks **overwrite** it — so an eventual order is stamped with the last-clicked campaign. **Last-touch wins**, with no first-touch, multi-touch, or split-credit model. See [[marketing-campaigns-statistics-full]].

### Channel-status flip cascades to campaigns

Turning OFF a channel auto-deactivates any campaign whose actions reference it, after confirming: *"There are campaigns that are ':name'. They will be automatically marked as stopped"*.

### Permissions

A staff member's role must include the campaigns permission to read or edit them.

### Soft-delete + cascade

Deleting a campaign (including bulk delete via [[campaigns-list-row-actions]]) is a soft-delete. Permanent deletion cascades to its actions, action templates, and action logs, and detaches its subscribers.

### Plan-tier quota enforced on every campaign-create

Every campaign creation — manual, predefined-clone, copy, or AI-from-suggestion — passes the plan-limit check. At quota the request fails with **402 Payment Required** (API) or redirects to the plan-upgrade page (admin panel). The quota counts every non-deleted campaign, including Drafts, Inactive, and Archived; a merchant at their cap frees a slot only by **permanent-deleting** an Archived one. The **+ Create campaign** button fires the error only after the click.

### Maximum action steps per campaign

Regular max **1** step; Automated max **5**. Exceeding returns *"Rows may not be greater than 1"* / *"Rows may not be greater than 5"*. See [[campaigns-list-types-and-actions]].

### Audience filter at execution time matches the segment-picker preview

At send time the audience is filtered through the **same** marketing-flag intersection the picker counter shows: subscribers must be on the relevant channel, `marketing = 1`, `bounced = 0`, `unsubscribed = 0`, and for email channels with `unconfirmed_send = false`, also `verified = 1`. So the Step 2 customer-count chip matches the deliverable population. The picker dialog states verbatim: *"To be subscribed to the {channel} channel..., to accept marketing, not to be unsubscribed, and not to be marked as Bounced."*

### Channel credit check happens on save, not just on send

Activating a campaign on a credit-based channel (SMS, Viber) compares `plan_remaining` against the subscriber count for the picked segment + channel intersection. If `plan_remaining < subscribers_count` the save returns *"You do not have enough credits for {name}"* and the campaign stays Draft / Inactive — shrink the audience or top up credits first.

### No time-based autosave, but a navigation guard

The editor does NOT autosave on a timer — changes stay in-browser until **Save campaign**. Two loss-protection guards: a *"Leave draft campaign?"* modal (Save changes / Leave anyway) on in-app navigation, and a browser warning on tab close. *Leave anyway* discards unsaved edits.

### Scheduled start

A campaign can have a future `start_at` ("Start delay") — until then its progress is `waiting_delayed` and it shows *"Scheduled for:date"*. See the progress-enum table on [[campaigns-list-tabs-and-filters]].

### Subscribers arriving after an Automated campaign's `start_at` get nothing

Newly-arriving segment members are skipped for any Automated campaign whose `start_at` has already passed. So a subscriber entering the trigger segment today is **not** enrolled in a campaign scheduled for yesterday; they enrol only if `start_at` is null or still future. (Regular campaigns auto-archive after their single send, so this doesn't apply.)

## Related

- [[marketing-campaigns]] — hub.
- [[marketing-campaigns-policy]] — anti-spam policy gate.
- [[marketing-campaigns-banned-info]] — banned-reason badges on the list row.
- [[marketing-campaigns-statistics-full]] — last-touch attribution mechanic in detail.
- [[campaigns-edit-launch-flow]] — Start-campaign preflight in the editor.
- [[campaigns-edit-validation-rules]] — per-step validation in the editor.
- [[plan-gates]] — `campaigns.*` plan limits, channel-credit limits.

## Open questions

None.
