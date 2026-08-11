---
type: feature
nav_path: "Settings → PAT Tokens → List view"
route_name: pat-tokens.settings
route_path: /admin/settings/pat-tokens
aliases: ["PAT Tokens list", "CLI Tokens table", "PAT empty state"]
tags: [settings, security, tokens, list-view]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-pat-tokens]]. See the hub for related aspects (create flow, scopes, restrictions, security, permissions, endpoints).

# PAT Tokens — list view

## Purpose

The default state of the PAT Tokens screen — a table of the store's existing tokens with row-level actions (Edit, Delete, Active toggle) and a header chip showing how many of the cap (10) are in use. The merchant uses this view to identify dormant tokens (via `Last used at`), enable / disable without deleting, and decide when to rotate or revoke.

## Where to find it

Sidebar → Settings → **PAT Tokens**. Default landing state when the screen has ≥1 token. When zero tokens exist, the table is replaced by the empty-state panel (see below).

## What the merchant can do here

- Read the **`<N>` of 10 tokens** chip in the page header — when `<N>` equals 10, the Create button is disabled (`meta.can_create=false`).
- Click **Create Token** (only when below the cap) → opens [[settings-pat-tokens-create-flow]].
- Click a row's **Name** cell → opens the Edit modal (see [[settings-pat-tokens-create-flow]] for the modal flow, which is shared between Create and Edit).
- Flip the per-row **Active** toggle → calls `POST /admin/api/core/account/cli-tokens/{id}/toggle-status` and toasts *"Token activated"* or *"Token deactivated"*. While the request is in flight a `statusLoader` boolean disables the row's toggle.
- Click the per-row **Delete** button → confirms with *"Are you sure you want to delete this token? This action cannot be undone."* → `DELETE /{id}` → toasts *"Token deleted successfully"*. The row is removed from the cache in-place.

## Settings & fields

### List table columns

| Column | What it shows |
|--------|---------------|
| **Name** | Merchant-chosen label. Click opens the Edit modal. |
| **Token (masked)** | Code-formatted prefix — exactly `cc_pat_` (7 chars) + the first 8 hex chars of the token + 49 asterisks. Enough to identify which token is which; not enough to reconstruct. See [[settings-pat-tokens-security]]. |
| **Scopes** | First 3 scope badges + "+N more" overflow indicator when the token holds more than 3 scopes. |
| **Created at** | Date the token was created. |
| **Last used at** | Timestamp of the most recent successful PAT-authenticated request. Updated by `recordUsage` on every accepted request — see [[settings-pat-tokens-endpoints]]. |
| **Active toggle** | Per-row `CcSwitch`. Calls toggle-status endpoint. |
| **(actions)** | Edit (opens modal) / Delete (confirms, then `DELETE /{id}`). |

The table has `show-bulk-actions=false` explicitly set — there is **no bulk-select / bulk-delete** path. Tokens are deleted one at a time. This is deliberate: deleting a token is destructive (the value is lost forever), so the confirm-per-row friction is a feature.

### Header chip — `<N> of 10 tokens`

- The denominator is hardcoded to **10** (the per-store cap — see [[settings-pat-tokens-permissions]]).
- The chip's colour shifts to a warning state as `<N>` approaches 10 *(verify exact threshold)*.
- When `<N> = 10`, the **Create Token** button is disabled and a tooltip explains the cap *(verify wording)*.

### Empty state

When the merchant has zero tokens, the table is replaced by a centred placeholder:

- Large grey `far fa-key` icon (`text-4xl`).
- Heading: *"No PAT Tokens"*.
- Sub-text: *"Create your first token to start using the CloudCart CLI or GraphQL API"*.
- Primary button: **Create Your First Token** → opens the same create modal as the header button.

The empty state is shown whenever the API response contains no token rows, regardless of whether previously-deleted tokens existed. There is no "deleted tokens" / archive view.

## Business rules

- **Click target.** The Name cell is the click target for Edit — clicking elsewhere in the row does nothing. This avoids accidental modal opens when the merchant is scanning scopes.
- **Delete is irreversible.** The confirm dialog message explicitly says *"This action cannot be undone."* Deleting destroys the hash; even recreating a token with the same name yields a new `cc_pat_` value. See [[settings-pat-tokens-security]] for why no recovery is possible.
- **Active toggle preserves the value.** Flipping `active=false` keeps the SHA-256 hash; flipping back to true makes the same token value work again immediately. Use this for "pause a CI token over the holidays without rotating".
- **Owner-only visibility.** Moderators / Administrators do not see this screen at all — the sidebar entry is hidden, and direct navigation to `/admin/settings/pat-tokens` returns HTTP 403. The list endpoint itself is owner-gated at four layers — see [[settings-pat-tokens-permissions]].
- **Sort / filter capability.** *(verify)* — whether the table supports server-side sort by `last_used_at` or filtering by scope is not currently documented in the codebase audit.

## Related

- [[settings-pat-tokens]] — hub.
- [[settings-api-keys]] — store-level API keys list (different model — no per-user, no scopes, no expiration).
- [[settings-staff]] — staff member list; deleting a moderator cascades to delete their (legacy) PAT tokens.

## Open questions

- Does the list view support sorting by `last_used_at` to surface dormant tokens, or is sort client-side only? `(verify)`
- Is there a filter / search input on the table for stores with many tokens? `(verify)`
