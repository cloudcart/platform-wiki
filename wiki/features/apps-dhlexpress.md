---
type: feature
nav_path: "Apps → DHL Express"
route_name: apps.dhlexpress.overview
route_path: /admin/shipping/dhlexpress
aliases: ["DHL Express", "DHL Time Definite", "DHL premium"]
tags: [apps, shipping, courier, international, premium, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 6
---
# DHL Express (premium international)

## Purpose

**DHL Express** integration — DHL's premium time-definite service for urgent international shipments (next-day or 2-day delivery worldwide). Used for high-value, time-critical packages where the standard [[apps-dhl]] would be too slow. Pricing is significantly higher; service is significantly faster.

## Where to find it

Sidebar → Apps → install → **DHL Express** OR direct routes. Standard OmniShip sub-pages.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- View generated waybills / shipments in the Shipments sub-page.
- Manage returns in the Shipments return sub-page.
- See real-time quotes at checkout once credentials are validated.

### What the merchant CANNOT do here
- Use the integration without an active courier contract + valid API credentials.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

Four required fields:

| Field | Notes |
|-------|-------|
| **Username** | DHL Express API username. |
| **Password** | DHL Express API password. |
| **Account number** | DHL Express account (single — vs DHL standard's 3 accounts). |
| **Mode** | Test / Production mode toggle. |

Simpler than DHL standard — single account number, no separate billing/duty accounts (DHL Express handles those internally).

## Business rules

### Premium pricing

DHL Express rates are typically 3-5x DHL standard. The merchant should configure the storefront to either:
- Surcharge customers (passing the premium to the buyer).
- Absorb the cost (offering free express shipping over a threshold).
- Hide DHL Express unless the customer explicitly requests it.

### Worldwide coverage

DHL Express delivers to 220+ countries. Excellent for global merchants.

### Customs handled by DHL Express

Unlike standard DHL where the merchant configures duty accounts, DHL Express bundles customs handling into the service (DDP is more common).

### Test mode for staging

The Mode field lets the merchant switch to DHL's sandbox API — useful for development and staff training.

## Per-channel delivery pricing

DHL Express delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time DHL Express quote; **no extra field** of its own.
- `calculator_fixed` — the DHL Express quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the DHL Express quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-dhl]] — standard DHL Parcel (cheaper, slower).
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## How it works (verified against backend)

### Address-only

Supported delivery channels are `['address']` — door-to-door only. No locker / office options.

### No hardcoded country list

The fallback allowed countries list is empty — DHL Express's worldwide coverage is reflected in NO platform-side country restrictions. The DHL Express API decides what destinations are quotable.

### Mode toggle (sandbox vs production)

Required credentials are Username, Password, Account number, and Mode — the **Mode** field is a first-class credential. The merchant flips it between sandbox and production for staging vs live use.

### COD supported with cap

COD support is gated by the merchant's COD toggle + COD-amount cap. For BGN stores, 10000 BGN; for non-BGN no platform cap.

### Insurance requires COD-band check

Insurance is offered ONLY when the order is also within the COD cap (in addition to the merchant's insurance toggle being on). Same combined check as Econt / Speedy.

### No auto-hide based on order value

DHL Express options always appear when the integration is installed and the destination is quotable. There is no platform-side rule that hides Express for low-value orders — the merchant either accepts that customers see a high quote, or shapes visibility via storefront customisation / a different shipping method per geo-zone.

### Surcharges come from DHL's quote response

Remote-area surcharges, fuel surcharges, and other DHL Express fees are included in the price DHL returns. CloudCart shows the customer whatever DHL's API quotes; there's no separate per-zone fee table maintained in CloudCart.

### Customs documentation is DHL's responsibility

DHL Express bundles customs handling — the platform sends shipment data and DHL generates customs paperwork on its side. CloudCart does not pass HS codes (no such product field exists), so non-standard or restricted goods may require the merchant to add details via DHL's portal post-shipment.

## Settings page — full layout (shared OmniShip form, custom credentials + sender)

DHL Express uses `SettingsFormShippings` with TWO custom slots:

### Credentials card (custom `#credentials` slot)
Three required text fields:
- **Username** (`username`) — DHL Express API username.
- **Password** (`password`) — DHL Express API password.
- **Account number** (`account_number`) — DHL Express account.

Error indicator: shared "The data entered is invalid" message on each field when credential validation fails.

A `Connect` button validates against DHL's API; on success the card collapses to a read-only badge.

### Sender data card (custom `#senderData` slot)
The merchant maintains a default sender (used on every DHL Express waybill). Fields (all required unless noted):

| Field | Input | Required |
|-------|-------|----------|
| Country | Country picker (no-clear) | Yes |
| City | Text | Yes |
| Post code | Text | Yes |
| Street | Text | Yes |
| Street number | Text | Yes |
| --- | --- | --- |
| First name | Text | Yes |
| Last name | Text | Yes |
| Telephone number | Phone-format input | No (error if missing) |
| Company name | Text | Yes |
| VAT | Text | Optional |

Sections separated by a horizontal rule between the address block and the contact block.

### Remaining cards (shared layout)
- **Visualization** — name + logo upload for storefront/email display.
- **Service types** — per delivery channel (`address` only for DHL Express). Pencil icon opens the **Service-type calculator modal** (XL side modal) with the 6 pricing modes + rate rows + countries + categories — same shape as DHL.
- **Ships to (Geo Zones)** — geo-zone allow-list.
- **Payment providers** — payment method multi-select.
- **Additional Settings box** — COD toggle, insurance toggle, default weight, default product dimensions (mm), test/production mode (the `Mode` flag), etc.

## Open questions
