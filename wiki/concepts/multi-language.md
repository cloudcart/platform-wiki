---
type: concept
nav_path: "Concept → Multi-language"
route_name: ""
route_path: ""
aliases: ["Multi-language", "Multilingual storefront", "Multilingual store", "Multi-language storefront", "Translations", "Storefront translations", "Catalog translation", "Per-language content", "Hreflang", "Език на магазина", "Език на админ панела", "Многоезичен магазин", "Преводи на каталога"]
tags: [i18n, multi-language, storefront, admin, concepts]
plan_gates: [multilang_product_translate, multilang_product_copy]
created: 2026-05-23
updated: 2026-06-10
source_count: 3
---

# Multi-language

## Definition

**Multi-language** is the platform-wide system for running CloudCart in more than one language — both inside the admin panel (which language the merchant sees) AND on the customer-facing storefront (which language each customer sees when browsing products, going through checkout, and receiving transactional emails). The two are separate concerns with separate switches and separate translation pools.

**The single most-misunderstood fact**: a "multi-language store" in CloudCart is **not one site rendered in many languages**. The Multilang app provisions each translated language as a **fully-independent CloudCart sister site** — its own catalog, customers, orders, theme, SSL cert, and subscription — and sets up a one-way data sync that pushes translated catalog content from master to sister. Multi-language storefronts therefore cost **more** than a single store at the CloudCart-billing level. See [[multi-language-multilang-app]].

The system has **three distinct layers**, often confused with each other:

1. **Admin panel language** — set per staff account (or store-wide default in [[settings-general]]). Drives the language of the admin UI. Free.
2. **Storefront UI labels** — overrideable via [[settings-translations]]. Customisations override the platform's built-in storefront strings ("Add to cart", validation messages, headings, email subjects). Free. Override pool is scoped to `(locale, theme)`.
3. **Storefront content translation** — handled by [[apps-multilang]]. Translates the actual catalog content (product names, descriptions, categories, blog articles, CMS pages). Plan-gated by `multilang_product_translate` + `multilang_product_copy` quotas.

For full details on each layer, the customer/order locale model, the translation engine, sister-site independence, sync rules, and SEO surfaces — drill into the aspect pages below.

## Sub-pages (in this cluster)

Split into 7 aspect pages, each covering one well-scoped slice. Drill into the aspect that matches the question, not every page.

- [[multi-language-layers]] — the three independent layers (admin language / storefront UI labels via [[settings-translations]] / storefront content via [[apps-multilang]]); per-staff vs store-wide admin language; the `(locale, theme)` override-scope rule.
- [[multi-language-customer-order-locale]] — Customer.`locale` (mutable) vs Order.`locale` (snapshotted at creation, immutable); what drives transactional email language; historical-orders-keep-their-language rule.
- [[multi-language-multilang-app]] — Multilang app overview; "sister = fully-independent CloudCart site" rule + billing impact; site relationship map; cross-site admin SSO via one-time login codes; auto-bundled prerequisite apps; uninstall cascade behaviour on master vs sister.
- [[multi-language-translation-engine]] — Google Cloud Translation API v3 (NOT Cloudio / OpenAI); `multilang_product_translate` vs `multilang_product_copy` queue tasks; plan-feature quota exhaustion; no review workflow (translations land live).
- [[multi-language-sister-site-model]] — per-sister independence on pricing / payment providers / shipping providers / tax rules / themes / currency / URL handles (slugs); the currency-language independence rule; why "I changed the price but the EN site shows the old price" is almost always master-vs-sister confusion.
- [[multi-language-sync-fallback]] — three sync rules: (1) master → sister, one-way; (2) re-translation OVERWRITES sister-side manual polish; (3) NO runtime fallback (missing translation = 404 on sister, not source-language render); the recommended "edit master, translate ONCE, polish sister LAST" workflow.
- [[multi-language-seo-and-switcher]] — hreflang tags auto-generated per sister (`x-default` for master, `<lang>` for sisters); per-site SEO meta translated alongside content; storefront language switcher module (`show_language` per-sister toggle); platform does NOT auto-detect browser language and redirect.

## Why it matters to the merchant

Multi-language is the **gating system for reaching markets beyond the store's primary language**. The most-frequent failure modes (each detailed on its sub-page above):

- **The three layers are independent.** Changing the admin language doesn't translate the storefront; switching the storefront language doesn't translate product names; installing Multilang doesn't override "Add to cart" labels.
- **Sister-site sync is master → sister, one-way; re-translation OVERWRITES sister-side polish.** Treating the sister as a parallel canonical edit surface is the most common Multilang misconception.
- **Per-sister commercial settings are independent of master.** Pricing, payment providers, shipping, tax, currency — all configured per sister; price changes on the master do NOT propagate.
- **Multi-language is NOT free for the catalog layer.** UI labels free; content translation is plan-gated.
- **Order language is frozen at creation.** A customer who placed an order in English keeps getting English emails for that order even after they switch their preferred language.
- **Hreflang + language switcher are auto-generated** from the master/sister relationship map.

## Scope

This concept covers (across the 7 sub-pages): the three-layer model (admin vs storefront UI vs storefront content); customer and order locale fields + the immutable-on-order rule; the Multilang app + master/sister site model; translation engine + plan quotas; per-sister independence on commercial settings + currency-language independence; one-way sync, re-translation overwrite, and no-runtime-fallback rules; SEO hreflang + language switcher module.

What it does NOT cover:

- The Cloudio AI translator skill (different system — Cloudio uses OpenAI; Multilang uses Google Cloud Translation API). See [[apps-cloudio-overview]].
- Multi-storefront / multi-business model with potentially different catalogs across stores. See [[apps-stores]].
- Per-language tax rules in detail — see [[tax-computation]].
- Right-to-left language support for theme directional CSS — a theme / custom-CSS concern; not extensively documented.
- Internal cost accounting — CloudCart's per-symbol margin over Google's wholesale rate (CloudCart-internal; not merchant-facing).

## Contrasts

- **Multilang vs [[apps-stores]]** — Multilang is "one catalog, many languages" (shared content with translations); Stores is "many catalogs / many businesses" (independent catalogs). See [[multi-language-multilang-app]].
- **Multilang vs [[apps-cloudio-overview]] (Cloudio AI)** — Multilang uses Google Cloud Translation API v3; Cloudio uses OpenAI. Separate plan-features, separate token balances. See [[multi-language-translation-engine]].
- **Admin language vs storefront language** — independent layers. See [[multi-language-layers]].
- **Customer locale (mutable) vs order locale (immutable)** — see [[multi-language-customer-order-locale]].
- **Master site (content canonical) vs sister site (commercial settings canonical)** — see [[multi-language-sister-site-model]].
- **Translate task vs Copy task** — translate runs Google's API; copy preserves source-language text. See [[multi-language-translation-engine]].

## Where it applies

The multi-language system spans admin settings, app screens, customer / order data, SEO surfaces, and downstream notifications. Each sub-page documents its own surface. Cross-cutting consequences:

- **Transactional emails respect the order's / customer's `locale`** — [[multi-language-customer-order-locale]] + [[notification-delivery]].
- **Storefront catalog rendering is per-sister** — each sister's listing pages, product pages, and search results reflect only that sister's translated entities; missing-translation = 404. [[multi-language-sync-fallback]].
- **SEO hreflang tags emitted per page on every sister** — [[multi-language-seo-and-switcher]].
- **Plan-gate exhaustion halts new translations** — [[multi-language-translation-engine]] + [[plan-gates]].

## Related

- [[settings-translations]] / [[settings-general]] — Layer-2 + Layer-1 admin surfaces.
- [[apps-multilang]] / [[apps-multilang-settings]] / [[apps-multilang-stores]] / [[apps-multilang-products]] / [[apps-multilang-create-step]] / [[apps-multilang-progress]] — Multilang app surfaces.
- [[multi-currency]] — currency is independent of language.
- [[seo-handling]] — hreflang and per-site SEO.
- [[customer]] / [[order]] — `locale` fields (mutable vs snapshotted).
- [[product]] / [[category]] — translated copies on sister sites.
- [[checkout-flow]] — order's `locale` set at submit.
- [[notification-delivery]] — transactional emails respect `locale`.
- [[plan-gates]] — translation quotas.
- [[apps-stores]] — distinct multi-storefront feature for multiple businesses.
- [[apps-cloudio-overview]] — Cloudio AI (separate from Multilang).
- [[apps-lets-encrypt]] — auto-bundled prerequisite on every sister.
- [[backups-and-restore]] — backups capture sister sites alongside master.

## Open Questions

- ⏸️ **Right-to-left language support** (Arabic, Hebrew). CloudCart's first-party themes do NOT ship with RTL CSS. A merchant who configures an RTL language via [[apps-multilang]] gets the locale activated for translation purposes, but the storefront layout itself does not flip to RTL automatically — the theme must be customised via [[design-custom-assets]] (Custom CSS/JS) or a custom-built theme to support RTL rendering.

All previously-flagged questions resolved or distributed to sub-pages. See aspect pages for any aspect-specific `(verify)` items.
