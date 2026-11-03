---
type: feature
nav_path: "Apps → FlixFacts → Settings"
route_name: apps.flix_facts.settings
route_path: /admin/apps/flix_facts/settings
aliases: ["FlixFacts Settings", "Flix Facts config"]
tags: [apps, administration, flix-facts, integration, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 1
---
# FlixFacts → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to **FlixFacts** — enters API credentials and configures which CloudCart events trigger sync. See [[apps-flix-facts]] for the full feature set.

## Where to find it

Sidebar → Apps → FlixFacts → **Settings tab**. Route: `/admin/apps/flix_facts/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **FlixFacts API key** | Authentication. |
| **FlixFacts API endpoint** | Service URL. |
| **Account / client ID** | When the merchant has multiple FlixFacts accounts. |

### Event subscription

Per [[apps-flix-facts]] Manager `getEvents`: returns the list of subscribed events. The merchant toggles which CloudCart events fire FlixFacts sync:
- order.created / order.updated / order.paid.
- customer.created / customer.updated.
- (Other events per `getEvents` return.)

### Key matching

The Manager's `match($key, ?Variant $variant)` maps CloudCart keys (product / variant IDs) to FlixFacts internal IDs. The merchant configures the match-key field here (typically EAN / SKU).

### Status change toggle

`hasStatusChange` indicates whether the integration listens to order-status events. Configurable here.

### What the merchant CANNOT do here
- Use without a FlixFacts subscription.
- Edit FlixFacts-side data — push-only sync.

## Settings & fields

Per [[apps-flix-facts]] Manager:
- the configured check — credential check.
- `getEvents` — event subscription list.
- `hasStatusChange` — status-change event flag.

## Business rules

### Event-driven sync

When a subscribed event fires + FlixFacts is configured, sync triggers automatically. No manual export needed.

### Permission
Standard apps permission scope.

## Related

- [[apps-flix-facts]] — hub.
- [[apps-szamlazz]] / [[apps-fgo]] / [[apps-smart-bill]] — sister invoicing apps (different sync model).
- [[apps-e-store-content]] — sister event-driven integration.

## How it works (verified against backend)

### Settings are 3 fields only

The form persists exactly these fields:
- `flix_facts` — Distributor ID (the only credential — there's no API key, endpoint, or account ID).
- `match.flix` — what FlixFacts looks for (`mpn` / `ean` / `sku`).
- `match.self` — what CloudCart provides as the matching value (`sku` or `barcode`).

When the merchant flips `active = 1`, the platform requires all three (validated `required_if:active,1`).

### NOT an accounting integration

Despite the "settings → sync events" framing in older descriptions, the FlixFacts integration is purely a **product-page content module**, not an accounting sync. The only event subscribed is `post.product.view` (per [[apps-flix-facts]]). There's no order sync, customer sync, or invoice generation. The merchant should run FlixFacts alongside (not as a replacement for) [[apps-fgo]] / [[apps-szamlazz]] / [[apps-smart-bill]] for accounting.

### No test mode toggle

There's no `test_mode` or `environment` field in the settings. The Distributor ID provided by FlixFacts works directly against their production endpoint.

### isConfigured check requires ALL three settings
The Manager's `isConfigured` requires all three of `flix_facts`, `match.flix`, `match.self` to be non-empty. Saving with any one missing leaves the integration inactive — the module simply won't render until all three are populated.

### Active flag is event-level, not app-level
The CoreEventEntity for FlixFacts ships with `active = false` by default. So even after the merchant configures the Distributor ID, they must explicitly activate the event subscription (via [[settings-hooks]]) for the module to fire. The platform does not auto-activate on save.

### Match key defaults: `match.flix = mpn`, `match.self = sku`
When the merchant doesn't override the matching defaults, FlixFacts looks for the product's MPN, and CloudCart provides the variant's SKU. So a typical setup just requires entering the Distributor ID and saving — the matching defaults work for most catalogues without further config.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
