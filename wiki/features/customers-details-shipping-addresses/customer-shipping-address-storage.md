---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Storage model"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping address storage", "Shipping address table model", "Pickup-point office_id discriminator", "Marketplace_id address discriminator", "Address order snapshot", "setAddressFromOrder re-sync"]
tags: [customers, addresses, shipping, storage]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, modal, Google Maps, defaults, save-hooks, validation, API).

# Customer shipping addresses — Storage model

## Purpose

This aspect documents the **persistence layer** behind the shipping-addresses list: where rows live, how "default" is represented (a customer-level pointer, NOT an address-level flag), how the same table holds real street addresses **plus** pickup-point and marketplace addresses through discriminator columns, the `realAddress` query scope that filters them apart, and the per-order snapshot decoupling that protects past-order data from later address edits or deletes.

Knowing this model is what makes the rest of the cluster make sense — particularly default-pointer semantics ([[customer-shipping-address-defaults]]) and why deletion doesn't cascade.

## Where to find it

The storage model is not directly visible in the admin UI. It shows up indirectly:

- "Set as default" updates a column on the customer row, not the address row — see [[customer-shipping-address-defaults]].
- Pickup-point + marketplace addresses appear in the same list as real street addresses — see [[customer-shipping-address-list]].
- Editing a saved address does NOT change addresses already attached to past orders — they keep their snapshot.

## What the merchant can do here

- See pickup-point (office) addresses and marketplace addresses in the same list as real street addresses.
- Delete an address knowing past orders remain unaffected (they keep their order-time snapshot).
- Edit a saved address and have only FUTURE orders pick up the new values.

### What the merchant CANNOT do here

- Update an address ON a past order by editing the customer's saved address — past orders carry their own snapshot. To change a past order's address, the merchant edits ON the order page (see [[orders-details]]).
- Edit an office / pickup-point address's geo coordinates — those addresses are tied to the courier's office record (the `office_id` discriminator). Allowed: deletion. Not allowed: arbitrary geo edits.
- Reuse a deleted address on a new order — once deleted from the customer's saved list, it's gone for future use even if past orders still reference its snapshot.

## Settings & fields

### Address row columns (relevant subset)

| Column | Purpose |
|---|---|
| `id` | Primary key. |
| `customer_id` | Owner. |
| `first_name`, `last_name`, `phone`, `country_iso2`, `country_iso3`, `country_name`, `state`, `city_name`, `street_name`, `street_number`, `post_code`, `additional_address_info`, `latitude`, `longitude`, `text` | Address content. |
| `office_id` | Discriminator: when populated, this is a **pickup-point** address tied to a courier office. |
| `integration` | The courier name owning the office (Speedy, Econt, etc.) — populated alongside `office_id`. |
| `marketplace_id` | Discriminator: when populated, this is a **marketplace pickup** address (e.g., Glovo). |

### Customer row pointers (NOT on the address row)

| Pointer | Purpose |
|---|---|
| `default_address_id` | The customer's default SHIPPING address. |
| `default_billing_address_id` | The customer's default BILLING address. |

See [[customer-shipping-address-defaults]] for how the pointer is updated.

### Query scope

`realAddress` — a query scope that filters to non-office, non-marketplace rows (i.e., `office_id IS NULL` AND `marketplace_id IS NULL`). Used when only street addresses are wanted.

## Business rules

### Default is a pointer, NOT a flag

The address row has no `is_default` column. "Is this the default?" is computed at read time by comparing `customer.default_address_id` to `address.id`. The list table's Type column does this comparison per row. See [[customer-shipping-address-defaults]] for promotion mechanics.

### Pickup-point addresses share the same table

When a customer at checkout selects a courier's office / pickup point (Speedy office, Econt office, etc.), the platform creates a **second** shipping address record with `office_id` filled in and `integration` set to the courier name. This is distinct from a real street address.

The customer's saved-addresses list shows BOTH types — real street addresses (no `office_id`) and office pickup-point addresses (with `office_id` + `integration`).

Office addresses cannot be edited with arbitrary geo data — they're tied to the courier's office record. Deletion is allowed; the courier-mapping regeneration hook (see [[customer-shipping-address-save-hooks]]) does NOT run on office addresses.

### Marketplace addresses share the same table too

Similar to office addresses, marketplace pickup addresses (when the merchant integrates marketplace pickup like Glovo) live in this same table with `marketplace_id` populated.

### `realAddress` scope filters to street addresses only

When the platform needs only real street addresses (e.g., for a list of addresses where geocoding makes sense, or for a default-address picker that excludes pickup points), the `realAddress` scope filters out rows with `office_id` or `marketplace_id` populated.

### Order placement snapshots the address

When an order is placed, the platform **copies** the address into the order's own shipping-address snapshot table. Editing or deleting the saved address afterwards has no effect on past orders — they read from their snapshot.

Practical consequence: a customer who moves house and updates their default shipping address does NOT retroactively change the delivery target on past orders. The Old Order still has the old address; the New Order will use the new address.

### Reverse path: `setAddressFromOrder`

The platform has a method (`setAddressFromOrder`) that takes an order's shipping snapshot and updates the customer's saved shipping address from those values. So when an admin edits the address ON the order detail page, the customer's saved shipping address CAN be re-synced from the order snapshot. Path-dependent — `(verify)` exactly which UI invokes this; the merchant should not assume edits to the order address always flow back.

### Side effects

- **First save** for a customer with zero addresses promotes the new address to default (sets `customer.default_address_id` — see [[customer-shipping-address-defaults]]).
- **Delete** of a non-default address removes the row but past orders retain their snapshots.
- **Delete** of the current default is rejected with HTTP 422 — see [[customer-shipping-address-defaults]] for the protection rule.
- **Save** (insert OR update) on a non-office address triggers the courier-mapping regeneration — see [[customer-shipping-address-save-hooks]].

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-defaults]] — the customer-level pointer rules + delete protection.
- [[customer-shipping-address-list]] — the table that surfaces pickup-point + marketplace addresses alongside real ones.
- [[customer-shipping-address-save-hooks]] — what runs on save (including the office-address skip).
- [[customer-shipping-address-api]] — JSON-API v2 endpoints that respect the same storage rules.
- [[orders-details]] — the order detail page where address edits may trigger `setAddressFromOrder` re-sync.
- [[customer]] — entity page carrying the `default_address_id` pointer.

## Open questions

- Exactly which UI / API path invokes `setAddressFromOrder` — is it only the admin order-detail address edit, or also customer-storefront flows? `(verify)`
