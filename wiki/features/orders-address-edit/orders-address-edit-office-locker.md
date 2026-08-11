---
type: feature
nav_path: "Orders → Order details → Address → Office / Locker"
route_name: admin.orders.address.office.edit
route_path: /admin/orders/address/shipping/{order_id}/edit (office radio) + /admin/orders/address/office/{order_id}
aliases: ["Office pickup", "Locker pickup", "Courier office", "Parcel locker", "BoxNow locker", "Econt office", "Speedy depot", "EuShipment external_id", "Shipping method radio"]
tags: [orders, address, office, locker, courier, shipping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[orders-address-edit]]. See the hub for related aspects (flows, form fields, propagation, side effects).

# Order address — Office / Locker selection

## Purpose

When the courier integration supports it, the merchant can swap the order's shipping destination from a home address to a courier OFFICE or parcel LOCKER. This page covers the shipping-method radio row, the courier-specific picker behaviour, and the special handling for the BoxNow and EuShipment integrations.

## Where to find it

Two paths reach office / locker selection:

1. **Through Panel A's shipping-method radio row** — when the merchant opens Edit shipping address ([[orders-address-edit-flows]]), the top of the form has up to three radios (Address / Office / Locker). Picking Office or Locker switches the form to the picker mode. This is the dominant flow.
2. **Through the dedicated Office submenu entry** — `admin.orders.address.office.edit`. This opens Panel C, which is a thin wrapper around the standard address `_form.tpl`. See [[orders-address-edit-form-fields]].

Office / Locker is **shipping-only**. Billing addresses have no concept of courier office.

## What the merchant can do here

### Shipping-method radio row (Panel A)

When the order's courier registers an `apps.<courier>.offices` and / or `apps.<courier>.lockers` route, the Edit form shows up to three radios at the top:

| Radio | Label | Visible when | Selected when |
|-------|-------|--------------|---------------|
| **address** | "Ship to address" | All couriers EXCEPT BoxNow | The order has no office linkage. |
| **office** | "Ship to office" | Courier registers `apps.<courier>.offices` | The order has an office linkage AND it is NOT a locker. |
| **locker** | "Ship to locker" | Courier registers `apps.<courier>.lockers` | The order has an office linkage AND it is flagged as a locker. |

For BoxNow specifically, the **address** radio is HIDDEN — BoxNow is locker-only and doesn't support home delivery. For couriers without any office / locker support, the radio row doesn't render at all and the form is plain address.

### Picking a radio

- Picking **address** swaps the form's action back to the standard `admin.orders.address.shipping.edit` route, shows the standard address-fields block, and hides the office / locker blocks.
- Picking **office** swaps the form's action to `apps.<courier>.changePickup?type=office&provider_id=<id>`, shows the office picker + recipient name + phone, and hides the other blocks.
- Picking **locker** swaps the form's action to `apps.<courier>.changePickup?type=locker&provider_id=<id>`, shows the locker picker + recipient name + phone, and hides the other blocks.

### Picker behaviour (live, per-courier)

The picker is a Select2 AJAX-loaded dropdown:

- Each query goes through the courier app's `apps.<courier>.offices` / `apps.<courier>.lockers` autocomplete route, which calls the courier's own API directly.
- Each option shows: office / locker name, full address, working hours (when the courier returns them).
- Placeholders use the Bulgarian strings *"Изберете офис"* / *"Изберете автомат"* — these are NOT localised at present.
- After picking, the platform sets a hidden "office name" input and the form is ready to save.

## Settings & fields

### Picker fields

See [[orders-address-edit-form-fields]] for the Office / Locker picker field block (Office name, First name, Last name, Phone).

### Courier integration prerequisites

The radio options are visibility-gated by route registration:

- The courier app must register `apps.<courier>.offices` for the Office radio to appear.
- The courier app must register `apps.<courier>.lockers` for the Locker radio to appear.

Without the courier app installed (or with the relevant route not registered), the merchant only sees the standard Address option.

### EuShipment `external_id` extraction

The EuShipment courier integration is special — the form parses the integration string in the `eushipment_<id>` format and extracts the `<id>` as `external_id`, which is then passed as a query parameter on the picker AJAX call. This routes the office / locker list to the correct sub-courier within EuShipment's aggregator-style integration.

### BoxNow special handling

BoxNow is locker-only. The address radio is hidden. The merchant cannot ship a BoxNow order to a home address — the only valid choice is a locker.

## Business rules

### Shipping method switch may invalidate the waybill

Changing shipping method (Address → Office, Office → Locker, etc.) may trigger:

- Courier recalculation (different shipping cost — see [[orders-address-edit-side-effects]]).
- If a waybill is already generated: the merchant typically must void via [[orders-shipping-waybill]] and regenerate, because the waybill points at the old destination type.

The platform does NOT auto-void the waybill on a shipping-method change — the merchant must do it manually before editing.

### Office / locker list is fetched live, no cache

Each query through the courier app's office / locker autocomplete routes calls the courier's API directly. The platform does NOT cache the office list between requests — so the merchant always sees the courier's current active offices / lockers, including new openings and closures. The trade-off: the dropdown is slower than a cached pick-list (network round-trip on every search), but always fresh.

### Panel C (Office submenu) is a thin wrapper

Panel C is reached via the explicit "Office" submenu link (`admin.orders.address.office.edit`) — distinct from Panel A's office radio. This panel re-uses the same standard address `_form.tpl` include, NOT a dedicated office picker. So the merchant filling in the Office panel gets the regular address-form layout, with the OFFICE picker exposed through the regular Country / City / etc fields. (This is a template artefact — for actual office picking, Panel A's office-radio path is the dominant flow.) The action URL is `admin.orders.address.office.edit/<order_id>`, which writes the same address record but is reached via the Office menu entry.

### Office address overwrites the home address

When the merchant picks an office or locker and saves, the platform OVERWRITES the order's shipping address fields with the office / locker's address (street, city, postal code). The original home address on the order is gone — the merchant cannot toggle Office → Address and get the original home address back automatically; they must re-type it or use Change to pull a saved one.

### Shipping address swap re-applies courier mapping

When the merchant uses Change (Panel B) to swap shipping addresses, the platform also re-applies courier-specific country / city mapping. So if the merchant has both an Econt-mapped and a Speedy-mapped version of a city saved on the customer's profile, the swap picks the mapping matching the order's current courier integration. The quarter field is always wiped on swap to force re-resolution.

## Related

- [[orders-address-edit]] — hub.
- [[orders-address-edit-flows]] — Office / Locker entry-point matrix.
- [[orders-address-edit-form-fields]] — picker field inventory.
- [[orders-address-edit-side-effects]] — what happens on save (courier re-quote, waybill warning).
- [[orders-shipping-waybill]] — must void manually before changing shipping method.
- [[apps]] — courier integrations register the relevant routes.

## Open questions

- **Verify** — does the Office / Locker picker support search by postal code on every courier, or only Econt? The placeholder text suggests city / area search by name only.
- **Verify** — when EuShipment routes to a sub-courier that itself has no `external_id` (legacy integration), does the picker fall back to the parent EuShipment list, or fail silently?
