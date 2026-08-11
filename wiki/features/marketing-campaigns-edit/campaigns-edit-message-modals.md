---
type: feature
nav_path: "Marketing → Campaigns → Edit → Message modals"
route_name: campaigns-edit
route_path: /admin/marketing-new/campaigns/edit/:type(regular|automated)/:id
aliases: ["Viber message editor", "SMS message editor", "Web Push editor", "Campaign message settings modal", "Variables legend", "Mobile phone preview", "Write with AI", "Channel settings modal"]
tags: [marketing, campaigns, edit, messages, modals]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns-edit]]. See the hub for the other aspects (main settings, trigger, actions, conditions, exit, launch flow, validation rules).

# Edit campaign — per-channel message modals

## Purpose

Clicking **Set message** (or **Edit**) on a Step 3 action step ([[campaigns-edit-step-3-actions]]) opens a per-channel message editor modal. The modal composes the message content — body, character limits, variable pills, optional image / button, AI-generated copy — with a live mobile-phone preview.

This page covers the **SMS / Viber / Web Push** modal and the **channel settings modal**. The **Email** path uses a different modal (Unlayer designer) — documented on [[marketing-campaigns-message-template]].

## Where to find it

Inside the **Edit campaign** screen ([[marketing-campaigns-edit]]):

- **Set message** / **Edit** buttons on any Step 3 SMS / Viber / Web Push action step.
- The modal is `CcModal` size `xll`, titled *"Edit - {internal_title}"*.

## What the merchant can do here

- **Set the internal title** (admin-side label, never sent to subscribers).
- **Write the message body** with character-counted pill editor, variable pills, AI-generated copy.
- **Add an image** (Viber promo / Web Push) from the media library or by external URL.
- **Add a button** (Viber promo) with text + URL.
- **Watch the live mobile-phone preview** render the message.
- **Save** — persists the message and links it to the action step.

## Settings & fields

The modal body is a 2-column responsive layout: form fields on the left, mobile-phone preview on the right.

### Channel routing

Step 3's **Set message** / **Edit** buttons open one of two modals depending on `action_type`:

- **Email** → `CampaignEmailTemplateModal` (template picker — see [[marketing-campaigns-message-template]] for the picker + the Unlayer editor inside it).
- **SMS / Viber / Web Push** → `CampaignMessageSettingsModal` (single modal, body switches by `action_type`).

### Common section — Internal title

Always shown when `show-campaign-fields = true`:

| Field | v-model | Validation |
|-------|---------|------------|
| **Internal title** | `record.label` | `errorStore.getError('internal_title')` |

### Viber message body

| Field | Type | Limits / notes |
|-------|------|----------------|
| **Viber message text** | `CcVariablePillEditor`, multiline | Max 1000 chars per Viber business message; remaining-chars counter visible |
| **Add variable** dropdown | `CcVariableDropdown` | Inserts a `{$variable}` pill at cursor |
| **Write with AI** button | Toggle | Opens inline `CcAiPromptField` → `apiMarketingChannels.aiGenerateMessage` → returns AI-generated text. Spinner + toast on success/failure. |
| **Image** card | Storage type (`internal` / `external`) + URL input + clear-X | Visible when `allow_promo_messages = true`. `internal` opens `CcImageModal` (media library); `external` is free-text URL. Live preview. |
| **Button** card | Button text input + Button URL input | Visible when `allow_promo_messages = true`. Image + button text + button URL form a required-trio. |

### SMS message body

| Field | Limits |
|-------|--------|
| **SMS message text** (`CcVariablePillEditor`, multiline) | Max **918 chars** (153 × 6 messages); error *"Text is too long"* if exceeded |
| **Add variable** / **Write with AI** | Same as Viber |
| **Characters counter** | Live, shows `count / 918` + `messages / 6`. Warning: *"The calculated message length is approximate. When using variables, the actual length may vary significantly."* |

### Web Push body

Three stacked cards:

| Card | Field | Limits |
|------|-------|--------|
| **Web Push title** | Single-line pill editor | Title length capped; error *"Text is too long"* |
| **Web Push body** | Multiline pill editor | Body length capped |
| **Web Push icon** / **image** | Storage type + URL + media library | Same pattern as Viber image |

### Variables legend pane

Always at the bottom of the form column: a 2-column grid of `{$variable_name}` (clickable to copy, toast *"Copied to clipboard"*) + human-readable label. Variables come from `apiMarketingCampaignEmailTemplates.variables` — campaign-aware, includes dynamic-tag variables when the segment supports them (see [[campaigns-edit-step-3-actions]]).

### Mobile-phone preview pane

Right column — faux iPhone frame with channel-appropriate rendering:

- **Viber** — chat bubble + optional image figure + optional CTA button.
- **SMS** — grey chat bubble + plain text.
- **Web Push** — Chrome notification card: icon, host name, "now" timestamp, title, body, optional image.

Updates live as the merchant types.

### Save behaviour

On save:

1. Updates the action's local `internal_title` and `condition.message` (string for SMS / Viber, object for Web Push).
2. If a campaign ID exists AND `action_order` is set: calls `POST /admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/0` to persist a `campaign_action_templates` row.
3. **Success** — merges server response, sets `has_chosen_template = true`, closes modal, toasts *"Saved successfully"*.
4. **Failure** — rolls back the action's template state; surfaces error.
5. **No campaign ID yet** (brand-new unsaved campaign) — no API call, state kept local; the step still shows **Set message**.

**Save button is disabled** when any character limit is exceeded OR `isPending`.

### Channel settings modal (`MarketingChannelsSettingsModal`)

Opens from inside the per-channel message editor when the merchant tweaks runtime settings (Viber sender ID, Web Push popup text). Also reachable from [[marketing-channels]].

| Channel | Inner component |
|---------|-----------------|
| Email | `MarketingChannelsSettingsModalEmail` |
| Viber | `MarketingChannelsSettingsModalViber` |
| Web Push | `MarketingChannelsSettingsModalWebPush` |
| SMS | (no settings modal — handled on the Channels page) |

Title *"Settings - {channel name}"*; saves via `PATCH /admin/api/core/marketing/channels/settings/{type}`.

## Business rules

- **Character limits enforced client-side AND on save.** Exceeding a limit disables Save; the merchant cannot persist an overflow.
- **SMS limit is 918 chars / 6 messages.** With `{$variables}` the rendered length is unpredictable — a draft under the cap may exceed at send-time for some subscribers. The counter warning copy is precise.
- **AI-generated copy runs through the same limits.** Output lands in the pill editor; merchant can edit before saving.
- **Image + Button trio on Viber is all-or-nothing.** When `allow_promo_messages = true`, any one of (image, button text, button URL) requires the other two.
- **`internal_title` is admin-only.** Never sent to subscribers — appears on the Step-3 saved-template card and in audit logs.
- **Save without a campaign ID is local-only.** On a brand-new unsaved campaign, the modal closes successfully but no `campaign_action_templates` row is created — the message survives in memory until parent Save draft materialises it via the save cascade ([[campaigns-edit-validation-rules]]).
- **Channel settings modal persists separately from the campaign.** Changes to Viber sender ID / Web Push popup text save via `PATCH /admin/api/core/marketing/channels/settings/{type}` — not part of the campaign payload, not rolled back by the draft guard.

## Related

- [[marketing-campaigns-edit]] — hub.
- [[marketing-campaigns-message-template]] — the Email-channel equivalent (Unlayer drag-and-drop designer).
- [[marketing-channels]] — channel settings; the channel settings modal is also reachable from there.

## Open questions

- (verify) Exact character cap for Web Push title and body — the code references `isWebPushTitleCharsExceeded` and `isWebPushBodyCharsExceeded` but the precise numeric caps aren't surfaced in the editor; confirm against the channel-side validation.
