---
type: feature
nav_path: "Apps → Econt → Coverage & caches"
route_name: apps.econt.overview
route_path: /admin/shipping/econt
aliases: ["Econt countries", "Econt BG RO", "Econt Romania", "Econt weight cap", "Econt 1000 kg", "Econtomat 20 kg", "Econt offices cache", "Econt quote currency", "Econt sender selection"]
tags: [apps, shipping, courier, bulgaria, romania, econt, coverage, cache, currency]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[apps-econt]]. See the hub for the other aspects (Settings, addresses, shipments, waybill mapping, pallet, COD / insurance).

# Econt — coverage, caches, currency, sender selection

## Purpose

This page collects the cross-cutting platform rules that don't belong to any single tab: the supported countries, the office/locker weight ceiling, the caches that govern how fresh the offices list is, how the quote currency is chosen, and how the platform picks WHICH sender address to use when the merchant has multiple. These rules are quietly important because they shape what the storefront customer sees at checkout and what the merchant can ship — without any visible setting that explains them.

## Where to find it

These rules are invisible — they apply automatically when the storefront calls Econt's quote API at checkout, when the merchant generates a waybill, and when the office picker on the order page fetches Econt's offices. There is no dedicated screen. The merchant interacts with the surfaces in [[econt-settings-tab]] and [[econt-addresses-tab]]; the rules below modulate what those surfaces produce.

## What the merchant can do here

- (Indirectly) ship to Bulgarian AND Romanian customers under one Econt integration — no second integration required.
- (Indirectly) rely on the platform refreshing Econt's offices list once a day — no manual refresh action.
- (Indirectly) ship Econt orders in the store's currency — the quote currency follows the store currency.
- Choose WHICH sender address is used for every order by marking exactly one address as Default in [[econt-addresses-tab]].

## Settings & fields

This page has no merchant-facing fields of its own — the rules below are platform behavior triggered by the Settings / Addresses fields.

| Behaviour | Trigger | Value |
|---|---|---|
| Multi-country coverage | Quote / waybill country selector | Bulgaria (`BG`) + Romania (`RO`) under one set of credentials |
| Office weight cap | Quote API | **1000 kg**, no size limit (above → only "To address" is offered) |
| Econtomat limit | Checkout | **20 kg**, cells 8 / 18 / 37 × 44 × 61 cm |
| Offices / Econtomats list cache | Quote / office-picker call | **1 day** server-side |
| Quote currency | Quote API request | Store currency (BGN / EUR / RON / etc.) |
| Sender address selection | Waybill generation | Merchant's Default address from [[econt-addresses-tab]] |

## Business rules

### Multi-country: Bulgaria + Romania

The fallback allowed countries list is `['BG', 'RO']` — the Econt integration covers BOTH Bulgaria and Romania under one set of credentials. A Bulgarian merchant can ship to Romanian customers via Econt without installing a second integration.

### Office and Econtomat limits

"To office" delivery takes up to **1000 kg**, with no size limit. An **Econtomat** takes up to **20 kg**, and the cart must pack into one cell: 8 / 18 / 37 × 44 × 61 cm (height × width × length). A point the cart does not fit is not offered at checkout: see [[shipping-provider-mech-locker-fit]].

### Offices / lockers list is refreshed daily

The list of Econt offices and Econtomats shown at checkout (and in the office picker on the order page) is cached for **1 day** server-side. After Econt updates its registry, merchants see the new offices within 24 hours; merchants don't need to do anything to refresh it.

### Quote currency follows the store currency

The platform sends the store currency (BGN / EUR / RON / etc.) to Econt's quote API; Econt returns prices in that currency. For Bulgaria-currency stores Econt's BGN tariff applies; for EUR or RON Econt's corresponding tariff applies. The COD cap (10000 BGN) is enforced only when the store currency is BGN — non-BGN stores rely on Econt's server-side limits. See [[econt-cod-insurance]] for the COD cap detail.

### Multi-warehouse sender selection — by merchant default only

The platform picks the sender address purely from the merchant's chosen **default** address in [[econt-addresses-tab]]. There is no smart routing (no nearest-warehouse / per-zone logic). When the merchant has multiple addresses in the address book, the one marked as default is used for every order; to ship from a different warehouse, the merchant changes which address is marked default (or picks a different sender when editing the order's waybill).

### OmniShip-based — falls through to parent

The Econt integration shares logic with all OmniShip-family couriers — bill-of-lading creation, etc., delegate to the shared OmniShip code after Econt-specific preprocessing. The OmniShip family handles common parcel-courier protocol; Econt overrides only what's Econt-specific (pallet, COD account validation, office/locker types, the [[econt-waybill-recipient-mapping|recipient-name billing override]]).

### Office vs locker vs address

The integration distinguishes **Econtomat lockers** from regular Econt offices. This affects whether the customer's pickup point is a courier office (with staff hours) vs an Econtomat (24/7 self-service). The two have different limits (above).

## Related

- [[apps-econt]] — hub.
- [[econt-addresses-tab]] — where the merchant marks ONE address as Default; that selection drives every waybill's sender.
- [[econt-settings-tab]] — `officesCountries` multi-select is where the merchant restricts which BG / RO countries Econt offices show up for (subject to the BG + RO coverage).
- [[econt-cod-insurance]] — 10000 BGN cap is BGN-store-specific (this page's currency rule explains why).
- [[econt-waybill-recipient-mapping]] — OmniShip falls through to shared code, with Econt-specific overrides for B2B name mapping.
- [[orders-shipping-waybill]] — waybill flow consumes the sender-default + multi-country coverage.

## Open questions

None.
