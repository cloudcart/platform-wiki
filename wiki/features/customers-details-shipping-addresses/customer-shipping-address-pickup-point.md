---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Add / Edit panel → Delivery to"
route_name: customers-shipping-addresses
route_path: /admin/customers/details/:id/shipping-addresses
aliases: ["Customer address courier office", "Customer address locker", "Deliver to office", "Deliver to locker", "Deliver to address", "Delivery to", "Save courier office on customer", "Адрес до офис на куриер", "Адрес до автомат"]
tags: [customers, addresses, shipping, couriers]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, panel, Google Maps, defaults, save-hooks, storage, validation, API).

# Customer shipping addresses — Delivery to an office or locker

## Purpose

A saved shipping address can point at a courier's office or locker instead of a street. The merchant sets this in the same [[customer-shipping-address-modal|Add / Edit panel]], through the **Delivery to** choice. This aspect covers when that choice shows, the form behind it, and what the platform fills in from the courier.

## Where to find it

[[customers-details]] → **Shipping addresses** tab → **+ Add address**, or click a row's **Address** cell → **Delivery to** card.

The card shows when the store has an active courier whose app offers offices or lockers. The Billing addresses tab has no such card.

## What the merchant can do here

- Choose **Deliver to address**, **Deliver to office** or **Deliver to locker**. Only the types an active courier offers appear.
- Pick the courier, then its office or locker.
- Change a saved office or locker: the row opens on its current courier and office.
- Turn a pickup address back into a street address with **Deliver to address**.

## Settings & fields

Choosing office or locker replaces the Address card with a card headed **Courier office** or **Locker**. The **Customer information** card stays.

| Field | Type | Rules |
|---|---|---|
| **Courier** | Dropdown | Active couriers offering that delivery type. Required. |
| **Office** / **Locker** | Searchable dropdown | Disabled until a courier is chosen. Search starts at 2 characters. Required. |
| **Phone** | Country-code phone input | Optional, max 191 chars. |

First name and last name are optional here, max 191 chars each.

## Business rules

### The picker starts over

Changing the courier clears the office. Switching between office and locker clears the picked point, and clears the courier too if it does not offer the new type.

### The location comes from the courier

Only the name, phone, courier and office travel with the save. The platform fills the country, city, post code and map coordinates from the courier's office record. The office's stored name reads *Name (address)*. See [[customer-shipping-address-storage]] for the `office_id` + `integration` scheme, and for `office_type` (1 for a locker, 0 for an office).

### Switching back to a street address

Saving with **Deliver to address** removes the courier and office from the address, and the usual address rules apply; see [[customer-shipping-address-validation]].

### Where it shows

In the list, the **Address** cell shows an office or locker icon with the office name. See [[customer-shipping-address-list]].

### Saves

The toast is *"Address has been saved successfully"*, as for any address. The [[customer-shipping-address-save-hooks]] apply, with the office-address skip rule described there.

### When the courier list cannot load

The panel then shows the plain address form, with no **Delivery to** card.

## Programmatic access

Office addresses can be created, read and deleted through JSON-API v2. See [[customer-shipping-address-api]].

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-modal]] — the panel that holds this form.
- [[customer-shipping-address-storage]] — how pickup addresses are stored.
- [[customer-shipping-address-list]] — how they show in the table.

## Open questions

None.
