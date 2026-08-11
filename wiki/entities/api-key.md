---
type: entity
aliases: ["API Key", "REST API key", "Store API key", "Integration key", "API token", "API ключ", "Достъп до API"]
tags: [settings, developer, integration, security, entity]
created: 2026-05-21
updated: 2026-05-24
source_count: 0
---
# API Key

## Identity

An **API Key** is a long random credential the merchant generates so that an external integration (Zapier, a custom ERP / CRM, an in-house script, a third-party app, an outgoing webhook receiver authenticating callbacks) can call CloudCart's public REST API as the store. Each Key is **bound to the store as a whole** — not to a specific admin user — and carries the same access scope as the store's plan (the platform's API permits everything the plan does). The merchant gives each Key a Name and Description (e.g., *"Zapier"*, *"ERP sync"*) so they can be told apart later, and can independently activate / deactivate or delete any Key. Keys are managed from [[settings-api-keys]] (Sidebar → Settings → Api keys).

To authenticate against the API, the calling integration sends both the **API Key value** and the store's **Site ID** (also shown on [[settings-api-keys]] as a chip in the page header) against the API base URL `<store-host>/api/v2`. The store's rate limit is enforced **per store** (not per Key), so creating more Keys does not increase throughput — see Business rules.

An API Key is intentionally **distinct from a [[pat-token|Personal Access Token (PAT)]]**: a PAT belongs to an individual admin user (only the store **owner** can create one), supports **fine-grained scopes** (e.g., `orders:read`, `products`, `inventory`), supports optional **expiration** and **IP allowlists**, is **one-shot revealed** at creation (the platform stores only a SHA-256 hash, so the value is gone after the create modal closes), and authenticates the CloudCart CLI and the GraphQL endpoint. An API Key is the older / coarser model: store-wide, no scopes, no expiration, no IP allowlist, plaintext-stored and re-readable from the admin UI at any time after creation.

## Aliases

- **API Key** / **API Keys** — the canonical merchant-facing term in the admin UI and sidebar (Settings → Api keys).
- **REST API key** — emphasises that these authenticate the REST endpoints at `/api/v2`.
- **Store API key** — emphasises the store-scope binding (vs. PAT's user-scope).
- **Integration key** / **API token** — informal phrasing common in support tickets and integration docs.
- **API ключ** / **Достъп до API** — Bulgarian terms used interchangeably across the settings area.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`name`) | Required free text, max 50 chars, must be **unique per store** | The merchant's internal label (e.g., *"Zapier"*, *"Google Sheets sync"*). Required; the create modal blocks save with *"Name is required"* if empty. A second Key cannot reuse an existing Key's name — the platform rejects the save with a uniqueness error. |
| **Description** (`description`) | Optional textarea | Free text context about what the Key is used for. Not shown to the integration; pure documentation for the merchant. |
| **Key value** (`key`) | n/a (server-generated at create time, never regenerated) | A 64-character random uppercase string generated server-side. **Cannot be supplied or chosen by the merchant, and cannot be re-generated** — the update endpoint silently restores the original value if a tampered request tries to change it. The only way to "rotate" a Key is to create a new Key and delete the old one. Visible in the table at any time (truncated to 30 chars + `...` + click-to-copy icon — the truncation is cosmetic; the full value is shipped to the browser). |
| **Active** (toggle) | Toggle switch in the table | When OFF, the Key is rejected at the API gateway. Reversible — flipping back ON reactivates the same value. Toggling does NOT change the Key value; it only flips the active flag. |
| **Created at** | n/a (auto) | Visible in the **Created** table column. |
| **Last updated** | n/a (auto, bumped on edit or status toggle) | Visible in the **Last updated** column. |
| **Site ID** (page-level) | n/a — store-level setting | Shown as a chip in the [[settings-api-keys]] page header. NOT stored on the Key row, but every API call must send the Site ID alongside the Key for authentication. |
| **In-use references** | n/a — derived | Each Key may be referenced by one or more **Webhooks** ([[settings-hooks]]) as their authentication credential. The platform blocks delete (single or bulk) when at least one Webhook still references the Key — see Business rules. |

The Key value is stored **in plaintext** at rest (verified against backend in [[settings-api-keys]] — *"Key encryption — VERIFIED PLAINTEXT"*). Anyone with access to the admin page can read the full value at any time. This is the most important security difference vs. [[pat-token|PAT tokens]] (which store only a SHA-256 hash).

API Keys do **NOT** track per-Key usage timestamps — unlike [[pat-token|PAT tokens]] which surface `last_used_at` and `last_used_ip`, no `last_used_at` or `last_used_ip` field exists on the API Key row, and none is shown in the UI.

**No auto-revocation:** the platform does not auto-deactivate an API Key on suspicious activity, repeated 401s, leaked-key detection, or staff-account removal. The merchant must manually disable (Active toggle) or delete the Key.

**Active toggle mid-request:** the Active flag is checked at the API gateway on each request. Flipping Active OFF rejects every new request immediately, but a request that has already passed the gateway and is processing completes — the platform does not abort in-flight work.

## Where it appears

- [[settings-api-keys]] — the master management screen (list, create, edit, toggle Active, delete, bulk-delete; also shows Site ID, API Base URL, and the plan's API rate-limit info).
- [[settings-hooks]] — the Webhooks screen; every Webhook **must** pick an API Key from this store, and the Key's value is auto-forwarded as the `X-CloudCart-ApiKey` HTTP header on every outgoing webhook POST so the receiver can authenticate the call.
- [[settings-pat-tokens]] — the comparison screen the merchant lands on when asking *"which credential do I need?"* (the page explicitly contrasts the two models).

There is no separate sidebar entry for "create API key" — the Add button lives on the management screen.

## Related

- [[pat-token]] — the personal, scoped, hash-stored, one-shot-revealed alternative used by the CloudCart CLI + GraphQL. Different security and access model — see Identity above.
- [[webhook]] — outgoing webhooks reference an API Key for their `X-CloudCart-ApiKey` authentication header. Deleting an API Key that's referenced by a Webhook is blocked.
- [[settings-hooks]] — Webhooks configuration where the Key is picked.
- [[settings-staff]] — `settings.api_keys` permission must be granted on the Moderator's permission tree for them to access [[settings-api-keys]].
- [[merchant-roles]] — concept page on permission scoping (which staff member can manage API Keys).
- [[plan]] — the `api_requests` plan feature governs the API rate-limit info shown on [[settings-api-keys]] (note that the actually-enforced platform-wide limit is hardcoded at 60 requests/minute per store domain regardless of the displayed plan value — see the verified details in [[settings-api-keys]]).
- [[plan-gates]] — concept page on plan-based feature gating; the API throughput sits behind one.

## Open Questions

No outstanding questions — all items resolved or removed.
