---
type: concept
nav_path: "Concept → Multi-language → Three layers"
aliases: ["Multi-language layers", "Admin language vs storefront language", "Storefront UI labels", "Translations layer", "Layer model", "Three-layer multi-language model"]
tags: [i18n, multi-language, admin, storefront, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (customer/order locale, Multilang app, translation engine, sister-site model, sync/fallback, SEO + switcher).

# Multi-language — three layers

## Definition

Multi-language inside CloudCart is **not one switch** — it is three independent layers, each driven by a different setting and each managed in a different place. Merchants and support agents who treat it as a single switch will reliably misdiagnose tickets. Flipping one layer does **not** flip the others.

| Layer | What it controls | Where it lives | Cost |
|---|---|---|---|
| 1. Admin panel language | The language of the admin UI itself (sidebar, page titles, form labels, validation messages) | per-staff account setting + store-wide default in [[settings-general]] | free |
| 2. Storefront UI labels | Platform-shipped storefront strings — buttons ("Add to cart"), validation, headings, email subjects | [[settings-translations]] (Settings → Translations) | free |
| 3. Storefront content | The actual catalog text — product names, descriptions, category names, blog articles, CMS pages, custom fields | [[apps-multilang]] (Multilang app) — separate sister site per language | plan-gated (`multilang_product_translate`, `multilang_product_copy` quotas) |

## Scope

Covered:

- The three layers and what each layer touches / doesn't touch.
- Layer 1 — per-staff vs store-wide admin language, and why there is no per-string admin-label override UI.
- Layer 2 — [[settings-translations]] override scoping (`(locale, theme)` pair), reset paths, master toggle, no CSV import.
- Layer 3 — what kinds of entities the Multilang app translates (product / category / article / custom field / CMS page).

Not covered here:

- The Multilang app's mechanics (master/sister sites, app installation) — see [[multi-language-multilang-app]].
- The translation engine itself (Google Cloud Translation API v3) and quotas — see [[multi-language-translation-engine]].
- Customer / order locale semantics — see [[multi-language-customer-order-locale]].

## Contrasts

- **Admin language vs storefront language** — independent. A merchant can run admin in English while the storefront stays Bulgarian, or vice versa. The two never share a setting.
- **Storefront UI labels vs storefront content** — [[settings-translations]] overrides platform-shipped strings (buttons, validation, headings); [[apps-multilang]] handles full catalog content. UI labels are free; content is plan-gated.
- **Per-staff admin language vs store-wide default** — the per-staff value wins where set; the store-wide default in [[settings-general]] applies to staff who haven't picked their own.

## Where it applies

### Layer 1 — Admin panel language

Set per staff account in their personal settings (the per-staff value wins) **or** as a store-wide default in [[settings-general]]:

- **Admin Panel Language** (per-staff) — language of the admin UI labels for THIS staff member only. Stored on the staff member's user record.
- **Admin Panel Language** (store default in [[settings-general]]) — default for new staff and for staff who haven't picked their own.

Changing the admin language ONLY affects the admin UI — sidebar labels, page titles, form labels, validation messages in the admin. It does NOT affect the storefront, the catalog content, or transactional emails sent to customers.

The admin uses a separate translation pipeline (`admin_translations` setting) controlled by a different endpoint than the storefront's `translations` setting. There is **no merchant-accessible UI for editing admin labels per-row** — admin labels are fixed per language; the merchant can only switch which language they see, not customise specific strings. The available admin-panel languages depend on which languages CloudCart has shipped (typically: Bulgarian, English, and a handful of other regional languages). (verify exact list)

### Layer 2 — Storefront UI labels via [[settings-translations]]

The Translations screen at Settings → Translations lets the merchant override platform-shipped storefront labels per language + per theme. Common targets:

- Button labels: "Add to cart" → "Купи сега" or "Buy now".
- Validation messages: "Please enter a valid email" → "Моля въведете валиден имейл".
- Section headings: "Related products" → "Свързани продукти".
- Email subjects: "Your order has been received" → "Поръчката ви е получена".

**Override scoping** — the most frequently-misunderstood rule:

- **Per language** — overrides made when the storefront language is BG apply ONLY when BG is the active storefront language; switching to EN loads a different override pool.
- **Per theme** — overrides made under Theme A don't carry over to Theme B (the merchant has to redo them per theme).

Combined: the override pool is keyed on the `(locale, theme)` pair. A merchant maintaining BG + EN on Theme A has **two** pools; adding Theme B doubles that to four.

**Master toggle**: the merchant can disable the entire override system via a "system labels" toggle — when OFF, only platform defaults are shown (overrides are preserved in the DB but ignored). Useful as a diagnostic "what's the platform default?" mode.

**Reset paths**:
- Per-row reset — clears one override; the platform default is shown.
- Reset all to default — clears every override; destructive and irreversible.

There is no CSV export/import for translations; the merchant types each override manually.

### Layer 3 — Storefront content via [[apps-multilang]]

The Multilang app handles full content translation. What it translates:

- **Product translations** — name, description, short description, SEO title / description per product.
- **Category translations** — name, description per category.
- **Blog article translations** — title, body, excerpt per article.
- **Custom field translations** — per defined custom field that has translatable content.
- **CMS page translations** — page title, body for static pages.

Each language gets its own **sister site** — its own URL / domain, its own catalog (translated copies), and its own per-language overrides for pricing, payment providers, and shipping providers. See [[multi-language-multilang-app]] for the master/sister model and [[multi-language-sister-site-model]] for per-sister independence on non-content fields.

The translation engine itself (Google Cloud Translation API v3, the `multilang_product_translate` / `multilang_product_copy` queue tasks, and the plan quotas) is covered in [[multi-language-translation-engine]].

## Related

- [[multi-language]] — hub.
- [[settings-translations]] — Layer 2 override screen.
- [[settings-general]] — Layer 1 store-wide admin language default + storefront language picker.
- [[apps-multilang]] — Layer 3 Multilang app main page.
- [[multi-language-multilang-app]] — Multilang app + master/sister mechanics.
- [[multi-language-translation-engine]] — Google translation API + plan quotas.
- [[design-themes]] — theme selection; switching theme loads a different Layer-2 override pool.

## Open Questions

- (verify) the exact list of admin-panel languages CloudCart currently ships.
