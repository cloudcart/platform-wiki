---
type: feature
nav_path: "Customers → Customer details → Billing addresses → List"
route_name: customers-billing-addresses
route_path: /admin/customers/details/:id/billing-addresses
aliases: ["Customer billing addresses list", "Billing address table", "Billing addresses bulk delete"]
tags: [customers, addresses, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (panel, company fields, VIES, defaults, save hooks, storage, API).

# Customer billing addresses — List view

## Purpose

The list table on the Billing addresses tab — the merchant's read-and-act view across every billing address saved for one customer. It also surfaces the **Add address** entry point and the bulk **Delete** action.

## Where to find it

From [[customers-details]] → **Billing addresses** tab. The whole tab content is the list and what opens from it.

## What the merchant can do here

- Browse every saved billing address for the customer in a paginated table.
- Sort by ID (descending — newest first).
- Filter by **Is Company address** (Yes / No): **Yes** means the address has a company name.
- Click the **Address column** value on any row → opens the Edit panel pre-populated. See [[customer-billing-address-modal]].
- Click **Set as default** in the **Type** column of a non-default row → promotes that row to the default billing. See [[customer-billing-address-defaults]].
- Click **+ Add address** in the header → opens the Add panel. See [[customer-billing-address-modal]].
- Tick rows and open **Tools** → **Delete** → confirmation → permanent removal of selected rows.

### What the merchant CANNOT do here

- Edit a single field of an address (e.g. just the VAT) without re-opening the panel and re-saving the whole form.
- Find a row by typing in the *"Search and Filter"* box: a text search on this tab ends in an error message (verify). Use the **Is Company address** filter.

## Settings & fields

### Per-row columns

| Column | Content |
|--------|---------|
| **Region** | Country, with the state below it. |
| **Address** | Street, street number, city, country. The cell is clickable — opens the Edit panel. |
| **Post code** | The post / ZIP code. |
| **Phone** | E.164-normalised phone. *N/A* when empty. |
| **Type** | Either the **Default** badge (when the row matches the customer's `default_billing_address_id`) or the **Set as default** button. |

Sort: ID descending. Filter: **Is company address** Yes / No.

### Header actions

- **+ Add address** — opens the Add panel. See [[customer-billing-address-modal]].

### Bulk actions

| Action | What it does |
|--------|--------------|
| **Delete** | Under **Tools**. Confirmation titled *"Delete"*: *"Are you are sure you want to delete? Caution: This action cannot be undone."*, with **No** and a red **Yes**. Toast: *"Deleted successfully"* (or *"Error while deleting"*). Permanent. |

## Business rules

- **Default badge is computed, not stored.** The list does not read an `is_default` flag from the address row — it compares each row id to the customer's `default_billing_address_id` pointer. Setting a new default swaps the badges without changing the address rows. See [[customer-billing-address-defaults]] + [[customer-billing-address-storage]].
- **Bulk delete is strict on missing ids.** The DELETE call to `/admin/api/core/customers/billing-address` validates every id in the payload against the actual billing-address table. Any non-existent id fails the entire request — the platform does NOT silently skip invalid ids.
- **The current default can be deleted.** It can be in the selection; the customer then has no default billing address. See [[customer-billing-address-defaults]].
- **Deletion does NOT cascade to past orders.** The invoice on a past order keeps its snapshot of the billing address even after the row is deleted here. See [[customer-billing-address-storage]].

### Permission

Standard `customers` permission scope. The list and its actions are protected by `hasApiPermission:customers` middleware.

## Programmatic access

The list is also readable via JSON-API v2 — see [[customer-billing-address-api]] for filtering, sorting, pagination, and its refusal to delete the default.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-modal]] — the panel that opens from the Add / Edit triggers in this list.
- [[customer-billing-address-defaults]] — the Set-as-default action surfaced in the Type column.
- [[customers-details]] — parent details page.

## Open questions

None.
