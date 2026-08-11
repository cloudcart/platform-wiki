---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → SMS / Viber / Web Push"
route_name: admin.api.campaigns.message-template.create
route_path: /admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/{predefined?}
aliases: ["SMS editor (campaign)", "Viber editor (campaign)", "Web Push editor (campaign)", "Channel message editor", "CampaignMessageSettingsModal", "SMS NTH editor", "SMS MsgHub editor", "Редактор на SMS съобщение", "Редактор на Viber съобщение", "Редактор на Web Push"]
tags: [marketing, campaigns, message, template, sms, viber, web-push]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (Email designer, merge tags, saved + predefined, demo send, validation, save flow).

# Campaign message editor — Channel variants (SMS / Viber / Web Push)

## Purpose

For Email the merchant gets the Unlayer drag-and-drop designer (see [[message-template-email-designer]]). For **SMS / Viber / Web Push** the merchant gets a text-first editor: `CampaignMessageSettingsModal` — a thin wrapper around `MarketingChannelsSystemMessagesConfiguration` (the same component used for the per-channel system-message editor on the Channels page). This aspect documents the per-channel field shapes, the mobile-phone preview pane, the AI message-generation helper, and the character-count caps that gate the Save button.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → open a campaign → Step 3 (Campaign actions) → click **Set message** on an SMS / Viber / Web Push step in [[marketing-campaigns-edit]]. The modal opens with the channel-specific fields.

## What the merchant can do here

### Wrapper configuration

`CampaignMessageSettingsModal` passes these flags into `MarketingChannelsSystemMessagesConfiguration`:

- `emit-only: true` — save doesn't call the channels-system-message endpoint directly; instead it emits a success event the wrapper handles. See [[message-template-save-flow]].
- `show-campaign-fields: true` — shows the **Internal title** field + Viber image/button cards (which are hidden on the Channels page).
- `is-campaign: true` — context flag the inner component uses to switch some behaviour.

Modal title is *"Edit - {internal_title}"*. Body is a 2-column responsive layout (form left, preview right).

### Left column — Viber form fields

| Card | Field | Behaviour |
|------|-------|-----------|
| Internal title | `record.label` | Plain `CcInput`, error inline |
| Viber message text | `record.message` (string) | `CcVariablePillEditor`, multiline, max **1000** chars; **Add variable** dropdown + **Write with AI** button |
| Image | `record.imageURL` | Storage type select (`internal` / `external`) → `internal` makes URL read-only and exposes **Add image** which opens `CcImageModal`; live thumbnail on the right |
| Button | `record.buttonText` + `record.buttonURL` | Two `CcInput` fields |

Viber image + buttonText + buttonURL form a **required-with trio** at save time — the merchant either provides ALL THREE or NONE. Partial sets fail validation. See [[message-template-validation]] for the full rules.

### Left column — SMS form fields

| Card | Field |
|------|-------|
| Internal title | `record.label` |
| SMS message text | `record.message` (string), `CcVariablePillEditor` multiline; max **918** chars (`SMS_CHARS_PER_MESSAGE = 153` × `SMS_MAX_MESSAGES = 6`); shows live counters `Characters: N/918` + `SMS: N/6`; warning *"The calculated message length is approximate. When using variables, the actual length may vary significantly."* |

The 918-cap is an editor-side gate; the SMS NTH backend imposes no max-length at save time (chunk count is computed at provider-response time). SMS MsgHub has no channel-level validation override beyond a valid request.

### Left column — Web Push form fields

| Card | Field |
|------|-------|
| Internal title | `record.label` |
| Web Push title | `record.message.title` — `CcVariablePillEditor` single-line; max **63** chars |
| Web Push body | `record.message.body` — `CcVariablePillEditor` multiline; max **128** chars |
| Web Push icon | `record.message.icon` — storage type + URL + media library picker |
| Web Push image | `record.message.image` — same pattern |

The Web Push 63 / 128 caps are stricter than what Chrome supports — the platform enforces them for cross-browser compatibility.

### Right column — `MarketingChannelMobilePhonePreview`

A faux iPhone frame shows the message in its native rendering, updated live as the merchant types:

- **Viber:** chat bubble (cloudio-tinted bg) with logo, text, optional image figure, optional button (rounded full-width primary CTA).
- **SMS:** chat bubble (light grey bg) with logo and plain text.
- **Web Push:** Chrome browser notification card with Chrome icon, host name, "now" timestamp, title, body, and optional image.

Variable pills render as `{$variable_name}` literal strings in the preview — the substitution happens at send time per [[message-template-merge-tags]].

### AI prompt — Write with AI

Clicking **Write with AI** reveals an inline `CcAiPromptField` under the relevant editor:

- Placeholder: *"What's the message about?"*
- On submit: calls `POST /admin/api/core/marketing/channels/{mapping}/ai-generate-message` with `{prompt, field, variables}` where `field` is `'message'` for SMS / Viber, `'title'` for Web Push title, `'body'` for Web Push body.
- Loading spinner during generation.
- On success: replaces the relevant field's value with `response.text`, hides the AI prompt, toasts *"Message generated successfully"*.
- On error: toasts *"Failed to generate message. Please try again."*

### Variables legend pane

Identical layout to the Email scratch modal — bottom of the form column, 2-column grid of `{$variable}` (click-to-copy) + human-readable label. The full variables catalogue + dynamic-tag semantics lives on [[message-template-merge-tags]].

## Settings & fields

### Per-channel required fields (modern editor)

| Channel | Required fields |
|---------|-----------------|
| SMS (NTH) | Internal title, Message body (counted in 153-char segments, max 6 = 918 chars in the editor), Send-to (for demo) |
| SMS (MsgHub) | Internal title, Message body, sender ID (channel-level), Send-to (for demo) |
| Viber | Internal title, Message body (≤ 1000 chars), optional image URL, optional button title + URL (all-or-none trio), Send-to (for demo) |
| Web Push | Internal title, Title (≤ 63 chars), Body (≤ 128 chars), optional image URL, optional click URL, Send-to (for demo — test push endpoint) |

### Save button gating

The modal's **Save** button is disabled when:

- Any character-limit is exceeded (Viber 1000 / SMS 918 / Web Push title 63 / Web Push body 128), OR
- `isPending` is true (request in flight).

Full save mechanics + post-save state propagation live on [[message-template-save-flow]].

## Business rules

### Same component, two callers

`MarketingChannelsSystemMessagesConfiguration` is used in two places: the per-channel system-message editor on the Channels page AND this campaign-step editor. The wrapper distinguishes them via the `is-campaign` flag, the `show-campaign-fields` flag (which surfaces the Internal title + Viber image/button cards), and the `emit-only` flag (which redirects save away from the channels endpoint to the campaign endpoint).

### Set tags / Set customer group steps don't use this editor

`set_tags`, `remove_from_campaign`, `remove_from_campaign_and_set_tags`, `set_customer_group` — these action types have inline configuration directly on the step in [[marketing-campaigns-edit]] (tag picker, customer-group picker). The **Set message** button isn't shown for them.

### Variables resolve at send time

Variables render as literal `{$variable_name}` strings in the preview. Substitution happens inside the per-channel send job against the real recipient's data — see [[message-template-merge-tags]] for the variables catalogue and [[message-template-demo-send]] for how demos use synthetic data.

### Channel must be registered

The route 404s if the requested channel type isn't registered. This protects against orphaned action types whose channel was removed from the platform.

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[marketing-campaigns-edit]] — parent campaign editor.
- [[marketing-channels-sms-msghub]] — SMS MsgHub channel internals.
- [[marketing-channels-sms-nth]] — SMS NTH channel internals.
- [[marketing-channels-viber]] — Viber channel internals.
- [[marketing-channels-webpush]] — Web Push channel internals.

## Open questions

None.
