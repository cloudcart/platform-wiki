---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → List view"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping addresses list", "Shipping address list table", "Shipping address bulk delete"]
tags: [customers, addresses, shipping, list]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (modal, Google Maps, defaults, save-hooks, storage, validation, API).

# Customer shipping addresses — List view

## Purpose

The paginated table that renders every shipping address saved on one customer record. This aspect covers the **list table itself** — its columns, sort order, the company-address filter, the per-row actions, and the bulk-delete confirmation. The Add / Edit modal triggered from this table is documented separately on [[customer-shipping-address-modal]].

## Where to find it

From [[customers-details]] → **Shipping addresses** tab. The route is `/admin/customers-new/details/:id/shipping-addresses`.

## What the merchant can do here

### List table

- See all of the customer's saved shipping addresses in a paginated table.
- Click any row's **Address** cell to open the Edit modal pre-populated — see [[customer-shipping-address-modal]].
- Click the **Set as default** action on a non-default row to make it the new default — see [[customer-shipping-address-defaults]].
- Click + **Add address** (top-right) to open the Create modal — see [[customer-shipping-address-modal]].
- Bulk-select rows via checkboxes for bulk delete (with confirmation).

### Sort

Sort is fixed: by ID descending (newest first). The merchant cannot change sort from the UI.

### Filter

| Filter | Options |
|---|---|
| **Is Company address** | Yes / No. (Company-flag is typically a billing concept, but the shipping list still exposes the filter — verify whether some shipping addresses can carry a company flag.) `(verify)` |

### Bulk actions

| Action | What it does |
|---|---|
| **Delete** | Confirmation: *"Are you sure you want to delete? This action cannot be undone."* Permanent. Whole-batch protection applies (see Business rules). |

(No bulk Set Default — default is per-row only.)

### What the merchant CANNOT do here

- Add an address from a customer-side **billing** address — separate per-type list. See [[customers-details-billing-addresses]].
- Toggle "ship to another address vs same as billing" — customer-side checkout-time flag, not stored on the address record.
- Change the sort order or the per-page count from the table header.

## Settings & fields

### Per-row columns

| Column | Notes |
|---|---|
| **Region** | Country + state combined display (custom rendering component). |
| **Address** | Street + street number + city. Click → Edit modal — see [[customer-shipping-address-modal]]. |
| **Post code** | The postal / ZIP code. |
| **Phone** | Recipient phone (stored in E.164 — see [[customer-shipping-address-save-hooks]]). |
| **Type** | "Default" pill badge (style `cc-tag-status--update`) on the default row, OR a "Set as default" action button on every other row. The "is default?" comparison runs against the customer's `default_address_id` pointer at read time — see [[customer-shipping-address-defaults]] + [[customer-shipping-address-storage]]. |

### Filter

| Filter | Options |
|---|---|
| **Is Company address** | Yes / No. |

## Business rules

### Pickup-point + marketplace addresses appear in the list too

The customer's saved-addresses list shows BOTH real street addresses AND pickup-point addresses (courier offices, marketplace lockers) — they share the same underlying table with the `office_id` + `integration` (Speedy office, Econt office, etc.) or `marketplace_id` discriminators. Office addresses cannot be edited with arbitrary geo data — they're tied to the courier's office record. See [[customer-shipping-address-storage]] for the discriminator scheme and the `realAddress` query scope.

### Click-target is the Address column

The clickable area for opening the Edit modal is the **Address** cell on each row — not the whole row. This avoids accidental edits when the merchant just wants to bulk-select.

### Bulk Delete validates every ID

Bulk delete validates every ID against the actual shipping-address table — any non-existent ID fails the entire batch. The validator also rejects the whole batch if **any** ID matches the customer's current default — single-row default deletion needs a promote-then-delete pattern (see [[customer-shipping-address-defaults]]).

### Set-as-default refreshes the parent details sidebar

The "Set as default" action triggers a toast *"Default address updated"* and refetches the [[customers-details]] Default address sidebar card. See [[customer-shipping-address-defaults]] for the customer-pointer mechanics.

### Side effects

- **Bulk Delete** triggers a toast *"Deleted successfully"* (or *"Error while deleting"*) and refetches the table + sidebar.
- **Set as default** triggers a toast *"Default address updated"* and refetches the table + sidebar — see [[customer-shipping-address-defaults]].

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customers-details]] — parent details page; Default address sidebar refreshes on actions here.
- [[customer-shipping-address-modal]] — the Add / Edit modal opened from this list.
- [[customer-shipping-address-defaults]] — "Set as default" mechanics + delete protection.
- [[customer-shipping-address-storage]] — pickup-point + marketplace discriminators.
- [[customers-details-billing-addresses]] — sister list for billing addresses.

## Open questions

- Is the **Is Company address** filter on the shipping list usable in practice, or is the company flag always 0 here because it's a billing-only concept? `(verify)`
