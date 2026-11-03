---
type: feature
nav_path: "Apps → Algolia → Dashboard-side configuration"
route_name: apps.algolia.overview
route_path: /admin/apps/algolia
aliases: ["Algolia dashboard", "Algolia facets", "Algolia ranking", "Algolia synonyms", "Algolia personalization", "Algolia A/B testing", "Algolia analytics", "Algolia quota", "Algolia downtime", "Algolia multi-language index"]
tags: [apps, algolia, search, configuration, quota, limitations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-algolia]]. See the hub for the other aspects (credentials, indexing, settings tab).

# Algolia — Dashboard-side configuration & limits

## Purpose

Sets the boundary between what the CloudCart app configures (credentials, result counts, the upload trigger) and what the merchant must configure inside **Algolia's own dashboard** (facets, ranking, synonyms, personalization, A/B testing, analytics, per-language indexes). It also covers the operational limits the merchant should expect: how the operations quota surfaces, how errors are logged, what happens when Algolia is down, and the fact that CloudCart never estimates Algolia plan cost. This is the page to read when a merchant asks "why can't I configure synonyms / facets / analytics from CloudCart" or "what happens when Algolia goes down".

## Where to find it

These behaviours straddle two places: the CloudCart Settings tab at `/admin/apps/algolia` (where the quota toast appears) and the merchant's **Algolia dashboard at algolia.com** (where all the search-tuning features live). Nothing on this aspect is configurable from a CloudCart screen beyond the credentials + result-count fields documented on [[apps-algolia-settings]].

## What the merchant can do here

- Understand which search-tuning features they must configure in Algolia's dashboard, not CloudCart.
- Read the `error.quota_exceeded` toast when Algolia's API reports the plan's operation quota is exhausted.
- Know that they must monitor plan usage + cost from Algolia's own dashboard.

### What the merchant CANNOT do here

- Configure facets, custom ranking rules, or synonyms from the CloudCart UI.
- Use Algolia's Personalization, A/B testing, or Search Insights / Analytics inside the CloudCart admin.
- Switch to per-language Algolia indexes from CloudCart (only one `appId` + key pair is stored).
- Get a proactive quota / plan-cost warning from CloudCart before the limit is hit.
- Rely on automatic fallback to built-in search when Algolia is unreachable.

## Settings & fields

| Setting / message (lang key) | Notes |
|---|---|
| `error.quota_exceeded` | *"Operations quota exceeded in Algolia, change plan to get more operations."* — surfaced when Algolia's API returns the quota-exceeded response. |
| `error_info_quota_exceeded` | The defined platform message for the quota-exceeded condition. |

No tuning fields live here — facets, ranking, synonyms, personalization, A/B, and analytics are all dashboard-side on algolia.com.

## Business rules

### Operations quota per Algolia plan

Each index / search operation consumes quota from the merchant's Algolia plan. The platform surfaces `error.quota_exceeded` when Algolia's API returns the quota-exceeded response.

### Facets are configured in the Algolia dashboard, not in CloudCart

The CloudCart side ships the searchable record fields (name, description, vendor, category, price, etc.) to Algolia. Choosing which of those become **filterable facets** (size, color, brand) is configured on the Algolia side via Algolia's dashboard — not from the CloudCart settings page. Same for **custom ranking rules** (boosting newer products, products with higher sales, etc.) and **synonyms** (per-language synonym lists).

### Personalization, A/B testing, query analytics are Algolia dashboard features

Algolia's Personalization, A/B testing, and Search Insights / Analytics features all live in Algolia's own UI at algolia.com. CloudCart does NOT surface any Algolia analytics inside the admin panel — to inspect popular queries / click-through rate / conversion-from-search the merchant logs into Algolia's dashboard.

### Multi-language: same index, name field is locale-stored

CloudCart pushes localized text fields (e.g., the product name) to Algolia using the storefront's primary language. For multi-language storefronts, the merchant would typically configure separate Algolia indexes per language via Algolia's dashboard — but CloudCart's app stores ONE `appId` + ONE `apiKey` pair, so it indexes into the default index Algolia provisions. Per-language index switching is not configurable from this app.

### Plan cost is NOT estimated by CloudCart

Algolia is a paid service with a free tier limited by record count and operations. CloudCart does not estimate, warn, or surface plan-cost projections — only the `error.quota_exceeded` toast appears when Algolia's API actually returns "quota exceeded". Merchants should monitor their Algolia plan usage from Algolia's own dashboard.

### When Algolia is down, the storefront search has no automatic fallback

The storefront search box loads Algolia's JavaScript autocomplete client with the merchant's `appId` + Search API Key. If Algolia is unreachable, the autocomplete fails silently in the browser — there is **no** automatic fallback to CloudCart's built-in [[apps-listing-engine]] search. The full search results page (POST to the search route) may still degrade through the regular server side, but Algolia-dependent UIs simply break until Algolia responds.

### Error handling: known errors filtered from logs

When the integration hits an error:

- If the exception message contains `'application is blocked'` OR `'please check your'`, the error is NOT logged (these are known transient / config errors, no point spamming logs).
- Otherwise, the error is written to the system log under the `'Algolia'` tag.
- The merchant ALWAYS receives an in-admin notification regardless.

This is a sensible operational pattern: known transient errors don't pollute logs but the merchant still sees them via notification.

### Permission

Standard apps permission scope.

## Related

- [[apps-algolia]] — hub.
- [[apps-algolia-settings]] — the only CloudCart-side configuration (credentials + result counts + show-price).
- [[apps-listing-engine]] / [[apps-advanced-search]] — the built-in search stack that does NOT take over when Algolia is down.

## Open questions

(None currently outstanding for this page.)
