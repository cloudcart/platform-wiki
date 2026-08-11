---
type: feature
nav_path: "Settings → Shipping → API & permissions"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping API access", "Shipping providers API", "Shipping permissions", "store.shipping permission", "settings.shipping permission", "Shipping geo zone deletion safety"]
tags: [settings, shipping, api, permissions, geo-zones]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-shipping]]. See the hub for the other aspects (list & Add modal, Custom rate types, edit panel, rate matching, lifecycle).

# Shipping — API access & permissions

## Purpose

This aspect documents the programmatic-read surface (JSON-API v2), the permission grants that gate sidebar access and integration installs, and the safety fallback when a [[settings-geo-zones|Geo zone]] in use by a shipping method is deleted from outside this page.

## Where to find it

- **JSON-API v2**: see [[api-shipping-providers]] for the endpoint and field map.
- **Permissions UI**: Sidebar → Settings → **Staff** ([[settings-staff]]) → Access permissions.

## What the merchant can do here

### JSON-API v2 — read-only

Shipping providers can be **read** via JSON-API v2 — see [[api-shipping-providers]] for the endpoint and field map. The API surface is **read-only**: integrations can list configured providers, check active state, inspect names, codes, geo-zone targets, and price configuration — but configuration changes (adding new methods, editing rate rows, toggling active, deleting) must happen through the admin Shipping screen.

**Important quirk:** the API exposes both Custom rate methods AND integration-backed providers in the same list — they're distinguished by the `app_id` reference. Geo-zone references resolve to numeric IDs only; the consumer needs a second call to [[settings-geo-zones]] data to get human-readable region names.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

### Permissions — two grants

| Grant | Where granted | What it gates |
|-------|--------------|---------------|
| `settings` or `settings.shipping` | [[settings-staff]] → Access permissions | The sidebar entry **Settings → Shipping**. Moderators without the grant don't see this entry in the sidebar. |
| `store.shipping` | [[settings-staff]] → Access permissions | API-endpoint-level enforcement inside most individual integration apps (Speedy, Econt, DPD, GLS, Fan Courier, DHL Express, Cargus, etc.). |

A moderator who can SEE the Shipping list but lacks `store.shipping` will get **403** errors when attempting to install/configure individual integrations. The merchant grants both for full operational autonomy.

### Geo zone deletion safety — auto-fallback to Global

A [[settings-geo-zones|Geo Zone]] in use by an active shipping method is referenced by `geo_zone_id` on the method. If the merchant deletes the zone from [[settings-geo-zones]] **without** first detaching it from this shipping method, the method's "Deliver to" column will fall back to showing "Global" semantics — the platform automatically clears the `geo_zone_id` and falls back to `target = restofworld` when no zone is set. The merchant re-links by editing the method and selecting a new zone.

This is a graceful-degradation safety net, not a recommended pattern. The merchant's correct sequence is: edit each affected shipping method first, switch its target to a different zone (or to "The whole world"), THEN delete the original zone.

### Cash-on-delivery sync per integration

For integrations that support cash-on-delivery (Econt, Speedy, etc.), the per-integration settings have a *"Automatically set order status to paid when we get information from shipping provider with Cash on delivery"* toggle — this lives on each integration's app settings page, **not** on this Shipping list. The Shipping list manages methods; the integrations manage their own COD reconciliation.

### Where defaults live (NOT here)

[[settings-cart]] is where the merchant picks:

- **Default shipping type** (auto-selected at checkout).
- **Default shipping provider** (auto-selected at checkout).
- **Automatically select shipping if only one is available** (saves the customer a click).
- **Ask for shipping address for digital products** (whether digital-only orders go through the shipping-address step).

These defaults are NOT configured on this Shipping list or via the API — only the methods themselves are managed here.

## Settings & fields

| Field / setting | Where it lives | Notes |
|----------------|---------------|-------|
| `app_id` (per provider) | JSON-API v2 read | Non-null for integration-backed; null for Custom rate methods. |
| `geo_zone_id` (per provider) | JSON-API v2 read | Numeric ID — needs a second call to [[settings-geo-zones]] data for the human-readable name. |
| `active` (per provider) | JSON-API v2 read | Mirrors the **Show in store** per-row toggle. |
| `settings.shipping` | [[settings-staff]] | Sidebar visibility. |
| `store.shipping` | [[settings-staff]] | Integration-app API endpoint enforcement. |

## Business rules

- **API is read-only.** All writes (create / update / toggle / delete) must go through the admin Shipping screen. There is no JSON-API v2 write surface for shipping providers.
- **Custom vs integration-backed are distinguished by `app_id`.** API consumers cannot easily list "only Custom" or "only integrations" without filtering on `app_id` presence locally. (verify whether a filter parameter exists for this distinction.)
- **Geo-zone names must be looked up separately.** The JSON-API v2 response only carries the numeric `geo_zone_id`; merchants and apps must call [[settings-geo-zones]] to resolve names.
- **Two permission grants, two layers.** `settings.shipping` gates the page; `store.shipping` gates the individual integration installs. Both are managed in [[settings-staff]].
- **Geo-zone deletion does not break methods** — the auto-fallback to `target = restofworld` preserves the method's existence; the merchant only loses regional targeting until they re-link.

## Related

- [[settings-shipping]] — hub.
- [[settings-shipping-edit-panel]] — where `geo_zone_id` is set.
- [[settings-shipping-lifecycle]] — `active` toggle + auto-target derivation (the mechanism behind the geo-zone deletion fallback).
- [[api-shipping-providers]] — JSON-API v2 endpoint reference.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[settings-geo-zones]] — the zone catalogue referenced by `geo_zone_id`.
- [[settings-staff]] — where `settings.shipping` and `store.shipping` grants live.
- [[settings-cart]] — where the **defaults** that this page does NOT cover are configured.

## Open questions

- (verify) Whether the JSON-API v2 list endpoint exposes a filter to separate Custom methods from integration-backed providers without local filtering on `app_id`.
