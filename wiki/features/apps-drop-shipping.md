---
type: feature
nav_path: "Apps → Drop Shipping"
route_name: apps.drop-shipping.settings
route_path: /admin/apps/drop-shipping
aliases: ["Drop Shipping", "DropShipping"]
tags: [apps, deprecated, drop-shipping]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Drop Shipping (DEPRECATED / NOT IN USE)

## Purpose

**This app is NOT in active use on the platform.** Merchants should NOT install or rely on it. The wiki entry is preserved for reference only.

For supplier-based product flows the merchant should use the modern stack:
- [[apps-suppliers]] — per-product supplier mapping with prices, lead times, SKUs.
- [[apps-xml-sync]] — recurring sync from supplier XML feeds (auto-updates stock + price).
- [[apps-frisbo]] — 3PL fulfillment outsourcing (close to drop-shipping operationally).

The drop-shipping workflow is more comprehensively handled by the combination of those apps. The standalone Drop Shipping app added no functionality beyond what they already provide.

## Where to find it

The app may still appear in the App Store catalogue but is effectively inert. Merchants should use the modern alternatives listed above.

## What the merchant can do here

- **DO NOT use.** Instead, configure the modern stack:
  - Install [[apps-suppliers]] to manage supplier-product relationships.
  - Install [[apps-xml-sync]] to auto-pull supplier feeds.
  - Optionally install [[apps-frisbo]] for full 3PL outsourcing.

## Settings & fields

Not applicable — the integration is deprecated.

## Business rules

Deprecated. No SLA / support on this integration.

## How it works (verified against backend)

### Status
The Drop Shipping app remains in the CloudCart codebase but is no longer the recommended way to run a drop-ship business. Merchants who never installed it will not see it actively promoted; merchants who configured it historically may still have residual data.

### Settings Vue is empty placeholder
The `Settings.vue` file at `CcModules/DropShipping/components/Settings.vue` contains an empty `<script setup>`, an empty `<template>`, and an empty `<style scoped>`. There is no backend manager class registered for the app under the theme templates. The app's route `apps.drop-shipping.settings` resolves to a blank screen.

So the wiki's deprecation note is verified at the code level: this app has been fully retired from the live platform and is preserved only as a route stub. Any merchant who navigates to `/admin/apps/drop-shipping` sees nothing — they should follow the migration path to the modern stack ([[apps-suppliers]] + [[apps-xml-sync]]).

### No App Store install entry
There is no PHP module under the theme templates named `DropShipping` or similar; the App Store's regular install flow cannot install this app because there's no manager class to register. Existing installations are legacy artefacts.

### Recommended migration path
For new and existing merchants, the modern drop-shipping workflow is:
1. **[[apps-suppliers]]** — register each drop-ship supplier and map products to suppliers with their wholesale prices, lead times, and SKUs.
2. **[[apps-xml-sync]]** — set up recurring syncs that pull supplier XML feeds and auto-update stock + price on the matching CloudCart products.
3. **[[apps-frisbo]]** — optionally outsource full 3PL fulfilment (pick / pack / ship).

This combination provides everything the standalone Drop Shipping app did and adds multi-supplier management, recurring sync schedules, and external fulfilment.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps]] — App Store hub.
- [[apps-suppliers]] — current recommended approach.
- [[apps-xml-sync]] — supplier feed sync.
- [[apps-frisbo]] — 3PL outsourcing.
- [[apps-deprecated]] — deprecated apps hub.

## Open questions

_None — all questions answered above._
