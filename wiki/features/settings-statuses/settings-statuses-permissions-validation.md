---
type: feature
nav_path: "Settings → Statuses → (permissions & validation)"
route_name: statuses
route_path: /admin/settings/statuses
aliases: ["Statuses permission grant", "settings.statuses moderator grant", "Status backend validation", "Form Request rules statuses", "Route type constraint statuses"]
tags: [settings, statuses, permissions, validation, moderators]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-statuses]]. See the hub for the three taxonomies and the other cross-cutting mechanics (rename, custom codes, delete protection).

# Statuses — permissions & server-side validation

## Purpose

The [[settings-statuses]] page is gated by a specific permission grant for moderators (the standard `settings` permission is NOT enough), and its mutating endpoints (PATCH update, POST create, DELETE) carry a thin but specific Form Request validation layer plus route-level constraints. This page is the reference for both — what permission a moderator needs, what the server validates, and what kinds of garbage input get rejected vs. silently accepted.

## Where to find it

This aspect documents server-side behaviour for every endpoint serving [[settings-statuses]]; there is no specific admin UI for it. The endpoints are:

- `GET /statuses/<type>` — list (orders / shipping / payment).
- `PATCH /statuses/<type>/update` — rename inline. All three types allowed.
- `POST /statuses/order/create` — add custom status. **Order only.**
- `DELETE /statuses/order/<status>` — delete custom status. **Order only.**

For moderator setup, see [[settings-staff]] (the moderator-grant UI).

## What the merchant can do here

(Reference page — no direct UI. The merchant interacts with this layer through the rest of [[settings-statuses]].) The behaviour documented here:

- Determines whether a moderator can see / use the page at all (`settings.statuses` grant check).
- Determines whether a manually crafted API call to a forbidden endpoint succeeds (route-level `type` constraint).
- Determines what kinds of names / status codes are accepted (Form Request validation).

## Settings & fields

The settings the merchant configures on [[settings-staff]] that intersect this page:

| Permission | Effect |
|------------|--------|
| `settings` | Required to see the Settings sidebar entry at all. Necessary but **not sufficient** for this page. |
| `settings.statuses` | Required specifically for any endpoint serving [[settings-statuses]]. Granted via [[settings-staff]] per moderator. |

The Form Request validates these fields on each endpoint:

| Endpoint | Field | Rule | Error message |
|----------|-------|------|---------------|
| `POST /statuses/order/create` | `name` | required, non-empty | *"There is no name for the status."* |
| `PATCH /statuses/<type>/update` | `status` | required (the status code being renamed) | *"No status"* |
| `PATCH /statuses/<type>/update` | `type` | one of `order`, `shipping`, `payment` | *"Invalid type"* |
| `PATCH /statuses/<type>/update` | `name` | (no validation rule — empty is allowed, see [[settings-statuses-rename-mechanic]]) | n/a |

## Business rules

### Permission middleware — both grants required

The backend route group requires **both** `settings` AND `settings.statuses` permission grants. The owner has both implicitly. Moderators ([[settings-staff]]) need the `settings.statuses` grant explicitly checked in their permission set; without it, any endpoint here returns **HTTP 403**, even if they have generic `settings` access (i.e., they can see the Settings landing page and other sub-pages, but the Statuses link / page will 403 out).

Practical merchant consequence: a moderator who can edit other Settings sub-pages might still get a 403 on [[settings-statuses]] until the owner grants `settings.statuses` explicitly.

### Route-level `type` constraint on Create + Delete

The Create and Delete routes are explicitly constrained at the route level to `type = order` (via `->where('type', 'order')` on the route definition). The route group accepts `type` as `order|shipping|payment`, but only the **GET list** and **PATCH update** routes work for all three types.

Attempting `POST /statuses/shipping/create`, `POST /statuses/payment/create`, `DELETE /statuses/shipping/<status>`, or `DELETE /statuses/payment/<status>` returns **404 from the router** (not a soft client-side error, not a 403, not a 422 — the route simply doesn't match). This double-gates the same protection the Vue tabs enforce (no Add button, no trash icon on Shipping / Payment tabs).

### `PATCH /statuses/<type>/update` — type validation in two places

The active type is gated twice: at the route level (URL must have a valid type segment — other values 404) AND at the Form Request level (body must also carry `type` matching one of the three values — otherwise 422 *"Invalid type"*). A request to `/statuses/order/update` with `type: "shipping"` in the body would be rejected with *"Invalid type"*. *(verify — exact URL-vs-body comparison rule.)*

### Create validation — only `name` is required

On `POST /statuses/order/create`:

- `name` — **required**. Submitting an empty body returns 422 with *"There is no name for the status."*
- No `max:` cap is set on `name` in the Form Request, so very long names pass validation here but may be truncated at display time elsewhere in the admin. Truncation also applies at the slug-generation step to 240 characters — see [[settings-statuses-custom-codes]].

### Rename validation — `status` + `type` required

On `PATCH /statuses/<type>/update`:

- `status` — **required**. The status code identifier being renamed. Missing → *"No status"*.
- `type` — must be one of `order`, `shipping`, `payment`. Other values → *"Invalid type"*.
- `name` — no explicit Form Request rule. Empty string is allowed and is interpreted as "clear the override" — the backend deletes the override row entirely. See [[settings-statuses-rename-mechanic]].

### What is NOT validated by the Form Request

The Form Request layer enforces minimal rules — the table-stakes is "name not empty" on create; everything else (the slug, the code uniqueness, the type guard on create / delete) is enforced downstream at the route or model level. Notably absent:

- **No name-uniqueness check** against existing custom statuses. Two custom statuses CAN share a display name — the platform only enforces unique CODES (at slug generation). See [[settings-statuses-custom-codes]].
- **No length cap** on the name string. The slug is truncated to 240 chars; the name itself can be longer.
- **No reserved-word check.** The merchant could rename "Pending" to "Completed" — the platform won't block it, though the merchant will then have two statuses showing the same label. This is a known footgun.

### Backend gate on delete: only `type = order`

The Delete route is explicitly constrained to `type = order` (route-level `->where('type', 'order')`). Even if a request manages to construct a DELETE for a non-order taxonomy, the router won't accept it. The Delete also requires the `settings.statuses` permission grant — moderators without it get 403 regardless of any other constraint. See [[settings-statuses-delete-protection]] for the attached-orders content gate that fires after both these checks pass.

### Failure-mode summary

- Moderator lacks `settings` → 403 (sidebar item hidden too).
- Has `settings` but lacks `settings.statuses` → 403 on every endpoint here.
- `POST /statuses/{shipping,payment}/create`, `DELETE /statuses/{shipping,payment}/<x>` → 404 (route constraint).
- `POST /statuses/order/create` empty `name` → 422 *"There is no name for the status."*
- `PATCH /statuses/order/update` with `type: "shipping"` in body → 422 *"Invalid type"* *(verify)*.
- `PATCH /statuses/<type>/update` without `status` → 422 *"No status"*.
- `DELETE /statuses/order/<custom>` with attached orders → 422 *"This status has attached: `<N>`"* — see [[settings-statuses-delete-protection]].

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-orders-tab]] — Orders tab; consumes Create + Update + Delete endpoints.
- [[settings-statuses-shipping-tab]] — Shipping tab; consumes only Update.
- [[settings-statuses-payment-tab]] — Payment tab; consumes only Update.
- [[settings-statuses-rename-mechanic]] — empty `name` deletes the override row; this is by design, not a validation bypass.
- [[settings-statuses-custom-codes]] — slug uniqueness at the model layer (downstream of Form Request).
- [[settings-statuses-delete-protection]] — the attached-orders gate (fires AFTER permission + route checks pass).
- [[settings-staff]] — moderator-grant UI; where `settings.statuses` is granted.
- [[settings]] — parent hub; carries the generic `settings` grant.

## Open questions

- Whether the Form Request enforces consistency between the URL's `type` segment and the body's `type` field on PATCH (or trusts the URL alone). *(verify)*
- Whether 422 responses carry structured error keys or only the raw error string for the rename / create paths. *(verify)*
