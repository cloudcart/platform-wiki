---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Fields & validation"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["System message fields", "Channel template fields", "Character limits", "Per-channel validation", "Template validation rules"]
tags: [marketing, channels, system-messages, validation, fields]
plan_gates: ["viber_messages", "campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (catalog, editor, variables, business rules, counters, AI assist).

# System messages — fields and validation

## Purpose

The per-channel field schema each system-message template editor exposes — what the merchant types into, what the maximum length is, and which validation rules apply both client-side (Save button disabled, inline error) and server-side (422 with per-field error).

## Where to find it

Inside the editor modal (see [[channels-system-messages-editor]]) for any system-message template.

## What the merchant can do here

- **Type into each per-channel field** within its character cap; a remaining-chars counter sits below the editor and disables Save when the cap is exceeded.
- **Pick a storage type** for image fields (Internal CDN picker vs External URL paste).
- **Clear** an image field with the X button; **add** one via the Add-image link.
- **Receive inline server-side errors** under each field on save failure (modal stays open).

## Settings & fields

### Editor fields — Viber template

| Field | Type | Limit | Validation |
|-------|------|-------|------------|
| Viber message text | Multi-line text with variable pills | **1000 chars** | Required. Exceeding shows *"Text is too long"* in the editor; Save is disabled. |
| Image | Image URL (internal CDN picker or external URL) | — | Only available when `allow_promo_messages = true` on the Viber channel. |
| Button text | Single-line text | — | Only available when `allow_promo_messages = true`. |
| Button URL | URL | — | Only available when `allow_promo_messages = true`. Placeholder `https://`. |

### Editor fields — Web Push template

| Field | Type | Limit | Validation |
|-------|------|-------|------------|
| Web Push title | Single-line text with variable pills | **63 chars** | Required. Exceeding shows *"Text is too long"*; Save is disabled. |
| Web Push body | Multi-line text with variable pills | **128 chars** | Required. Exceeding shows *"Text is too long"*; Save is disabled. |
| Web Push icon | Image (internal CDN picker or external URL) | — | The small corner icon in the Chrome notification. |
| Web Push image | Image (internal CDN picker or external URL) | — | The larger hero image inside the notification card. |

### Editor fields — SMS template (NTH Mobile)

SMS NTH does not expose a per-event system-messages list at the channels-page level. The same edit modal is reachable through the campaign editor and some legacy contexts. Limits:

| Field | Type | Limit | Validation |
|-------|------|-------|------------|
| SMS message text | Multi-line text with variable pills | **918 chars total** (153 chars × 6 messages — multi-part SMS) | Plus a message-count meter showing *"Characters: N/918"* and *"SMS: M/6"*. Warning displayed: *"The calculated message length is approximate. When using variables, the actual length may vary significantly."* |

## Validation summary

Each template's save route enforces:

- **Viber message** (`viber_message`): required string, max 1000 chars.
- **Web Push title** (`web_push.title`): required string, max 63 chars.
- **Web Push body** (`web_push.body`): required string, max 128 chars.
- **Web Push icon / image**: optional string, must be a URL when provided.
- **SMS NTH message** (`sms_nth_message`): required string (no max enforced server-side; NTH handles concatenation).

## Storage-selector behaviour (icon / image fields)

For Web Push icon, Web Push image, and the Viber promo-message image, the merchant picks a storage type:

- **From internal storage** — opens the platform image-library picker; the chosen image is hosted on CloudCart's CDN.
- **From external source** — the merchant pastes any public URL.

When **Internal** is picked, the URL input is read-only — the merchant changes the image via the **Add image** link only. When **External** is picked, the URL input is editable. The X (clear) button resets the field.

## Business rules

### Client-side blocks Save; server-side returns 422

The editor blocks Save whenever any field is over its limit (client-side). If the limit is bypassed (e.g., direct API call), the server re-validates and returns a 422 with per-field errors. Both layers display inline error messages via `errorStore.getError(field)`.

### Promotional Viber messages need a separate plan flag

For Viber templates, the editor only exposes the **image + button** cards when `allow_promo_messages = true` on the Viber channel. This is provisioned by CloudCart based on the merchant's Viber Business contract — promotional Viber sends are typically priced differently from service Viber sends. Without the flag, only the message-text field is editable. See [[marketing-channels-viber]].

### Per-channel max chars feed back into AI assist

The AI assist (see [[channels-system-messages-ai-assist]]) is told the channel's character limit and hard-trims its output to fit: Viber 1000, SMS 160 *(verify — note `MINI_MODEL` AI cap differs from the 918 multi-part SMS field limit)*, Web Push title 63, Web Push body 128.

### Modal stays open on validation failure

When server-side validation fails, the editor stays open so the merchant can fix the offending field. Only successful saves close the editor. See [[channels-system-messages-editor]] for the save flow.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[channels-system-messages-editor]] — the editor surface that hosts these fields.
- [[channels-system-messages-variables]] — variables inserted inside these fields as pills.
- [[channels-system-messages-ai-assist]] — AI generation respects these limits.
- [[marketing-channels-viber]] — `allow_promo_messages` provisioning.
- [[marketing-channels-webpush]] — Web Push channel reference.
- [[marketing-channels-sms-nth]] — SMS NTH channel reference; campaign-only at channels-page level.

## Open questions

- AI-assist SMS cap is documented as 160 chars while the SMS field allows 918 chars (6-part); confirm whether AI text is trimmed to single-part SMS specifically or to the 918 multi-part total. Marked (verify) in the AI-assist aspect.
