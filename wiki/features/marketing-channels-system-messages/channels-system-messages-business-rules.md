---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Business rules"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["System messages business rules", "Template status switch", "Language fallback for templates", "Anti-spam policy gate", "Channel active gate"]
tags: [marketing, channels, system-messages, business-rules, language-fallback]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (catalog, editor, variables, validation, counters, AI assist).

# System messages — business rules

## Purpose

The cross-cutting platform rules that govern when system messages actually go out, what happens on save, how the language fallback behaves, and what gates the merchant has to clear before they can even open the modal.

## Where to find it

These rules are not a screen of their own — they govern the System messages outer list ([[channels-system-messages-catalog]]) and the per-template editor ([[channels-system-messages-editor]]) reachable from sidebar -> **Marketing** -> **Channels** -> **Channels setup** -> Viber / Web Push card -> **System messages**.

## What the merchant can do here

- **Toggle a template ON / OFF** with the status switch (immediate effect on the next event firing).
- **Save** an edited template (atomic per template).
- **Pick the language** by switching the store-wide language setting — the modal then serves templates in that language with silent English fallback.
- **Accept the anti-spam policy** when first opening the channels page (redirect-gated; see [[marketing-campaigns-policy]]).
- The merchant **cannot** bulk-toggle from the UI (the bulk endpoint exists but is unexposed — see [[channels-system-messages-counters]]).

## Settings & fields

The rules here govern interactions with the status switch (binary ON / OFF; no draft state) and the Save action — see field-level validation rules on [[channels-system-messages-fields-validation]]. There are no merchant-settable fields specific to "business rules"; the rules describe how existing fields behave on the larger surface.

## Where it applies

Across the System messages outer list ([[channels-system-messages-catalog]]) and the per-template editor ([[channels-system-messages-editor]]).

## Business rules

### Status switch — ON / OFF, not draft / published

The status switch in the list is a simple binary:

- **ON** (status = 1) — when the event fires, the platform looks up this template and dispatches a send.
- **OFF** (status = 0) — when the event fires, the platform skips this template. **No log row is written** in [[marketing-channels-logs]], and no plan-cap counter is incremented.

Toggling fires an inline switch update — the row's loader spinner appears while the PATCH is in flight, the toggle keeps its visual position, and on success the platform fires toast *"Status updated successfully"*. On error the loader clears without a toast.

### Per-event uniqueness — one template per event per channel per language

Each `(channel, language, event)` combination has exactly one template row. The merchant edits that one row's content; there is no "duplicate template" or "A/B test template" support.

### Language fallback is automatic — no UI prompt

When the modal opens, the backend checks whether any system-message template exists in the store's current language (`site('language')`). If NO templates exist for that language, the platform silently falls back to `config('app.fallback_locale')` (typically English) and serves those templates.

Consequences:

- The merchant sees the fallback rows as normal editable rows — there is **no banner** explaining *"you're editing the English fallback because Bulgarian templates haven't been seeded yet"*.
- Edits made under the fallback save against the fallback-locale row.
- If the merchant later switches the store language back to the original, edits made under the fallback **will not appear** — they belong to the fallback's row.

### Save is atomic per template

The Save button calls the per-channel update endpoint with the template id + the channel mapping. The response is either:

- **Success** — `{status: 'success', msg: 'Saved successfully'}` — toast *"Saved successfully"*, modal closes, the list refreshes the updated row (label / send-count / status).
- **Validation error** — `{status: 'error', msg: '...'}` — toast *"Error saving message. Please check the fields and try again."* — modal stays open. The error store populates per-field errors (e.g., `web_push.title` is too long). See [[channels-system-messages-fields-validation]].

### Channel must be installed + active to send

A System message template that's toggled ON, on a channel that's NOT installed or NOT active, will not send anything when its event fires. The platform short-circuits the dispatch **before** reaching the template lookup. The merchant should ensure the channel is installed + activated on [[marketing-channels]] before toggling templates ON.

### Anti-spam policy gate

The parent channels page enforces the [[marketing-campaigns-policy|anti-spam policy]] acceptance before any of its modals (including System messages) can open. A merchant who hasn't accepted the policy is redirected to `/admin/marketing-new/campaigns/policy` before they can see the channels list.

### Mapping normalization — dash and underscore both accepted

Verified: the API endpoint accepts the channel `mapping` in either `viber-message` or `viber_message` form (and `web-push` / `web_push`). The controller normalizes the mapping internally — first checking the original, then converting dashes to underscores, then underscores to dashes. So both URL formats land on the same per-channel templates list.

### System messages are not campaigns

System messages are **not** campaigns. They are not triggered by segment matching, they are not scheduled, and they go out one-per-event when the event fires. The variable legend, the cap accounting, and the editor's available fields all differ from campaigns. The catalog of events is fixed (see [[channels-system-messages-catalog]]) — for custom triggers, the merchant must use campaigns instead.

### Plan-cap awareness

System messages still count toward the channel's overall plan cap (verify) — but the per-template send-counter shown in the list is informational, NOT a plan-cap counter. See [[channels-system-messages-counters]] for the counter semantics.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[channels-system-messages-catalog]] — fixed event list per channel.
- [[channels-system-messages-editor]] — the editor that hosts Save validation.
- [[channels-system-messages-fields-validation]] — the per-field rules surfaced as inline errors here.
- [[channels-system-messages-counters]] — sent-count behaviour + the bulk-status endpoint.
- [[marketing-channels]] — channel install + activation.
- [[marketing-campaigns-policy]] — anti-spam policy gate.
- [[marketing-channels-logs]] — where actual sends are logged; OFF templates don't write here.

## Open questions

- Whether system-message sends count against the channel's plan-cap counter or are exempt — marked (verify).
