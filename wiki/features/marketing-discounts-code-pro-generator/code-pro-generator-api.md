---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → JSON-API v2"
route_name: discounts-code_pro-generator
route_path: /admin/marketing/discounts/code-pro/:id/generator
aliases: ["Generator API", "POST /generate", "Code PRO generator JSON-API", "API generator divergence"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation, api, json-api-v2]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-11-04
source_count: 5
---

# Code PRO generator — JSON-API v2 programmatic access

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (form layout, modes, fields, validation, business rules).

## Purpose

The Code PRO bulk-generation pipeline is also exposed through **JSON-API v2** via a custom `POST /api/v2/discount-codes-pro/generate` endpoint. This aspect documents its route, fields and limits, and how they differ from the admin-panel generator.

## Where to find it

See [[api-discount-codes-pro]] for the full resource (Schema, Attributes, Relationships, Filtering). The bulk-generation action is `POST /api/v2/discount-codes-pro/generate`, with `discount_id` in the request data. See [[code-pro-endpoints-api]] for the endpoint catalogue.

## What the merchant can do here

- Trigger the same bulk-generation pipeline from an external integration (no admin login).
- Send `generator_type`, `limit`, `length`, `structure`, `range_from` and `range_to`.
- Persist with shared discount terms (`conditions`, `customer_groups`, `geo_zone_id`, dates, limits, stacking flags).

## Settings & fields

The fields are those above, with their own names rather than the admin form's (see [[code-pro-generator-fields]] for the admin keys). In `conditions`, `value` and `order_over` are stored as sent: money in minor units, percent × 100 (1000 means 10%). `date_start` is required, in `Y-m-d`.

## Business rules

### Same save, own validation

A POST through JSON-API v2 saves codes the same way as the admin-panel generator:

- The transactional all-or-nothing batch insert.
- The collision pre-check (range mode) or collision-retry loop (random mode) — see [[code-pro-generator-modes]].
- `customer_groups` and `targets` cascade-save per generated code.
- Per-code, per-target, per-customer-group model events.

### JSON-API v2 cap is 5,000 in random mode

In **random** mode the JSON-API v2 `POST /generate` endpoint is **hard-capped at 5,000 codes per request regardless of the merchant's `discount-code-pro-generator` plan-feature value** (the `limit` field is validated `max:5000`).

**Only the admin-panel generator honours the higher plan-feature cap.** A merchant on a plan with `discount-code-pro-generator = 10000` can generate 10,000 codes in one batch from the admin panel but only **5,000 in a single random-mode API call**. To exceed 5,000 via random API calls, the integrator must issue multiple sequential calls.

> **Range mode is the exception.** The API's `range_from` / `range_to` (range mode) is **not** count-capped — it is bounded only by the field magnitude (`max:999999999999999`) and `range_to > range_from`, so a range spanning millions of codes is not rejected. (The admin generator, by contrast, caps the range *span* at the plan value too.)

**Over-cap random-mode API requests** return HTTP 422 with the validation error pointing at the `limit` field.

### Validation rules that differ

Both paths require a range `from` below `to`, a length of 6-18, and a structure in random mode. The API differs in these ways:

- No numbers-only check: `limit` is limited only by the 5,000 cap.
- A range clash returns *"Some of the codes in the specified range already exist."*
- Other validation errors use the API's standard messages, not the admin form's.

See [[code-pro-generator-validation]] for the admin message reference.

### No audit log

The platform does NOT capture an audit-log row for batch generation — no actor identity, no diff, no record of which API key triggered the batch. (Same as the admin-panel path — see [[code-pro-generator-business-rules]].)

### For non-batch single-code creation

Use the standard JSON:API resource POST instead. See [[json-api-v2]] for authentication and rate-limit, and [[api-discount-codes-pro]] for the resource Schema.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[api-discount-codes-pro]] — JSON-API v2 resource (Schema, Attributes, Relationships, the `POST /generate` action).
- [[code-pro-endpoints-api]] — endpoint catalogue including this action.
- [[code-pro-generator-business-rules]] — admin-panel cap derivation (which the API does NOT honour for `> 5000`).
- [[code-pro-generator-validation]] — admin message reference.
- [[json-api-v2]] — auth, rate-limit.
- [[settings-api-keys]] — auth credentials for API callers.

## Open questions

None.
