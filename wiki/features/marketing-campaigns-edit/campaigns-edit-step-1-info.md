---
type: feature
nav_path: "Marketing → Campaigns → Edit → Step 1 (Main settings)"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Campaign main settings", "Campaign title", "Start delay", "Repeat campaign", "Use existing subscribers"]
tags: [marketing, campaigns, edit, step-1]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (trigger, actions, conditions, exit, message modals, launch flow, validation rules).

# Edit campaign — Step 1 (Main settings)

## Purpose

Step 1 collects the campaign's identity and (for Regular campaigns) its scheduled start time. It is rendered as a `CampaignStepCard` numbered "1", titled *"Main settings"* with the description *"Set campaign`s main settings, so you can find it later"*. Fields differ between Regular and Automated shapes.

## Where to find it

Top box on the **Edit campaign** screen ([[marketing-campaigns-edit]]) — the first card the merchant fills in after landing on the editor.

## What the merchant can do here

### Regular shape — 2-column grid

- Enter the **Campaign name** (required, unique per store — see [[campaigns-edit-validation-rules]]).
- Optionally tick **Start delay** and pick a future date+time. If unchecked, the campaign starts immediately on activation. If checked, the merchant picks a future date+time and the campaign waits until then before sending (campaign `progress` shows as `waiting_delayed` until the timestamp).

### Automated shape — stacked

- Enter the **Campaign name** (required, unique per store).
- **Repeat the campaign for customers that got into it more than once** — switch. If ON, a customer re-entering the trigger re-enters the campaign; if OFF, each customer flows through once and is locked out from re-enrolment.
- **Execute campaign for existing subscribers in segment** — switch. ON enrols all current segment members at campaign launch; OFF enrols only subscribers who newly enter the segment after launch.

## Settings & fields

### Regular shape

| Field | v-model | Type | Validation source |
|-------|---------|------|--------------------|
| **Campaign name** | `formData.title` | `CcInput`, placeholder *"Enter campaign name"* | Inline error from `errorStore.getError('title')` |
| **Start delay** date+time picker | `formData.start_at` | `CcDatePicker`, disabled until checkbox below is on | `errorStore.getError('start_at')` |
| **Start delay** checkbox | `formData.start_at_enabled` | `CcCheckbox` | — |

### Automated shape

| Field | v-model | Type |
|-------|---------|------|
| **Campaign name** | `formData.title` | `CcInput` |
| **Repeat the campaign for customers that got into it more than once** | `formData.repeat` | `CcSwitch` |
| **Execute campaign for existing subscribers in segment** | `formData.use_exists_subscribers` | `CcSwitch` |

All inputs respect `isReadOnly` — for non-draft campaigns the inputs are visually disabled. See [[campaigns-edit-validation-rules]] for the rules that drive `isReadOnly`.

## Business rules

- **Title is required and unique per store.** Saving a duplicate title surfaces: *"Campaign with this title already exists"*. See [[campaigns-edit-validation-rules]] for the full uniqueness rule.
- **`start_at_enabled` gates the picker.** When unchecked, the date picker is disabled; the campaign starts immediately on activation. When checked, the campaign waits until `start_at` before queueing the first enrolment job — the activation cascade in [[campaigns-edit-launch-flow]] respects the `start_at` delay.
- **`repeat` and `use_exists_subscribers` are tri-state-safe booleans** — the save endpoint validates these as strict booleans (`true|false|1|0|"1"|"0"`). Any other value returns *"Field accepted only true, false, 1, 0, '1', and '0'"*. The Vue UI emits booleans cleanly, but custom-API callers must respect this.
- **Regular campaigns don't get `repeat` / `use_exists_subscribers`.** They run once against the audience snapshot at activation time; there's no re-enrolment model.
- **Inputs are disabled when the campaign is not in Draft.** Active (`active=1`) and Inactive (`active=0`) campaigns visually grey out the fields — the merchant must Inactivate then re-enter Draft (or Copy) to edit; see [[campaigns-edit-validation-rules]].

## Related

- [[marketing-campaigns-edit]] — hub.
- [[campaign]] — Campaign entity.

## Open questions

No outstanding questions.
