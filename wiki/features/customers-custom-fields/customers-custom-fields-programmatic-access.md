---
type: feature
nav_path: "Customers → Custom fields → Programmatic access"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Custom fields API", "Custom fields plan gates", "Custom fields permission", "Customer custom fields JSON-API"]
tags: [customers, custom-fields, json-api, plan-gates, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — programmatic access

> Part of [[customers-custom-fields]]. See the hub for the other aspects (list view, editor modal, types, system linkage, validation & storage, storefront behaviour).

## Purpose

This aspect documents what an integrator can — and cannot — do via the public JSON-API v2 for customer custom fields, plus the plan gating and permission model that govern access to the admin page itself. The headline answer is: **definitions are admin-only**, and there is **no plan-tier cap** on the number of fields.

## Where to find it

- **Admin UI**: `/admin/customers/custom-fields` (see [[customers-custom-fields-list-view]]).
- **JSON-API v2**: no public endpoint for custom-field definitions (see below).
- **Permission middleware**: `customers` + `customers.custom_fields` — applied to every admin route on this resource.

## What the merchant can do here

### Via the admin UI

- Full CRUD on custom-field definitions through the editor modal — see [[customers-custom-fields-editor-modal]].
- Bulk delete via the list page — see [[customers-custom-fields-list-view]].
- View stored customer answers per customer on [[customers-details]], or in aggregate via segments / filters — see [[customers-custom-fields-storefront-behaviour]].

### Via JSON-API v2

- **No public CRUD on definitions.** The custom-field definitions managed on this page are admin-only configuration with no public resource for create / read / update / delete.
- **Limited read of stored values** per customer may be available on the customer resource — verify per the API reference. Creating / updating those values for a given customer is **not** a separately documented operation in JSON-API v2.
- The canonical paths for writing stored values are: (a) storefront checkout (for customers), and (b) the admin Edit Customer modal (for staff). Merchants who need to bulk-populate custom-field values for existing customers should contact CloudCart support.

### Bulk operations

There is no bulk-import surface for custom-field definitions — every field must be created one at a time through the editor modal. The list page does support **bulk delete** via the table actions toolbar (see [[customers-custom-fields-list-view]]).

## Settings & fields

### Permission model

| Permission | What it grants |
|------------|----------------|
| `customers` | Access to the Customers section in general. |
| `customers.custom_fields` | Access to the Custom fields page at `/admin/customers/custom-fields`. |

The list page requires both permissions. Moderators with read-only grants see the table but the Create / Edit / Delete actions are disabled — write grants are a separate setting on the role.

The list page is **permission-gated**, not plan-gated — see the next section.

### Plan gating

This feature is **NOT plan-gated** (verified against backend). See [[plan-gates]] for the gating-concept overview.

| Mapping | Shape | What it controls |
|---------|-------|------------------|
| (none) | — | No plan-feature mapping exists for customer custom fields. |

Lower-tier plans see the same Custom fields page as Enterprise plans here. The merchant can create as many definitions as their workflow requires; the only practical caps are:

- **Server-side validation rules** — 191-character max on Name and Storefront name, uniqueness on both (see [[customers-custom-fields-validation-storage]]).
- **DB primary-key size** on the shared `form_fields` table — effectively unlimited at merchant scale.
- **Storefront UX** — too many fields at checkout will hurt conversion, but the platform doesn't enforce a hard limit.

There is also **no plan-tier limit on the number of stored customer answers** — the answers table grows linearly with the customer count.

## Business rules

### Definitions are admin-only

Custom-field definitions (the entries this page manages — Dropdown / Radio / Checkbox / Text / Phone / URL fields and their option values) are NOT exposed in JSON-API v2. The CRUD lives behind the admin permission middleware. Integrators that need to provision fields per merchant must do so through the admin UI (or via an API key with admin-equivalent access, where available).

### Customer tags are a different concept

A separate resource exists for **customer tags** — see [[api-customer-tags]]. Tags and custom fields look similar at first glance but serve different purposes:

| Concept | Shape | Use case |
|---------|-------|----------|
| **Custom fields** (this page) | Typed checkout-form inputs with options, validation, system-linkage | Collect structured data from customers at checkout |
| **Customer tags** ([[api-customer-tags]]) | Free-form many-per-customer string labels | Segmentation, internal classification, marketing filters |

Don't confuse the two when integrating: tags ARE exposed via JSON-API v2 (create / read / update / delete on the tag resource); custom-field definitions are NOT.

### Stored values: partial read, no documented write

The customer resource in JSON-API v2 *may* surface custom-field answers in its response payload (verify per the API reference for the exact shape). There is **no documented write operation** for those values — i.e., an integrator cannot POST to a custom-field-value endpoint to set a customer's answer programmatically. The values flow into the answers table via the storefront checkout submit and the admin Edit Customer modal only.

For bulk imports (e.g., migrating from another platform), the merchant should contact CloudCart support — there is no DIY API path.

### Storefront flush still applies

When the underlying field definitions change via the admin UI, the storefront checkout cache is flushed — see [[customers-custom-fields-storefront-behaviour]]. This is an admin-side side effect; no integrator action is required even if the change was triggered by an internal automation.

### See also: side-effects principle

The JSON-API v2 side-effects principle (write operations flush relevant caches; idempotency guarantees; sequential transaction semantics) is documented at [[json-api-v2]]. The fact that custom-field definitions are not exposed there does not affect the side-effects of writes to other resources that touch customer data.

### When in doubt: prefer the admin UI

For one-off definition changes the admin UI at `/admin/customers/custom-fields` is the canonical path. For bulk customer-data work the merchant should contact CloudCart support rather than build a workaround on top of the public API.

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-list-view]] — admin UI for browsing / reordering / deleting.
- [[customers-custom-fields-editor-modal]] — admin UI for create / edit.
- [[customers-custom-fields-storefront-behaviour]] — how values flow in via the storefront checkout.
- [[customers-custom-fields-validation-storage]] — what server-side rules apply on any write.
- [[json-api-v2]] — authentication and side-effects principle.
- [[api-customer-tags]] — different concept (tags vs custom fields).
- [[plan-gates]] — gating-concept overview.

## Open questions

- Exactly which custom-field answer attributes appear on the JSON-API v2 customer resource? (Inherited from the original page — verify per the API reference.)
