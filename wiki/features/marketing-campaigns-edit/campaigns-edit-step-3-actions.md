---
type: feature
nav_path: "Marketing → Campaigns → Edit → Step 3 (Actions)"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Campaign action step", "Action type", "Execute after", "Set message", "Per-channel state preservation", "Funnel builder", "Channel credit banner"]
tags: [marketing, campaigns, edit, action-step, step-3]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, trigger, conditions, exit, message modals, launch flow, validation rules).

# Edit campaign — Step 3 action steps

## Purpose

Step 3 is the funnel builder. The merchant builds an ordered list of **action steps** — each step is one delivery (Email / SMS / Viber / Web Push) or one in-line operation (tag set/remove, customer-group change, campaign exit). For Automated campaigns, steps can be chained and branched via **condition blocks** (see [[campaigns-edit-step-3-conditions]]).

This page covers the action step itself. The card is titled *"Campaign actions"* with the description *"Setup the main logic of the campaign"*.

## Where to find it

Third box on the **Edit campaign** screen ([[marketing-campaigns-edit]]). The biggest card on the page.

## What the merchant can do here

- **Add an action step** via the **Next action** dropdown (`step` option) at the bottom of the funnel.
- **Pick the action type** from the channel dropdown — fed by `apiMarketingChannels.configured` so only **configured** channels appear.
- **Set the execute-after delay** — *Immediately* or *After N hours/days/weeks/months*. Regular campaigns are always immediate (picker disabled).
- **Attach a message template** via **Set message** — opens the per-channel editor ([[campaigns-edit-message-modals]]) or the Email template picker ([[marketing-campaigns-message-template]]).
- **Edit / delete** a saved message via the links on the saved-template card.
- **Save the step** — runs validators and collapses to saved state.
- **Edit / delete** a saved step via hover overlay / trash icon (confirm dialogs warn when downstream steps would be lost).

## Settings & fields

### Action types available per step

| Action key | Label | Notes |
|-----------|-------|-------|
| `email` | Email | Unlayer designer — see [[marketing-campaigns-message-template]] |
| `sms_nth_message` | SMS (NTH) | NTH SMS editor |
| `sms_msghub_message` | SMS (MsgHub) | MsgHub SMS editor |
| `viber_message` | Viber message | Viber editor |
| `web_push` | Web Push | Web Push editor |
| `set_tags` / `remove_tags` | Set / Remove tags | Tag picker inline |
| `remove_from_campaign` | Remove from campaign | Hard-exits subscriber |
| `remove_from_campaign_and_set_tags` | Set tags and remove from campaign | Tag + exit |
| `set_customer_group` | (Set Customer Group) | Reassigns subscriber's [[customer-group]] |

**Important — the dropdown lists ONLY message channels** (Email / SMS / Viber / Web Push), fed by `apiMarketingChannels.configured` (only **configured** + **active** channels appear). The non-delivery action types (`set_tags`, `remove_tags`, `remove_from_campaign`, `remove_from_campaign_and_set_tags`, `set_customer_group`) are NOT selectable from the dropdown — they only appear on steps pre-set from a predefined-template clone, where the tag-picker / customer-group-picker renders inline. Once a message is configured, the Action-type select is **locked** (`isActionTypeLocked = true`). Tooltip: *"To change the action type, remove the current message first (use Delete on the message card)."*

### Action step fields

Each step is a card with a `Step N` badge (orange `#FF9059`) on the top edge.

| Field | v-model | Type / Notes |
|-------|---------|--------------|
| **Execute after** | `internalAction.complete_time_type / _interval / _interval_type` | `MarketingCampaignExecuteActionSelect`: **Immediately** radio OR **After N hours/days/weeks/months** radio + number + unit. Disabled for Regular. |
| **Action type** | `internalAction.action_type` | `CcSelect` fed by `apiMarketingChannels.configured`. Locked once a message is set. |
| **Configuration column** | (varies by `action_type`) | See per-channel rendering below |

### Configuration column per action type

- **Email / Viber / SMS / Web Push** (`requiresMessageTemplate`):
  - **No message set** → **Set message** button. Opens `CampaignEmailTemplateModal` (Email) or `CampaignMessageSettingsModal` (others).
  - **Message saved** → renders a `CampaignActionCard` with channel icon + internal title + **Edit** / **Delete** links. Delete calls `POST /admin/api/core/marketing/campaigns/message/delete/{template_row_id}` (toast *"Template deleted successfully."*). The delete uses the `campaign_action_templates` linkage row id (`_template_row_id` / `template.id`), never the saved-template library id.
- **Set tags / Remove tags**: `CcSelect` in `tags` mode wired to `/admin/autocomplete/customer-tags?key=tag` — v-model `internalAction.customers_tags`.
- **Set customer group**: `CcSelect` wired to `/admin/api/core/customers/groups` — v-model `internalAction.customer_group`.

### Credit / channel-limit banner

A red banner shows below the row when the action type's last save returned a credit / limit error:

| Action type | Banner title |
|-------------|--------------|
| `viber_message` | *"You have reached your Viber limit"* |
| `sms_nth_message` | *"You have reached your SMS limit"* |
| `email` | *"You have reached your email sending limit"* |
| `web_push` | *"You have reached your web push limit"* |

Carries a **Purchase credits** button (links to `campaigns-channels`). For `viber_messages`-typed errors the button opens a `PlanFeature` modal instead.

### Save step validators

Clicking **Save step** runs: *"Please select an action type."* / *"Please specify the time interval."* (interval mode) / *"Please select a message template."* (message channels) / *"Please select tags."* / *"Please select a customer group."*

On pass: card collapses to saved state and the **Next action** skeleton appears below.

### Edit / delete affordances + "Next action" skeleton

- **Edit step overlay**: dark backdrop with **Edit step** button on hover/tap. For steps with downstream steps, confirm reads *"Are you sure you want to edit the step? If you change the action type, or delete the step, the next steps will be deleted!"*.
- **Delete step**: trash icon → confirm *"Remove step?"*.
- **"Next action" skeleton**: dropdown with `step` (*"Action step"*) and `condition` (*"Condition"*, only when last block is an action step — see [[campaigns-edit-step-3-conditions]]). Hidden whenever any step / condition is in editing state; **always visible** when the actions array is empty.

### Per-channel state preservation

When the merchant switches **Action type** between Email / SMS / Viber / Web Push, the previous channel's message state is snapshotted into a `messageStateByType` ref. Switching back restores `condition`, `has_chosen_template`, `template_id`, `internal_title`, and `template`. So a carefully-crafted Email design survives a brief toggle to Viber to compare. The snapshot persists across changes **within the editor session only** — it does NOT survive a page reload.

### Dynamic-tags toggle

Automated campaigns whose segment uses *Segment triggered products* can toggle **Dynamic generated tags from segment condition** — templates can reference dynamic tags resolved from segment-matched products (e.g., the abandoned-cart product). The toggle is hidden when the segment doesn't support dynamic tags. Even if ticked, the save endpoint forces the value to 0 when the segment lacks supporting conditions — see [[campaigns-edit-validation-rules]].

## Business rules

- **Action-type dropdown lists only configured + active channels.** Installed-but-unconfigured / inactive channels are absent. The merchant completes channel setup in [[marketing-channels]] first.
- **Action-type locks once a message is saved.** Delete the saved message to switch channel.
- **Regular campaigns hardcode Execute-after to Immediately.** The picker is disabled.
- **Max action steps cap** — Regular: **1**, Automated: **5**. See [[campaigns-edit-validation-rules]].
- **Deleting a step cascade-deletes downstream steps.** Confirm dialog warns explicitly.
- **Channel credit pre-check happens on Start, not on Save draft** — see [[campaigns-edit-launch-flow]].
- **Saved-email-template linkage auto-creates on save.** A step carrying a `template_id` from the [[marketing-campaigns-message-template|saved templates library]] but no `campaign_action_templates` row triggers the save endpoint to bootstrap one (name, subject, HTML, Unlayer JSON copied). If the row already exists, only `template_id` + `template_type` linkage is synced — previously-customised content is preserved. See [[campaigns-edit-validation-rules]].

## Related

- [[marketing-campaigns-edit]] — hub.
- [[marketing-campaigns-message-template]] — Email template picker + Unlayer designer.
- [[marketing-channels]] — where merchants configure channels so they appear in the dropdown here.
- [[customer-group]] — entity referenced by the `set_customer_group` action.

## Open questions

No outstanding questions.
