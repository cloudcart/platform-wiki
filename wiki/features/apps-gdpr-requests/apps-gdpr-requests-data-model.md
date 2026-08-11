---
type: feature
nav_path: "Apps → GDPR → Requests → Data model"
route_name: apps.gdpr.requests
route_path: /admin/apps/gdpr/requests
aliases: ["GDPR request fields", "gdpr_requests table", "processed_at", "GDPR request validation", "GDPR request data model", "requestsList endpoint"]
tags: [apps, gdpr, compliance, requests, data-model]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR → Requests: data model

> Part of [[apps-gdpr-requests]]. See the hub for the other aspects (types & channels, processing workflow).

## Purpose

This aspect documents **what a request actually stores and how the workflow state is represented**. It covers the per-request fields written to the `gdpr_requests` table, the binary `processed_at` workflow (there is no status / approve / reject / close enum), the storefront form validation split between popup and full-page modes, the 191-character `message` cap, automatic IP capture, the transactional insert, and the vestigial empty `requestsList` endpoint that confuses anyone reading the routes.

## Where to find it

The merchant sees these fields rendered in the admin Requests tab (`/admin/apps/gdpr/requests` — see [[apps-gdpr-requests]]). The data is written when a customer submits the storefront form (see [[apps-gdpr-requests-types-channels]] for the routes). The admin listing reads from the nested `/api/gdpr/requests/` endpoint.

## What the merchant can do here

- Read the stored fields per row: customer, email, request type, the customer's message, submission timestamp, and processed-at timestamp.
- Mark a request **processed** — this sets the `processed_at` timestamp; leaving it open keeps `processed_at` NULL. That single flag is the entire workflow state.

What the merchant **cannot** rely on: a status enum (`Open / Processed / Closed / Rejected` is a description of the *workflow*, not stored states), a guaranteed-populated Name column, or the top-level `/api/gdpr/requests` endpoint returning data.

## Settings & fields

### Per-request fields stored

A submission writes a row to the `gdpr_requests` table with:

- `customer_id` (when logged in; null for guest).
- `email` (required).
- `name` (optional — stored as an empty string when missing).
- `message` (optional — the customer's description of what they want; max 191 chars).
- `type` (one of the 4 types — see [[apps-gdpr-requests-types-channels]]).
- `client_ip` (IP at submission).
- `created_at` (timestamp).
- `processed_at` (set when the merchant marks the request processed; NULL while open).

The admin lists `created_at` and `processed_at` formatted as datetime, plus a human-readable type label.

### Storefront form validation — split by mode

The storefront submission validation differs by mode:

- **Popup variant** (`/gdpr/request/{type}/popup`, body includes `popup=1`) validates ONLY `email` (required, valid email, max 191 chars). It is the lightest path for the customer.
- **Full-page variant** (`/gdpr/request/{type}` regular submission) validates `email` (required, email, max 191), `name` (required, max 191), and `message` (optional, max 191).

### `message` is capped at 191 characters

The `message` field accepts at most 191 characters. **Long-form complaints will be truncated by the validator** — the customer must keep the message brief or contact the merchant by email instead. The 191 cap comes from the database's indexable text-column limit.

### Name field is OPTIONAL on the stored row

Although the full-page form validates `name` as required, the row's `name` column is stored as an EMPTY string when missing (the controller defaults the input to `''`). For popup submissions `name` isn't validated at all, so the column is blank. **The admin Requests list may show a blank Name for popup-submitted requests** — only `email` is guaranteed populated.

## Business rules

### No "approve / reject / close" semantics — only "processed or not"

The `gdpr_requests` table has only `created_at` and `processed_at` timestamps. There is no `status` enum, no `rejected_at`, no `closed_at`. The merchant marks a request "processed" (sets `processed_at`) or leaves it "open" (NULL). The `Open / Processed / Closed / Rejected` terminology describes the merchant's external *workflow*; the backend stores only binary processed/not-processed.

### IP captured automatically — cannot be spoofed via form

The `client_ip` field is auto-set from the request IP (which respects trusted proxies / `X-Forwarded-For` per the platform's proxy config). The customer cannot spoof it via form data.

### Submission writes via a DB transaction

The submission wraps the row insert in a database transaction. On error the whole insert rolls back — there are no half-inserted request rows.

### The top-level `requestsList` endpoint is empty / vestigial

`GET /api/gdpr/requests` returns an EMPTY collection — this endpoint exists in the routes but its handler returns an empty JSON collection. The real listing endpoint is the nested `/api/gdpr/requests/`, which actually queries the requests table. **Two endpoints share the prefix; only the nested one returns data.** The empty one is likely vestigial — debugging an "empty Requests list" should confirm the admin is hitting the nested endpoint.

## Related

- [[apps-gdpr-requests]] — hub.
- [[apps-gdpr-requests-types-channels]] — the 4 stored `type` values and the storefront routes that write these rows (referenced inline above).
- [[apps-gdpr-requests-processing]] — how the merchant transitions a row from open to processed.
- [[customers]] — the customer record `customer_id` links to.

## Open questions

None.
