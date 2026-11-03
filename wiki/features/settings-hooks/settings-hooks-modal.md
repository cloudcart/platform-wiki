---
type: feature
nav_path: "Settings → Webhooks → Create / edit modal"
route_name: hooks.settings
route_path: /admin/settings/hooks
aliases: ["Create webhook modal", "Edit webhook modal", "Webhook form", "+ Add webhook", "Webhook bulk delete", "Webhook validation"]
tags: [settings, webhooks, modal, form, integrations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-hooks]]. See the hub for the other aspects (events, delivery, retry, auto-disable, activity log, auth & headers).

# Webhooks — create / edit modal & row controls

## Purpose

The Create / Edit modal is the only UI surface where a merchant adds, edits, or reconfigures a webhook subscription. This page covers the modal layout, every field's behaviour, the inline row controls (Active toggle, delete, click-to-edit), bulk-delete, and the server-side validation rules that reject invalid submissions.

## Where to find it

- Sidebar → Settings → **Webhooks** → **+ Add webhook** (header button) → Create modal opens.
- Sidebar → Settings → **Webhooks** → click any row's Event or Destination URL cell → Edit modal opens pre-loaded with that row.

## What the merchant can do here

In the table:

- See the **Site ID** as a chip in the page header — most webhook receivers want this for store identification.
- Click **+ Add webhook** to open the create modal.
- See the table of all defined webhooks with destination URL, event, API key reference, active status, last-used count, and per-row edit/delete actions.
- **Click a row's Event or Destination URL cell** to open the Edit modal (`SettingsWebhooksOpenEdit.vue`). URLs longer than 25 chars display truncated with `...` but the full URL is stored.
- **Toggle Active inline** (`SettingsWebhooksStatusChange.vue`) — the same toggle the merchant uses to re-enable an auto-disabled webhook ([[settings-hooks-auto-disable]]).
- **Delete a row** via the per-row delete button → confirmation prompt → toast *"Deleted successfully"*.
- **Bulk-delete** via the table's checkbox column + Delete from the bulk-action bar → POST to `/admin/api/core/settings/hooks/delete` with the array of IDs. No additional confirm modal beyond the standard "Are you sure" prompt.
- Filter, search, sort, paginate the webhooks table.

In the modal:

- Toggle **Active**, pick the **API key** + **Event**, enter the **Destination URL**, toggle the conditional **"It is used on a new structure"**, edit the **Custom headers** list (see Settings & fields).

## Settings & fields

### Modal layout

The same modal handles both create and edit modes — title flips between *"Create new Webhook"* and *"Edit Webhook"*. **Size**: `xl`. While a create/update mutation is in flight, the backdrop click is blocked (`no-close-on-backdrop` while `isCreating || isUpdating`). A loader covers the body while either the existing webhook is being fetched (edit mode) OR the event-types list is loading.

Body is built from TWO stacked cards.

### Card 1 — main fields

| Field | Control | Behaviour |
|-------|---------|-----------|
| **Active** | switch | Defaults to `1` (on) for new webhooks. Edit mode preserves saved value. Inactive webhooks stay configured but are skipped entirely at event-fire time (no queue row, no attempt). |
| **API key** | searchable async select, populated from `/admin/api/core/settings/api-keys` | Required. Tooltip: *"Please select an API key. You can create a new API key from the API Keys menu"*. The chosen key value is auto-injected as the `X-CloudCart-ApiKey` header on every delivery (see [[settings-hooks-auth-headers]]). Edit mode pre-populates the picker with the currently-linked key (merchant sees the key name immediately, not just an ID). |
| **Destination URL** | text input | Required. Tooltip: *"This is the URL where the webhook will be sent"*. Backend Zod-style URL validator enforces format. |
| **Event** | searchable select, `groups=true`, `can-clear=false` | Required. Renders the 20-event list grouped by entity. Tooltip: *"Select an action where the webhook will be executed. For example: If there is a new order, the action will execute a webhook to the URL destination"*. See [[settings-hooks-events]] for the catalogue. |
| **"It is used on a new structure"** | conditional switch | Appears ONLY when event is `order.created` OR `order.updated`. Selects v2 payload schema (default true) vs legacy v1 shape. See [[settings-hooks-events]]. |

### Card 2 — Headers editor

A key/value list with **Add header** button. Each existing row renders as two side-by-side inputs (Key + Value) + a small remove-icon button. When zero headers exist, only the **Add header** affordance shows (no column labels until at least 1 row exists, at which point a Key / Value header strip appears). See [[settings-hooks-auth-headers]] for the merge / replacement semantics and what gets sent on the wire.

### Footer

Standard save action wired to `createOrEdit`. On success → toast *"Saved successfully"*, modal closes, list refetches.

### Server-side validation

The Form Request enforces three rules on save:

- **`api_key_id`** — **required** AND must exist in the `api_keys` table (foreign-key integrity at validation time). Selecting a key that has been deleted between page load and save fails with *"Invalid API key"*. See [[settings-api-keys]].
- **`url`** — **required** AND must be a valid URL. Plain text, IP-only entries, or schemes other than http/https fail.
- **`event`** — **required** AND must be one of the **20 active supported events** (`order.deleted` is disabled at the code level — submitting it via the API is rejected even though the picker hides it). See [[settings-hooks-events]].

There is **NO validation that the destination URL is reachable BEFORE saving** — a webhook to a typo'd domain saves successfully and only fails (auto-disable) on the first delivery attempt. There is **no "test webhook" / dry-run feature** surfaced on this page.

### Inline row controls — endpoints

- **Active toggle**: `GET /admin/api/core/settings/hooks/get-status/{id}/{0|1}` → toast *"Status changed successfully"* on success; toggle visually reverts on failure.
- **Delete button**: `DELETE /admin/api/core/settings/hooks/{id}` with confirmation prompt → toast *"Deleted successfully"*.
- **Bulk delete**: `POST /admin/api/core/settings/hooks/delete` with the array of IDs.
- **Click-to-edit**: opens Edit modal with that row pre-loaded.

### What is NOT in this modal

- **No "Test webhook" / dry-run button.** Validation happens only at first delivery.
- **No activity-log viewer.** See [[settings-hooks-activity-log]] for why and what merchants can do.
- **No "duplicate webhook" action.** To create a similar webhook the merchant types it again from scratch.
- **No per-event payload preview.** The platform documents payload shapes only in [[api-webhooks]] / developer docs.

## Business rules

- **Permission gate.** Endpoint middleware is `hasApiPermission:settings,settings.hooks`. A moderator needs either the broad Settings permission or the specific Webhooks permission to view, create, edit, delete, or toggle webhooks. Permission tree is configured under [[settings-staff]].
- **One event per webhook row.** The Event picker is single-select with `can-clear=false`. To listen to multiple events the merchant creates one webhook row per event (intentional — keeps each subscription independently disable-able).
- **Toggling Active inline mid-failure clears the alert mute.** Re-enabling an auto-disabled webhook resets the alert's notification flags so future failures DO ping the merchant. See [[settings-hooks-auto-disable]].
- **CRUD on the webhook row is synchronous.** No queue lag for create / edit / delete. The actual webhook delivery is the queued / direct pipeline described in [[settings-hooks-delivery]].

## Related

- [[settings-hooks]] — hub.
- [[settings-hooks-events]] — the catalogue powering the Event picker.
- [[settings-hooks-auth-headers]] — the `X-CloudCart-ApiKey` injection + the headers editor in Card 2.
- [[settings-hooks-auto-disable]] — what triggers the inline Active toggle to flip OFF automatically.
- [[settings-hooks-activity-log]] — why there's no activity-log viewer in this modal.
- [[settings-api-keys]] — source for the API key picker; FK-blocks key deletion when a webhook is using it.
- [[settings-staff]] — moderator permission tree containing the Webhooks permission.
- [[api-webhooks]] — programmatic equivalent of this modal (same validation, same event catalogue).

## Open questions

- Confirm the maximum number of custom headers per webhook (UI allows unbounded add). (verify)
