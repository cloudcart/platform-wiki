---
type: feature
nav_path: "Orders → Order details → Address → Edit / Add / Change / Office"
route_name: admin.orders.address.shipping
route_path: /admin/orders/address/{shipping|billing}/:order_id
aliases: ["Edit order address", "Change order address", "Add order address", "Order shipping address", "Order billing address", "Office pickup", "Locker pickup", "Промяна на адрес на поръчка"]
tags: [orders, address, shipping, billing, office, locker, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---

# Order address edit (shipping + billing + office / locker)

## Purpose

The flow for **modifying the addresses attached to a specific order** — both the shipping address (where to deliver) and the billing address (where to issue the invoice). The merchant uses this when a customer phones to correct an address typo, wants the parcel rerouted to a different saved address, needs to switch from home delivery to courier office pickup mid-fulfillment, or needs to update the billing address before invoice generation.

There are FOUR distinct mutation operations plus a fifth shipping-only sub-flow:

1. **View** — read-only address display in the order sidebar.
2. **Add** — create a brand-new address on this order (when none exists yet).
3. **Edit** — modify the existing address in place.
4. **Change** — swap to a DIFFERENT existing address from the customer's saved addresses ([[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]]).
5. **Office / Locker** (shipping only) — pick a courier office / parcel locker as the delivery point (for couriers like Econt, Speedy, BoxNow).

This page is the **hub** for the order-address-edit cluster. Drill into the sub-pages below for the operational mechanics.

## Sub-pages (in this cluster)

- [[orders-address-edit-flows]] — the four operations (View / Add / Edit / Change) + the fifth Office / Locker sub-flow; route table; when to use each.
- [[orders-address-edit-form-fields]] — Panel A (full form), Panel B (Change picker), Panel C (Office menu entry); shipping vs billing field differences; required vs optional fields.
- [[orders-address-edit-office-locker]] — shipping-method radio row (Address / Office / Locker); courier-specific picker behaviour (Econt, Speedy, BoxNow, EuShipment); live courier-API queries with no caching.
- [[orders-address-edit-propagation]] — snapshot semantics; the "Update address in profile" toggle for shipping; the asymmetric AUTOMATIC propagation for billing.
- [[orders-address-edit-side-effects]] — tax + shipping re-quote on save; history-entry types per action; waybill-not-auto-voided pitfall; courier-level validation; AJAX panel reloads; `order.updated` webhook.

## Where to find it

From [[orders-details]] → **Customer sidebar** card → settings cog → **Edit shipping / billing address** OR **Change address** OR (shipping only) **Office / Locker pickup**.

Routes live under `/admin/orders/address/{shipping|billing}/{order_id}/...` — see [[orders-address-edit-flows]] for the full route table.

## What the merchant can do here

The hub-level summary (drill into the aspects for full detail):

- **Choose the right operation** — Add when there is no address yet, Edit to modify in place, Change to swap to a different saved address, Office / Locker for courier pickup. See [[orders-address-edit-flows]].
- **Fill the form** with recipient name, country, city, postal code, street, additional info, phone — and (for billing) company name, VAT, registration number, owner. See [[orders-address-edit-form-fields]].
- **Pick a courier office or parcel locker** when the courier supports it (Econt offices, Speedy depots, BoxNow lockers, etc.). See [[orders-address-edit-office-locker]].
- **Decide whether the change propagates to the customer's profile** — for shipping, controlled by a checkbox; for billing, automatic when a link exists. See [[orders-address-edit-propagation]].
- **Trigger tax + shipping recalculation** automatically on every save. See [[orders-address-edit-side-effects]].

### What the merchant CANNOT do here

- Edit an address on an archived order (likely blocked at controller level — `(verify)`).
- Add an address when one already exists — must Edit OR Change instead.
- Change shipping method (office / locker / address) for couriers that don't support those options — the radio options are hidden. See [[orders-address-edit-office-locker]].
- Skip the "Update address in profile" toggle decision on shipping — it always defaults to OFF; on billing, propagation is automatic with no opt-out. See [[orders-address-edit-propagation]].

## Settings & fields

The hub does not enumerate fields. Field-by-field detail per template lives on [[orders-address-edit-form-fields]] (Panels A / B / C). The shipping-method radio row and the office / locker picker have their own page at [[orders-address-edit-office-locker]].

The address-edit flow does NOT have any store-wide settings of its own. It reads from:

- [[settings-cart]] — Google Maps API key for the City autocomplete.
- [[settings-taxes]] — recalculated on save.
- [[settings-geo-zones]] / [[settings-geo-distances]] — geo-zone reassignment on save.
- [[apps]] — courier integrations register the `apps.<courier>.offices` / `.lockers` routes that drive the office / locker picker.

## Business rules

The hub-level rules (full mechanics on the sub-pages):

- **One shipping address per order — strict.** No multi-destination orders. See [[orders-address-edit-flows]].
- **The address is a snapshot at order time.** Editing changes the snapshot, not the customer's saved address — UNLESS the "Update address in profile" toggle is ticked (shipping) OR there is a billing-link (billing, automatic). See [[orders-address-edit-propagation]].
- **Shipping toggle vs billing automatic propagation** — the asymmetry is the highest-impact mechanic in this cluster. Billing edits are profile-level by default; shipping edits are order-only by default. See [[orders-address-edit-propagation]].
- **Shipping address Edit triggers a full courier re-quote.** Shipping cost may CHANGE silently after a save. See [[orders-address-edit-side-effects]].
- **The platform does NOT auto-void an existing waybill on address change** — the merchant must manually void via [[orders-shipping-waybill]] BEFORE editing to avoid an inconsistent state. See [[orders-address-edit-side-effects]].
- **Office / locker list is fetched live with no caching** — the merchant always sees the courier's current open offices. See [[orders-address-edit-office-locker]].

## Related

- [[orders-details]] — parent page (Customer sidebar action triggers this flow).
- [[customers-details-shipping-addresses]] — customer's saved shipping addresses (source of the Change picker).
- [[customers-details-billing-addresses]] — same for billing.
- [[customers-details]] — customer profile (where the Update Info toggle propagates to).
- [[orders-customer-change]] — sibling flow for editing customer NAME / email (different from address).
- [[orders-shipping-waybill]] — waybill is affected when shipping address / method changes.
- [[orders-history]] — address-change events appear in the audit log.
- [[settings-cart]] — Google Maps API key.
- [[settings-taxes]] — tax recalculation triggered by address change.
- [[settings-geo-zones]] — geo-zone reassignment.
- [[settings-geo-distances]] — distance-based shipping recalculation.
- [[apps]] — courier integrations provide the offices / lockers routes.
- [[api-order-shipping-address]] — read-only JSON-API v2 resource.
- [[api-order-billing-address]] — read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview (read-vs-mutate principle).

## Open questions

None at the hub level. Aspect-specific open questions live on each sub-page.
