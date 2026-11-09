---
type: concept
nav_path: "Concept → Multi-language → Customer + order locale"
aliases: ["Customer locale", "Order locale", "Locale snapshot", "Order language", "Per-customer language", "Transactional email language", "Email language"]
tags: [i18n, multi-language, customer, order, locale, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, Multilang app, translation engine, sister-site model, sync/fallback, SEO + switcher).

# Multi-language — customer and order locale

## Definition

Every [[order|Order]] carries a **`locale`** (a language code such as `bg`, `en`, `ro`), set when the order is created to the **store's language** (the storefront language in [[settings-general]]). The [[customer|Customer]] record carries **no** language field of its own: there is no per-customer preferred language.

What decides the language a shopper receives is therefore the **store**, not the person. A store that sells in several languages does so through sister sites ([[multi-language-multilang-app]]); each sister site is a separate store with its own language, its own email templates and its own orders.

## Scope

Covered:

- The order's `locale` — where it comes from and what it drives.
- Which language transactional emails use.
- The absence of a per-customer language.

Not covered here:

- The Multilang app + sister sites that make per-language storefronts possible — see [[multi-language-multilang-app]].
- The three-layer model (admin vs storefront UI vs storefront content) — see [[multi-language-layers]].
- The translation engine and quotas — see [[multi-language-translation-engine]].

## Contrasts

- **Order locale vs email language** — related but not the same thing. Customer emails (order confirmation, status changes, password reset and the rest) are always built in the store's **current** language, with the English template version as fallback when that language has none. The order's own `locale` is used for its invoice, receipt and credit-note PDFs and for money formatting. See [[omnichannel-mails-order-confirmation]].
- **Locale vs currency** — different fields, different semantics. The order's currency is determined by the store (sister site) the order was placed on. See [[multi-currency]] and [[multi-language-sister-site-model]].
- **Store language vs admin language** — the admin panel's own language (set separately) never changes the language of what shoppers receive.

## Where it applies

### Order `locale`

- Set on creation to the store's language, when the order does not already carry one.
- Drives the language of the order's **invoice, receipt and credit-note PDFs** (falling back to the store's language when empty).
- Does **not** choose the email template: emails follow the store's current language.

### Emails follow the store, not the shopper

- One store = one storefront language = one email language. The shopper's browser language, the language they browsed in, and any past order's `locale` play no part.
- If the merchant changes the store's language in [[settings-general]], every email sent from then on (including follow-ups on older orders) uses the new language's template version, or English when that version does not exist.
- An order placed on an English sister site belongs to that English store and gets that store's (English) emails.

### Example — BG store with an EN sister site

1. A shopper on `merchant.bg` (Bulgarian store) orders → Bulgarian confirmation; order `locale = bg`.
2. A shopper on the EN sister site (separate English store) orders → that store's English confirmation; order `locale = en`.
3. The merchant later switches `merchant.bg`'s language to English. New emails from `merchant.bg`, including status changes on the first order, now use the English template versions; the first order's invoice PDF stays Bulgarian, because its `locale` is still `bg`.

## Related

- [[multi-language]] — hub.
- [[customer]] — Customer entity; no language field of its own.
- [[order]] — Order entity; carries the `locale` set at creation.
- [[checkout-flow]] — where the order is created.
- [[notification-delivery]] — how transactional emails are sent; their language is the store's.
- [[multi-language-multilang-app]] — sister sites are what make per-language storefronts possible.
- [[multi-language-layers]] — three-layer model that distinguishes admin / storefront-UI / content language.

## Open Questions

No outstanding questions.
