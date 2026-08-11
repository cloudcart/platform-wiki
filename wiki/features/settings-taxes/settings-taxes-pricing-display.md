---
type: feature
nav_path: "Settings → Taxes and fees → Pricing display (inclusive vs exclusive)"
route_name: taxes.create
route_path: /admin/settings/taxes/tax/:id?
aliases: ["Price with VAT", "VAT inclusive", "VAT exclusive", "Inclusive pricing", "Exclusive pricing", "Storefront VAT label", "Shipping VAT inclusion", "VAT reverse-compute formula"]
tags: [settings, taxes, vat, pricing, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, fees, overrides, OSS / no-VAT, validation, integrations).

# Taxes and fees — pricing display (inclusive vs exclusive)

## Purpose

Documents the two flags on a VAT rule that decide how prices are shown on the storefront and how the tax-totals math runs at checkout: `price_with_vat` (are the merchant's entered prices VAT-inclusive or VAT-exclusive?) and `shipping` (does this VAT apply to shipping too?). Pricing display is the single biggest source of merchant confusion in CloudCart's tax setup — EU stores typically use inclusive pricing (`price_with_vat=1`) while B2B / US stores typically use exclusive pricing (`price_with_vat=0`).

## Where to find it

Inside the Tax edit form (`type=tax`):

- **`price_with_vat`** — *"Prices include VAT"* checkbox / switch.
- **`shipping`** — flag controlling whether the tax also applies to shipping cost.

Route: `/admin/settings/taxes/tax/:id?`.

## What the merchant can do here

Toggle the two flags. Both are only meaningful for `vat=yes` rules — for fees they are **hard-overridden** on save:

- `price_with_vat` → forced to `0` for fees.
- `shipping` → forced to `no` for fees.

See [[settings-taxes-fees]] for the fee-side hard-override behaviour.

## Settings & fields

| Field | Value | Notes |
|-------|-------|-------|
| `price_with_vat` | `1` (inclusive) / `0` (exclusive) | Only meaningful for `vat=yes`. Forced to `0` for fees on save. |
| `shipping` | `yes` / `no` only | Enum is binary (no *"specific"* value — older wiki was wrong). Controls bucketing in the totals pipeline (`tax.before` vs `tax.after`), NOT whether VAT applies to the shipping line itself. Forced to `no` for fees on save. |

## Business rules

### Inclusive vs exclusive — the two math modes

The two modes give the merchant a choice about which number is the "real" price:

- **Inclusive (`price_with_vat=1`)** — prices on the storefront ARE VAT-inclusive (typical for EU consumers). The tax portion is computed **backwards** from the displayed price.
- **Exclusive (`price_with_vat=0`)** — prices on the storefront are net (VAT-exclusive). VAT is added on top at checkout (typical for B2B / US markets).

### VAT calculation depends on `price_with_vat` AND customer entitlement

The engine combines `price_with_vat` with the customer's `isWithVat` flag (set on the billing address) to pick which math runs:

| `price_with_vat` | Customer is "with VAT" | Result |
|---|---|---|
| `1` (inclusive) | Yes | **Reverse-compute** — `vat = price − price / (rate/10000 + 1)`. The customer sees the inclusive price; the VAT line on the invoice shows the extracted portion. |
| `1` (inclusive) | No (B2B intra-community supply, etc.) | VAT amount = 0 — the engine treats the line as net (the inclusive price stays as-is but the VAT contribution drops to zero). |
| `0` (exclusive) | Yes | **Add on top** — `vat = price × (rate/10000)`. The customer sees the net price plus a separate VAT line. |
| `0` (exclusive) | No | VAT amount = 0 — exclusive price already represents the net, customer pays net. |

The customer's `isWithVat` flag comes from the billing address — it's flipped via the EU VAT number flow at checkout. See [[settings-taxes-oss-no-vat]] for the *"Without VAT reasons"* text printed on the invoice in these cases.

### Storefront product label

Storefront product labels prefix the tax name with **"VAT included"** when both `is_vat=true` AND `price_with_vat=1`; otherwise the line is shown after totals with a plain **"VAT"** label.

### `shipping` flag buckets VAT into `tax.before` vs `tax.after`

The `shipping` flag does **NOT** directly say *"VAT is charged on the shipping line"*. What it actually does is decide which bucket the VAT contribution lands in during the cart-totals pipeline:

- `shipping=yes` → VAT contribution from the order goes into `tax.before` (calculated before the shipping line is added).
- `shipping=no` → VAT contribution goes into `tax.after` (calculated on the post-shipping subtotal).

The practical effect is what the merchant intuitively wants — a VAT rule with `shipping=yes` will result in VAT being charged on the shipping line too. But the storage flag is binary and the bucketing is plumbing — not a per-line *"apply VAT to shipping"* toggle.

### Rate precision — stored ×100 internally

Internally the platform stores `tax` as an integer scaled ×100 (e.g., a 20% rate is stored as `200000` and a 9% rate as `90000`); divisions by `10000` appear throughout the calculation code. Merchants see and enter the human-readable value (`20.00`); the conversion is automatic on save.

Practical implication: there are **2 decimal places of precision** on tax rates — `20.005%` would be rounded to `20.01%` on save. See [[settings-taxes-validation]] for the rate-cap details.

### Inclusive pricing typically pairs with `vat=yes`

The `price_with_vat` flag is only meaningful for `vat=yes` rules. The save layer forces it to `0` on `vat=no` (fee) rows — so merchants cannot configure a fee in *"prices include VAT"* mode. The VAT-on-fee behaviour is driven instead by the **winning VAT rule's** `price_with_vat` value — see [[settings-taxes-fees]] for the full *"how does VAT apply to a fee"* explanation.

## Related

- [[settings-taxes]] — hub.
- [[settings-taxes-vat-rules]] — the rule whose `price_with_vat` drives this math.
- [[settings-taxes-fees]] — explains how the WINNING VAT's `price_with_vat` decides VAT-on-fee math (the fee's own flag is hard-overridden to `0`).
- [[settings-taxes-oss-no-vat]] — the *"without VAT"* customer path that zeros out VAT regardless of inclusive / exclusive mode.
- [[settings-cart]] — `invoicing_address` decides which address's `isWithVat` is checked.
- [[multi-currency]] — concept page on currency interaction with rate precision.
- [[tax-computation]] — concept page on the full checkout-time math.

## Open questions

None.
