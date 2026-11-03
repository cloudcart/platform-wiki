---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → List view"
route_name: customers-shipping-addresses
route_path: /admin/customers/details/:id/shipping-addresses
aliases: ["Customer shipping addresses list", "Shipping address list table", "Shipping address bulk delete"]
tags: [customers, addresses, shipping, list]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (modal, Google Maps, defaults, save-hooks, storage, validation, API).

# Customer shipping addresses — List view

## Purpose

The paginated table that renders every shipping address saved on one customer record. This aspect covers the **list table itself** — its columns, sort order, search, the company-address filter, the per-row actions, and the bulk-delete confirmation. The Add / Edit panel opened from this table is documented separately on [[customer-shipping-address-modal]].

## Where to find it

From [[customers-details]] → **Shipping addresses** tab. The route is `/admin/customers/details/:id/shipping-addresses`.

## What the merchant can do here

### List table

- See all of the customer's saved shipping addresses in a paginated table.
- Click any row's **Address** cell to open the Edit panel pre-populated — see [[customer-shipping-address-modal]].
- Click the **Set as default** action on a non-default row to make it the new default — see [[customer-shipping-address-defaults]].
- Click + **Add address** (top-right) to open the Add panel — see [[customer-shipping-address-modal]].
- Tick rows and open **Tools** for the bulk delete (with confirmation).
- Search with the *"Search and Filter"* box: country, state, city, street, office name, post code, phone, first name, last name and more.

### Sort

Sort is fixed: by ID descending (newest first). The merchant cannot change sort from the UI.

### Filter

| Filter | Options |
|---|---|
| **Is Company address** | Yes / No. **Yes** means the address has a company name, which this tab's panel does not set. |

### Bulk actions

| Action | What it does |
|---|---|
| **Delete** | Confirmation titled *"Delete"*: *"Are you are sure you want to delete? Caution: This action cannot be undone."*, with **No** and a red **Yes**. Permanent. |

(No bulk Set Default — default is per-row only.)

### What the merchant CANNOT do here

- Add an address from a customer-side **billing** address — separate per-type list. See [[customers-details-billing-addresses]].
- Toggle "ship to another address vs same as billing" — customer-side checkout-time flag, not stored on the address record.
- Change the sort order from the table header.

## Settings & fields

### Per-row columns

| Column | Notes |
|---|---|
| **Region** | Country, with the state below it. |
| **Address** | Street, street number, city, country. For an office or locker: its icon and name. Click → Edit panel — see [[customer-shipping-address-modal]]. |
| **Post code** | The postal / ZIP code. |
| **Phone** | Recipient phone (stored in E.164 — see [[customer-shipping-address-save-hooks]]). *N/A* when empty. |
| **Type** | "Default" pill badge (style `cc-tag-status--update`) on the default row, OR a "Set as default" action button on every other row. The "is default?" comparison runs against the customer's `default_address_id` pointer at read time — see [[customer-shipping-address-defaults]] + [[customer-shipping-address-storage]]. |

## Business rules

### Pickup-point + marketplace addresses appear in the list too

The customer's saved-addresses list shows BOTH real street addresses AND pickup-point addresses (courier offices, lockers, marketplace pickups) — they share the same underlying table with the `office_id` + `integration` or `marketplace_id` discriminators. An office or locker row opens in the panel on its courier and office; see [[customer-shipping-address-pickup-point]]. See [[customer-shipping-address-storage]] for the discriminator scheme.

### Click-target is the Address column

The clickable area for opening the Edit panel is the **Address** cell on each row — not the whole row. This avoids accidental edits when the merchant just wants to bulk-select.

### Bulk Delete validates every ID

Bulk delete validates every ID against the actual shipping-address table — any non-existent ID fails the entire batch. The customer's current default can be in the selection; see [[customer-shipping-address-defaults]].

### Set-as-default updates the Default address card

The "Set as default" action triggers a toast *"Default address updated"* and the [[customers-details]] Default address card switches to that address. See [[customer-shipping-address-defaults]] for the customer-pointer mechanics.

### Side effects

- **Bulk Delete** triggers a toast *"Deleted successfully"* (or *"Error while deleting"*), removes the rows and refreshes the Default address card.
- **Set as default** triggers a toast *"Default address updated"* and swaps the Default badge in the table — see [[customer-shipping-address-defaults]].

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customers-details]] — parent details page; the Default address card refreshes on actions here.
- [[customer-shipping-address-modal]] — the Add / Edit panel opened from this list.
- [[customer-shipping-address-pickup-point]] — office and locker rows.
- [[customer-shipping-address-defaults]] — "Set as default" mechanics.
- [[customer-shipping-address-storage]] — pickup-point + marketplace discriminators.
- [[customers-details-billing-addresses]] — sister list for billing addresses.

## Open questions

None.
