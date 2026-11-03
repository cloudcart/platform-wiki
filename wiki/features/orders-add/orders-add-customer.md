---
type: feature
nav_path: "Orders → + Add order → Customer selection"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order customer picker", "Manual order customer", "Add customer inline from order", "Customer autocomplete on manual order", "Customer name fallback"]
tags: [orders, manual, smarty, draft, customer]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-add]]. See the hub for the other aspects (wizard, delivery methods, address handling, validation, draft state, no-API rationale).

# Add order — customer selection

## Purpose

Every manual order **must be associated with a Customer record** — there is no "guest manual order" path. This page documents how the merchant picks (or creates) the customer in step 1 of the manual-order wizard, what auto-loading happens on customer change, the inline customer-create slide-out, and the customer-name fallback chain used downstream.

## Where to find it

The Customer card lives in the sidebar of the **+ Add order** side panel — see [[orders-add-wizard]] for the panel layout. The two controls are the **Customer** autocomplete and the **+ Add customer** link directly under it.

## What the merchant can do here

### Customer search (autocomplete)

The Customer field is a Select2 autocomplete (`customer_id`) backed by an AJAX call to `admin.autocomplete.customer`. The merchant types the customer's name, email, or phone and picks from suggestions.

### Customer change handler — auto-loads address list

When the merchant picks a customer in the autocomplete, JavaScript fires:

1. AJAX GET to `admin.customers.list.addresses?customer_id=<id>` to fetch the customer's saved addresses.
2. **If results returned** → populates the `address_id` select with one option per saved address, enables the dropdown, hides the help alert.
3. **If no results** → shows *"No addresses for this customer"* help text and surfaces the **+ Add new address** link.
4. Also rewrites the **+ Add new address** link's href to point at `admin.customers.shipping-addresses-add` for THIS customer.

The downstream consequence is documented on [[orders-add-address-handling]].

### + Add customer (inline create — slide-out-over-panel)

The **+ Add customer** link in the Customer card opens the full customer-edit panel from [[customers]] in `wide` mode — a SECOND panel that slides in **over** the order panel.

On successful create (`#customerSummaryForm` fires the `cc.ajax.success` jQuery custom event), the JavaScript:

- Auto-fills the `customer_id` autocomplete with the new customer's `{id, name}`.
- Re-fetches the (empty) address list for the new customer.
- Surfaces the **+ Add new address** link pointing at the new customer.

So the typical flow for a brand-new walk-in customer is: **+ Add customer → + Add new address → pick delivery method → Save**.

### Customer card visuals

The Customer card also renders a Google Maps thumbnail in the sidebar (default centred on Europe lat/lng before any address is selected) — see the layout regions on [[orders-add-wizard]]. The map updates once the address is resolved. The thumbnail requires the Google Maps API key configured on [[settings-cart]].

## Settings & fields

| Field | Required at step-1 save | Notes |
|-------|--------------------------|-------|
| **Customer** (`customer_id`) | Yes — always | Autocomplete against existing Customer records. |
| **First name** / **Last name** | Conditional | Required when delivery is to office, locker, or marketplace AND the customer record has no name. See [[orders-add-validation-save]]. |

The save endpoint enforces *"Please select a customer"* when `customer_id` is empty.

## Business rules

### Customer is mandatory; no guest manual orders

The platform doesn't support "guest manual orders" — the merchant must associate the order with a Customer record. The **+ Add customer** link makes this fast for new customers, opening the full customer-edit modal from [[customers]].

### Customer name fallback chain

The platform uses this fallback order for the order's customer name:

1. Customer record's `first_name` + `last_name`.
2. Merchant-entered `first_name` / `last_name` on the form.
3. Address record's `first_name` + `last_name` (when delivery is to address).

This handles edge cases where a customer was created without a name (some legacy customer imports).

### Order initial customer fields (verified)

After the step-1 save, the platform creates an order with:

- `customer_id` from the picker.
- `customer_group_id` inherited from the customer.
- `customer_first_name` / `customer_last_name` (from the customer record, falling back to the merchant-entered fields per the chain above).
- `customer_email` from the customer.

### Permission

To create a customer inline via **+ Add customer**, the merchant needs the customers create permission in addition to the standard orders permission scope.

### Side effects

- **Customer creation** (if used inline) creates a real customer record visible in [[customers]]. This persists beyond this order — the customer remains in the database even if the merchant abandons the draft.

## Related

- [[orders-add]] — hub.
- [[customers]] — Customer create modal that opens via + Add customer.
- [[customers-details-shipping-addresses]] — saved-addresses list auto-loaded on customer change.
- [[orders-add-address-handling]] — what happens with the customer's saved-address list after the picker fires.
- [[orders-add-wizard]] — Customer card sits in the sidebar layout region.
- [[orders-add-validation-save]] — first-name / last-name conditional requirement.
- [[settings-cart]] — Google Maps API key powers the sidebar map thumbnail.

## Open questions

None.
