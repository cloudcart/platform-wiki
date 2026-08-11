---
type: feature
nav_path: "Settings → Taxes and fees"
route_name: taxes.settings
route_path: /admin/settings/taxes
aliases: ["Taxes and fees", "Tax rules", "VAT", "Fees", "Данъци и такси", "ДДС", "Такси"]
tags: [settings, taxes, fees, finance, vat]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Taxes and fees

## Purpose

A single management screen for two related entity types — **Tax** (a percentage or flat amount applied to product prices based on customer location, product category, and VAT settings) and **Fee** (an additional flat or percentage charge added to orders based on payment method or shipping method). The list view shows both in one table; the create flow first asks the merchant to choose which type via a picker modal, then opens a dedicated form. Taxes scope to geo zones from [[settings-geo-zones]] (or *"rest of world"*); fees scope to payment / shipping providers globally or to a specific subset. The system supports EU VAT semantics — OSS for cross-border B2C, separate *"no-VAT reasons"* text fields for EU vs non-EU customers.

## Where to find it

Sidebar → Settings → **Taxes and fees**. Route `/admin/settings/taxes` (list root) or `/admin/settings/taxes/:type/:id?` (create / edit).

## Sub-screens

Distinct routes within this feature.

| Label | Route name | Route path |
|-------|------------|------------|
| List | `taxes.settings` | `/admin/settings/taxes` |
| Create / Edit | `taxes.create` | `/admin/settings/taxes/:type/:id?` |

## Sub-pages (in this cluster)

This feature is split into seven aspect pages — each covers one well-scoped slice of the Taxes and Fees surface. The Assistant should drill into the aspect that matches the question, not read every page.

- [[settings-taxes-vat-rules]] — VAT-type rules (`vat=yes`): geo-zone scoping, country-level matching, single-winner precedence, the auto-created "Global" companion tax, the hidden billing-address country-limit side effect, OSS for cross-border EU.
- [[settings-taxes-fees]] — Fee-type rules (`vat=no`): global vs target activation, single-provider-per-fee semantics, additive stacking, the corrected VAT-on-fee behaviour (a fee's `vat` flag does NOT suppress VAT on the fee).
- [[settings-taxes-overrides]] — per-category and per-region rate overrides: shared `tax_overrides` storage, the four-level precedence ladder at checkout, the per-category uniqueness check, the gotcha where a category override silently beats a region override on the same line.
- [[settings-taxes-pricing-display]] — `price_with_vat` (inclusive vs exclusive pricing), `shipping` inclusion flag, storefront "VAT included" labels, the inclusive-VAT reverse-compute formula, what changes for "without VAT" customers.
- [[settings-taxes-oss-no-vat]] — OSS (One-Stop-Shop) registration mechanics + the two `without_vat_reasons` text fields (EU vs non-EU export) printed on invoices when VAT is zero.
- [[settings-taxes-validation]] — every field's validation rule, error messages, the 90% rate cap, save-time normalisation, the `vat` flag immutability (cannot flip Tax ↔ Fee after create), and the hard-delete behaviour.
- [[settings-taxes-integrations]] — downstream consumers of the Tax row: SmartBill invoicing, DPD BG / DPD RO fiscal-receipt eligibility, XML product feeds, the one-time BGN→EUR migration command, and JSON-API v2 access (read-only, computed-only via [[api-order-tax]]).

## What the merchant can do here

From the list view: see all defined Taxes and Fees in one table (name, rate value, type badge), sort / filter / paginate, click row to edit, click **+ Add new** to open the type picker modal (*"Add Tax or Fee"*), choose **Add Tax** or **Add Fee**, delete via the row trash icon (no confirmation modal). Selecting a card navigates to `taxes.create` with `type=tax` or `type=fee`; backdrop click dismisses the modal without choosing.

For the field-by-field catalogue of each form (Name + Rate, Regions, Categories exceptions, Regions exceptions, Payments, Shippings) — see the relevant aspect page.

## Settings & fields

Each tax / fee record stores 14 fields shared between Tax and Fee rows; which apply depends on the `vat` flag. Summary:

- **Identity** — `name` (max 100 chars), `description` (free text). Taxes do **not** track created / updated timestamps.
- **Rate** — `type` (`percent` / `flat`) + `tax` (the value). Percent capped at 90%, flat has no numeric cap. See [[settings-taxes-validation]].
- **Type** — `vat` (`yes` = VAT rule / `no` = fee). NOT user-toggleable after create.
- **Geo scope** — `target` (`regions` / `restofworld`) + `geo_zone_id` ([[settings-geo-zones]] when `target=regions`).
- **Pricing display (Tax only)** — `price_with_vat` (inclusive / exclusive), `shipping` (inclusion). Both forced to `0` / `no` for fees — see [[settings-taxes-pricing-display]].
- **EU compliance (Tax only)** — `oss_registration`, `without_vat_reasons`, `without_vat_reasons_non_eu` (max 64K chars each). See [[settings-taxes-oss-no-vat]].
- **Fee target (Fee only)** — `payment_provider` (single key when `payment_active=target`), `shipping_provider` (single key when `shipping_active=target`). See [[settings-taxes-fees]].

Per-category and per-region rate overrides live in separate `tax_overrides` storage — see [[settings-taxes-overrides]].

## Business rules

Each cross-cutting rule is documented on its aspect page. Slim summary:

- **Exactly ONE VAT tax wins per order** — regional beats rest-of-world; between two regional matches, the most recently created wins. Only country-level zone operations count (city / region / polygon / distance / post-code rules are ignored for tax matching). See [[settings-taxes-vat-rules]].
- **ALL matching fees stack additively** — every fee whose payment / shipping target matches adds its own line. See [[settings-taxes-fees]].
- **Per-category override beats per-region override on the same line** — they do NOT combine. See [[settings-taxes-overrides]].
- **A fee's `vat` flag does NOT suppress VAT on the fee** — with an active VAT rule, every fee ALWAYS gets VAT. The only way to make a fee VAT-free is to make the whole order VAT-exempt via the customer's B2B VAT-number flow. See [[settings-taxes-fees]].
- **A new regional VAT auto-creates a `- Global` companion** when no rest-of-world VAT exists. See [[settings-taxes-vat-rules]].
- **A regional-only VAT setup hidden-restricts the storefront's billing-address country picker** to the zone's countries. See [[settings-taxes-vat-rules]].
- **Saving applies immediately** — next checkout uses the new rule. No queue, no webhooks.
- **Delete is hard delete** (no cascade, no soft-delete). Existing orders keep their `orders_taxes` snapshot — historical invoices unaffected. See [[settings-taxes-validation]].
- **Permission** — a moderator needs either the broad **Settings** permission OR the specific **Taxes** (`store.taxes`) grant from [[settings-staff]] to list, create, edit, or delete tax rules. Owners always pass.
- **`invoicing_address` drives tax matching** — the `invoicing_address` setting on [[settings-cart]] (BillingAddress vs ShippingAddress) decides which address is the customer location when matching geo zones. Changing it can change which taxes apply — important for stores serving multiple jurisdictions.

## Programmatic access

There is **no dedicated tax/fee resource** in the public **JSON-API v2** — tax and fee records are not exposed for direct read or write. What IS exposed is the **computed tax breakdown per order** via [[api-order-tax]]. To inspect or modify tax / fee rules, the merchant must use this admin screen. See [[settings-taxes-integrations]] for downstream consumers, and [[json-api-v2]] for the API overview.

## Related

- [[settings]] — parent hub.
- [[settings-geo-zones]] — `target=regions` references geo zones; required prerequisite.
- [[settings-cart]] — `invoicing_address` decides which address is used for tax matching.
- [[settings-general]] — `operation_country` is the default VAT jurisdiction when OSS is not enabled.
- [[settings-invoicing]] — invoices include the tax / fee breakdown; "no-VAT reasons" text is printed there.
- [[settings-payment-providers]] — fee target activation references payment providers.
- [[settings-staff]] — `store.taxes` permission.
- [[shipping]] — fee target activation references shipping providers.
- [[product]] — products carry category memberships that drive per-category tax overrides.
- [[category]] — entity page.
- [[tax]] — entity page.
- [[tax-computation]] — concept page on how taxes are computed at checkout.
- [[multi-currency]] — concept page on currency interaction with tax amounts.
- [[checkout-flow]] — concept page; taxes / fees applied during the checkout step.
- [[api-order-tax]] — JSON-API v2 read endpoint for the per-order tax breakdown.
- [[json-api-v2]] — API overview.

## Open questions

None.
