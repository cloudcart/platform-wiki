---
type: feature
nav_path: "Marketing → Discounts → Countdown → Programmatic access"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/countdown
aliases: ["Countdown API", "Countdown GraphQL", "Countdown webhook", "Countdown JSON-API v2 unsupported", "Countdown audit log"]
tags: [marketing, discounts, countdown, api, webhooks, graphql]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, storefront popup + timer, eligibility, single-instance rule, cart totals + stacking).

# Countdown discount — programmatic access (API, GraphQL, webhooks, audit)

## Purpose

This page documents what an external integration can and cannot do with the Countdown discount: which API surfaces accept writes, which CRUD events fire as webhooks, and what audit trail is (and isn't) captured.

The short version: **JSON-API v2 cannot write Countdown.** Only the admin SPA save path and the GraphQL admin-session mutations can create / update / delete Countdown discounts. Webhook CRUD events fire normally. **No audit-log row is captured** for create / update — merchants needing a compliance trail must keep their own change log externally.

## Where to find it

- **JSON-API v2** — base path `<store>/api/v2/discounts`. Countdown is NOT supported.
- **GraphQL** — admin-session mutations (`createDiscount`, `updateDiscount`) accept `type = countdown`.
- **Webhooks** — managed at [[settings-hooks]]. Countdown CRUD fires the standard `discount.*` events.

## What the merchant can do here

The merchant (or their integrator) reaches programmatic access mainly through three surfaces:

- Configure webhook subscriptions for `discount.created` / `updated` / `deleted` in [[settings-hooks]].
- Use a GraphQL admin-session client to read or write Countdown discounts (admin session cookies required).
- Mirror Countdown CRUD into an external compliance log by persisting webhook payloads (no native audit-log row exists for Countdown).

The merchant CANNOT provision Countdown via JSON-API v2 (the validator allowlist excludes `countdown`) and CANNOT pull a built-in audit-log row showing who created / edited / deleted a Countdown.

## What integrations can do here

- **Read** Countdown discounts via GraphQL (admin session) or via direct DB queries.
- **Create / update / delete** Countdown discounts via GraphQL with admin-session cookies — NOT via JSON-API v2.
- **Subscribe** to `discount.created` / `discount.updated` / `discount.deleted` webhooks to mirror state into a downstream system.

### What integrations CANNOT do here

- Create or update Countdown discounts through JSON-API v2 (`<store>/api/v2/discounts`) — the validator allowlist excludes `countdown` from the writable `type` enum.
- Pull an audit-log row showing who created / edited / deleted a Countdown — no actor identity, request source, or diff is captured.

## Settings & fields

### JSON-API v2 — NOT writable for Countdown

The JSON-API v2 `discounts` resource validator allowlist for the `type` attribute is: `flat`, `percent`, `shipping`, `fixed`, `code-pro`. **`countdown` is NOT in the allowlist.**

Attempting to POST or PATCH with `type = countdown` via `<store>/api/v2/discounts` fails the validator with a `type` validation error. There is no JSON-API v2 path to create, update, or delete a Countdown discount.

Integrations that need to provision Countdown campaigns must use GraphQL with admin-session cookies (below) or drive the admin SPA's save path directly.

See [[api-discounts]] for the full JSON-API v2 discount resource.

### GraphQL — writable via admin-session

The GraphQL `Discount` resource supports `createDiscount` / `updateDiscount` mutations with `type = countdown`. The Discount type exposes the countdown-specific metadata fields:

- `countdownMinutes`
- `countdownPopupEffect`
- `countdownDescription`

Authentication uses admin-session cookies, NOT the merchant-facing JSON-API v2 key.

The GraphQL save path runs the same uniqueness validator as the admin form — see [[countdown-discount-single-instance]]. A mutation creating a second Countdown is rejected the same way.

### Webhook events

CRUD on a Countdown discount fires the standard [[settings-hooks]] `discount.*` events:

| Event | When | Payload |
|-------|------|---------|
| `discount.created` | A Countdown is created (via admin SPA or GraphQL). | The Discount record, with `countdown_minutes`, `countdown_description`, `countdown_popup_effect` in the meta payload. |
| `discount.updated` | A Countdown is edited OR its `active` is toggled. | The updated Discount. |
| `discount.deleted` | A Countdown is deleted. | The deleted Discount's last state. |

Webhook receivers must be idempotent — the `active` toggle (which is cooldown-free for Countdown — see [[countdown-discount-single-instance]]) can fire `discount.updated` many times in quick succession.

### No audit-log row for Countdown CRUD

There is **no audit-log row** captured for create / update / delete on Countdown — the platform does not record actor identity, request source, or a diff `(verify)`. Merchants who need a compliance trail must keep their own change log externally (e.g., by subscribing to the webhook events and persisting the payloads).

This is the same behaviour as other discount types — discount CRUD is generally not audit-logged.

## Business rules

### GraphQL and admin SPA share the validator

Both the GraphQL mutation path and the admin SPA save path run the same backend validator. The uniqueness check, the `only_customer` REQUIRED rule, and the `type_value` validator-branch quirk (see [[countdown-discount-editor]]) all apply identically.

### Webhook payload includes meta_data fields

The three Countdown-specific fields (`countdown_minutes`, `countdown_description`, `countdown_popup_effect`) are stored as `meta_data` entries on the discount row but DO appear in the webhook payload. Integrations subscribing to `discount.created` / `discount.updated` can read them directly from the payload.

### `active` toggle fires `discount.updated`

Each `active` flip (cooldown-free for Countdown) fires a `discount.updated` webhook. A merchant who toggles `active` repeatedly while testing will produce a rapid sequence of webhooks — receivers must be idempotent.

### JSON-API v2 read DOES surface Countdown

While JSON-API v2 can't write Countdown, it CAN read all discounts including Countdown via GET `<store>/api/v2/discounts` `(verify)`. The Countdown-specific meta fields surface in the response via the included meta-data relationship.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-editor]] — the admin save path that the same backend validator backs.
- [[countdown-discount-single-instance]] — the uniqueness validator applies to GraphQL mutations too.
- [[settings-hooks]] — webhook subscription management.
- [[api-discounts]] — the JSON-API v2 discount resource that excludes Countdown from writes.

## Open questions

- Verify whether JSON-API v2 GET on `<store>/api/v2/discounts` returns Countdown rows (with their meta fields), or excludes them from the listing entirely `(verify)`.
- Confirm the absence of any audit-log row for Countdown CRUD across all save paths `(verify)`.
