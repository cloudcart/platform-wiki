---
type: feature
nav_path: "Customers → Customer details → Billing addresses → List"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Customer billing addresses list", "Billing address table", "Billing addresses bulk delete"]
tags: [customers, addresses, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (modal, company fields, VIES, defaults, save hooks, storage, API).

# Customer billing addresses — List view

## Purpose

The list table on the Billing addresses tab — the merchant's read-and-act view across every billing address saved for one customer. It also surfaces the **Add address** entry point and the bulk **Delete** action.

## Where to find it

From [[customers-details]] → **Billing addresses** tab. The whole tab content is the list and its modal triggers.

## What the merchant can do here

- Browse every saved billing address for the customer in a paginated table.
- Sort by ID (descending — newest first).
- Filter by **Is company address** (Yes / No) — the only built-in filter.
- Click the **Address column** value on any row → opens the Edit modal pre-populated. See [[customer-billing-address-modal]].
- Click **Set as default** in the **Type** column of a non-default row → promotes that row to the default billing. See [[customer-billing-address-defaults]].
- Click **+ Add address** in the header → opens the Add modal. See [[customer-billing-address-modal]].
- Select rows + **Delete** (bulk action) → confirmation dialog → permanent removal of selected rows.

### What the merchant CANNOT do here

- Edit a single field of an address (e.g. just the VAT) without re-opening the modal and re-saving the whole form.
- Filter or search by company name / VAT / city — only the Is-company-address filter is exposed.
- Delete the customer's current default billing in any way (single or bulk) — see [[customer-billing-address-defaults]] for the hard guard.

## Settings & fields

### Per-row columns

| Column | Content |
|--------|---------|
| **Region** | Country / state summary derived from the address. |
| **Address** | Street + street number + city. The cell is clickable — opens the Edit modal. |
| **Post code** | The post / ZIP code. |
| **Phone** | E.164-normalised phone. |
| **Type** | Either the **Default** badge (when the row matches the customer's `default_billing_address_id`) or the **Set as default** button. |

Sort: ID descending. Filter: **Is company address** Yes / No.

### Header actions

- **+ Add address** — opens the Add modal (xl-sized). See [[customer-billing-address-modal]].

### Bulk actions

| Action | What it does |
|--------|--------------|
| **Delete** | Confirmation: *"Are you sure you want to delete? This action cannot be undone."* Permanent. Fails the whole batch if any selected id is the customer's current default billing or if any id is missing — see Business rules below. |

## Business rules

- **Default badge is computed, not stored.** The list does not read an `is_default` flag from the address row — it compares each row id to the customer's `default_billing_address_id` pointer. Setting a new default re-renders the badges without changing the address rows. See [[customer-billing-address-defaults]] + [[customer-billing-address-storage]].
- **Bulk delete is strict on missing ids.** The DELETE call to `/admin/api/core/customers/billing-address` validates every id in the payload against the actual billing-address table. Any non-existent id fails the entire request — the platform does NOT silently skip invalid ids.
- **Bulk delete is strict on the current default.** If any id in the bulk matches the customer's `default_billing_address_id`, the request is rejected with HTTP 422 *"Cannot delete customer default billing address."* and no rows are deleted (even the valid ones). The merchant must promote a different billing address first. See [[customer-billing-address-defaults]].
- **Deletion does NOT cascade to past orders.** The invoice on a past order keeps its snapshot of the billing address even after the row is deleted here. See [[customer-billing-address-storage]].

### Permission

Standard `customers` permission scope. The list and its actions are protected by `hasApiPermission:customers` middleware.

## Programmatic access

The list is also readable via JSON-API v2 — see [[customer-billing-address-api]] for filtering, sorting, pagination, and the matching delete protection.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-modal]] — the modal that opens from the Add / Edit triggers in this list.
- [[customer-billing-address-defaults]] — the Set-as-default action surfaced in the Type column and the delete-protection of the default.
- [[customers-details]] — parent details page; the Default address sidebar card reads from here.

## Open questions

None.
