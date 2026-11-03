---
type: feature
nav_path: "Apps → ACS Courier → Pickup list"
route_name: apps.acscourier.pickuplist
route_path: /admin/shipping/acscourier/pickuplist
aliases: ["ACS pickup list", "ACS voucher", "Generate pickup list", "ACS manifest", "ACS insurance", "ACS Saturday delivery", "ACS Smartpoint", "ACS товарителница", "Списък за вземане ACS", "Застраховка ACS"]
tags: [apps, shipping, courier, greece, waybill]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-acscourier]]. See the hub for credentials, the pickup station, channels and pricing.

# ACS Courier — pickup list and vouchers

## Purpose

What happens to an ACS voucher after it is created: the daily **pickup list** that finalises a day's vouchers, how a manual and an automatic voucher are filled in, and when a voucher can still be deleted.

## Where to find it

Sidebar → **Apps → ACS Courier**, tabs **Pickup list** (`/admin/shipping/acscourier/pickuplist`) and **History** (`/admin/shipping/acscourier/history`). A manual voucher is created from the order through the waybill form ([[orders-shipping-waybill]]).

## What the merchant can do here

- Pick a date and click **Generate pickup list**.
- Print a pickup list, and read past lists under **History** (**Show pickup lists**).
- Print or delete a voucher that is not on a list yet.
- Fill in insurance, Saturday delivery, back documents and protocol on the manual waybill form.

## Settings & fields

| Control | What it does |
|---|---|
| **Date** (Pickup list tab) | The day the list is issued for. Defaults to tomorrow. ACS issues the list per single day. |
| **Generate pickup list** | Issues the list for that date. Opening the tab issues nothing and waits for this button. |
| **Insurance** on the waybill form | The insured amount typed on the form is used, up to **3000 EUR** on the voucher. |
| **Back documents** (RDO), **Protocol** (PRO), **Saturday** on the waybill form | Each checkbox works on its own, and each reaches the voucher. |

## Business rules

### Generating finalises the day

**Generate pickup list** finalises that day's vouchers, and they can no longer be deleted. If unprinted waybills remain for the date, ACS returns them instead of issuing the list. With none at all the tab shows: *"You have not created any waybills with a delivery date of {date}. To generate a pickup list, you need to have created and printed waybills for the selected date."*

Each row in **History** has a Print action that opens ACS's PDF in a new tab.

### Deleting and cancelling

Cancelling a fulfilment deletes the voucher at ACS, unless it is already on a pickup list. Errors from ACS on delete and print are shown to the merchant.

### Automatic waybills

- Insured only when **Insurance** (`insurance`) is on in the settings.
- If ACS refuses Saturday delivery, the waybill is sent again once without it.
- The order's shipping amount is not overwritten by the voucher.

### What the voucher carries

- The customer's email.
- For a Smartpoint or locker point: its station and branch ([[apps-acscourier]] offers these in the office channel).
- Default dimensions, read in millimetres and sent to ACS in centimetres.

Whether each add-on is honoured depends on the merchant's ACS contract tier.

### Tracking on the storefront

The tracking page shows no events for a voucher ACS does not know yet. Events arrive in Greek.

### Admin GraphQL

Mutation `generateAcscourierPickupList(date)` issues the list, with the same effect as the button. It replaces the query `acscourierPickupList`. Mutation `deleteAcscourierVoucher` deletes a voucher. See [[admin-graphql-api]].

## Related

- [[apps-acscourier]] — hub.
- [[orders-shipping-waybill]] — the waybill flow.
- [[shipping-provider-mech-waybill]] — the shared waybill mechanism.

## Open questions

None.
