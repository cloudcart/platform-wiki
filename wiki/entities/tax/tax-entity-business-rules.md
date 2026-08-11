---
type: entity
nav_path: "Entity → Tax / Fee → Business rules"
aliases: ["Tax business rules", "Tax constraints", "Tax export limitations", "No bulk tax import", "Tax address resolution setting"]
tags: [entity, taxes, fees, business-rules, constraints]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax]]. See the hub for the other aspects (attributes, VAT vs Fee, overrides, order snapshot, validation).

# Tax / Fee — business rules and constraints

## Identity

The catalogue of platform-level rules and constraints that govern how a Tax / Fee row behaves outside the form, the picker, the snapshot, and the external-VAT-validation flows. These are the rules merchants run into during onboarding, migration, or accounting integration that are not obvious from the [[settings-taxes]] UI alone.

## Aliases

- **Tax business rules** — umbrella term.
- **Tax constraints** — the platform limits.
- **No bulk tax import** — the most-asked migration constraint.

## Key Attributes — the business rules catalogue

### `invoicing_address` decides which address the engine reads

The `invoicing_address` setting on [[settings-cart]] (values: **BillingAddress** / **ShippingAddress**) decides which of the customer's addresses the tax engine reads for geo matching. Changing this can change which Tax rule applies — important for merchants serving multiple jurisdictions. A B2B merchant with billing in Germany and shipping in France will see DE VAT vs FR VAT depending on this single setting.

See [[tax-address-resolution]] for the full address-resolution rules.

### Settings cache flushed on save

Saving a Tax / Fee row flushes the platform Settings cache so the next checkout picks up the new rule immediately. No queue, no notifications, no webhooks from this screen — the change is visible on the very next checkout request.

### No bulk import

There is **no CSV import** for taxes / fees. The merchant creates them one at a time through the Add Tax / Add Fee form. For large migrations the only options are manual re-entry or asking CloudCart support to bulk-insert via direct DB writes. This is the single most-cited migration friction.

### No delete protection from existing orders

Deleting a Tax / Fee rule does NOT retroactively affect existing orders (because they hold a snapshot — see [[tax-entity-snapshot]]). The merchant can safely clean up old rules — but they should be careful not to delete a rule that's still needed for new orders, since deletion is immediate. There is no warning UI on delete.

### No dedicated tax-breakdown CSV export

There is no per-tax-line CSV endpoint for accountant-friendly tax breakdowns. The merchant can export Orders via [[orders-export]] (the tax breakdown appears as columns), but a per-tax-line CSV (one row per applied tax per Order) is **not** exposed. The workaround is to use the per-Order Invoice PDF / XML export via [[orders-invoice]].

### OSS threshold tracking is manual

OSS thresholds are **NOT auto-tracked** — the merchant must manually monitor their cross-border B2C revenue and flip the OSS toggle when they register. There is no dashboard module or notification for the €10,000 annual OSS threshold today. See [[tax-oss-semantics]] for the OSS runtime semantics.

### Per-zone VAT uniqueness

Only ONE VAT rule per [[geo-zone]] is allowed. Attempting to save a second VAT-type rule that points to the same `geo_zone_id` is rejected. Fees have no such uniqueness check — multiple Fees can target the same zone (each applies additively).

### Reverse-charge has no single toggle

There is no single *"Enable B2B reverse charge"* toggle on the entity. The merchant configures a zero-rate VAT rule and relies on VIES validation (see [[tax-entity-vat-validation]]). The `without_vat_reasons` text field is where the merchant types the legal wording printed on the invoice when reverse-charge applies.

### No `created_at` / `updated_at` on the parent row

The `taxes` row carries no timestamps — the model has `$timestamps = false`. For ordering / tie-breaking, the picker uses the underlying `geo_zone_id` value (highest wins). The `tax_overrides` table DOES carry timestamps.

### Validator quirks worth knowing

- **Percent rate cap at 90** (NOT 100). The validator rejects `100%` with the *"rate must be at least"* / max-value error. The 90 cap exists to prevent typo-induced runaway VAT.
- **Negative rates rejected** with the *"rate must be at least"* error.
- **Flat rate "max" is a string-length cap** — not a numeric ceiling. A flat amount of `9999999999` is rejected for length, not for being too large.
- **`name` max 100 chars.**
- **`without_vat_reasons` / `without_vat_reasons_non_eu` each max 64,000 chars.**

### Flat-amount Fees need currency conversion

A `flat`-type Fee carries a single rate value, which is interpreted as the store's **base currency**. When an order is placed in a non-base currency, the platform converts the flat amount through [[multi-currency]]. `percent`-type rules are currency-independent.

### Settings cache key is store-wide

The flush on save affects the whole store's Settings cache, not just the tax slice. This is intentional — the next checkout request reads a fresh cache regardless of which setting changed.

### No webhooks, no notifications

The Tax / Fee screen does not fire any webhooks (no `tax.created` / `tax.updated` events). The merchant integrating an accounting system via [[settings-hooks]] must poll the [[settings-taxes]] read endpoint to detect changes. No email notifications either — silent save.

### Older invented terms to avoid

A few terms appear in legacy support tickets but are NOT real:

- *"yes / no / specific"* for the `shipping` field — there is **no `specific` value**. Only `yes` and `no`.
- *"per-category beats per-region beats base"* — understated; the real ladder is in [[tax-entity-overrides]].
- *"`vat` toggle on the form"* — not a user-toggleable field; locked from the Add modal pick.

## Where it appears

- [[settings-taxes]] — the form whose validators enforce these rules.
- [[settings-cart]] — `invoicing_address`, `checkout_validate_company_vat`.
- [[orders-export]] — the order export that approximates a tax-breakdown CSV.
- [[orders-invoice]] — the per-order PDF / XML invoice export.
- [[tax]] — entity hub.

## Related

- [[tax]] — hub.
- [[tax-entity-attributes]] — the field-level validators.
- [[tax-entity-snapshot]] — why deletion does not retroactively affect orders.
- [[tax-entity-vat-validation]] — reverse-charge mechanics.
- [[tax-oss-semantics]] — OSS threshold tracking.
- [[tax-address-resolution]] — billing vs shipping address pick.
- [[multi-currency]] — flat-amount Fee conversion.
- [[settings-cart]] — `invoicing_address` + `checkout_validate_company_vat`.
- [[settings-hooks]] — webhook config (none fire from this screen).

## Open Questions

None.
