---
type: feature
nav_path: "Orders → Order details → Status → Admin GraphQL"
route_name: changeOrderStatus
route_path: /api/gql
aliases: ["changeOrderStatus", "ordersBulkChangeStatus", "fulfillOrder", "Admin GraphQL order status", "skippedIds", "A draft order cannot be fulfilled.", "Статус на поръчка през GraphQL"]
tags: [orders, status, fulfillment, api, graphql]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, transition rules, side effects, notification, fulfillment gate, bulk, JSON-API v2).

# Order status change — Admin GraphQL

## Purpose

Three operations of the [[admin-graphql-api]] change an order's status or fulfilment: `changeOrderStatus` for one order, `ordersBulkChangeStatus` for many, and `fulfillOrder` for a manual fulfilment. They refuse what the admin's status menu and its **Fulfill products** button refuse, so an agent, a script and the mobile app follow the same rules as a person in the admin. All three need the **Orders** staff permission.

## Where to find it

There is no screen. The same changes in the admin are on [[orders-status-change-pill]] and in the bulk action on [[orders-status-change-bulk]].

## What the merchant can do here

- Change one order's status: `changeOrderStatus`.
- Change the status of many orders in a background job: `ordersBulkChangeStatus`, followed with `bulkOperationStatus` ([[admin-graphql-api]]).
- Record a manual fulfilment with its tracking details: `fulfillOrder`. For an order its courier fulfils, the operation is `createShippingWaybill`.

## Settings & fields

**Accepted status values**, for both status operations:

- The platform's order statuses.
- The fulfilment values `not_fulfilled` and `fulfilled`.
- The store's custom statuses of type order ([[settings-statuses]]).

`partially_fulfilled` and custom payment or shipping statuses are refused. An unknown value is answered with the list of valid ones.

## Business rules

### Status changes

`changeOrderStatus` and `ordersBulkChangeStatus` refuse:

- An order whose payment authorisation is short of its total.
- A fulfilment status on an order its courier fulfils.
- Any change on an archived order.
- `completed`, unless the order is paid or fulfilled.
- `cancelled` on a paid or completed order.
- Re-opening an order after a cancellation or refund that has a return or a credit note.

`changeOrderStatus` also answers *"Order is already in status '<status>'. No change performed."* when nothing would change.

The full rules are on [[orders-status-change-transition-rules]]. An accepted change has the same effects as in the admin ([[orders-status-change-side-effects]]), customer notifications included.

### Bulk: refused orders are skipped

`ordersBulkChangeStatus` checks each order in the background job and changes each one separately. A refused order goes into `skippedIds`, and the others continue. The admin's own bulk action works differently: one refused order rolls back the whole batch ([[orders-status-change-bulk]]).

### Fulfilment

`fulfillOrder` refuses:

- A draft: *"A draft order cannot be fulfilled."*
- A status other than pending, paid, authorized or a custom one: *"An order with the status '<status>' cannot be fulfilled."*
- An order with an open return.
- An authorisation short of the total.
- An order whose courier fulfils it through its waybill.

Insufficient stock, an archived order, an order with no shipping method and products already fulfilled are refused too. See [[orders-status-change-fulfillment-gate]] for the fulfilment gate in the admin.

## Related

- [[orders-status-change]] — hub.
- [[admin-graphql-api]] — sign-in, permissions, request limit, background jobs.
- [[orders-details-shipping]] — the **Fulfill products** button and courier waybills.
- [[orders-status-change-api]] — the same change through JSON-API v2.

## Open questions

None.
