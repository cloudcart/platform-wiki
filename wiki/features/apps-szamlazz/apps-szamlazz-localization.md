---
type: feature
nav_path: "Apps → Szamlazz → Settings (language, template, currency, tax)"
route_name: apps.szamlazz.overview
route_path: /admin/apps/szamlazz
aliases: ["Szamlazz language", "Szamlazz template", "Szamlazz currency", "Szamlazz multi-currency", "Szamlazz taxpayer status", "Szamlazz NAV lookup", "Szamlazz EU VAT", "Szamlazz per-store account"]
tags: [apps, erp, invoicing, hungary, accounting]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-szamlazz]]. See the hub for the other aspects (settings, per-order invoice / credit-note / receipt flows, document mechanics, automation).

# Szamlazz — language, template, currency & tax classification

## Purpose

This aspect documents how a Szamlazz document is **formatted and classified**: which currencies are supported, the invoice language choice, the PDF template options, the NAV-based taxpayer classification that drives EU-VAT handling, and the per-store account model. These are the "how does the document look and which VAT rule applies" settings, as opposed to the issuance mechanics ([[apps-szamlazz-operations]]) or the automation engine ([[apps-szamlazz-automation]]).

## Where to find it

Language, template, and the extra-logo upload live on the Settings tab (Sidebar → **Apps** → **Szamlazz** → Settings — see [[apps-szamlazz-settings]]). Currency and taxpayer classification are not merchant-picked here — they are derived per order at invoice-creation time (below).

## What the merchant can do here

- Pick **one** default invoice language for all outgoing documents.
- Pick one of **five** PDF layout templates and optionally upload an extra logo.
- Issue invoices in whatever currency the order is in (currency is taken from the order, not chosen in the integration).
- Rely on automatic NAV validation of B2B buyers' Hungarian tax numbers, which sets the correct EU-VAT treatment.

## Settings & fields

### Invoice language (one global value — 8 options)

The merchant picks a single default invoice language that applies to **all** outgoing documents. The 8 values the platform exposes are:

`hu` (Hungarian), `en` (English), `de` (German), `it` (Italian), `fr` (French), `ro` (Romanian), `sk` (Slovak), `hr` (Croatian).

Szamlazz itself supports more languages (12 total, adding `es` Spanish, `cz` Czech, `pl` Polish), but only the 8 above are selectable in CloudCart.

**The invoice language is global — not per-customer or per-order.** Every customer receives invoices in the same language. A merchant with multilingual customers cannot auto-localize per buyer; a different-language invoice must be requested manually.

### Invoice template (5 layout variants)

| Template | Layout |
|---|---|
| `DEFAULT` | Szamlazz's standard template. |
| `TRADITIONAL` | Traditional layout. Also the fallback when a saved template name doesn't match a known value. |
| `ENV_FRIENDLY` | Environmentally-friendly compact format. |
| `8CM` | Narrow / receipt-printer width. |
| `RETRO` | Retro / vintage styling. |

An `extra_logo` (uploaded image) can be set to overlay on the invoice header.

### Currency (taken from the order)

The platform passes the order's currency straight to Szamlazz — the merchant does not pick a currency in the integration. Szamlazz accepts a wide list of currency codes, including HUF (Ft), EUR, CHF, USD, AED, AUD, BGN, BRL, CAD, CNY, CZK, DKK, GBP, HKD, ILS, INR, ISK, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, RSD, RUB, SEK and others. HU-based merchants typically invoice in HUF, but cross-currency works when the Szamlazz account allows it.

## Business rules

### Taxpayer-status classification (NAV lookup at invoice time)

For B2B buyers, the platform classifies the buyer's VAT identifier into one of these categories, set **only at invoice-creation time** (not at cart validation):

- `TAXPAYER_NO_TAXNUMBER` — no VAT number provided.
- `TAXPAYER_HAS_TAXNUMBER` — matches the Hungarian format (`\d{8}-\d{1}-\d{2}`); validated against NAV (the Hungarian tax authority).
- `TAXPAYER_EU_ENTERPRISE` — matches a generic EU VAT format (e.g. `BG206004146`, `DE123456789`); treated as EU intra-Community / reverse-charge.
- `TAXPAYER_NON_EU_ENTERPRISE` — anything else (non-EU).
- `TAXPAYER_WE_DONT_KNOW` — Hungarian-format number whose NAV lookup failed (network / API error).

The EU vs non-EU classification drives the **EU-VAT flag** on the invoice — important for correct cross-border VAT. Because the lookup runs at invoice creation, a buyer who corrects their tax number after the invoice is issued needs a re-issued document, not just a profile edit.

### Per-store Szamlazz account

Each CloudCart store has its own Szamlazz app instance with its own API key (apps are scoped per store). A merchant running multiple stores connects each store to its own Szamlazz account (or reuses one Szamlazz API key per store if Szamlazz permits it on their side). Credentials are entered on [[apps-szamlazz-settings]].

## Related

- [[apps-szamlazz]] — hub.
- [[apps-szamlazz-settings]] — where language, template, and the extra logo are configured.
- [[apps-szamlazz-operations]] — what issuance records on the order (the document the language / template / currency apply to).
- [[orders-invoice]] — generic per-order invoice flow.
- [[order]] — entity page; carries the buyer's tax number and the order currency.

## Open questions

(none — resolved against backend)
