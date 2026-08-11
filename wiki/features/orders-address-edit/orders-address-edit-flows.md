---
type: feature
nav_path: "Orders → Order details → Address → Edit flows"
route_name: admin.orders.address.shipping
route_path: /admin/orders/address/{shipping|billing}/:order_id
aliases: ["Add order address", "Edit order address", "Change order address", "Order address operations", "Address flow matrix"]
tags: [orders, address, flows, routes]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[orders-address-edit]]. See the hub for related aspects (form fields, office/locker, propagation, side effects).

# Order address — flows (Add / Edit / Change / Office)

## Purpose

There are FOUR distinct address-mutation operations on the order, plus a fifth shipping-only sub-flow for courier office / parcel locker pickup. This page is the operational map: WHICH operation to pick for WHICH situation, and WHICH route serves each.

## Where to find it

All entry points are reachable from [[orders-details]] → Customer sidebar card → settings cog. The exact menu entry depends on the order's current state:

- **Add... address** — visible when the order has no address of that type yet.
- **Edit... address** — visible when an address of that type already exists.
- **Change... address** — visible when the customer has more than one saved address of that type.
- **Office / Locker pickup** (shipping only) — visible when the order's courier integration registers `apps.<courier>.offices` or `apps.<courier>.lockers` routes.

## What the merchant can do here

The decision matrix:

| Situation | Right operation | What happens |
|-----------|-----------------|--------------|
| The order has no shipping address (e.g. a digital-only order, or one created with skipped fields). | **Add** | Creates a fresh address record on the order. Billing-Add ALSO creates a new saved billing address on the customer's profile. |
| The customer phones to correct a typo (wrong house number, wrong postal code). | **Edit** | Modifies the existing address fields. Shipping changes propagate to the saved profile only if the merchant ticks the toggle; billing changes propagate automatically when there's a link — see [[orders-address-edit-propagation]]. |
| The customer wants their parcel rerouted to a different saved address (e.g. "send it to my work address instead"). | **Change** | Swaps to a different saved address from the customer's address book — one dropdown pick, no field typing. |
| The customer wants to switch from home delivery to courier-office or locker pickup mid-fulfillment. | **Office / Locker** | Replaces the home address with the courier's office or locker address. See [[orders-address-edit-office-locker]]. |
| The merchant just needs to inspect the address. | **View** | Read-only display in the sidebar card. No mutation. |

### Routes

Sub-routes under `/admin/orders/address/{type}/{order_id}/`:

| Route name | Method | Purpose |
|------------|--------|---------|
| `admin.orders.address.shipping` | GET | View the shipping address (panel display). |
| `admin.orders.address.shipping.add` | GET / POST | Add new shipping address. |
| `admin.orders.address.shipping.edit` | GET / POST | Edit existing shipping address. |
| `admin.orders.address.shipping.update` | POST | Save shipping edit. |
| `admin.orders.address.shipping.change` | GET / POST | Switch to a different saved address. |
| `admin.orders.address.office.edit` | GET / POST | Office / locker pickup selection (Panel C). |
| `admin.orders.address.billing` | GET | View the billing address. |
| `admin.orders.address.billing.add` | GET / POST | Add new billing address. |
| `admin.orders.address.billing.edit` | GET / POST | Edit billing address. |
| `admin.orders.address.billing.change` | GET / POST | Switch billing address. |

### Edit is different from Change is different from Add

| Action | What it does |
|--------|--------------|
| **Edit** | Modify the existing address fields. Full form, slide-from-right side-panel. |
| **Change** | Swap to a DIFFERENT saved address from the customer's address book. One dropdown pick. |
| **Add** | Create a new address record (when the order has no address yet). |

Change is fast: one dropdown. Edit is full form. The merchant should pick the right tool for the job — Edit + retyping when the goal is "send to the SAME address book entry but corrected" is wasted effort; the merchant should Edit the saved profile address instead and re-pull via Change.

## Settings & fields

This page covers operations only — no fields. See [[orders-address-edit-form-fields]] for the per-panel field inventory.

## Business rules

### One shipping address per order — strict

Strictly one shipping address per order. The platform does not support multiple shipping destinations on a single order (e.g. splitting one order across two addresses). For B2B / multi-destination workflows the merchant creates separate orders.

### Add operation is reachable only when no address exists

The "Add" entry point is hidden once an address of that type is attached. The merchant must use Edit (modify in place) or Change (swap to a saved one) instead. The platform does not have a separate "replace address" operation — that's exactly what Edit and Change cover.

### Digital-only orders — shipping address optional

Even for orders containing only digital products, the platform supports a shipping address being attached (the customer may still have entered one at checkout). When no shipping address is on the order, the Edit / Change / Office routes throw *"Invalid address"* and the merchant uses Add instead to create one. The platform does NOT require a shipping address for digital orders to be processed.

### Office / Locker route is distinct from the Office radio

There are two ways to reach office / locker selection on shipping addresses:

1. Through the **Edit** form's shipping-method radio row (Panel A — the dominant flow).
2. Through the dedicated **Office / Locker** menu entry (Panel C — `admin.orders.address.office.edit`).

Both write to the same underlying address record. Panel A is the rich path; Panel C is a thin wrapper that re-uses the standard address form. See [[orders-address-edit-office-locker]] for the full picker mechanics.

### Edit on an archived order

Likely blocked at controller level for archived orders (`(verify)`). The Edit form may be enabled regardless of order state, but saving on an archived order should fail.

### Change uses the customer's saved address book

The Change operation reads from the customer's saved addresses ([[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]]). If the customer has only one saved address (or zero), the Change entry is effectively unusable — the merchant adds a new saved address on the customer profile first, then comes back to the order and uses Change.

## Related

- [[orders-address-edit]] — hub.
- [[orders-address-edit-form-fields]] — per-panel field inventory.
- [[orders-address-edit-office-locker]] — Office / Locker picker mechanics.
- [[orders-address-edit-propagation]] — snapshot semantics + propagation rules.
- [[orders-details]] — parent page; the Customer sidebar card is the entry point.
- [[customers-details-shipping-addresses]] — saved addresses that feed the Change picker.
- [[customers-details-billing-addresses]] — same for billing.

## Open questions

- **Verify** the archived-order block — is Edit / Add / Change disabled in the controller, or only at the UI level?
