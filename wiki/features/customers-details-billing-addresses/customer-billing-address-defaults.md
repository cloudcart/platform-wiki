---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Default billing"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Default billing address", "Set as default billing", "default_billing_address_id", "Cannot delete customer default billing address"]
tags: [customers, addresses, billing, defaults]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, company fields, VIES, save hooks, storage, API).

# Customer billing address — Default management

## Purpose

The rules around **which one** of a customer's billing addresses is the default — the address the platform uses when rendering invoices for a new order placed without an explicit override. A customer can have unlimited billing addresses but exactly one default at a time; this aspect documents how that default is set, protected, and changed.

## Where to find it

- The current default is indicated by the **Default** badge in the **Type** column of the list (see [[customer-billing-address-list]]).
- Non-default rows show a **Set as default** button in the same column.
- The customer's [[customers-details]] sidebar shows a Default address card — note: that card surfaces the **shipping** default, not the billing default (the billing default is currently not surfaced in the sidebar; verify).

## What the merchant can do here

- Click **Set as default** on any non-default billing row → promotes that address to default.
- Add the customer's first billing address → it auto-promotes to default with no merchant action.
- Add or edit a different billing address without touching the default — adds beyond the first do NOT auto-promote.
- Promote a different default first → then delete the previous default.

### What the merchant CANNOT do here

- Delete the customer's current default billing — see the hard guard below.
- Set "no default" (zero defaults) while billing addresses still exist — the platform always keeps exactly one default while at least one billing address exists.
- Set the same address as both default shipping and default billing — they live in separate lists and on separate customer columns.

## Settings & fields

| Customer column | What it points to | Independence |
|------------------|--------------------|--------------|
| `default_billing_address_id` | The current default **billing** address row ID. | Independent from `default_address_id` (shipping). |
| `default_address_id` | The current default **shipping** address row ID. | Independent from `default_billing_address_id`. |

The address row itself carries NO `is_default` flag — default is computed by comparing the customer pointer to the row id at read time.

## Business rules

### One default per customer, always

While the customer has at least one billing address, exactly one of them is marked as default. The platform's invariants:

- **First-added billing auto-promotes.** When the customer has zero billing addresses and the merchant (or API) adds one, the platform automatically sets `default_billing_address_id` to that row. The merchant does NOT need to click "Set as default" on the first one.
- **Subsequent adds do NOT auto-promote.** The newly added row sits in the list with a "Set as default" button until the merchant promotes it.
- **Set as default** updates the customer pointer; the previous default's badge disappears and the new row's badge appears. The address rows themselves are not touched.

### Default billing CANNOT be deleted directly (hard guard)

A delete request — single-row or bulk — that targets the customer's current `default_billing_address_id` is REJECTED at validation with HTTP 422 *"Cannot delete customer default billing address."*

To delete the current default, the merchant must:

1. Promote a different billing address to default via **Set as default**.
2. Then delete the previous default.

Bulk delete: if any id in the bulk matches the current default, the **entire batch fails** — even the valid ids are not deleted. The merchant must remove the default id from the selection (or promote a different default first).

This protects invoice integrity — there's always exactly one default billing in place as long as the customer has any billing address.

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
- **Success toast:** *"Default address updated"*; **failure toast:** *"Error while updating default address"*.
- **Side effect:** list refetches + [[customers-details]] sidebar Default address card refetches (though the sidebar today shows the shipping default, not billing — verify whether a future change exposes billing too).

### Edge cases

- Deleting the LAST billing address (after it has been demoted from default? — impossible since the platform always keeps exactly one default). In practice: while one billing row exists, it IS the default, and deletion is blocked. To remove all billing data for a customer, the merchant must... (verify — likely impossible without going through a different cleanup path).
- API auto-promotion behaviour mirrors the UI — see [[customer-billing-address-api]].

## Programmatic access

The Set-as-default endpoint is also reachable via JSON-API v2; the default-delete protection is enforced identically. See [[customer-billing-address-api]].

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-list]] — the Type column where the Default badge / Set-as-default button surfaces.
- [[customer-billing-address-storage]] — the `default_billing_address_id` column on the customer row.
- [[customer-billing-address-api]] — JSON-API v2 default-management + delete-protection parity.
- [[customers-details]] — parent details page (sidebar Default address card).
- [[customer-shipping-address-defaults]] — the parallel concept for shipping; same model, separate column, independent pointer.

## Open questions

- Confirm whether the [[customers-details]] sidebar Default address card is updated to also surface the default billing alongside the default shipping (verify).
- Confirm the exact path / mechanism for fully wiping a customer's billing addresses (since the last one cannot be deleted while it's the default) (verify).
