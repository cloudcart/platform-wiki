---
type: feature
nav_path: "Apps → Membership → API endpoints"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership API", "Membership endpoints", "addExtraDays", "createSubscription", "Membership install hook"]
tags: [apps, administration, membership, api]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Membership — API endpoints

> Part of [[apps-membership]]. See the hub for the other aspects (data model, purchase flow, renewal/revocation, records admin).

## Purpose

This aspect catalogues the **internal API endpoints** the Membership module exposes and the Manager surface it registers. These are the endpoints the admin modals call (see [[apps-membership-records-admin]]) and the hooks the platform calls on install / order events. This is module-internal plumbing, not the public JSON-API v2.

## Where to find it

These endpoints are not merchant-facing screens — they back the Settings-tab modals and the install / order lifecycle. The merchant interacts with them indirectly through the UI.

## What the merchant can do here

- Nothing directly — the merchant uses the [[apps-membership-records-admin]] UI, which calls these endpoints on the merchant's behalf.

### What the merchant CANNOT do here

- There is no documented public-API surface for membership; these are internal module routes.

## Settings & fields

The module Manager exposes:

- `getMigrationsPath` — DB migrations for the membership tables (run on install).
- `appInfo` — App Store metadata.

The integration creates DB tables for the membership records on install (see [[apps-membership-data-model]] for the record shape).

## Business rules

### The 5 endpoints

Per the module routes:

- `GET /api/membership/subscriptions` — list all memberships.
- `POST /api/membership/install` — install hook.
- `POST /api/membership/uninstall` — uninstall hook.
- `POST /api/membership/add-extra-days` — extend an existing membership by N days (the Extra Days modal / renewal flow).
- `POST /api/membership/create` — manually create a membership (the Add Subscription modal, or a post-purchase webhook).
- `DELETE /api/membership/delete/{subscription_id}` — cancel / delete a membership (the per-row delete action).

### `add-extra-days` is the renewal mechanism

Instead of creating a NEW membership on renewal, the platform extends the existing membership's `expired` timestamp via `add-extra-days`. This keeps a cleaner audit trail — one record per customer-product-page combo rather than a new row per renewal. The order-driven grant flow uses the same extend-in-place behaviour (see [[apps-membership-purchase-flow]] for expiry stacking).

### `create` is also the manual / gift path

`POST /api/membership/create` is what the Add Subscription modal posts to. It is also the path a merchant would use for a manual gift workflow (creating a membership for a recipient after a gift purchase), since there is no built-in gift flow (see [[apps-membership-data-model]]).

### Install / uninstall hooks

`install` runs the migrations and registers the module; `uninstall` tears it down. These fire from the App Store install / uninstall actions, not from any merchant button inside the app itself.

## Related

- [[apps-membership]] — hub.
- [[apps-membership-records-admin]] — the UI that calls create / add-extra-days / delete.
- [[apps]] — App Store install / uninstall that fires the hooks.

## Open questions

None.
