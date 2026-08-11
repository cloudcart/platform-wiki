---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["System messages", "Channel system messages", "Transactional templates", "Per-channel system messages", "Системни съобщения", "Системни шаблони", "Транзакционни съобщения за канал"]
tags: [marketing, channels, system-messages, transactional, templates]
plan_gates: ["viber_messages", "campaign.channel.web_push"]
created: 2026-05-23
updated: 2026-06-10
source_count: 3
---
# Channel system messages

## Purpose

The **Channel system messages** modal lets the merchant manage the platform's per-event **transactional templates** for a given channel — the short message that fires automatically when something happens in the store: a customer registers, an order is placed, a payment confirms, an order status changes, an order is fulfilled.

System messages are **not** campaigns. They are not triggered by segment matching, they are not scheduled, and they go out one-per-event when the event fires. The merchant configures the **content** of each event template — the text body for Viber and SMS-style channels, the title + body + icon + image for Web Push.

This modal is only exposed on the **Viber** and **Web Push** channel cards. Email's transactional templates live separately under [[marketing-omnichannel-mails-list|Email notifications]]; the two SMS channels (MsgHub + NTH Mobile) don't have per-event system messages at the channels-page level (they are pure marketing pipes used by campaigns only).

## Where to find it

Sidebar -> **Marketing** -> **Channels** -> **Channels setup** -> click the **Viber** or **Web Push** card -> click **System messages**. The modal opens over the channels list — it does not have its own route. The parent route is `/admin/marketing-new/campaigns/channels`. Modal title is built dynamically: *"System messages - {Channel Name}"*.

## What the merchant can do here

At hub level, the modal lets the merchant browse the per-channel template catalog, toggle each template ON / OFF, click into the editor for any template, and see the lifetime send-count beside each row. The detailed actions and surfaces are documented per aspect — see [[channels-system-messages-catalog]] (catalog + status switch), [[channels-system-messages-editor]] (editor surface), [[channels-system-messages-ai-assist]] (Write with AI), and [[channels-system-messages-counters]] (send counters + bulk endpoint).

## Settings & fields

Per-channel field schemas and validation rules differ enough to live on a dedicated aspect — see [[channels-system-messages-fields-validation]] for the full table (Viber 1000-char message + promo image + promo button; Web Push 63-char title + 128-char body + icon + image; SMS NTH 918-char multi-part text; storage-selector Internal CDN vs External URL). Variables available per channel are catalogued on [[channels-system-messages-variables]].

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[channels-system-messages-catalog]] — channel applicability (Viber / Web Push / Email / SMS); the fixed event catalog (Viber 7 templates, Web Push 2); event keys + default titles + default bodies.
- [[channels-system-messages-editor]] — the two-stacked-modals UI; outer list + nested per-template editor; two-column layout (content left + live mobile-phone preview right); save flow + outer-list refresh.
- [[channels-system-messages-variables]] — the merge-tag legend per channel; transactional vs marketing variable sets; the pills-protect-tags rule; the cross-channel `web_push.variables.patterns` quirk.
- [[channels-system-messages-fields-validation]] — per-channel field schema; Viber 1000-char text + promo image + promo button; Web Push 63-char title + 128-char body + icon + image; SMS NTH 918-char multi-part text; storage-selector (Internal CDN vs External URL).
- [[channels-system-messages-business-rules]] — status switch ON/OFF (no log row when OFF); per-event uniqueness; language fallback to English with no UI prompt; channel-must-be-installed gate; anti-spam policy gate; mapping normalization (dash vs underscore).
- [[channels-system-messages-counters]] — *"Send messages (N)"* unique-subscriber-per-event aggregation; lifetime cumulative; per-row vs full-list refresh; bulk-status endpoint that's not exposed in UI.
- [[channels-system-messages-ai-assist]] — Write with AI flow (Cloudio `MINI_MODEL` at temperature 0.7); channel + industry + variables passed in; per-channel hard-trim to char limit; failure-mode surfacing.

## Why it matters to the merchant

- **System messages are how the store talks to customers about their orders.** Order-placed receipts, payment confirmations, fulfillment dispatch notices — these are not marketing; they are operational touch-points. A misconfigured or OFF template means the customer hears nothing when their order moves through the pipeline.
- **The catalog is fixed.** The merchant cannot add a custom event template like *"Trigger when subscriber abandons cart"* — those use campaigns. The 7 Viber + 2 Web Push templates are what the platform exposes; see [[channels-system-messages-catalog]].
- **Language fallback is silent.** A Bulgarian-language store with no Bulgarian seed gets the English fallback templates served as if they were native — without a banner. Edits then save against the fallback's row, not the missing language row. See [[channels-system-messages-business-rules]].
- **OFF doesn't log.** When a template is OFF, the event firing leaves no trace in [[marketing-channels-logs]] — the merchant cannot retroactively see *"this would have sent if it were ON"*. See [[channels-system-messages-business-rules]].
- **Counters under-count repeat customers.** *"Send messages (N)"* counts unique subscribers per event, not raw sends — a 1000-fire template to 200 customers shows ~200. See [[channels-system-messages-counters]].

## Channels that expose System messages

- **Viber** — `viber_message` mapping. 7 templates. Modal title: *"System messages - Viber Message"*.
- **Web Push** — `web_push` mapping. 2 templates. Modal title: *"System messages - Web Push"*.
- **Email** — does NOT expose System messages here. Use [[marketing-omnichannel-mails-list]] instead.
- **SMS MsgHub** — campaign-only.
- **SMS NTH** — campaign-only at the channels-page level. The same edit modal is reachable through the campaign editor and some legacy contexts (`sms_nth_message` mapping).

## Scope

What this cluster covers (across the 7 sub-pages):

- The event catalog per channel + default content.
- The two-modal editor UI + live preview.
- Variable legend semantics.
- Field schema + char-limit + image-storage validation.
- Status switch + language fallback + policy / channel-active gates.
- Send-counter aggregation + bulk-status endpoint.
- Cloudio-powered AI generation.

What it does NOT cover:

- Email transactional templates — see [[marketing-omnichannel-mails-list]].
- Campaign authoring (segment matching, scheduling, plan caps) — see [[marketing-campaigns]].
- Channel installation / activation flows — see [[marketing-channels]].
- The anti-spam policy itself — see [[marketing-campaigns-policy]].

## Business rules

The cross-cutting rules — status switch ON/OFF, per-event uniqueness, silent language fallback, channel-must-be-installed gate, anti-spam policy gate, mapping normalization (dash vs underscore) — live in [[channels-system-messages-business-rules]]. The counter aggregation (unique-subscriber-per-event, lifetime cumulative, OFF templates don't increment) lives in [[channels-system-messages-counters]].

## Related

- [[marketing-channels]] — parent channels hub. System messages is one of the modals reachable from each channel card (Viber / Web Push only).
- [[marketing-channels-logs]] — Channel logs modal; system-message sends appear here with Type = *"System message"* and the event label.
- [[marketing-channels-email]] — Email channel reference. Email's transactional templates live under [[marketing-omnichannel-mails-list]] instead.
- [[marketing-channels-sms-msghub]] — SMS via MsgHub. Campaign-only — no system messages.
- [[marketing-channels-sms-nth]] — SMS via NTH Mobile. Campaign-only at channels-page level.
- [[marketing-channels-viber]] — Viber channel reference; owns 7 system-message templates and the `allow_promo_messages` flag.
- [[marketing-channels-webpush]] — Web Push channel reference; owns 2 system-message templates.
- [[marketing-omnichannel-mails-list]] — Email's transactional notifications (parallel concept for Email).
- [[marketing-campaigns]] — campaigns use a different (smaller) variable legend even on the same channels.
- [[marketing-campaigns-policy]] — anti-spam policy gate that must be accepted before opening any channels modal.
- [[notification-delivery]] — outbound delivery concept.

## Open questions

- Whether system-message sends count against the channel's plan-cap counter or are exempt — tracked on [[channels-system-messages-business-rules]] and [[channels-system-messages-counters]] as (verify).
- AI-assist SMS cap is documented as 160 chars while the SMS NTH field allows 918 chars (multi-part); confirm against backend — tracked on [[channels-system-messages-ai-assist]] and [[channels-system-messages-fields-validation]] as (verify).
