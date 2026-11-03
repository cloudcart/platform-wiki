---
type: feature
nav_path: "Settings → Taxes and fees → OSS and 'without VAT' reasons"
route_name: taxes.create
route_path: /admin/settings/taxes/tax/:id?
aliases: ["OSS", "One Stop Shop", "EU VAT", "Cross-border B2C VAT", "Without VAT reasons", "VAT exemption text", "Reverse charge", "B2B VAT", "Intra-community supply"]
tags: [settings, taxes, vat, eu, oss, invoicing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, fees, overrides, pricing display, validation, integrations).

# Taxes and fees — OSS and "without VAT" reasons

## Purpose

Documents the EU-specific compliance fields on a VAT rule: the **OSS (One-Stop-Shop)** registration flag — which switches the platform's cross-border B2C VAT handling — and the two **"without VAT reasons"** free-text fields that print on invoices when an order qualifies for zero VAT (EU intra-community supply, non-EU export). These are the fields most merchants forget to configure until their first cross-border order surfaces the problem.

## Where to find it

Inside the Tax edit form (`type=tax`):

- **OSS flag (`oss_registration`)** — the **"One Stop Shop"** switch is visible **ONLY** when `type=tax` AND the *"Make the tax Global"* switch is OFF (i.e., the rule targets a regional zone).
- **`without_vat_reasons`** / **`without_vat_reasons_non_eu`** — two textarea fields on the form.

Route: `/admin/settings/taxes/tax/:id?`.

## What the merchant can do here

### Toggle OSS registration

Flip the switch to indicate the store is EU OSS-registered. When ON, the platform uses the **destination country's** VAT rate for cross-border B2C sales within the EU. When OFF (or not set), the merchant's home-country VAT (the store's `operation_country` from [[settings-general]]) is used as the default.

### Author the no-VAT reason text

Two textareas hold the merchant-customisable text printed on invoices when VAT is **not** charged. These appear on the invoice template (see [[settings-invoicing]]). Empty values fall back to a platform default:

- **`without_vat_reasons`** — shown on invoices for EU customers (typically intra-community supply rules — B2B with a valid EU VAT number).
- **`without_vat_reasons_non_eu`** — shown on invoices for non-EU customers (export rules).

## Settings & fields

| Field | Constraint | Notes |
|-------|------------|-------|
| `oss_registration` | nullable | **Presence-based**: stored `true` when the request includes the field at all, `false` when omitted. Not a numeric value. Tax-only. |
| `without_vat_reasons` | optional, **max 64,000 characters** | Free-text rendered on the invoice when an EU order qualifies for zero VAT. The 64K cap is effectively unbounded for normal use. |
| `without_vat_reasons_non_eu` | optional, **max 64,000 characters** | Same, for non-EU exports. |

## Business rules

### OSS — when it fires

When `oss_registration=1`, the platform applies the EU OSS rules: for B2C cross-border sales within the EU, the **destination country's** VAT rate is used. Without OSS registration, the merchant's home country VAT is used by default.

The OSS rules also drive which *"without VAT reasons"* text is printed on the invoice when an order qualifies for zero VAT (e.g., export outside EU, or B2B reverse-charge inside the EU).

### Customer "without VAT" flag — the trigger for the reasons text

The customer becomes "without VAT" (`isWithVat` returns false on the billing address) in two main scenarios:

1. **EU B2B with valid VAT number** — customer entered a VAT number at checkout that validated against VIES. The order goes through the reverse-charge flow, the EU-side `without_vat_reasons` text prints on the invoice.
2. **Non-EU customer** — billing address falls outside the EU. The `without_vat_reasons_non_eu` text prints on the invoice.

In both scenarios, the cart-totals engine sets VAT amount = 0 on the order (regardless of inclusive / exclusive pricing — see [[settings-taxes-pricing-display]]) and the chosen reasons text appears as a footer or annotation on the customer's invoice (the exact placement is controlled by [[settings-invoicing]]).

### VAT-on-fee suppression — only via the customer's VAT-exempt flag

This is the **only** path that suppresses VAT on a fee. Setting `vat=no` on a fee row does **NOT** make the fee VAT-free — see [[settings-taxes-fees]] for the full clarification. When the customer is "without VAT" via one of the two scenarios above, the customer pays the fee net of VAT and the invoice prints the reverse-charge wording.

### Empty no-VAT reasons fall back to a platform default

If the merchant leaves `without_vat_reasons` or `without_vat_reasons_non_eu` empty, the invoice still prints a default reason string (the platform's own boilerplate) — but merchants subject to accounting audits typically need their **own** wording, so the practical recommendation is to fill these in once during store setup and never touch them again.

### Default jurisdiction when OSS is off — `operation_country`

When OSS is OFF and the platform needs a default VAT jurisdiction (e.g., for a customer whose billing address didn't match any regional zone), it falls back to the merchant's `operation_country` setting from [[settings-general]]. This is the *"home country"* of the store and decides which VAT rate the platform applies as the fallback.

## Related

- [[settings-taxes]] — hub.
- [[settings-taxes-vat-rules]] — the OSS switch is only visible when the VAT rule targets a regional zone.
- [[settings-taxes-pricing-display]] — when `isWithVat` is false, VAT zero-out is the same regardless of inclusive / exclusive mode.
- [[settings-taxes-fees]] — fees inherit the customer's VAT-exempt status as the ONLY path to a VAT-free fee.
- [[settings-invoicing]] — invoice template; renders the chosen `without_vat_reasons` text.
- [[settings-general]] — `operation_country` is the default jurisdiction when OSS is off.
- [[checkout-flow]] — the EU VAT number entry step that flips `isWithVat`.

## Open questions

None.
