---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Default rules"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer default shipping address", "Set as default shipping address", "Default shipping address delete protection", "First-added auto-promote"]
tags: [customers, addresses, shipping, defaults]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, modal, Google Maps, save-hooks, storage, validation, API).

# Customer shipping addresses — Default-address rules

## Purpose

The platform guarantees a customer always has a single default shipping address as long as they have any shipping address at all. This aspect documents the four mechanics that maintain that guarantee: **first-added auto-promotion**, the per-row **"Set as default"** action, the **hard-guarded deletion** of the current default, and the **default-shipping vs default-billing independence**.

The "Is this the default?" comparison is computed by matching the customer's `default_address_id` pointer to the address ID — the address row itself has no `is_default` flag. See [[customer-shipping-address-storage]] for the pointer model.

## Where to find it

- "Set as default" action button in the **Type** column on the [[customer-shipping-address-list]] for every non-default row.
- "Default" pill badge in the **Type** column on the current default row (no button — already default).
- Default address sidebar card on [[customers-details]] reads from the customer's `default_address_id`.

## What the merchant can do here

- Promote a non-default shipping address to default by clicking **Set as default** on its row.
- Add a first shipping address — it auto-promotes to default on save.
- Delete any non-default address (subject to bulk-validation rules — see [[customer-shipping-address-list]]).

### What the merchant CANNOT do here

- **Delete the current default shipping address** without promoting another one first — the server rejects with HTTP 422 *"Cannot delete customer default address."* Bulk delete that includes the default also fails for the whole batch.
- Manually clear "default" with no replacement — there is no "unset default" action. The merchant must promote a different address, which atomically unsets the previous default as a side effect.
- Use the same default address row for both shipping AND billing — the two are independent customer-level pointers.

## Settings & fields

### Customer-level pointers (stored on the customer row)

| Pointer | What it points to |
|---|---|
| `default_address_id` | The customer's default SHIPPING address ID. |
| `default_billing_address_id` | The customer's default BILLING address ID. |

Both live on the customer row, NOT on the address row. So the customer record is the source of truth for "which address is default" — and the address itself doesn't carry a flag. See [[customer-shipping-address-storage]].

### Set-as-default endpoint

`POST /admin/api/core/customers/shipping-address/default/{customer_id}` with body `{address_id}`. Under `hasApiPermission:customers` middleware.

## Business rules

### First-added auto-promotes to default

When the customer has zero shipping addresses, adding the first one **automatically** sets `customers.default_address_id` to that row's ID. Subsequent adds do NOT auto-promote — they stay as non-default until the merchant clicks "Set as default".

This guarantees a brand-new customer's first saved address is always usable at checkout without an extra "make this default" step.

### "Set as default" flips the customer-level pointer

The "Set as default" action issues a direct UPDATE to `customers.default_address_id`. It does NOT touch the address row — the address has no `is_default` column. The previous default loses its "default" status simply because the pointer no longer matches its ID.

This means atomic promotion: there is never a moment where the customer has zero defaults OR two defaults. The pointer update is one statement; the previous default is "un-promoted" by definition.

### Inline spinner during the request

Clicking "Set as default" shows an inline `b-spinner` on the clicked row while the request is in flight (per-row loading state). Other rows remain interactive.

### Already-default rows show a pill, not a button

A row that matches the customer's `default_address_id` renders a **"Default" pill** badge (style `cc-tag-status--update`) in the Type column instead of the "Set as default" button. The merchant can't promote an already-default row.

### Delete-protection — hard guard

A delete that targets the customer's current `default_address_id` is rejected with HTTP 422 *"Cannot delete customer default address."* The merchant must first promote a different address to default before the old default can be deleted.

This applies to:

- Single-row deletes via JSON-API v2 — see [[customer-shipping-address-api]].
- Bulk-delete from the [[customer-shipping-address-list]] — the whole batch fails if any ID in the selection matches the current default.

### Default-shipping and default-billing are INDEPENDENT

The customer record has TWO independent default pointers. Toggling one has zero effect on the other:

- `default_address_id` — shipping. Edited from this list + the [[customers-details]] sidebar pen icon.
- `default_billing_address_id` — billing. Edited from [[customers-details-billing-addresses]].

A customer can have a default shipping address AND a default billing address pointing to two completely different address records. They're maintained separately.

### Side effects of "Set as default"

- Toast: *"Default address updated"*.
- Refetches the address list (so the pill / button states swap on the right rows).
- Refetches the [[customers-details]] Default address sidebar card via the shared inject context.

### Side effects of saving a new (first) address

When the saved address is the customer's first shipping address:

- Customer row is updated with `default_address_id = <new-id>`.
- The [[customers-details]] sidebar refetches to show the new default.

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-list]] — where the "Set as default" action lives.
- [[customer-shipping-address-storage]] — the pointer-on-customer model that makes "default" a comparison, not a flag.
- [[customer-shipping-address-modal]] — the modal that triggers first-added auto-promotion on save.
- [[customer-shipping-address-api]] — the API path that respects the same delete protection.
- [[customers-details]] — the Default address sidebar card that re-renders on these actions.
- [[customers-details-billing-addresses]] — the independent billing-default mechanism.

## Open questions

None.
