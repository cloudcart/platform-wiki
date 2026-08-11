---
type: feature
nav_path: "Marketing → Discounts → Shipping → Plan gates & API"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Free shipping plan gates", "Shipping discount API", "Shipping discount webhooks", "Shipping discount cooldown", "discount_global", "discount_coupon"]
tags: [marketing, discounts, shipping, plan-gates, api, webhooks, cooldown]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, stacking, force-save, other zero-paths, examples).

# Shipping discount — plan gates, API, webhooks, cooldown

## Purpose

This page collects the **non-form mechanics** of the Free-shipping discount: the plan-feature quotas (`discount_global` for no-code, `discount_coupon` for code-based), the HTTP behaviour at the cap (403 Forbidden), the JSON-API v2 + GraphQL write paths, the webhook events, and the 10-minute activation cooldown.

It also corrects two pieces of older wiki phrasing: (a) the HTTP code at the cap is **403**, not 402; (b) there is **no audit-log row** for discount writes (the previously documented `api2` source tag claim was wrong).

## Where to find it

Plan-gate behaviour surfaces on the type-picker modal (Free shipping is grayed out at the cap) and on the create endpoint (`POST /admin/api/discounts` returns 403 at the cap). The 10-minute cooldown surfaces on row-level Activate/deactivate toggles in the [[marketing-discounts]] list. See [[marketing-discounts-shipping]] for the form entry-surface.

## What the merchant can do here

- Create / update / delete a shipping discount via JSON-API v2 (`<store>/api/v2/discounts`, see [[api-discounts]]).
- Create / update via GraphQL (`createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus` mutations).
- Subscribe to the `discount.created` / `discount.updated` / `discount.deleted` webhooks via [[settings-hooks]].
- (Cannot) bypass the plan-feature quota — overflow returns HTTP 403.
- (Cannot) toggle a no-code Free-shipping discount's `active` state more than once per 10 minutes.
- (Cannot) audit who-changed-what — there is no audit-log row for discount writes.

## Settings & fields

Plan-feature quotas (read-only from the merchant's perspective; consumed by every create that lands):

| Mapping | Shape | What it controls |
|---|---|---|
| `discount_global` | Numeric quota | Counts non-code (always-on / order-over) Free-shipping discounts toward the **codeless-discount** cap. Same counter is shared with Global discounts and Countdown discounts — see [[plan-gates]] for the codeless-vs-coupon split. Also path-gates the create-discount entry point at `discounts/add` via `plan.restrict.access`. |
| `discount_coupon` | Numeric quota | Counts code-based Free-shipping discounts (Promo code path) toward the **code-based-discount** cap. Same counter is shared with all other code-based discounts (Code PRO, Container, Promo). Also path-gates the code-based create endpoint at `discounts/add/code`. |

Behaviour: lower plans get redirected to the per-feature upsell at [[plan-features]] or to a plan-upgrade panel. Both gates are numeric — they extend via packs ([[plan-vs-feature-pack]]). The cap counts only ACTIVE discounts; deleting / deactivating a discount frees a slot.

The type-picker modal grays out "Free shipping" if the merchant's plan has hit either cap (depending on which sub-type — codeless vs code-based — the merchant attempts). The platform's `discount.code-pro` boolean gate does NOT apply to shipping discounts.

## Business rules

### Plan-gating — counters and HTTP behaviour at the cap

Free-shipping discounts count toward two plan-feature quotas depending on whether they carry a code:

- A **non-code (Global) free-shipping discount** counts toward the `discount_global` quota (shared with no-code Flat and Percent discounts).
- A **code-based free-shipping discount** counts toward the `discount_coupon` quota (shared with all code-based variants).

The type-picker modal grays out "Free shipping" when the merchant's plan has hit either cap. A create attempt at the cap returns **HTTP 403 Forbidden** with the *"Not supported by plan"* message (older wiki phrasing said 402; corrected).

### Activation rate-limit (10-minute cooldown — no-code shipping only)

Toggling a **no-code** Free-shipping discount's `active` state is rate-limited to **once per 10 minutes per discount**. Within the cooldown window:

> *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."*

The cooldown exists because toggling triggers a per-product attachment regeneration cycle. The throttle prevents thrashing the background queue.

**Scope clarification:** the cooldown applies to **no-code** Flat / Percent / Shipping / Fixed discounts only. **Code-based shipping coupons have NO cooldown** — neither do Container, Quantity, Countdown, or Code PRO. See the per-type cooldown table on [[discount-stacking]].

### Webhook events

CRUD fires the same platform-wide [[settings-hooks]] events as the rest of the discount engine:

| Event | When | Payload |
|-------|------|---------|
| `discount.created` | A shipping discount is created. | The Discount record. |
| `discount.updated` | A shipping discount is edited or its `active` is toggled. | The updated Discount. |
| `discount.deleted` | A shipping discount is deleted. | The deleted Discount's last state. |

### JSON-API v2 — REST endpoint

Resource: `discounts` (see [[api-discounts]]). Full CRUD plus status toggle. Both no-code (always-on / `order_over` free shipping) and code-based variants are supported via the same resource — set the `code` attribute to switch between them. The base URL is `<store>/api/v2/discounts`, authenticated with the standard Site ID + API key headers per [[settings-api-keys]].

The validator allows `type ∈ {flat, percent, shipping, fixed, code-pro}` on this endpoint — Quantity and Countdown discounts are NOT writable via JSON-API v2.

### GraphQL — admin-session endpoint

Resource: `Discount` (mutations: `createDiscount`, `updateDiscount`, `discountsBulkDelete`, `changeDiscountsStatus`). Same field set as the admin panel; uses admin-session authentication.

### Same side effects regardless of source

A create / update through JSON-API v2 or GraphQL triggers the **same pipeline** as the admin-panel save:

- All validation rules apply: the `type_value`-must-be-empty rule for shipping discounts is enforced (rejects with *"Type value must be empty"*); the `force_save` toggle is required for `type=shipping` (rejects without it); the parent-child category combination rejection; the 10,000-combinations cap.
- Plan-feature usage counters consume (`discount_global` for no-code, `discount_coupon` for code-based) — overflow returns **HTTP 403 Forbidden** with *"Not supported by plan"*.
- Per-product attachment regeneration runs.
- The `discount.created` / `discount.updated` webhooks emit (see [[settings-hooks]]).
- The 10-minute activation cooldown applies on subsequent status-toggle attempts (no-code shipping only).

### No audit-log row for discount writes

There is **no audit-log row** captured for the create / update — the platform does not record actor identity, request source (admin vs API), or a diff. Older wiki phrasing claimed an `api2` source tag — that claim was incorrect; no audit log exists for discounts.

For support tickets that ask "who created this discount" or "when did this discount change", the only signals available are:

- The `created` / `updated` timestamps on the Discount record itself.
- Webhook delivery logs (if the merchant captures them on their side).
- Indirect: orders that consumed the discount have a timestamp.

There is no in-product audit screen for discount history.

### Cart-engine selection rules apply identically

Only ONE shipping discount applies per cart at totals time — the first match in the no-code shipping pool returns (unspecified order, NOT sorted by `order_over DESC` as older wiki phrasing claimed). For predictable behaviour, the merchant should avoid overlapping no-code Free-shipping discounts. See [[shipping-discount-stacking]] for the full selection rules.

### Permissions

The form and CRUD endpoints are scoped under the standard `marketing.discounts` permission.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[api-discounts]] — JSON-API v2 resource for discount CRUD.
- [[settings-hooks]] — `discount.created` / `updated` / `deleted` webhook events.
- [[settings-api-keys]] — Site ID + API key auth for JSON-API v2.
- [[plan-gates]] — codeless-vs-coupon split + plan-gate model.
- [[plan-features]] — per-feature upsell screen.
- [[plan-vs-feature-pack]] — extending quotas via packs.
- [[discount-stacking]] — per-type 10-minute-cooldown table.

## Open questions

None.
