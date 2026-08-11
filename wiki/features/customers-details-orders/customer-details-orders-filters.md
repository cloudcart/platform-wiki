---
type: feature
nav_path: "Customers → Customer details → Orders → Filters"
route_name: customers-orders.new
route_path: /admin/customers-new/details/:id/orders
aliases: ["Customer orders filters", "Order history filters", "Order filter bar", "Order filter chips", "UTM order filters"]
tags: [customers, orders, history, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-orders]]. See the hub for the other aspects (list view, scoping).

# Customer orders — Filters

## Purpose

The filter bar on the customer order-history table. This aspect catalogues all **21+ filters** (grouped by what they target), the operator vocabulary each filter type exposes, the CcTable filter-chip surface they render through, and the exact-match-not-contains quirk that trips merchants up on the marketing-attribution filters. The columns those filters narrow are on [[customer-details-orders-list]]; the strict customer auto-scope that sits underneath every filter is on [[customer-details-orders-scoping]].

## Where to find it

From [[customers-details]] → **Orders** tab. The route is `/admin/customers-new/details/:id/orders`. The filter bar sits above the table.

## What the merchant can do here

- Apply any combination of 21+ filters; multiple filters AND-compose.
- Filter by order content (price, order status, payment status, fulfillment status).
- Filter by shipping method or payment provider.
- Filter by discount type / discount code.
- Filter by date range, customer group at order time, invoice / credit-note presence.
- Filter by marketing attribution (Recovered source, Made through, Referer, UTM Source / Medium / Campaign).
- Filter by metadata (Fast order, Archived, Draft, Created by admin, Region, Supplier).

### What the merchant CANNOT do here

- Widen the view past the current customer — the filter set always runs on top of the strict `customer_id` scope (see [[customer-details-orders-scoping]]).
- Bring back voided orders via the Order status = Voided filter — voided orders are hard-excluded server-side (see [[customer-details-orders-scoping]]).

## Settings & fields

### The 21+ filters

**Order-content filters:**
- **Total price** — currency value with comparison: More than / Less than / More than or equal / Less than or equal.
- **Order status** — multi-select (In / Not in) with 11 options: Authorized, Pending, Voided, Timeouted, Cancelled, Failed, Refunded, Chargebacked, Paid, Completed, Disputed.
- **Payment status** — multi-select (In / Not in) with 12 options: Initiated, Pending, Requested, Held, Completed, Failed, Refunded, Voided, Cancelled, Timeouted, Chargebacked, Disputed.
- **Fulfillment status** — Is / Is not: Fulfilled, Not Fulfilled.

**Provider filters:**
- **Shipping method** — multi-select from registered shipping providers (Is / Is not).
- **Payment providers** — multi-select from configured payment providers (Is / Is not).

**Discount filters:**
- **Discount** — multi-select with options: Any Discount, No Discount, Flat, Percent, Shipping, Fixed.
- **Discount code** — multi-select autocomplete from defined discount codes.

**Date / customer filters:**
- **Date** — date range with: Between, More than, Less than, More than or equal, Less than or equal.
- **Customer group** — multi-select (the customer's group at order time).

**Document filters:**
- **Credit Note** — Yes / No (orders that have / haven't generated a credit note).
- **Invoice** — Yes / No (orders with / without a generated invoice).
- **Invoice number** — multi-select autocomplete from generated invoice numbers.

**Marketing attribution filters:**
- **Recovered source** — which abandoned-cart recovery flow brought the order back.
- **Made through** — which UI / channel created the order (admin, storefront, mobile app, etc.).
- **Referer** — HTTP referer URL.
- **UTM Source** / **UTM Medium** / **UTM Campaign**.

**Metadata filters:**
- **Fast order** — Yes / No (one-click order vs full checkout flow).
- **Archived** — Yes / No.
- **Draft** — Yes / No (a draft order that hasn't been completed yet).
- **Created by admin** — Yes / No (manual orders entered by staff vs customer-side).
- **Region** — multi-select from city autocomplete.
- **Supplier** — multi-select from configured suppliers (Is / Is not).

### Filter operator vocabulary

| Filter type | Operators available |
|-------------|---------------------|
| Currency | More than / Less than / More than or equal / Less than or equal |
| Multi-select (provider, code, group) | In / Not in OR Is / Is not (depending on filter) |
| Yes/No | Yes / No |
| Date | Between / More than / Less than / More than or equal / Less than or equal |
| String | Contains (but see the exact-match rule below) |

## Business rules

### Payment statuses are independent of order statuses

The payment-status filter (12 options) is independent of the order-status filter. So an order can be Order Status = Paid but Payment Status = Refunded if the merchant manually refunded — the merchant can filter both dimensions to find specific edge cases.

### UTM filters bring attribution into customer history

The UTM Source / Medium / Campaign filters expose which marketing campaigns brought this customer back to place orders. Combined with the Referer field, the merchant can understand the customer's acquisition channel(s) per-order.

### Made through, UTM, Referer are exact-match, not contains

Despite the operator table suggesting "contains" for the **Made through** / UTM Source / UTM Medium / UTM Campaign / Referer / Recovered source filters, the backend implementation uses **exact-match** on the order's meta values stored at order-creation time. The merchant must type the exact value used by the source system (e.g., `admin`, `storefront-checkout`, `fast-order-flow` for Made through).

### Draft and Archived have separate filters

- **Draft = Yes** shows orders the customer started but didn't complete (a draft order record). Pure abandoned-cart records (cart not yet promoted to an order) live elsewhere and are not surfaced by this filter.
- **Archived = Yes** shows orders the merchant moved to archive. This filter is **required** to see archived orders at all — see [[customer-details-orders-scoping]].

### "Is admin" filter identifies merchant-created orders

When `Created by admin = Yes`, the merchant filters down to orders manually entered by staff (e.g., phone orders, in-store sales recorded retroactively). Useful for distinguishing customer-self-served orders from staff-entered ones. Note the filter-chip mislabel bug documented on [[customer-details-orders-scoping]].

### Filter chips are a CcTable sub-surface (no modal)

The filters are exposed through the **CcTable filter bar**, NOT through a modal. Each filter is a chip with an operator dropdown + a value picker; multiple filters AND-compose. The filter set is per-store — some filters depend on store config (e.g., **Supplier** is empty when no suppliers are configured).

## Related

- [[customers-details-orders]] — hub.
- [[settings-statuses]] — order / payment status taxonomies behind the status filters.
- [[settings-payment-providers]] — payment providers in the provider filter.
- [[shipping]] — shipping providers in the shipping-method filter.
- [[marketing-discounts]] — discount codes in the discount-code filter.
- [[settings-invoicing]] — invoice numbers in the invoice-number filter.

## Open questions

None.
