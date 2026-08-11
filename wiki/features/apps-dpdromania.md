---
type: feature
nav_path: "Apps → DPD Romania"
route_name: apps.dpdromania.overview
route_path: /admin/shipping/dpdromania
aliases: ["DPD Romania", "DPD RO", "DPD Romania courier"]
tags: [apps, shipping, courier, romania, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-23
source_count: 5
---
# DPD Romania

## Purpose

**DPD Romania** integration — DPD's Romanian operating company. Same Geopost network family as [[apps-dpdbulgaria-speedy]] but with separate credentials, separate contract, and Romanian-specific service tiers. Romanian merchants use it alongside [[apps-sameday]] and [[apps-cargus]] for diversified courier options.

## Where to find it

Sidebar → Apps → install → **DPD Romania** OR direct routes.

Standard OmniShip sub-pages.

## What the merchant can do here

### Settings

| Field | Notes |
|-------|-------|
| **Username** | DPD Romania API username. |
| **Password** | DPD Romania API password. |

Same simple credentials pattern as DPD Bulgaria. A `client_id` field is also stored in settings (used internally when calling DPD's API) but the merchant-visible login uses just username + password.

> **These are NOT the merchant's DPD website login.** The Username + Password entered here are dedicated **API / integration credentials** issued by DPD Romania for connecting external platforms — they are different from the login the merchant uses for DPD's own website / client portal. A merchant who doesn't have the integration credentials should **call DPD Romania and request the API credentials** for the CloudCart integration.

### PDF waybill support

DPD's API returns the waybill PDF directly (no separate rendering step on CloudCart side). When the merchant clicks "Print waybill" on an order the platform fetches DPD's PDF on demand and opens it in a new tab. This is a more streamlined waybill experience than couriers that require CloudCart-rendered PDFs.

### What the merchant CANNOT do here
- Use DPD Romania without contract.
- Mix DPD Romania credentials with DPD Bulgaria — each is a SEPARATE integration.

## Settings & fields

Standard credentials. The PDF support is a notable differentiator.

## Business rules

### RON-quoted

For DPD Romania, quotes are returned in **RON** (Romanian Leu), matching the local currency. (Compare [[apps-dpdbulgaria-speedy]] which quotes in EUR.)

### Native PDF waybill

The merchant clicks "Download PDF" on a fulfilled order and gets DPD's official PDF (not a CloudCart-rendered version). This is the format DPD's couriers expect to scan at pickup.

### Same OmniShip pattern

Real-time quotes → bill-of-lading → tracking. The PDF flow is the only meaningful UX difference vs other couriers.

### COD support

DPD Romania supports cash-on-delivery (subject to the merchant's `cd` setting + amount cap).

## Per-channel delivery pricing

DPD Romania delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time DPD Romania quote; **no extra field** of its own.
- `calculator_fixed` — the DPD Romania quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the DPD Romania quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote. It also adds **Free Delivery Service within the City**, **Intercity**, and **International** selects that pick which DPD Romania service fulfils the free leg.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-dpdbulgaria-speedy]] — sister DPD operating company in Bulgaria.
- [[apps-sameday]] / [[apps-cargus]] — alternative Romanian couriers.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow with PDF support.
- [[orders-sync-cod]] — COD sync.

## How it works (verified against backend)

### Romania-ONLY

The fallback allowed countries list is `['RO']` — DPD Romania is strictly Romanian. Different from DPD Bulgaria which covers BG + RO. **Answers the cross-border question**: a Romanian merchant using DPD Romania CANNOT ship to BG / HU via this integration — they'd need DPD's local equivalent in destination country OR DPD Bulgaria from BG.

### Same 3-channel + 2-credential + receiver-pays default as DPD Bulgaria

Same architectural shape as [[apps-dpdbulgaria-speedy]]: three delivery channels (address, office, locker), 2 credential fields (Username + Password), and a receiver-pays default. DPD operates two separate corporate entities (one per country) with separate APIs, but the CloudCart wrapper unifies the surface.

### PDF download is on-demand

Clicking "Print waybill" on an order opens DPD Romania's print modal/selector. The PDF is fetched on demand each time (re-call to DPD's API), so the link doesn't carry an expiry concept — re-clicking always pulls a fresh PDF.

### Romania-only — customs is N/A for EU destinations

DPD Romania is strictly Romanian-domestic. For Romanian merchants shipping within Romania (or to other EU countries via a different DPD entity), customs paperwork is NOT needed. DPD Romania's integration doesn't handle non-EU customs — that would be DHL Express territory.

### Print waybill: A4 or A6 format selector

When the merchant clicks the print button on the order, a modal opens with two paper-format options (A4 or A6). Picking one opens the PDF in a new tab. If the shipment is a return-voucher, the modal also exposes the return-voucher PDF in both A4 and A6 formats.

### Pickup points from DPD's office API

The customer's pickup-point picker at checkout (and the merchant's per-order pickup-point selector) populates from DPD Romania's office API. The list refreshes on a 1-day cache (OmniShip-family default). The merchant doesn't curate the list — DPD's API drives it.

## Settings tab — full layout (deep audit 2026-05-27)

### 1. Credentials box
- **Username** + **Password** — required.
- **Renew client information** button (when valid session) — refreshes DPD's client/contract metadata via `GET /admin/api/dpdromania/refresh-client`.

### 2. Name & logo (Visualization)

### 3. Sender data box — slide-down editor (`SenderDataSection.vue`)
- **Pickup** radio (required):
  - Client's address
  - Office
  - (Automat — commented-out in code; not exposed for RO. DPD Romania does NOT offer APS lockers in this integration.)
- **Client** (`address_id`) — async-search select against the DPD RO client list. Required.
- **Full name** (`client_name`) — required.
- **Phone number** (`client_phone`) — required.
- **Select DPD location** (`office_id`) — async-search against `/admin/api/dpdromania/offices`; ONLY when pickup = office. Required.

Pickup keys: `client_name`, `address_id`, `office_id`, `client_phone`.

### 4. Services / 5. Per-channel rate cards
Same as DPD Bulgaria — three channels (address / office / locker). Per-channel `SettingsModal` with:
- Pricing-type select.
- Office/Locker country picker (`/admin/api/dpdromania/countries`).
- Free-shipping service pickers (city / intercity / international tags).

### 6. Geo zones / 7. Payment providers — standard.

### 8. Additional settings — three boxes
SAME structure as DPD Bulgaria (the trait is mirrored), with these RO-specific differences:
- The COD contract checks (`codFiscalReceiptAllowed`, `moneyTransferAllowed`) are read from the DPD RO contract API instead of DPD BG.
- **Print paper size** (`speedy_print_size`) — All / A4 / A6.

Box 1 = `parcel_and_waybill_settings` (rendered first):
- side, payer_id, cd, cod_ref2, fiscal_receipt (contract-gated), pos_enabled, money_transfer (contract-gated), declared_value, fragile, back_documents, back_receipt, documents, sync_payments (plan-gated).

Box 2 = `general_settings`:
- default_weight (required), default_width/depth/height (mm), packing (required), order_content, item_sizes, boxes (multi-select), speedy_print_size.

Box 3 = additional pickup/services box (same shape as DPD BG).

### 9. Submit-changes sticky footer.

## Shipments / Shipments return tabs

`Shipments.vue` shared. Bulk-print obeys `speedy_print_size`:
- If `ALL`, opens **Print Format Select modal**: two big buttons — **A4** | **A6**. Picking one POSTs to `/admin/api/labels` with the type, opens the PDF blob in a new tab.
- For a return-voucher shipment, the same A4/A6 picker is presented but the resulting PDF is DPD's return-voucher label.

## Overview / Payments tabs — standard.

## Open questions
