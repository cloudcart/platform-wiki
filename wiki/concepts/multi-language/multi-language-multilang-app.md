---
type: concept
nav_path: "Concept → Multi-language → Multilang app"
aliases: ["Multilang app overview", "Master sister sites", "Sister site", "Master site", "Sister-site provisioning", "Cross-site SSO", "Multilang prerequisite apps", "Multilang uninstall"]
tags: [i18n, multi-language, apps, multilang, sister-site, concepts]
plan_gates: [multilang_product_translate, multilang_product_copy]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, customer/order locale, translation engine, sister-site model, sync/fallback, SEO + switcher).

# Multi-language — Multilang app + master/sister sites

## Definition

The **Multilang app** ([[apps-multilang]]) is the layer-3 system that makes multi-language storefronts work in CloudCart. Critically, its "sister site" model is **not** a virtual overlay on a single CloudCart store — each sister is provisioned as a **fully-independent CloudCart site** with its own database, catalog, customers, orders, theme, and subscription. The Multilang app sets up a one-way data sync that pushes catalog content (translated) from master to sister.

This has direct cost / billing implications: multi-language storefronts cost **more** than a single store at the CloudCart-billing level — the sister site needs its own plan, its own paid apps, its own SSL cert (via [[apps-lets-encrypt]]), its own domain config. The master and each sister have independent plan-feature quotas — the master's `multilang_product_translate` quota is what's billed for content translation; the sister inherits the same plan tier as the master at create-time but each has its own subscription thereafter.

## Scope

Covered:

- The "sister = fully-independent CloudCart site" rule and what it means for billing.
- Master/sister role: master = canonical content; sisters = receivers of synced (translated) content.
- The site relationship map (master ↔ sister correspondence per entity).
- Auto-bundled prerequisite apps installed on every new sister.
- Cross-site admin SSO via one-time login codes.
- Uninstall behaviour on master vs sister.

Not covered here:

- The translation engine (Google Cloud Translation API v3) + plan quotas — see [[multi-language-translation-engine]].
- One-way sync semantics, re-translation overwrite rule, and missing-translation 404 behaviour — see [[multi-language-sync-fallback]].
- Per-sister independence on pricing / payment / shipping / currency — see [[multi-language-sister-site-model]].
- Hreflang + language switcher mechanics — see [[multi-language-seo-and-switcher]].
- Plan-gate details — see [[plan-gates]].

## Contrasts

- **Multilang vs [[apps-stores]]** — Multilang is "one catalog, many languages" — sister sites share the catalog with translations; the master is the canonical source. [[apps-stores]] is "many catalogs / many businesses" — independent stores with potentially different products. Different apps, different data models.
- **Cloudio AI vs Multilang translation** — Cloudio uses OpenAI (via the merchant's `cloudio_ai` token balance). Multilang uses Google Cloud Translation API v3 (via its own plan feature `multilang_product_translate`). The merchant's Cloudio tokens do **not** subsidise Multilang. See [[multi-language-translation-engine]] and [[apps-cloudio-overview]].
- **Single store vs master+sister setup** — adding a single language to a CloudCart store doubles (or more) the billing footprint: each sister is a separate CloudCart site with its own plan subscription, its own paid apps, and its own SSL.

## Where it applies

### Sister-site provisioning

When the merchant installs Multilang and adds a language, the app provisions a new CloudCart site: a new domain / subdomain is configured (e.g., `en.merchant.com` or `merchant.com/en` sub-path), a new database / catalog is created (empty until content sync runs), a subscription is established at the master's current plan tier (independently renewable thereafter), the auto-bundled prerequisite apps (see below) are installed, and the site relationship map is initialised with the sister registered as a child of the master. The setup wizard ([[apps-multilang-create-step]]) walks the merchant through language picker, domain, currency, and theme inheritance.

### The site relationship map

The Multilang app maintains a **site relationship map** — for each entity (product, category, article), a row records the master → sister correspondence. It's used to generate the storefront's language switcher (master / sister URLs for the same product), emit SEO `<link rel="alternate" hreflang="LANG" href="URL">` tags (see [[multi-language-seo-and-switcher]]), and power the cross-site admin login. The map is persistent — once a master/sister pair is established for an entity, it stays linked even if the sister is later edited locally.

### Cross-site admin SSO

The Multilang app provides one-click navigation between the master admin and each sister admin via a one-time login code: from the master admin, the merchant clicks "Switch to EN site" (or similar control on [[apps-multilang-stores]]); the master mints a one-time login code and redirects to the sister admin URL; the sister admin validates the code and drops the merchant straight in without a re-login prompt. This is the merchant's main mechanism for editing per-sister overrides (pricing, shipping providers, theme) without having to remember separate sister-admin passwords.

### Auto-bundled prerequisite apps

Every new sister comes pre-installed with a fixed set of apps required for it to function: **GDPR** (sister needs its own cookie-consent / GDPR surface), **[[apps-lets-encrypt]]** (own SSL cert for the sister's domain), **Stores Sync** (keeps `quantity` in sync between master and sister so a Variant's stock decrement on the master reflects on the sister), **Domain Redirect** (canonical redirects for the sister's domain), and **Bumper Offer** (upsell app — verify, may be merchant-configurable). These cannot be uninstalled from the sister without breaking the Multilang relationship; treat the sister's app set as governed by the master.

### Uninstall behaviour

**On the master**: cascades the uninstall to every sister site. Each sister site's app instance is removed; the sister sites themselves **remain as independent stores**, but the master ↔ sister linkage is broken and content sync stops. The sister keeps its already-translated content and continues to operate at its own URL.

**On a sister**: the sister detaches from the master (the master removes its reference to that sister); the sister continues to operate as a standalone CloudCart store with whatever translated content it had. Re-installing doesn't automatically rebuild the relationship — the merchant re-establishes it via the setup wizard, which may need manual slug reconciliation.

Neither path deletes the sister site itself — they only break the sync linkage. Deleting a sister is a separate operation handled by the CloudCart account / billing flow.

## Related

- [[multi-language]] — hub.
- [[apps-multilang]] — Multilang app main page.
- [[apps-multilang-settings]] — configuration.
- [[apps-multilang-stores]] — sister-site setup + cross-site SSO controls + `show_language` toggle (see [[multi-language-seo-and-switcher]]).
- [[apps-multilang-products]] — per-product translation status, manual translate / copy actions.
- [[apps-multilang-create-step]] — setup wizard.
- [[apps-multilang-progress]] — sync queue progress tracker.
- [[apps-lets-encrypt]] — auto-bundled prerequisite on every sister.
- [[apps-stores]] — distinct multi-storefront feature for MULTIPLE BUSINESSES (not multi-language).
- [[multi-language-translation-engine]] — Google translation API + plan quotas.
- [[multi-language-sister-site-model]] — per-sister independence on pricing / payment / shipping / currency.
- [[multi-language-sync-fallback]] — one-way sync mechanics + re-translation overwrite + missing-translation 404.
- [[multi-language-seo-and-switcher]] — hreflang + storefront language switcher.

## Open Questions

- (verify) the full auto-bundled prerequisite list — Bumper Offer in particular may be merchant-toggleable rather than truly mandatory.
- (verify) precise behaviour when the master and a sister are on different plan tiers (e.g., master downgrades to a tier with lower `multilang_product_translate` quota — does the sister's translation pipeline halt immediately or at next quota-period rollover?).
