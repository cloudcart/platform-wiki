---
type: feature
nav_path: "Customers → Customer details → Billing addresses"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Customer billing addresses", "Customer billing address list", "Billing addresses", "Адреси за фактуриране"]
tags: [customers, addresses, billing]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---

# Customer billing addresses

## Purpose

The list of **saved billing addresses** for one customer — the addresses that appear on invoices. For B2B customers these typically include company name, VAT number, registration number ("BULSTAT" in Bulgarian context), and company owner ("MOL"); for B2C customers the company section is left blank and the billing address often mirrors the shipping address.

Each customer can have many billing addresses but exactly **one default** (used for invoice rendering and tax computation). The page is functionally identical to [[customers-details-shipping-addresses]] but with the **Company details** section of the address modal exposed (since billing is where company info legally lives) and with a **VIES VAT validation** save-time hook layered on top.

This hub is split into focused aspects — read the one that matches the question, not all of them.

## Sub-pages (in this cluster)

- [[customer-billing-address-list]] — list table columns (Region, Address, Post code, Phone, Type), the Is-company-address filter, the bulk Delete action, and what the merchant CANNOT do from this view.
- [[customer-billing-address-modal]] — the Add / Edit modal: the four sections (Customer info + Address + Company details), field-by-field, B2C vs B2B usage, Set-as-default and Edit triggers.
- [[customer-billing-address-company-fields]] — the four company fields (`company_name`, `company_mol`, `company_bulstat`, `company_vat`), what each maps to in Bulgarian invoice law, independent optionality, and the server-coupled `company_name ↔ company_vat` interlock.
- [[customer-billing-address-vies-validation]] — EU VIES check at save (not only at checkout), the four gating conditions, the 7-day cache, country-prefix format check (Greece "EL"), the `vat_validation` extension and the admin REST vs legacy JSON-API behaviour gap.
- [[customer-billing-address-defaults]] — one-default-per-customer rule, first-added auto-promotion, "Set as default" action, hard-guarded deletion of the current default, independence from default shipping.
- [[customer-billing-address-save-validation]] — save-time hooks shared with shipping (phone E.164, country ISO normalisation, lat/lng auto-fill, address text snapshot), conditional `checkout_hide_*` validation, no per-courier mapping for billing.
- [[customer-billing-address-storage]] — separate DB table from shipping addresses, `default_billing_address_id` pointer on the customer, the `vies` JSON column, the `activeByGeoZones` scope for tax matching, and the invoice-snapshot decoupling.
- [[customer-billing-address-api]] — JSON-API v2 read / create / update / delete for billing addresses, same side effects + VIES, default-billing delete protection, plus the API auto-promotion behaviour.

## Where to find it

From [[customers-details]] → **Billing addresses** tab. The route is `/admin/customers-new/details/:id/billing-addresses`.

## What the merchant can do here

- View every saved billing address in a paginated, sortable, filterable table — see [[customer-billing-address-list]].
- Add a new billing address through the Add modal — see [[customer-billing-address-modal]].
- Edit any existing billing address (click the row's Address cell) — see [[customer-billing-address-modal]].
- Fill in the Company details (B2B) or leave them blank (B2C) — see [[customer-billing-address-company-fields]].
- Promote a non-default address to default via "Set as default" — see [[customer-billing-address-defaults]].
- Bulk-delete selected billing addresses with confirmation — see [[customer-billing-address-list]].

### What the merchant CANNOT do here

- Add a customer-side shipping address from this tab — shipping addresses live in their own list. See [[customers-details-shipping-addresses]].
- Mark an address as "billing-only" or "shipping-only" — the lists are physically separated; the same conceptual address must be entered twice if needed in both places.
- Delete the customer's current default billing address without promoting another billing address first — see [[customer-billing-address-defaults]].

## Settings & fields

This is a hub — per-aspect pages carry the field tables. Quick map:

- List columns + filter → [[customer-billing-address-list]].
- Add / Edit modal fields (Customer info + Address + Company details) → [[customer-billing-address-modal]].
- The four B2B company fields and what they mean → [[customer-billing-address-company-fields]].
- Conditional `checkout_hide_*` required-vs-optional behaviour → [[customer-billing-address-save-validation]].

## Business rules

This is a hub — full mechanics live on the aspect pages. Six rules every consumer of this cluster must know:

- **Default is a customer-level pointer (`default_billing_address_id`), independent from default shipping.** Setting a new default billing has zero effect on the default shipping. See [[customer-billing-address-defaults]] + [[customer-billing-address-storage]].
- **B2B company fields are independently optional — except `company_name ↔ company_vat`, which is coupled at the server.** Filling either of those two makes the other required at the validator level. `company_mol` and `company_bulstat` remain freely optional. See [[customer-billing-address-company-fields]].
- **VIES VAT validation runs at save-time, NOT only at checkout, when four conditions all hold.** Setting `checkout_validate_company_vat` ON in [[settings-cart]] + EU country + VAT prefix matching the country + a non-empty `company_vat`. Result cached for 7 days in a `vies` JSON column. See [[customer-billing-address-vies-validation]].
- **Default billing CANNOT be deleted directly.** A delete that targets the customer's current default billing is rejected with HTTP 422 *"Cannot delete customer default billing address."* Bulk delete that includes the default fails the whole batch. See [[customer-billing-address-defaults]].
- **Deletion does NOT cascade to past orders.** Invoices on past orders keep their snapshot of the billing address at the time the order was placed. See [[customer-billing-address-storage]].
- **No per-courier mapping side effect on billing saves** (unlike shipping). Billing saves run only the phone / lat-lng / country-ISO / text-snapshot / VIES hooks. See [[customer-billing-address-save-validation]].

### Permission

Standard `customers` permission scope. All admin API endpoints under `/admin/api/core/customers/billing-address` are protected by `hasApiPermission:customers` middleware.

### Storefront sync

Changes here reflect immediately on the storefront — the next time the customer visits their address book on the storefront account page, they see the updated list.

## Programmatic access

Customer billing addresses can be read, created, updated, or deleted via **JSON-API v2** — see [[customer-billing-address-api]] and [[api-customer-billing-address]].

**Same side effects apply.** API writes fire the same save-time hooks as the modal (phone E.164, country ISO normalisation, address text snapshot, **plus VIES VAT validation** when the gating conditions in [[customer-billing-address-vies-validation]] hold) and respect the same default-billing delete protection. See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

Aspects in this cluster — see Sub-pages above: [[customer-billing-address-list]], [[customer-billing-address-modal]], [[customer-billing-address-company-fields]], [[customer-billing-address-vies-validation]], [[customer-billing-address-defaults]], [[customer-billing-address-save-validation]], [[customer-billing-address-storage]], [[customer-billing-address-api]].

External pages:

- [[customers-details]] — parent details page.
- [[customers-details-shipping-addresses]] — sister tab using the SAME modal component but with Company details hidden and no VIES hook.
- [[settings-cart]] — `checkout_validate_company_vat` flag, `checkout_hide_company_*` settings, Google Maps API key.
- [[settings-invoicing]] — invoice template pulls the billing address from here at order placement time.
- [[settings-taxes]] — VAT brackets evaluated against the billing-address country via the `activeByGeoZones` scope.
- [[api-customer-billing-address]] — JSON-API v2 endpoints.
- [[customer]] — entity page.

## Open questions

None — all previously-flagged items distributed to sub-pages.
