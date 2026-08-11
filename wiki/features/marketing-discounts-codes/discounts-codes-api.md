---
type: feature
nav_path: "Marketing → Discounts → Container codes → JSON-API"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container codes API", "Container codes JSON-API", "Programmatic code generation", "Container codes no audit log", "API за промо кодове"]
tags: [marketing, discounts, coupons, container, json-api, programmatic]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Container codes — programmatic access (JSON-API v2)

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, redemption, and parent-term inheritance.

## Purpose

Container codes can be managed without the admin panel via **JSON-API v2** — list, create, toggle active, and delete. This aspect covers what the API exposes, the side-effects it shares with the admin actions, the absence of an audit log, and the fact that the 1,000-per-request cap does not apply to API-driven generation.

## Where to find it

The endpoints, attributes, and validation are documented on [[api-discount-codes]]. Each row in the API corresponds to one code row — a single child code under a parent Container discount. Authentication and rate-limit conventions are on [[json-api-v2]].

## What the merchant can do here

- **List** the store's Container codes.
- **Create** individual child codes under a parent Container (one at a time, or batched via JSON:API atomic operations).
- **Toggle** a code's `active` flag.
- **Delete** a code.

## Settings & fields

The API attributes mirror the code row's fields (`code`, `type`, `value`, `active`) — see [[api-discount-codes]] for the full attribute list and validation. The parent-derived terms are not on the code resource; they live on the parent Container discount (see [[discounts-codes-parent-terms]]).

## Business rules

### Same side-effects as the admin panel

A POST / PATCH / DELETE through JSON-API v2 triggers the same pipeline as the admin-panel actions:

- The parent Container's `uses` counter is recomputed (a queued background process) whenever a child code redemption reaches a counted status — same recompute described on [[discounts-codes-parent-terms]].
- The per-row `active` toggle is reflected identically at checkout lookup (see [[discounts-codes-redemption]]).
- The `discount.created` / `discount.updated` / `discount.deleted` webhooks emit — see [[settings-hooks]].

### No audit log

The platform does **not** capture an audit-log row for Container code create / update / delete — no actor identity, no diff. (Older wiki phrasing claimed an `api2` source tag was written; that claim was incorrect.)

### No built-in 1,000-per-request cap

API-driven generation has **no** built-in 1,000-per-request cap — that cap is a server-side validator on the **legacy** admin generator only (the modern Vue modal is also uncapped; see [[discounts-codes-generator]]). Programmatic clients may push child codes one at a time, or batch via JSON:API atomic operations, and are subject only to the parent Container's `discount_coupon` plan-feature counter consumption. When that quota is exhausted, the create call returns **HTTP 403 Forbidden** with an upgrade-required plan message (built from the plan-feature mapping, not a literal "Not supported by plan" string; older wiki phrasing said 402, corrected).

## Related

- [[marketing-discounts-codes]] — hub.
- [[api-discount-codes]] — endpoints, attributes, and validation for the code resource.
- [[json-api-v2]] — authentication, rate-limits, and the same-side-effects principle.
- [[settings-hooks]] — the discount webhooks that fire on API writes.

## Open questions

No outstanding questions.
