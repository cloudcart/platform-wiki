---
type: feature
nav_path: "Orders → Export → Permissions + plan"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Orders export permission", "orders.export grant", "Export plan gate", "export_orders plan feature", "Orders export staff role"]
tags: [orders, export, permissions, staff, plan-gates]
plan_gates: ["export_orders"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-export]]. See the hub for related aspects (trigger / 2FA, sync vs async, CSV schema, delivery, filter scope).

# Orders export — permissions + plan gating

## Purpose

Documents **who can see and trigger the Export button** — the staff permission grant (`orders.export`) and the plan-feature mapping (`export_orders` — registered but NOT effective due to a URL-pattern mismatch with the live route). The takeaway: every plan tier can run the orders export; gating is purely permission-based.

## Where to find it

- Staff permission: [[settings-staff]] → edit moderator → grant the `orders` permission section + `orders.all` permission group + `orders.export` permission grant.
- Plan-feature: registered in the platform's plan configuration under the key `export_orders` — but see "Business rules" for why it is not enforced.

## What the merchant can do here

- Grant / revoke the `orders.export` permission to moderators from [[settings-staff]].
- View / verify the moderator's effective permissions on their staff edit page.

The merchant CANNOT change the plan-feature registration (it's a platform-level config), nor escalate `orders.export` from anywhere outside the staff permission framework.

## Settings & fields

### Permission grants required

| Grant | What it controls |
|---|---|
| `orders` (permission section) | Visibility of the Orders sidebar item and access to [[orders]]. |
| `orders.all` (permission group) | Access to all orders rows (not scoped down to a subset). |
| `orders.export` (permission grant) | Visibility of the Export button on the orders list header + access to the export endpoint. |

Moderators without all three grants don't see the Export button. The endpoint also rejects the request if the permission check fails server-side — the button visibility and the endpoint gate are two layers of the same permission.

### Plan-feature mapping — `export_orders`

The platform's plan-feature configuration registers `export_orders` under `restrict.access` mapped to the URL pattern `orders/export/orders`. However, the actual export endpoint is `/admin/api/core/export-import/export_orders` — after the plan middleware strips `/admin/`, the URI it checks is `api/core/export-import/export_orders`, which does **NOT** match the registered `orders/export/orders` pattern.

So **the middleware never matches this route and never gates the export**. The `export_orders` mapping appears to be a legacy / placeholder entry pointing at a URL that no longer corresponds to a live route. If the URL ever matched, `export_orders` would behave as a boolean access gate; it does NOT extend via feature packs (see [[plan-vs-feature-pack]]).

## Business rules

### Plan gating is NOT effective

In practice the orders export is **NOT plan-gated** — every plan tier can run it. The only real gate on reaching the Export button is staff permission (`orders` + `orders.all` + `orders.export`). The `export_orders` mapping is a platform-config artefact that does not actually enforce anything against the live export endpoint.

This is a known quirk surfaced to support when a merchant on a lower plan asks "why can I export?" — the answer is "the gate isn't wired up; this is intentional behaviour at the platform-config level." If the platform ever realigns the URL pattern, the feature could become enforced.

### Permission applies to the endpoint, not just the button

Hiding the Export button via permission also gates the underlying endpoint — a moderator without `orders.export` who manually navigates to `/admin/api/core/export-import/export_orders` is rejected by the permission middleware. The button visibility and the endpoint access check are the same permission, applied twice (UI + server).

### 2FA is independent of permission

The 2FA modal (see [[orders-export-trigger-2fa]]) is driven by the admin's personal 2FA configuration (`cc2fa_secret` for TOTP, `2fa_email` platform flag for email-2FA), **NOT** by the staff permission grant. A moderator with `orders.export` granted and no 2FA configured runs the export without any verification step (when the store-level `2fa_email` flag is also OFF).

### Per-admin permission, per-admin 2FA

Both layers are per-admin:

- **Staff permission** — granted per moderator from [[settings-staff]].
- **2FA configuration** — set per admin (TOTP via `cc2fa_secret`, email-2FA via the store flag + admin enrollment).

A team with multiple moderators may have different export experiences: one moderator may face the 2FA modal, another may not — even though both can hit the same Export button.

## Related

- [[orders-export]] — hub.
- [[orders-export-trigger-2fa]] — the 2FA layer that runs on top of the permission check.
- [[settings-staff]] — where the `orders.export` grant is administered.
- [[plan-gates]] — plan-feature framework overview.
- [[plan-features]] — the registry where `export_orders` is defined.
- [[plan-vs-feature-pack]] — contrast: this feature would be a boolean access gate (if it were enforced), NOT a feature-pack extension.

## Open questions

None.
