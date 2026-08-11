---
type: feature
nav_path: "Nitrogen (Headless storefronts)"
route_name: nitrogen
route_path: /admin/nitrogen
aliases: []
tags: [nitrogen, hub, owner-only]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
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

### Owner-only — moderators have no access to Nitrogen

The entire Nitrogen API surface (`/admin/api/core/nitrogen/*` — storefronts, customer-accounts, tokens, deployments, Nova tokens, scopes, env vars, GitHub installation) is wrapped in the `isOwner` middleware. **Only the store owner can list, create, edit, rotate tokens, or deploy storefronts.** Moderators — regardless of which permission boxes have been ticked for them in [[settings-staff]] — are blocked at the API level with HTTP 403 and never see this sidebar entry. There is no separate `nitrogen` permission row in the [[settings-staff]] permission tree; the gate is binary (owner vs everyone else). If a moderator needs to manage a headless storefront, the merchant must either transfer that work to the owner, or contact CloudCart support to discuss ownership transfer ([[settings-staff]] — *"Ownership transfer is NOT exposed in the admin panel"*).

## Related

- [[nitrogen-deployments]]
- [[nitrogen-storefront-overview]]
- [[nitrogen-storefronts]]

## Open questions

_None._
