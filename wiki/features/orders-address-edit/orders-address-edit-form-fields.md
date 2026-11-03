---
type: feature
nav_path: "Orders → Order details → Address → Form fields"
route_name: admin.orders.address.shipping.edit
route_path: /admin/orders/address/{shipping|billing}/{order_id}/edit
aliases: ["Order address form fields", "Address form panels", "Address edit field list", "Billing company fields", "Shipping address fields"]
tags: [orders, address, fields, forms]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-address-edit]]. See the hub for related aspects (flows, office/locker, propagation, side effects).

# Order address — form fields (Panels A / B / C)

## Purpose

The address-edit feature opens THREE distinct panel templates depending on the action — full Edit form, Change saved-address picker, and the Office menu entry. This page is the field-by-field inventory across all three, separated by shipping vs billing where they differ.

## Where to find it

All three panels open as slide-from-right side-panels (`side-panel` chrome — Cancel + Save buttons in the header). The merchant reaches them from [[orders-details]] → Customer sidebar card → settings cog. See [[orders-address-edit-flows]] for the exact entry-point matrix.

## What the merchant can do here

The merchant fills in the panel's fields and clicks **Save** to commit. Cancel discards. Each panel has a different field shape.

### Panel A — Edit / Add (`address/form.tpl`)

This is the full address form. It has up to four sections:

1. **Shipping-method radio row** (shipping only, courier-dependent) — see [[orders-address-edit-office-locker]].
2. **Standard address fields** (everyone).
3. **Billing-specific company fields** (billing only).
4. **Update-in-profile toggle** at the bottom — see [[orders-address-edit-propagation]].

### Panel B — Change (`address/change.tpl`)

ONE field only — a dropdown of the customer's saved addresses. No typing. See below for the field table.

### Panel C — Office (`address/office.tpl`)

Reached via the explicit "Office" submenu link (`admin.orders.address.office.edit`) — distinct from Panel A's office radio. This panel re-uses the same standard address `_form.tpl` include, NOT a dedicated office picker. So the merchant filling in the Office panel gets the regular address-form layout. (This is a minor template artefact — for actual office picking, Panel A's office-radio path is the dominant flow. See [[orders-address-edit-office-locker]].)

## Settings & fields

### Standard address fields (shipping + billing — Panel A)

| Field | Required | Notes |
|-------|----------|-------|
| First name | Yes | Recipient name. |
| Last name | Yes | Recipient name. |
| Country | Yes | Autocomplete + flag. |
| City | Yes | Autocomplete via Google Places when configured per [[settings-cart]]. |
| Postal code | Yes | |
| Street | Yes | |
| Street number | Yes | |
| Additional info | No | Apartment, suite, building — free-text. |
| Phone | Yes | International phone input (`js-phone-intl`); country-iso2 + IP auto-detect; error label *"Invalid phone number"*. |

The address-fields block is included from the SAME partial template that drives [[customers-details-shipping-addresses]] (`customers/details/addresses/_form.tpl`), so the merchant gets exactly the same form layout used on the customer profile.

### Billing-specific extra fields (Panel A — billing only)

| Field | Required | Notes |
|-------|----------|-------|
| Company name | No | |
| Company VAT identification number | No | VAT ID for invoicing. |
| Company registration number | No | BULSTAT in Bulgarian context. |
| Company owner | No | MOL in Bulgarian context. |

Billing addresses do NOT have a shipping-method radio row and do NOT support office / locker. Billing is always "to address".

### Office / Locker picker fields (Panel A — shipping, when Office or Locker radio is selected)

| Field | Element | Notes |
|-------|---------|-------|
| Office / Locker picker | Select2 AJAX-loaded | Live-queries `apps.<courier>.offices` or `.lockers` — see [[orders-address-edit-office-locker]] for the full mechanics. |
| Office name | Hidden input | Auto-set when picker selection changes. |
| First name | Required text input | Recipient name. |
| Last name | Required text input | Recipient name. |
| Phone | International phone input | Same `js-phone-intl` widget as the address form. |

### Panel B field (Change — both shipping and billing)

| Field | Element | Notes |
|-------|---------|-------|
| Customer address | Select2 dropdown | Lists all of the customer's saved addresses (`{$addresses}` from the controller). Each option's label is the formatted address minus the name. When the order's current address has a link to a saved address, the matching option is pre-selected. |

POSTs to `admin.orders.address.{shipping|billing}.change` with `customer_address_id`. See [[orders-address-edit-side-effects]] for what happens on save.

### Update-in-profile toggle (Panel A — shipping only)

A checkbox at the bottom of the Panel A form:

- **Field name**: `update_address_in_profile`, value `1`.
- **Default**: unchecked. The platform reads this via a presence check (request.has) — an unchecked checkbox is not submitted at all.
- **Effect**: when checked AND the order's shipping address has a saved-profile link, the changes also propagate to the customer's saved shipping address; when unchecked, only the order's snapshot updates.

See [[orders-address-edit-propagation]] for the full propagation rules (including the asymmetric automatic billing propagation).

## Business rules

### Shipping vs billing field shape

The two shapes diverge in three places:

- Shipping has the shipping-method radio row (when the courier supports offices / lockers); billing never does.
- Billing has four extra company fields (name, VAT, registration number, owner); shipping does not.
- Shipping has the update-in-profile checkbox; billing does not need one — propagation is automatic.

### Phone field is the same widget as the customer profile

The `js-phone-intl` widget normalises the phone to international format, validates against the selected country's pattern, and surfaces a per-field error message when invalid. The same widget runs on [[customers-details]] and the checkout flow, so the field UX is consistent across the platform.

### Google Places integration

The City field has Google Places autocomplete when the merchant has configured a Google Maps API key on [[settings-cart]]. Without the key, the field falls back to a plain text input. The autocomplete is driven by `data-google-place-country_id` and `data-google-place-locality_id` attributes on the address-fields partial.

### Required vs optional

The required fields (First name, Last name, Country, City, Postal code, Street, Street number, Phone) match the storefront's checkout requirements. Optional fields (Additional info, all four billing company fields) can be left empty without blocking save. For non-Bulgarian merchants the company fields may not apply at all; for Bulgarian merchants, the VAT + Registration number + Owner triplet is normally required for VAT-registered B2B invoicing — but the form does NOT enforce this at the field level. The merchant verifies completeness against the invoice rules separately.

### Smarty + jQuery + AJAX panels

- Forms open as slide-from-right panels (`data-ajax-panel`).
- Submission uses `ajaxForm`.
- The update-in-profile toggle uses the jQuery `switchButton` plugin for the visual switch UI.
- After save, the platform auto-cascades reload of the address card, summary, and history — see [[orders-address-edit-side-effects]].

## Related

- [[orders-address-edit]] — hub.
- [[orders-address-edit-flows]] — which panel for which operation.
- [[orders-address-edit-office-locker]] — the shipping-method radio row + picker.
- [[orders-address-edit-propagation]] — what the Update-in-profile checkbox does.
- [[orders-address-edit-side-effects]] — what happens after Save.
- [[customers-details-shipping-addresses]] — same `_form.tpl` partial, customer-profile context.
- [[customers-details-billing-addresses]] — billing equivalent.
- [[settings-cart]] — Google Maps API key for City autocomplete.

## Open questions

- None.
