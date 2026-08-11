---
type: feature
nav_path: "Payment Providers → DSK BNPL → Promotions"
route_name: apps.dsk_bnpl.promotions
route_path: /admin/payment-providers/dsk_bnpl/promotions
aliases: ["DSK BNPL Promotions", "DSK promotions", "DSK promotion ID", "Промоции DSK BNPL", "ДСК промоции"]
tags: [paymentproviders, payment-providers, dsk-bnpl, bnpl, promotions]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---
# Promotions

## Purpose

DSK Bank can put specific products on a **promotional loan scheme** — e.g., "0% interest for 6 months on TV X", "free 12 months on washing machine Y" — and assigns each such product a **DSK promotion ID** in their bank-side system. By default CloudCart sends the cart's CloudCart product IDs to DSK's calculation API; this Promotions tab lets the merchant override that for specific products, telling CloudCart "when this CloudCart product is in the cart, send DSK's promotion ID instead." The result is that DSK returns the promotional loan terms (lower rate or interest-free) for that product instead of the default catalog terms.

The tab also exposes a rich-text **promotional HTML** field whose contents are stored in the provider configuration as `promo_html` and rendered on the product page (the customer sees a DSK promo banner / explainer block).

This page is the **hub** for the DSK BNPL Promotions tab. It is split into three aspects so the Assistant can drill into the exact slice a merchant is asking about.

## Sub-pages (in this cluster)

- [[dsk-bnpl-promo-mapping]] — the product → DSK promotion ID mapping: the promotions table, the Add / Edit modal (three cards), the live leasing-schemes preview + per-variant filtering, the override flow, and the bundle auto-rewrite rule.
- [[dsk-bnpl-promo-html]] — the rich-text **Promo text area** field stored as `promo_html` and rendered on the storefront product page next to DSK's installment table.
- [[dsk-bnpl-promo-bulk]] — Excel bulk export / import of the promotion rows, the (currently non-enforced) start / end date gating, and the full backend endpoint reference.

## Where to find it

Sidebar → **Payment Providers** → **DSK BNPL** → **Promotions** tab.

The route is `/admin/payment-providers/dsk_bnpl/promotions`. The page renders a list/table of promotion rows (one per product) plus the rich-text editor for `promo_html`. Backend endpoints all live under `/admin/api/payment_providers/dsk_bnpl/`.

## What the merchant can do here

- Map a CloudCart product to a DSK promotion ID, with optional scheme-variant filters and start/end dates — see [[dsk-bnpl-promo-mapping]].
- Preview the live installment table the customer will see, and tick which pricing variants survive — see [[dsk-bnpl-promo-mapping]].
- Edit the **Promo text area** rich-text snippet (`promo_html`) shown on the product page — see [[dsk-bnpl-promo-html]].
- Bulk export all mappings to Excel and re-import them in bulk — see [[dsk-bnpl-promo-bulk]].

## Settings & fields

The Promotions tab carries two distinct configuration surfaces:

- **The promotion rows** — one row per product, each holding a Product, a DSK promotion ID, an optional variant filter list, and a start/end date range. Full field reference on [[dsk-bnpl-promo-mapping]].
- **The `promo_html` blob** — a single rich-text block stored in the provider configuration, saved by its own **Save** button. Full reference on [[dsk-bnpl-promo-html]].

## Business rules

- **A mapping is necessary but not sufficient.** DSK's promotional terms only show at checkout when both the merchant has added the mapping AND DSK Bank has actually configured the promotion for that ID on their side. The mapping by itself doesn't create a promotion — see [[dsk-bnpl-promo-mapping]].
- **Bundles auto-rewrite** to the first child product's ID on save, because DSK's pricing API needs a real product ID — see [[dsk-bnpl-promo-mapping]].
- **Date gating is stored but not enforced** by the storefront at the time of writing — see [[dsk-bnpl-promo-bulk]].
- **Plan-gating** inherits from the parent DSK BNPL provider, which is **none** — every CloudCart plan can use this tab.

## Related

- [[payment-providers-dsk-bnpl]] — parent hub for DSK BNPL.
- [[payment-providers-dsk-bnpl-settings]] — Store Unique ID + public key + minimum order value.
- [[payment-providers-fibank-bnpl-promotions]] — equivalent Promotions screen for the Fibank BNPL provider (same shape, different bank).
- [[product]] — the entity each promotion row maps to.
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

_None._
