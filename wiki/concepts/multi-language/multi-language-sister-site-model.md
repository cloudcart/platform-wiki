---
type: concept
nav_path: "Concept → Multi-language → Sister-site independence"
aliases: ["Sister site independence", "Per-sister overrides", "Per-sister pricing", "Per-sister payment providers", "Per-sister shipping providers", "Per-sister currency", "Currency-language independence", "Per-site slug", "Per-site URL handle"]
tags: [i18n, multi-language, multilang, sister-site, currency, pricing, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, customer/order locale, Multilang app, translation engine, sync/fallback, SEO + switcher).

# Multi-language — sister-site independence (non-content fields)

## Definition

A common merchant misconception is that "the master is the source of truth for everything on the sister." It is **not**. The master is the canonical source for **catalog CONTENT only** — product names, descriptions, category labels, blog articles, CMS pages, custom-field translations. **Per-market commercial settings** stay independent per sister and are NOT pushed from master to sister. This includes pricing, payment providers, shipping providers, tax rules, themes, currency, and URL handles.

This independence is what lets a Bulgarian merchant offer different EUR prices on the English sister, accept different payment methods per market, and ship via different couriers — all while sharing one translated catalog across all sites.

## Scope

Covered:

- The list of per-sister independent fields (pricing, payment, shipping, tax, themes, currency, slug).
- The currency-language independence rule and what it means for customers.
- Per-site URL handle (slug) and the relationship-table mapping.

Not covered here:

- The Multilang app itself, master/sister provisioning, prerequisite apps — see [[multi-language-multilang-app]].
- Content sync mechanics (one-way, overwrite-on-re-translate) — see [[multi-language-sync-fallback]].
- The customer / order locale fields — see [[multi-language-customer-order-locale]].
- The currency model (BGN → EUR transition, FX, base currency) — see [[multi-currency]].

## Contrasts

- **Catalog content (master-driven) vs commercial settings (sister-independent)** — content syncs master → sister; pricing, payment, shipping, tax, theme do not. The merchant must configure each sister independently for these.
- **Language vs currency** — independent dimensions. The customer cannot "switch language without changing currency" because switching language navigates to the sister site, and the sister site has its own currency. There is no in-page currency-only toggle.
- **Master slug vs sister slug** — independent. Each sister has its own URL handle per entity; the relationship table maps master `primary_slug` ↔ sister `secondary_slug` so cross-site links resolve.

## Where it applies

### Per-sister commercial independence

Each sister site has its own configuration for:

- **Pricing** — different EUR / RON / GBP prices for the same product across sister sites. Each sister has its own currency setting; prices are stored per-sister in the sister's own currency. The merchant does NOT enter a master price that gets FX-converted — they enter the price they want on each sister site.
- **Payment providers** — different payment options per market (e.g., Bulgarian sister site uses iCard / ePay; English sister site uses Stripe; Romanian sister uses Netopia). The merchant configures payment apps separately per sister.
- **Shipping providers** — different couriers per market (e.g., BG site uses Speedy / Econt; RO site uses Cargus; EN/EU sites use DPD / DHL).
- **Templates / themes** — different storefront templates per language if needed. A merchant might pick a different theme for the EN sister to emphasise different brand cues for a different market.
- **Tax rules** — different VAT rates / tax-inclusion conventions per country. The sister's `country` setting drives [[tax-computation]] independently of the master.

This means cross-market commercial differences (the Polish market expects different shipping and different VAT than the Bulgarian one, even if the products are identical) can be configured cleanly — but the merchant has to do the configuration per sister, not once on the master.

### Currency and language are independent

Storefront language and storefront currency are SEPARATE settings:

- Each sister site has its own currency (BG sister could be in BGN, EN sister could be in EUR, RO sister could be in RON).
- Customers cannot "switch language without changing currency" — switching language navigates to the sister site, which has its own currency.
- There is **no automatic FX conversion** between sister sites; the merchant configures prices independently per sister.

If a merchant wants "same currency, different language" (e.g., serve both BG and EN audiences but always in EUR), they configure both sisters with EUR currency. If they want "same language, different currency" (rare — typically achieved via account-level locale negotiation), see [[multi-currency]].

See [[multi-currency]] for the full currency model and the BGN → EUR transition pattern.

### Per-site URL handle (slug)

Each translated entity has its OWN URL handle on the sister site. A product can have:

- `/product/laptop-acer-aspire` on the EN sister.
- `/produkt/laptop-acer-aspire` on the BG master.
- `/produs/laptop-acer-aspire` on the RO sister.

The slug is independently editable per site; the relationship table on the master maps master `primary_slug` ↔ sister `secondary_slug` so the language switcher's "View this same product in EN" button works even when the slugs differ. See [[multi-language-seo-and-switcher]] for how the switcher uses this mapping to emit hreflang.

The slug is initially set automatically when [[multi-language-translation-engine|translation]] runs (Google's transliteration / translation produces an initial slug). The merchant can edit it per sister thereafter — sister-side slug edits stay local and are NOT overwritten by re-translation of CONTENT fields (only the body content is overwritten by re-translate; the slug, once set, is treated as a separate field). (verify exact slug-overwrite behaviour on re-translate.)

### Why this matters operationally

When a merchant says "I changed the price on a product but the EN site still shows the old price," the right diagnosis is almost always: **the price change was made on the master**, which doesn't sync to the sister. The merchant has to log into the sister admin (via cross-site SSO — see [[multi-language-multilang-app]]) and update the price there.

Symmetrically, when a merchant says "I activated Stripe on my BG site and it works, but my EN customers can't pay" — the right diagnosis is: **payment providers are per-sister**; Stripe needs activating on the EN sister too.

This is the single most common source of "Multilang isn't working as expected" tickets that aren't actually about translation.

## Related

- [[multi-language]] — hub.
- [[multi-language-multilang-app]] — Multilang app + cross-site SSO (how to log into the sister to edit per-sister settings).
- [[multi-language-translation-engine]] — what IS pushed from master (content + SEO meta).
- [[multi-language-sync-fallback]] — one-way sync mechanics that explain why per-sister edits stay local.
- [[multi-language-seo-and-switcher]] — how the per-site slug mapping powers hreflang + the storefront language switcher.
- [[multi-currency]] — sister concept; currency is independent of language; each sister has its own currency.
- [[tax-computation]] — per-sister VAT computation driven by sister's country setting.
- [[shipping-calculation]] — per-sister courier configuration.
- [[payment-provider-mechanism]] — per-sister payment provider activation.

## Open Questions

- (verify) the exact set of sister-independent fields — `country`, `currency`, `tax_*`, theme, payment apps, shipping providers, prices are confirmed; whether things like minimum-order-amount thresholds and free-shipping rules are also per-sister is plausible but unverified.
- (verify) whether per-sister slug edits survive a subsequent re-translate (working assumption: yes, slug is treated as a separate field once set; only content fields are overwritten).
