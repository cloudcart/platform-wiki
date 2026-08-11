---
type: feature
nav_path: "Settings → Api keys → Delete protection"
route_name: api_keys.settings
route_path: /admin/settings/api_keys
aliases: ["API key in use", "API key delete protection", "Bulk delete API keys", "FK protection API keys"]
tags: [settings, api-keys, webhooks, delete-protection, foreign-key]
plan_gates: ["api_requests"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Api keys — Delete protection

> Part of [[settings-api-keys]]. See the hub for related aspects (overview, modal, rate limits, security).

## Purpose

What happens when the merchant clicks Remove on a single key row OR triggers the table's bulk-delete with multiple rows selected: which deletes succeed, which are blocked, how the in-use check works, and why the bulk path is not transactional. This is the page to read for the support ticket *"the system won't let me delete this API key"* or *"I deleted 5 keys and now some are gone and some aren't"*.

## Where to find it

Single delete: [[settings-api-keys-overview]] → row's **Remove** button.

Bulk delete: [[settings-api-keys-overview]] → table tick boxes → standard `CcTable` bulk-delete action.

## What the merchant can do here

- Delete a single key (subject to in-use protection).
- Bulk-delete several keys at once (subject to the same protection, but with non-transactional caveats — see below).
- Reassign or remove dependent webhooks first when the in-use check blocks a delete.

## Settings & fields

There are no editable fields on this flow — it is an action surface. The `CcTable` confirm dialog asks for a generic "are you sure" before issuing the delete.

| Action | HTTP call | Effect on success |
|--------|-----------|-------------------|
| **Single delete** | `DELETE /admin/api/core/settings/api-keys/{id}` | Toast *"Deleted successfully"*; row removed from table. |
| **Bulk delete** | `POST /admin/api/core/settings/api-keys/delete` with body `{ids: [...]}` | Toast *"Deleted successfully"*; selected rows removed from table. |

## Business rules

### Reference protection: a webhook using the key blocks the delete

The "in-use" check that blocks deletion is a **referential constraint enforced at the database layer**, not application logic. When a delete is attempted, the platform catches the database's reference-violation error and surfaces the user-friendly message:

> *"This API key is in use. First delete the webhook using this API key. API key not deleted - `<key name>`"*

Practical implication: even direct database operations cannot delete a key while a webhook references it — the constraint is enforced for every code path, not just the admin UI.

To proceed, the merchant must:

1. Go to [[settings-hooks]] (Webhooks).
2. Find the webhook(s) using this key and either delete them or reassign them to a different API key.
3. Return to [[settings-api-keys-overview]] and delete the API key.

### Bulk delete is stop-on-first-failure, NOT all-or-nothing

If a merchant selects 5 keys and 3 are in use, the bulk delete attempts each in order. The FIRST in-use key encountered triggers a 500 response. **Keys deleted BEFORE that point are already gone.** Keys after that point in the list are NOT touched. The error message names only the first blocking key.

| Behaviour | Confirmed |
|-----------|-----------|
| Transactional (all-or-nothing) | No |
| Stop on first failure | Yes |
| Error message names blocking key | Yes (first one only) |
| Already-deleted keys recoverable | No — values are gone forever |

Merchants should be cautious with bulk delete: if accidental partial deletion occurs, recreating the deleted keys gives them new values (the old values are lost). To safely bulk-delete, the merchant should either:

- Resolve all known webhook dependencies first ([[settings-hooks]]), THEN bulk-delete.
- OR delete one row at a time, where the in-use error blocks only that row and the merchant can investigate before continuing.

### Deactivating is reversible; deleting is not

Toggling the **Active** switch off (see [[settings-api-keys-overview]] / [[settings-api-keys-security]]) keeps the row in the table but the key stops working for API authentication. Toggling back on reactivates the SAME key value — no key rotation required. This is the safer option for *"temporarily revoke access without losing the value"*. Deletion permanently removes the key; recreating it gives a new value.

### No queue / async / notification side effects

Delete actions are synchronous. No background jobs, admin notifications, or webhooks fire on delete or bulk-delete (the deleted key obviously cannot itself authenticate further webhook calls).

## Related

- [[settings-api-keys]] — hub.
- [[settings-api-keys-overview]] — Remove button + bulk-delete trigger.
- [[settings-api-keys-security]] — Active toggle as the reversible alternative.
- [[settings-api-keys-create-edit-modal]] — recreating a deleted key.
- [[settings-hooks]] — Webhooks; the source of the FK reference.
- [[webhook]] — entity page.

## Open questions

None.
