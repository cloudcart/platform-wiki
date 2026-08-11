---
type: feature
nav_path: "Apps → Multilang → SEO & domains"
route_name: apps.multilang.overview
route_path: /admin/apps/multilang
aliases: ["Multilang hreflang", "Multilang SEO", "Multilang domains", "Multilang subdomain", "Multilang language switcher", "Multilang force-stop"]
tags: [apps, administration, multi-language, storefront, seo, domains]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-multilang]]. See the hub for the other aspects (master/sister model, translation engine).

# Multilang — SEO & domains

## Purpose

This page documents the **storefront-facing + provisioning side** of Multilang: automatic `hreflang` generation for SEO, how a new sister site is first provisioned on a CloudCart subdomain (and later mapped to a custom domain), the language switcher, and the sync controls that are CloudCart-internal-only. The translation engine is on [[apps-multilang-main-translation-engine]]; the structural model on [[apps-multilang-main-model]].

## Where to find it

Sidebar → Apps → Multilang. New sister sites are created via the wizard (see [[apps-multilang-create-step]]); custom domains are mapped from the sister site's own [[settings-domains]] page after it is provisioned. Route: `/admin/apps/multilang`.

## What the merchant can do here

- Get SEO `hreflang` tags generated automatically across the network — no manual configuration.
- Provision a new sister site at `<slug>.cloudcart.net` via the create wizard.
- Map a custom domain (`en.merchant.com`, `merchant.ro`) to a sister site after it is up, via DNS + SSL.
- Show or hide a storefront language switcher per sister site (`show_language` — see [[apps-multilang-stores]]).

### What the merchant CANNOT do here

- Enter a custom domain at create time — the wizard accepts only an alphanumeric subdomain slug (see Business rules).
- Force-stop or force-restart a running sync themselves — those endpoints are CloudCart-internal-only.

## Settings & fields

- **`show_language`** — storefront language-switcher visibility, stored per sister site. When on, the storefront displays a language switcher. See [[apps-multilang-stores]] for the footer toggle.
- **Cache-busting version string** — the integration exposes a version string used to cache-bust the storefront-side JS / language-switcher module.
- **Create-wizard `domain` field** — an alphanumeric slug only (regex `[a-z0-9\-]+`, dots NOT allowed). The platform appends `.cloudcart.net`.

## Business rules

### Hreflang generation per sister site

The platform builds an array of `[language_code => url]` for the storefront's `<link rel="alternate" hreflang>` tags. The merchant's MAIN site gets `x-default` as the hreflang code; other sister sites use their own language code. The function iterates the merchant's sister-site map: for each site_id with `show = true` AND not the current site, it generates the alternate URL, using a per-request URL cache to avoid hitting the DB on every request. This means **SEO hreflang is auto-generated** without merchant configuration. (The master-vs-sister flag that drives `x-default` is documented on [[apps-multilang-main-model]].)

### Multi-language storefront switcher

The storefront displays a language switcher when the `show_language` setting is on. The switcher lets the customer move between the master and sister sites mid-browsing; because slugs are per-site, the "view this same product in the other language" link resolves through the relationship table (see [[apps-multilang-main-model]]).

### New-sister-site domain is a CLOUDCART SUBDOMAIN — not a custom domain at create time

When the merchant runs the create-new wizard, the `domain` field they enter is just an alphanumeric slug (dots NOT allowed). The platform appends `.cloudcart.net` — sister sites are provisioned at `<slug>.cloudcart.net` by default. The merchant maps a custom domain (`en.merchant.com`, `merchant.ro`) AFTER the sister site is up, via the sister site's [[settings-domains]] page + DNS + [[apps-lets-encrypt]]. The wizard's "domain" field is just the initial CloudCart subdomain slug.

### Force-stop and force-restart of sync are CloudCart-internal-only

The force-stop and force-restart endpoints are gated by the internal admin console session — they only work when accessed via CloudCart's internal team support tool. **A regular merchant cannot force-stop or force-restart their Multilang sync** — they have to wait for the queue to complete, or contact CloudCart support to invoke these endpoints.

### FREE_FOR carve-out (internal)

The setup wizard, the progress endpoint, and the unpaid-feature blocking all check whether the master site ID is in a hardcoded internal `FREE_FOR` whitelist. Whitelisted sites skip the checkout redirect for plan + features, bypass the HTTP 402 unpaid-feature block on the Progress page, and get the entire sync for free. This is a CloudCart-internal carve-out (demo / staff / showcase stores). Regular merchants are NEVER on this list — noted here only so the audit records its existence; the wiki should NOT instruct merchants to seek "FREE_FOR" status.

### Permission

Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang feature hub.
- [[apps-multilang-main-model]] — master/sister flag (drives `x-default`) + per-site slugs.
- [[apps-multilang-create-step]] — sister-site creation wizard (subdomain slug field).
- [[apps-multilang-progress]] — sync progress (where the 402 block / FREE_FOR bypass applies).
- [[apps-multilang-stores]] — `show_language` switcher toggle.
- [[settings-domains]] — custom-domain mapping for a provisioned sister site.
- [[apps-lets-encrypt]] — SSL certs for sister-site custom domains.

## Open questions

None.
