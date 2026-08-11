---
type: feature
nav_path: "Apps → DHL"
route_name: apps.dhl.overview
route_path: /admin/shipping/dhl
aliases: ["DHL", "DHL eCommerce", "DHL Parcel", "DHL courier"]
tags: [apps, shipping, courier, international, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 5
---
# DHL (international courier)

## Purpose

**DHL** integration — global parcel network with worldwide coverage. Used by CloudCart merchants for international shipments (especially outside the EU where domestic couriers don't deliver). DHL handles the customs documentation flow for non-EU destinations.

The DHL integration is the **standard** DHL Parcel / eCommerce flow (slower / cheaper than DHL Express). For premium time-critical shipments, see [[apps-dhlexpress]].

## Where to find it

Sidebar → Apps → install → **DHL** OR direct routes.

DHL exposes only TWO sub-pages (same lean router shape as GLS):

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.dhl.overview` | `/admin/shipping/dhl/` |
| Settings | `apps.dhl.settings` | `/admin/shipping/dhl/settings` |

No Payments tab, no Shipments tab, no Shipments-Return tab. Waybills DHL has generated appear in the global [[orders]] list filtered by shipping provider.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- See real-time quotes at checkout once credentials are validated.
- View / manage generated waybills from the global Orders list (not under the DHL app).

### What the merchant CANNOT do here
- Use the integration without an active courier contract + valid API credentials.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

DHL requires **5 credentials** (most complex of the OmniShip couriers):

| Field | Notes |
|-------|-------|
| **Username** | DHL API username. |
| **Password** | DHL API password. |
| **Shipper account number** | DHL account for outbound shipments. |
| **Billing account number** | DHL account billed for the shipping cost. |
| **Duty account number** | DHL account billed for any customs duties (non-EU destinations). |

The triple-account structure lets the merchant split who pays for what — shipper, billing, duty can be three different DHL accounts.

## Business rules

### Customs handling for non-EU

When shipping outside the EU, DHL requires HS codes, value declaration, commodity descriptions. The platform passes line-item data to DHL's API; DHL generates customs paperwork.

### Duty paid by recipient OR sender

The Duty account number config determines who pays — if a separate duty account is configured, the merchant pre-pays customs; otherwise, the recipient pays on delivery (DDU vs DDP shipping incoterms).

### Same OmniShip pattern

Standard real-time quotes → bill-of-lading → tracking flow. See [[orders-shipping-waybill]].

## Per-channel delivery pricing

DHL delivers to **address** and to **office** — each of its **2** delivery channels (to **address** and to **office**) is a separate rate card with its own enable toggle (`to_address` / `to_office`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time DHL quote; **no extra field** of its own.
- `calculator_fixed` — the DHL quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the DHL quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-dhlexpress]] — premium DHL Express tier.
- [[apps-gls]] / [[apps-dpdbulgaria-speedy]] — alternative European couriers.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## How it works (verified against backend)

### Address-only

Door-to-door only. No locker or pickup-point options through the DHL integration. (For non-EU shipments, the customer simply chooses DHL at checkout and the courier delivers to their address.)

### Default: sender pays

By default the merchant pays for DHL shipments. Different from couriers like Cargus / DPD where the customer pays. Aligned with international shipping practices.

### Insurance opt-in

Insurance is offered only when the merchant has enabled the Insurance toggle in Settings. No COD-cap dependency (unlike Speedy / Econt).

### Three account numbers for split billing

The merchant configures THREE separate DHL account numbers as credentials:
- **Shipper account** — identifies the merchant as the sender.
- **Billing account** — who's invoiced for the shipping cost.
- **Duty account** — who's invoiced for customs duties.

Different DHL accounts can fill each role — useful when the merchant has multiple DHL contracts (e.g., one for retail shipping, one for B2B duty pass-through).

### DDP vs DDU is set by which DHL accounts are configured

The merchant controls who pays customs duties via the **Duty account number** field in Settings:
- If a duty account is configured → DDP (merchant pre-pays duties).
- If not → DDU (recipient pays duties on delivery).

The choice is per-integration, not per-shipment — every order goes out under whatever the Settings dictate.

### Multi-country DHL handled through one set of credentials

The DHL integration has no country restriction — the same DHL credentials and account numbers are used for shipments anywhere DHL serves; DHL routes via its global network based on the recipient's address.

### Label size choice for printing

The merchant picks a label format on the Settings or per-waybill flow:
- 6×4 — A4 PDF / thermal
- 8×4 — A4 PDF / A4 TC PDF / CI PDF / CI thermal / thermal

The chosen format applies when downloading or printing the DHL label.

## Settings page — full layout (shared OmniShip form)

DHL uses the **shared `SettingsFormShippings` form** — same chrome as the other generic OmniShip couriers (single-section layout, no custom `senderData` slot). Sections appear in this order from top to bottom:

1. **Credentials card** — pencil icon toggles edit mode. Fields:
   - Username (text, required)
   - Password (text, required)
   - Shipper account number (text, required)
   - Billing account number (text, required)
   - Duty account number (text, optional — determines DDP vs DDU)

   A `Connect` button validates against DHL's API; on success the card collapses to a read-only summary and the rest of the page slides into view.

2. **Visualization card** — courier display name + logo upload (used in checkout + emails).

3. **Services / Service-types cards** — multi-select of DHL service tiers the merchant wants to expose (driven by what DHL's API returns for the contract). For each enabled delivery type (`to_address`), pencil icon opens the **Service-type calculator modal** (see below).

4. **Ships to (Geo Zones)** — geo-zone allow-list. Pickers from `geo_zones` input.

5. **Payment providers** — multi-select of payment methods. Toggle "Selected providers" / "All payment's".

6. **Additional Settings box** — generic OmniShip switches/dropdowns: COD toggle, insurance toggle, label size, default weight, default product dimensions, etc.

### Service-type calculator modal (XL)

Per service type (typically `address`), the merchant opens a side-modal with these tabs/sections:
- **Pricing model picker** — the 6 standard pricing modes (calculator, calculator + fee, calculator + free, fixed-price, fixed-weight, price+weight).
- **Rate rows** — only visible for fixed modes; weight-from / weight-to / price columns.
- **Allowed services** — sub-services within the picked DHL tier.
- **Available countries** — geo restriction for THIS rate row.
- **Categories** — restrict by product categories.

Save = persists the per-type pricing block to `dhl` settings.

### No per-product HS code field today

CloudCart's product model has no HS code / tariff code field. Customs paperwork for non-EU shipments is generated by DHL based on the shipment data the platform sends — without per-product HS codes, DHL falls back to its own default classifications or merchants must add HS codes via DHL's portal post-shipment.

## Open questions
