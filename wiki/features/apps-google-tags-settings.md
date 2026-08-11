---
type: feature
nav_path: "Apps → Google Tag Manager → Settings"
route_name: apps.google_tags.settings
route_path: /admin/apps/google_tags/settings
aliases: ["Google Tag Manager Settings", "GTM settings", "GTM container config"]
tags: [apps, google, tag-manager, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 4
---
# Google Tag Manager → Settings

## Purpose

The **Settings** tab is where the merchant enters the **GTM container ID** for injection on storefront pages. See [[apps-google-tags]] for the full feature set.

## Where to find it

Sidebar → Apps → Google Tag Manager → **Settings tab**. Route: `/admin/apps/google_tags/settings`.

## What the merchant can do here

### Configuration

The Vue Settings UI exposes a SINGLE field:

| Field | Notes |
|---|---|
| **GTM Container ID** (`code`) | Text input labelled *"Insert the code provided by Google Tag Manager"*, placeholder `GTM-XXXXXXX` from tagmanager.google.com. Validated against `/GTM-[0-9A-Z]{5,}/i`. |

There is **NO** Server-side GTM URL field, ecommerce-event toggle, customer-identifier toggle, or order-metadata toggle here — the data layer emission is governed by [[apps-datalayer]] separately.

### What the merchant CANNOT do here
- Configure individual tags / triggers / variables — that's done in GTM's web UI.
- Add multiple containers to one store — single container per store.
- Toggle ecommerce-event firing or customer-identifier pushing — those don't exist as fields here.

## Settings & fields

Per [[apps-google-tags]] Manager:
- the configured check — verifies container ID is set.

## Business rules

### Container snippet injection

When the container ID is configured + the app is active, CloudCart injects:
- The GTM `<script>` snippet in `<head>`.
- The GTM `<noscript>` fallback at the start of `<body>`.

These are the standard GTM bootstrap requirements.

### Data layer pushes

CloudCart pushes ecommerce events to the GTM data layer at user-action moments. The merchant's GTM tags consume these events to fire whichever pixels they want.

### Cookie consent integration

GTM tags should respect [[apps-gdpr-overview]] consent state. The merchant configures consent triggers inside GTM's UI.

### Permission
Standard apps permission scope.

## Related

- [[apps-google-tags]] — hub.
- [[apps-datalayer]] — companion data layer enrichment.
- [[apps-google-analytics]] / [[apps-google-dynamic]] — sister apps (managed via GTM in best-practice setup).
- [[apps-gdpr-cookies]] — cookie consent gating.

## How it works (verified against backend)

### Single saveable setting: `code`

The platform code's `$only` allowlist is exactly `['code']`. So this page lets the merchant configure just ONE field — the GTM container ID. No multi-container support, no server-side GTM URL setting, no data-layer toggles.

### Validation: GTM ID format required

The container ID is validated against `/GTM-[0-9A-Z]{5,}/i` (case-insensitive). Invalid format → *"The Google Tag ID is invalid"*. Empty while the app is active → *"Please add your Google Tag ID"*.

### Single container per store

The `code` is a single string field — the platform stores ONE GTM container ID per store. Multi-store merchants configure separate containers per store; multi-container-per-single-store is not supported through this integration.

### Built-in data-layer variables come from the Datalayer app

The variables available in the data layer are NOT configured on this Settings page — they're emitted by [[apps-datalayer]] when that app is installed. The two main payloads are `cc_page_data` (page-specific context: product, category, cart, line items, totals, order on checkout-return) and `cc_customer_data` (when the customer is logged in). On the checkout-return page, an additional GA4-format `purchase` event fires via the cc-analytics events pipeline.

### GTM Preview Mode works out of the box

There is no special toggle for GTM Preview Mode here. Because CloudCart injects the standard GTM `<script>` / `<noscript>` snippets unchanged, GTM's Preview Mode (`?gtm_debug=...`) functions normally on a CloudCart storefront — the merchant enables Preview from inside tagmanager.google.com and navigates to their storefront URL.

### Settings save → JS rebuild → storefront cache busts on next page load

Saving a new GTM container ID triggers a rebuild of the shared `cc_applications_config.js` on S3 (because the Google Tags manager implements `AppJsRegenerate`). The file is versioned by `last_build` timestamp, so storefront browsers naturally fetch the new version on the next page load.

### Wiki note: no "Server-side GTM URL" field exists

This page's earlier table mentions a "Server-side GTM URL" field; verified against backend, that field does NOT exist — the only saveable setting is the GTM container ID. Server-side GTM routing is handled inside the merchant's own GTM container configuration.

### Wiki note: no "Push ecommerce events" / "Include customer identifiers" toggles on this page

Those toggles also don't exist as saveable fields. The data layer pushes are controlled by whether [[apps-datalayer]] is installed (the actual emitting app), not by a setting on Google Tag Manager's page.

### Single inline-edit box, single field

The Vue Settings renders ONE `SettingsBox` with `editMethod: 'inline'` containing a single text input labeled *"Insert the code provided by Google Tag Manager"* with placeholder `GTM-XXXXXXX`. There is no slide-over panel, no Connect button, no OAuth — it's a plain inline-edit text field. Validation runs on save against the regex described above.

## Open questions

(None currently outstanding for this page.)
