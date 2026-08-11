---
type: feature
nav_path: "Marketing → Channels → Channels setup → System messages → Send counters"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Send count", "Sent counter", "Send messages counter", "Bulk status update", "System messages send aggregation"]
tags: [marketing, channels, system-messages, counters, statistics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-system-messages]]. See the hub for the other aspects (catalog, editor, variables, validation, business rules, AI assist).

# System messages — send counters and bulk operations

## Purpose

The lifetime send-count shown next to each system-message template in the outer list, and the (unexposed-in-UI) bulk-status endpoint that lets external integrations toggle many templates at once.

## Where to find it

In the outer System messages list ([[channels-system-messages-catalog]]) — the middle column on each row reads *"Send messages (**N**)"*, where N is the lifetime cumulative count from the channel-statistics aggregation.

## What the merchant can do here

- **Read the lifetime send-count** per template — informational only.
- **Toggle the status switch** to ON / OFF (the per-row update triggers the row's refresh of label + send-count + status).
- The merchant **cannot** reset, filter, or date-range the counter from the UI.
- The merchant **cannot** bulk-toggle status from the UI — the endpoint exists (`POST.../system-messages/update-statuses`) and is reachable by external integrations.

## Settings & fields

The counter is **read-only** — there are no merchant-settable fields here. The single interactive field on each row is the status switch (covered on [[channels-system-messages-business-rules]]).

## Counter semantics

### Send-counter is per-event, NOT per-status

The sent-count shown beside each template is the **count of unique subscribers where `successfully_sent > 0` for that `system_event`** — aggregated from the channel-statistics collection.

Consequences:

- A template that fired 1,000 times to the same 200 customers shows ~200, not 1,000.
- Each `(subscriber_id, system_event)` row is counted once — duplicate sends to the same recipient don't bump the counter again.
- The counter excludes failed / blocked attempts.

### Lifetime cumulative — never resets

The counter is cumulative since the store was created. There is no "this month" filter, no "since I last opened this modal" filter, no reset. The merchant is seeing total reach per template across the entire store lifetime.

### Informational, NOT a plan-cap counter

The counter is purely for merchant awareness. System messages still count toward the channel's overall plan cap (verify — see [[channels-system-messages-business-rules]]), but this per-template counter is not the plan-cap counter — the merchant should look at the channel's plan-usage indicators ([[marketing-channels]]) for cap status.

## List-row refresh behaviour

### Per-row refresh on save / toggle

When a template is saved or its status toggled, the list refreshes the **affected row's data** (label + send-count + status). The whole list does NOT reload.

Consequence: counters for un-edited rows stay at their value from the last modal-open. If the merchant edits row A while row B's event fires in the background, row B's counter shows the stale value until the modal is re-opened.

### Full list fetched lazily on modal-open

The full list of templates per channel is fetched only when the modal `modal.value` flips to `true`, NOT when the parent channels page mounts. Closing and re-opening the modal refetches the full list from the per-channel system-messages source (Viber: `campaigns_viber_system_messages`; Web Push: `campaigns_web_push_system_messages`), filtered to rows where `event` is not null and `language` matches the store's language (with English fallback per [[channels-system-messages-business-rules]]).

## Status toggle endpoint

Toggling the switch fires a per-channel mutation with `{key: message_id}` URL param + `{status: 0|1}` body. The mutation is async:

- Per-row loader (`loaders[row.key]`) spins while the PATCH is in flight.
- The toggle keeps its visual position.
- On success, the platform fires toast *"Status updated successfully"* and the loader clears.
- On error, the loader clears without a toast.

## Bulk status update endpoint exists but is NOT exposed in UI

There is a bulk-status endpoint (`POST.../system-messages/update-statuses`) that accepts a `{id: status}` map and updates each template's on/off in one round-trip. The current Vue list only fires per-row toggles — there is no "Enable all" or "Disable all" button visible to the merchant.

External integrations (e.g., a custom merchant tool) can reach this endpoint directly to atomically toggle many templates at once. A future UI button could surface it without backend changes.

## Business rules

### OFF templates don't increment counters

When a template is toggled OFF and its event fires, the platform skips the template — no send happens and **no log row is written** in [[marketing-channels-logs]]. Consequently, the send-counter for that template is also not bumped, since the aggregation reads from the channel-statistics rows that didn't get created.

### Failed sends don't count

The aggregation reads `successfully_sent > 0` per `(subscriber_id, system_event)`. Failed or blocked attempts do not contribute. So a template firing into a misconfigured Viber gateway during an outage shows zero counter movement even if the platform attempted hundreds of dispatches.

### Modal full-list refetch is the only way to see global counter updates

Because per-row refresh only updates the saved/toggled row, a merchant who wants to see fresh counters across all templates must close the modal and re-open it.

## Related

- [[marketing-channels-system-messages]] — hub.
- [[channels-system-messages-catalog]] — list where the counters appear.
- [[channels-system-messages-business-rules]] — status switch semantics, plan-cap awareness.
- [[marketing-channels-logs]] — Channel logs modal; system-message sends appear with Type = *"System message"*.
- [[marketing-channels]] — channel-level plan-cap indicators (separate from these per-template counters).

## Open questions

None.
