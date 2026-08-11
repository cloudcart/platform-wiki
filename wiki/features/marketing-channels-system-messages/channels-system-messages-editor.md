---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Editor"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["System message editor", "Template editor", "Per-template configuration modal", "Channel template editor"]
tags: [marketing, channels, system-messages, editor, preview]
plan_gates: ["viber_messages", "campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (catalog, variables, validation, business rules, counters, AI assist).

# System messages — editor (per-template configuration)

## Purpose

The **nested editor modal** that opens when the merchant clicks a template label in the outer System messages list. It is where the actual message content gets typed, previewed, and saved. The same component is shared across channels — its UI branches on the channel mapping (`viber_message` / `web_push` / `sms_nth_message`).

## Where to find it

Sidebar -> **Marketing** -> **Channels** -> **Channels setup** -> click **Viber** or **Web Push** card -> click **System messages** -> click a template label. Title: *"Edit - {template label}"*.

The outer list modal is sized `xll` (extra-large); when the nested editor opens it expands to `full`.

## What the merchant can do here

- **Edit the message body** in a variable-aware pill editor — typed variables become coloured pills that can't be accidentally split into broken fragments.
- **Insert variables** via the **Add variable** dropdown — searchable list with placeholder *"Search"*, group title *"Variables"*, empty-text *"No variables found"*. Available merge tags depend on channel + context (see [[channels-system-messages-variables]]).
- **Generate text with AI** via the **Write with AI** button (see [[channels-system-messages-ai-assist]]).
- **Preview the result** live on a mobile-phone mock that re-renders as the merchant types.
- **Save** the template — runs validation, persists, fires *"Saved successfully"* toast, closes the editor, refreshes the affected row in the outer list.

## Layout — two columns

### Left column (scrollable, max-height `calc(100dvh - 11rem)`)

The content editor varies by channel:

**Viber templates** (`channel.mapping = viber_message`):

- **Viber message text** card — multiline variable-pill editor for the body (max 1000 chars; remaining-chars counter below). Above the editor: **Add variable** dropdown + **Write with AI** button (Cloudio variant).
- **Image** card — only shown when `showCampaignFields = true` AND `allow_promo_messages = true` on the Viber channel. Storage-type select (Internal / External), Image URL input (read-only when Internal), clear (X) button, **Add image** link opening `CcImageModal`, 10x10rem preview tile.
- **Button** card — only shown under the same promo-mode flag. Button text input + Button URL input (placeholder `https://`).
- **Internal title** card (only in campaign-action edit context, not in System messages) — sits at the top of the column.

**Web Push templates** (`channel.mapping = web_push`):

- **Web Push title** card — single-line pill editor (max 63 chars, remaining counter), Add variable + Write with AI.
- **Web Push body** card — multiline pill editor (max 128 chars, remaining counter), Add variable + Write with AI.
- **Web Push icon** card — storage type select (Internal / External), URL input, clear X, **Add image** link, preview.
- **Web Push image** card — same controls as icon, separate URL field.

**SMS NTH templates** (`channel.mapping = sms_nth_message`, only in campaign-action context) — see [[channels-system-messages-fields-validation]] for the SMS-specific char + SMS-part counter.

Below the content editor sits the **Variables legend** — 2-column grid; each variable name is a clickable link that copies it to clipboard.

## Settings & fields

The editor's per-channel field set is documented in [[channels-system-messages-fields-validation]] (Viber text + promo image + promo button; Web Push title + body + icon + image; SMS NTH text + char/SMS counter). The Add-variable dropdown's contents are documented in [[channels-system-messages-variables]]. AI prompt-field behaviour is documented in [[channels-system-messages-ai-assist]].

### Right column — live mobile-phone preview

`MarketingChannelMobilePhonePreview` re-renders in real time as the merchant types. Per channel:

- **Viber**: chat-bubble with the message body + optional image + action button (when promo mode is on).
- **Web Push**: Chrome-style notification card with title + body + icon + image + host + *"now"* timestamp.
- **SMS**: simple phone chat-bubble.

The preview shows raw variable pills (`{$customer_first_name}`); the real recipient's data is only substituted at send time — there is no "preview as a specific subscriber" feature.

## Save and validation

The **Save** button is disabled when any character cap is exceeded OR when `isPending` is true. On click, the editor calls the per-channel update endpoint with the template id and the channel mapping. The response is either:

- **Success** — toast *"Saved successfully"*, modal closes, the outer list's affected row refreshes (label / send-count / status). The rest of the list keeps its state.
- **Validation error** — toast *"Error saving message. Please check the fields and try again."* — modal stays open. Per-field errors populate via `errorStore.getError(field)` and display inline.

See [[channels-system-messages-fields-validation]] for the per-field validation rules.

## Business rules

### Save is atomic per template

Each save call updates one template row's content + status. There is no "save all" button. Toggling another template's switch is a separate request (see [[channels-system-messages-counters]]).

### Editor is shared across channels — UI branches on `channel.mapping`

The same component handles Viber, Web Push, and SMS NTH editing — the rendered cards switch on the channel mapping. This is why the variables dropdown can show variables that don't strictly apply (see [[channels-system-messages-variables]] for the cross-channel quirk).

### Closing the editor on success preserves outer list state

After Save, the editor closes and ONLY the affected row reloads — the outer list does not refresh in full. Counters and labels for un-edited rows stay at their value from the last list-open.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[channels-system-messages-catalog]] — what templates exist per channel.
- [[channels-system-messages-variables]] — the merge-tag legend the editor exposes.
- [[channels-system-messages-fields-validation]] — char limits + per-channel validation rules.
- [[channels-system-messages-ai-assist]] — Write with AI flow.
- [[channels-system-messages-business-rules]] — status switch, language fallback, channel-active gate.
- [[marketing-channels-viber]] — `allow_promo_messages` flag that unlocks Image + Button cards.
- [[marketing-channels-webpush]] — Web Push channel reference.

## Open questions

None.
