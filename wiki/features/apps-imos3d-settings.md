---
type: feature
nav_path: "Apps → IMOS-3D → Settings"
route_name: apps.imos3d.settings
route_path: /admin/apps/imos3d/settings
aliases: ["IMOS-3D Settings", "Imos 3D config"]
tags: [apps, administration, imos3d, furniture, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# IMOS-3D → Settings

## Purpose

The **Settings** tab is where the merchant enters the 4 required credentials to connect CloudCart to **IMOS** 3D furniture-design software. See [[apps-imos3d]] for the full feature set.

## Where to find it

Sidebar → Apps → IMOS-3D → **Settings tab**. Route: `/admin/apps/imos3d/settings`.

## What the merchant can do here

### Required credentials (per [[apps-imos3d]] the configured check)

| Field | Notes |
|---|---|
| **API key** (`imos3d.apiKey`) | IMOS API authentication token. |
| **Shop ID** (`imos3d.shop`) | The merchant's shop identifier in IMOS. |
| **Integration ID** (`imos3d.id`) | This specific CloudCart store's integration ID. |
| **Country** (`imos3d.country`) | Country code (drives currency / language). |

All 4 are required for the configured check to return true. Missing any blocks integration usage.

### What the merchant CANNOT do here
- Use IMOS-3D without an active IMOS subscription.
- Skip any of the 4 credentials.
- Connect to multiple IMOS instances simultaneously (single instance per store).

## Settings & fields

Per [[apps-imos3d]] Manager the configured check validation: all four of `imos3d.apiKey`, `imos3d.shop`, `imos3d.id`, `imos3d.country` must be populated.

## Business rules

### All-four required

The integration is binary: either all 4 credentials are valid + the integration works, OR something's missing + the integration doesn't fire. No partial mode.

### Country drives downstream

The country code affects:
- IMOS-side currency for bills of material.
- Language for 3D-configurator UI.
- Production-routing rules.

### Permission
Standard apps permission scope.

## Related

- [[apps-imos3d]] — hub.
- [[products-products]] — products with IMOS metadata.
- [[orders-details]] — order-side IMOS XML download.

## How it works (verified against backend)

### Country list: full CloudCart Country model

The merchant's country dropdown is populated from CloudCart's full country list (all countries supported in CloudCart's locale system). The settings endpoint returns each country's `code` + `localized_name`. This is the master country list — same as used everywhere else in CloudCart's admin.

### Settings persisted

The form persists exactly: `apiKey`, `shop`, `id`, `country`. No additional fields.

### No built-in test mode

There's no `test_mode` / `environment` field. The merchant uses their IMOS-issued credentials directly; for sandbox testing, the merchant gets test credentials from IMOS separately and swaps them in/out of the Settings.

### Single IMOS shop per store

The settings model holds ONE set of credentials per CloudCart store. A merchant operating multiple stores must connect each to its respective IMOS shop. Multiple IMOS shops per single store is not supported.

### Activation gate is strict

Per the Manager's the configured check and the storefront route check: ALL 4 credentials must be populated AND `active = 1` for the IMOS configurator to be reachable from the storefront. Missing any field — or app inactive — returns 404 on the storefront route.

### Settings keys are namespaced

The 4 IMOS-3D settings are stored under the `imos3d.` namespace (`imos3d.apiKey`, `imos3d.shop`, `imos3d.id`, `imos3d.country`). This is different from most ERP apps which use top-level keys — meaning the merchant won't see these settings in a generic key-value scan of the app's settings; they live in the nested `imos3d` object.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
