---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → JSON-API v2"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Generator API", "POST /generate", "Code PRO generator JSON-API", "API generator divergence"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation, api, json-api-v2]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Code PRO generator — JSON-API v2 programmatic access

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (form layout, modes, fields, validation, business rules).

## Purpose

The Code PRO bulk-generation pipeline is exposed programmatically through **JSON-API v2** via a custom `POST /generate` endpoint. This aspect documents what the API path shares with the admin-panel generator (everything except one critical cap), how to find the resource, and the divergence merchants and integrators must be aware of.

## Where to find it

See [[api-discount-codes-pro]] for the full resource (Schema, Attributes, Relationships, Filtering). The bulk-generation action lives at the resource-specific path `/code-pro/{id}/generate` and is the only batch-generation action in the discount API. See [[code-pro-endpoints-api]] for the endpoint catalogue.

## What the merchant can do here

- Trigger the same bulk-generation pipeline from an external integration (no admin login).
- Send the same generator-type / range / random / structure / length payload as the admin form.
- Persist with the same shared discount terms (conditions, customer groups, region, dates, limits, stacking flags).

## Settings & fields

The payload mirrors the admin form's field catalogue — see [[code-pro-generator-fields]] for backend keys. Validation messages are identical — see [[code-pro-generator-validation]].

## Business rules

### Same pipeline, same side effects

A POST through JSON-API v2 triggers the **same** pipeline as the admin-panel generator:

- The transactional all-or-nothing batch insert.
- The collision pre-check (range mode) or collision-retry loop (random mode) — see [[code-pro-generator-modes]].
- `customer_groups` and `targets` cascade-save per generated code.
- Per-code, per-target, per-customer-group model events.

### Critical divergence — JSON-API v2 hard cap is 5,000

In **random** mode the JSON-API v2 `POST /generate` endpoint is **hard-capped at 5,000 codes per request regardless of the merchant's `discount-code-pro-generator` plan-feature value** (the `limit` field is validated `max:5000`). Older wiki phrasing implied the plan-feature value drives the API cap as well — that's incorrect.

**Only the admin-panel generator honours the higher plan-feature cap.** A merchant on a plan with `discount-code-pro-generator = 10000` can generate 10,000 codes in one batch from the admin panel but only **5,000 in a single random-mode API call**. To exceed 5,000 via random API calls, the integrator must issue multiple sequential calls.

> **Range mode is the exception.** The API's `range_from` / `range_to` (range mode) is **not** count-capped — it is bounded only by the field magnitude (`max:999999999999999`) and `range_to > range_from`, so a range spanning millions of codes is not rejected. (The admin generator, by contrast, caps the range *span* at the plan value too.)

**Over-cap random-mode API requests** return HTTP 422 with the validation error pointing at the `limit` field.

### Validation rules carry over

The other validation rules carry over **verbatim** between admin and API paths:

- Range `from < to`.
- Length 6-18.
- Numeric-only soft cap (the helper that caps `range_to` when only `numeric` structure is selected).
- At least one structure flag must be selected.

See [[code-pro-generator-validation]] for the full message reference.

### No audit log

The platform does NOT capture an audit-log row for batch generation — no actor identity, no diff, no record of which API key triggered the batch. (Same as the admin-panel path — see [[code-pro-generator-business-rules]].)

### For non-batch single-code creation

Use the standard JSON:API resource POST instead. See [[json-api-v2]] for authentication, rate-limit, and the same-side-effects principle, and [[api-discount-codes-pro]] for the resource Schema.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[api-discount-codes-pro]] — JSON-API v2 resource (Schema, Attributes, Relationships, the `POST /generate` action).
- [[code-pro-endpoints-api]] — endpoint catalogue including this action.
- [[code-pro-generator-business-rules]] — admin-panel cap derivation (which the API does NOT honour for `> 5000`).
- [[code-pro-generator-validation]] — message reference shared by both paths.
- [[json-api-v2]] — auth, rate-limit, same-side-effects principle.
- [[settings-api-keys]] — auth credentials for API callers.

## Open questions

None.
