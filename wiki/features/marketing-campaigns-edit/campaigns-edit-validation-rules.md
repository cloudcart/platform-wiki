---
type: feature
nav_path: "Marketing → Campaigns → Edit → Validation rules"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Campaign edit validators", "Pre-flight checks", "Save cascade", "Max action steps", "Edit-only-in-draft", "Title uniqueness", "?edit=1", "Plan-tier campaign quota"]
tags: [marketing, campaigns, edit, validation, business-rules]
plan_gates: ["campaigns", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, trigger, actions, conditions, exit, message modals, launch flow).

# Edit campaign — validation rules & business constraints

## Purpose

The **Edit campaign** screen has two save paths (Save draft vs Start campaign) and a server-side gate that enforces all rules regardless of UI. This page catalogues every validator, error message, save-cascade transaction step, and platform constraint (plan-tier quota, max-steps cap, edit-only-in-Draft, `?edit=1` fallback).

UI-side flows (modals, buttons, redirects) live on [[campaigns-edit-launch-flow]]. Field-level validators (character limits, required tags) live on the corresponding step pages.

## Where to find it

Rules fire at three points on [[marketing-campaigns-edit]]:

- **On Save draft / Start campaign** — server-side gate on `PUT /admin/api/core/marketing/campaigns/{id}`.
- **On Start only** — pre-flight checks on `GET /admin/api/core/marketing/campaigns/status/{id}/1`.
- **On row insert** — plan-tier quota on creation, copy, predefined-clone (not on save).

## What the merchant can do here

Nothing directly — this is the validation catalogue, not a UI screen. The merchant interacts with the [[marketing-campaigns-edit|editor screen]]; the rules below fire on Save / Start. Refer here to understand error toasts.

## Settings & fields

Documents rule enforcement, not form fields — every constraint ties back to a field on one of the step-aspect pages. See those pages for the inputs; see the rules below for what save accepts.

## Business rules

### Edit is only fully open in Draft state

| `active` value | State | Edit behaviour |
|----------------|-------|----------------|
| `2` | Draft | Every box editable; **Save draft** + **Start campaign** buttons show. |
| `1` | Active | Boxes get the `disabled` class — view-only. Must Inactivate first to re-enter edit. |
| `0` | Inactive | Same edit-locked behaviour as Active. |

Regular campaigns that have completed (`progress=completed`) auto-archive — read-only forever (`archived_at=now`).

### Title uniqueness

Title must be **unique per store**. Duplicate save returns: *"Campaign with this title already exists"*.

### Only Draft campaigns are editable through the API

The save endpoint's `campaign_is_active` rule rejects non-Draft saves with: *"Campaign has status {status}! You can only edit draft campaigns!"*. Applies uniformly to **Active**, **Inactive**, **and Archived** — no API back door. To edit a started campaign, Copy it (which produces a new Draft) and edit the copy. See [[marketing-campaigns-copy]].

### Pre-flight checks on Start campaign

On Start campaign the backend validates this checklist before activating:

| Check | Error if failed |
|-------|-----------------|
| All steps saved (no unsaved drafts in Step 3) | *"You must save all steps and conditions first!"* |
| All required settings filled (title, segment, etc.) | *"You haven't filled all the settings!"* |
| Every step has a message template set | *"You need to set all the messages"* |
| Each referenced channel is configured | *"Channel ':name' is not configured"* |
| Each referenced channel is active | *"Channel ':name' is not active"* |
| Each referenced channel has sufficient credits | *"You do not have enough credits for:name"* |
| Linked segment has finished filtering subscribers | *"Subscribers are still being filtered"* |
| Generic catch-all | *"Campaign was not started"* |

On failure the merchant stays on the editor with an error toast; the offending box is visually highlighted.

### Pre-start confirmation modal

Before Draft → Active the merchant sees: *"Clicking the 'Start Campaign' button will launch your chosen campaign, and you won't be able to edit it once it's started."* Wording is cautious — Regular campaigns become immutable once started; Automated can be paused (Inactive) and re-edited.

### Save-as-draft is always permitted

**Save draft** persists the partial form without pre-flight checks. Only title-uniqueness + basic schema (title required, segment required, ≥ 1 action with `action_type`) is enforced. The campaign stays in Draft.

### Campaign-edit cascade (transaction)

On save, the PUT handler runs inside a DB transaction:

1. Updates the `campaigns` row.
2. **Deletes all** existing `campaign_actions` rows.
3. Inserts fresh `campaign_actions` rows from the form.
4. Deletes orphan `campaign_action_templates` whose `action_order` isn't in the new form.
5. Re-links surviving templates by `action_id` (action IDs changed in steps 2-3).
6. If activating: walks every template and materialises variable references on the channel.
7. If activating + `gets_in_segment`: queues `SetSubscribersToSingleSegment` → chains `ExecuteCampaign` — see [[campaigns-edit-launch-flow]].

Any throw rolls back the whole transaction.

### Trigger-segment swap, auto-archive, banned-reason, permissions

- **Swap rules:** Draft = free; Active = dropdown disabled (segment locked); Inactive = swap allowed but must re-activate. `campaigns.save-trigger-segment` refreshes after the inline side-panel returns. See [[campaigns-edit-step-2-trigger]].
- **Auto-archive on completion** — Regular campaigns finish into `progress=completed` + `archived_at=now`; surface in [[marketing-campaigns-archive|Archived]]. Automated campaigns don't auto-archive.
- **Banned-reason badges block re-save** — suspended channel / deleted segment renders badges that open [[marketing-campaigns-banned-info]]; must fix before re-saving.
- **Permissions** — the campaign-edit endpoint gates both reading and saving by the campaign-edit permission.

### Maximum action steps per campaign

Hard cap enforced on save (the Vue editor does NOT pre-check):

| Campaign type | Max action steps | Error if exceeded |
|---------------|------------------|-------------------|
| Regular | **1** | *"Rows may not be greater than 1"* |
| Automated | **5** | *"Rows may not be greater than 5"* |

See [[campaigns-edit-step-3-actions]].

### Repeat / use_exists_subscribers / dynamic_tags tri-state-safe

Save validates these three switches as strict booleans (`true|false|1|0|"1"|"0"`). Anything else returns *"Field accepted only true, false, 1, 0, '1', and '0'"*. Vue UI emits booleans cleanly; custom-API callers must respect this.

### `dynamic_tags` quietly forces to 0 when the segment doesn't support it

The *Dynamic generated tags from segment condition* switch (see [[campaigns-edit-step-3-actions]]) is cross-checked server-side. If the segment lacks dynamic-tag-capable conditions (e.g., abandoned-cart product conditions), the saved value is **forced to 0** regardless of UI state.

### Channel credit pre-check is on Start, not on Save draft

**Save draft** skips the channel credit check — drafts can target audiences larger than the current SMS / Viber credit pool. The check fires on **Start**, comparing deliverable subscriber count against `plan_remaining`. If short: *"You do not have enough credits for {channel name}"* — activation fails, campaign stays Draft.

### Plan-tier campaign quota enforced on creation, not on edit

The plan-tier max-campaigns limit (`campaigns` plan-feature key) is checked on **row insert** — creation, copy, predefined-clone. NOT on save. Once a draft exists the merchant can keep editing / starting / stopping it without hitting the ceiling; only **adding new campaigns** does.

### `?edit=1` is a legacy usability fallback

The Vue editor's read-only flag is bypassed when the URL has `?edit=1` AND the campaign is Draft. The campaigns list passes `?edit=1` only for Draft rows. Appending `?edit=1` to an Active campaign's URL shows editable inputs but the save still fails server-side — **the API is the real gate, the UI flag is a usability layer.**

### Activation cascade

On Start with `gets_in_segment`, the API dispatches `SetSubscribersToSingleSegment` (`segments5` queue) chained to `ExecuteCampaign` (`campaigns6` queue). Delayed if `start_at` is future. See [[campaigns-edit-launch-flow]].

### Saved-email-template linkage auto-creates on save

A step with a `template_id` from the [[marketing-campaigns-message-template|saved templates library]] but no `campaign_action_templates` row → save bootstraps one (name, subject, HTML, Unlayer JSON copied). If the row already exists, only `template_id` + `template_type` linkage syncs — previously-customised content preserved.

## Related

- [[marketing-campaigns-edit]] — hub.
- [[marketing-campaigns-copy]] — clone an Active campaign back into Draft for editing.
- [[marketing-campaigns-banned-info]] — banned-reason badges that block re-save.
- [[marketing-campaigns-archive]] — Regular campaigns auto-archive on completion.

## Open questions

No outstanding questions.
