---
type: feature
nav_path: "Apps → Domain Redirect → Settings"
route_name: apps.domain_redirect.settings
route_path: /admin/apps/domain_redirect/settings
aliases: ["Domain Redirect Settings"]
tags: [apps, administration, redirect, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Domain Redirect → Settings

## Purpose

The **Settings** tab is where the merchant configures **country-to-domain mappings** for [[apps-domain-redirect]] — visitors are routed to the right CloudCart storefront based on their detected country. See [[apps-domain-redirect]] for the full behaviour, bypass mechanism, allowed-route list, and caching rules.

## Where to find it

Sidebar → Apps → Domain Redirect → **Settings tab**. Route: `/admin/apps/domain_redirect/settings`.

## What the merchant can do here

### Global (fallback) destination

A single **Domain** dropdown listing the merchant's own CloudCart sites. This is where visitors land when no country mapping matches (or when the visitor's country isn't in the mapping list). Required when any mapping rows are configured — validation rejects save with *"Domain is required"* otherwise.

### Per-country mapping rows

Below the global selector, the merchant adds rows pairing a **Country** (dropdown of countries) with a **Domain** (dropdown of the merchant's own CloudCart sites). Each row says: *"visitors from this country, send them to this storefront."*

- **+ Add new row** appends an empty row.
- The X icon removes a row.
- Both Country and Domain are required per row — save fails with *"Country is required"* / *"Domain is required"* otherwise.

### Bypass instructions

The page shows a help note at the top instructing visitors how to disable the redirect for themselves: append `?_disableRedirect={user}` to any URL (where `{user}` is the merchant-account user id, shown in the help text). This lets the merchant share a Bulgarian-store link with a Romanian customer who specifically wants to see that store.

### What the merchant CANNOT do here
- Configure source-domain → target-domain 301-style redirects (this app is NOT for that — see [[marketing-seo-301-redirects]] for per-URL redirects, or external DNS / hosting providers for whole-domain forwarding from non-CloudCart domains).
- Pick a redirect type (301 vs 302) — the redirect is always a 302 Found (the application framework's default `redirect`).
- Preserve the visitor's URL path on redirect — only the target site's root URL is used.
- Map to a domain not owned by the merchant — the target must be one of the merchant's own CloudCart sites.

## Settings & fields

| Field | Notes |
|---|---|
| **`global`** | Fallback destination site id (used when no country mapping matches). Required when any mapping row exists. |
| **`mapping[].country`** | ISO-2 country code (from the Country dropdown). Required per row. |
| **`mapping[].site_id`** | Target CloudCart site id from the merchant's account. Required per row. |

Validation messages — exact text:

| Trigger | Message |
|---|---|
| `global` missing while mapping rows exist | *"Domain is required"* |
| Mapping row missing site_id | *"Domain is required"* |
| Mapping row missing country | *"Country is required"* |

## Business rules

### Country detection uses MaxMind GeoIP

The visitor's country is detected from their IP address via MaxMind GeoIP — see [[apps-domain-redirect]] for the full middleware behaviour.

### Mapping rows are deduplicated by country

If two rows are saved for the same country, only the first match is used (the middleware applies `unique('country')` on the loaded mapping collection). The merchant should ensure each country appears at most once.

### Save invalidates the per-user redirect cache

Changes take effect on the next visitor — the cached redirect lookup is keyed per-user and cleared on save. See [[apps-domain-redirect]] for cache-key details.

### Country dropdown is the platform-wide country list
The Country dropdown is sourced from the platform's standard ISO-2 country list — same list used by [[settings-geo-zones]] and [[customers]] addresses. The merchant cannot add a custom country code to the list; they're restricted to the standardised codes.

### Validation rejects empty mapping rows
A row with no country picked OR no destination picked is rejected on save — even if other rows in the same submission are valid. The merchant must either fill in or remove empty rows before the save proceeds.

### Permission
Standard apps permission scope.

## Related

- [[apps-domain-redirect]] — hub, with the full middleware/allow-list/caching behaviour.
- [[marketing-seo-301-redirects]] — per-URL redirects (a different scope).
- [[settings-domains]] — domain configuration.

## Open questions

All previously-flagged questions resolved. See body sections.
