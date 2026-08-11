---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Add / Edit modal"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping address modal", "Add shipping address modal", "Edit shipping address modal", "CustomersAddressModal shipping mode"]
tags: [customers, addresses, shipping, modal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, Google Maps, defaults, save-hooks, storage, validation, API).

# Customer shipping addresses — Add / Edit modal

## Purpose

The single modal that handles both **Add** and **Edit** for a customer's saved shipping address. Mode is chosen by whether an `address` prop is passed in — passing one makes it Edit mode and pre-populates every field. The same modal is reused by the [[customers-details]] Default address sidebar (pen icon opens it in shipping mode pre-populated with the current default).

The modal is an `xl` (extra-large) `CcModal` with a sticky save button. Background dismiss is blocked while saving (`no-close-on-backdrop=true` during submit).

## Where to find it

- Click + **Add address** at the top right of the [[customer-shipping-address-list]] → opens in Add mode.
- Click any row's **Address** cell on the same list → opens in Edit mode pre-populated.
- Click the pen icon on the [[customers-details]] Default address sidebar → opens in Edit mode against the current default.
- Click the empty-state **+ Add address** link inside the [[customers-details]] Default address sidebar (when the customer has zero addresses) → opens in Add mode.

## What the merchant can do here

- Fill in the customer's first + last name.
- Use Google Maps autocomplete to fill country / state / city / street / street number / post code in one click — see [[customer-shipping-address-google-maps]].
- Drag the interactive map marker to update the address fields via reverse-geocoding — see [[customer-shipping-address-google-maps]].
- Override any field manually (Country, State, City, Street, Street number, City postal code).
- Add free-text apartment / suite / "leave at front door" instructions.
- Enter the recipient's phone with a country-code phone input (auto-reformatted to E.164 on save — see [[customer-shipping-address-save-hooks]]).
- Save the address with a sticky **Save** button.

### What the merchant CANNOT do here

- Fill in **Company details** (VAT id, company name, etc.) — that card is hidden on shipping addresses; only shown when the modal opens in `addressType === 'billing'`. See [[customers-details-billing-addresses]].
- Skip required fields — server-side validation rejects with field-by-field 422 errors. Which fields are required depends on store settings — see [[customer-shipping-address-validation]].
- Edit the geo on a pickup-point / office address — those addresses have `office_id` set and are tied to the courier's office record. See [[customer-shipping-address-storage]].

## Settings & fields

The modal has three sections — only two are visible in shipping mode.

### 1) Customer information card

| Field | Type | Required | Notes |
|---|---|---|---|
| First name | text | Required | min 2 / max 191 chars |
| Last name | text | Required | min 2 / max 191 chars |

### 2) Address card

| Field | Type | Required | Notes |
|---|---|---|---|
| Enter city and address here | Google Places autocomplete | n/a (UI helper) | Visible only when `google_maps_api_key` is set in [[settings-cart]]. See [[customer-shipping-address-google-maps]]. |
| Google Map (300px height) | Interactive map | n/a | Visible only when the API key is set. Initial centre: lat 42.6977082, lng 23.3218675 (Sofia, BG). See [[customer-shipping-address-google-maps]]. |
| No-map banner | info | n/a | Visible when key NOT set: *"To see Google Map, you need to set up a Google Maps Api Key"* + link to [[settings-cart]] (opens in new tab). |
| Geo-error banner | red error | n/a | Slides down when validation returns `geo_name_city_id` or `city_id` errors: *"Currently the address can not be saved, please try again later, or contact our support team."* |
| Country | text | Required | Disabled while submit-loader or geo-loader running. |
| State | text | Required (per settings) | Conditional rules from `checkout_hide_state_iso2` / `checkout_hide_state_name`. |
| City | text | Required | Mapped to `locality` payload key for validation. |
| Street | text | Required (per settings) | Conditional from `checkout_hide_street_name`. |
| Street number | text | Required (per settings) | Conditional from `checkout_hide_street_number`. |
| City postal code | text | Required | Min 2 chars when `post_code_not_required` is ON, else min 3. |
| Additional address info | text (full-width row) | Optional (or Required per `checkout_hide_additional_information`) | Apartment / suite / instructions. |
| Phone | country-code phone (full-width row) | Required (per settings) | Validated by libphonenumber against country.iso2; auto-reformatted to E.164 on save — see [[customer-shipping-address-save-hooks]]. |

For the conditional required / optional / hidden rules per checkout setting, see [[customer-shipping-address-validation]].

### 3) Company details card — HIDDEN on shipping

Only appears when the modal opens in `addressType === 'billing'`. See [[customers-details-billing-addresses]].

## Business rules

### Same modal handles Add + Edit (mode picked by `address` prop)

The component `CustomersAddressModal` is one component used twice. The title swaps between "Add address" and "Edit address" based on whether `address.id` is present. When opened from the [[customers-details]] sidebar, the prop omission defaults `addressType='shipping'`.

### Watcher resets form on close (no leak between opens)

Closing the modal without saving resets the form back to the loaded address's values + clears validation errors. So re-opening on a different row doesn't carry stale data from the previous edit.

### Save handler routes

- POST `/admin/api/core/customers/shipping-address` (create).
- PATCH `/admin/api/core/customers/shipping-address/{id}` (edit).
- Both under `hasApiPermission:customers` middleware.

### Save effects

- Toast on success: *"Address has been saved successfully"*.
- 422 validation errors are surfaced field-by-field via the central error store.
- On success: closes modal, refetches the address list AND the [[customers-details]] Default address sidebar card.

### Side effects (post-save)

Every save runs the four save-time hooks documented on [[customer-shipping-address-save-hooks]] — phone E.164 normalisation, lat/lng auto-fill, country ISO normalisation, and the heavy courier-mapping regeneration across every active courier via OmniShip. This is a side effect of saving — not visible in the modal, but worth knowing about for support tickets like *"why does saving an address take 3 seconds?"*.

### First-added auto-promotes to default

When the customer has zero shipping addresses and the merchant saves the first one, the platform sets that address as the customer's default. Subsequent saves do NOT auto-promote. See [[customer-shipping-address-defaults]].

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-list]] — the table that triggers this modal.
- [[customer-shipping-address-google-maps]] — autocomplete + interactive-map mechanics inside the Address card.
- [[customer-shipping-address-validation]] — which fields are required vs optional per store settings.
- [[customer-shipping-address-save-hooks]] — what runs after the merchant clicks Save.
- [[customer-shipping-address-defaults]] — first-added auto-promotion + "Set as default".
- [[customers-details]] — the Default address sidebar that re-uses this modal.
- [[customers-details-billing-addresses]] — sister modal in `billing` mode with Company details exposed.
- [[settings-cart]] — Google Maps API key + `checkout_hide_*` settings.

## Open questions

None.
