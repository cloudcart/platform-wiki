---
type: feature
nav_path: "Marketing → Campaigns → Edit → Launch flow"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Review and launch modal", "Save draft", "Start campaign", "Campaign draft guard", "Leave draft campaign", "Activation cascade", "SetSubscribersToSingleSegment", "ExecuteCampaign"]
tags: [marketing, campaigns, edit, launch, draft, activation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, trigger, actions, conditions, exit, message modals, validation rules).

# Edit campaign — save, launch & draft-guard flow

## Purpose

The **Edit campaign** header has two terminal actions: **Save draft** (persist as Draft) and **Start campaign** (activate). This page covers the full flow for both — the **Review and launch** modal, the draft guard, the activation cascade onto the queue, and the toast/redirect behaviour.

The pre-flight **validators** (which checks fire, which error messages) live on [[campaigns-edit-validation-rules]].

## Where to find it

Header of the **Edit campaign** screen ([[marketing-campaigns-edit]]):

- **Save draft** button (visible when `isDraft=true` AND not read-only).
- **Start campaign** button (same condition + campaign already has an ID).

The draft guard fires automatically on Vue-router navigation and on browser `beforeunload`.

## What the merchant can do here

- **Click Save draft** → persists with `draft=true`; navigates to `campaigns-draft`; toasts *"Draft saved successfully."*
- **Click Start campaign** → opens the **Review and launch** modal; confirming triggers save → activate → toast → redirect.
- **Navigate away with unsaved changes** → the **Leave draft campaign?** modal pops up. Tab close / reload triggers the native `beforeunload` dialog first.

## Settings & fields

### Top-right action buttons

| Button | Visible when | Action |
|--------|--------------|--------|
| **Save draft** | Not read-only (create page OR draft being edited) | Persists current form state with `draft=true` payload; navigates to `campaigns-draft` on success and toasts *"Draft saved successfully."* |
| **Start campaign** | Same condition AND campaign already has an ID | Opens the **Review and launch** modal |

### "Review and launch campaign" modal

**Opens when:** merchant clicks **Start campaign** AND all blocks are saved (otherwise toast *"You must save all steps and conditions first!"* — see [[campaigns-edit-validation-rules]]).

`CcPopup` size `lg`, titled *"Review and launch campaign"*. Body is 4 horizontal rows:

| Section | Fields shown |
|---------|--------------|
| **Campaign overview** | Campaign name (or *"Untitled"*); Start date (date string OR *"Immediately"* OR *"When trigger conditions are met"* for Automated) |
| **Target audience** | Segment badge; Subscribers count (large semibold); Optional *"Trigger: Gets in segment"* hint for Automated |
| **Campaign settings** | One info badge per unique send channel (Email / SMS / Viber / Web push) used in any action step — deduped in campaign order |
| **Exit criteria** | Exit-when label (*"Makes an order"* by default) |

**Summary banner** (light-purple bg, rocket icon): *"You are about to launch this campaign to **{N}** subscribers via **{channel_list}**."*

**Footer:** **Cancel** (secondary, closes — nothing saved) | **Start campaign** (primary, triggers launch flow).

### Launch flow on Start campaign click

When the merchant confirms in the modal:

1. Builds the full save payload (`buildPayload(false)`) from current form state.
2. Calls `PUT /admin/api/core/marketing/campaigns/{id}` to persist all changes.
3. On save success: calls `GET /admin/api/core/marketing/campaigns/status/{id}/1` to flip `active` to 1.
4. On status success: allows the draft guard to skip the leave-confirm, navigates to `campaigns-active`, toasts *"Campaign started successfully"*.
5. On any failure: toast *"Error saving campaign"* or *"Error starting campaign"*; modal stays closed; merchant remains on the editor.

### Save flow on Save draft button

When the merchant clicks **Save draft** in the page header:

1. The shared composable's `submitDraftRef` is invoked.
2. Calls `PUT /admin/api/core/marketing/campaigns/{id}` with `buildPayload(true)` (`draft=true`).
3. On success: toast *"Draft saved successfully."*, allows leaving without re-prompt, navigates to `campaigns-draft`.
4. On error: stays on page, errors surface via the global error store.

Save draft does **NOT** run the pre-flight validators (channel checks, all-messages-set, etc.) — only basic schema validation runs (title required, segment required, at least one action with `action_type`). See [[campaigns-edit-validation-rules]] for the full ordering of validators.

### Draft guard navigation modal

**Opens when:** merchant tries to leave the editor via Vue router (in-app navigation) AND the form has unsaved changes AND the campaign is Draft.

`CcPopup` size `md`, titled *"Leave draft campaign?"*. Amber warning: *"This campaign is saved as a draft. Any unsaved changes will be lost if you leave."* + body: *"Would you like to save your changes before leaving?"*.

**Footer:** **Leave anyway** (ghost — discards edits and navigates) | **Save changes** (calls `PUT /admin/api/core/marketing/campaigns/{id}` with `draft=true`; on success closes modal + navigates; on error keeps modal open, toast *"Could not save draft. Please fix the errors and try again."*).

**Detection logic:** the guard snapshots `formData` (UI-only `_`-prefixed fields stripped) on first render when `isDraft=true`. The `hasChanges` computed deep-equals current `formData` against the snapshot — if equal, the guard does NOT fire.

**Browser `beforeunload`:** independent listener fires the native browser dialog (*"Changes you made may not be saved"*) on tab close / reload with unsaved changes. Runs **before** the in-app guard.

### Activation cascade — what runs after `active=1`

On Start campaign with `gets_in_segment`, two chained jobs dispatch immediately:

1. **`SetSubscribersToSingleSegment`** — rebuilds the segment's subscriber pivot. Onto the `segments5` queue.
2. **`ExecuteCampaign`** — enrols subscribers + dispatches per-step messages. Onto the `campaigns6` queue, chained after step 1.

If `start_at` is set, the first job is delayed until that timestamp; otherwise it runs as soon as a worker picks it up. A campaign with no start delay can dispatch messages **within seconds** of clicking Start (subject to queue worker availability).

**Side-effect — channel log labels.** Activation writes channel-log-name entries — `(type=campaign, name=title, channel=action_type)` and `(type=segment, name=segment.name, channel=action_type)` — used by the per-channel logs and [[marketing-campaigns-statistics]] for human-readable labels.

## Business rules

- **Save draft skips pre-flight checks** — only basic schema validation runs. Full pre-flight (channels configured + active + credits, messages set, segment filtered) fires only on **Start campaign**. See [[campaigns-edit-validation-rules]].
- **Pre-start confirmation modal precedes Start campaign**: *"Clicking the 'Start Campaign' button will launch your chosen campaign, and you won't be able to edit it once it's started."* Regular campaigns become immutable once started; Automated campaigns can be paused and re-edited, but the wording is cautious.
- **Save endpoint is guarded for non-Draft campaigns** — *"Campaign has status {status}! You can only edit draft campaigns!"* See [[campaigns-edit-validation-rules]].
- **Draft guard only fires when `hasChanges` is truthy.** Navigating away from an untouched draft skips the modal.
- **`beforeunload` runs first.** Tab close fires the native browser dialog before Vue-side logic; "Leave" in the browser dialog bypasses the in-app guard.
- **Activation cascade is queue-driven.** Time-to-first-message depends on `campaigns6` worker backlog.

## Related

- [[marketing-campaigns-edit]] — hub.
- [[marketing-campaigns-draft]] — landing page after a successful Save draft.
- [[marketing-campaigns]] — landing tab `campaigns-active` after a successful Start campaign.
- [[marketing-campaigns-statistics]] — analytics screen reads the channel-log labels written during activation.

## Open questions

No outstanding questions.
