---
type: feature
nav_path: "Customers → Customer groups → Programmatic access"
route_name: customers-custom-groups
route_path: /admin/customers/groups
aliases: ["Customer groups API", "Customer groups JSON-API", "Programmatic customer groups", "Customer group API protection", "API клиентски групи"]
tags: [customers, groups, api, json-api-v2, programmatic]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# Customer groups — programmatic access (JSON-API v2)

> Part of [[customers-custom-groups]]. See the hub for the other aspects (manage, system groups, plan gating, integration).

## Purpose

How customer groups are read, created, updated, and deleted through **JSON-API v2**, and the guarantee that the API enforces the **same** protection layer as the admin UI — reserved names, system-group blocks, the dual delete cascade, and the plan cap. Read this for any integration touching customer-group management.

## Where to find it

The taxonomy is managed in the UI at `/admin/customers/groups` (see [[customers-custom-groups-management]]); the programmatic equivalent is the JSON-API v2 customer-groups resource — see [[api-customer-groups]] for the full endpoint shape, attributes, and relationships.

## What the merchant can do here

Through JSON-API v2 the merchant (or their integration) can:

- **Read** the group list and individual groups.
- **Create** a group with a `name` attribute.
- **Update** a group's `name`.
- **Delete** an eligible group.

All four operations route through the same validation and side-effect layer as the admin UI — there is no "API bypass" of any business rule.

## Settings & fields

| Attribute | Notes |
|-----------|-------|
| `name` | Max 100 chars, case-insensitive unique. The only writable attribute. See [[api-customer-groups]] for the full attribute / relationship shape. |

## Business rules

### Same side effects as the admin UI

A POST / PATCH / DELETE through JSON-API v2 hits the same protection layer as the admin screen: the 24-hour group cache is invalidated on save, the Guests-lookup 1-hour cache is refreshed when applicable, and the delete validator enforces **both** the "no customers" **and** the "no referencing discounts" rules (the same dual cascade documented on [[customers-custom-groups-system-groups]]).

### Reserved-name protection applies via the API too

- Creating or renaming any group to **"Default"** (case-insensitive — `Default`, `default`, `DEFAULT`) is rejected with HTTP 422 *"Group name is reserved"*.
- Renaming the Default group itself is rejected with *"Cannot edit default group"*.
- Deleting the Default group → *"Cannot delete the default group"*; deleting Guests → *"Cannot delete the guests group"*. Both blocks are at the data layer — the API cannot bypass them.

### Plan cap enforced server-side

The cap is checked on every API write: when the total group count meets or exceeds the plan's `customer_groups` value, the API returns *"Group limit reached"* on overflow. The count **includes** the 2 system groups, so a plan offering "5 customer groups" yields 3 creatable slots — identical to the UI behaviour (see [[customers-custom-groups-plan-gating]]).

### No `customer_group.*` webhook

Group lifecycle is silent over the API as well — no dedicated group event fires. Only `customer.updated` fires when individual customers move between groups (see [[settings-hooks]] and [[customers-custom-groups-integration]]).

### Authentication, rate limit, side-effects principle

Authentication, rate limiting, and the general side-effects principle are shared across all JSON-API v2 resources — see [[json-api-v2]].

## Related

- [[customers-custom-groups]] — hub.
- [[api-customer-groups]] — the JSON-API v2 resource shape (attributes, relationships, validation).
- [[json-api-v2]] — authentication, rate limit, and the side-effects principle.
- [[customers-custom-groups-system-groups]] — the protection layer the API shares.
- [[customers-custom-groups-plan-gating]] — the plan cap enforced on API writes.
- [[customers-custom-groups-integration]] — caching + the `customer.updated` webhook.
- [[settings-hooks]] — webhook events.

## Open questions

None.
