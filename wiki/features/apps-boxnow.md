---
type: feature
nav_path: "Apps → BoxNow"
route_name: apps.boxnow.overview
route_path: /admin/shipping/boxnow
aliases: ["BoxNow", "Box Now", "BoxNow locker", "Locker delivery", "Activate cash on delivery", "Активиране на наложен платеж", "lockers not showing at checkout", "локърите не се показват", "BoxNow not appearing at checkout", "why must COD be enabled for lockers"]
tags: [apps, shipping, locker, multi-country, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 4
---
# BoxNow (locker shipping)

## Purpose

**BoxNow** is a **locker-only** delivery network operating across multiple countries (Bulgaria, Romania, Greece, Cyprus, Croatia, and others). Unlike traditional couriers ([[apps-econt|Econt]], [[apps-dpdbulgaria-speedy|Speedy]]), BoxNow does NOT deliver to home addresses — packages are deposited in self-service lockers at convenient locations (gas stations, shops, residential complexes), and the customer picks up using a code BoxNow sends by SMS.

Through the platform, BoxNow handles locker selection at checkout (the customer picks a specific locker), waybill generation, and parcel tracking. The integration uses the OmniShip abstraction with provider-specific behaviour for the locker-only flow. A defining UX trait: in [[orders-address-edit]] the "To address" shipping method is **hidden** for BoxNow — only "To locker" is offered.
## Where to find it

Sidebar → **Apps** → install → **BoxNow**, or via direct routes. Four sub-pages, no Addresses tab (the locker network is BoxNow-side) and no Payments tab (see Business rules):

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.boxnow.overview` |
| Settings | `apps.boxnow.settings` |
| Shipments | `apps.boxnow.shipments` |
| Shipments return | `apps.boxnow.shipments-return` |

## What the merchant can do here

- **Configure credentials** and connect to BoxNow's API (Settings).
- **Pick a pricing model** and rate card (locker channel only).
- **Choose the sender pickup point** from BoxNow's API list.
- **Generate waybills** (creates the BoxNow shipment, returns a tracking number).
- **Print labels** in bulk (A4 / A6).
- **Issue return shipments** via the Shipments return sub-page (merchant-initiated; the customer drops the parcel in a BoxNow locker).

The merchant **cannot**: deliver to home addresses (locker-only by design); use BoxNow without an active contract in the operation country; override locker availability (if the chosen locker is full, BoxNow may reject — pick another); or use a live price calculator (BoxNow's API does not return live quotes).

## Settings & fields

The Settings page uses the shared shipping form with BoxNow-specific boxes:

**1. Credentials** (`CourierCredentialsSection.vue`) — all three issued by BoxNow on contract signing, all required for every API call:
- **Client ID** (`client_id`).
- **Client secret** (`client_secret`) — stored encrypted; displayed as a plain input in this Vue (not UI-masked).
- **Partner ID** (`partner_id`).

A **Connect** button validates the credentials against BoxNow's API; "Invalid credentials" shows inline on failure.

**2. Name & logo** (Visualization). **3. Sender data** (`SenderDataSection.vue`) — three fields only (BoxNow does not expose a full sender address; the pickup point comes from its API): **Sender name** (`sender_name`), **Sender Phone** (`sender_phone`), **Sender Email** (`sender_email`).

**4–5. Services / rate cards** — BoxNow supports only the **locker** channel, so a single rate card. **6. Geo zones** + **7. Payment providers** — standard.

**Pricing models** — pick ONE (there is NO calculator mode, so no `calculator` / `calculator_fixed` / `free` and no fallback-price table — the rate table is the price):
- **Fixed price without BOX NOW calculator** (`fixed_price`) — flat tier per order subtotal.
- **Fixed weight value without BOX NOW calculator** (`fixed_weight`) — flat tier per weight.
- **Fixed value by price and weight without BOX NOW calculator** (`price_and_weight`) — combined matrix.

Each model also exposes a **per-category** sub-table for charging chosen categories differently. The shared field-by-type reference is on [[shipping-calc-rate-card-fields]].

> **Rate-table rule (avoids a common false diagnosis):** in the from/to rate table, an **empty upper bound (`до` / `to`) means NO upper limit — the bracket runs to infinity**, and both bounds are inclusive. A single row with a blank `до` is the correct, intended way to cover *every* weight/price; it does **not** make the row invalid and is **never** the reason BOX NOW fails to appear at checkout. A method is dropped only when **no row matches** — i.e. the cart value is below the lowest `from`. See [[shipping-calc-rate-models]] for the full lookup arithmetic.

**Package types** picked when generating a waybill: **Small** / **Medium** / **Large**.

**8. Additional settings** — two backend-driven `SettingsBox` panels:

- Box 1 `general_settings` (inline edit): **Choose a content description** (`order_content` — Product name / SKU / barcode), **Enable cash on delivery** (`cd` — switch), **Default weight for one item** (`default_weight`).
- Box 2 `return_settings` (inline edit, BoxNow-specific): **Allow return of shipment** (`allowReturn` — switch). When `allowReturn = 1`, six fields appear — **Name** (`name`, required), **Select country** (`country`, from the platform country list), **Postal code** (`postalCode`), **Address** (`addressLine1`), **Additional address information** (`addressLine2`), **Note** (`note`). This defines where returned parcels are picked up from — distinct from the sender pickup point.

**9. Submit-changes** sticky footer.

## Business rules

- **Locker-only design.** BoxNow does not operate home delivery, so the "To address" radio is hidden in [[orders-address-edit]] for both merchant and customer — only a locker can be selected.
- **No platform-side country restrictions.** Which markets a merchant ships to is decided entirely by their BoxNow contract plus what the lockers API returns — not by CloudCart. Cross-border (e.g. a BG merchant shipping to a RO customer) follows the same rule. BoxNow does not expose detailed city/country APIs; locker selection is via the lockers API.
- **Locker selection at checkout.** When the customer picks BoxNow, the storefront calls the lockers API, returns nearby lockers with availability indicators, the customer picks one, and the locker data (ID, address, operating hours) is stored on the order.
- **Locker capacity is real-time.** If a chosen locker fills before the waybill is generated, BoxNow's API may reject at generation time — the merchant picks a different locker or asks the customer to re-choose.
- **Default sender pays** for the shipment; can be overridden per shipment if the contract allows. Each merchant typically has one configured pickup location — no automatic rotation between senders.
- **Open-before-pay requires the SENDER to pay.** Per the in-app help text: *"The option 'Open before paying' can only be used if the payer of the shipment is the SENDER"* — if the customer is set to pay (typical for COD), Open-before-pay is silently disabled.
- **Default weight 100 g.** When a product has no weight, 100 g is used as a fallback — light enough not to inflate cost, heavy enough to qualify for most locker tiers.
- **COD is contract-driven**, gated by three checks: (1) the OmniShip base check (BoxNow's contract allows COD), (2) the merchant's COD-enabled flag (`cd`) is true, (3) the order's COD amount is within BoxNow's market-specific server-side limit. The platform cap is **10000 BGN** per order, but only when the store currency is the literal `BGN` (legacy) — a store on `EUR` (the new Bulgarian norm) gets no platform cap, only BoxNow's server-side limit. The merchant can lower it with a per-courier cap setting. Above the cap, COD is silently hidden. When COD is supported and the order uses a non-default currency, the COD amount is converted to the destination currency at waybill generation.
- **Shipping recalculation on payment-method change** is supported only when COD is supported (switching off COD removes the COD fee).
- **No Payments tab.** Unlike Econt / Speedy, BoxNow's Settings mounts no Payments sub-page in the modern Vue — visibility is controlled by the integration's `supports.cod_payment` flag, which is false when BoxNow's market does not enable COD.
- **COD support is gated by BoxNow's own "Activate cash on delivery" (`cd`) toggle.** BoxNow accepts COD only when **"Активиране на наложен платеж" / "Enable cash on delivery" (`cd`) is ON** (Apps → BoxNow → Settings → *general settings*, inline edit) and the order is within the COD cap. A store whose only active payment method is Cash on delivery shows only COD-capable shipping methods at checkout (see [[shipping-calc-cascade]] → Step 6 special case), so in that case BoxNow with its `cd` toggle off does not appear — its locker selector included. Not BoxNow-specific: every courier has the same `cd` toggle (see [[shipping-provider-mech-cod]]); BoxNow is just the most visible because it is locker-only.
- **Side effects.** Saving settings validates credentials against BoxNow's API; waybill generation calls the API to create the shipment record (returns a tracking number; BoxNow then SMSes the customer's pickup code). Standard apps permission scope applies.

## Related

- [[apps]] — App Store hub.
- [[shipping]] — shipping providers landing.
- [[orders-shipping-waybill]] — per-order waybill flow (BoxNow's locker-only specifics).
- [[orders-address-edit]] — shipping method picker (BoxNow hides "To address").
- [[apps-econt]] — sister Bulgarian courier (home + office + Econtomat).
- [[apps-dpdbulgaria-speedy|Speedy]] — sister Bulgarian courier; Speedy Box lockers are one of several options (not locker-only).
- [[settings-payment-providers]] — COD configuration.
- [[settings-geo-zones]] — geo-zone filtering (BoxNow available only in served countries).
- [[orders-sync-cod]] — COD sync (when supported).

## Open questions

None.
