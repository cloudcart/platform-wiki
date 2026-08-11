---
type: feature
nav_path: "Marketing → Campaigns → Edit → Step 2 (Trigger)"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Campaign trigger", "Campaign segment", "Trigger condition", "Subscribers count chip", "Inline create segment"]
tags: [marketing, campaigns, edit, segments, step-2]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, actions, conditions, exit, message modals, launch flow, validation rules).

# Edit campaign — Step 2 (Trigger / segment)

## Purpose

Step 2 picks the audience. For Regular campaigns it's a single segment — the audience that receives the campaign at launch. For Automated campaigns it's the **trigger** — subscribers enter (or leave) the campaign as they move in / out of the segment. The card is titled *"Trigger"* with a description that varies by type (*"Choose a segment for this campaign"* for Regular, *"Trigger campaign when a customer."* for Automated).

The card includes a live **Subscribers count chip** that estimates how many subscribers are eligible for this campaign's channels (intersection of segment, channel marketing flag, not-bounced, not-unsubscribed).

## Where to find it

Second box on the **Edit campaign** screen ([[marketing-campaigns-edit]]). Laid out as a 3-column responsive flex: When customer / Segments / Subscribers count chip.

## What the merchant can do here

- **Pick a trigger condition** (Automated only) — `Gets in segment` or `Gets out of segment`. Regular campaigns hardcode this to `gets_in_segment` (hidden input).
- **Pick a segment** from the autocomplete dropdown. For Regular campaigns it's the audience; for Automated it's the trigger that enrols subscribers.
- **Create a new segment inline** via the **Create segment** link (with `+` icon) below the row. This opens the **Segment add modal** → choose segment type → opens the **Segment create/edit modal** inline. On success, the new segment is automatically selected into `formData.trigger_segment` and the count chip starts polling.
- **Watch the subscribers-count chip** update as the selected segment is filtered server-side.

## Settings & fields

### Fields per type

| Field | Type | Visible when | Options |
|-------|------|--------------|---------|
| **When customer** | `CcSelect` (single-select, `can-clear: false`), v-model `formData.trigger_condition` | Automated only | `{id: 'gets_in_segment', name: 'Gets in segment'}`, `{id: 'gets_out_of_segment', name: 'Gets out of segment'}` |
| **Segments** | `CcSelect` with `api-url: /admin/api/core/marketing/segments/search`, v-model `formData.trigger_segment` | Always | Autocomplete-driven; pre-loaded option is the campaign's current `formData.segment` if set |
| **Subscribers count chip** | Side panel (left border) | Only when a segment is picked | 3 states: processing spinner (*"Your subscribers are currently being filtered"*), live count number + *"Subscribers"* label, or `—` if no count yet |

### Trigger-condition options

`trigger_condition` has exactly **three** valid values:

| Trigger key | Label | Notes |
|-------------|-------|-------|
| `gets_in_segment` | Gets in segment | Default for Regular (hardcoded); selectable for Automated |
| `gets_out_of_segment` | Gets out of segment | Automated only |
| `none` | (no segment-movement trigger) | Carried by **post-purchase** automated campaigns, where enrolment is driven by an order event rather than by entering/leaving a segment — see the `makes_an_order` purpose below. Not offered in the When-customer dropdown. |

**`makes_an_order` and `is_in_segment` are NOT `trigger_condition` values.** `makes_an_order` is the campaign **`purpose`** field — a separate switch set only by a predefined post-purchase template (see [[campaigns-create-predefined-clone]]), never by the When-customer dropdown. A campaign carrying `purpose=makes_an_order` + a segment enrols a customer when they **place a qualifying order** (the order's products / total match the segment) and is removed again on the next qualifying order — independent of the gets-in / gets-out segment-movement triggers above. `is_in_segment` ("Is in segment") survives only as a legacy display label and is not a value the modern editor saves.

### Inline segment-create flow

Below the row, when not read-only, the **Create segment** link opens the **Segment add modal** (`MarketingSegmentAddModal`) → segment-type chooser → **Segment create/edit modal** (`MarketingSegmentCreateOrEditModal`) inline.

On segment-created success, the new segment is automatically selected into `formData.trigger_segment` and the count chip starts polling.

### Subscribers-count endpoint

The count chip's data comes from `apiMarketingCampaigns.triggerSegmentCount` (`GET /admin/api/core/marketing/campaigns/set-segment/{campaign}/{segment}/0`). The response has:

- `customers_count` (string) — the deliverable subscribers count.
- `processing` (boolean) — true while the segment is still being filtered server-side.

The query auto-refetches on segment change and skips `refetchOnWindowFocus`. The "Your subscribers are currently being filtered" spinner is shown while `processing=true`.

## Business rules

- **Regular campaigns hardcode `trigger_condition` to `gets_in_segment`.** The When-customer dropdown is hidden; the field is sent as a fixed value in the save payload.
- **The post-purchase pattern is `trigger_condition=none` + `purpose=makes_an_order`.** A predefined "after an order" automated template ships with no segment-movement trigger (`none`) and the `makes_an_order` purpose; enrolment fires when a customer places an order whose products / total match the linked segment, not when they enter or leave it. The `purpose` field is not exposed in the When-customer dropdown — it only arrives via a [[campaigns-create-predefined-clone|predefined clone]].
- **`trigger_segment` is required to save.** A campaign without a segment fails the pre-flight checks on Start (*"You haven't filled all the settings!"* — see [[campaigns-edit-validation-rules]]).
- **Trigger segment swap rules by state:**
  - For an **unsaved (Draft)** campaign, segment changes are free.
  - For **Active** campaigns the dropdown is disabled.
  - For **Inactive** campaigns the merchant can swap but must re-activate to re-enrol.
  - A special `campaigns.save-trigger-segment` endpoint refreshes the segment after a create-segment side-panel returns.
- **Subscribers count is approximate until filtering finishes.** If the merchant clicks Start campaign while the count chip is still showing the processing spinner, the pre-flight check rejects with *"Subscribers are still being filtered"* — see [[campaigns-edit-validation-rules]]. The merchant must wait for the count to resolve.
- **Banned-reason badge when segment is deleted.** If the campaign references a deleted segment, the editor shows a banned-reason badge; clicking the chip opens [[marketing-campaigns-banned-info]]. The merchant must fix the segment reference before re-saving.
- **Dynamic-tag support depends on the segment's conditions.** Automated campaigns whose segment uses *Segment triggered products* can toggle **Dynamic generated tags from segment condition** (see [[campaigns-edit-step-3-actions]] for where the toggle lives). If the segment doesn't support dynamic tags, the save endpoint silently forces the field to 0 — see [[campaigns-edit-validation-rules]].

## Related

- [[marketing-campaigns-edit]] — hub.
- [[marketing-segments]] — segments list and editor (also opened inline via the Create-segment side-panel).
- [[marketing-campaigns-banned-info]] — banned-reason explainer for broken segment references.

## Open questions

No outstanding questions.
