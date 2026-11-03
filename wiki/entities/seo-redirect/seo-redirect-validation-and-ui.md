---
type: entity
nav_path: "Entity → SEO 301 Redirect → Validation and UI"
aliases: ["301 redirect validation", "Redirect error messages", "Duplicate old_url rejection", "Redirect filters and search", "No 302 option", "No redirect on-off toggle"]
tags: [entity, seo, marketing, redirects, validation, ui, permissions]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[seo-redirect]]. See the hub for the other aspects (types, lookup and cache, marketing passthrough, CSV import, auto-tracking).

# 301 Redirect — Validation and UI

## Identity

The catalogue of validation messages, list-view controls, and the deliberate product decisions about what the admin UI does NOT offer for [[seo-redirect|301 Redirects]]. The two notable omissions — **no 302 option** and **no on/off toggle** — are intentional product choices that surprise merchants migrating from platforms with richer redirect controls.

This page is the reference the AI Assistant cites when a merchant asks *"Why is my redirect not saving?"*, *"Can I make this temporary?"*, *"Can I pause a rule?"*, or *"How do I find a specific rule?"*.

## Aliases

- **Validation messages** — the literal error strings surfaced on save.
- **Duplicate rejection** — the behaviour on creating a rule with an `old_url` that already exists.
- **No 302 option** — the deliberate absence of a temporary-redirect choice.
- **No on/off toggle** — the absence of a per-rule disable switch.

## Key Attributes

### Validation messages catalogue

| Trigger | Message | Field |
|---|---|---|
| `old_url` empty | *"Field is required"* | `old_url` |
| Duplicate `old_url` on create / update | *"Old URL is already exist"* | `old_url` |
| Invalid `location` value | *"Location is not valid"* | `location` |
| Missing target entity (chosen Product deleted before save) | per-entity not-found message (`product.err.not_found`, `category.err.not_found`, etc.) | `item_id` |
| `manual` / `external` with empty `new_url` | *"Value is required"* | `new_url` |
| `section` with an unregistered identifier | *"Value is not valid"* | `new_url` |
| Shape mismatch (e.g., type `product` with `new_url` instead of `item_id`) | *"Field is invalid"* | varies |

### Duplicate `old_url` — three different behaviours

| Path | Behaviour on duplicate `old_url` |
|---|---|
| **Modern Vue manager** ([[marketing-seo-301-redirects]] inline create / edit) | **Rejects** with *"Old URL is already exist"* on the offending row. Per-row create/update so the merchant sees the error inline. |
| **Legacy bulk-update endpoint** | Silently **skips** duplicates. Response message: *"SEO settings changed successfully. You have unrecorded URLs due to duplication."* with a list of offending URLs. |
| **CSV import** | **Last-write-wins** — deletes the existing row and inserts the new one. Re-importing the same CSV is idempotent. See [[seo-redirect-csv-import]]. |

The three inconsistent behaviours are a known migration artifact — the Vue manager is the modern path; merchants who hit the bulk-update behaviour are using older surfaces.

### List-view controls

| Control | Behaviour |
|---|---|
| **Search box** | Searches `old_url` LIKE, `new_url` LIKE, AND the names / slugs of linked Products / Categories / Vendors / Blogs / Articles / Pages. Searching for a product name finds redirects targeting it. |
| **Type filter** | Dropdown matching the type enum (`manual`, `external`, `product`, `category`, `vendor`, `blog`, `article`, `page`, `section`). Only redirects of that type are listed. |
| **Sort** | Fixed `id desc` (newest first). **No column is sortable.** The merchant uses search + filter rather than sort. |
| **Bulk delete** | Multi-select rows then Delete. After bulk-delete, `has_301_redirects` is re-evaluated — if zero rules remain, the middleware short-circuits future requests. |
| **Per-row Delete** | Single-row delete. Same `has_301_redirects` re-evaluation. |
| **Per-row Edit** | Inline edit modal with the per-type field shape — see [[seo-redirect-types]]. |
| **Created / updated timestamps** | NOT shown in the table UI. The merchant cannot see when a rule was created or last edited from this screen. |

## Relationships

- **Constrains** what the merchant can save into the [[seo-redirect|301 Redirect]] table.
- **Reads from** [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] for the search and the not-found-entity validation.
- **Is bypassed by** [[seo-redirect-csv-import]] for the duplicate-rejection rule (the CSV path uses last-write-wins).

## Lifecycle

1. The merchant opens [[marketing-seo-301-redirects]] and clicks "Add redirect" (or edits an existing row).
2. They fill the form (Old URL + Redirect type + New URL / Entity picker / Section).
3. They click Save.
4. Server-side validation runs the checks listed above.
5. On error, the message surfaces inline on the offending field; the rule is NOT saved.
6. On success, the rule is created / updated, `redirects301` cache is invalidated, and `has_301_redirects` is recomputed.

## Business rules

### Always 301 — no 302 (temporary) option

Every rule returns HTTP 301 (permanent). The admin UI does NOT expose 302 because the merchant intent for this screen is always permanent migration / restructuring. For temporary redirects (e.g., maintenance pages, A/B tests), the merchant needs a custom server-side rule outside CloudCart.

### No per-rule on/off toggle

To pause a rule, the merchant **deletes and re-creates** it. No temporary-disable toggle. Rules are present-or-absent, never disabled — a deliberate product simplification.

### Fixed sort by ID descending; search matches linked entities

The redirects table is fixed-sort by ID descending (newest first); no column is sortable. The search box matches `old_url` / `new_url` AND linked-entity names — typing "blue t-shirt" finds redirects targeting a product whose name contains that string. The easiest way to find all rules pointing to a specific entity.

### Duplicate-rejection inconsistency

The three different duplicate-handling behaviours (reject / silent-skip / last-write-wins) across the Vue manager, legacy bulk-update, and CSV import are a known inconsistency. Merchants on the modern Vue manager don't hit this; merchants with older workflows might.

### Created / updated timestamps are hidden

Timestamps are stored but not shown in the UI. For audit ("when did this rule get created?"), the merchant needs [[api-redirects]] (JSON-API v2) to query the timestamps directly.

### Permission gate, no plan gate

API endpoints sit behind the `marketing.seo` API permission group; CSV import additionally requires 2FA when the `required_2fa` flag is set (see [[seo-redirect-csv-import]]). No plan tier gate — every plan can create, edit, delete rules. The implicit performance limit (path-prefix optimisation) is documented in [[seo-redirect-lookup-and-cache]].

### Errors are per-row, not transactional

Editing is per-row create / update — one failing row doesn't roll back the others. CSV import is also per-row but reports the aggregate.

## Where it appears

- [[marketing-seo-301-redirects]] — the manager screen where validation surfaces.
- [[seo-redirect-csv-import]] — the bulk-import path with last-write-wins instead of rejection.
- [[seo-redirect-types]] — the per-type "New URL" field shape that drives some validation messages.
- [[api-redirects]] — same validation applies to POST / PATCH.
- [[settings-staff-permissions-tree]] — the `marketing.seo` permission gate.

## Related

- [[seo-redirect]] — hub.
- [[seo-redirect-types]] — the type dropdown and its per-type field validation.
- [[seo-redirect-csv-import]] — the alternative duplicate behaviour.
- [[seo-redirect-lookup-and-cache]] — performance considerations the validation does NOT enforce (custom prefixes).
- [[marketing-seo-301-redirects]] — the manager screen.

## Open Questions

- Whether a future UI revision will expose `created_at` / `updated_at` in the list view (would close a common audit gap).
- Whether the duplicate-handling will be unified across Vue manager / legacy / CSV import in a future release.
