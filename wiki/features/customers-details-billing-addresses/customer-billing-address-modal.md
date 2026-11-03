---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Add / Edit panel"
route_name: customers-billing-addresses
route_path: /admin/customers/details/:id/billing-addresses
aliases: ["Customer billing address modal", "Add billing address", "Edit billing address", "Billing address form"]
tags: [customers, addresses, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, company fields, VIES, defaults, save hooks, storage, API).

# Customer billing address — Add / Edit panel

## Purpose

The side-panel form the merchant uses to **create** a new billing address or **edit** an existing one. It is the panel of the Shipping addresses tab, with one more card: **Company details**. Billing addresses have no **Delivery to** choice.

## Where to find it

- **Add:** click **+ Add address** in the header of the Billing addresses tab list.
- **Edit:** click the **Address column** value on any row of the list.

Both open an extra-large side panel, with **Cancel** and **Save** in its header. The title is **Add address** or **Edit address**.

## What the merchant can do here

- Fill in customer name (First name + Last name) for whose invoice this is.
- Enter address details — country, state, city, street, street number, post code, phone — with Google Maps autocomplete when the merchant has set the Google Maps API key in [[settings-cart]].
- Optionally fill in the four B2B **Company details** fields. Leave them blank for a B2C invoice. See [[customer-billing-address-company-fields]].
- Save the form via the **Save** button. Cancel discards the changes.

### What the merchant CANNOT do here

- Skip the Address section even for purely B2B customers — the address fields are required regardless of whether company details are filled.
- Save partial updates to a single field — every save re-validates and re-saves the full form.
- Mark the address as billing-only or shipping-only — physically separated by which tab opened the panel.

## Settings & fields

### Card 1 — Customer information

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| First name | text | Required | Min 2 chars, max 191. |
| Last name | text | Required | Min 2 chars, max 191. |

### Card 2 — Address

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Country | text | Required | Stored with its ISO 3166-1 alpha-2 code (e.g. `BG`). |
| State | text | Conditional | Required for countries that have states; rules driven by `checkout_hide_state_iso2` / `checkout_hide_state_name`. |
| City | text | Required | |
| Street | text | Required | Configurable via `checkout_hide_street_name`. |
| Street number | text | Required | Configurable via `checkout_hide_street_number`. |
| Additional address info | text | Optional | Placeholder *"Info"*. Configurable via `checkout_hide_additional_information`. |
| City postal code | text | Required | Min 3 chars; min 2 when the `post_code_not_required` setting on [[settings-cart]] is on. |
| Phone | country-code phone input | Required (per settings) | Normalised to E.164 on save — see [[customer-billing-address-save-validation]]. |

Google Maps autocomplete + an interactive map appear when the Google Maps API key is configured on [[settings-cart]]; see [[customer-shipping-address-google-maps]]. Without the key the merchant sees a plain manual form and the message *"To see Google Map, you need to set up a Google Maps Api Key"*.

### Card 3 — Company details

The four B2B fields are documented in detail on [[customer-billing-address-company-fields]]. Field summary:

| Field | Required | Maps to |
|-------|----------|---------|
| Company name | Optional (required when `checkout_hide_company_name = required`, OR when `company_vat` is filled — server-side interlock) | Business name on the invoice. |
| Company owner | Optional (required when `checkout_hide_company_mol = required`) | Bulgarian "MOL" — Materially-Responsible Person. |
| Company registration number | Optional (required when `checkout_hide_company_bulstat = required`) | Bulgarian "BULSTAT" — company-registration ID. |
| Company VAT identification number | Optional (required when `checkout_hide_company_vat = required`, OR when `company_name` is filled) | EU VAT / VIES-validated — see [[customer-billing-address-vies-validation]]. |

All four are independently optional **except** the coupled `company_name ↔ company_vat` interlock (filling either makes the other required at the validator level).

## Business rules

- **Field required-status is dynamically computed from store-level `checkout_hide_*` settings on [[settings-cart]].** Two CloudCart stores can have different required-vs-optional rules for the same field depending on their checkout configuration. The panel shows no required marks: a missing field comes back as an error next to it. See [[customer-billing-address-save-validation]].
- **Saving an invalid EU VAT may or may not block the save** depending on which endpoint is used — see [[customer-billing-address-vies-validation]] for the admin REST vs JSON-API v2 behaviour gap.

### Save handler

- **Create:** `POST /admin/api/core/customers/billing-address` under `hasApiPermission:customers`.
- **Edit:** `PATCH /admin/api/core/customers/billing-address/{id}`.
- Success toast: *"Address has been saved successfully"*.
- HTTP 422 validation errors are surfaced field-by-field in the panel.
- On success: the panel closes and the list reloads.

## Programmatic access

The same create / update operations are exposed via JSON-API v2 — see [[customer-billing-address-api]]. The save side effects (phone E.164, country-ISO normalisation, address text snapshot, VIES) apply identically to API writes.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-company-fields]] — the four B2B fields in this panel.
- [[customer-billing-address-vies-validation]] — VIES VAT validation triggered from this panel's save.
- [[customer-billing-address-save-validation]] — the conditional `checkout_hide_*` validation that drives the required-status of these fields, plus the shared save-time hooks.
- [[customer-billing-address-defaults]] — the first-added auto-promotion that happens transparently on the first save.
- [[customers-details-shipping-addresses]] — sister tab using the same panel, with no Company details.
- [[settings-cart]] — Google Maps API key, `checkout_hide_*` settings, `checkout_validate_company_vat`.

## Open questions

None.
