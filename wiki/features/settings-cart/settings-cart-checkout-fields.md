---
type: feature
nav_path: "Settings → Cart and checkout → Checkout fields"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Checkout fields visibility", "Required checkout fields", "Hide billing address", "VIES VAT validation", "Company VAT field", "BULSTAT field", "MOL field", "post_code_not_required", "checkout_hide_first_name", "checkout_hide_last_name", "checkout_hide_phone", "checkout_hide_billing_address", "checkout_require_billing_address", "invoicing_address", "checkout_validate_company_vat"]
tags: [settings, cart, checkout, fields, address, vat, b2b]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, payment/shipping defaults, limits, UI behavior, Google Maps, marketing consent).

# Cart and checkout — Checkout fields

## Purpose

Two boxes on the Cart and checkout page that together control **which checkout fields are required, optional, or hidden** for both private and B2B customers. Specifically: per-field visibility for first name, last name, phone, state, street, apartment, postal code; the "don't ask for billing address at all" toggle plus the conditional "require billing address" follow-up; the rule that decides whether fees/taxes are computed from billing or shipping address; the company-info fields (name, VAT, BULSTAT, MOL); and the EU VIES VAT validation switch that blocks orders with invalid company VAT numbers.

## Where to find it

Sidebar → Settings → **Cart and checkout** → boxes **Additional fields settings** (`process_orders`, titled "Abandoned cart reminder" in the underlying code identifier — that's a known mis-naming, the header label rendered to the merchant reads "Additional fields settings") and **Company info** (`company_info`).

## What the merchant can do here

- For each standard checkout field, choose **required** / **shown but optional** / **hidden**.
- Toggle "don't ask for billing address at all" — the billing-address-required dropdown then disappears.
- Decide whether fees and taxes use the **billing** or the **shipping** address (`invoicing_address`).
- Toggle whether postal/zip code is required (switch is inverted in code: `post_code_not_required` ON = required).
- Configure the four company-info fields (name, VAT, BULSTAT, MOL) per the same required/optional/hidden choices.
- Enable EU VIES VAT validation for company orders — blocks order placement if VIES rejects the VAT.

## Settings & fields

### Box: Additional fields settings (`process_orders`)

Header label rendered: *"Additional fields settings"*.

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Don't ask for billing address** (`checkout_hide_billing_address`) | When ON, hides the billing address step entirely from checkout. | |
| **Require billing address on checkout** (`checkout_require_billing_address`) | `Required` / `Not required` toggle. | Visible only when "Don't ask for billing address" is OFF (dependField rule). |
| **Application of fees and taxes according to** (`invoicing_address`) | Whether to compute fees and taxes based on the billing address or the shipping address. | Two options: `BillingAddress` / `ShippingAddress`. |
| **First name** (`checkout_hide_first_name`) | Field visibility: required / shown but optional / hidden. | Options come from a shared `fieldOptions` helper. |
| **Last name** (`checkout_hide_last_name`) | Same. | |
| **Phone** (`checkout_hide_phone`) | Same. | |
| **State** (`checkout_hide_state_name`) | Same. | Uses a slightly different "fieldless" option set (only show/hide, no required). |
| **Street name** (`checkout_hide_street_name`) | Same. | |
| **Street number** (`checkout_hide_street_number`) | Same. | |
| **Additional information: Apt, suite, etc.** (`checkout_hide_additional_information`) | Same. | |
| **Require postal/zip code at checkout** (`post_code_not_required`) | Switch with inverted semantics — when the switch is ON, the underlying setting is `false` (i.e., postal code IS required). | Code: `trueValue: false, falseValue: true`. |

### Box: Company info (`company_info`)

For B2B / VAT-registered orders.

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Company name** (`checkout_hide_company_name`) | Required / shown / hidden. | |
| **Company VAT or EIN** (`checkout_hide_company_vat`) | Same. | |
| **Company registration number** (`checkout_hide_company_bulstat`) | Same. The setting key uses Bulgaria's "BULSTAT" naming but the field label is generic. | |
| **Company owner** (`checkout_hide_company_mol`) | Same. The setting key uses Bulgaria's "MOL" abbreviation. | |
| **Validate VAT number from VIES service** (`checkout_validate_company_vat`) | When ON, the entered company VAT is checked against the EU VIES web service at order time. | Validation failure blocks the order. |

## Business rules

### `post_code_not_required` is inverted

The Vue field config uses `trueValue: false, falseValue: true` for this switch — meaning the UI's "ON" position stores literal `false` in settings (postal code IS required). Practical merchant-facing wording is positive (*"Require postal/zip code at checkout"*) but storage is the opposite. A support agent looking at a raw API dump should mentally invert this key. See the hub [[settings-cart]] for the cross-cutting list of inverted switches.

### `checkout_hide_billing_address` hides the dependent dropdown

When **Don't ask for billing address** is ON, the **Require billing address on checkout** dropdown is hidden via dependField rule (parent value `false` or `0`). The backend won't enforce consistency — see the hub [[settings-cart]] for the general "dependFields are cosmetic" rule.

### `invoicing_address` decides which address drives fees/taxes

The toggle picks one of `BillingAddress` / `ShippingAddress`. Affects: shipping-fee computation (zone-based pricing reads from this address), tax rate selection (region/VAT computation reads from this address), and invoice content. If the merchant hides the billing-address step entirely (`checkout_hide_billing_address = ON`), the platform falls back to the shipping address regardless of this setting. See [[settings-invoicing]] for the invoice-side implications.

### EU VIES validation blocks order placement on failure

When `checkout_validate_company_vat = yes`, the entered company VAT is called against the EU VIES web service at order time. **Validation failure blocks the order** — the customer sees an inline error and cannot complete checkout until a valid VAT is entered (or the merchant turns this off). The check only runs when a company VAT is provided; private orders without a VAT number are unaffected.

VIES service availability is outside CloudCart's control — VIES outages can spuriously block orders. The merchant should consider this when enabling validation.

### BULSTAT and MOL keys reflect Bulgarian origin

The setting keys `checkout_hide_company_bulstat` and `checkout_hide_company_mol` use Bulgarian terminology:

- **BULSTAT** is the Bulgarian unified company registration code (now called EIK).
- **MOL** is the Bulgarian abbreviation for "Material Liability Person" (the company representative).

The **field labels** rendered to the merchant are generic ("Company registration number" and "Company owner") so non-Bulgarian merchants see neutral wording, but the underlying keys remain BG-named. This is purely internal naming; merchants in any country can use these fields for the equivalent local concepts.

### State field uses a different option set

The `checkout_hide_state_name` field uses a "fieldless" option set with only **show** / **hide** options — no "required but optional" choice. This is by design: the state field is either available for the customer to fill or completely hidden; there's no "shown but optional" middle ground.

### "Don't ask for billing address" + `invoicing_address` interaction

When billing address is hidden entirely, fee/tax computation falls back to the shipping address (the only one collected), invoices use the shipping address as the billing party (see [[settings-invoicing]]), and the `invoicing_address` setting has no practical effect. For B2B-friendly stores that need invoices with separate billing party, leave `checkout_hide_billing_address` OFF and configure the billing fields to be **required**.

### Field visibility doesn't affect data already collected

Switching from "shown" to "hidden" only affects future checkouts — existing orders keep their data, still visible in order details.

## Related

- [[settings-cart]] — hub.
- [[settings-cart-accounts-registration]] — sibling aspect; the `require_registration_*_address` switches push the same address-collection step earlier into the registration flow.
- [[settings-invoicing]] — `invoicing_address` (BillingAddress vs ShippingAddress) also affects how invoices compute totals.
- [[settings-taxes]] — the tax-rate selection logic that reads the chosen invoicing address.
- [[shipping]] — shipping-fee computation that reads the chosen invoicing address.
- [[order]] — the order entity that stores the collected address fields.
- [[customer]] — the customer entity with the same address fields.
- [[checkout-flow]] — end-to-end checkout sequence concept page.

## Open questions

_None._
