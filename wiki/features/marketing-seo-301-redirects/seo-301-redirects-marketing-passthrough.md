---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → Marketing pass-through"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["Preserve UTM on redirect", "fbclid gclid passthrough", "Marketing tracking params on 301", "Manual scheme strip", "External auto-prepend http", "Location header normalisation"]
tags: [marketing, seo, redirects, utm, tracking, analytics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (types, validation, CSV import, middleware, wildcards, auto-tracking).

# 301 Redirects — Marketing pass-through & URL normalisation

## Purpose

This aspect covers two related behaviours the 301 redirect middleware applies on top of the matched destination:

1. **Marketing-tracking query param pass-through** — a hardcoded whitelist of click-tracking params is preserved from the original URL onto the redirect target so the merchant's analytics still attribute the click.
2. **URL normalisation on save** — `manual` rules auto-strip the store's own scheme+host so the rule survives HTTP→HTTPS migrations; `external` rules auto-prepend `http://` if the merchant forgot to type a scheme.

Both behaviours are invisible to the merchant in the editor but critical to support questions like "my UTMs are gone after the redirect" or "I pasted a full URL into the Manual field — why does the redirect still work after we moved to HTTPS?"

## Where to find it

Both behaviours run automatically — no UI. The pass-through happens at request time inside the redirect middleware (see [[seo-301-redirects-middleware]]). The URL normalisation happens at save time inside the saving callback on the redirect model.

## What the merchant can do here

- Type a paid-ad URL like `https://merchant.com/old?gclid=ABC123` into a browser and watch the 301 redirect arrive with `?gclid=ABC123` appended — so Google Ads analytics still attribute the click.
- Paste a full URL on the store's own host into a `manual` redirect (e.g., `https://merchant.com/contacts`) and have the platform store the relative `/contacts` so the rule survives an HTTP→HTTPS migration.
- Type an external destination without a scheme (`external-site.com/foo`) into an `external` rule and have the platform auto-prepend `http://`.

### What the merchant CANNOT do here

- Add custom tracking params to the whitelist — the 10-param list is hardcoded.
- Strip tracking params from the redirect (the pass-through is always-on; there's no opt-out per rule).
- Use protocol-relative URLs (`//external-site.com/foo`) in `external` rules — the auto-prepend assumes the scheme is missing entirely and prepends `http://`.

## Settings & fields

### The 10 preserved marketing-tracking params

When the middleware fires a 301, it preserves a whitelist of query parameters from the original URL onto the redirect target so the merchant's analytics still attribute the click:

| Param | Source |
|-------|--------|
| `fbclid` | Facebook click ID |
| `gclid` | Google Ads click ID |
| `gclsrc` | Google Ads source |
| `msclkid` | Microsoft Ads (Bing) click ID |
| `utm` | Generic UTM container |
| `utm_source` | UTM source tag |
| `utm_medium` | UTM medium tag |
| `utm_campaign` | UTM campaign tag |
| `dclid` | DoubleClick click ID |
| `zanpid` | Zanox / Awin affiliate ID |

So a customer clicking a Google Ad to an OLD URL → 301'd to the new URL → analytics still sees the gclid on the destination page.

### NOT preserved

The following UTM-family params are **NOT** in the whitelist:

- `utm_term` — the keyword variation of the campaign
- `utm_content` — the ad-variant identifier

Merchants who rely on `utm_term` / `utm_content` for ad-level attribution will lose that resolution on every 301-redirected click. There is no merchant-visible setting to add them; support escalation is required to extend the whitelist (verify whether a config exists).

### Manual auto-strip own scheme+host

For `manual` redirects, the platform auto-strips the merchant's own scheme+host from `new_url` if they pasted a full URL to one of the store's own hosts. So pasting `https://merchant.com/contacts` into a manual redirect's New URL field gets stored as `/contacts` (relative).

The resulting `Location` header is **always relative** to the storefront's current scheme+host. This handles HTTP→HTTPS migrations gracefully: a rule created when the store was HTTP keeps working after the merchant moves to HTTPS — the `Location` header simply uses whatever scheme the current request is on.

### External auto-prepend `http://`

For `external` redirects, if the merchant typed something without a scheme, `http://` is auto-prepended on save. So `external-site.com/foo` becomes `http://external-site.com/foo`.

**Merchants who want HTTPS** for the external target must type the scheme themselves (`https://external-site.com/foo`). The auto-prepend is `http://` only — never `https://`.

## Business rules

### The pass-through is appended, not merged

If the merchant's redirect target already contains query params (e.g., `new_url = "/landing?promo=summer"`), the marketing-tracking params are **appended** to the existing query string. The resulting URL is `/landing?promo=summer&gclid=ABC123`. No conflict resolution if `gclid` happens to be in both — the original query wins (verify the merge order).

### Pass-through only fires when the original URL has the param

The whitelist is a **filter**, not a default. If the customer hit the old URL without a `gclid`, the redirect target won't grow a `gclid`. The middleware only copies params that were actually on the incoming URL.

### Manual auto-strip uses the store's primary domain

The auto-strip is keyed on the store's **primary domain** from [[settings-domains]]. Pasting a URL on a secondary domain may NOT be stripped — the saving callback only recognizes the primary host as "own scheme+host" (verify the exact host-comparison logic against the saving callback).

### External auto-prepend handles protocol-less URLs only

The auto-prepend triggers when the value does NOT start with `http://` or `https://`. Protocol-relative URLs (`//external-site.com/foo`) are NOT in the auto-prepend logic; they get stored verbatim and the resulting `Location` header is broken in browsers that interpret protocol-relative URLs as relative paths under the storefront's host (verify).

### Pass-through doesn't apply to non-Section types differently

The 10-param pass-through runs **before** the Location header is finalised — regardless of redirect type. A `section` redirect that converts `cart` → `/cart` at runtime still gets the marketing params appended to the resolved Location. Same for `product`, `category`, etc. — the pass-through is universal across types.

### URL normalisation is one-way

Once a `manual` URL is auto-stripped to relative, switching the rule's type to `external` and back to `manual` won't bring back the original full URL — the merchant has to re-type it. The saving callback is idempotent at the stored value, not at the merchant's input.

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-301-redirects-types]] — `manual` auto-strip / `external` auto-prepend are properties of these types.
- [[seo-301-redirects-middleware]] — the middleware that fires the 301 with the appended params.
- [[seo-redirect-marketing-passthrough]] — entity-side documentation of the same pass-through (data-model view).
- [[settings-domains]] — primary domain determines which hosts the auto-strip recognises.
- [[analytics-pipeline]] — the analytics-attribution layer that consumes the preserved tracking params.

## Open questions

- The merge order when the destination URL already has a marketing-tracking param that's also on the source URL (verify against the middleware merge logic).
- Whether the auto-strip recognises secondary domains from [[settings-domains]] or only the primary (verify).
- Whether a config exists to extend the 10-param whitelist (e.g., to add `utm_term` / `utm_content`) (verify).
