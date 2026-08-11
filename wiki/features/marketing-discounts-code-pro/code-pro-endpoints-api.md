---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Endpoints & API"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO endpoints", "Code PRO JSON-API v2", "Code PRO programmatic access", "Code PRO bulk-generate cap"]
tags: [marketing, discounts, code-pro, api, endpoints, json-api-v2]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, fields, business rules, checkout).

# Code PRO — admin endpoints & JSON-API v2

## Purpose

This page documents the **HTTP surface** for Code PRO codes: the admin-panel endpoints (used by the Vue UI) and the JSON-API v2 endpoints (used by external integrations). Both paths trigger the same side-effects — the deletes-and-recreates transaction, the store-wide unique constraint, the `uses` counter recompute job. Use this page when answering *"what's the URL to bulk-toggle codes?"* or *"can I generate 10,000 codes via API?"*.

For the field schema see [[code-pro-fields]]. For save-flow behaviour see [[code-pro-business-rules]].

## Where to find it

The admin endpoints sit under `/admin/api/core/discounts/code-pro/`; the JSON-API v2 endpoints are documented separately on [[api-discount-codes-pro]].

## What the merchant can do here

Drive code CRUD programmatically — typically used by:

- Integrators syncing partner / influencer code rosters from an external CRM.
- ERP systems issuing per-customer one-off codes.
- Bulk-rotation scripts that disable expired codes nightly.

## Settings & fields

### Admin-panel endpoints (used by the Vue UI)

Base: `/admin/api/core/discounts`. Authenticated via the admin session; protected by the `marketing.discounts` permission.

| Action | Endpoint | Method |
|--------|----------|--------|
| List codes | `/code-pro/{id}` | GET |
| Single code (load) | `/code-pro/{id}/{code_id}` | GET |
| Create code | `/code-pro/{id}/save` | POST |
| Edit code | `/code-pro/{id}/save/{code_id}` | POST |
| Toggle status | `/code-pro/{id}/status` | POST |
| Delete code(s) | `/code-pro/{id}?ids[]={code_id}` | DELETE |
| Generate codes | `/code-pro/{id}/generate` | POST → [[marketing-discounts-code-pro-generator]] |
| Export to CSV | `/code-pro/{id}/export` | GET → [[marketing-discounts-code-pro-export]] |

There is also a legacy single-toggle endpoint: `GET /admin/discounts/code-pro/{discount_id}/status/{code_id}/{status?}` — toggles a single code's `active` flag and returns updated row HTML for the inline grid renderer. The modern Vue page uses the unified `POST.../status` with `{ ids: [code_id], status: 1|0 }` instead.

### JSON-API v2 surface

The full schema lives on [[api-discount-codes-pro]] (the resource page for individual Code PRO codes). The parent Code PRO discount itself is managed via [[api-discounts]] (with `type=code-pro`).

The conditions array schema, validation rules, and writable / read-only attribute split are documented there.

## Business rules

### Same side-effects principle

A POST / PATCH through JSON-API v2 triggers the same pipeline as the admin-panel save (see [[code-pro-business-rules]]):

- The delete-then-recreate of `targets` and `customer_groups` join rows runs identically (on edit of an existing code).
- The `discounts_code_pro.code` store-wide uniqueness is enforced by the **create-time form validator** (not a DB constraint, and not re-checked on edit) — see [[code-pro-overview]].
- The per-code `uses` counter recompute fires on order-status transitions (see [[code-pro-checkout]]).
- **No internal audit-log entry is written** — discount CRUD has no audit log (only webhooks fire); the payload does not distinguish API from admin changes. See [[discounts-audit-trail]].

This is the wiki-wide [[json-api-v2]] same-side-effects principle: the API path is **not** a shortcut around platform invariants. Whatever fires on the UI fires on the API.

### Plan-gating

The `discount-code-pro` plan feature gates creation — API requests on plans that don't enable it return **HTTP 403 Forbidden** with the *"Not supported by plan"* message (older wiki phrasing said 402; corrected).

The store-wide unique constraint on `code` returns **HTTP 422** with the same *"Discount code is exists"* error (`code_pro.validation.code.unique`).

### Bulk-generate cap — 5,000 per request, HARD on the API path

The bulk-generate endpoint is **hard-capped at 5,000 codes per request regardless of the merchant's `discount-code-pro-generator` plan-feature value**.

| Path | Cap |
|---|---|
| Admin-panel generator (`POST /admin/api/core/discounts/code-pro/{id}/generate`) | Reads `discount-code-pro-generator` plan-feature value (default 5,000; plan-specific). |
| JSON-API v2 bulk-generate | Hard-coded ceiling of **5,000 codes per request**; plan-feature value is ignored. |

So a plan with `discount-code-pro-generator = 10000` will still be capped at 5,000 codes per call when invoked through the API. To generate more, the integrator must issue multiple sequential calls. See [[marketing-discounts-code-pro-generator]] for the admin-panel generator behaviour.

### Listing filters via JSON-API v2

The JSON-API v2 resource supports the same filters as the admin list (see [[code-pro-fields]] for the filter set) via `filter[active]`, `filter[time_used]`, `filter[uses_left]`, `filter[start_date]`, `filter[date_end]`. The exact operator syntax follows [[json-api-v2]] conventions — see [[api-discount-codes-pro]] for the resource-specific notes.

### Permission

Admin-panel endpoints require the `marketing.discounts` permission. JSON-API v2 endpoints require an API key with the corresponding scope — see [[settings-api-keys]].

## How it works

The admin endpoints and the JSON-API v2 endpoints share the same domain layer underneath, which is why the side-effects are identical. The only behavioural differences are:

- **Auth**: admin session vs API key.
- **Response format**: admin returns HTML / redirect payloads in some legacy cases; JSON-API v2 returns the canonical resource document.
- **The 5,000-codes hard cap on the API generate path** — the only place the API is more restrictive than the UI.

The `discount.updated` webhook fires on the parent campaign whenever a child code is created / edited / toggled / deleted (see [[settings-hooks]]). Receivers must be idempotent — bulk-generate fires it once per affected parent (not per code).

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[api-discount-codes-pro]] — JSON-API v2 resource for individual Code PRO codes.
- [[api-discounts]] — JSON-API v2 resource for the parent Code PRO discount.
- [[json-api-v2]] — same-side-effects principle, auth, rate-limits, pagination.
- [[settings-api-keys]] — API key scopes for the `marketing.discounts` area.
- [[settings-hooks]] — `discount.updated` webhook fires on per-code CRUD.
- [[code-pro-overview]] — store-wide uniqueness on `discounts_code_pro.code`.
- [[code-pro-business-rules]] — deletes-and-recreates save flow that the API path also follows.
- [[code-pro-checkout]] — `uses` counter recompute job triggered after status transitions.
- [[marketing-discounts-code-pro-generator]] — admin-panel generator (honours the plan-feature cap).
- [[marketing-discounts-code-pro-export]] — CSV export endpoint.

## Open questions

No outstanding questions.
