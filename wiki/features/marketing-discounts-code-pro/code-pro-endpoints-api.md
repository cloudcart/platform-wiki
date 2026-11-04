---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Endpoints & API"
route_name: discounts-code_pro-list
route_path: /admin/marketing/discounts/code-pro/:id
aliases: ["Code PRO endpoints", "Code PRO JSON-API v2", "Code PRO programmatic access", "Code PRO bulk-generate cap"]
tags: [marketing, discounts, code-pro, api, endpoints, json-api-v2]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, fields, business rules, checkout).

# Code PRO — admin endpoints & JSON-API v2

## Purpose

This page documents the **HTTP surface** for Code PRO codes: the admin-panel endpoints (used by the Vue UI) and the JSON-API v2 endpoints (used by external integrations). Both paths write the same codes and conditions, each with its own validation. Use this page when answering *"what's the URL to bulk-toggle codes?"* or *"can I generate 10,000 codes via API?"*.

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

The legacy single-toggle endpoint (`GET /admin/discounts/code-pro/{discount_id}/status/{code_id}/{status?}`) was removed with the Smarty discount pages on 2026-10-21. The Vue page toggles codes with `POST.../status` and `{ ids: [code_id], status: 1|0 }`.

### JSON-API v2 surface

The full schema lives on [[api-discount-codes-pro]] (the resource page for individual Code PRO codes). The parent Code PRO discount itself is managed via [[api-discounts]] (with `type=code-pro`).

The conditions array schema, validation rules, and writable / read-only attribute split are documented there.

## Business rules

### What the API shares with the admin save

A POST / PATCH through JSON-API v2 writes the same codes and conditions as the admin-panel save (see [[code-pro-business-rules]]), with these differences:

- Conditions and customer groups are deleted and recreated only when they are sent in the request; the admin save always replaces both.
- `discounts_code_pro.code` store-wide uniqueness is a form check, not a database rule. The API checks it on create and on edit; the admin checks it only on new codes — see [[code-pro-overview]].
- The per-code `uses` counter recompute fires on order-status transitions (see [[code-pro-checkout]]).
- **No audit-log entry is written** on either path — see [[discounts-audit-trail]].

### Plan-gating

In the admin, the `discount-code-pro` plan feature gates creating a campaign (403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."*). JSON-API v2 does not read it: creating a campaign compares usage with `discount_coupon` and returns **402 Payment Required**. Adding, editing or generating codes has no plan check on the API.

A duplicate `code` returns **HTTP 422**.

### Bulk-generate cap — 5,000 per request in random mode on the API

In random mode the JSON-API v2 generate endpoint is **hard-capped at 5,000 codes per request regardless of the merchant's `discount-code-pro-generator` plan-feature value**. Its range mode has no count limit.

| Path | Cap |
|---|---|
| Admin-panel generator (`POST /admin/api/core/discounts/code-pro/{id}/generate`) | Reads `discount-code-pro-generator` plan-feature value (default 5,000; plan-specific). |
| JSON-API v2 bulk-generate | Random: hard-coded ceiling of **5,000 codes per request**, plan-feature value ignored. Range: no count limit. |

So a plan with `discount-code-pro-generator = 10000` will still be capped at 5,000 codes per random-mode call through the API. To generate more, the integrator must issue multiple sequential calls. See [[marketing-discounts-code-pro-generator]] for the admin-panel generator behaviour.

### Listing filters via JSON-API v2

The JSON-API v2 resource filters only by `filter[discount_id]`. The admin list's other filters (see [[code-pro-fields]]) are not available there — see [[api-discount-codes-pro]] for the resource-specific notes.

### Permission

Admin-panel endpoints require the `marketing.discounts` permission. JSON-API v2 endpoints require an API key with the corresponding scope — see [[settings-api-keys]].

## How it works

The admin endpoints and the JSON-API v2 endpoints write the same codes and conditions. The main differences are:

- **Auth**: admin session vs API key.
- **Response format**: admin returns JSON for the Vue pages; JSON-API v2 returns the canonical resource document.
- **Validation**: each path has its own rules and field names, including the 5,000-codes cap on random-mode API generate.

Changes to Code PRO codes send no webhook, whether created, edited, toggled, deleted or generated. `discount.created` / `discount.updated` fire when the campaign itself is saved through the form or JSON-API (see [[settings-hooks]]).

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[api-discount-codes-pro]] — JSON-API v2 resource for individual Code PRO codes.
- [[api-discounts]] — JSON-API v2 resource for the parent Code PRO discount.
- [[json-api-v2]] — auth, rate-limits, pagination.
- [[settings-api-keys]] — API key scopes for the `marketing.discounts` area.
- [[settings-hooks]] — discount webhooks; changes to Code PRO codes send none.
- [[code-pro-overview]] — store-wide uniqueness on `discounts_code_pro.code`.
- [[code-pro-business-rules]] — the admin save flow.
- [[code-pro-checkout]] — `uses` counter recompute job triggered after status transitions.
- [[marketing-discounts-code-pro-generator]] — admin-panel generator (honours the plan-feature cap).
- [[marketing-discounts-code-pro-export]] — CSV export endpoint.

## Open questions

No outstanding questions.
