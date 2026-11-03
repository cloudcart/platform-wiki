---
type: feature
nav_path: "Orders → Order details → Address → Side effects on save"
route_name: admin.orders.address.shipping.update
route_path: /admin/orders/address/{shipping|billing}/{order_id}/update
aliases: ["Address save side effects", "Tax recalculation on address change", "Shipping re-quote", "Address history actions", "order.updated webhook on address edit", "Courier address validation", "Waybill not auto-voided"]
tags: [orders, address, side-effects, tax, shipping, history, webhook]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[orders-address-edit]]. See the hub for related aspects (flows, form fields, office/locker, propagation).

# Order address — side effects on save

## Purpose

Every Save on an address-edit panel triggers a cascade: tax recalculation, shipping re-quote, history-entry write, AJAX panel reloads, and a webhook fire. This page documents what happens after the merchant hits Save — so the merchant knows what to expect, what might silently change, and what to verify.

## Where to find it

Side effects happen on the POST submission of any of the address routes — see [[orders-address-edit-flows]] for the full route table. The merchant sees the side effects as:

- Updated values in the [[orders-details]] sidebar address card.
- A potentially different shipping cost in the order summary.
- A new entry in [[orders-history]].
- A real-time `order.updated` webhook firing to any subscribed receiver per [[settings-hooks]].

## What the merchant can do here

Nothing extra — the side-effect cascade is automatic on Save. The merchant should however **review the order summary after every shipping address edit** to confirm:

- Shipping cost is what they expect (the re-quote may have changed it).
- Tax line is correct for the new address.
- No silent courier error has degraded the order state.

## Settings & fields

This page has no field inputs of its own. The downstream settings consulted on save:

- [[settings-taxes]] — tax brackets re-applied based on the new address's country / region.
- [[settings-geo-zones]] — geo-zone reassignment.
- [[settings-geo-distances]] — distance-based shipping recalculation.
- [[settings-hooks]] — receivers for the `order.updated` webhook.

## Business rules

### Tax + shipping auto-recalculated on save (with silent change risk)

Saving triggers tax + shipping recalculation in one transaction. The new address's geo zone is matched against [[settings-taxes]] and [[settings-geo-distances]] to produce the new totals. No separate recalculate action is needed.

On a shipping address edit, the platform also runs a **full courier re-quote**: it invalidates the saved quote cache, calls the courier's quote API for the new address, and updates the shipping line on the order to the new quote's price, service name, and "side" (sender / recipient pays). So **shipping cost may CHANGE silently**.

**Recalc-lock caveat:** on an order whose recalculation is **locked** (the default once payment is `completed`), the shipping **price is kept** rather than re-quoted — the address fields, geo-zone and tax update, but the shipping cost stays frozen (see [[order-pipeline-recalculation]]). So the silent-change risk applies to unpaid / unlocked orders; a paid order's shipping price won't move on an address edit unless the merchant force-unlocks it.

If the courier returns NO quote for the new address (out-of-coverage, weight-rule mismatch, etc.), the order keeps its previous shipping line but the `service_quote_error` meta flag was just cleared — meaning subsequent fulfilment workflows may misbehave silently. The merchant should verify the shipping line is sensible after every shipping address edit, especially when the address moves to a different region.

### Validation — courier-level address validity

Some courier integrations (those implementing address validation) call the courier API on save to verify the address exists in their system. If the courier rejects the address, the save fails with the courier's error message (translated where available). For couriers without validation support, the save succeeds even for nonsense addresses — the error surfaces later at waybill generation via [[orders-shipping-waybill]].

### Address change after fulfillment — warns, doesn't auto-void

The platform does NOT auto-void an existing waybill when the address changes. The merchant must manually void the waybill via [[orders-shipping-waybill]] BEFORE editing — the form is enabled regardless, but saving may leave the order in an inconsistent state where the waybill points to the OLD address.

Recommended workflow when changing an address after waybill generation: void the waybill via [[orders-shipping-waybill]] → edit / change the address → regenerate the waybill. Skipping the void will not surface an error at save time, but the parcel will physically be picked up from the courier with the old address printed.

### Country defaults to "internal" integration on missing courier

If the shipping address is saved with no courier integration assigned, the platform defaults the integration field to `internal`. This is the catch-all for orders without a real courier. The Country name is also auto-filled from the country ISO code (using the locale-localised country name) when the field was empty.

### History entries — action codes per change

Every Save records an entry in [[orders-history]]. The action code identifies which type of address change happened:

| Action code | Action name | What changed |
|-------------|-------------|--------------|
| 9 | `order_address_change` | Shipping address swapped via Change. |
| 10 | `order_address_edit` | Shipping address edited in place via Edit. |
| 11 | `order_address_reposition_billing` | Billing address coordinates moved (e.g. Google Maps reposition). |
| 12 | `order_address_change_billing` | Billing address swapped via Change. |
| 13 | `order_address_edit_billing` | Billing address edited in place. |
| 14 | `order_address_reposition_shipping` | Shipping address coordinates moved. |
| 15 | `order_address_add_shipping` | New shipping address added (Add operation). |

So the merchant can see exactly which type of address change happened, and when, on the order's history page. There is also a corresponding `order_address_add_billing` (`(verify)` exact action code — the same pattern as code 15 for shipping).

### AJAX panel reloads after save

The platform triggers a chain of `cc.ajax.reload` calls on success:

- `#order_preview` — the side-panel preview.
- `#order_{shipping|billing}_address` — the address card itself.
- `#order_summary` — the products + totals table (in case taxes / shipping cost changed).
- `#order_history` — the timeline picks up the new entry.

The merchant sees the side panel close and the underlying sidebar / summary refresh in place, without a full-page reload.

### `order.updated` webhook fires

Every address save fires the `order.updated` webhook to any subscribed receiver per [[settings-hooks]]. The webhook payload is the full updated order resource — receivers should be idempotent because address edits can fire multiple updates in quick succession (Edit → Office → Edit again, etc.). Receivers integrating with ERP / WMS should match on the order's ID and overwrite, not append.

### Programmatic access — read-only API, admin-only mutation

Order addresses are exposed as the **read-only** [[api-order-shipping-address]] and [[api-order-billing-address]] resources on JSON-API v2. Address mutation (Add / Edit / Change / Office / Locker) is admin-panel-only — the API does NOT expose endpoints to edit addresses, swap saved addresses, or pick courier offices / lockers. All the rich side-effect behaviour above (tax + shipping re-quote, courier validation, propagation, history entry, webhook fire) lives in admin code only. The platform requires these flows to run through validated admin paths so that tax, shipping, courier-mapping, and customer-profile invariants hold. See [[json-api-v2]] for the read-vs-mutate principle.

## Related

- [[orders-address-edit]] — hub.
- [[orders-address-edit-flows]] — which route triggers each side-effect chain.
- [[orders-address-edit-form-fields]] — what the merchant typed before the save.
- [[orders-address-edit-office-locker]] — Office / Locker switch's effect on re-quote.
- [[orders-address-edit-propagation]] — separate propagation rules (snapshot vs profile).
- [[orders-history]] — the history list where the action codes show up.
- [[orders-shipping-waybill]] — must void manually before address change.
- [[settings-taxes]] — tax recalculation.
- [[settings-geo-zones]] — geo-zone reassignment.
- [[settings-geo-distances]] — distance-based shipping recalculation.
- [[settings-hooks]] — `order.updated` webhook receivers.
- [[api-order-shipping-address]] — read-only API resource.
- [[api-order-billing-address]] — read-only API resource.
- [[json-api-v2]] — API overview.

## Open questions

- **Verify** the exact action code for `order_address_add_billing` — likely a code between 11 and 15 paired with action 15 for shipping.
- **Verify** — does the `order.updated` webhook fire on a Change operation where no underlying field changed (customer picked the same saved address)? Likely yes (the platform fires unconditionally), but worth confirming.
