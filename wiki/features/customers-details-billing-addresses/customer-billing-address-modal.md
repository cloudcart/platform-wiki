---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Add / Edit modal"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Customer billing address modal", "Add billing address", "Edit billing address", "Billing address form"]
tags: [customers, addresses, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, company fields, VIES, defaults, save hooks, storage, API).

# Customer billing address — Add / Edit modal

## Purpose

The side-panel form the merchant uses to **create** a new billing address or **edit** an existing one. It is the SAME component as the shipping-address modal but invoked with `addressType="billing"` — that prop unlocks the fourth **Company details** section.

## Where to find it

- **Add:** click **+ Add address** in the header of the Billing addresses tab list.
- **Edit:** click the **Address column** value on any row of the list.

Both open an xl-sized side panel. The title is **Add address** or **Edit address** based on whether `address.id` is present.

## What the merchant can do here

- Fill in customer name (First name + Last name) for whose invoice this is.
- Enter address details — country, state, city, street, street number, post code, phone — with Google Maps autocomplete when the merchant has set the Google Maps API key in [[settings-cart]].
- Optionally fill in the four B2B **Company details** fields. Leave them blank for a B2C invoice. See [[customer-billing-address-company-fields]].
- Save the form via the **Save** button. Cancel discards the changes.

### What the merchant CANNOT do here

- Skip the Address section even for purely B2B customers — the address fields are required regardless of whether company details are filled.
- Save partial updates to a single field — every save re-validates and re-saves the full form.
- Mark the address as billing-only or shipping-only — physically separated by which tab opened the modal.

## Settings & fields

### Section 1 — Customer information

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| First name | text | Required | Min 2 chars, max 191. |
| Last name | text | Required | Min 2 chars, max 191. |

### Section 2 — Address

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Country | select / autocomplete | Required | Stored as ISO 3166-1 alpha-2 (e.g. `BG`). |
| State | select / text | Conditional | Required for countries that have states; rules driven by `checkout_hide_state_iso2` / `checkout_hide_state_name`. |
| City | text | Required | |
| Street | text | Required | Configurable via `checkout_hide_street_name`. |
| Street number | text | Required | Configurable via `checkout_hide_street_number`. |
| Post / ZIP code | text | Required by default | Toggleable via the `post_code_not_required` setting on [[settings-cart]]; min 2 chars when required. |
| Phone | country-code phone input | Required | Normalised to E.164 on save — see [[customer-billing-address-save-validation]]. |
| Additional address info | text | Optional | Configurable via `checkout_hide_additional_information`. |

Google Maps autocomplete + a 300 px interactive map appear when the Google Maps API key is configured on [[settings-cart]]; without the key the merchant sees a plain manual form (and a banner explaining the key is missing).

### Section 3 — Company details (billing only)

The four B2B fields are documented in detail on [[customer-billing-address-company-fields]]. Field summary:

| Field | Required | Maps to |
|-------|----------|---------|
| Company name | Optional (required when `checkout_hide_company_name = required`, OR when `company_vat` is filled — server-side interlock) | Business name on the invoice. |
| Company owner | Optional (required when `checkout_hide_company_mol = required`) | Bulgarian "MOL" — Materially-Responsible Person. |
| Company registration number | Optional (required when `checkout_hide_company_bulstat = required`) | Bulgarian "BULSTAT" — company-registration ID. |
| Company VAT identification number | Optional (required when `checkout_hide_company_vat = required`, OR when `company_name` is filled) | EU VAT / VIES-validated — see [[customer-billing-address-vies-validation]]. |

All four are independently optional **except** the coupled `company_name ↔ company_vat` interlock (filling either makes the other required at the validator level).

## Business rules

- **Same Vue component as the shipping-address modal, different prop.** The form is `CustomersAddressModal.vue`; `addressType="billing"` exposes the Company details card. `addressType="shipping"` hides it. (verify)
- **Field required-status is dynamically computed from store-level `checkout_hide_*` settings on [[settings-cart]].** Two CloudCart stores can have different required-vs-optional markers for the same address-modal field depending on their checkout configuration. See [[customer-billing-address-save-validation]].
- **Saving an invalid EU VAT may or may not block the save** depending on which endpoint is used — see [[customer-billing-address-vies-validation]] for the admin REST vs legacy JSON-API behaviour gap.
- **Save triggers refetch of the [[customers-details]] Default address sidebar card** so the parent screen reflects the change immediately.

### Save handler

- **Create:** `POST /admin/api/core/customers/billing-address` under `hasApiPermission:customers`.
- **Edit:** `PATCH /admin/api/core/customers/billing-address/{id}`.
- Success toast: *"Address has been saved successfully"*.
- HTTP 422 validation errors are surfaced field-by-field in the modal.
- On success: the modal closes, the list refetches, and the [[customers-details]] sidebar refreshes.

## Programmatic access

The same create / update operations are exposed via JSON-API v2 — see [[customer-billing-address-api]]. The save side effects (phone E.164, country-ISO normalisation, address text snapshot, VIES) apply identically to API writes.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-company-fields]] — the four B2B fields exposed by this modal.
- [[customer-billing-address-vies-validation]] — VIES VAT validation triggered from this modal's save.
- [[customer-billing-address-save-validation]] — the conditional `checkout_hide_*` validation that drives the required-status of these fields, plus the shared save-time hooks.
- [[customer-billing-address-defaults]] — the first-added auto-promotion that happens transparently on the first save.
- [[customers-details-shipping-addresses]] — sister tab using the SAME modal component but with Company details hidden.
- [[settings-cart]] — Google Maps API key, `checkout_hide_*` settings, `checkout_validate_company_vat`.

## Open questions

- Confirm the exact `CustomersAddressModal.vue` prop and the `addressType` discriminator (verify).
