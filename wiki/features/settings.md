---
type: feature
nav_path: "Settings"
route_name: settings
route_path: /admin/settings
aliases: ["Settings hub", "Settings home", "Настройки", "Settings landing"]
tags: [settings, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 3
---
# Settings

## Purpose

Hub page for the **Settings** area of the CloudCart admin panel. The hub is *designed* as a grid of route-cards split across two labelled sections — **General settings** (the everyday store-identity / branding / commerce screens) and **Advanced settings** (developer-oriented and operational tooling — API keys, webhooks, queue, banned IPs, etc.). The cards are not configurable — each one is a click-through link to its dedicated sub-screen.

> **Current state (verified against the Vue router):** the route-card-grid component (`SettingsPage`) is built and present in the codebase, **but its index route under `/admin/settings` is commented out**. So today, navigating to `/admin/settings` does NOT render the card grid — it falls back to a bare parent placeholder (`<router-view>`). Merchants reach each Settings sub-screen directly from the sidebar's Settings sub-menu entries, not by landing on a hub-grid page. The card-grid hub described below documents the intended design; it is not live at the bare `/admin/settings` URL.

## Where to find it

Settings (top-level sidebar entry). Direct URL: `/admin/settings`.

## What the merchant can do here

- See **two card-grids**: "General settings" first, then "Advanced settings" below.
- Click any card to navigate to that sub-screen (title + icon + short description per card).
- See ONLY cards the merchant's plan + permissions + installed apps allow — the card is filtered out when (`visible === false` OR `installedApp === false`) on the navigation entry served by the backend. So a merchant on a no-Backups plan won't see the Backups card; a moderator without `settings.domains` won't see the Domains card.

## Settings & fields

Not applicable — this is a navigation hub, not a screen with its own settings. The card grid is built from the backend-supplied `settings` node of the navigation tree (`serverSettings('navigation')`). Cards in the tree before a `type=title` separator are placed in the "General settings" group; cards after the separator are placed in "Advanced settings".

### Card grid layout

The grid is responsive (1 column on mobile, 2 on medium screens, 3 on extra-large screens). Each card has an icon (FontAwesome class), a title (translated), a short description (translated), and a click-through to the named route. Card titles, descriptions, icons, and target route names come from `useSettingsGrid` mappings (e.g., `settings.general` → "Store settings" with the info icon, `settings.branding` → "Brand", etc.).

## Business rules

### Sidebar visibility is permission-gated

The Settings sidebar entry only appears for staff who hold at least one of the following access permissions (see [[settings-staff]] → Access permissions): `settings` (umbrella), or any granular section permission — `settings.general`, `settings.payment_providers`, `settings.shipping`, `settings.regions`, `settings.geo_zones`, `settings.taxes`, `settings.domains`, `settings.sizes`, `settings.labels`, `settings.notifications`, `settings.translations`, `settings.files`, `settings.admins.all`, `settings.admins`, `settings.backups`. A moderator with none of these grants does not see Settings in the sidebar at all.

### Each sub-screen has its own permission

Sub-screens are individually gated. A merchant who grants a moderator only `settings.general` will see Settings in the sidebar but only the Store settings / Brand / Admin notifications screens are accessible — Domains, SSL, Taxes etc. require their own granular permissions.

## Related

- [[settings-admin-notifications]]
- [[settings-api-keys]]
- [[settings-backups]]
- [[settings-banned-ip]]
- [[settings-boxes]]
- [[settings-brand]]
- [[settings-cart]]
- [[settings-domains]]
- [[settings-files]]
- [[settings-general]]
- [[settings-general-industry]]
- [[settings-geo-distances]]
- [[geo-polygons-settings-main-new]]
- [[settings-geo-zones]]
- [[settings-hooks]]
- [[settings-import-history]]
- [[settings-invoicing]]
- [[settings-pat-tokens]]
- [[settings-payment-providers]]
- [[settings-queue-view]]
- [[settings-staff]]
- [[settings-statuses]]
- [[settings-taxes]]
- [[settings-translations]]

**Concepts (the mechanisms behind these screens):**

- [[tax-computation]] — how VAT is computed (behind [[settings-taxes]]).
- [[shipping-calculation]] / [[shipping-provider-mechanism]] — how shipping rates + carriers work (behind shipping settings).
- [[payment-provider-mechanism]] — how payment methods attach + charge (behind [[settings-payment-providers]]).
- [[order-status-workflow]] — the status taxonomy behind [[settings-statuses]].
- [[notification-delivery]] — the event → webhook / email spine behind [[settings-hooks]] + [[settings-admin-notifications]].
- [[geo-targeting]] — the zone / polygon / distance model behind [[settings-geo-zones]].
- [[invoicing-and-accounting]] — invoice / receipt / credit-note model behind [[settings-invoicing]].
- [[import-pipeline]] / [[background-queue-inventory]] — the bulk-import + queue model behind [[settings-import-history]] + [[settings-queue-view]].
- [[backups-and-restore]] — the backup / restore model behind [[settings-backups]].
- [[merchant-roles]] — the staff role / permission model behind [[settings-staff]].
- [[multi-currency]] — store-currency model affecting taxes, payments, and totals.
- [[plan-gates]] — how plan-features gate which settings screens + options appear.

## Open questions

_None._
