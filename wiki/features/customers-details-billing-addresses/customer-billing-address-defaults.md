---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Default billing"
route_name: customers-billing-addresses
route_path: /admin/customers/details/:id/billing-addresses
aliases: ["Default billing address", "Set as default billing", "default_billing_address_id", "Delete default billing address"]
tags: [customers, addresses, billing, defaults]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, company fields, VIES, save hooks, storage, API).

# Customer billing address — Default management

## Purpose

The rules around **which one** of a customer's billing addresses is the default — the address the platform uses when rendering invoices for a new order placed without an explicit override. A customer can have unlimited billing addresses and one default at a time; this aspect documents how that default is set and changed, and what deleting it does.

## Where to find it

- The current default is indicated by the **Default** badge in the **Type** column of the list (see [[customer-billing-address-list]]).
- Non-default rows show a **Set as default** button in the same column.
- The customer's [[customers-details]] page has a Default address card. That card follows the **shipping** default. The billing default shows through the badge on this tab.

## What the merchant can do here

- Click **Set as default** on any non-default billing row → promotes that address to default.
- Add the customer's first billing address → it auto-promotes to default with no merchant action.
- Add or edit a different billing address without touching the default — adds beyond the first do NOT auto-promote.
- Delete any billing address, including the current default.

### What the merchant CANNOT do here

- Clear "default" while keeping the address — there is no "unset default" action. Promoting a different address unsets the previous default as a side effect.
- Set the same address as both default shipping and default billing — they live in separate lists and on separate customer columns.

## Settings & fields

| Customer column | What it points to | Independence |
|------------------|--------------------|--------------|
| `default_billing_address_id` | The current default **billing** address row ID. | Independent from `default_address_id` (shipping). |
| `default_address_id` | The current default **shipping** address row ID. | Independent from `default_billing_address_id`. |

The address row itself carries NO `is_default` flag — default is computed by comparing the customer pointer to the row id at read time.

## Business rules

### One default per customer

A customer has at most one default billing address. The rules:

- **First-added billing auto-promotes.** When the customer has zero billing addresses and the merchant (or API) adds one, the platform automatically sets `default_billing_address_id` to that row. The merchant does NOT need to click "Set as default" on the first one.
- **Subsequent adds do NOT auto-promote.** The newly added row sits in the list with a "Set as default" button until the merchant promotes it.
- **Set as default** updates the customer pointer; the previous default's badge disappears and the new row's badge appears. The address rows themselves are not touched.

### Deleting the current default

The list allows deleting the customer's current default billing address, alone or in a bulk selection. The customer then has no default billing address, and the remaining rows all show **Set as default**. The merchant picks a new default there.

JSON-API v2 works differently: a delete of the current default is rejected with HTTP 422 *"Cannot delete customer default billing address."* See [[customer-billing-address-api]].

### Independent from default shipping

The customer record has TWO independent default fields: `default_address_id` (shipping) and `default_billing_address_id` (billing). Setting a new default on one tab has zero effect on the other:

- Promote billing-default to row X → `default_address_id` (shipping) is untouched.
- Promote shipping-default to row Y → `default_billing_address_id` is untouched.

The two are stored as separate columns on the customer row. See [[customer-billing-address-storage]].

### Set-as-default action mechanics

- **Trigger:** clicking **"Set as default"** in the **Type** column on a non-default row.
- **Endpoint:** `POST /admin/api/core/customers/billing-address/default/{customer_id}` with body `{address_id}`.
- **Permission:** `hasApiPermission:customers`.
- **Per-row spinner** while pending.
- **Success toast:** *"Default address updated"*.
- **Side effect:** the badge and button swap in the list. The [[customers-details]] Default address card stays on the shipping default.

### Edge cases

- Deleting the last billing address leaves the customer with none, and the next one added becomes the default.
- Saving the default billing address in the panel shows it on the [[customers-details]] Default address card until the page is reloaded. The card then returns to the shipping default.
- API auto-promotion behaviour mirrors the UI — see [[customer-billing-address-api]].

## Programmatic access

The default can also be managed via JSON-API v2, which refuses to delete it. See [[customer-billing-address-api]].

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-list]] — the Type column where the Default badge / Set-as-default button surfaces.
- [[customer-billing-address-storage]] — the `default_billing_address_id` column on the customer row.
- [[customer-billing-address-api]] — JSON-API v2 default-management.
- [[customers-details]] — parent details page.
- [[customer-shipping-address-defaults]] — the parallel concept for shipping; same model, separate column, independent pointer.

## Open questions

None.
