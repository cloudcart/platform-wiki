---
type: feature
nav_path: "Apps → EuShipment → (sub-courier) Settings → rate calculator"
route_name: apps.eushipment.external
route_path: /admin/shipping/eushipment/external/:id
aliases: ["EuShipment pricing", "EuShipment rate models", "EuShipment calculator", "EuShipment shipping cost", "EuShipment ценообразуване", "EuShipment калкулатор"]
tags: [apps, shipping, b2b, europe, omniship, aggregator, eushipment, pricing, checkout]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-eushipment]]. See the hub for the other aspects (credentials & sub-courier framework, sub-courier settings).

# EuShipment — pricing modes & checkout visibility

## Purpose

Each EuShipment sub-courier prices its delivery channels independently. For every enabled channel (Address / Office / Locker) the merchant opens a rate calculator and picks ONE of six pricing modes — either a live API quote from EuShipment or a flat rate table the merchant defines. This page documents the six modes, the calculator modal, and the rules that decide whether a sub-courier even appears at checkout (a common "the courier disappeared" support scenario).

## Where to find it

Sidebar → Apps → EuShipment → Settings → an installed courier's **Settings** → in the **Service-types** section, the pencil on any channel card opens the rate calculator modal (size `xll`, side-panel / hide-card variant). The chosen rate is saved back to the sub-courier and persisted via that page's sticky submit bar — see [[apps-eushipment-subcourier-settings]].

## What the merchant can do here

- Pick the pricing mode for this channel (one of six).
- Set a free-shipping threshold (free mode) or a processing-fee amount (calculator + fee mode).
- Build flat rate-row tables (by weight, by order price, or by both) for the fixed modes.
- Restrict to allowed EuShipment services, available countries, and product categories.

## Settings & fields

### The six pricing modes (per sub-courier, per channel)

Per the EuShipment lang strings, when configuring a per-courier rate the merchant picks ONE of:

| Mode | Behaviour |
|---|---|
| **euShipments calculator** | Automatic API-driven quote at checkout (live rates from EuShipment). |
| **euShipments calculator + processing fee** | API quote PLUS a fixed merchant processing fee added on top. |
| **euShipments calculator + free shipping** | API quote BUT zeroed out for the customer (merchant absorbs the cost). |
| **Fixed value at price without euShipments calculator** | Flat price tier per order subtotal (rate-row model). |
| **Fixed weight value without euShipments calculator** | Flat price tier per package weight. |
| **Fixed value for price and weight without euShipments calculator** | Combined price + weight matrix. |

These six modes mirror the standard CloudCart rate models (see [[shipping-calculation]]) but applied on a per-sub-courier, per-channel basis.

### Calculator modal fields

The shared calculator section exposes:

- **Pricing-mode select** (radio) — the six modes above.
- **Free-shipping threshold** — for the `free` mode.
- **Processing-fee input** — for the `calculator_fixed` (calculator + fee) mode.
- **Rate-rows table** — for the fixed modes (weight from / to → price; OR price from / to → price).
- **Allowed services** — multi-select from EuShipment's per-courier services.
- **Available countries** — multi-select.
- **Categories** — product-category restriction.

Save returns to the sub-courier settings page with the new rate applied to local state; the sticky submit bar then persists it.

## Business rules

### Live-quote modes vs flat-rate modes

The three "calculator" modes call EuShipment's API at checkout, so the customer sees EuShipment's current rate for the package weight + destination. The three "Fixed..." modes never call the API — the merchant's rate table decides the price. Choose flat-rate modes when API quotes are unreliable for the route or the merchant wants predictable shipping charges.

### Quote currency follows the store currency

Live API quotes are returned in the store's currency.

### "Free shipping" means the merchant absorbs the cost

The **calculator + free shipping** mode still gets a real quote from EuShipment (so the merchant is billed by the courier) but charges the customer 0 — the merchant eats the shipping cost. This is different from the flat-rate modes where a 0 row simply means free for that tier.

### COD-only payment + a courier without COD = the courier silently disappears at checkout

Per the lang alert: *"Attention, You have only one active payment method Cash on delivery — if the selected courier does not support this payment method or it is not activated for courier, when completing the order, the selected courier will not be displayed."*

This is a frequent debugging scenario: a customer doesn't see the EuShipment sub-courier at checkout because the merchant's ONLY payment method is COD AND that sub-courier doesn't support COD (or the merchant didn't enable COD on it). The fix is either to enable COD on the sub-courier (only possible if the contract permits — see the capability rule on [[apps-eushipment-credentials-couriers]]) or to add a non-COD payment method.

### Availability is driven by the API, not a hardcoded country list

The fallback allowed-countries list is empty — markets are determined by the merchant's EuShipment contract and the API's quote response, not by a platform country restriction. EuShipment supports all three delivery channels (`address`, `office`, `locker`) — door, office, and locker delivery.

## Related

- [[apps-eushipment]] — hub.
- [[shipping-calculation]] — the standard CloudCart rate models these six modes mirror.
- [[apps-eushipment-subcourier-settings]] — the sub-courier page that hosts the channel cards + calculator.
- [[orders-shipping-waybill]] — waybill flow once a rate is chosen at checkout.

## Open questions

None.
