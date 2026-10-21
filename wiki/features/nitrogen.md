---
type: feature
nav_path: "Nitrogen (Headless storefronts)"
route_name: nitrogen
route_path: /admin/nitrogen
aliases: []
tags: [nitrogen, hub, staff-permission]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 1
---
# Nitrogen (Headless storefronts)

## Purpose

Hub page for the **Nitrogen (Headless storefronts)** area of the CloudCart admin panel. Lists the screens that live under this section.

## Where to find it

Nitrogen (Headless storefronts) (top-level sidebar entry).

## What the merchant can do here

- Navigate to any sub-screen listed in `## Related`.

## Settings & fields

Not applicable — this is a navigation hub, not a screen with its own settings.

## Business rules

### The Nitrogen Storefronts permission

The entire Nitrogen API surface (`/admin/api/core/nitrogen/*` — storefronts, tokens, deployments, Nova tokens, env vars, GitHub installation) requires the **Nitrogen Storefronts** permission, a row of its own in the [[settings-staff]] permission tree. The store owner always has it; a moderator can list, create, edit, rotate tokens or deploy storefronts only when that permission is ticked for them. Without it, the calls are refused with HTTP 403.

## Related

- [[nitrogen-deployments]]
- [[nitrogen-storefront-overview]]
- [[nitrogen-storefronts]]

## Open questions

_None._
