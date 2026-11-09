---
type: feature
nav_path: "Settings → Taxes and fees → Pricing display (inclusive vs exclusive)"
route_name: taxes.create
route_path: /admin/settings/taxes/tax/:id?
aliases: ["Price with VAT", "VAT inclusive", "VAT exclusive", "Inclusive pricing", "Exclusive pricing", "Storefront VAT label", "Shipping VAT inclusion", "VAT reverse-compute formula"]
tags: [settings, taxes, vat, pricing, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, fees, overrides, OSS / no-VAT, validation, integrations).

# Taxes and fees — pricing display (inclusive vs exclusive)

## Purpose

Documents the two flags on a VAT rule that decide how prices are shown on the storefront and how the tax-totals math runs at checkout: `price_with_vat` (are the merchant's entered prices VAT-inclusive or VAT-exclusive?) and `shipping` (stored, but it does not decide VAT on shipping). Pricing display is the single biggest source of merchant confusion in CloudCart's tax setup — EU stores typically use inclusive pricing (`price_with_vat=1`) while B2B / US stores typically use exclusive pricing (`price_with_vat=0`).

## Where to find it

Inside the Tax edit form (`type=tax`):

- **`price_with_vat`** — *"Prices include VAT"* checkbox / switch.
- **`shipping`** — a stored yes/no value; VAT on shipping is decided as described under Business rules.

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
| `shipping` | `yes` / `no` only | Stored on a VAT rule but not read by the totals: it neither decides VAT on the shipping line nor moves the VAT between stages (see Business rules). Forced to `no` for fees on save. |

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

### The VAT line in the totals ("С включен ДДС")

The VAT line in the cart, checkout and order totals carries the VAT rule's own name:

- **Inclusive (`price_with_vat=1`):** it reads *"С включен"* + the rule's name (EN *"Including"*), e.g. *"С включен ДДС"* for a rule named *ДДС*, with the rate. The amount is the VAT already contained in the prices (goods, VAT-bearing fees and taxed shipping, after discounts). It is shown for information and **not added** to the total.
- **Exclusive (`price_with_vat=0`):** the plain rule name; the amount **is added** to the total.
- **VAT not due** for the customer (see the table above): the amount is 0.

### VAT on the shipping line

The `shipping` value on a VAT rule plays no part. All VAT is worked out after shipping, and the shipping line carries VAT only when all of these hold:

- a VAT rule matches the order's address;
- **the store charges the shipping** (the sender pays): not when the receiver pays the courier directly. Free shipping, a payment method set to make the seller pay, or any wallet amount make the sender pay;
- the courier integration supports it (DHL and DHL Express never put VAT on shipping).

When the **receiver pays**, the shipping line stays on the order and in its total, but carries no VAT, is left off the invoice and receipt, is not part of the cash-on-delivery amount ([[shipping-provider-mech-cod]]) and counts as 0 in Analytics ([[analytics-total-sales-details]]).

**Is the shipping price gross or net?** When the VAT rule's prices include VAT, the shipping price (the courier's live price or the merchant's own rate) is taken as VAT-inclusive and the VAT is extracted from it. When prices exclude VAT, only the plain courier price model (**calculator**) is taken as net, with VAT added on top; every other model, the courier price plus a fixed fee included, is still taken as VAT-inclusive (verify). With prices including VAT and a customer not charged VAT, the VAT is taken off the shipping price. Whether a courier's own price already contains the courier's VAT is the courier's matter.

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
