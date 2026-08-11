---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Storage"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Billing address storage", "default_billing_address_id", "vies JSON column", "Billing address table", "activeByGeoZones"]
tags: [customers, addresses, billing, storage]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, company fields, VIES, defaults, save hooks, API).

# Customer billing address — Storage model

## Purpose

How billing addresses are physically stored: their own DB table separate from shipping addresses, a customer-level pointer for the default, a JSON column for the VIES result, and a geo-zone scope for tax matching. Critically: an order placed against a billing address keeps a **snapshot** of the address fields, so subsequent edits / deletes to the saved address don't retroactively change past invoices.

## Where to find it

Storage is invisible to the merchant directly — but the shape determines support investigations:

- "Customer changed their VAT, but the old invoice still has the old VAT" → invoice snapshot decoupling, by design.
- "Customer's default billing column on their JSON-API record is different from their default shipping column" → two separate pointers.
- "VIES result was cached / not re-called" → the `vies` JSON column on the row.

## What the merchant can do here

(There is no merchant-facing UI for storage; this aspect documents the on-disk shape for support reference.)

### What the merchant CANNOT do here

- Edit the `text` snapshot column directly — it is recomputed on every save (see [[customer-billing-address-save-validation]]).
- Edit the `vies` JSON column directly — it is overwritten by the VIES save-hook (see [[customer-billing-address-vies-validation]]).
- Combine billing + shipping rows into a single physical address — they live in separate tables, even when the same conceptual address is needed in both places.

## Settings & fields

### Customer-level pointers (on the customer row)

| Column | Points to | Indep. |
|--------|-----------|--------|
| `default_billing_address_id` | The current default billing-address row. | Independent from `default_address_id` (shipping). |
| `default_address_id` | The current default shipping-address row. | Independent from `default_billing_address_id`. |

The billing-address row carries NO `is_default` flag — default is computed by comparing the customer pointer to the row id at read time.

### Billing-address row — key columns

| Column | Purpose |
|--------|---------|
| `id` | Primary key. |
| `customer_id` | Foreign key to the customer row. |
| Person fields | `first_name`, `last_name`, `phone` (E.164), `phone_international`, `phone_national`, `phone_rfc3966`. |
| Address fields | `country_iso2`, `country_iso3`, `country_name`, `state_iso2`, `state_name`, `city`, `street`, `street_number`, `post_code`, `additional_information`, `latitude`, `longitude`. |
| Company fields | `company_name`, `company_vat`, `company_bulstat` (= registration number), `company_mol` (= owner). |
| `vies` | JSON object: `{countryCode, vatNumber, requestDate, valid, name, address, checkDate}`. See [[customer-billing-address-vies-validation]]. |
| `text` | Computed text snapshot — read by lists / API responses / invoice rendering. See [[customer-billing-address-save-validation]]. |
| Timestamps | `created_at`, `updated_at`. |

### Scopes

| Scope | What it does |
|-------|--------------|
| `activeByGeoZones` / `whereActiveByGeoZones` | Joins each billing address to the VAT geo-zones table. The address's `country_iso2` is looked up against the VAT geo-zone country lists from [[settings-taxes]] — this is how the invoice rendering picks the right tax rate. |
| `realAddress` | Excludes pickup-point / marketplace pseudo-addresses if any are stored here (verify — likely shipping-only; billing rows are always "real" addresses). |

## Business rules

### Separate table from shipping

Billing addresses and shipping addresses live in physically separate DB tables. There is NO single "addresses" table with a `type` discriminator. Practical consequences:

- The same conceptual address (e.g. the customer's office) must be entered twice if needed in both places — once via the Shipping addresses tab, once via the Billing addresses tab.
- Bulk operations operate per table — a bulk delete on billing addresses cannot accidentally remove shipping addresses.
- Storage / disk footprint is approximately 2× a unified-table design when the merchant tracks both shipping and billing for every customer.

### Two independent default pointers on the customer

`default_billing_address_id` and `default_address_id` (shipping) are independent columns on the customer record. Setting one has zero effect on the other. See [[customer-billing-address-defaults]].

### Invoice snapshot decoupling

When an order is placed, the invoice / credit note rendering pulls the customer's default billing address fields **at order-placement time** and stores them on the order row itself (the order's own billing-address snapshot). After that point:

- Editing the saved billing address (e.g. fixing a typo in company name) does NOT change the original order's invoice.
- Deleting the saved billing address does NOT cascade to the order's snapshot — the past invoice keeps its data.
- Re-generating the original invoice pulls the SNAPSHOT, not the live address row.

This is the standard CloudCart pattern: every customer-data point that an order depends on is snapshotted at the order-placement boundary. See [[order]] for the broader snapshot model.

### `vies` JSON column persists across saves

The result object lives in its own JSON column on the address row. The 7-day cache is implemented by reading `vies.checkDate` against today's date at save time — see [[customer-billing-address-vies-validation]]. The column is `null` for non-EU addresses, addresses without a `company_vat`, and addresses where the VIES gating conditions did not all hold.

### Geo-zone tax matching

The `activeByGeoZones` scope is how the platform decides which VAT rate to apply when rendering an invoice. The address's `country_iso2` is joined against the VAT geo-zones table from [[settings-taxes]]. A billing address in Bulgaria + an EU geo-zone with Bulgaria in its list → that geo-zone's VAT rate applies.

### No per-courier mapping rows

Shipping addresses have a satellite table of per-courier mapping rows (one row per active courier, mapping the address to that courier's office / zone / city IDs). Billing addresses have NO such satellite — billing is used for invoicing + tax, not for shipping routing. See [[customer-shipping-address-save-hooks]] for the shipping-side equivalent.

## Programmatic access

JSON-API v2 exposes the billing-address row + the customer-level pointers. See [[customer-billing-address-api]] for the field list and how the `vies` JSON column is surfaced (typically as a nested object).

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-defaults]] — the customer-level pointers and the delete-protection that depends on them.
- [[customer-billing-address-vies-validation]] — the `vies` JSON column lifecycle.
- [[customer-billing-address-save-validation]] — the `text` snapshot and the hooks that write it.
- [[customer-billing-address-api]] — JSON-API v2 representation of these columns.
- [[settings-taxes]] — VAT geo-zones evaluated against the stored `country_iso2`.
- [[settings-invoicing]] — invoice rendering pulls from the order's snapshot, not the live row.
- [[order]] — the snapshot pattern at the order-placement boundary.

## Open questions

- Confirm whether the `realAddress` scope applies to billing-address rows at all (likely shipping-only) (verify).
- Confirm the exact column / table names for the billing-address satellite if any (the doc lists the row columns but not the table name — kept generic on purpose) (verify).
