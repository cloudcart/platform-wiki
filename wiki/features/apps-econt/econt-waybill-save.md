---
type: feature
nav_path: "Orders → Order details → Shipping → Fulfill products (Econt) → Generate Waybill"
route_name: apps.econt.waybill
route_path: /admin/orders/details/:order_id (Econt waybill modal)
aliases: ["Econt waybill timeout", "cURL error 28 Econt", "Econt duplicate waybills", "Дублирани товарителници Еконт", "Съобщение от Еконт", "Econt yellow message", "Econt waybill created outside CloudCart", "Link existing Econt waybill", "Econt redirected to office"]
tags: [apps, shipping, courier, bulgaria, econt, waybill, troubleshooting]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[apps-econt]]. See the hub for the other aspects (settings, addresses, waybill form, recipient mapping, pallet, COD / insurance).

# Econt — generating a waybill: outcomes, timeouts, duplicates

## Purpose

What happens when the merchant clicks **Generate Waybill** (**Генериране на товарителница**) in the Econt form ([[econt-waybill-form]]): the request to Econt, the possible outcomes, the yellow message from Econt, and why a slow Econt can leave duplicate or unrecorded waybills.

## Where to find it

[[orders-details]] → Shipping row → **Fulfill products** (**Подготви за изпращане**) → **Generate Waybill**.

## What the merchant can do here

- Generate one waybill per order.
- Read Econt's message on the order after a successful waybill.
- Cancel the waybill with **Mark as unfulfilled** (**Маркирай като неизпратена**), see [[waybill-remove-void]].

## Settings & fields

None of its own. The request uses the form's values and the Econt settings.

## Business rules

### One request, one attempt, a short wait

The platform sends one create request to Econt and gives it **3 seconds** to answer when the merchant clicks in the admin or an app calls the Admin API (10 seconds for work done in the background). The wait cannot be changed by the merchant, and there is no automatic retry. The request carries no order reference that Econt could use to recognise a repeat.

### The outcomes

- **Econt answers with an error.** The message shows in the form; nothing is saved and the order stays not fulfilled.
- **Econt does not answer in time.** The admin shows a connection error (the text contains `cURL error 28` and "timed out"). Nothing is saved on the order. Econt may still have created the shipment after the wait ran out: the platform cannot know, because it never received a waybill number.
- **Econt answers with a waybill number.** The order is marked fulfilled with that number. If saving then fails on the platform's side, the platform asks Econt to cancel that waybill.

### Why duplicates happen

Each click is a new create request. After a timeout, clicking again can create a second shipment at Econt if the first one was in fact created. Whether Econt itself merges repeated requests is Econt's rule, not the platform's (verify with Econt). Before retrying after a timeout, the merchant should look for the order's shipment in their Econt account.

### Waybills CloudCart does not hold

- **No import.** There is no way to attach a waybill made in Econt's own system to an Econt order: **Fulfill products** always creates a new one, and the Admin GraphQL operation `fulfillOrder` refuses orders a courier fulfils ([[orders-status-change-admin-graphql]]).
- **The JSON API path.** A `POST /api/v2/order-fulfillments` records a tracking number on any order without contacting Econt ([[api-order-fulfillment]]). Such a number has no stored Econt waybill behind it: no label to print, no cash-on-delivery sync ([[orders-sync-cod]]) and no cancellation at Econt on **Mark as unfulfilled**. The storefront tracking page still asks Econt about any number recorded on the order.
- **Cancelling.** Shipments the platform never recorded are cancelled in Econt's own system; the platform cannot cancel them.

### Econt's message on the order

When Econt creates the waybill but adds a warning (for example that the address cannot be served and the shipment goes to an office), the platform stores it with any delayed-delivery note. The Shipping row then shows it in a yellow box starting **"Съобщение от Еконт:"**, followed by Econt's own text, for as long as the order is fulfilled. The next waybill replaces it. The platform does not change the order's address, delivery type or shipping method because of the message: whatever Econt does with the shipment is recorded only at Econt.

### Price sync

If the merchant answered Yes to **Do you want to sync the prices?**, the order's shipping price becomes the waybill's price (after the merchant's own pricing rules, such as a free-shipping threshold) and the totals are recomputed. This happens only when the payer is the receiver, and not on a paid or completed order whose recalculation is locked ([[order-pipeline-recalculation]]).

## Related

- [[apps-econt]] — hub.
- [[econt-waybill-form]] — the fields of the form.
- [[waybill-remove-void]] — **Mark as unfulfilled** and cancellation at the courier.
- [[orders-details-shipping]] — the Shipping row.
- [[econt-shipments]] — the list of Econt waybills.

## Open questions

- Whether Econt recognises a repeated create request is Econt's rule and is not visible in the platform.
