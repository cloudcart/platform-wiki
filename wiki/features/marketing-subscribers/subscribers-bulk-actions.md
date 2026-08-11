---
type: feature
nav_path: "Marketing → Subscribers → Bulk actions"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers
aliases: ["Subscribers bulk actions", "Bulk-tag subscribers", "Bulk-accept marketing", "Per-row subscriber actions"]
tags: [marketing, subscribers, bulk, actions]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, detail modal, channels, import, settings, lifecycle).

# Subscribers — bulk actions and per-row actions

## Purpose

Once the merchant has filtered the list down to a target slice, the bulk-action bar and the per-row icons let them apply marketing-consent flips, tag changes, deletion, or log inspection across one or many subscribers in a single operation. The bulk actions also propagate side-effects to linked customers and segment re-evaluation.

## Where to find it

Sidebar → **Marketing** → **Subscribers**. The bulk-action menu appears once at least one row's checkbox is ticked.

## What the merchant can do here

- Bulk-set tags on a selection (opens the Set-tags modal).
- Bulk-flip marketing consent on (`Accept marketing`) or off (`Do not accept marketing`).
- Bulk-delete selected subscribers.
- Per-row: toggle the inline "Accepts marketing" switch.
- Per-row: open the activity Log side modal.
- Per-row: delete a single subscriber with confirm prompt.

## Settings & fields

### Bulk-actions bar — 3 custom actions + default delete

The table's bulk-action menu (visible once 1+ rows are checked) exposes 3 explicit external actions plus the default delete:

| Action label | Icon | Behaviour |
|---|---|---|
| **Set tags** | `fa-tag` | Opens the Set-tags modal — a small (`size=md`) modal with one tag-select control *"Set tags"* (tags mode, autocompletes against `/admin/api/core/customers/tags`, allows creating new tags on the fly). Saves via `POST /admin/api/core/marketing/subscribers/tagging` with comma-joined tag string. Validation: `tags: required|string|min:2`. |
| **Accept marketing** | `fa-envelope-open-text` | Bulk-flips `marketing = 1` on selected ids. Optimistic UI: the cached rows are immediately updated; on error, reverted. Toast on success: *"Accept marketing changed successfully."* |
| **Do not accept marketing** | `fa-envelope` (solid) | Bulk-flips `marketing = 0`. Same optimistic behaviour. |
| (default) **Delete** | trash | Calls `DELETE /admin/api/core/marketing/subscribers` with checked ids; refetches the page. |

### Per-row actions

- **Log button** (`fa-chart-bar`, ghost-button) — opens the per-subscriber activity-log side modal (size `xll`), a marketing-log viewer with 5 columns: Action, Subscriber, Info, Created at, Updated at. The query state (page, perpage) resets to `{page: 1, perpage: 25}` each time the modal opens.
- **Delete trash icon** — confirm prompt: *"Remove subscriber?"* → on accept, `DELETE /admin/api/core/marketing/subscribers` with the single id, then refetch.
- **Accepts-marketing toggle** — inline on/off switch (true=1, false=0). Optimistic flip via the bulk-marketing endpoint with a single-id payload; reverts on error. **No-op when `row.deleted_customer` is truthy** (prevents flips on orphan-customer rows).

## Business rules

### Bulk marketing-toggle propagates to customer + segments (3 side-effects)

The bulk "Accept marketing" / "Decline marketing" action (`POST /admin/api/core/marketing/subscribers/marketing/{allow}`) does THREE things in one transaction:

1. Updates the per-channel marketing-consent flag on every channel to the new value.
2. Writes a `marketing` entry to the subscriber's activity log, recording the admin who initiated the change as `initiator`.
3. Updates the marketing flag on EVERY linked customer to the corresponding yes/no value.

Then queues a background task to re-evaluate segment membership for the affected ids — so any segments filtered by marketing state immediately re-evaluate. **This is why a single bulk-accept can shift many segments' counts at once.**

The reverse asymmetry on customer-side marketing flips applies here too: a bulk admin flip *propagates BOTH ways* (it's an explicit admin action), but the storefront customer-side `no → yes` does NOT auto-re-enable channels. See [[subscribers-lifecycle]].

### Bulk-tag also re-evaluates segments

`POST /admin/api/core/marketing/subscribers/tagging` requires a string of at least 2 characters (`tags: required|string|min:2`). After tagging, it queues a background task to re-evaluate segment membership for the tagged ids — segments using `tag` conditions re-evaluate.

### Bulk delete cascades the full cleanup

When the merchant bulk-deletes, the platform cascades per the subscriber-delete contract — see [[subscribers-lifecycle]] for the full join-cleanup catalogue. Each deleted subscriber fires its own `subscriber.deleted` webhook ([[settings-hooks]]). Hard-delete cascades produce N `remove_channel` events (one per channel row removed).

### Permission required

All bulk endpoints honour `hasApiPermission:marketing,marketing.subscribers`. A moderator without that permission sees the buttons but the API call returns 403. The bulk-delete action does NOT have a separate finer-grained permission — anyone with the marketing.subscribers grant can purge the list. See [[subscribers-lifecycle]] for the permission gate.

### Optimistic UI — what to know

The Accept-marketing / Do-not-accept-marketing actions and the per-row toggle apply OPTIMISTICALLY: the row state flips immediately in the UI before the backend confirms. On error, the cached state reverts and a toast surfaces the failure. This means a merchant clicking through rapid toggles may briefly see a state that the server later rejects — usually because the row was concurrently edited by another admin user.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-list-view]] — the table the bulk actions operate on.
- [[subscribers-lifecycle]] — delete cascade, marketing-flip asymmetry, permission gate.
- [[subscribers-channels]] — the underlying per-channel rows the bulk-marketing updates.
- [[marketing-segments]] — re-evaluation consumer; bulk actions queue segment recompute.
- [[settings-hooks]] — `subscriber.updated` / `subscriber.deleted` webhooks fired by bulk actions.

## Open questions

None.
