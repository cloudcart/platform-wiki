---
type: feature
nav_path: "Orders → + Add order → Address handling"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order address handling", "Manual order address picker", "Add new address from manual order", "Address slide-out-over-panel", "Saved address side effect on manual order"]
tags: [orders, manual, smarty, draft, address]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-add]]. See the hub for the other aspects (wizard, customer, delivery methods, validation, draft state, no-API rationale).

# Add order — address handling

## Purpose

The manual-order flow needs an address for every order — either a saved one from the customer's profile, or a brand-new one created inline. This page documents the saved-address dropdown, the **+ Add new address** slide-out-over-panel mechanic, the side effect that adds new addresses to the customer's profile, and the cloning rule that protects saved addresses from being mutated through the order.

## Where to find it

The address controls sit in the sidebar of the **+ Add order** side panel — see [[orders-add-wizard]] for the layout. There are two distinct controls:

- The **Shipping address** dropdown (`address_id`) — visible when **Delivery to = address** (see [[orders-add-delivery-methods]]).
- The **+ Add new address** link — visible immediately under the dropdown and inside the empty-state alert when the customer has no saved addresses.

## What the merchant can do here

### Saved-address dropdown

The address dropdown lists the customer's saved [[customers-details-shipping-addresses]]. The list is populated automatically when the customer is picked — see [[orders-add-customer]] for the customer-change handler.

- If the customer has **at least one** saved address → the dropdown is enabled with one option per saved address.
- If the customer has **no** saved addresses → the dropdown is disabled with the empty-state message *"No addresses for this customer"* and the **+ Add new address** link is highlighted.

### + Add new address (slide-out-over-panel)

The **+ Add new address** link uses `data-ajax-panel` with `data-panel-class="wide"` — it slides a **second panel** in over the order panel. Inside that second panel, the platform renders the customer-address create form (the same form used on [[customers-details-shipping-addresses]] for shipping-address create).

On successful address create (`#addressForm` fires the `cc.ajax.success` jQuery custom event), the JavaScript:

- **Re-fetches the customer's address list** (so the new address appears in the dropdown of the outer order panel).
- **Returns the OUTER panel to its leftmost position** (`right: 0`) — the address sub-panel closes, the order panel stays and now has the new address in its dropdown.

The merchant's flow is therefore: pick customer → click **+ Add new address** → fill the form → save → the new address is auto-selected back in the order panel.

### Address-create link rewrites for the current customer

The customer-change handler not only fetches the address list, it **also rewrites the +Add new address link's href** to point at `admin.customers.shipping-addresses-add` for THIS customer. So clicking +Add new address always creates the address attached to the currently-selected customer.

## Settings & fields

The address-create form itself (city, postcode, street, first/last name, phone, etc.) is documented on [[customers-details-shipping-addresses]].

| Field at the order level | Required when | Notes |
|---|---|---|
| **Address ID** | Delivery-to = address | Must be a saved-address record. *"Please select an address"* on miss. |

There is no inline "free-text address" option on the order — the address always lives on the customer's profile first, then is referenced from the order.

## Business rules

### Address — saved or new

The address dropdown lists the customer's saved shipping addresses. If the customer has none, the merchant is prompted to create one (slide-out modal that opens over the order panel). Created addresses are saved to the customer's saved-addresses list at the same time — so they're available next time too.

### Saved-address side effect (verified, for pickup deliveries)

When delivery-to is `office`, `locker`, or `marketplace`, the platform creates a **new entry** in the customer's saved-addresses list using the captured pickup-point details (name, phone, office details). This side-effect persists beyond this order — next time the merchant creates an order for this customer, the new address shows up in the saved-address dropdown.

This is **different** from the `address` delivery path:

- **For `office` / `locker` / `marketplace`** → a new saved-address record is created with the pickup-point details.
- **For `address`** → the existing saved address is **CLONED** (copied with a new ID) to the order's shipping address — no new entry is added to the customer's saved-addresses list.

### Address cloning protects the customer's profile

For `address` delivery, the address attached to the order is a **clone** of the saved address — not a pointer to it. If the merchant edits the shipping address on the order later (street typo, etc.), the customer's saved address on their profile is **not** affected. The reverse is also true: editing the customer's saved address afterwards does not change the address frozen on this order.

### Customer name fallback chain (address-delivery case)

When delivery-to is `address`, the order's customer name falls back through:

1. Customer record's `first_name` + `last_name`.
2. Merchant-entered `first_name` / `last_name` on the form.
3. Address record's `first_name` + `last_name`.

See [[orders-add-customer]] for the full chain.

### Google Maps thumbnail in the sidebar

When the address is resolved (saved address selected or pickup point picked), the sidebar's Google Maps thumbnail re-renders at that address's lat / lng. The thumbnail requires the Google Maps API key on [[settings-cart]] — without it, the slot stays as a placeholder.

## Related

- [[orders-add]] — hub.
- [[orders-add-wizard]] — sidebar layout regions including the Address-create slot.
- [[orders-add-customer]] — customer-change handler that populates the address list.
- [[orders-add-delivery-methods]] — which delivery types trigger the saved-address side effect.
- [[customers-details-shipping-addresses]] — the address form rendered in the slide-out-over-panel and the saved-addresses list the side effects mutate.
- [[settings-cart]] — Google Maps API key for the sidebar thumbnail.
- [[orders-details]] — where the merchant later edits the cloned shipping address without touching the customer's profile.

## Open questions

None.
