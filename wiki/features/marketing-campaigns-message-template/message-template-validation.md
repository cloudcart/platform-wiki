---
type: feature
nav_path: "Marketing → Campaigns → Edit → Set message → Validation"
route_name: admin.api.campaigns.message-template.create
route_path: /admin/api/core/marketing/campaigns/message/create/{campaign_id}/{action_order}/{type}/{predefined?}
aliases: ["Campaign message validation", "Channel message validators", "Per-channel validation rules", "Message validation errors", "Валидация на съобщение", "Грешки при запис на шаблон"]
tags: [marketing, campaigns, message, template, validation]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-message-template]]. See the hub for the other aspects (Email designer, channel variants, merge tags, saved + predefined, demo send, save flow).

# Campaign message editor — Validation rules

## Purpose

Every channel runs its message template through a **two-pass validation** on save (and on demo dispatch): first the field-level rules (required, max length, URL format, etc.), then a per-variable validator that scans the body for `{$variable}` occurrences and checks each one. This aspect documents the verbatim error strings, the per-channel field rules, the variable-extraction regex, and the merchant-facing implications.

## Where to find it

Validation errors surface inline on the editor (the Email scratch modal, and the message-settings modal for SMS / Viber / Web Push) next to the offending field. Nothing is saved when validation fails.

## What the merchant can do here

The merchant fixes validation errors inline: they read the per-field error message (verbatim strings tabled below), correct the offending field, and re-click **Save** (or **Send example email** for demos). The editor doesn't auto-correct; the merchant must change the body to satisfy each rule. For variable-validator errors that depend on out-of-editor setup (e.g., a `{$dynamic_discount_code}` without a linked discount), the merchant has to leave the editor, fix the campaign-level configuration, then return.

## Settings & fields

### Pass 1 — Field-level rules per channel

The platform's strict per-channel save validation rules:

**Email**

| Field | Rule | Error |
|-------|------|-------|
| `name` | Required, max 191 chars | Custom — internal title required |
| `subject` | Required, max 191 chars | Custom — *"Subject is required"* |
| `message_html` | Required; rejects base64-embedded local images (`#image/(\w+);base64#` regex) | *"Local image paste has been disabled. Local images have been removed from pasted content."* |
| `message_html` | Required (HTML missing) | *"You haven't filled all the settings!"* |

**SMS NTH**

| Field | Rule |
|-------|------|
| `internal_title` | Required, max 191 |
| `sms_nth_message` | Required, string. **No max-length validation at save time** — the chunk count is computed at provider-response time, not enforced upfront. |

The editor-side counter caps at 918 chars (`SMS_CHARS_PER_MESSAGE = 153` × `SMS_MAX_MESSAGES = 6`) and disables Save when exceeded; the **backend** doesn't enforce this. Pasting beyond 918 via API bypasses the cap. (verify the API path)

**SMS MsgHub**

No channel-level validation override (uses abstract base). Validation effectively just requires the request to be valid.

**Viber**

| Field | Rule |
|-------|------|
| `internal_title` | Required, max 191 |
| `viber_message` | Required, max **1000** chars (`MAX_MESSAGE_LENGTH = 1000`) |
| `imageURL` | Required-with `buttonText, buttonURL`; max 1000 chars; URL format |
| `buttonURL` | Required-with `imageURL, buttonText`; max 1000 chars; URL format |
| `buttonText` | Required-with `imageURL, buttonURL`; max **30** chars |

**The required-with trio**: the merchant either provides ALL THREE (image + button URL + button text) OR provides none of them — partial sets fail validation. The Viber business-message protocol requires the button-card to be complete.

**Web Push**

| Field | Rule |
|-------|------|
| `internal_title` | Required, max 191 (unless on the system-message edit path, where it's optional) |
| `web_push.title` | Required, max **63** chars |
| `web_push.body` | Required, max **128** chars |

The Web Push limits (63 / 128) are stricter than typical browser implementations — Chrome supports longer titles / bodies, but the platform enforces these caps for cross-browser compatibility.

### Pass 2 — Variable validation

The second pass scans the message body to extract every `{$variable_name}` and `{$variable:argument}` occurrence, then validates each one individually.

Examples of variable-validator failures:

- `{$generate_discount_code:25%}` references a discount setup the merchant hasn't created → fails with a per-variable validation error.
- `{$dynamic_discount_code}` without a linked discount on the campaign → fails.
- Variables that depend on segment context (e.g., `{$triggered_products:N}`) without the right segment type on the campaign → may fail or resolve to empty at send time. (verify)

Full variables catalogue + the dynamic-discount semantics live on [[message-template-merge-tags]].

### Common validation table

| Validation | Channel | Message |
|-----------|---------|---------|
| Empty message body | All | *"Empty message text"* |
| Body exceeds max length | All | *"The message is longer than:max symbol"* |
| Subject missing | Email | Custom error — Subject is required |
| HTML missing | Email | *"You haven't filled all the settings!"* |
| Invalid send-to (demo) | All | Per-channel validation message |

## Business rules

### Two passes, two distinct failure modes

A save can fail for two distinct reasons:

1. **Malformed body fields** — pass-1 error (required missing, max-length exceeded, URL format invalid, etc.).
2. **Un-resolvable variable references** — pass-2 error (variable references a discount that doesn't exist, etc.).

Both surface inline in the editor next to the relevant field; the merchant has to fix both before save succeeds.

### Save button gating on the editor

The modal's **Save** button is disabled while any character-limit is exceeded (Viber 1000 / SMS 918 / Web Push title 63 / Web Push body 128) or while a save is already in progress. This prevents the merchant from even attempting a server-rejected save. Demos use the same gating.

### Editor caps vs backend caps differ for SMS NTH

The editor caps SMS NTH at 918 chars and disables Save when exceeded, but the backend `sms_nth_message` rule has no max-length. A longer message would pass the server if it ever reached it; the editor gate prevents that path in normal UI use, and the real limit surfaces only at provider-response time as a chunk count.

### Local image rejection is a spam-trigger / size protection

The Email `message_html` rule rejects base64-embedded local images. Inline base64 images bloat HTML size and trip spam filters. The merchant must upload images to the media library (served from a CDN URL) before referencing them in Email HTML.

### Tampered saved-template links are silently dropped

If a save references a saved template (`template_id` + `template_type`) that can't be loaded or is of an unrecognised type, the save skips the link and persists the template without a saved-template reference. No error surfaces — see [[message-template-saved-and-predefined]].

### Anti-spam policy gate runs before validation

The campaign anti-spam policy gate is checked **before** the editor even opens for an unaccepted merchant. So validation rules only matter once the merchant has accepted the policy. See [[marketing-campaigns-edit]].

### Variable validation scans recursively into all body fields

The body scan applies to whatever field carries the message text per channel: `message_html` for Email, `viber_message` for Viber, `sms_nth_message` for SMS NTH, `web_push.title` + `web_push.body` for Web Push. So a `{$dynamic_discount_code}` typo in the Web Push title still triggers the per-variable validator.

## Related

- [[marketing-campaigns-message-template]] — hub.
- [[message-template-merge-tags]] — variables catalogue + the per-variable validator semantics.
- [[message-template-saved-and-predefined]] — saved-template link verification at save time.
- [[message-template-save-flow]] — the wider save handler that runs these passes.
- [[marketing-channels-email]] / [[marketing-channels-sms-nth]] / [[marketing-channels-sms-msghub]] / [[marketing-channels-viber]] / [[marketing-channels-webpush]] — per-channel send pipelines.

## Open questions

- Does an SMS NTH save via API (bypassing the editor cap) actually accept a >918-char body? Backend rule says yes, behaviour at provider-response time needs verification.
- For dynamic-tag variables like `{$triggered_products:N}` on a campaign with the wrong segment type — does the variable-validator block at save time, or does it silently resolve to empty at send time?
