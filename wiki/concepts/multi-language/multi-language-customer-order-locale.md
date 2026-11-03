---
type: concept
nav_path: "Concept → Multi-language → Customer + order locale"
aliases: ["Customer locale", "Order locale", "Locale snapshot", "Order language frozen", "Per-customer language", "Transactional email language"]
tags: [i18n, multi-language, customer, order, locale, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, Multilang app, translation engine, sister-site model, sync/fallback, SEO + switcher).

# Multi-language — customer and order locale

## Definition

Every [[customer|Customer]] record carries a **mutable `locale` field** — the customer's preferred language. Every [[order|Order]] also carries a **`locale` field**, but the order's value is **snapshotted at creation and immutable thereafter**. This pair of fields is what makes "the customer who placed an order in English keeps getting English emails for that order, even after they switch their preferred language to Bulgarian" the correct behaviour rather than a bug.

The `locale` value is a language code (e.g., `bg`, `en`, `ro`). It is set independently of currency — see [[multi-language-sister-site-model]] for the language-currency independence rule.

## Scope

Covered:

- The Customer.`locale` field — set on registration, editable by customer + merchant.
- The Order.`locale` field — snapshotted at creation, immutable.
- What each locale drives (transactional emails, sister-site URL routing in email links, marketing-campaign language routing).
- The "historical orders keep their language" rule and why it matters for merchants who switch their primary language later.

Not covered here:

- The Multilang app + sister sites that make per-language storefronts possible — see [[multi-language-multilang-app]].
- The three-layer model (admin vs storefront UI vs storefront content) — see [[multi-language-layers]].
- The translation engine and quotas — see [[multi-language-translation-engine]].

## Contrasts

- **Customer locale (mutable) vs order locale (immutable)** — the customer can switch languages and the merchant can edit it in the customer's record; the order's locale is frozen at create time and cannot be edited from the admin. So a customer can change their preferred language, but their existing orders' emails stay in the language they were placed in.
- **Locale vs currency** — different fields, different semantics. A customer's locale is a per-customer preference; the order's currency is determined by the sister site the order was placed on. See [[multi-currency]] and [[multi-language-sister-site-model]].
- **Storefront language at the time of guest checkout vs registered-customer locale** — for guest checkouts, the order's locale is taken from the storefront's active language at submit; for logged-in checkouts, the order inherits the customer's locale.

## Where it applies

### Per-customer locale stored on the Customer record

Every [[customer|Customer]] has a `locale` field — the customer's preferred language. The platform sets this:

- **On registration** — from the storefront's current language at sign-up.
- **On profile edit** — the customer can change it in their account area.
- **On admin edit** — the merchant can change it in the customer's admin record.

The locale drives:

- Which language the customer's transactional emails are rendered in (order confirmation, password reset, etc. — see [[notification-delivery]]).
- Which sister-site URLs the platform sends them to when emails contain product / category links — the email's "View your order" link points to the sister site matching the customer's locale.
- Per-customer marketing campaigns' default language (the campaign editor uses this for "send in customer's preferred language" routing).

### Per-order locale frozen at creation

Every [[order|Order]] has a `locale` field — snapshotted from the customer's locale (or from the storefront's language at the time of guest checkout). This is **immutable after creation** — even if the customer later changes their preferred language, the order's emails / invoice / receipt stay in the original language.

Practical consequence: an English-speaking customer who places one order in English then switches their preferred language to Bulgarian sees their next order's emails in Bulgarian, but the first order's emails stay in English. This is correct — historical records shouldn't retroactively change language.

What the order's `locale` drives downstream:

- Order-confirmation email language at the moment the order is placed.
- Every follow-up transactional email for that order (shipped, fulfilled, refunded, etc.).
- The downloadable invoice / receipt PDF language.
- Storefront "track your order" page language (the page is rendered in the order's locale, not the visitor's current storefront language).

### Example — customer order in English on a BG-primary store

1. EN customer visits the merchant's BG primary site, clicks the language switcher → goes to `en.merchant.com`.
2. Customer browses, adds to cart, places an order. Cart's `locale = en`.
3. Order is created with `locale = en`. If guest, `customer_id` is null but their email is captured; the platform stores `customer.locale = en` if "Convert guests into members" later creates the customer record.
4. Order-confirmation email is rendered using the EN template; customer sees it in English.
5. Three months later, the merchant decides to fully switch their PRIMARY language to English (an org change). The master site is now EN; the BG site is now the sister.
6. Existing orders placed in EN still send emails in EN — their `locale` was frozen at creation. Existing orders placed in BG also still send emails in BG — same logic.

### Example — customer switches preferred language mid-stream

1. Customer A registered while browsing the BG storefront — `customer.locale = bg`.
2. Customer A places Order #1 — `order.locale = bg` (snapshotted).
3. Customer A later switches the storefront to EN, updates their profile language to `en` — `customer.locale = en` now.
4. Customer A places Order #2 — `order.locale = en` (snapshotted at THIS order's create time).
5. Marketing campaign "send in customer's preferred language" routes Customer A into the EN cohort going forward.
6. Order #1 follow-up emails (shipped, delivered, refunded) all still render in BG — the order's frozen `locale` wins over the customer's current preference.

## Related

- [[multi-language]] — hub.
- [[customer]] — Customer entity; carries the mutable `locale` field.
- [[order]] — Order entity; carries the snapshotted immutable `locale`.
- [[checkout-flow]] — where the order's `locale` is set from the cart / customer / storefront language at submit.
- [[notification-delivery]] — transactional emails respect the order's / customer's `locale`.
- [[multi-language-multilang-app]] — sister sites are what make per-language storefronts possible.
- [[multi-language-layers]] — three-layer model that distinguishes admin / storefront-UI / content language.

## Open Questions

- (verify) exact precedence when a logged-in customer's `customer.locale` differs from the active storefront language at submit — does the order snapshot the customer's preference or the storefront's active language? Working assumption: the storefront's active language (i.e., whichever sister site the customer is actually on) wins, since cross-sister content doesn't exist on the master.
