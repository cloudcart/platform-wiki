---
type: feature
nav_path: "Orders → Order details → Address → Propagation to customer profile"
route_name: admin.orders.address.shipping.update
route_path: /admin/orders/address/{shipping|billing}/{order_id}/update
aliases: ["Update address in profile", "Update customer info", "Address propagation", "Snapshot semantics", "Billing automatic propagation", "Shipping propagation toggle"]
tags: [orders, address, customers, propagation, snapshot]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-address-edit]]. See the hub for related aspects (flows, form fields, office/locker, side effects).

# Order address — snapshot vs propagation

## Purpose

The order's address is a **snapshot at order time** — editing it on the order does not automatically rewrite the customer's saved profile address. Whether the edit propagates to the customer's saved address book is the highest-impact mechanic in this cluster, and it works very differently for shipping vs billing. This page documents the snapshot rule and the asymmetric propagation behaviour.

## Where to find it

The propagation control lives in [[orders-address-edit-form-fields]] — specifically:

- **Shipping**: the "Update address in profile" checkbox at the bottom of Panel A.
- **Billing**: there is NO toggle. Propagation is automatic.

The downstream destination is the customer's saved address book — [[customers-details-shipping-addresses]] and [[customers-details-billing-addresses]].

## What the merchant can do here

### For shipping — opt in to propagation per save

When the merchant edits a shipping address on the order:

- **Checkbox UNCHECKED (default)** — only the order's address snapshot updates. The customer's saved shipping address is untouched.
- **Checkbox CHECKED** — the order's snapshot updates AND the customer's saved shipping address is also updated, provided the order's shipping address has a link to a saved one (`address_id` is set).

The checkbox is unchecked by default on every Edit. The merchant must consciously tick it to push the change upstream.

### For billing — propagation is automatic

When the merchant edits a billing address on the order:

- **Always propagates** to the customer's saved billing address if there is a link to a saved one.
- There is NO toggle to suppress this.

When the merchant ADDS a billing address on an order (Add operation):

- A new billing address is ALWAYS created on the customer's saved billing addresses.
- There is NO toggle to suppress this either.

So billing changes are profile-level changes by default. The merchant should treat billing edits accordingly — if the customer just wants the invoice issued differently this time only, the merchant must either (a) revert the customer's saved billing afterwards, or (b) understand that this is a customer-wide change.

## Settings & fields

### The Update-in-profile checkbox (shipping only)

- **Field name**: `update_address_in_profile`, value `1`.
- **Where**: at the bottom of Panel A (Edit form) — NOT a header switch.
- **Default**: unchecked.
- **Implementation**: the platform checks for the field's PRESENCE in the request — an unchecked checkbox is not submitted at all, so the default-OFF behaviour is automatic. The platform does not look at the value.

Required state for propagation to happen:

1. Checkbox checked.
2. Order's shipping address has a saved-address link (`address_id` is set).

If the order's shipping address was free-typed at checkout and not linked to a saved customer address, propagation fails with *"Invalid address"* — there is no record to update.

### Field-by-field copy when propagation happens

When the merchant ticks the checkbox and saves (shipping), the platform copies a comprehensive field list to the customer's saved address record. The full list:

- country, state, city, quarter
- street, street number
- postal code
- address1 / address2 / address3
- first name, last name
- company name, company VAT
- phone
- building, entrance, floor, apartment
- note
- latitude, longitude
- neighborhood, locality, timezone

So the toggle is **full-field push**, not just name + email. Any field the merchant changes on the order replaces the same field on the saved profile address.

## Business rules

### Snapshot semantics — the foundation

The address on an order is a **snapshot at order time**. The customer's saved addresses can change later, but the order keeps the address it had when it was placed. This protects against unintended propagation — typo fixes on one order shouldn't change the customer's saved address unless the merchant says so.

This rule applies to BOTH shipping and billing — the address fields on the order are stored on the order record itself, not as a foreign-key reference to the saved customer address. The `address_id` linkage (when present) is for traceability, not for live read-through.

### Asymmetric propagation — the trap

The shipping-vs-billing asymmetry is the single most-misstated mechanic in this cluster. Restated for clarity:

| Operation | Shipping | Billing |
|-----------|----------|---------|
| **Add** | Creates a new shipping address on the order. Always also adds to the customer's profile (no toggle). | Creates a new billing address on the order. Always also adds to the customer's profile (no toggle). |
| **Edit** | Updates the order snapshot. Propagates to the customer's profile ONLY when the checkbox is ticked AND a profile link exists. | Updates the order snapshot. AUTOMATICALLY propagates to the customer's profile when a profile link exists. No toggle. |
| **Change** | Swaps the order to a different saved address. The profile address itself is untouched. | Same — swap only, no profile mutation. |

So:

- For **shipping**, the default behaviour of Edit is "order-only" — safer for one-off typo fixes.
- For **billing**, the default behaviour of Edit is "profile-level" — every fix to a billing address on an order is a fix to the customer's billing identity.

This is by design — billing data (VAT, BULSTAT, MOL, company name) is treated as identity data that the merchant should keep consistent across all of the customer's orders. Shipping data is treated as per-shipment.

### "Update customer info" is the checkbox label internally

Some templates / older copy refer to the toggle as "Update customer info"; the actual input name is `update_address_in_profile`. The merchant sees a single switch labelled per the active language locale.

### When the link is missing

If the order's shipping address has no `address_id` link to a saved customer address (e.g. the customer placed the order as a guest, or filled in the shipping address by hand at checkout), the checkbox cannot achieve anything — there is no record to update. The save will surface *"Invalid address"* in that case. The merchant should use Change to attach a saved address first, then Edit afterwards, OR ignore propagation entirely.

### History entries do NOT distinguish toggle on / off

The order's history entry (`order_address_edit`, etc.) does not record whether the propagation was triggered. The merchant must check the customer profile separately to confirm whether the saved address was touched. See [[orders-address-edit-side-effects]] for the history entry actions.

## Related

- [[orders-address-edit]] — hub.
- [[orders-address-edit-flows]] — operations that interact with propagation (Add / Edit / Change).
- [[orders-address-edit-form-fields]] — where the checkbox lives.
- [[orders-address-edit-side-effects]] — history entry actions per change.
- [[customers-details]] — customer profile (where propagation lands).
- [[customers-details-shipping-addresses]] — saved shipping addresses.
- [[customers-details-billing-addresses]] — saved billing addresses.

## Open questions

- **Verify** — when Change swaps the order to a different saved billing address, does the platform copy the NEW saved one's fields onto the order, then immediately push back to the same saved one (no-op), or does the platform skip propagation on Change?
