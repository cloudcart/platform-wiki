---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → System messages"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber system messages", "Viber templates", "Viber transactional messages", "Viber per-event templates", "viber_system_messages", "Viber editor image button"]
tags: [marketing, channels, viber, system-messages, templates]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (settings, self-credentials, send pipeline, DLR, plan cap, message format).

# Viber channel — System messages

## Purpose

**System messages** are the merchant-editable transactional Viber templates fired by internal platform events (order placed, password reset, payment confirmed, etc.) — distinct from Campaign-driven sends. The Viber channel maintains its own per-language template list and tracks per-template send counts. Editing rules and the Viber-specific editor variants are documented here; the cross-channel editor shell is in [[marketing-channels-system-messages]].

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → **Viber** card → **System messages** button. Title: *"System messages - Viber Message"*. The outer modal is `MarketingChannelsSystemMessagesModal`. Clicking a template label opens the nested editor (`MarketingChannelsSystemMessagesConfiguration`) — see [[channels-system-messages-editor]] for the editor mechanics common to all channels.

## What the merchant can do here

- See the list of 7 Viber transactional templates with their per-template `sent_count` *"Send messages (**N**)"*.
- Toggle each template on/off via a per-row switch (PATCHes `status` on the message).
- Click a template label to open the nested editor and edit the message body, image (if promo-enabled), and button (if promo-enabled).
- Use the **Write with AI** assist to generate a draft message from a short prompt.

## Settings & fields

### The 7 Viber system-message events

| Event key | Fires on |
|-----------|----------|
| `customer_create` | New customer account is created. |
| `customer_forgot_password` | Customer requests a password reset. |
| `cash_on_delivery` | Order placed with COD payment method. |
| `bank_wire_transfer` | Order placed with bank-wire payment method. |
| `credit_card` | Order placed with credit-card payment method (successful). |
| `order_status_change` | Order's status changes (cancel, refund, etc.). |
| `order_status_fulfillment_change` | Fulfillment status changes (shipped, delivered, etc.). |

The list is restricted at runtime to rows with a non-empty event for the current site language, with fallback to the platform default if no rows exist for that language. See [[channels-system-messages-catalog]] for the catalog reference shared across channels.

### Viber-specific editor fields

The nested editor is the shared `MarketingChannelsSystemMessagesConfiguration` component, but it shows additional fields for Viber:

- **Message text** — variable-aware pill editor; max 1000 chars; live remaining-character counter; merge-tags via **Add variable** dropdown.
- **Write with AI** — short prompt → generated message; see [[channels-system-messages-ai-assist]].
- **Live mobile-phone preview** on the right with the Viber-style chat bubble.
- **Image card** *(only when `allow_promo_messages = true`)* — storage picker (internal CDN vs external URL), image URL field with delete X, internal-gallery picker via `CcImageModal`, 80×80 preview.
- **Button card** *(only when `allow_promo_messages = true`)* — button text + button URL inputs.

Without the `allow_promo_messages` flag (i.e., for most merchants), only the message-text field is editable. See [[viber-channel-settings]] for the flag's provisioning.

### Per-language template fallback

`getSystemMessages` queries the `viber_system_messages` table for rows matching the current site's language. If no rows exist for that language, it falls back to `config('app.fallback_locale')`. The list is ordered by `title`.

## Business rules

### System messages are SEPARATE from campaign messages

System messages are fired by platform events — the merchant does not "send" them from a campaign editor. They share the channel's send pipeline (see [[viber-channel-send-pipeline]]) and DLR pipeline (see [[viber-channel-dlr-status]]) but their authoring surface is this modal, not the campaign editor.

A merchant who wants to send a marketing-style Viber message uses the campaign editor's **"Viber message"** action type instead — see [[marketing-campaigns]].

### Per-template counter increments on DLR success

Each Viber system message tracks its `sent_count` — incremented when a DLR moves the log row to `DELIVERED`, `SENT`, `SEEN`, or `CLICKED`. Failures (`REJECTED`, `UNDELIVERED`, `EXPIRED`, `NOT_SENT`) don't increment the counter. The counter is shown in the outer list as *"Send messages (**N**)"*.

### Image + Button cards are gated on the merchant's contract

The `allow_promo_messages` flag is server-computed (currently isZora OR `site_id 30585`) `(verify — special-client carve-out)`. Without it, the editor shows only the message-text field even though the underlying campaign-editor template format supports image / button. This matches the InfoBip-side service-vs-promo routing — see [[viber-channel-send-pipeline]].

### Per-row toggle PATCH

Toggling a row on/off PATCHes `status` on the message. The row shows a per-row loader during the request. Status updates are reflected in the per-row switch on success.

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-settings]] — `allow_promo_messages` is the flag that unlocks image + button cards.
- [[viber-channel-send-pipeline]] — system-message sends use the same dispatch + retry pipeline as campaign sends.
- [[viber-channel-dlr-status]] — DLR events drive `sent_count` increments per template.
- [[marketing-channels-system-messages]] — cross-channel system-messages hub.
- [[channels-system-messages-editor]] — the nested editor's shared layout.
- [[channels-system-messages-catalog]] — the per-channel event catalog reference.
- [[channels-system-messages-ai-assist]] — AI-generated message drafts.

## Open questions

- Does the per-row toggle's `status` PATCH also fire any audit / history event? `(verify)`
- Are the 7 event keys language-agnostic, or does the merchant need to re-create the row for each language? The fallback rule above suggests language-agnostic — `(verify)`.
