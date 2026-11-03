---
type: feature
nav_path: "Settings → Taxes and fees → Fees"
route_name: taxes.create
route_path: /admin/settings/taxes/fee/:id?
aliases: ["Fees", "Payment fee", "Shipping fee", "Surcharge", "Fee scoping", "Global vs target fee", "Fee stacking", "VAT on fee"]
tags: [settings, taxes, fees, payment, shipping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, overrides, pricing display, OSS / no-VAT, validation, integrations).

# Taxes and fees — Fees (`vat=no`)

## Purpose

How a **Fee** (`vat=no`) is configured and applied at checkout. Fees are extra charges added to the order subtotal based on the chosen payment and / or shipping method — e.g. a 2% surcharge for credit-card payments, a flat 3 EUR cash-on-delivery handling fee. Unlike VAT, **ALL matching fees stack additively** — every qualifying fee shows as its own line on the order total. Two common misconceptions: (a) you can target only **ONE** payment / shipping provider per fee row (no per-provider rate map), and (b) the `vat=no` flag does NOT mean *"VAT-free fee"*.

## Where to find it

Settings → Taxes and fees → **+ Add new → Add Fee**, OR click any existing row whose type badge says **Fee**. Form route: `/admin/settings/taxes/fee/:id?`.

## What the merchant can do here

In the Fee form:

- Set **Name** + **Rate** (`tax`) — percent or flat. Same UI as a Tax.
- Choose **target scope** (`target`): `restofworld` (global) or `regions` (specific geo zone from [[settings-geo-zones]]).
- Toggle **Payment activation** (`payment_active`): `global` (every payment method) OR `target` (only the chosen single payment provider).
- When `payment_active = target`: pick the **single Payment provider** from a searchable dropdown (placeholder *"Select payment method"*; no *"Setup payment methods"* button here).
- Toggle **Shipping activation** (`shipping_active`): `global` or `target`.
- When `shipping_active = target`: pick the **single Shipping provider** from a searchable dropdown — this section DOES have a **"Setup shipping methods"** button navigating to [[shipping]].

A fee can have BOTH payment and shipping activation at once — when both are `target`, the fee applies only when the customer picked exactly that payment provider **AND** exactly that shipping provider. It is silently skipped when only one matches.

## Settings & fields

Fee-specific fields (the rest are shared with taxes — see the [[settings-taxes]] hub):

| Field | Value | Notes |
|-------|-------|-------|
| `vat` | `no` | Auto-set from the "Add Fee" type card; **NOT user-toggleable** after create. |
| `payment_active` | `global` \| `target` | Form-only switch — drives the `payment_provider` required-when rule. NULLs `payment_provider` on save when `global`. |
| `payment_provider` | single provider key | Required when `payment_active=target`. Error: *"You have not specified a payment method for which the fee will apply"*. |
| `shipping_active` | `global` \| `target` | Same shape, for shipping. |
| `shipping_provider` | single provider key | Required when `shipping_active=target`. Error: *"You have not selected a shipping method for which the fee will apply"*. |

On save, two shared fields are **hard-overridden** regardless of submitted value:

- `price_with_vat` → forced to `0` (a fee cannot be configured in *"prices include VAT"* mode).
- `shipping` → forced to `no` (a fee cannot itself include shipping in its base).

See [[settings-taxes-pricing-display]] for what these flags would otherwise mean.

## Business rules

### Fees stack additively

While VAT picks a single winner (see [[settings-taxes-vat-rules]]), **ALL matching fees apply additively**. Three fees that all match an order are all charged — each as a separate line on the order total. The platform does NOT pick "the most specific" or "the most recent" fee; every qualifying fee fires.

### ONE provider per fee — `_values` is NOT a per-provider rate map

The `payment_provider_values` / `shipping_provider_values` fields are **NOT** per-provider rate-override maps. The platform stores **ONE** provider and **ONE** rate per fee row. The `_values` fields are only display-name lookups (`{provider_key: title}`) so the admin UI can show the provider's friendly name (e.g. *"Visa / Mastercard"*) next to the key — they carry no per-provider rate variations.

To charge different rates on different payment methods, create **multiple separate fee rows** — one per provider, each with its own rate. Same for shipping methods.

### The `vat` flag on a fee does NOT control whether VAT is applied to the fee

What the `vat` flag actually does:

- **`vat=yes`** — the rule is a VAT rate rule for the region. Picked via the single-winner precedence in [[settings-taxes-vat-rules]].
- **`vat=no`** — the rule is a fee (additional charge). All matching `vat=no` rules stack.

**VAT-on-fee behaviour is NOT controlled by the fee's own `vat` flag.** When the order has an active VAT rule (any `vat=yes` rule matching the customer's region), the platform **always** computes a VAT contribution from every applicable fee — whether the fee was saved with `vat=yes` or `vat=no`. Only HOW the VAT is computed differs, driven by the store-wide *"prices include VAT"* setting on the winning VAT rule:

| Store's *"prices include VAT"* | What happens to a fee at checkout |
|---|---|
| **YES** (prices include VAT) | The entered fee amount is treated as VAT-inclusive. The platform extracts the embedded VAT portion and adds it to the order's VAT line. The invoice shows the fee at its full configured value, with that VAT broken out in the VAT total. |
| **NO** (prices exclude VAT) | The entered fee amount is treated as net (pre-VAT). The platform calculates VAT on top of the fee and adds it to the order's VAT line. The invoice shows the fee at its configured value plus a separate VAT line that includes the fee's contribution. |

The only way to suppress VAT on a fee is to make the **whole order** VAT-exempt — the customer enters a valid EU VAT number that triggers the B2B reverse-charge flow (the *"Without VAT reasons"* path, see [[settings-taxes-oss-no-vat]]). Then the customer pays the fee net of VAT and the invoice prints the reverse-charge wording.

**There is NO per-fee toggle** for *"don't apply VAT on this specific fee"*. Merchants wanting a VAT-free fee for VAT-paying customers cannot configure it here — they must bake the desired total into the product price or use a Cart Rule instead ([[apps-cart-rules]]). A merchant who set `vat=no` expecting *"VAT-free fee"* has actually been carrying VAT on the fee all along (the VAT line is one combined total, not per-fee, so it goes unnoticed).

### Geo-zone scoping for fees works the same as for VAT

Fees support `target=regions` and `target=restofworld` like Taxes do, and obey the same country-level-only matching rule (see [[settings-taxes-vat-rules]] — *"Country-level matching only"*). Unlike VAT, there is **no** `unique_geozone` validator for fees — the merchant CAN have many fees on the same zone, and all matching fees stack.

## Related

- [[settings-taxes]] — hub.
- [[settings-taxes-vat-rules]] — single-winner VAT precedence (the contrast to fee stacking).
- [[settings-taxes-pricing-display]] — `price_with_vat` is forced to `0` for fees; explains what that field would otherwise do.
- [[settings-payment-providers]] — provider keys selectable in `payment_provider`.
- [[shipping]] — provider keys selectable in `shipping_provider`; the *"Setup shipping methods"* CTA navigates here.
- [[apps-cart-rules]] — alternative path for conditional surcharges when fee semantics don't fit.
- [[checkout-flow]] — when fees are computed and added.

## Open questions

None.
