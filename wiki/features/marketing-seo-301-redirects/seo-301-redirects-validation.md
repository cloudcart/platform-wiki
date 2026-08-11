---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → Validation"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["301 redirect validation", "Old URL already exists", "Location is not valid", "Redirect form errors", "Same-URL silent skip", "Old URL is required"]
tags: [marketing, seo, redirects, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (types, CSV import, middleware, wildcards, marketing pass-through, auto-tracking).

# 301 Redirects — Validation

## Purpose

This aspect covers the **server-side and frontend validation** that runs when the merchant creates or edits a 301 redirect rule. It lists the three custom backend validators, the Zod shape validation on the Vue page, the catalogue of error messages with their precedence, and the silent-skip edge case where a `creating` callback aborts the save with no feedback at all.

Understanding the validation rules matters for two support patterns: "I got an error message I don't understand" (look up the message in the table here) and "I clicked Create but nothing happened" (the silent-skip case below).

## Where to find it

The validation runs on the Create / Edit row inline editor on [[marketing-seo-301-redirects]] and on the equivalent JSON-API endpoint [[api-redirects]]. The Vue page surfaces backend 422 errors inline against the offending field; the older bulk-update endpoint surfaces them as a top-of-page banner.

## What the merchant can do here

- See per-field error messages displayed inline on the row when Create / Save fails.
- See `"Old URL is already exist"` against the old-URL field on a duplicate-save.
- See `"Field is required"` against an empty old-URL or empty new-URL on free-form types.
- See an entity-not-found message (always in English even on a localized admin) when the picked entity's ID doesn't resolve.

## Settings & fields

### Backend validators on Create / Update

The store/update endpoints (`POST /admin/api/core/seo/redirects`, `PATCH /admin/api/core/seo/redirects/{id}`) run these three custom rules:

| Validator | Field(s) | What it checks | Error message |
|-----------|----------|----------------|---------------|
| `is_existing_url` | `old_url` | Required, string, **unique** store-wide. | *"Old URL is already exist"* on duplicate; *"Old URL is required"* on empty. |
| `validate_item` | `item_id` | For `product` / `category` / `vendor` / `page` / `blog` / `article` types, the ID must resolve to an existing record. For `manual` / `external` / `section`, `item_id` is not required. | Per-entity not-found message (in English): *"Product not found"*, *"Category not found"*, *"Vendor not found"*, etc. |
| `validate_new_url` | `new_url` | For `manual` / `external`: required, non-empty. For `section`: must be one of the registered Sections (see [[seo-301-redirects-types]]). Otherwise: *"Value is required"* / *"Value is not valid"*. | *"Value is required"* or *"Value is not valid"*. |
| (location enum) | `location` | Must be one of the 9 type keys from [[seo-301-redirects-types]]. | *"Location is not valid"*. |

### Frontend (Zod) validation

The Vue page additionally enforces:

- `old_url` cannot be empty: *"Field is required"*.
- The shape is internally consistent — if `location` is one of `manual` / `external` / `section`, `item_id` must be null/empty AND `new_url` must be the payload field used; for entity-based types, `new_url` must be empty and `item_id` is the field used. Mismatch → *"Field is invalid"*.

These Zod errors fire before the request is sent, so the merchant doesn't waste a round-trip.

## Business rules

### Validation error precedence

the application framework runs the three custom validators in arbitrary order. In practice, this is what the merchant sees:

- Empty `old_url` → *"Old URL is required"* wins.
- Non-empty duplicate `old_url` → *"Old URL is already exist"* wins.
- Invalid `location` → *"Location is not valid"* wins.
- Entity-typed redirect with missing target ID → uses the **English** translation namespace (`__en`), so the merchant sees the English error message even on a localized admin (e.g., *"Category not found"* rather than the Bulgarian translation). This is a known quirk.

### Same-URL silent skip on `creating` callback

When a merchant creates a `product` / `category` / `vendor` redirect AND the `old_url` is identical to the entity's CURRENT URL, the `creating` callback returns `false` — silently aborting the save with **no error message**. This prevents merchants from accidentally creating a redirect from a product to itself, but it also means the merchant has no feedback that the save was skipped. Support pattern: "I clicked Create and nothing happened" with an entity-type redirect → check whether `old_url` equals the entity's current URL.

### `parseOldUrl` — strips fragment, keeps query

The stored `old_url` is URL-decoded on save and stripped of any `#fragment`. The query string IS kept — so a redirect from `/old?source=newsletter` to a new URL only fires when the customer hits `/old?source=newsletter` exactly. To match the path regardless of query, the merchant uses a wildcard (`/old*`) — see [[seo-301-redirects-wildcards]].

### Update endpoint sets `item_type = location` transiently

The PATCH endpoint maps `item_type` directly from the request's `location` field — so updating a `manual` redirect transiently mutates `item_type = "manual"` even though the model's saving boot callback later resets `item_type` to `null` for non-entity types. The transient inconsistency is auto-corrected by the saving callback before the row persists. Support visibility: never observable from the UI.

### Duplicate `old_url` detection — silent skip on legacy bulk save

The legacy bulk-update endpoint silently skips duplicate `old_url`s — the response message reads *"SEO settings changed successfully. You have unrecorded URLs due to duplication."* with the offending URLs listed. The Vue page uses per-row create/update calls, so duplicate-detection returns a per-row 422 with *"Old URL is already exist"* displayed inline against the row.

### URL-decoding on save normalises the stored value

Percent-encoded characters in `old_url` are decoded on save (`%20` → space, `%2F` → `/`, etc.) — so the stored value is human-readable. The lookup at request time also URL-decodes the incoming path, so the comparison is consistent.

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-301-redirects-types]] — the type enum that the `location` validator enforces.
- [[seo-301-redirects-wildcards]] — how `old_url` is parsed (fragment stripped, query kept) and how literal `*` becomes SQL `%`.
- [[seo-redirect-validation-and-ui]] — entity-side validation catalogue (data-model view of the same rules).
- [[api-redirects]] — JSON-API v2 endpoint applies the same validation pipeline.

## Open questions

- Whether the same-URL `creating` callback skip extends to `page` / `blog` / `article` entity types or is scoped to `product` / `category` / `vendor` only (verify).
