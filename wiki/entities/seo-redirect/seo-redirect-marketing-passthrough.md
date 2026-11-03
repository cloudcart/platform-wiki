---
type: entity
nav_path: "Entity → SEO 301 Redirect → Marketing parameter passthrough"
aliases: ["Redirect UTM passthrough", "gclid passthrough", "fbclid passthrough", "Marketing tracking on redirect", "Query parameter whitelist on 301"]
tags: [entity, seo, marketing, redirects, analytics, tracking]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[seo-redirect]]. See the hub for the other aspects (types, lookup and cache, CSV import, auto-tracking, validation and UI).

# 301 Redirect — Marketing parameter passthrough

## Identity

When the redirect middleware fires a 301, it doesn't just send the customer to the new URL — it also **re-attaches a hardcoded whitelist** of marketing-tracking query parameters from the original URL onto the redirect target. The behaviour is critical for migrations: a customer clicking a Google Ad pointing at an OLD URL → gets 301'd to the new URL → and the new URL still carries the `gclid` so Google Analytics attributes the click correctly.

The whitelist is hardcoded — the merchant cannot configure which parameters pass through. Two commonly-used UTM parameters (`utm_term` and `utm_content`) are **NOT** in the whitelist, which is worth flagging for merchants running detailed UTM campaigns.

## Aliases

- **Marketing-tracking pass-through** — the canonical internal term.
- **UTM passthrough** — informal phrasing when UTM-only campaigns are the concern.
- **Click-ID preservation** — emphasises the click-ID half of the list (`gclid`, `fbclid`, `msclkid`, etc.).

## Key Attributes

The whitelisted parameters preserved on every 301:

| Parameter | Source | Notes |
|---|---|---|
| `fbclid` | Facebook click ID | Set by Facebook / Meta Ads on outbound clicks. |
| `gclid` | Google Ads click ID | Set by Google Ads. Used for offline-conversion uploads and click attribution. |
| `gclsrc` | Google Ads source identifier | Distinguishes Search / Display / etc. for the same `gclid`. |
| `msclkid` | Microsoft Ads click ID | Bing / Microsoft Ads attribution. |
| `utm` | UTM aggregate parameter | Some merchant configurations use a single `utm=` param. |
| `utm_source` | UTM source | Standard UTM tagging. |
| `utm_medium` | UTM medium | Standard UTM tagging. |
| `utm_campaign` | UTM campaign | Standard UTM tagging. |
| `dclid` | DoubleClick click ID | Display & Video 360 / DV360 attribution. |
| `zanpid` | Zanox / Awin affiliate ID | Affiliate network tracking. |

### What is NOT in the whitelist

Notable omissions — these are NOT preserved on redirect:

- **`utm_term`** — the keyword / search term parameter. Lost on every redirect.
- **`utm_content`** — the A/B-test / creative-variant parameter. Lost on every redirect.
- **`utm_id`** — campaign-ID parameter. Lost on every redirect.
- **Any other custom tracking parameters** the merchant might add — third-party affiliate networks beyond Zanox/Awin, custom-built attribution, custom campaign tracking.

If the merchant runs UTM campaigns that rely on `utm_term` or `utm_content` (typical for paid-search teams tracking keyword-level conversion), the data is lost the moment a redirect fires. The platform doesn't surface this anywhere.

## Relationships

- **Reads from** the original request's query string at redirect time.
- **Writes to** the `Location` header by appending the whitelisted parameters to the resolved destination URL.
- **Independent of** the redirect type — applies equally to `manual`, `external`, entity-typed, and `section` redirects.

## Lifecycle

1. The middleware matches a request URL against an `old_url` (see [[seo-redirect-lookup-and-cache]]).
2. The destination URL is resolved per the rule's type (see [[seo-redirect-types]]).
3. The whitelisted query parameters from the original request URL are extracted.
4. The whitelisted parameters are appended to the destination URL (preserving any query parameters the destination already had).
5. The combined URL is set as the `Location` header on the HTTP 301 response.

## Business rules

### The whitelist is hardcoded — not merchant-configurable

The merchant cannot add custom parameters to the pass-through list through the admin UI. Adding new parameters requires a platform change.

### Custom tracking parameters are dropped

If the merchant's analytics integration relies on a custom parameter (e.g., `partner_id`, `campaign_uuid`, `affiliate_code` that isn't `zanpid` / `dclid`), that parameter is silently dropped on redirect. The merchant sees the click hit the new URL with a clean query string and the attribution gap is invisible until it shows up as missing-attribution rows in the analytics tool.

### Same applies to internal redirects from slug rename

The 30-day URL-handle-history auto-redirects (see [[seo-redirect-auto-tracking]]) follow a different code path internally but the same merchant intent applies — clicks from Google Ads to a renamed product's old slug should still attribute correctly. The whitelist behaviour for those auto-redirects is consistent with the manual rules (verify).

### External CDN caching can mask the passthrough

If a 301 is cached at an external CDN (browser, ISP, etc.), the cached response is replayed without the original request's query string being seen by the platform. This is invisible from the merchant's side — the symptom is "the campaign report shows fewer clicks than the ad platform shows" and the diagnosis usually traces back to caching, not redirect logic.

### UTM-term and UTM-content gap is undocumented

Merchants running paid-search campaigns with keyword-level UTM tagging will lose `utm_term` and `utm_content` on every 301. The platform doesn't warn about this on the redirect editor or anywhere else. For SEO migrations where the merchant cares about keyword-level attribution, manual URL building (each old URL gets its own redirect with the parameters baked into the `new_url`) is the only workaround.

## Where it appears

- [[seo-redirect-lookup-and-cache]] — the passthrough is the last step of the redirect-fire sequence.
- [[seo-redirect-types]] — applies to every type (free-form and entity).
- [[marketing-seo-301-redirects]] — the manager screen where rules are created (no UI hint about the passthrough behaviour).
- [[apps-domain-redirect]] — whole-domain redirects also preserve marketing parameters (separate mechanism, similar intent).
- [[storefront-architecture]] — analytics integration sits downstream of the storefront.

## Related

- [[seo-redirect]] — hub.
- [[seo-redirect-lookup-and-cache]] — the redirect-fire sequence within which this passthrough runs.
- [[seo-redirect-types]] — destination resolution that happens before the parameter append.
- [[apps-domain-redirect]] — parallel passthrough on whole-domain forwarding (verify the exact parameter list there).

## Open Questions

- Whether the platform plans to make the whitelist merchant-configurable (would close the `utm_term` / `utm_content` gap) (verify).
- Whether the 30-day slug-rename auto-redirect path uses the same hardcoded whitelist (verify against the storefront controller paths).
