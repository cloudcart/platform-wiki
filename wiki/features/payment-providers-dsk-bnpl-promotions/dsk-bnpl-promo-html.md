---
type: feature
nav_path: "Payment Providers → DSK BNPL → Promotions → Promo HTML"
route_name: apps.dsk_bnpl.promotions
route_path: /admin/payment-providers/dsk_bnpl/promotions
aliases: ["DSK BNPL promo HTML", "promo_html DSK", "DSK promo banner", "Promo text area DSK BNPL", "Промо текст DSK BNPL"]
tags: [paymentproviders, payment-providers, dsk-bnpl, bnpl, promotions, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---
> Part of [[payment-providers-dsk-bnpl-promotions]]. See the hub for the other aspects (the product → DSK promotion ID mapping, and bulk export / import).

# DSK BNPL — Promo HTML banner

## Purpose

The Promotions tab exposes a single rich-text **Promo text area** field whose contents are stored in the provider configuration as `promo_html`. This is an arbitrary HTML block the merchant types or pastes — a DSK-branded banner, an interest-free explainer, or terms text — that renders on the storefront product page next to DSK's installment table. It is independent of the per-product promotion mappings: it is one block of HTML for the whole DSK BNPL provider, not a per-product field.

## Where to find it

Sidebar → **Payment Providers** → **DSK BNPL** → **Promotions** tab. The rich-text editor sits in a card **below** the promotions table, with its own **Save** button (separate from the per-row Add / Edit modal).

## What the merchant can do here

- Type or paste arbitrary HTML into the **Promo text area** rich-text editor.
- Save it with the card's own **Save** button, which posts to `POST /promotion/html/save` (under `/admin/api/payment_providers/dsk_bnpl/`).
- The saved content shows up on the storefront wherever the DSK BNPL theme template renders `{$provider.configuration.promo_html}`.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Promo text area** (rich-text editor, labelled "Promo text area") | Arbitrary HTML block stored in the provider configuration as `promo_html`. Saved via its own **Save** button (`POST /promotion/html/save`). Rendered on the storefront product page below / next to the DSK installment table. | Empty | No length limit enforced on the backend. The merchant can paste a DSK-branded banner, terms text, or any HTML. Note that the storefront theme must include the `promo_html` block for it to be visible. |

## Business rules

### Storefront rendering depends on the theme

The `promo_html` content is only visible on the storefront if the active theme's DSK BNPL template renders the `{$provider.configuration.promo_html}` placeholder. If a merchant saves promo HTML but doesn't see it on the product page, the theme template is missing the placeholder — the saved value is intact, it just isn't being output.

### Separate from the promotion rows

Saving the promo HTML is independent of the per-product promotion mappings. Editing the rich text and clicking its **Save** button updates only `promo_html`; it does not touch any promotion row. Conversely, adding / editing / deleting a promotion row does not affect `promo_html`. The two share the tab but are stored and saved separately — see [[dsk-bnpl-promo-mapping]] for the per-product rows.

### Plan-gating

This aspect inherits the same plan-gating as the parent DSK BNPL provider, which is **none** — every CloudCart plan can use it.

## Related

- [[payment-providers-dsk-bnpl-promotions]] — hub.
- [[payment-providers-dsk-bnpl]] — parent hub for DSK BNPL.
- [[payment-providers-fibank-bnpl-promotions]] — equivalent Promotions screen for the Fibank BNPL provider (same shape, different bank).
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

_None._
