---
type: feature
nav_path: "Marketing → Discounts → Countdown → Programmatic access"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/countdown
aliases: ["Countdown API", "Countdown GraphQL", "Countdown webhook", "Countdown JSON-API v2 unsupported", "Countdown audit log"]
tags: [marketing, discounts, countdown, api, webhooks, graphql]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, storefront popup + timer, eligibility, a second Countdown, cart totals + stacking).

# Countdown discount — programmatic access (API, GraphQL, webhooks, audit)

## Purpose

This page documents what an external integration can and cannot do with the Countdown discount: which API surfaces accept writes, which CRUD events fire as webhooks, and what audit trail is (and isn't) captured.

The short version: **JSON-API v2 cannot create a Countdown.** The admin form and GraphQL can. JSON-API v2 lists a Countdown as a `flat` or `percent` discount without the timer fields, and accepts update and delete by id. Webhook events fire on saves, not on the `active` switch. **No audit-log row is captured** for create / update — merchants needing a compliance trail must keep their own change log externally.

## Where to find it

- **JSON-API v2** — base path `<store>/api/v2/discounts`. A Countdown cannot be created here.
- **GraphQL** — mutations (`createDiscount`, `updateDiscount`) accept `type = countdown`; one created this way is always Percentage.
- **Webhooks** — managed at [[settings-hooks]]. Saving a Countdown fires the standard `discount.*` events.

## What the merchant can do here

The merchant (or their integrator) reaches programmatic access mainly through three surfaces:

- Configure webhook subscriptions for `discount.created` / `updated` / `deleted` in [[settings-hooks]].
- Use a GraphQL client to read or write Countdown discounts.
- Mirror Countdown saves into an external compliance log by persisting webhook payloads (no native audit-log row exists for Countdown).

The merchant CANNOT create a Countdown via JSON-API v2 (the validator allowlist excludes `countdown`) and CANNOT pull a built-in audit-log row showing who created / edited / deleted a Countdown.

## What integrations can do here

- **Read** Countdown discounts via GraphQL, or list them through JSON-API v2 without the timer fields.
- **Create / update / delete** Countdown discounts via GraphQL. JSON-API v2 can update or delete one by id, but not create one.
- **Subscribe** to `discount.created` / `discount.updated` / `discount.deleted` webhooks to mirror state into a downstream system.

### What integrations CANNOT do here

- Create Countdown discounts through JSON-API v2 (`<store>/api/v2/discounts`) — the validator allowlist excludes `countdown` from `discount_type`, and the resource has no timer fields.
- Pull an audit-log row showing who created / edited / deleted a Countdown — no actor identity, request source, or diff is captured.

## Settings & fields

### JSON-API v2 — cannot create a Countdown

The JSON-API v2 `discounts` resource validator allowlist for the `discount_type` attribute is: `flat`, `percent`, `shipping`, `fixed`, `code-pro`. **`countdown` is NOT in the allowlist.**

A POST with `discount_type = countdown` via `<store>/api/v2/discounts` fails with a validation error. An existing Countdown is listed as `flat` or `percent`, without the timer fields, and update and delete by id work on it.

Integrations that need to create Countdown campaigns use GraphQL (below) or the admin form.

See [[api-discounts]] for the full JSON-API v2 discount resource.

### GraphQL — writable

The GraphQL `Discount` resource supports `createDiscount` / `updateDiscount` mutations with `type = countdown`. A Countdown created this way is stored as `percent`. The Discount type exposes the countdown-specific metadata fields:

- `countdownMinutes`
- `countdownPopupEffect`
- `countdownDescription`

Authentication uses an admin session token or a personal access token, NOT the merchant-facing JSON-API v2 key.

A mutation creating a second Countdown is accepted — see [[countdown-discount-single-instance]].

### Webhook events

Saving a Countdown discount fires the standard [[settings-hooks]] `discount.*` events:

| Event | When | Payload |
|-------|------|---------|
| `discount.created` | A Countdown is created (via admin SPA or GraphQL). | The Discount record, with `countdown_minutes`, `countdown_description`, `countdown_popup_effect` in the meta payload `(verify)`. |
| `discount.updated` | A Countdown is edited and saved through the form, JSON-API v2 or GraphQL. | The updated Discount. |
| `discount.deleted` | A Countdown is deleted through JSON-API v2. | The deleted Discount's last state. |

The `active` switch in the list, bulk status, list delete, `changeDiscountsStatus`, `discountsBulkDelete` and the expiry sweep send none.

### No audit-log row for Countdown CRUD

There is **no audit-log row** captured for create / update / delete on Countdown — the platform does not record actor identity, request source, or a diff. Merchants who need a compliance trail must keep their own change log externally (e.g., by subscribing to the webhook events and persisting the payloads).

This is the same behaviour as other discount types — discount CRUD is generally not audit-logged.

## Business rules

### Each path validates separately

GraphQL and JSON-API v2 do not run the admin form's checks, such as the limit of 100 on a percent (see [[countdown-discount-editor]]). JSON-API v2 does not store the **Save the discount on your order** setting.

### Webhook payload includes meta_data fields

The three Countdown-specific fields (`countdown_minutes`, `countdown_description`, `countdown_popup_effect`) are stored as `meta_data` entries on the discount row but DO appear in the webhook payload `(verify)`. Integrations subscribing to `discount.created` / `discount.updated` can read them directly from the payload `(verify)`.

### JSON-API v2 read DOES surface Countdown

GET `<store>/api/v2/discounts` lists all discounts, a Countdown included, as `flat` or `percent`. The timer fields are not in the response.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-editor]] — the admin form and its checks.
- [[countdown-discount-single-instance]] — what happens with a second Countdown.
- [[settings-hooks]] — webhook subscription management.
- [[api-discounts]] — the JSON-API v2 discount resource, which cannot create a Countdown.

## Open questions

None.
