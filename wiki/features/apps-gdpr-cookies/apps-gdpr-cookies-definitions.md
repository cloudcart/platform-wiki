---
type: feature
nav_path: "Apps → GDPR → Cookies → Cookie definitions"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Cookie definitions", "Add cookie modal", "Cookie name", "Cookie description", "cookies_table placeholder", "Cookie mapping slug", "No auto cookie scan"]
tags: [apps, gdpr, compliance, cookies, consent, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# GDPR — Cookies: cookie definitions

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, groups, consent mode, consent state).

## Purpose

This aspect documents the **individual cookie definitions** the merchant lists inside each group — the rows the visitor sees when they expand a group in the consent modal. It covers the add/edit modal and its three fields, the auto-generated `mapping` slug and the duplicate-rejection rule, one-click deletion, the `{cookies_table}` storefront placeholder, and the important non-feature: the platform does **not** scan and auto-classify cookies. The groups these definitions belong to are covered on [[apps-gdpr-cookies-groups]].

## Where to find it

Sidebar → Apps → GDPR → **Cookies tab** (`/admin/apps/gdpr/cookies`). Each group's accordion lists its cookies as a table; an "add cookie" action and a per-row edit/delete icon open the modal (`AddOrEditCookieModal.vue`).

## What the merchant can do here

- Add a cookie definition to a group (name, description, technical cookie names).
- Edit or delete an existing definition.
- Insert the `{cookies_table}` placeholder into any storefront page to render the full cookie table (useful for a Cookie Policy page).

## Settings & fields

### Add / edit cookie modal (`AddOrEditCookieModal.vue`) — 3 fields only

The per-cookie modal is far simpler than typical cookie-policy editors. It exposes exactly three fields:

| Field | Component | Notes |
|---|---|---|
| **Cookie name** (`cookie.name`, required, max 191) | InputComponent | The display label of the row (e.g., "Google Analytics"). |
| **Cookie description** (`cookie.description`) | TextareaComponent | What the cookie does / why it is set. Free-form text, no HTML editor. |
| **Cookies** (`cookie.cookies`, tag input) | SelectWithAjax, `mode="tags"` | The TECHNICAL cookie names (`_ga`, `_gid`, `cf_clearance`, etc.) — comma-separated tags, press Enter to add. Disabled when `group.type !== 'cookie'` (informational-only groups). |

**There are NO fields for vendor, duration, expiry, or domain** — those concepts don't exist in the modal. The merchant captures vendor + duration + domain as prose inside the free-form **description**; the storefront renders that description verbatim and does not structure or surface it separately.

## Business rules

### `mapping` slug is auto-generated + duplicates are rejected

Save fires `POST /api/gdpr/cookies/edit-cookie-consent/{group_id}/{cookie_id?}` (`cookie_id` present on edit, absent on create). The server generates a `mapping` slug from `name + cookies` (lowercase, underscore-separated) and **rejects duplicates within the same group** with a validation error — the merchant cannot register the same cookie twice. Field-level errors surface inline on the modal (`responseErrors['name']`, `['description']`, `['cookies']`).

### Deletion is one-click + no soft-delete

A delete icon on each cookie row fires `GET /api/gdpr/cookies/delete-cookie-consent/{cookie_id}` immediately — there is no confirmation modal and no recoverable trash. The storefront cookie JS regenerates on save (see [[apps-gdpr-settings]]).

### `{cookies_table}` placeholder for storefront pages

When the merchant inserts the `{cookies_table}` placeholder into any storefront page's content, the platform replaces it with a rendered cookie table listing all active groups + their cookies — useful for a Cookie Policy page. The table reflects the visitor's **current** consent state: groups they have accepted show as "accepted".

### No auto cookie scan — definitions are merchant-managed

There is no scan-storefront-and-classify automation. When the merchant installs a tracking app (Google Analytics, Facebook Pixel, etc.) the cookies those scripts set are NOT auto-discovered. The merchant must manually add each definition to the appropriate group. Because consent is stored per group, not per cookie, adding a NEW cookie to an existing group does not re-prompt visitors — see [[apps-gdpr-cookies-consent-state]] for the re-consent rules.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-groups]] — the groups these definitions live inside.
- [[apps-gdpr-cookies-consent-state]] — why adding a cookie does not force re-consent (referenced inline above).
- [[apps-gdpr-settings]] — GDPR app settings; storefront cookie JS regenerates on save.

## Open questions

None.
