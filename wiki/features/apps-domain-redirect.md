---
type: feature
nav_path: "Apps → Domain Redirect"
route_name: apps.domain_redirect.overview
route_path: /admin/apps/domain_redirect
aliases: ["Domain Redirect", "Domain forwarding", "301 domain redirect", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, redirect, seo, infrastructure]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Domain Redirect (geo-routing between the merchant's own CloudCart stores)

## Purpose

**Domain Redirect** integration — geo-routes visitors to whichever of the merchant's own CloudCart storefronts matches their country. Used by merchants who operate parallel country-specific stores under one account (e.g., `bg.shop.com`, `ro.shop.com`, `gr.shop.com`) and want a visitor's IP to decide which store they see first. A visitor's country is detected from their IP, and they are forwarded to the store mapped to that country; a **global** target catches everyone whose country isn't mapped.

This is NOT a generic source-to-target domain forwarder. The targets must already be CloudCart sites in the same merchant account; no external domains are accepted. For per-URL redirects within one storefront, use [[marketing-seo-301-redirects]].

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → install → **Domain Redirect**. See [[apps-domain-redirect-settings]] for configuration.

## What the merchant can do here

- Pick a **global (fallback) destination** — which of the merchant's CloudCart stores receives visitors when no country mapping matches.
- Add **per-country mapping rows** — for each country, which of the merchant's CloudCart stores should that country's visitors see.
- Share a link with the bypass parameter (`?_disableRedirect=<owner-user-id>`) so a specific visitor can land on a non-default storefront — e.g. share a Bulgarian-store link with a Romanian customer who specifically wants that store. The parameter must equal the site-owner's user id, so random visitors can't bypass.

### What the merchant CANNOT do here
- Redirect from a non-CloudCart domain — the source visit must arrive at one of the merchant's CloudCart sites already.
- Choose 301 (permanent) vs 302 (temporary) — every redirect is a 302 Found.
- Preserve the visitor's URL path — the redirect always lands at the target site's root URL. A visitor opening `bg.shop.com/products/module` from Romania ends up at the Romanian site's home page, not at `/products/module`.
- See per-redirect hit analytics — the app does NOT log redirect counts; visit volume per domain is observed through the merchant's external analytics (e.g., [[apps-google-analytics]] / [[analytics]]).
- Bulk-import country mappings — each row is added one-by-one in the settings form; the configuration is normally a short list (one per country the merchant targets).

## Settings & fields

| Field | Notes |
|---|---|
| **`global`** | Fallback destination site id (used when no country mapping matches). Required when any mapping row exists. Validation error if missing: *"Domain is required"*. |
| **`mapping[].country`** | ISO-2 country code from the Country dropdown. Required per row. |
| **`mapping[].site_id`** | Target CloudCart site id (one of the merchant's own sites). Required per row. |

Uninstalling the app clears the merchant's mapping rows and the redirect cache.

## Business rules

### Country detection uses MaxMind GeoIP

The visitor's country is detected via MaxMind GeoIP at request time, then matched against the mapping rows.

### Mapping rows are deduplicated by country

If two rows reference the same country, only the first match wins. The merchant should configure each country once.

### Incomplete configuration silently does nothing

When the visitor's country isn't in any mapping row, the global fallback target is used. If no global target is configured AND no country matches, the visitor is not redirected at all and stays on the original site — a partial setup never breaks the visit.

### A visitor already on the matching store is not redirected

If the visitor's country maps to the same site they're already on, no redirect fires — this prevents infinite loops. Bulgarian visitors on the Bulgarian store stay put.

### Every redirect is a 302 Found

There is NO 301-vs-302 toggle in this app — every redirect is a 302 (temporary). Search engines treat this as temporary, so the source domain remains the canonical SEO record.

### Crawlers and non-content routes are skipped

Search-engine crawlers are never redirected, so Google indexes each domain's own content. Only content routes are eligible: home, search, selection, showcase, vendors, vendor view, tag, category list / view, blog list / view / article, page, private page, bundles list & category, product view, compare. Checkout, customer account, admin panel and similar routes are never redirected — the customer can finish a checkout on whichever domain they landed on.

### HTTPS — both sides are CloudCart and already TLS-secured

This app does not configure SSL. Each of the merchant's CloudCart stores already has its own TLS certificate (managed via [[apps-lets-encrypt]]). There is no "redirect HTTP → HTTPS on a source domain" toggle here — the source IS a CloudCart store that already serves HTTPS.

### Redirect rules are scoped to the merchant, cached one day

Rules are stored against the site owner, not a single site — the app's purpose is "forward this country's visitors to the right store on any of my stores", so the rule must fire across all of the merchant's sites. The `(country → site)` lookup is cached per merchant for 24 hours; saving the settings flushes the cache so changes take effect on the next visitor. Cross-merchant interference is impossible.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-domain-redirect-settings]] — settings sub-page.
- [[settings-domains]] — domain configuration (target domains live there).
- [[marketing-seo-301-redirects]] — per-URL redirects (different scope).

## Open questions

All previously-flagged questions resolved. See body sections.
