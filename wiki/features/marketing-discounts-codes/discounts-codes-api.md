---
type: feature
nav_path: "Marketing → Discounts → Container codes → JSON-API"
route_name: discounts-codes_list
route_path: /admin/marketing/discounts/codes
aliases: ["Container codes API", "Container codes JSON-API", "Programmatic code generation", "Container codes no audit log", "API за промо кодове"]
tags: [marketing, discounts, coupons, container, json-api, programmatic]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

# Container codes — programmatic access (JSON-API v2)

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, redemption, and parent-term inheritance.

## Purpose

Container codes can be managed without the admin panel via **JSON-API v2** — list, create, update, delete, and generate in bulk. This aspect covers what the API exposes, the absence of webhooks and an audit log, and the 1,000-per-call limit on generate.

## Where to find it

The endpoints, attributes, and validation are documented on [[api-discount-codes]]. Each row in the API corresponds to one code in the shared pool. Authentication and rate-limit conventions are on [[json-api-v2]].

## What the merchant can do here

- **List** the store's Container codes.
- **Create** individual codes one at a time, or **generate** up to 1,000 with `POST /discount-codes/generate`.
- **Toggle** a code's `active` flag.
- **Delete** a code.

## Settings & fields

The API attributes are `code`, `value` (1–10000, percent × 100, so 1000 means 10%) and `active` — see [[api-discount-codes]] for the full attribute list and validation. Every code made through the API is a percent code. Target, dates and region live on the Container discounts (see [[discounts-codes-parent-terms]]).

## Business rules

### Side-effects

A POST / PATCH / DELETE through JSON-API v2 changes the same codes as the admin actions:

- A Container's `uses` counter is recounted whenever an order that used it changes status — see [[discounts-codes-parent-terms]].
- The per-row `active` toggle has the same effect at checkout (see [[discounts-codes-redemption]]).
- No webhook fires for changes to a Container code — see [[settings-hooks]].

### No audit log

The platform does **not** capture an audit-log row for Container code create / update / delete — no actor identity, no diff.

### Generate — up to 1,000 per call

`POST /discount-codes/generate` takes `count` (1–1,000) and `value` (1–10000) and creates that many percent codes. There is no plan check on this resource. To make more than 1,000, send several calls. The admin modal has no upper limit on the count (see [[discounts-codes-generator]]).

## Related

- [[marketing-discounts-codes]] — hub.
- [[api-discount-codes]] — endpoints, attributes, and validation for the code resource.
- [[json-api-v2]] — authentication and rate-limits.
- [[settings-hooks]] — discount webhooks; changes to Container codes send none.

## Open questions

No outstanding questions.
