---
type: concept
nav_path: "Concept → Multi-language → SEO + switcher"
aliases: ["Hreflang", "Hreflang x-default", "Language switcher", "Storefront language switcher", "show_language", "Per-site SEO meta", "Auto-detection browser language", "Language alternates"]
tags: [i18n, multi-language, seo, hreflang, storefront, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, customer/order locale, Multilang app, translation engine, sister-site model, sync/fallback).

# Multi-language — SEO + language switcher

## Definition

Once master + sister sites are configured via [[multi-language-multilang-app]], the Multilang app handles the customer-facing surfaces that connect the sites — **the SEO inter-language signal** (`<link rel="alternate" hreflang>` tags emitted on every page) and **the storefront language switcher module** (a header dropdown letting customers flip to the same page on a different sister). Both are computed from the site relationship map.

Critically, the platform does NOT auto-detect customer browser language and auto-redirect. Customers land on whichever sister's URL they navigated to; the switcher gives them a manual jump.

## Scope

Covered:

- Hreflang tag emission: `<link rel="alternate" hreflang>` per sister, `x-default` for master.
- Per-sister SEO meta (translated alongside content, distinct URL handles).
- The customer-facing language switcher module and its `show_language` per-sister toggle.
- The "no auto browser-language redirect" rule and where merchants can layer it on themselves.

Not covered here:

- The Multilang app + master/sister provisioning — see [[multi-language-multilang-app]].
- Translation of SEO meta itself (handled by the translate task alongside content) — see [[multi-language-translation-engine]].
- Per-sister URL handles (slugs) — see [[multi-language-sister-site-model]].
- General SEO surfaces unrelated to multi-language — see [[seo-handling]].

## Contrasts

- **Hreflang `x-default` (master) vs language-specific hreflang (sisters)** — the master site emits `hreflang="x-default"` so search engines know it's the canonical "no preference" fallback. Each sister emits its own `hreflang="<lang>"` (e.g., `hreflang="en"`, `hreflang="ro"`).
- **Auto-hreflang vs manual hreflang** — fully automatic. The merchant doesn't configure inter-language pointers manually; they're computed from the master/sister relationship table.
- **Switcher ON (`show_language = true`) vs OFF** — per-sister setting. When OFF, the switcher module is hidden and customers stay locked to the sister they landed on.
- **No platform-level browser-language redirect vs theme-layered redirect** — the platform default is "respect the URL the customer landed on." Merchants who want auto-redirect by browser language add it via theme JavaScript or [[design-custom-assets]].

## Where it applies

### Hreflang tags auto-generated

The Multilang app emits SEO `<link rel="alternate" hreflang>` tags automatically on every translated entity's page. The merchant doesn't manually configure SEO inter-language pointers — they're computed from the master/sister relationship table (see [[multi-language-multilang-app]] for the relationship map).

- Master site uses `<link rel="alternate" hreflang="x-default" href="<master-url>">` — signals "this is the default version for users whose language preference doesn't match any sister".
- Each sister uses `<link rel="alternate" hreflang="<lang>" href="<sister-url>">` where `<lang>` is the sister's language code (e.g., `en`, `ro`, `de`).
- Hreflang tags on each sister site point to **all other sister sites** (and to the master) — so search engines understand the full set of language alternatives and can rank the right language for the right user.

Practical implication: a merchant who launches an EN sister doesn't need to file sitemaps for inter-language alternates separately. Google / Bing read the hreflang tags directly from each page and infer the language graph.

### Per-site SEO meta

Each product / category / article on each sister site has its own:

- **SEO title** (translated by the translate task — see [[multi-language-translation-engine]]).
- **SEO description** (translated).
- **SEO keywords** (where applicable, translated).
- **Canonical URL** on its own domain (computed from the sister's domain + the sister's slug — see [[multi-language-sister-site-model]] for the per-site slug rule).

Multilang's auto-translation translates the SEO fields along with the content — the merchant doesn't have to separately translate meta tags. The merchant can override per-sister via the sister's product / category editor if they want manual SEO copy (subject to the re-translation overwrite rule — see [[multi-language-sync-fallback]]).

### Customer-facing language switcher

The Multilang app installs a storefront language-switcher module — typically a dropdown in the header. Customers click it to navigate to the sister site equivalent of the page they're currently on (e.g., from `merchant.bg/produkt/laptop-acer-aspire` to `en.merchant.com/product/laptop-acer-aspire`). The switcher uses the site relationship map's `primary_slug` ↔ `secondary_slug` mapping so the navigation lands on the same product even when the slugs differ.

The switcher is enabled per the **`show_language`** setting (configurable per sister site via [[apps-multilang-stores]]). When OFF, the switcher is hidden on that sister — useful for stores that want the customer locked to their detected / chosen language.

Visual presentation of the switcher (dropdown vs flag icons vs language names) is a theme-level concern; the Multilang app exposes the data, and the theme renders it.

### No platform-level browser-language auto-redirect

The platform does **NOT** auto-detect browser language and redirect customers to the matching sister. The default behaviour is "show the language the customer landed on" with the switcher allowing manual switch.

If the merchant wants browser-language auto-redirect (e.g., a customer with `Accept-Language: en-US` browsing the BG master should auto-redirect to the EN sister), that's a separate behaviour the merchant layers on via:

- Theme JavaScript that reads `navigator.language` and `window.location.href` and redirects on first visit.
- [[design-custom-assets]] (Custom CSS / JS) injecting the same logic without theme-file edits.
- A third-party "GeoIP redirect" app (verify availability in the marketplace).

The platform's choice not to auto-redirect by default is deliberate — many customers prefer their landed URL even when their browser language is different (e.g., a Bulgarian customer abroad using a US-locale browser may still want to land on the BG site).

### Example — hreflang on a 3-site setup

Merchant has BG master + EN sister + RO sister. On the master's product page for "Laptop Acer Aspire 5", the platform emits:

```
<link rel="alternate" hreflang="x-default" href="https://merchant.bg/produkt/laptop-acer-aspire">
<link rel="alternate" hreflang="bg" href="https://merchant.bg/produkt/laptop-acer-aspire">
<link rel="alternate" hreflang="en" href="https://en.merchant.com/product/laptop-acer-aspire">
<link rel="alternate" hreflang="ro" href="https://ro.merchant.com/produs/laptop-acer-aspire">
```

On each sister's equivalent page, the same set of alternates is emitted (the relationship table is shared across sites). Search engines now have full inter-language navigation data without the merchant configuring anything.

## Related

- [[multi-language]] — hub.
- [[multi-language-multilang-app]] — the site relationship map that powers hreflang + the switcher.
- [[multi-language-sister-site-model]] — per-site slugs that the switcher mapping resolves.
- [[multi-language-translation-engine]] — SEO meta is translated alongside content.
- [[multi-language-sync-fallback]] — re-translation overwrites manual SEO meta polish.
- [[seo-handling]] — general SEO surfaces; the Multilang-specific hreflang behaviour is documented here.
- [[apps-multilang-stores]] — where `show_language` per-sister toggle lives.
- [[design-custom-assets]] — where merchants layer on browser-language auto-redirect if they want it.

## Open Questions

- (verify) whether the master's hreflang set includes a self-referencing `hreflang="<master-lang>"` tag in addition to `x-default` — the example above assumes yes (both `x-default` and `bg` for the BG master), but the actual emitted output may use `x-default` alone for the master.
- (verify) whether the switcher hides entire categories when those categories are missing on the target sister (per the missing-translation 404 rule in [[multi-language-sync-fallback]]).
