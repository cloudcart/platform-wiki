---
type: entity
nav_path: "Entity → Tax / Fee → Attributes"
aliases: ["Tax fields", "Fee fields", "Tax / Fee attributes", "Tax form fields", "Tax rate fields"]
tags: [entity, taxes, fees, vat, attributes, fields]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax]]. See the hub for the other aspects (VAT-vs-Fee discrimination, overrides, order snapshot, validation, business rules).

# Tax / Fee — attributes

## Identity

The full attribute catalogue for a single Tax / Fee row on [[settings-taxes]]. The two sub-types (Tax vs Fee) share one form, but the visible / required fields differ — the table below marks which apply to which.

## Aliases

- **Tax fields** / **Fee fields** — the labels on the Add / Edit form.
- **Tax form fields** — the form variant for Tax (no Percent/Flat radio).
- **Fee form fields** — the form variant for Fee (Percent/Flat radio at top).

## Key Attributes

| Attribute | Applies to | What the merchant controls | Notes |
|-----------|-----------|----------------------------|-------|
| **Name** (`name`) | Tax + Fee | Free text on the form | Required, **max 100 chars**. Shown on the management list and on each printed invoice line. |
| **Rate value** (`tax`) | Tax + Fee | Numeric input | Required. For percent type the validator caps at **90** (NOT 100 — the common merchant assumption is wrong); negative rates are rejected with the *"rate must be at least"* error. For flat type the "max" is a string-length cap, not a numeric ceiling. |
| **Rate type** (`type`) | Fee only (Tax form has no radio) | enum `percent` / `flat` | The Tax form is percent-only (defaulted to `percent`, no toggle). Fees show the radio at the top. A `percent` rate is currency-independent; a `flat` rate is converted through [[multi-currency]] for non-base-currency orders. |
| **Entity type** (Tax vs Fee) | Both | Picked in the Add modal (Add Tax / Add Fee) — **locked after create** | Determines which fields apply and which runtime semantics fire (single-winner VAT vs additive Fee — see [[tax-entity-vat-vs-fee]]). Cannot be changed by editing; delete and re-create instead. |
| **Target scope** (`target`) | Tax + Fee | Dropdown: `restofworld` or `regions` | `restofworld` is the fallback matching any address not caught by a regional rule. `regions` ties the rule to one [[geo-zone]]. **`geo_zone_id` is REQUIRED when target = regions** and must point to an existing zone. |
| **Geo zone** (`geo_zone_id`) | Tax + Fee | Picker visible only when target = `regions` | One of the merchant's [[geo-zone|geo zones]] from [[settings-geo-zones]]. **For VAT** matching looks ONLY at country rules — city / region / polygon / distance / post-code rules are ignored. **For Fees** the full geo-zone scope is honoured (all 11 zone-value operations). **Uniqueness:** only ONE VAT rule per zone; fees have no such check. |
| **VAT flag** (`vat`) | Both — **NOT user-toggleable** | Auto-set on create from the Add Tax / Add Fee pick; preserved on update | Discriminates rule TYPE — **NOT** whether the rule's own amount is VAT-taxable. `vat = yes` → a VAT rate rule; `vat = no` → a Fee. The type-picker choice becomes `vat` and is locked; any value the form submits is overwritten. See [[tax-entity-vat-vs-fee]]. |
| **Price includes VAT** (`price_with_vat`) | Tax only | Toggle on the Tax form (`tax_prices`) | `1` = entered product prices ALREADY include VAT (GROSS, typical EU consumer pricing); `0` = NET (typical US / B2B, VAT added at checkout). Per-rule, not store-wide. **FORCED to `0` for fees.** See [[tax-pricing-models]]. |
| **OSS registration** (`oss_registration`) | Tax only | Toggle inside the Regions box when target = `regions` | EU One-Stop-Shop flag. Does NOT auto-swap to destination-country VAT rate — see [[tax-oss-semantics]]. Persistence is presence-based (stored `true` when the field is present at all). Manual switch — does NOT auto-track the €10,000 annual threshold. |
| **Shipping inclusion** (`shipping`) | Tax only — no UI control | enum **`yes` / `no` only** (defaults to `yes`) | Controls **bucketing in the totals pipeline** (`tax.before` when `no`; `tax.after` when `yes`), NOT "VAT also applies to the shipping line". Whether VAT applies to shipping is driven by the shipping quote's own `allow_modify_vat` flag, not this field. **FORCED to `no` for fees.** There is no `specific` value (older wiki phrasing was wrong). |
| **Per-region overrides** (`regions[]`) | Tax only | Repeatable rows in the Regions Exceptions box | Visible only when a Google Maps API key is configured AND a `geo_zone_id` is picked. Different rate per sub-region via Google Places autocomplete. Each row stores `state_iso_2`, the place name (`text`), and the rate. See [[tax-entity-overrides]]. |
| **Per-category overrides** (`categories[]`) | Tax only | Repeatable rows in the Categories Exceptions box | Always visible on the Tax form. Different rate for specific product categories (e.g., 9% on Books while base is 20%). Each row has Description (required), Category (required), Region (only if target=regions AND maps key configured), Amount. See [[tax-entity-overrides]]. |
| **No-VAT reason — EU** (`without_vat_reasons`) | Tax only | Free text, **max 64,000 characters** | Wording printed on the invoice when an EU sale qualifies for zero VAT (intra-community supply, reverse charge). Empty falls back to a platform default. |
| **No-VAT reason — non-EU** (`without_vat_reasons_non_eu`) | Tax only | Free text, **max 64,000 characters** | Same purpose for non-EU exports. |
| **Payment activation** (`payment_active`) | Fee only | Transient form switch `global` / `target` — **NOT persisted** | Drives whether `payment_provider` is required at save. `global` NULLs `payment_provider`; `target` makes it required. |
| **Payment provider** (`payment_provider`) | Fee only | **SINGLE-select** server-search dropdown when `payment_active = target` | `NULL` = "global / every method". When set, the fee applies only when the customer picks exactly this provider. For different rates per method, create multiple Fee rows — there is **no per-provider rate-override map**. `payment_provider_values` is a runtime display-name lookup, NOT persisted and NOT a rate map. |
| **Shipping activation** (`shipping_active`) | Fee only | Transient form switch `global` / `target` — **NOT persisted** | Same shape as `payment_active`. A Fee can use both payment and shipping activation at once — when both are `target`, it applies only when both conditions match. |
| **Shipping provider** (`shipping_provider`) | Fee only | **SINGLE-select** server-search dropdown when `shipping_active = target` | `NULL` = "global". Same shape as `payment_provider`. `shipping_provider_values` is a runtime display-name lookup, NOT a rate map. |

## Save-time normalization

On every save three normalizations run together:

- **Target inferred from `geo_zone_id`** — if `target` is empty but a `geo_zone_id` is supplied, `target` becomes `regions`. No orphan rule sits with `target=null` and a zone populated.
- **Zone wipe for rest-of-world** — when `target = restofworld`, any `geo_zone_id` is cleared to NULL. Switching regions → rest-of-world discards the old zone cleanly.
- **Rate stored as cents** — the entered `tax` value is integer-scaled (e.g. `20.50` → `2050`) so checkout math stays exact. Edits re-display the decimals; exports see the scaled value.

## Persistence quirks

- **No created/updated timestamps on the parent row.** Newest-zone-wins for VAT instead relies on the underlying [[geo-zone]] ID (highest wins) — see [[tax-rate-selection]].
- **Per-region/per-category override rows DO carry timestamps** — distinct from the parent row.

## Where it appears

- [[settings-taxes]] — the management screen carrying the form.
- [[tax]] — entity hub.

## Related

- [[tax]] — hub.
- [[tax-entity-vat-vs-fee]] — what the locked `vat` flag actually controls.
- [[tax-entity-overrides]] — per-region + per-category override mechanics.
- [[geo-zone]] — the zone the rule targets.
- [[settings-geo-zones]] — zone management screen.
- [[multi-currency]] — flat-amount Fee conversion.
- [[tax-pricing-models]] — runtime effect of `price_with_vat`.
- [[tax-oss-semantics]] — runtime effect of `oss_registration`.

## Open Questions

None.
