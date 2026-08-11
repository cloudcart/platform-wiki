---
type: feature
nav_path: "Settings → Api keys → Security"
route_name: api_keys.settings
route_path: /admin/settings/api_keys
aliases: ["API key plaintext", "API key immutability", "API key permissions", "API key Active toggle", "Сигурност на API ключове"]
tags: [settings, api-keys, security, permissions, plaintext]
plan_gates: ["api_requests"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Api keys — Security model

> Part of [[settings-api-keys]]. See the hub for related aspects (overview, modal, rate limits, delete protection).

## Purpose

The trust + access model around API keys: plaintext storage, immutability of the key value once generated, no per-key scopes / endpoint restrictions, what Active=OFF actually does and when it takes effect, why the table truncation is purely cosmetic, and which permission gates the screen itself. This is the page to read for a security-review ticket like *"is our key safe if we leak the database?"* or *"can a moderator see API keys?"* or *"how fast does revoking a key actually stop the integration?"*.

## Where to find it

The behaviours documented here apply to the screen at Sidebar → Settings → Api keys, but they're surfaced across [[settings-api-keys-overview]] (truncation, Active toggle) and [[settings-api-keys-create-edit-modal]] (read-only key value in Edit mode).

## What the merchant can do here

- Toggle a key Active=OFF to immediately stop accepting it for new API requests (see latency below).
- Toggle Active=ON to resume — no rotation needed because the value is preserved.
- Confirm which staff users can see / edit API keys via the permission tree.

What the merchant cannot do:

- Encrypt or hash the key value at rest — there is no UI for this; values are plaintext.
- Change the key value in place — the platform reverts any attempt to change it.
- Hide the key value after creation — there is no "show only once" pattern.
- Restrict a key to specific endpoints / scopes — no per-key permission model exists.

## Settings & fields

There are no security-configuration fields on this screen. The merchant's controls are:

| Surface | Behaviour |
|---------|-----------|
| **Active toggle** | Per-row switch on [[settings-api-keys-overview]]; turns the key into a non-authenticator without deleting the value. |
| **Delete** | Permanent — see [[settings-api-keys-delete-protection]]. |
| Permission tree | Configured at [[settings-staff]] → Access permissions tree, NOT here. |

## Business rules

### Storage is PLAINTEXT — VERIFIED

API keys are stored **in plaintext** in the database — generated as 64-character random uppercase strings, but NOT hashed or NOT encrypted at rest. Implications:

- If the database is compromised, all API keys are readable in plaintext.
- The value is also returned in the JSON page payload to the browser, so anyone with admin-page access (or browser dev tools while viewing the page) can read the full value — the table truncation to 30 chars is purely cosmetic.
- Merchants should treat API keys as **secrets** and rotate them periodically if they suspect a breach. Rotation = delete + create new ([[settings-api-keys-delete-protection]] + [[settings-api-keys-create-edit-modal]]).

### Key value is immutable — enforced by the platform

The platform detects any attempt to change a key's value on save and reverts it to the original value. So:

- Even a developer with database-level access through the application cannot rotate a key in place — the platform silently reverts the change.
- Only a direct database write that bypasses the application entirely would get around this — i.e. no application code path can rotate a key.
- The only path to actually change a key value is **delete + create** (see [[settings-api-keys-delete-protection]]).

### Display truncation is cosmetic, not a security boundary

The 30-character truncation + `...` shown in the table is a purely client-side display nicety. The full key value is shipped in the JSON response to the browser, so anyone with access to the admin page (or browser dev tools while viewing it) can read the full value. The clipboard-copy feature reads from the full string in the row data, not from the truncated display.

No "show the full key only once at creation" pattern exists — the value is visible (and copyable) forever from the Edit modal.

### No per-key scopes — any active key can hit any endpoint the plan allows

There is no per-key permission / scope model. Any active key on the store can call any JSON-API v2 endpoint that the merchant's plan permits. The plan governs the available surface area; the keys are interchangeable credentials with no fine-grained restrictions.

This is by design — the credential surface is admin-panel-only — but it means key rotation (delete + create) is the only mitigation when a key value is suspected to be exposed.

### Active=OFF takes effect on the NEXT request

The API authentication layer checks, on every request, that an active key with the supplied value exists. There is no per-request session or token cache — every API call looks this up freshly. So:

- Toggling Active=OFF takes effect within seconds (the next request fails authentication).
- In-flight requests at the moment of toggle DO complete; they were already past the authentication check. Only NEW requests are blocked.
- No "force-disconnect" of long-running queries / streams.

Active=OFF is the fastest way to revoke a key without losing the value. Use it as the first response to a suspected leak, THEN decide whether to rotate.

### Permission gate: `settings` OR `settings.api_keys`

The API endpoints under `/admin/api/core/settings/api-keys` are gated by the `settings` / `settings.api_keys` permission. So a Moderator needs either:

- The broad **Settings** permission, OR
- The specific **API Keys** permission (more granular).

A Moderator without those permissions cannot view, create, edit, delete, or toggle keys. The store **Administrator** (owner) has full access by default. Granular per-Moderator permissions are set from [[settings-staff]] → Access permissions tree, NOT here.

### No JSON-API v2 management of API keys themselves

**API keys cannot be managed via the API itself.** There is no JSON-API v2 resource for create / list / edit / delete of API keys — by design, the credential surface is admin-panel-only. An integration cannot bootstrap its own credentials; the merchant must generate the key on this screen and hand the value to the integration out-of-band.

### Authentication uses BOTH the key value and the Site ID

The Site ID chip in the page header isn't decoration — integration code must send the store's Site ID alongside the key value to authenticate (header `X-CloudCart-ApiKey` — verify). The API base URL `<host>/api/v2` is the prefix for all requests. Together: Site ID + API key + base URL = the three pieces a developer needs.

## Related

- [[settings-api-keys]] — hub.
- [[settings-api-keys-overview]] — Active toggle + truncation in the table.
- [[settings-api-keys-create-edit-modal]] — read-only key in Edit mode + the "Generate" label semantics.
- [[settings-api-keys-delete-protection]] — rotation requires delete + create.
- [[settings-staff]] — `settings` / `settings.api_keys` permission grants.
- [[settings-pat-tokens]] — Personal Access Tokens — different auth model (user-bound, not store-bound).
- [[json-api-v2]] — auth + side-effects principle.
- [[api-key]] — entity page.

## Open questions

- Confirm authentication header name (`X-CloudCart-ApiKey` vs alternative) (verify).
